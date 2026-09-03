#!/usr/bin/env python3
"""Build a traceability matrix by scanning a perimeter for keyed markers.

Consolidation works like a GROUP BY: walk every file in the perimeter, extract
the markers, group the facts under the key they share, emit the aggregate.

Two properties matter more than the output format:

  * Elements inside the perimeter that carry no key are REPORTED, never
    skipped. A scan that silently ignores what it does not recognize hides
    exactly the gaps it was built to surface.
  * Nothing is stored. Re-run it; the artifacts stay authoritative.

Adapt the marker patterns to your own convention -- the defaults below are
examples, not a standard.

    python3 build_matrix.py --root src --tests tests --spec docs/spec.md \
        --since v1.2.0 --out matrix.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone

# --- Marker patterns -------------------------------------------------------
# Matched loosely on purpose: coupling the extractor to specific marker
# definitions welds it to them, so they can never move or be renamed.
DEFAULT_KEY = r"REQ-\d+"

MARKER_PATTERNS = [
    r"@Requirement\(\s*[\"']?({key})",       # annotation / decorator
    r"@covers\s+({key})",                     # docstring or comment tag
    r"\[\s*Requirement\(\s*[\"']?({key})",   # attribute syntax
    r"#\s*({key})\b",                         # bare comment marker
]

SUPPRESS_PATTERN = r"traceability[:-]\s*ignore"

TEXT_EXTENSIONS = {
    ".py", ".java", ".cs", ".ts", ".tsx", ".js", ".jsx", ".go", ".rb",
    ".kt", ".scala", ".rs", ".php", ".c", ".h", ".cpp", ".hpp", ".md",
    ".feature", ".yaml", ".yml", ".sql",
}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
             "dist", "build", "target", ".idea", ".tox"}


def compile_patterns(key_regex):
    return [re.compile(p.format(key=key_regex)) for p in MARKER_PATTERNS]


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1] in TEXT_EXTENSIONS:
                yield os.path.join(dirpath, name)


def scan(root, patterns, suppress_re, label):
    """Return (facts, unmatched, suppressed).

    facts: key -> set of file paths
    unmatched: files in the perimeter carrying no key and no suppression
    """
    facts = defaultdict(set)
    unmatched, suppressed = [], []
    if not root or not os.path.isdir(root):
        return facts, unmatched, suppressed

    for path in walk(root):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"warn: cannot read {path}: {exc}", file=sys.stderr)
            continue

        found = set()
        for pattern in patterns:
            found.update(m.group(1) for m in pattern.finditer(text))

        if found:
            for key in found:
                facts[key].add(path)
        elif suppress_re.search(text):
            suppressed.append(path)
        else:
            unmatched.append(path)

    print(f"scanned {label}: {len(facts)} keys, "
          f"{len(unmatched)} unmatched, {len(suppressed)} suppressed",
          file=sys.stderr)
    return facts, unmatched, suppressed


def scan_spec(spec_path, key_regex):
    """Map key -> spec section heading. Sections are markdown headings."""
    sections = defaultdict(set)
    if not spec_path or not os.path.isfile(spec_path):
        return sections
    key_re = re.compile(key_regex)
    heading = "(top)"
    with open(spec_path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                heading = line.lstrip("#").strip()
            for key in key_re.findall(line):
                sections[key].add(heading)
    return sections


def scan_commits(since, key_regex):
    """Map key -> commit shorthashes. Reads history, the authoritative source."""
    commits = defaultdict(set)
    rev = f"{since}..HEAD" if since else "HEAD"
    try:
        out = subprocess.run(
            ["git", "log", rev, "--pretty=format:%h%x1f%s%x1f%b%x1e"],
            capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"warn: no commit data ({exc}); commit column will be empty",
              file=sys.stderr)
        return commits
    key_re = re.compile(key_regex)
    for record in out.split("\x1e"):
        if not record.strip():
            continue
        parts = record.strip().split("\x1f")
        sha, message = parts[0], " ".join(parts[1:])
        for key in key_re.findall(message):
            commits[key].add(sha)
    return commits


def rel(paths, root):
    return sorted(os.path.relpath(p, root) if root else p for p in paths)


def render(keys, spec, components, tests, commits, unmatched, meta):
    lines = [f"# Traceability matrix — {meta['scope']}", ""]
    lines.append(f"Generated: {meta['generated']}  ")
    lines.append(f"Source commit: {meta['commit']}  ")
    lines.append(f"Perimeter: {meta['perimeter']}")
    lines += ["", "| REQ-ID | Spec section | Components | Tests | Commits |",
              "|---|---|---|---|---|"]

    for key in keys:
        lines.append("| {} | {} | {} | {} | {} |".format(
            key,
            "; ".join(sorted(spec.get(key, []))) or "**—**",
            "<br>".join(rel(components.get(key, []), meta["root"])) or "**—**",
            "<br>".join(rel(tests.get(key, []), meta["tests_root"])) or "**—**",
            " ".join(sorted(commits.get(key, []))) or "—",
        ))

    lines += ["", "## Unmatched elements", ""]
    if unmatched:
        lines.append("Files inside the perimeter carrying no requirement key. "
                     "Each is either a genuine gap or should be explicitly "
                     "suppressed — silence is not an option here.")
        lines.append("")
        for path in unmatched:
            lines.append(f"- `{path}`")
    else:
        lines.append("None — every file in the perimeter carries a key or an "
                     "explicit suppression.")

    lines += ["", "## What this matrix cannot see", "",
              "- **Uncovered mechanisms.** Links created by any route this scan "
              "does not walk are simply absent.",
              "- **Shared-state coupling.** Relationships neither side declares "
              "— another system reading this database directly — are "
              "undetectable from the artifacts.",
              "- **Declared versus exercised.** This shows links present in the "
              "artifacts, not which are exercised in production.",
              ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="component perimeter to scan")
    ap.add_argument("--tests", help="test perimeter to scan")
    ap.add_argument("--spec", help="specification file to map sections from")
    ap.add_argument("--since", help="tag or ref to read commits from")
    ap.add_argument("--key", default=DEFAULT_KEY, help="identifier regex")
    ap.add_argument("--scope", default="all", help="name for this view")
    ap.add_argument("--out", help="output file (default: stdout)")
    ap.add_argument("--json", help="also write the raw aggregate as JSON")
    args = ap.parse_args()

    patterns = compile_patterns(args.key)
    suppress_re = re.compile(SUPPRESS_PATTERN, re.I)

    components, unmatched, _ = scan(args.root, patterns, suppress_re, "components")
    tests, test_unmatched, _ = scan(args.tests, patterns, suppress_re, "tests")
    spec = scan_spec(args.spec, args.key)
    commits = scan_commits(args.since, args.key)

    keys = sorted(set(components) | set(tests) | set(spec) | set(commits))
    if not keys:
        print("no requirement keys found — check --key and --root",
              file=sys.stderr)

    try:
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:
        head = "unknown"

    meta = {
        "scope": args.scope,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit": head,
        "perimeter": f"{args.root}" + (f", {args.tests}" if args.tests else ""),
        "root": args.root,
        "tests_root": args.tests,
    }

    doc = render(keys, spec, components, tests, commits,
                 unmatched + test_unmatched, meta)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(doc)

    if args.json:
        aggregate = {
            "meta": meta,
            "keys": {k: {"spec": sorted(spec.get(k, [])),
                         "components": rel(components.get(k, []), args.root),
                         "tests": rel(tests.get(k, []), args.tests),
                         "commits": sorted(commits.get(k, []))}
                     for k in keys},
            "unmatched": unmatched + test_unmatched,
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(aggregate, fh, indent=2)
        print(f"wrote {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()
