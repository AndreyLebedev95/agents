#!/usr/bin/env python3
"""Inspect a vendor's next-page token and report what it leaks.

A correctly built page token is encrypted, not merely encoded, so that consumers
cannot see or depend on its contents. If a token decodes into something readable,
the vendor is almost certainly doing offset- or cursor-based paging behind an
opaque-looking wrapper, and the consumer inherits those bugs:

  offset paging  -> concurrent inserts make you re-read records; deletes make
                    you skip them, both silently
  cursor paging  -> avoids the shifting-window bug but still gives no
                    point-in-time consistency

Usage:
    python3 inspect_page_token.py <token> [<token2> ...]
    python3 inspect_page_token.py --compare <token1> <token2>

--compare takes two consecutive tokens from the same walk and reports what
changed between them, which usually reveals the paging scheme even when a single
token is ambiguous.
"""
import base64
import binascii
import json
import math
import re
import sys
from collections import Counter


def _try_decode(tok):
    """Yield (label, bytes) for each decoding that produces plausible output."""
    variants = []
    padded = tok + "=" * (-len(tok) % 4)
    for label, fn in (
        ("base64", base64.b64decode),
        ("base64url", base64.urlsafe_b64decode),
        ("base32", base64.b32decode),
    ):
        try:
            raw = fn(padded)
        except (binascii.Error, ValueError):
            continue
        if raw:
            variants.append((label, raw))
    try:
        if re.fullmatch(r"[0-9a-fA-F]+", tok) and len(tok) % 2 == 0:
            variants.append(("hex", bytes.fromhex(tok)))
    except ValueError:
        pass
    return variants


def _shannon_entropy(raw):
    if not raw:
        return 0.0
    counts = Counter(raw)
    n = len(raw)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def _printable_ratio(raw):
    if not raw:
        return 0.0
    return sum(1 for b in raw if 32 <= b < 127) / len(raw)


OFFSET_HINTS = [
    (r'"?offset"?\s*[:=]', "an explicit offset field"),
    (r'"?page(_?num(ber)?)?"?\s*[:=]', "a page number"),
    (r'"?skip"?\s*[:=]', "a skip count"),
    (r'"?start(_?index|_?at|_?row)?"?\s*[:=]', "a start index"),
    (r'"?limit"?\s*[:=]', "a limit"),
    (r'"?(last|after)_?(seen|id|key|sort)?"?\s*[:=]', "a last-seen cursor"),
    (r'"?(created|updated|modified)_?(at|time|on)"?\s*[:=]', "a timestamp cursor"),
]


def analyse(tok):
    print(f"\n{'=' * 68}\ntoken: {tok[:60]}{'...' if len(tok) > 60 else ''}")
    print(f"length: {len(tok)}")

    variants = _try_decode(tok)
    if not variants:
        print("verdict: does not decode as base64/base32/hex.")
        print("         Treat as opaque, but confirm with --compare on two")
        print("         consecutive tokens before trusting it.")
        return

    revealed = False
    for label, raw in variants:
        ratio = _printable_ratio(raw)
        entropy = _shannon_entropy(raw)
        if ratio < 0.75:
            continue
        text = raw.decode("utf-8", errors="replace")
        print(f"\n  decodes as {label} -> printable ({ratio:.0%} printable, "
              f"entropy {entropy:.2f} bits/byte)")
        print(f"  content: {text[:300]}")

        try:
            parsed = json.loads(text)
            print(f"  valid JSON: {json.dumps(parsed, indent=2)[:400]}")
        except (json.JSONDecodeError, ValueError):
            pass

        for pattern, human in OFFSET_HINTS:
            if re.search(pattern, text, re.I):
                print(f"  !! contains {human}")
                revealed = True
        revealed = True

    if revealed:
        print("\nverdict: NOT OPAQUE. The token's structure is visible, so this is")
        print("         offset- or cursor-based paging. Assume the walk can skip and")
        print("         duplicate records if the collection changes underneath it.")
        print("         Plan: chunk by a stable filter, checkpoint by business key,")
        print("         and reconcile independently of the vendor's totals.")
    else:
        print("\nverdict: decodes, but the payload looks binary/encrypted.")
        print("         Probably genuinely opaque. Note that opaque still does NOT")
        print("         mean point-in-time consistent - most page walks are a smear.")


def compare(a, b):
    print(f"{'=' * 68}\ncomparing two consecutive tokens")
    if len(a) != len(b):
        print(f"lengths differ ({len(a)} vs {len(b)}) - suggests an encoded payload")
        print("whose content grows, e.g. an embedded key or offset.")
    else:
        diff = sum(1 for x, y in zip(a, b) if x != y)
        print(f"same length ({len(a)}), {diff} differing characters "
              f"({diff / len(a):.0%})")
        if diff / len(a) < 0.25:
            print("!! Only a small part changes between pages. That is the signature")
            print("   of a counter or cursor embedded in an otherwise fixed wrapper,")
            print("   not of an encrypted token. Treat as offset/cursor paging.")
    for tok in (a, b):
        analyse(tok)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    if args[0] == "--compare":
        if len(args) != 3:
            print("--compare needs exactly two tokens")
            return 1
        compare(args[1], args[2])
        return 0
    for tok in args:
        analyse(tok)
    return 0


if __name__ == "__main__":
    sys.exit(main())
