#!/usr/bin/env bash
set -euo pipefail
base=https://platform.claude.com/docs/en/agents-and-tools/agent-skills
dir="$(cd "$(dirname "$0")/../references" && pwd)"
for page in overview best-practices; do
  tmp="$(mktemp)"
  curl -fsSL "$base/$page.md" -o "$tmp"
  head -1 "$tmp" | grep -q '^---$' || { echo "unexpected content for $page" >&2; rm -f "$tmp"; exit 1; }
  mv "$tmp" "$dir/$page.md"
  echo "updated $page.md ($(wc -c <"$dir/$page.md") bytes)"
done
