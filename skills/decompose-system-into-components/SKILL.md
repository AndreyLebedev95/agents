---
name: decompose-system-into-components
description: Breaks a system into components and services and gets the sizes right — the part where decomposition actually goes wrong. Covers the identification loop, granularity as distinct from modularity, connascence as a precise coupling vocabulary with a refactoring direction, cohesion, why the Law of Demeter redistributes coupling rather than reducing it, the Entity Trap, and service granularity — transaction scope, data isolation, database-per-service, and when to merge services back together. Use whenever someone is deciding what the components, modules or services should be, whether to split or merge one, how big a microservice should be, where data should live, whether services should share a database, or why services are chattering. Use it when a monolith is being decomposed, when a component has grown unwieldy, when someone proposes a CustomerManager-style component, or when a cross-service transaction is being designed. Use it even when the request is only "how should I structure this" or "should this be one service or several". For the overall style use choose-architecture-style; for which characteristics drive the design use elicit-architecture-characteristics; for enforcing the structure use govern-architecture-with-fitness-functions.
---

# Decomposing a system into components

Two questions look like one and are not. **Modularity** is whether to break a system into smaller pieces. **Granularity** is how big those pieces are. Deciding to decompose is rarely the mistake; sizing the pieces is.

Embrace modularity, but beware of granularity. Wrong piece-size is what couples components and services to each other and produces spaghetti architecture, distributed monoliths, and the big ball of distributed mud. Rising coupling *between* pieces is the signal that granularity, not modularity, is wrong.

## The output

A logical architecture — what the system does, how the functionality is demarcated, and how the parts interact. Independent of deployment: do not decide monolith or services here.

```
## <Component name>
Responsibility: <one prose statement — see the conjunction test>
Assigned:       <user stories / requirements>
Characteristics:<what this part specifically demands>
Talks to:       <components, and in which direction>
Owns:           <data, where relevant>
Granularity rationale: <why this boundary and not a bigger or smaller one>
```

Build this before the physical architecture. Skipping to the physical view is common and damaging: it does not show where functionality lives — payment processing may be smeared across several services — and it gives teams no guidance on organizing code, which produces unstructured systems that are hard to maintain, test and deploy.

A useful consequence: because components are realized as namespaces or directories, the logical architecture of an existing system can be read straight off its directory tree. Leaf source directories are components; their parents are subdomains.

## Procedure

### 1. Identify initial components as empty buckets

The common mistake is trying to get the initial components right at the exact moment you know least about the system. Make a best guess from the core functionality and let the loop correct it.

An initial component is an empty bucket: its name states a proposed role, and it holds nothing until stories are assigned. You usually do not need all — sometimes not any — of the requirements to start.

Two approaches:

**Workflow.** Write the major happy-path workflow as numbered steps and name a component for each step's function. Collapse repeated functions onto one component — "email order details" and "email shipment notice" both map to a notification component. Repeat for the other major journeys, then stop. Do not attempt to model every workflow.

**Actor/Action.** List the human actors and add *the system itself* as an actor, since it performs automated functions like billing and stock replenishment. List each actor's major actions and name a component per action's function, collapsing related ones. This generally produces more components than the workflow approach, and it is the right generic default when the team has no special constraints.

### 2. Assign user stories

Fill the buckets. Assign each story to the component the user interacts with, or that owns the logic.

When no single component fits and three would each need the same code, that is the signal to create a fourth. The story is implemented as source code that has to live in one directory; replicating it across three components is worse than adding one.

### 3. Run the responsibility-statement test

Write each component's role and responsibility as one prose paragraph covering everything assigned to it. Then look for conjunctions — *and*, *also*, *in addition*, *as well as* — and heavy comma series.

Each conjunction marks a responsibility that probably belongs elsewhere. This turns an otherwise subjective cohesion judgment into something checkable on a piece of text.

> This component is responsible for validating the order and displaying the valid shopping cart, complete with item picture, description, quantity and price. This component is **also** responsible for determining the correct shipping address, **as well as** collecting payment information. **In addition**, it's **also** responsible for applying the payment, adjusting inventory, **and** emailing the customer the order summary.

Everything after "in addition" became three separate components.

### 4. Re-cut on characteristics

Functional analysis groups work by what it *does*. Characteristics analysis splits it by what it *needs*. Both matter, and the second is the one that gets skipped.

Two parts of a system that both handle user input belong in one component functionally. If one serves thousands of concurrent users and the other a handful, they need different characteristics and should be separate.

A worked case: bid capture in an auction system handles bids from both bidders and the auctioneer, and functionally that is one thing. But bidders may number in the thousands and need scalability and elasticity, while the auctioneer needs reliability and availability — a dropped bidder connection is bad, a dropped auctioneer connection is disastrous. Two components.

Because of this, component design has to come *after* the important characteristics are known.

### 5. Loop

Identify → assign stories → analyze roles and responsibilities → analyze characteristics → refactor by splitting or combining → repeat. The loop never stops. It runs on greenfield systems and again every time a feature is added or changed, because changing responsibilities can force restructuring.

Expect to restructure frequently, in new systems and in maintained ones. It is virtually impossible to anticipate the discoveries and edge cases that will arise, and understanding of where behaviors belong deepens as the system is built.

## Assessing coupling precisely

"This is coupled" is not actionable. **Connascence** gives it a vocabulary with a direction: two components are connascent if a change in one requires the other to change to keep the system correct.

Name the form, then read three properties together — see `references/connascence.md` for the full taxonomy:

- **Strength** — how easily the coupling can be refactored away. Prefer static (visible in source) to dynamic (existing only at runtime), because static forms are findable by source analysis and trivially improved by tooling.
- **Locality** — how close the coupled elements sit. The same form is acceptable inside one module and a smell across module boundaries.
- **Degree** — how many elements one change touches. Strong coupling over few modules is survivable, but code bases grow, which turns a small degree problem into a large one.

Only the combination that is strong *and* distant *and* high-degree is urgent. Strong-but-local is fine — in fact desirable.

The program: minimize overall connascence by encapsulating; minimize what crosses encapsulation boundaries; and **maximize connascence within** boundaries. That third rule is the counterintuitive one. Then: convert strong forms into weaker forms, and as distance between elements increases, use weaker forms.

The general principle underneath: **couple tightly in narrow scopes and loosely in broad ones.** Tight coupling is desirable where high cohesion is required. An architecture is brittle when one implementation change ripples into ostensibly unrelated places — renaming a field from `State` to `StateCode` in the belief it affects one caller, and breaking many.

## Before splitting anything, check cohesion

Dividing a module whose parts genuinely belong together only increases coupling and decreases readability, because the parts must now call each other across a boundary to do anything useful. The split converts cohesion into coupling.

Three questions before extracting:

1. Does the candidate new module have enough operations to justify existing, or would it collapse back?
2. Is the original expected to grow much larger? Growth pressure justifies extraction that current size does not.
3. Would the extracted module need so much knowledge of the original's data that separating them forces high coupling?

`references/cohesion.md` has the seven-point cohesion scale for naming what actually holds a module together.

## Knowledge is coupling

A component should have limited knowledge of other components. The part that gets missed: *knowing that something must happen is itself coupling*, even when the component does not do it.

An order-placement component that knows inventory must be decremented, stock may need reordering, prices may need adjusting and an email must go out is highly coupled to all four, despite performing none of that work.

Push each item of knowledge down to the component that owns the trigger. But check the arithmetic afterwards: this **does not reduce system-wide coupling, it redistributes it** — the receiving component's coupling rises by what the sender's fell. And adding a component purely to relay a call does not reduce the caller's outgoing coupling at all, so that coupling point has to stay.

## Service-level granularity

Once the pieces are separately deployable, the trade-off sharpens and becomes explicit:

**Coarse-grained services** buy data integrity — a business transaction stays inside one service, so ordinary transactions with commits and rollbacks protect it. They cost deployment isolation: changing order placement inside a combined service means testing and redeploying payment processing too, and a larger deployment carries more risk of breaking something unrelated.

**Fine-grained services** invert both. A change touches one single-responsibility service and nothing else is retested or redeployed. Transactional integrity is what you give up.

Decide which you need. That *is* the decision, not a detail of it.

Three guides to boundaries, then iterate:

- **Purpose.** Each service should be functionally cohesive, contributing one significant behavior.
- **Transactions.** The entities that must cooperate in a transaction usually mark a good boundary. Since distributed transactions cause trouble, designing to avoid them tends to produce better designs anyway.
- **Communication volume.** A set of services with excellent domain isolation that requires extensive communication to function should be considered for bundling back into a larger service.

Nobody finds the right granularity, data dependencies and communication style on the first pass. Iteration is the only route to good service design.

### Do not span transactions across services

A transaction crossing service boundaries violates decoupling and creates the worst form of runtime coupling — values in several places that must all change together. **Needing transactions to wire the architecture together is the signal that the services are too granular.** Fix the granularity first.

Only where two services genuinely need very different characteristics *and* still need coordination does a saga apply, with explicit compensating transactions. If cross-service transactions become the dominant feature of the architecture, the whole style is wrong.

### Data ownership follows the boundary

Where bounded contexts are the point, each service owns its data and others request it through a contract rather than reaching the structure. A schema change then affects only the owning service, and the database technology can change without touching anyone.

The realistic exception: where services write the same tables, or an outside service must query directly for performance, up to **five or six** services may share a database, forming a broader bounded context rather than none at all. Beyond that the change-control, scalability, availability and fault-tolerance problems return.

`references/service-granularity.md` covers transaction scope, sagas, data topologies and the sharing thresholds in full.

## Reuse and duplication

Reuse is implemented via coupling. That is not a criticism of reuse; it is the mechanism, and it means you cannot have both high decoupling and high institutional reuse. Two factors decide whether reuse pays:

- **Abstraction** — can this be abstracted and called from multiple points? Architects find this one.
- **Low volatility** — this is the one that gets missed. Reusing code that keeps changing creates churn through the whole system, because every change forces all callers to coordinate, and even a non-breaking change must be verified everywhere.

So the successful reuse targets are plumbing — frameworks, libraries, platforms. The domain, which changes fastest and is the reason the software exists, is a terrible reuse candidate. In a bounded-context architecture, prefer duplication over coupling deliberately.

A second cost of a shared canonical entity: it must carry every attribute any consumer needs, so every consumer inherits complexity it does not want.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Components named Manager, Handler, Processor, Engine, Supervisor, Controller | Entity Trap — derived from entities | Rename to the action performed; split the dumping ground |
| Responsibility statement full of "and", "also", "in addition" | Doing too much | Extract the trailing clauses |
| Services need transactions between them | Too granular | Merge; saga only if characteristics truly differ |
| Services constantly calling each other | Boundaries wrong — not a plumbing problem | Redraw the domains or merge |
| Every capability became a separate service | Jumped straight from monolith to fine-grained | Coarse domain services as a stepping stone |
| One schema change redeploys everything | Shared entity library or shared database | Partition the data; mirror with per-domain libraries |
| Module boundaries dissolved over time | Over-reuse across boundaries | Duplicate across boundaries, reuse inside |
| Splitting made things worse | Split a cohesive module | Run the three cohesion questions first |
| One component knows everything that must happen | Knowledge is coupling | Push knowledge down; check the receiver's new level |
| Structure invented ad hoc by developers | No logical architecture published | Publish it; govern the source tree against it |
| Ordering bug that no tool can find | Temporal coupling | Document ordering constraints deliberately |
| Changes take too long; one change breaks elsewhere; people collide; slow startup | The monolith outgrew its size | Those four signs together mean decompose |

## The Entity Trap

Deriving components from domain entities — `Customer Manager`, `Item Manager`, `Order Manager` — fails three ways:

1. **The names are ambiguous.** Asked what `Order Manager` does, the only answer is "it manages orders". Compare `Validate Order`.
2. **They become dumping grounds.** Every scrap of order functionality lands in one component: validation, placement, history, fulfilment, shipping, tracking. The kitchen-sink utility class, at architecture scale.
3. **They grow too coarse-grained,** doing too much and becoming hard to maintain, test and deploy.

The tell is a name ending in Manager, Supervisor, Controller, Handler, Engine or Processor.

One honest exception: if the system genuinely is CRUD over entities and nothing more, it does not need an architecture at all. It needs a CRUD framework or a low-code environment that generates the code.

## When to reach for a reference

- `references/connascence.md` — the full taxonomy weakest to strongest with recognition cues and examples, the three properties, and the improvement rules. Read when assessing or discussing coupling precisely, or in code review.
- `references/cohesion.md` — the seven-point cohesion scale with cues, and using lack-of-cohesion metrics to find classes that were never one class. Read when judging whether a module's parts belong together.
- `references/service-granularity.md` — coarse versus fine trade-offs, transaction scope and sagas, data ownership topologies with thresholds, operational-versus-domain reuse, and migration sequencing. Read when the decomposition is at service rather than component level.

## Further reading

- *Domain-Driven Design*, Eric Evans — bounded contexts and the modelling technique underneath domain partitioning.
- *Building Microservices* (2nd ed.), Sam Newman — service decomposition in depth.
- *Software Architecture: The Hard Parts* — a full chapter on service granularity, and eight distinct transactional saga patterns for the cases where a saga is genuinely warranted.
