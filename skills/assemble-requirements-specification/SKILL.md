---
name: assemble-requirements-specification
description: Structures a full requirements specification around business events (never "high-level vs. low-level"), applies one consistent requirement schema and ID scheme, and picks a single decomposition hierarchy for the whole project. Use whenever putting together or reorganizing a specification document, deciding what sections it needs, numbering or ID-ing requirements, reconciling story-language with use-case-language on the same project, or writing a project goal statement. Not for producing an individual requirement's own content (see decompose-requirement-into-scenario, write-atomic-requirement-statement, derive-fit-criteria-and-acceptance-criteria — this skill assembles their output) or resolving specific open gaps (see flag-requirement-gaps-as-open-questions, which owns the open-issues register's content — this skill only decides where that register lives in the document).
---

# Assemble Requirements Specification

A pile of well-written individual requirements is not a specification until it has a structure that lets someone find any given requirement, trust its ID is unique, and know which hierarchy the project is using. This skill is about that structure, not about writing any individual requirement — it's where the output of the other requirement-writing skills gets filed.

## Structure the document around business events

Use business events as the organizing unit — never an ad hoc "high-level requirement" vs. "low-level requirement" split. The reason is mechanical: a business event has an unambiguous start and end and doesn't overlap with any other business event, so grouping by it gives every reader the same, checkable answer to "does this belong here." "High-level" vs. "low-level" is a judgment call two people can disagree about forever, and disagreement about the organizing principle itself is a structural defect, not a matter of taste.

A workable three-area shape:

- **Area 1 — The Problem**: goals, stakeholders, glossary, scope of the problem space, business data dictionary.
- **Area 2 — The Solution**: scope of automation — what's inside vs. outside the product boundary.
- **Area 3 — The Business Events**: the event list, then per event, its functional requirements, non-functional requirements, and any additional material.

## Pick one decomposition hierarchy and hold to it

Two legitimate hierarchies exist, both rooted in the same business event:

- **Use-case track**: Business Event → Business Use Case → Product Use Case → Atomic Requirement.
- **Story track**: Business Event → Business Event Story → Functional Story → Detailed Task.

Choose one per project and don't mix them ad hoc — a project that talks about "epics" in one section and "product use cases" in another has usually drifted into using both tracks without deciding to, and that's a sign the decomposition itself has lost a consistent boundary rule, not just a vocabulary inconsistency.

Whichever track you use, the same boundary signal applies at the level below the top: if a piece of work has a genuine natural stopping point partway through, that's a sign it should be split into a separate story/use-case rather than forced into one continuous unit. "I could pause here and it would still make sense" is the tell.

Keep a top-level, business-event-scoped story deliberately undetailed at discovery time — that's not the same as an incomplete draft. It's a placeholder that gets detailed later; don't force it to satisfy every criterion you'd apply to a development-ready story (in particular, "small" and "estimable" are development-iteration concerns and don't apply yet at this level — trying to force them onto a top-level story usually means splitting something that isn't ready to be split, before its detail has actually been discovered).

## Give every requirement type one schema

Functional, non-functional, constraint, and technological requirements should all use the *same* underlying record shape — they differ only in the value of a Type field and which section they're filed under, not in what fields they carry. A minimum viable set:

Number · Description · Rationale · Type · Fit Criterion · Source · Customer Satisfaction · Customer Dissatisfaction · Conflicting Requirements · Dependent Requirements · Supporting Material · Version Number

Never invent a different field set per requirement type — that's a sign the schema was designed around one type and stretched to fit the others, and it makes cross-type queries ("show me every requirement with no fit criterion yet") impossible to write generically.

**Non-functional requirements attach at the business-event level and are inherited downward** — a compliance or look-and-feel requirement on the event applies to every story/task beneath it. Tag it as inherited rather than re-deriving or re-stating it at each leaf. When one non-functional requirement genuinely applies to several business events, duplicate it into each event's package (explicitly flagged as a duplicate) rather than only cross-referencing a single instance — a developer working one event's package end-to-end shouldn't have to chase a cross-reference into an unrelated part of the document just to know the product has to meet a security requirement that applies to their event too.

## Give every atomic requirement a unique ID, from the start

Assign the ID the moment a requirement is written — not as a batch numbering pass at the end. This is the one thing that makes the whole traceability chain (Work Scope → Business Event → Use Case/Story → Atomic Requirement → Implementation Unit) followable in either direction, and it's a hard gate, not a nice-to-have: a requirement with no ID can't be referenced by a test, a conflict record, or a change log, which means none of that tooling can actually be built around it later.

## Write goals so they can later be judged achieved

State a project or product goal with three parts:
- **Purpose** — one sentence, why the organization is investing.
- **Advantage** — one sentence, the benefit if successful.
- **Measurement** — one sentence (or a diagram) quantifying how the benefit will actually be measured.

A goal with no measurement can be *claimed* achieved by anyone, but never actually verified — treat a goal statement with no Measurement line as incomplete, not just informal.

## Enumerate systematically, not by brainstorming

Once the event list and product boundary exist, walk the event list to enumerate functional requirements for each product use case — don't brainstorm requirements unanchored from any event, since anything that doesn't trace to an event is a candidate for being out of scope or a duplicate under a different name. If the product boundary hasn't been decided yet (for example, when evaluating a purchasable product against business needs before deciding what to build vs. buy), fall back to writing requirements at the business-use-case level instead of waiting for the boundary decision.

## Resolving requirement conflicts within the structure

When two stakeholders' requirements conflict, resolve by declared user-priority tier — key users (critical to the product's continued success) take precedence over secondary users, who in turn outrank unimportant/infrequent/unauthorized users. This is a structural decision (which priority register the project maintains) as much as a per-conflict judgment call; if no such register exists yet, that's a gap for the gap-flagging skill to log, not something to invent in the moment.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Spec organized as "high-level requirements" then "detailed requirements" | No real organizing unit was chosen | Reorganize around business events |
| The same requirement gets different fields depending on its type | Ad hoc, per-type schema | Use one requirement schema for every type, varying only the Type value |
| A requirement has no ID | ID treated as optional, or added later in a batch | Assign a unique ID the moment the requirement is written |
| A project mixes "epic/story" language with "business use case/product use case" language | Two decomposition tracks in use at once | Pick one track for the project and hold to it |
| A goal statement gives no way to know later whether it was achieved | Missing Measurement | Add Purpose/Advantage/Measurement structure |

## Reference

`references/spec-skeleton.md` — the full three-area section list and the atomic-requirement schema, laid out as a ready-to-copy document template.
