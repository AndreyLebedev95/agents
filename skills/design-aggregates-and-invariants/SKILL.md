---
name: design-aggregates-and-invariants
description: Designs the entity model — which concepts are value types, which are entities, and where the aggregate boundaries that enforce consistency belong. Covers value-versus-identity, replacing primitives with typed domain values that validate themselves, the consistency boundary and its command-only interface, the one-instance-per-transaction rule and how a violation exposes a wrong boundary, the strong-consistency test for what goes inside, aggregate roots, id-only references out, stateless services, optimistic concurrency, and why invariants reduce complexity rather than adding it. Use whenever designing or reviewing an entity model or data model, deciding what belongs in one transaction, deciding whether a field lives on this object or another, working out whether something is a value or an entity, deciding where a business rule belongs, refactoring objects that cannot enforce their own rules, or investigating an invariant that breaks under concurrency — even when the ask is only "how should I model this". For lifecycle states and event names use model-lifecycle-and-events; for whether this machinery is warranted use choose-business-logic-pattern; for where the surrounding boundary goes use map-subdomains-and-boundaries; for sizing by coupling use decompose-system-into-components.
---

# Designing aggregates and invariants

An entity model is not a set of tables with behaviour bolted on. It is a set of **consistency boundaries**: groups of objects where something must be true at every moment, and where one object's rules can only be trusted because nothing outside can reach in and break them.

Getting these boundaries right is most of the work, and getting them wrong is what produces rules implemented in three places, invariants that hold in testing and fail in production, and transactions that fight each other.

## The output

For each concept in the domain:

- **Value types** — identified by their values, immutable, carrying their own validation and the operations on them.
- **Entities** — identified by a stable id, mutable, always living inside an aggregate.
- **Aggregates** — the consistency boundary: its root, everything inside it, the invariants it enforces, the commands that are the only way to change it, the events it emits, and the id-only references out.
- **Domain services** — stateless holders for logic that fits no single aggregate.

Each aggregate boundary comes with its justification stated in terms of **what must be strongly consistent**, because that is the only argument that makes a boundary defensible later.

## Step 1 — Separate values from entities

**A value type is identified by the composition of its values.** Two instances with the same values *are* the same thing, and changing any field conceptually produces a different value. Colour, money, a phone number, a height, a status, a version range.

Such a concept needs no identity field, and adding one is not merely redundant — it opens a defect. With an id, two rows can hold identical values under different ids, and comparing ids will report them as different things. The id creates the possibility of a distinction that does not exist in the domain.

**An entity needs a stable identity of its own.** Two people with the same name are not the same person. The id must be unique per instance and, barring rare exceptions, immutable for the entity's whole lifetime. Its underlying type is a domain decision — a generated id, a number, or something domain-meaningful like a serial number — and should itself be a value type rather than a bare primitive.

**Entities are never modelled standalone.** They exist only inside an aggregate. If you have found an entity, you have not yet finished — you still have to find the boundary it belongs to.

### Replace primitives that depend on convention

Representing domain concepts with strings, integers and dictionaries pushes correctness onto a convention someone has to remember. Two things then go wrong, both quietly:

- Validation logic duplicates across the codebase.
- There is no way to enforce that it runs before the value is used — and this gets worse as people who did not write the original code extend it.

A constructor taking eight strings where two must be phone numbers, one an email and one a two-letter country code is a defect waiting for its first careless caller.

Give each such concept a type that parses and validates on construction, and move every operation on those values onto it. Three things improve at once: intent becomes visible without long variable names, validation has exactly one home, and the operations become cohesive and testable.

**Money is the highest-value case.** Primitive representations of money invite rounding and precision defects, and scatter the arithmetic rules that should live in one place.

### Value types are immutable and compare by value

Since changing a field conceptually yields a different value, operations return new instances rather than mutating. Equality must be implemented over the values — inherited reference or id semantics will silently misbehave in collections, comparisons and deduplication.

Immutability also makes the behaviour side-effect free and safe to share across threads, which is a real benefit and not the reason to do it.

Default to value types wherever the concept permits. The string type in most languages is exactly this pattern: immutable, with rich behaviour that produces new instances rather than mutating.

## Step 2 — Name the invariants

For each candidate group of objects, write down what must be true at every moment. Not what is usually true, not what the UI prevents — what the business would call broken if it were violated.

This is the step people skip, and skipping it makes every later decision arbitrary, because **invariants are what boundaries are drawn around**. Without them you are grouping by data affinity, which is a schema, not a model.

Invariants are also under-stated in interviews, because they are too obvious to the business to mention. Incident history is the richest source: every "we had to correct that by hand" describes an invariant nothing was enforcing.

**Then sort them into two piles**, because they have different remedies and only one of them belongs to this skill:

- **Invariants a type's shape can carry.** "At least one line" is structural — a collection defined as one element plus the rest cannot be empty. "Either provisioned with a firmware version, or unprovisioned with none" is structural too, once the states are separate types. These need no runtime check, no command to guard them, and no test. Encode them and they are gone. That work is `make-illegal-states-unrepresentable`.
- **Invariants that span several objects, or depend on data outside any one of them.** "The order total equals the sum of its lines." "A device cannot join a fleet already at capacity." These cannot be encoded in a shape; they need a boundary that owns them and a command that enforces them. Those are the ones this skill is about.

Doing the first pile first is worth the detour: it usually shrinks the second pile substantially, and an invariant that no longer exists is cheaper than one enforced correctly.

## Step 3 — Draw the boundary with the strong-consistency test

Keep aggregates as small as the invariants allow. Include only the data the aggregate's own logic requires to be **strongly consistent**; everything that may be eventually consistent belongs outside, in another aggregate, referenced by id.

The test is concrete, and it is applied per piece of data:

> Would this logic be able to reach a state the business calls invalid if this data were stale?

If yes, it is inside. If no, it is referenced by id.

**A worked case.** A ticket is reassigned automatically if the agent has not read new messages within half the response window. Suppose read-acknowledgements were eventually consistent — a delay of some seconds before a read registers. Then a large number of tickets would be reassigned when in fact the agent had read them. That is state corruption, so the messages belong inside the ticket's boundary. The customer, the assigned agent and the related products are not read by any rule with that property, so they are referenced by id.

Referencing outside aggregates by id is deliberate on both counts: it makes the boundary visible in the code, and it keeps each aggregate's transaction scope separate.

**Oversized aggregates cost real money.** Everything inside shares one transaction, so a boundary that grew past its invariants produces contention and slow writes. If an aggregate is getting slow, apply this test again before optimising anything.

## Step 4 — Make it a consistency enforcement boundary

Everything outside may read the aggregate's state. Nothing outside may write it.

State changes happen only by executing **commands** on the aggregate's public interface, and those commands validate their input and enforce every relevant rule and invariant. The payoff is that all business logic for the concept lives in exactly one place — which is the actual reason for the rule, not encapsulation as an aesthetic.

The surrounding orchestration layer then shrinks to four lines: load, execute one command, persist, return the result.

```
load the aggregate
execute the command            # all rules and invariants enforced here
persist
return the result — or a concurrency failure the caller can retry
```

**One aggregate instance per transaction.** All changes to an aggregate commit atomically, and no operation may assume a transaction spanning more than one instance.

This is not merely a rule to obey — it is a design instrument. **When you find yourself needing to commit changes to several aggregates together, that is evidence the boundary is drawn in the wrong place.** Take it as a finding about the model rather than an obstacle to route around.

## Step 5 — Designate the root

An aggregate is a hierarchy of entities and value objects bound together by the domain's logic, and exactly one entity is its public interface. Operations that modify an inner entity are still invoked on the root; inner entities are never reached directly from outside.

Membership is decided by the business logic binding the objects together, not by what is convenient in the data model.

## Step 6 — Add concurrency control

When two processes update the same aggregate concurrently, the second must not blindly overwrite the first. It has to be told the state its decisions were based on is out of date, and retry.

The minimum mechanism is a version on the aggregate, incremented on every update, with the write applying only where the stored version still matches the one that was read. The storage you choose must support this.

Without it, the second writer silently destroys the first writer's change — including, potentially, an invariant check that passed against data that no longer exists.

## Step 7 — Place the logic that fits nowhere

Some logic belongs to no single aggregate, or genuinely spans several. Put it in a **stateless object** whose job is to orchestrate reads and perform a calculation.

Computing a response deadline, for instance, may need the ticket's priority and escalation state, the department's SLA policy, and the agent's upcoming shifts — three sources, so it belongs in a service rather than being forced into any one aggregate.

This is **not a loophole around one-instance-per-transaction.** That limit still holds. These services read across aggregates; they do not write across them.

For a business *process* spanning several aggregates — where each step triggers the next and failures need compensating — the answer is a saga, not a bigger aggregate. Do not merge entities with different responsibilities just to make a transaction fit. See `model-lifecycle-and-events`.

## Why invariants reduce complexity rather than adding it

Complexity is the difficulty of controlling and predicting behaviour, and it is measured by **degrees of freedom**: how many data points you need to describe the state.

A class with five independent public fields has five degrees of freedom. A class with the same five fields, where three are derived from the other two, has **two** — and is less complex, despite containing more code.

This is counterintuitive and worth holding onto, because the objection to encapsulating rules is almost always that it adds code. It does. It also removes independent ways for the state to be wrong, and that is what complexity actually is.

To use it as a check: count the values needed to fully describe the state, identify which are derivable from others, move each derivation inside the boundary that owns it, and recount. The drop is the complexity you removed.

## Keep infrastructure out

The domain's logic is already complex, so the objects modelling it must add no accidental complexity: no database calls, no framework dependencies, no technological concerns inside the model.

That is not purism. Keeping infrastructure out is what makes it possible for the aggregate's name, its fields, its commands and its events to be stated in the domain's own language, so the code reads the way the business talks. That in turn is what lets a domain expert confirm or correct a rule by reading it.

Names come from the glossary — see `build-domain-glossary`.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Two rows with identical values compare unequal | An identity field was added to a value concept | Remove the id; compare by value |
| Validation for the same field duplicated across the codebase | Primitives standing in for domain concepts | Move validation into a type that parses on construction |
| A transaction must write two aggregates | The boundary is in the wrong place | Redraw it — or make the flow a saga |
| The same rule implemented in several places | State is mutable from outside the boundary | Private state; commands only |
| An aggregate has grown; writes are slow or contended | It holds data that not all its logic needs strongly consistent | Re-apply the strong-consistency test and extract |
| The second writer silently overwrites the first | No concurrency control | Version field plus conditional write |
| Invariants pass in tests, fail in production | They are enforced in the caller, not the aggregate | Move them inside the boundary |
| Rich objects wrapping simple create-read-update-delete | Machinery applied where the logic is trivial | Use a simpler pattern — see `choose-business-logic-pattern` |

## A note on pragmatism

Consistency guarantees are a business decision, not an absolute. Before engineering full transactional integrity, price the failure: corrupting one record in a million may be irrelevant, and at high ingest volumes losing or duplicating a thousandth of a percent of events may cost nothing.

The licence here is to *decide*, not to skip deciding. Evaluate the business implications, then cut the corner deliberately and write down that you did.

## Bundled references

- `references/refactoring-to-aggregates.md` — the compiler-first migration from setter-driven objects into aggregates, in order, and what to do when the logic already spans several codebases. Read when an entity model already exists and has to be reshaped.

## Related

Before drawing consistency boundaries, run the entity's own fields through `make-illegal-states-unrepresentable`. A field that cannot hold a contradictory value is one fewer thing for an aggregate to guard, and flags governing other fields — the commonest source of a corrupt entity — are better removed structurally than defended at runtime.

## Worth reading

- Eric Evans, *Domain-Driven Design* (2003) — the origin of these building blocks.
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013) — extended worked examples of aggregate design.
