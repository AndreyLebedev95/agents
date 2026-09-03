---
name: check-traceability-integrity
description: Checks a traceability chain for orphans and drift after a stage completes, and reports findings rather than quietly patching them. Covers checking in both directions so neither side can move silently, reading declared relationships as a whitelist so undeclared actuals and stale declarations both surface, canary checks on preconditions so a failure says the ground moved rather than the subject is wrong, the reconciliation check that cannot fail and how to prove yours can, detecting broken references before a reader hits one, and comparing what was intended against what is actually in the artifacts. Use after a spec revision, refactor, merge or release; whenever a requirement may have no implementing component, a test may cite a requirement that no longer exists, or a matrix passes but nobody quite believes it; when asked what became orphaned or what drifted; or when asked whether a check actually verifies anything — even if the request is just "did we break any of the requirement links". For generating the matrix use build-living-traceability-matrix; for coupling, complexity, cycles and layer-violation governance use govern-architecture-with-fitness-functions; for reviewing a diff use code-review-expert.
---

# Checking traceability integrity

Run this when a stage completes — a spec revision, a refactor, a merge, a release — to answer one question: **is every link in the chain still true, and does the checking apparatus itself still work?**

Two commitments shape everything below.

**Report, do not repair.** A checker that fixes what it finds is grading its own work, and the independence is the whole value. Where a fix belongs upstream, name it and say where; leave the fixing to whoever owns the thing.

**A check that cannot fail is worse than no check.** It buys trust while providing no coverage. Half of this skill is about proving the checks can actually go red.

## The output

```
# Traceability integrity — <stage>
Checked: <timestamp>   Against: <commit or version>

## Findings
### <severity> — <finding>
Link:        <which link of the chain>
Detected by: <the check that caught it>
Evidence:    <the specific items>
Action:      <what to do, and who owns it>

## Checks that did not run, and why

## What this check cannot see
```

Findings ordered most severe first. If nothing was found, say so plainly and still print the blind spots — a clean result means nothing without them.

## The core move: declared relationships as a whitelist

The same extraction that renders a matrix answers a different question if you stop at the comparison instead of the render. The declared links are a **whitelist of permitted relationships**; compare the actual against it.

That comparison has two halves, and running only the first is the most common way a check gives false comfort:

- **Actual without declaration** — a component, test or commit that carries no requirement key, or references one that was never declared. An undeclared actual.
- **Declaration without actual** — a requirement whose declared components, tests or spec sections no longer exist. A stale declaration.

Checking only for undeclared actuals leaves declarations pointing at things that vanished — which is exactly the orphan people worry about. Run both directions, always.

Applied across the chain, that gives the orphan classes:

| Orphan | Direction | Means |
|---|---|---|
| Requirement with no spec section | declaration → actual | Specified nowhere; may not be real |
| Requirement with no component | declaration → actual | Nothing implements it |
| Requirement with no test | declaration → actual | Nothing verifies it |
| Component with no requirement | actual → declaration | Code serving nothing declared |
| Test citing a dead requirement | actual → declaration | Verifying something removed |
| Commit citing a dead requirement | actual → declaration | Usually a rename that missed a place |
| Spec section with no requirement key | actual → declaration | Invisible to every derived view |

`references/check-catalogue.md` gives each of these as a runnable check with the evidence it should emit. `scripts/check_integrity.py` implements the whitelist comparison over a matrix aggregate.

## Prove each check can fail

A check written without extracting values from *both* sides passes regardless of whether the two sides agree. Hardcoding the expectation inside the check produces a green result that verifies nothing.

The proof is mechanical and takes a minute:

1. Change one side alone. Confirm the check goes red.
2. Change the other side alone. Confirm it goes red.
3. Restore both.

If either mutation leaves it green, the check is decorative. This is worth doing when a check is written and again whenever someone reports that "everything passes but the matrix looks wrong" — that sentence is usually literally true.

Two related habits:

- **Parameterize rather than loop.** A loop inside a check reports one failure for the whole set and does not name which item failed. A parameterized check names it.
- **Fail loudly on the unrecognized.** A checker that silently skips elements it cannot parse hides exactly the violations it exists to catch. Report them as a distinct finding class: *not checked*, which is different from *passed*.

## Check the preconditions first

Assumptions a check depends on — that the specification file exists, that the perimeter resolves, that the version-control history is reachable, that the key regex matches anything at all — should be verified before the substantive checks run.

These are **canary checks**, and their value is diagnostic routing. When a precondition fails, the substantive check that follows "does not even fail" for its stated reason: it reports something misleading about the subject when the real problem is elsewhere. Nobody should spend an afternoon investigating a subsystem because a path was wrong.

Report their failure in a distinct voice: *the ground moved*, not *the subject is wrong*.

Standard canaries before a traceability check:

- The specification source is present and parseable
- The component and test perimeters exist and are non-empty
- The identifier pattern matches at least one thing
- The history range resolves
- The marker vocabulary file is present, if the scheme uses one

## Check the references, not just the links

Every path, identifier and search the documentation depends on will eventually break — targets are renamed, moved, reorganized, or disappear. Run a checker across the whole body of documentation so breakage is found by the build rather than by a colleague, because a single stale reference costs a document its credibility with the person who hits it.

Where an off-the-shelf link checker cannot reach — into your own artifacts — a low-tech check does the same job: assert the referenced identity against a hardcoded literal copy of it. It fails on precisely the refactoring that broke the reference, and then the decision is deliberate: fix the reference, or revert the change that broke a published contract.

Treat a broken reference as a defect, not as maintenance.

## Check the vocabularies

The chain rests on its vocabularies, and they decay quietly:

- **Every tag in use is declared**, and every declared tag is still used. An undeclared tag means queries over that vocabulary are under-reporting; a declared-but-unused tag means the vocabulary is drifting from the work.
- **Every commit scope in use is declared**, and — the property that matters — **every change that could be committed falls under some scope.** An uncovered change is an invisible change.
- **Process tags have not outlived their work.** An "in progress" tag still present three iterations later is being read as current and is not.

## Compare intended against actual

Implementations drift from their intent one small decision at a time until nothing resembles what was meant. The counter is frequency, not rigour.

Generate the picture of what is actually there, set it against the stated intent, and enumerate the differences. For each difference decide deliberately: correct the implementation, or amend the intent. Both are legitimate; leaving it unexamined is not, because that is where the drift resumes.

The asymmetry that makes this work: **intent changes rarely while implementation changes constantly**, so the intent is a usable stable baseline. If no intent was ever stated, reverse-engineer a first version from what exists and treat that as the baseline going forward.

The same comparison catches something a link check cannot: a picture drawn before building versus one derived from what was built are two independent statements about the same system, and their differences are either implementation defects or evidence that the up-front picture was speculation.

## Reporting

**Report; do not repair.** When a fix belongs upstream, say so and where. If the generated view reads badly, the defect is in the artifacts it read — an unclear name, a missing marker, a structure that does not match how people think — and the fix is there, not in the output.

**State what the check cannot see**, beside the findings, before anyone reads them. Three blind spots recur, and `references/stating-blind-spots.md` gives wording that does not overclaim:

- **Uncovered mechanisms.** Links created by a route the check does not walk are absent, not clean.
- **Shared-state coupling.** A relationship neither side declares — another system reading your database directly — is undetectable from the artifacts and surfaces only in conversation.
- **Declared versus exercised.** The check verifies links present in the artifacts, not which are exercised in production.

**Escalate what recurs.** A report listing the same orphan every cycle has stopped being a finding. It has become a record of something nobody is fixing — documentation whose existence proves an unfixed problem, and the effort spent regenerating it was effort not spent removing the need for it.

When a finding survives three cycles, change its treatment: say plainly that it is not being fixed, and name which of the honest reasons applies — budget allocated elsewhere, a fix that is genuinely expensive or needs coordination across teams, or the team lacking the knowledge to do it. Some of those are legitimate. Naming which one is what separates a considered decision from an evasion, and it is the point at which a mechanical check has to hand something to a person.

**Escalate the mechanism, not the diligence.** Where a decision is being violated repeatedly, the answer is not to communicate it again. Communication does not survive turnover, and other teams — remote ones, ones in other departments — may never have read it. The escalation ladder: state it in the record with its rationale → mark it in the artifacts → add an automatic check → make the check fail the build where that is safe → block the change outright, ensuring whoever hits the block learns the reason at that moment. Reserve the upper rungs for the few decisions whose violation actually causes harm; enforcing everything gets the enforcement removed wholesale.

## Where this ends and other checks begin

This checks *link integrity*: does the chain still connect what it claims to connect. It does not check coupling, cyclomatic complexity, dependency cycles or layer violations — that is architecture governance, and `govern-architecture-with-fitness-functions` covers it. The two share a mechanism and answer different questions; run both.

Worth knowing while building either: a generated view and an automated check are the same extraction with different endings. Build the extraction once, render it for people, and apply the rule to the same extracted data as a check. Do not build it twice.

## Reference material

- `references/check-catalogue.md` — every check by chain link: what it compares, how to prove it can fail, and the finding it emits. Read when implementing or auditing a specific check.
- `references/stating-blind-spots.md` — the three recurring blind spots and wording that keeps absence from being read as evidence. Read before publishing a result to anyone outside the team.
- `scripts/check_integrity.py` — whitelist comparison in both directions over a matrix aggregate, with canary preconditions and severity-ordered findings.
