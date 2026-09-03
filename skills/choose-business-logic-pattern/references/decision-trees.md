# The decision trees, written out

Read when applying the decision to a concrete area. Contents: [logic pattern](#tree-1-business-logic-pattern) · [architecture](#tree-2-codebase-organisation) · [testing](#tree-3-testing-emphasis) · [worked examples](#worked-classifications) · [exceptions](#the-exception-cases)

## Tree 1: business logic pattern

```
Does this area track money or monetary transactions,
owe a consistent audit log, or need deep analysis of its own behaviour?
├── yes ──> EVENT-SOURCED MODEL
└── no
    │
    Is the business logic complex?
    (complicated rules, invariants, algorithms — not input validation;
     language describing processes and rules — not create/read/update/delete)
    ├── yes ──> DOMAIN MODEL
    └── no
        │
        Are the data structures complex?
        (hierarchies, one-to-many and many-to-many relationships whose
         mapping would otherwise be duplicated across every procedure)
        ├── yes ──> RECORD OBJECTS
        └── no  ──> PROCEDURAL SCRIPTS
```

**Stop at the first yes.** Question 1 outranks question 2: an area with simple logic that must produce a legally required audit trail still needs events, and its simplicity is irrelevant to that requirement.

### What each answer commits you to

| | Rules live in | State changes via | Typical fit |
|---|---|---|---|
| Procedural scripts | one procedure per operation | direct writes, transactionally | extract-transform-load, adapters, translation layers |
| Record objects | procedures over objects that own their persistence | public accessors | data-entry areas with awkward schemas |
| Domain model | inside aggregates | commands enforcing invariants | areas the business competes on |
| Event-sourced model | inside aggregates | commands appending events | money, audit, behavioural analysis |

**Non-negotiable:** procedural organisation must never carry an area the business competes on. Its rules duplicate across procedures and the copies drift, in exactly the code that changes most often.

## Tree 2: codebase organisation

```
Event-sourced model ──> segregated read models (required)
Domain model        ──> infrastructure-inverted, logic at the centre
Record objects      ──> layers + an application service layer
Procedural scripts  ──> minimal layers
```

Plus one orthogonal rule:

```
Does this area need the same data in several persistent models?
(operational store + search index + reporting store + prerendered views)
└── yes ──> add read-model segregation, whatever the logic pattern
```

**Why segregation is required, not advised, for event-sourced models:** without projections you can only fetch the events of one instance at a time. There is no way to query across instances by state — "all rollouts currently halted" is unanswerable. Projections are what restore querying.

**Why a domain model needs inverted dependencies:** aggregates and value types must have no knowledge of persistence. Top-down layering, where the logic layer depends on the data-access layer, forces workarounds to achieve that. It is possible; it just fights you continuously.

## Tree 3: testing emphasis

```
Domain model or event-sourced ──> PYRAMID       (mostly unit)
Record objects                ──> DIAMOND       (mostly integration)
Procedural scripts            ──> INVERTED      (mostly end-to-end)
```

The reasoning in each case is about **where the logic actually is**:

- In a domain model it is inside aggregates and value types, which are ideal units — self-contained, no infrastructure, fast, and testing them tests the rules directly.
- With record objects it is split across the service layer and the objects themselves. Neither side is meaningful alone, so the seam between them is where the defects are, and integration tests cover that seam.
- With procedural scripts the logic is simple and the layers are few. There is little to unit-test in isolation, and verifying the whole flow end to end is the efficient check.

## Worked classifications

**A device update lifecycle, where the business needs to analyse failure patterns and optimise the rollout algorithm.**
Q1: deep analysis of its own behaviour → yes. **Event-sourced model**, segregated read models, testing pyramid. The analysis requirement alone settles it; the complexity of the rules never gets asked.

**Managing a tenant's list of product categories.**
Q1 no, Q2 no — creating and renaming categories is validation. Q3: a shallow list → no. **Procedural scripts**, minimal layers, end-to-end tests.

**Entering support agents' work schedules — shifts, rotations, coverage per region.**
Q1 no. Q2: is scheduling complex, or is it data entry? If the system only records what a manager decided, it is data entry. If it *computes* coverage and enforces rules about consecutive shifts, it is complex. Q3: the structures are nested regardless. So: **record objects** if it records, **domain model** if it decides. This is the boundary case where the two complexity tests earn their keep.

**Pulling public holidays from an external provider on a schedule.**
Q1 no, Q2 no, Q3 no. **Procedural scripts** — this is a translation layer, one of the natural homes for procedural organisation. Test it end to end against a recorded response.

**A promotions module: coupon codes, validity windows, active flags.**
Q1 no — no money moves here, it only marks eligibility. Q2: if it is a management screen over coupon records, no. **Record objects**. But note how close Q1 is: if the module started *computing discounts applied to transactions*, the answer changes.

## The exception cases

**Team fluency.** A team experienced with event-sourced models may use them everywhere, because for them it is the simplest option and switching between patterns costs more than the uniformity saves. This is legitimate and is not general advice — it depends on that team actually having the fluency.

**Non-technical core.** An area can be what the business competes on while the software around it is trivial. A manual fraud-analysis operation may be entirely core, while the system the analysts use just displays documents and records comments — a supporting-shaped system serving a core business capability. The pattern follows the software's complexity; the strategic classification follows the business.

**Consistency requirements are negotiable.** Before engineering full transactional integrity, price the failure. Corrupting one record in a million may cost the business nothing, and at high ingest volumes losing a thousandth of a percent of events may be irrelevant. Deciding to cut that corner is legitimate; failing to decide is not.

**Everything can change later.** The trees give a starting point, not a permanent commitment. Areas change strategic type, and the design should follow. The signal that it needs to is that adding functionality has become painful.
