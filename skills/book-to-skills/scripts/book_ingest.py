#!/usr/bin/env python3
"""Convert a book to page-anchored text segments plus a manifest.

Usage:
    book_ingest.py <book-file> [--out DIR] [--chunk-chars N] [--force]

Supports PDF (pdftotext), EPUB/MOBI/AZW3/FB2 (ebook-convert), and plain text/markdown.
Writes <out>/raw.txt, <out>/segments/seg-NNNN.md, <out>/manifest.json.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

EBOOK_EXTS = {".epub", ".mobi", ".azw3", ".azw", ".fb2", ".lit", ".pdb", ".rtf", ".docx"}
TEXT_EXTS = {".txt", ".md", ".markdown", ".text"}

HEADING_PATTERNS = [
    re.compile(r"^\s*(chapter|part|section|appendix|book)\s+([0-9]+|[ivxlcdm]+|[a-z]+)\b.*", re.I),
    re.compile(r"^\s*(#{1,3})\s+\S.*"),
    re.compile(r"^\s*\d{1,2}[.)]\s+[A-Z][^.]{3,70}$"),
]


def die(msg: str) -> None:
    sys.exit(f"book_ingest: {msg}")


def need(tool: str, why: str) -> str:
    path = shutil.which(tool)
    if not path:
        die(f"{why} requires `{tool}`, which is not installed.")
    return path


def run(cmd: list) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        die(f"command failed: {' '.join(cmd)}\n{proc.stderr.strip()[:800]}")


def extract_text(src: Path, out: Path) -> str:
    """Return raw text. PDFs keep form feeds so page numbers survive."""
    ext = src.suffix.lower()
    if ext == ".pdf":
        need("pdftotext", "PDF extraction")
        raw = out / "raw.txt"
        run(["pdftotext", "-layout", "-enc", "UTF-8", str(src), str(raw)])
        return raw.read_text(encoding="utf-8", errors="replace")
    if ext in EBOOK_EXTS:
        need("ebook-convert", f"{ext} extraction")
        tmp = out / "converted.txt"
        run(["ebook-convert", str(src), str(tmp), "--enable-heuristics"])
        return tmp.read_text(encoding="utf-8", errors="replace")
    if ext in TEXT_EXTS or ext == "":
        return src.read_text(encoding="utf-8", errors="replace")
    die(f"unsupported extension '{ext}'. Convert to PDF, EPUB, or TXT first.")


PSEUDO_PAGE_CHARS = 2500


def paginate(text: str) -> list:
    """Split into (page_number, page_text).

    Form feeds mean real page breaks (pdftotext) and page numbers are meaningful.
    Without them — most epub/txt conversions — fall back to paragraph-aligned pseudo-pages
    numbered 0, so segmentation still has a unit smaller than the whole book to work with.
    """
    if "\f" in text:
        return [(i + 1, p) for i, p in enumerate(text.split("\f"))]
    pages, buf, size = [], [], 0
    for para in text.split("\n\n"):
        buf.append(para)
        size += len(para) + 2
        if size >= PSEUDO_PAGE_CHARS:
            pages.append((0, "\n\n".join(buf)))
            buf, size = [], 0
    if buf:
        pages.append((0, "\n\n".join(buf)))
    return pages or [(0, text)]


def find_headings(page_text: str, page_no: int) -> list:
    found = []
    for line in page_text.splitlines():
        stripped = line.strip()
        if not (3 < len(stripped) < 90):
            continue
        for pat in HEADING_PATTERNS:
            if pat.match(stripped):
                found.append({"text": stripped, "page": page_no})
                break
        else:
            # ALL-CAPS standalone line, a common typeset chapter title
            letters = [c for c in stripped if c.isalpha()]
            if letters and all(c.isupper() for c in letters) and len(stripped.split()) <= 10:
                found.append({"text": stripped, "page": page_no})
    return found


def segment(pages: list, chunk_chars: int) -> list:
    """Group pages into segments of roughly chunk_chars, never splitting a page."""
    segments, buf, buf_len, first_page = [], [], 0, None
    for page_no, page_text in pages:
        if first_page is None:
            first_page = page_no
        buf.append((page_no, page_text))
        buf_len += len(page_text)
        if buf_len >= chunk_chars:
            segments.append((first_page, page_no, buf))
            buf, buf_len, first_page = [], 0, None
    if buf:
        segments.append((first_page, buf[-1][0], buf))
    return segments


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("book")
    ap.add_argument("--out", default=None, help="output dir (default: book-forge/<slug>/source)")
    ap.add_argument("--chunk-chars", type=int, default=24000, help="target chars per segment")
    ap.add_argument("--force", action="store_true", help="overwrite an existing output dir")
    args = ap.parse_args()

    src = Path(args.book).expanduser()
    if not src.is_file():
        die(f"no such file: {src}")

    slug = re.sub(r"[^a-z0-9]+", "-", src.stem.lower()).strip("-") or "book"
    out = Path(args.out) if args.out else Path("book-forge") / slug / "source"
    if out.exists() and any(out.iterdir()) and not args.force:
        die(f"{out} already exists and is not empty (use --force to overwrite)")
    (out / "segments").mkdir(parents=True, exist_ok=True)

    text = extract_text(src, out)
    if not text.strip():
        die("extraction produced no text (scanned images? try OCR first)")
    (out / "raw.txt").write_text(text, encoding="utf-8")

    pages = paginate(text)
    paged = pages[0][0] != 0
    segs = segment(pages, args.chunk_chars)

    manifest = {
        "source": str(src.resolve()),
        "slug": slug,
        "chars": len(text),
        "approx_words": len(text.split()),
        "pages": len(pages) if paged else None,
        "paginated": paged,
        "chunk_chars": args.chunk_chars,
        "segments": [],
        "headings": [],
    }

    for idx, (first, last, buf) in enumerate(segs, start=1):
        seg_id = f"seg-{idx:04d}"
        body = []
        for page_no, page_text in buf:
            if paged:
                body.append(f"\n<!-- p.{page_no} -->\n")
                manifest["headings"].extend(find_headings(page_text, page_no))
            else:
                manifest["headings"].extend(find_headings(page_text, 0))
            body.append(page_text)
        span = f"p.{first}-{last}" if paged else "unpaginated"
        content = f"<!-- {seg_id} | {span} | source: {src.name} -->\n" + "".join(body)
        (out / "segments" / f"{seg_id}.md").write_text(content, encoding="utf-8")
        manifest["segments"].append({
            "id": seg_id,
            "path": f"segments/{seg_id}.md",
            "page_start": first if paged else None,
            "page_end": last if paged else None,
            "chars": len(content),
        })

    # de-duplicate headings, keep order
    seen, uniq = set(), []
    for h in manifest["headings"]:
        key = h["text"].lower()
        if key not in seen:
            seen.add(key)
            uniq.append(h)
    manifest["headings"] = uniq

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"slug:      {slug}")
    print(f"out:       {out}")
    print(f"words:     {manifest['approx_words']:,}")
    print(f"pages:     {manifest['pages'] if paged else 'n/a (no page breaks)'}")
    print(f"segments:  {len(segs)}")
    print(f"headings:  {len(uniq)} detected (heuristic — verify against the real TOC)")
    print(f"\nNext: read {out}/manifest.json, then write map.md before harvesting.")


if __name__ == "__main__":
    main()
