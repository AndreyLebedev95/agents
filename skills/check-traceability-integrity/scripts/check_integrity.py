#!/usr/bin/env python3
"""Check a traceability chain for orphans and stale declarations.

Reads the JSON aggregate produced by build_matrix.py --json and compares the
declared relationships against the actual ones IN BOTH DIRECTIONS:

  * actual without declaration -- a component or test carrying no key, or
    citing a key that was never declared
  * declaration without actual -- a requirement whose components, tests or
    spec sections no longer exist

Running only the first direction is the usual reason a check gives false
comfort: it leaves declarations pointing at things that vanished, which is
exactly the orphan people worry about.

Canary preconditions run first. When one fails the substantive checks are not
run at all, because a substantive failure on moved ground reports something
misleading about the subject.

Exit status: 0 clean, 1 findings, 2 canary failure (nothing was checked).

    python3 check_integrity.py aggregate.json --stage "sprint 12 close"
    python3 check_integrity.py aggregate.json --require-tests --fail-on high
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Finding:
    def __init__(self, severity, title, link, detected_by, evidence, action):
        self.severity = severity
        self.title = title
        self.link = link
        self.detected_by = detected_by
        self.evidence = evidence
        self.action = action

    def render(self):
        ev = self.evidence
        if len(ev) > 12:
            ev = ev[:12] + [f"... and {len(self.evidence) - 12} more"]
        return "\n".join([
            f"### {self.severity.upper()} — {self.title}",
            f"Link:        {self.link}",
            f"Detected by: {self.detected_by}",
            "Evidence:",
            *(f"  - {e}" for e in ev),
            f"Action:      {self.action}",
            "",
        ])


def canaries(aggregate, path):
    """Verify the ground before checking the subject."""
    problems = []
    if not isinstance(aggregate, dict):
        problems.append(f"{path} is not a JSON object")
        return problems
    if "keys" not in aggregate:
        problems.append(f"{path} has no 'keys' section — was it produced by "
                        "build_matrix.py --json?")
        return problems
    if not aggregate["keys"]:
        problems.append("the aggregate contains no requirement keys at all — "
                        "check the identifier pattern and the perimeter, not "
                        "the requirements")
    meta = aggregate.get("meta", {})
    for field, label in (("root", "component perimeter"),
                         ("tests_root", "test perimeter")):
        value = meta.get(field)
        if value and not os.path.isdir(value):
            problems.append(f"{label} '{value}' does not exist — the aggregate "
                            "was built against a different tree")
    return problems


def check(aggregate, require_tests, require_commits):
    findings = []
    keys = aggregate["keys"]
    meta = aggregate.get("meta", {})

    # --- declaration without actual -----------------------------------
    def missing(field, label, severity, action):
        bad = sorted(k for k, v in keys.items() if not v.get(field))
        if bad:
            findings.append(Finding(
                severity,
                f"{len(bad)} requirement(s) with no {label}",
                f"REQ-ID -> {label}",
                f"declared-without-actual scan over '{field}'",
                bad, action))

    missing("spec", "spec section", "medium",
            "Either the requirement is specified nowhere and is not real, or "
            "the spec section is missing its key. Decide which; do not assume "
            "the second.")
    missing("components", "implementing component", "high",
            "Nothing implements this. Confirm it is genuinely unimplemented "
            "rather than implemented without a marker — the two look identical "
            "from here.")
    if require_tests:
        missing("tests", "test", "high",
                "Nothing verifies this requirement. Add coverage, or mark the "
                "requirement as deliberately unverified with a stated reason.")
    if require_commits:
        missing("commits", "commit in range", "low",
                "No commit in the range cited this requirement. Expected if it "
                "predates the range; otherwise the commit convention was not "
                "followed.")

    # --- stale declarations: referenced paths that no longer exist -----
    roots = {"components": meta.get("root"), "tests": meta.get("tests_root")}
    stale = []
    for key, entry in keys.items():
        for field, root in roots.items():
            for path in entry.get(field, []):
                full = os.path.join(root, path) if root else path
                if not os.path.exists(full):
                    stale.append(f"{key} -> {full} (declared, does not exist)")
    if stale:
        findings.append(Finding(
            "high", f"{len(stale)} declaration(s) pointing at missing artifacts",
            "REQ-ID -> artifact", "actual-existence scan over declarations",
            stale,
            "The artifact was renamed, moved or deleted without the link "
            "following. This is the failure mode the carrier choice was "
            "supposed to prevent — reconsider it, not just this instance."))

    # --- actual without declaration ------------------------------------
    unmatched = aggregate.get("unmatched", [])
    if unmatched:
        findings.append(Finding(
            "medium", f"{len(unmatched)} artifact(s) carrying no requirement key",
            "artifact -> REQ-ID", "unmatched-element report from the scan",
            unmatched,
            "Each is a genuine gap or should be explicitly suppressed. Silence "
            "is not an option: an unkeyed artifact is invisible to every "
            "derived view."))

    # --- fully orphaned: declared nowhere but the spec ------------------
    dangling = sorted(k for k, v in keys.items()
                      if not v.get("components") and not v.get("tests")
                      and not v.get("commits"))
    if dangling:
        findings.append(Finding(
            "high", f"{len(dangling)} requirement(s) with no trace at all",
            "REQ-ID -> everything", "full-chain absence scan", dangling,
            "These exist only in the specification. Either work has not "
            "started, or the chain broke completely. Confirm which before the "
            "next stage gate."))

    findings.sort(key=lambda f: SEVERITY_ORDER.get(f.severity, 3))
    return findings


def render(findings, canary_problems, stage, aggregate_path, not_checked):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = [f"# Traceability integrity — {stage}", "",
           f"Checked: {now}  ", f"Against: {aggregate_path}", ""]

    if canary_problems:
        out += ["## Preconditions failed — nothing was checked", "",
                "The ground moved. These are not findings about the "
                "requirements; they say the check could not run meaningfully.",
                ""]
        out += [f"- {p}" for p in canary_problems]
        out += ["", "Fix these and re-run. Do not read a clean result from a "
                "run that did not happen.", ""]
        return "\n".join(out)

    out += ["## Findings", ""]
    if findings:
        out += [f.render() for f in findings]
    else:
        out += ["No orphans or stale declarations found in the links this "
                "check covers. Read that together with the blind spots below "
                "— a clean result means nothing without them.", ""]

    out += ["## Checks that did not run, and why", ""]
    out += ([f"- {n}" for n in not_checked] if not_checked
            else ["All configured checks ran."])

    out += ["", "## What this check cannot see", "",
            "- **Uncovered mechanisms.** Links created by any route this scan "
            "does not walk are absent from the result, not clean.",
            "- **Shared-state coupling.** Relationships neither side declares "
            "— another system reading this database directly — cannot be "
            "detected from the artifacts and surface only in conversation.",
            "- **Declared versus exercised.** This verifies links present in "
            "the artifacts, not which are exercised in production.",
            "- **Marker presence is not correctness.** A component marked "
            "REQ-42 is asserted to implement it, not shown to.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aggregate", help="JSON from build_matrix.py --json")
    ap.add_argument("--stage", default="unnamed stage")
    ap.add_argument("--require-tests", action="store_true",
                    help="treat a requirement with no test as a finding")
    ap.add_argument("--require-commits", action="store_true",
                    help="treat a requirement with no commit in range as a finding")
    ap.add_argument("--fail-on", choices=["high", "medium", "low", "never"],
                    default="high", help="minimum severity that exits nonzero")
    ap.add_argument("--out")
    args = ap.parse_args()

    try:
        with open(args.aggregate, encoding="utf-8") as fh:
            aggregate = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"# Preconditions failed\n\nCannot read {args.aggregate}: {exc}",
              file=sys.stderr)
        sys.exit(2)

    problems = canaries(aggregate, args.aggregate)
    findings = [] if problems else check(aggregate, args.require_tests,
                                         args.require_commits)

    not_checked = []
    if not args.require_tests:
        not_checked.append("requirement-to-test coverage (enable with "
                           "--require-tests)")
    if not args.require_commits:
        not_checked.append("requirement-to-commit linkage (enable with "
                           "--require-commits)")

    doc = render(findings, problems, args.stage, args.aggregate, not_checked)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(doc)

    if problems:
        sys.exit(2)
    if args.fail_on != "never":
        threshold = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER.get(f.severity, 3) <= threshold for f in findings):
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
