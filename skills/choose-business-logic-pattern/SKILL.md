---
name: choose-business-logic-pattern
description: Decides how much modelling machinery a piece of business logic deserves, running an ordered decision from the area's strategic value to the implementation pattern, the codebase organisation and the testing emphasis. Covers the four ordered questions selecting procedural scripts, record objects, a rich domain model or an event-sourced model; the test distinguishing real rules and invariants from input validation; why the fitting pattern audits the strategic classification in reverse; and why a team fluent in an advanced pattern may rightly use it everywhere. Use whenever starting a component and asking how to structure its logic; deciding between plain CRUD and a rich model; when someone proposes event sourcing; when a design is called over-engineered, anemic or gold-plated; when an area has become painful to change; when asking which kinds of tests matter most in this codebase; or when deciding whether a legacy component should be refactored or replaced — even when the ask is only "is this worth modelling properly". For topology and style use choose-architecture-style; for service sizing use decompose-system-into-components; once chosen use design-aggregates-and-invariants and model-lifecycle-and-events.
---

# Choosing a business logic pattern

Both failure directions cost real money, and they are symmetrical.

Under-model an area that matters and the rules duplicate across call sites, drift apart, and start contradicting each other — in exactly the part of the system that changes most often. Over-model an area that does not and you have paid for indirection that protects nothing, in code that will barely change.

There is a defensible answer, and it comes from the business rather than from taste. This skill is the ordered decision that produces it.

## The output

Per area, four things and the reasoning:

1. **Strategic type** — differentiating, bought-in, or merely necessary.
2. **Business logic pattern** — how the rules are organised.
3. **Codebase organisation** — what hosts that pattern without fighting it.
4. **Testing emphasis** — which kind of test carries the weight.

Plus the result of the **cross-check**, which is where this earns its keep.

## Step 1 — Establish what the area is worth

Before anything technical: is this area what the business competes on, something everyone buys off the shelf, or something necessary that confers no advantage?

That classification is the input to everything below. If it has not been done, do it first — see `map-subdomains-and-boundaries`.

## Step 2 — Four questions, in order, stop at the first yes

**1. Does this area track money or monetary transactions, owe a consistent audit log, or need deep analysis of its own behaviour?**
→ **Event-sourced model.** Every state change recorded as an event; events are the source of truth.

**2. Is the business logic complex?**
→ **Domain model.** Aggregates enforcing invariants, value types, commands as the only way to change state.

**3. Are the data structures complex?**
→ **Record objects.** Objects that encapsulate mapping complicated structures to storage, with the logic organised as procedures over them.

**4. Otherwise.**
→ **Procedural scripts.** One procedure per operation, each transactional.

The order matters. Each question is a sufficient condition for its answer, so answering them out of order lets a lesser reason pre-empt a stronger one.

### What "complex" means here

The line is not razor-sharp, but it is useful. Two tests, and they usually agree:

- **The shape of the logic.** Complicated rules, invariants and algorithms are complex. Validating inputs and converting between formats is not.
- **The shape of the language.** Is the vocabulary describing create-read-update-delete operations, or business processes and rules? A domain whose experts talk in terms of eligibility, escalation, thresholds and reversals has complex logic regardless of how the current code looks.

## Step 3 — Run the cross-check

**The pattern that fits audits the classification that produced it.**

If you called an area core but a procedural script or record objects fit it comfortably, or you called it supporting and it demands a full domain model, the mismatch is evidence that the classification is wrong. Go back and re-examine the area, and take the question to the business.

This is the most useful step here and the one most often skipped, because it feels like the decision has already been made. It has not — the tree runs in both directions, and the technical answer is a genuine check on the strategic one.

One caveat before you conclude the classification loses: **an area's competitive advantage need not be technical.** Something can be genuinely core to the business while the software supporting it is a data-entry screen. The mismatch is a prompt to look again, not a verdict.

## Step 4 — Derive the architecture

Once the logic pattern is fixed, the codebase organisation follows. Choosing it independently is how teams end up fighting their own structure.

| Logic pattern | Organisation | Because |
|---|---|---|
| Event-sourced model | segregated read models | otherwise querying collapses to fetch-one-by-id — you cannot query across instances at all |
| Domain model | infrastructure-inverted (logic at the centre) | layered organisation fights aggregates that must know nothing of persistence |
| Record objects | layers plus an application service layer | the service layer hosts the logic that controls the records |
| Procedural scripts | minimal layers | there is nothing to insulate |

**The one pattern that escapes the chain** is read-model segregation. It is worth adopting with any logic pattern when one dataset needs several persistent representations — a relational store for writes, a search index, prerendered views — kept synchronised.

### One caution on that pattern

A widespread misreading holds that a state-changing operation must return nothing, with all data fetched through read models. That is wrong, and it produces both accidental complexity and a poor experience.

A command must tell its caller whether it succeeded and, on failure, why — validation or technical — so the caller can act. It may and often should return the resulting data, sparing a round trip and letting consumers use the result in their next step. The real constraint is only that returned data must come from the strongly consistent write model, never from an eventually consistent projection.

## Step 5 — Derive the testing emphasis

The same decision settles the argument about which tests matter, which is otherwise a matter of belief:

| Logic pattern | Weight tests toward | Because |
|---|---|---|
| Domain model (either variant) | **unit** — classic pyramid | aggregates and value types are ideal units; the logic is in them |
| Record objects | **integration** — diamond | the logic is split across the service and logic layers, so the seam between them is where defects live |
| Procedural scripts | **end-to-end** — inverted pyramid | the logic is simple and the layers few; verifying the whole flow is the efficient check |

## Step 6 — Apply per subdomain, not per boundary

None of this is a system-wide setting, and it is not even necessarily boundary-wide. One boundary can hold areas of different types with genuinely different needs, and even two areas of the same type may need different treatment.

Imposing one architecture across a whole boundary produces accidental complexity for the areas it does not suit. Give each subdomain its own module and pick the tools inside it. Those logical divisions are also what can later be promoted into separate physical boundaries, so drawing them early costs little and buys optionality.

## The judgement these rules do not replace

**These are heuristics, not laws.** They encode a preference for simple tools, escalating only when necessary, and every one of them has exceptions.

The clearest exception: a team with deep experience in an advanced pattern may legitimately apply it everywhere, because **for them it genuinely is the simpler option**. Fluency changes what "simple" means. If the tree contradicts your context, alter it or build your own — the right response is never to follow it against your judgement.

Two further correctives:

- **Design pain is a signal about the domain, not just the code.** When adding functionality to an area becomes painful, the common cause is that the area changed strategic type and the design no longer carries its complexity. Reassess the business before refactoring.
- **Needing to change the pattern later is normal.** Nobody can foresee how a business evolves, and applying elaborate patterns everywhere in advance is wasteful. Choose the appropriate design and evolve it when the evidence arrives.

## Migrating between patterns

Moves happen in a fixed direction as complexity grows, and each has an entry condition:

**Procedural → record objects.** When working with the data becomes the difficulty. Look for complicated structures and encapsulate them.

**Record objects → domain model.** When the logic manipulating them has become complex *and* inconsistencies and duplication are appearing. See the compiler-first sequence in `design-aggregates-and-invariants`.

**Domain model → event-sourced.** Only once aggregate boundaries are properly designed.

**Never jump straight to event sourcing from the first two.** Land on state-based aggregates first and spend the effort getting those boundaries right. Discovering a wrong transaction boundary is orders of magnitude cheaper in a state-based aggregate than in one where the events are already the truth and cannot be rewritten.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Rich model wrapping a create-read-update-delete screen | Pattern chosen by prestige | Drop to the simpler pattern |
| An area the business competes on, implemented as procedures | Under-modelled; rules duplicating across call sites | Move up the tree |
| Classified core, but a procedural script fits | The classification is probably wrong | Re-examine the area with the business |
| Event sourcing adopted "because it's better" | Pattern-led rather than domain-led | Answer the four questions honestly |
| Aggregates fighting the layering | The organisation does not host the pattern | Invert the infrastructure dependency |
| Commands returning nothing, forcing extra round trips | Misreading of read/write segregation | Return the result from the consistent model |
| One architecture imposed across a whole boundary | Applied per boundary instead of per subdomain | Module per subdomain; choose inside each |
| "Anemic model" raised as an objection to simple code | The label was applied to shape, not to complexity | Judge against the complexity of the logic |

## On the word "anemic"

Objects that hold a data structure with public accessors and persistence, with the rules living outside in procedures, are routinely condemned as an anemic domain model.

The label depends entirely on the area. Where the logic is genuinely simple, that shape is *correct*, and applying a richer pattern there introduces accidental complexity of its own. It becomes a real defect only when it is carrying complex logic — and then the problem is not the shape, it is that the rules have nowhere to live.

The same even-handedness applies downward: procedural organisation is the foundation every other pattern is built on, not an anti-pattern. Treating it as forbidden is what pushes teams into over-engineering simple things.

## Bundled references

- `references/decision-trees.md` — the three trees written out with their exception cases, plus worked classifications. Read when applying the decision to a concrete area.

## Worth reading

- Martin Fowler, *Patterns of Enterprise Application Architecture* (2002) — where these logic patterns were originally defined.
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013) — extended treatment of when the richer patterns pay.
