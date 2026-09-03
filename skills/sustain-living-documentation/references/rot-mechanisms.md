# Rot mechanisms

Read when working out why a specific artifact is decaying. Diagnose per artifact — the mechanisms are different and so are the fixes.

## Contents
- [The diagnostic question](#the-diagnostic-question)
- [The mechanisms](#the-mechanisms)
- [The six defects of knowledge already present](#the-six-defects-of-knowledge-already-present)
- [De-volatilizing a document](#de-volatilizing-a-document)
- [The four properties an artifact needs to survive](#the-four-properties-an-artifact-needs-to-survive)

## The diagnostic question

> **What keeps this accurate today?**

Ask it of each artifact separately and take the answer literally. "Someone is supposed to update it" is the answer in most cases and is the whole diagnosis.

The follow-up that sharpens it: *what would have to happen for this to become wrong without anyone noticing?* If you can describe that path in one sentence, that path is being taken right now.

## The mechanisms

### Accuracy rests on diligence

**Tell:** accurate for two or three weeks after someone works on it, then progressively not.

**Cause:** the artifact duplicates knowledge that lives elsewhere, and nothing forces the copy to follow the original.

**Fix:** move up the mechanism ladder — generate it from the authoritative source; or let a tool propagate changes; or add a check that fails when the two disagree. Assign ownership of that mechanism, never of the updating.

**Do not:** assign an owner to keep it current. That is the same failure with a name attached.

### A step in the practice is a chore

**Tell:** the practice was followed for a while and then quietly stopped. Nobody decided to stop.

**Cause:** the practice contains a step that is tedious and unrewarded — almost always copying information from one place to another.

**Fix:** identify the specific step people stopped doing and automate it, or redesign so the copy is unnecessary. Exhortation has no effect here; the step will stop again.

### Communicated rather than enforced

**Tell:** the decision is violated repeatedly, usually by people outside the immediate team.

**Cause:** the decision was communicated — a document, an email, a mention at standup — and communication does not survive turnover, distance or inattention.

**Fix:** escalate for the few decisions whose violation causes harm: record with rationale → mark in artifacts → automatic check → fail the build → block the change with an explanation at the point of blocking. Reserve the upper rungs; enforcing everything gets the enforcement removed wholesale.

### Perishable values written into a durable document

**Tell:** the document needs editing every few months for reasons unrelated to its subject — a name changed, a date passed, a threshold moved.

**Cause:** values with a short lifetime were written where a long-lived document could reach them.

**Fix:** see [De-volatilizing a document](#de-volatilizing-a-document) below.

### Markers on the surviving side

**Tell:** transitional tags — in progress, being replaced, pending — persist long after the transition ended.

**Cause:** the marker was attached to the artifact that survives the transition, so nothing removes it.

**Fix:** attach transitional markers to the side that gets deleted. The deletion then removes the marker. Where the surviving side must be marked, accept that cleanup is a real task — and read a lingering marker as a signal that the initiative was never finished, which is information.

### The link carrier does not move with the element

**Tell:** links break at every reorganization; a refactor produces a wave of broken references.

**Cause:** the link lives somewhere that has no knowledge of the element's identity — a path in an external register, a sidecar file, a hardcoded name.

**Fix:** move to a carrier collocated with the element, so it survives renames and moves. Where that is impossible, add a reconciliation check that detects the break, and accept that you are now maintaining a check.

### Trust already lost

**Tell:** the artifact is roughly accurate but nobody consults it.

**Cause:** it was wrong once, visibly, and readers learned they had to verify it. That cost never goes away for them, so consulting it stopped being worth the trouble.

**Fix:** this is the slowest to repair. Fix the mechanism first so it cannot be wrong again, then say so explicitly, then wait. Do not attempt to restore trust by improving the content; content was never the problem.

### The documentation is protecting itself

**Tell:** "we'd have to update all the docs" appears as an argument against making a change.

**Cause:** enough static documentation accumulated that maintaining it competes with the work.

**Fix:** treat this as a defect in the documentation, not a cost of the change. Reduce the volume, or move it to a form that regenerates. Watch the number of words and diagrams needed to explain something — fewer is better, and any artifact or process impeding continuous change should be removed.

### Documenting instead of fixing

**Tell:** a troubleshooting guide, a known-issues list, or a workarounds page that keeps growing.

**Cause:** documenting the problem was cheaper in the moment than fixing it.

**Fix:** before documenting a problem, ask whether the same effort would fix it. Where it genuinely would not, name which reason applies — budget allocated to documentation but not to the code, a fix requiring coordination across teams or a release to many clients, the team lacking the knowledge. Some are legitimate; naming which one separates a decision from an evasion.

### The mechanism outgrew the work

**Tell:** more effort is going into the generators than into what they describe. Nobody has said so out loud.

**Cause:** the tooling is more enjoyable than the delivery, and nothing bounded it.

**Fix:** require each improvement to yield a demonstrable short-term benefit in delivery, quality or user satisfaction. Treat every technique as an option, never a requirement. Watch for perfectionism, which here is procrastination with a respectable motive.

### Automated too early

**Tell:** the mechanism is rewritten more often than it is used.

**Cause:** it was built while the shape of the knowledge was still moving.

**Fix:** remove it and wait. Automation is justified by repetition; when the task is new or different every time, there is nothing to automate yet. If existing automation is making change harder rather than easier, delete some.

## The six defects of knowledge already present

Before building anything to fix a gap, diagnose which defect it is. The knowledge you need almost always already exists somewhere; what is wrong with it is one of six things, and each has a different remedy.

| Defect | What it looks like | Remedy |
|---|---|---|
| Inaccessible | Present but unreadable by the audience | Extraction and publication |
| Too abundant | Buried in volume | Curation and search |
| Fragmented | One concept spread across many places | Consolidation |
| Implicit | All but the marker that names it | Add the marker |
| Unrecoverable | Obfuscated beyond reading | Reverse-engineer or rewrite |
| Unwritten | Only in people's heads; only consequences in the system | Have the conversation and capture it |

Diagnosing wrongly is expensive. Extraction machinery pointed at an unwritten fact produces an empty report and a lot of wasted effort.

## De-volatilizing a document

Documents rot at identifiable points. Each has a standard repair: replace the perishable value with a pointer to wherever that value authoritatively lives.

| In the document | Replace with |
|---|---|
| A project or product code name chosen for internal or marketing reasons | A name drawn from the business function |
| A person's name or role | A link to wherever team membership is actually maintained |
| A date or schedule | A link to the channel where the announcement is made |
| A concrete artifact name, such as a class or file | A link to a *search* for the marker that identifies it, so the reference survives renames and splits |
| A concrete parameter value or threshold | A pointer to the configuration or the scenarios that hold it |
| A version number | A pointer to where the current version is published |
| A logo, footer or house style | Keep the content in a lightweight text format under source control and let the styling live elsewhere |

Every replacement trades directness for durability — the reader now takes one more hop. That is the right trade for anything expected to outlive its current values, and the wrong one for a document with a known short life.

The most useful entry in that table is the fourth. Linking to a search rather than to a path is the move most people have not considered, and it converts the most fragile reference class into one of the most durable.

## The four properties an artifact needs to survive

Whatever the artifact, it persists only if all four hold. Any one missing predicts a specific failure.

**Reliable** — accurate and in sync at any point in time. Requires a mechanism, not discipline. *Missing → nobody trusts it, and the trust does not come back.*

**Low effort** — costs almost nothing extra when things change. Achieved through simplicity, standards, evergreen content, collocation, and knowledge that moves with what it describes. *Missing → abandoned within weeks, whoever owns it.*

**Collaborative** — reachable by the audiences who cannot read the artifacts, without manual work. Ownership is collective; developers hold the technical responsibility, not the knowledge. *Missing → it serves one group and the others build their own, which then disagree.*

**Insightful** — the act of producing it gives feedback on the actual state of the system. *Missing → it is bookkeeping, and bookkeeping is the first thing dropped under pressure.*

A scheme that is reliable but high-effort gets abandoned. One that is low-effort but unreliable is worse than nothing. Check all four before concluding an artifact is fine.
