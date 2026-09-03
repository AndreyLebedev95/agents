# Check catalogue

Every check by chain link: what it compares, how to prove it can fail, and the finding it emits.

## Contents
- [Canary checks](#canary-checks)
- [Declaration-without-actual checks](#declaration-without-actual-checks)
- [Actual-without-declaration checks](#actual-without-declaration-checks)
- [Reference checks](#reference-checks)
- [Vocabulary checks](#vocabulary-checks)
- [Intent-versus-actual checks](#intent-versus-actual-checks)
- [Proving a check can fail](#proving-a-check-can-fail)
- [Severity](#severity)

## Canary checks

Run before everything else. Their failure means the check could not run meaningfully — a different statement from a finding, and it must be reported in a different voice.

| Canary | Fails when | Says |
|---|---|---|
| Specification source present and parseable | The spec path is missing or malformed | The check was pointed at nothing |
| Perimeters exist and are non-empty | A scanned root does not resolve | The aggregate was built against a different tree |
| Identifier pattern matches something | Zero keys found anywhere | The pattern is wrong, not the requirements |
| History range resolves | The tag or ref does not exist | The range is wrong |
| Marker vocabulary file present | The declared-tags file is missing | Vocabulary checks cannot run |

When a canary fails, **do not run the substantive checks and do not report a clean result.** A clean result from a run that did not happen is the most damaging output this whole apparatus can produce.

## Declaration-without-actual checks

The chain declares something exists; verify it does.

### Requirement with no spec section

*Compares:* keys found in the specification against keys found anywhere.
*Emits:* the requirement identifiers absent from the specification.
*Ambiguity to state:* either the requirement is specified nowhere and may not be real, or the spec section exists but is missing its key. These look identical from here and the finding must say so rather than assuming the second.
*Severity:* medium.

### Requirement with no implementing component

*Compares:* declared keys against keys carried by artifacts in the component perimeter.
*Emits:* requirements nothing implements.
*Ambiguity to state:* genuinely unimplemented, or implemented without a marker. Indistinguishable from here.
*Severity:* high.

### Requirement with no test

*Compares:* declared keys against keys carried by artifacts in the test perimeter.
*Emits:* requirements nothing verifies.
*Action:* add coverage, or mark the requirement as deliberately unverified **with a stated reason** — an unverified requirement with a recorded rationale is a decision; one without is an oversight.
*Severity:* high.

### Requirement with no commit in range

*Compares:* declared keys against keys cited in the history range.
*Emits:* requirements no commit in the range mentioned.
*Expected noise:* high. A requirement predating the range legitimately has no commits in it. Treat this as informational unless the range covers the whole life of the requirement.
*Severity:* low.

### Declaration pointing at a missing artifact

*Compares:* every path declared in the aggregate against the filesystem.
*Emits:* the declared links whose target no longer exists.
*What it really tells you:* the artifact was renamed, moved or deleted and the link did not follow. That is the failure mode the carrier choice was supposed to prevent — so the finding is about the scheme, not only about this instance. Reconsider the carrier.
*Severity:* high.

### Requirement with no trace at all

*Compares:* requirements against the union of components, tests and commits.
*Emits:* requirements existing only in the specification.
*Action:* confirm before the next stage gate whether work has not started or the chain broke completely.
*Severity:* high.

## Actual-without-declaration checks

Something exists; verify the chain accounts for it.

### Artifact carrying no requirement key

*Compares:* every artifact in the perimeter against those carrying a key or an explicit suppression.
*Emits:* the unkeyed artifacts, by name.
*Why it is not optional:* an unkeyed artifact is invisible to every derived view. Skipping these is how a matrix looks complete and is not.
*Action:* each is a genuine gap or should carry an explicit suppression. There is no third state.
*Severity:* medium.

### Test citing a requirement that no longer exists

*Compares:* keys cited in the test perimeter against declared keys.
*Emits:* tests verifying something that was removed.
*Usual cause:* a requirement was renamed or withdrawn and the citations were not followed through.
*Severity:* medium.

### Commit citing a requirement that no longer exists

*Compares:* keys cited in history against declared keys.
*Emits:* the commits and the dead keys.
*Note:* history is immutable, so this is never fixed by editing the past. Either the key was renamed — in which case record the mapping — or the requirement was withdrawn, which is legitimate and worth annotating rather than chasing.
*Severity:* low.

### Spec section with no requirement key

*Compares:* specification sections against those carrying a key.
*Emits:* sections invisible to every derived view.
*Severity:* medium.

## Reference checks

*Compares:* every path, link and search the documentation depends on against its target.
*Emits:* broken references, before a reader hits one.

Where an off-the-shelf checker cannot reach into your own artifacts, use a **contract check**: assert the referenced identity against a hardcoded literal copy of it, positioned so automated refactoring will not update it. It then fails on exactly the refactoring that broke the reference, and the response is a deliberate choice — fix the reference, or revert the change that broke a published contract.

Treat a broken reference as a defect. A single stale reference costs a document its credibility with the person who hits it, and they do not come back to check whether it was fixed.

## Vocabulary checks

| Check | Fails when | Means |
|---|---|---|
| Every tag in use is declared | A tag appears in the artifacts but not in the vocabulary file | Queries over that vocabulary are under-reporting |
| Every declared tag is still used | A declared tag has no occurrences | The vocabulary is drifting from the work |
| Every commit scope in use is declared | A scope appears in history but not in the list | Same |
| The scope list covers every possible change | A change can be named that fits no scope | An uncovered change is an *invisible* change |
| Process tags have not outlived their work | An in-progress or iteration tag persists past its iteration | It is being read as current and is not |

The coverage property is the one that matters most and the one nobody tests. It cannot be checked mechanically — it is checked by trying to name changes that fit no scope, and adding scopes until none remain.

## Intent-versus-actual checks

*Compares:* the stated intended structure against the structure derived from the artifacts.
*Emits:* the differences, each requiring a deliberate decision — correct the implementation, or amend the intent.

Both outcomes are legitimate. Leaving a difference unexamined is not, because that is where drift resumes.

The asymmetry making this workable: intent changes rarely, implementation constantly. That makes intent a usable stable baseline. Where no intent was ever stated, reverse-engineer a first version from what exists and use that going forward — an imperfect baseline detects drift; no baseline detects nothing.

A related comparison catches what no link check can: a picture drawn before building versus one derived from what was built are two independent statements about the same system. Their differences are either implementation defects or evidence that the up-front picture was speculation, and both are worth knowing.

## Proving a check can fail

For each check, before trusting it:

1. Change one side alone → confirm red.
2. Change the other side alone → confirm red.
3. Restore both.

If either mutation leaves it green, the check is decorative. The most common cause is an expectation hardcoded inside the check rather than read from the source it is supposed to be comparing against — which passes regardless of whether the two sides agree, and buys trust while providing no coverage.

Two supporting habits:

- **Parameterize rather than loop.** A loop reports one failure for a whole set without naming which item failed.
- **Distinguish *not checked* from *passed*.** A checker that silently skips what it cannot parse hides exactly the violations it exists to catch. Report the unparseable as its own class, and list which configured checks did not run and why.

## Severity

| Severity | Meaning |
|---|---|
| High | A link is broken or absent where the chain claims one exists. Blocks a stage gate. |
| Medium | Something is invisible to the chain, or a link is ambiguous. Fix before it accumulates. |
| Low | Informational, or expected noise from the range or scope of the run. |

Order findings most severe first. A recurring finding, whatever its severity, changes category after three cycles — see the escalation guidance in the main skill.
