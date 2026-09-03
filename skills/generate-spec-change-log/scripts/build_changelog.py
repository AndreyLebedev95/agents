#!/usr/bin/env python3
"""Generate a change-log skeleton from conventional commit history.

Produces the SKELETON, not the finished document. A person rewrites subjects
written for developers into subjects meant for readers, merges entries that
describe one user-visible change, and confirms every breaking change carries
its migration path. What they must not do is add what did not happen or drop
what did -- the generated output is the factual floor.

Off-convention commits are REPORTED, never dropped. A log that silently omits
whatever was committed off-convention looks complete and is not.

    python3 build_changelog.py --since v1.2.0 --version 1.3.0
    python3 build_changelog.py --since v1.2.0 --version 1.3.0 \
        --repo-url https://github.com/acme/widget --out CHANGELOG-1.3.0.md
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date

TYPES = {
    "feat": "New features",
    "fix": "Bug fixes",
    "docs": "Documentation",
    "style": "Formatting",
    "refactor": "Refactoring",
    "perf": "Performance",
    "test": "Tests",
    "chore": "Chores",
}

# Sections that appear in a published log, in order. Others are extracted but
# held back -- readers of release notes do not want the chore list.
PUBLISHED = ["Breaking changes", "New features", "Bug fixes"]

HEADER_RE = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]*)\))?(?P<bang>!)?:\s*(?P<subject>.+)$"
)
BREAKING_RE = re.compile(r"^breaking[ -]change:?\s*(?P<text>.*)", re.I | re.M)
ISSUE_RE = re.compile(r"(?:closes|fixes|resolves|refs)\s+#(\d+)", re.I)

SEP_FIELD, SEP_RECORD = "\x1f", "\x1e"


def read_commits(rev_range):
    fmt = SEP_FIELD.join(["%h", "%H", "%s", "%b"]) + SEP_RECORD
    try:
        out = subprocess.run(["git", "log", rev_range, f"--pretty=format:{fmt}"],
                             capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("git is not available")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"cannot read history for '{rev_range}': "
                 f"{exc.stderr.strip() or 'range does not resolve'}")

    commits = []
    for record in out.split(SEP_RECORD):
        if not record.strip():
            continue
        parts = record.strip("\n").split(SEP_FIELD)
        if len(parts) < 3:
            continue
        short, full, subject = parts[0], parts[1], parts[2]
        body = parts[3] if len(parts) > 3 else ""
        commits.append({"short": short, "full": full,
                        "subject": subject, "body": body})
    return commits


def classify(commits):
    """Return (grouped, off_convention, scopes_seen)."""
    grouped = defaultdict(list)
    off_convention, scopes = [], set()

    for commit in commits:
        match = HEADER_RE.match(commit["subject"])
        if not match:
            off_convention.append(commit)
            continue

        ctype = match.group("type")
        if ctype not in TYPES:
            off_convention.append(commit)
            continue

        if match.group("scope"):
            scopes.update(s.strip() for s in match.group("scope").split(","))

        entry = dict(commit,
                     text=match.group("subject").strip(),
                     scope=match.group("scope"),
                     issues=ISSUE_RE.findall(commit["body"]))

        breaking = BREAKING_RE.search(commit["body"])
        if breaking or match.group("bang"):
            note = breaking.group("text").strip() if breaking else ""
            grouped["Breaking changes"].append(
                dict(entry, breaking_note=note))
            # A breaking change can also be a feature; list it in both.
        grouped[TYPES[ctype]].append(entry)

    return grouped, off_convention, scopes


def link(repo_url, kind, ref):
    if not repo_url:
        return None
    base = repo_url.rstrip("/")
    return {"commit": f"{base}/commit/{ref}",
            "issue": f"{base}/issues/{ref}",
            "compare": f"{base}/compare/{ref}"}[kind]


def render_entry(entry, repo_url):
    line = f"- {entry['text']}"
    url = link(repo_url, "commit", entry["full"])
    line += f" ([{entry['short']}]({url}))" if url else f" ({entry['short']})"
    if entry["issues"]:
        refs = ", ".join(
            f"[#{i}]({link(repo_url, 'issue', i)})" if repo_url else f"#{i}"
            for i in entry["issues"])
        line += f", closes {refs}"
    if entry.get("breaking_note"):
        line += f"\n  - **Migration:** {entry['breaking_note']}"
    elif "breaking_note" in entry:
        line += ("\n  - **Migration: NOT STATED — a breaking change without a "
                 "migration path is incomplete; add it before publishing.**")
    return line


def render(grouped, off_convention, scopes, version, since, repo_url, total):
    heading = f"## {version} ({date.today().isoformat()})"
    if repo_url and since:
        compare = link(repo_url, "compare", f"{since}...{version}")
        heading += f"  \n[Compare with {since}]({compare})"
    lines = [heading, ""]

    for section in PUBLISHED:
        entries = grouped.get(section)
        if not entries:
            continue  # suppressed -- an empty heading trains readers to skip it
        lines += [f"### {section}", ""]
        lines += [render_entry(e, repo_url) for e in entries]
        lines.append("")

    if not any(grouped.get(s) for s in PUBLISHED):
        lines += ["_No user-visible changes in this range._", ""]

    # --- reviewer notes: never part of the published log ---------------
    lines += ["---", "", "## Reviewer notes — remove before publishing", ""]
    placed = sum(len(grouped.get(s, [])) for s in TYPES.values())
    lines.append(f"Commits in range: {total}. Placed: {placed}. "
                 f"Off-convention: {len(off_convention)}.")
    lines.append("")

    if off_convention:
        lines += ["**Off-convention commits — not placed in any section.** "
                  "These are reported rather than dropped: a log that silently "
                  "omits them looks complete and is not. Decide for each "
                  "whether it belongs in the log.", ""]
        for commit in off_convention:
            lines.append(f"- `{commit['short']}` {commit['subject']}")
        lines.append("")

    held = [s for s in TYPES.values()
            if s not in PUBLISHED and grouped.get(s)]
    if held:
        lines += ["**Extracted but held back from the published sections** "
                  "(present in the range, not usually wanted by readers of "
                  "release notes): "
                  + ", ".join(f"{s} ({len(grouped[s])})" for s in held), ""]

    if scopes:
        lines += [f"**Scopes seen in range:** {', '.join(sorted(scopes))}. "
                  "If a change in this release fits none of these, the scope "
                  "list has a coverage gap and that change is invisible to "
                  "every derived view.", ""]

    lines += ["**Before publishing:** rewrite subjects written for developers "
              "into subjects meant for readers; merge entries describing one "
              "user-visible change; confirm every breaking change states its "
              "migration path. Do not add what did not happen, and do not drop "
              "what did.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", help="previous tag or ref (default: whole history)")
    ap.add_argument("--version", required=True, help="version being released")
    ap.add_argument("--repo-url", help="base URL for commit and issue links")
    ap.add_argument("--out")
    args = ap.parse_args()

    rev_range = f"{args.since}..HEAD" if args.since else "HEAD"
    commits = read_commits(rev_range)
    if not commits:
        sys.exit(f"no commits in range '{rev_range}'")

    grouped, off_convention, scopes = classify(commits)

    adherence = 1 - len(off_convention) / len(commits)
    if adherence < 0.5:
        print(f"WARNING: only {adherence:.0%} of commits follow the "
              "convention. The generated log will under-report. Consider "
              "fixing the convention going forward and labelling this gap "
              "explicitly rather than publishing a log that looks complete.",
              file=sys.stderr)

    doc = render(grouped, off_convention, scopes, args.version,
                 args.since, args.repo_url, len(commits))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"wrote {args.out} — skeleton, needs review before publishing",
              file=sys.stderr)
    else:
        print(doc)


if __name__ == "__main__":
    main()
