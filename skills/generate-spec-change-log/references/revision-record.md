# The revision record

Read when recording a specification revision rather than generating a release log.

## Contents
- [Why a record as well as a log](#why-a-record-as-well-as-a-log)
- [The entry format](#the-entry-format)
- [The supersession rule](#the-supersession-rule)
- [The four parts of a rationale](#the-four-parts-of-a-rationale)
- [Worked examples](#worked-examples)
- [What does not belong here](#what-does-not-belong-here)

## Why a record as well as a log

A change log says **what changed**. A revision record says **what was decided and why**. They answer different questions and have different lifetimes.

The question a later reader actually has is almost never "what changed in release 1.4". It is "why is this like this, and can I change it". Only the record answers that, and only if it kept the reasoning rather than the outcome.

Where the decision is an architecture decision with trade-offs to analyze, use `record-architecture-decisions` — that covers the analysis method and the ADR structure properly. What follows is the narrower case: recording that a *specification* moved, so downstream readers can see the history.

## The entry format

```
## <identifier> — <title>

Status:       Accepted | Superseded by <identifier>
Date:         <date>
Supersedes:   <identifier, if any>

### Context
<the situation at the time — stakes, load, priority, assumptions, constraints>

### Decision
<what was decided>

### Rationale
<why, including the assumptions that shaped it>

### Alternatives considered
<what else was seriously considered, why it lost, and when it would win>

### Consequences
<what follows, including risks and what this forecloses>
```

Keep entries as structured text files in a folder at the root of the repository, versioned alongside the artifacts they describe. Not in a separate store — the record and the thing it describes should move together, be branched together, and be reviewed together.

## The supersession rule

> **Never edit an accepted entry. Supersede it.**

When a decision changes: add a new entry, reference the one it replaces, and mark the old one superseded. The old entry stays, in full, saying what was true then.

This is what turns the record into a history rather than a snapshot. A reader can then see not just what is true but how it came to be — and, critically, can distinguish "this was considered and rejected" from "this was never considered", which are the two situations most often confused when someone proposes reopening a settled question.

Editing an entry destroys exactly that, and the loss is invisible: the record still looks complete and consistent. Nobody ever discovers what was overwritten.

The corollary: a record with no superseded entries in a project of any age is not a record of a project that never changed its mind. It is a record that has been edited.

## The four parts of a rationale

Recording "why" is not recording a reason.

### 1. The context at the time

The stakes, the current load, the priority then in force, the assumptions held, and the constraints coming from people rather than technology.

Examples of real context: *"Only a thousand end users, weekly."* — *"Priority is finding product-market fit as fast as possible."* — *"This is not expected to change."* — *"The team is unwilling to take on another language."*

That last kind is the one people are embarrassed to write and the one that most often explains a decision.

### 2. The problem or requirement

What forced a choice at all. *"The page must load in under 800ms or we lose visitors."* — *"The old module must be decommissioned this year."*

### 3. The decision, with its main reasons

The decision, not merely the solution that resulted. There is a difference: "we use a facade over the legacy system" is a solution; "we decided not to rewrite the legacy system because there is no good reason to, but we still want to consume it as conveniently as if it were new" is a decision.

### 4. The alternatives seriously considered

Why they were not chosen, and under what different context they would be.

**This is the part always omitted and the part that matters most.** Design rationale is largely about the options that were discarded, and those are never visible in the artifact itself — the artifact shows only what won.

Without it, a later reader cannot tell whether an alternative was rejected for a reason that still holds or one that expired years ago. So they leave it alone, and the status quo wins by default even where an obvious improvement is in plain sight. The other failure is the mirror image: someone changes it and breaks a forgotten concern they had no way of seeing.

Phrase alternatives with their conditions: *"Buying off the shelf would be better if the needs were more standard."* — *"A graph structure would be more powerful but is harder to map onto the spreadsheets the users actually work in."* — *"A different datastore would be a better fit if we did not already have this investment in the current one."*

### Include the structuring assumptions

An assumption is usually the real reason a decision took its shape, and it is the thing most likely to have quietly stopped being true. *"We assume articles published in the last 24 hours account for over 80% of traffic"* is what actually explains partitioning recent from archived content — and it is the sentence someone should re-examine in three years.

## Worked examples

### Thin — insufficient

```
## SPEC-014 — Use the batch import path
Status:  Accepted
Date:    2026-03-02
Decision: Imports go through the batch path.
Rationale: It is simpler.
```

Nothing here survives contact with a later reader. Simpler than what? Under what load? Was streaming considered? A year from now this entry cannot be acted on, only worked around.

### Adequate

```
## SPEC-014 — Imports go through the batch path
Status:  Accepted
Date:    2026-03-02

### Context
Partner files arrive nightly, largest seen is 40MB. No partner has asked
for intraday delivery. Two engineers, both new to the streaming stack.

### Decision
All partner imports go through the existing batch path. No streaming
ingestion for now.

### Rationale
The nightly cadence matches how partners actually publish, and the batch
path already handles retry and replay. Assumption: file sizes stay under
roughly 100MB and nobody needs intraday. Both are worth rechecking.

### Alternatives considered
- Streaming ingestion: better if intraday delivery is ever required, and
  the right answer the moment a partner asks for it. Rejected now because
  it means operating a second ingestion path for no current benefit.
- Per-partner choice: rejected — two paths to maintain from day one, and
  no partner needs the second.

### Consequences
Intraday delivery is not possible without revisiting this. If a partner
asks, reopen rather than working around it inside the batch path.
```

The second entry can be acted on years later by someone who was not there. That is the whole test.

### When the rationale resists being written

If the rationale is hard to state, or two or three credible alternatives cannot be named, that is a finding about the **decision** — either it was not deliberate, or the first workable option was taken without looking further.

Note that *"we took the first workable option to hit the date"* is a legitimate rationale. Once written down it becomes a known, revisitable choice rather than an accident nobody can distinguish from a considered design.

The hardest entries to write honestly are the ones where the decision was made for a poor reason — someone senior insisted, or a developer wanted the technology on their record. Those are the entries most worth having and the least likely to be written. No technique fixes this; the only useful thing is knowing that a suspiciously thin rationale often marks one.

## What does not belong here

- **Status and progress.** How far along something is changes constantly while the record does not. Merging them makes the record inherit the faster change rate, so it needs constant updating and then nobody trusts either. Separate overlay.
- **Speculation.** Record decisions taken against needs that were proven necessary. A record of a design that was never built describes something that does not exist and will not be built that way.
- **Anything that can be derived.** If the change log already says it, link rather than restate.
