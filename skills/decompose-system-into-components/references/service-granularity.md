# Service granularity

Read when the decomposition is at service level rather than component level — when the pieces will be separately deployed.

## Contents
- [The core trade-off](#the-core-trade-off)
- [Transaction scope](#transaction-scope)
- [Sagas and compensating transactions](#sagas-and-compensating-transactions)
- [Data ownership topologies](#data-ownership-topologies)
- [The shared-library antipattern](#the-shared-library-antipattern)
- [Domain reuse versus operational reuse](#domain-reuse-versus-operational-reuse)
- [Migration sequencing](#migration-sequencing)
- [Risks that all reduce to granularity](#risks-that-all-reduce-to-granularity)

## The core trade-off

Stated exactly, because this is the decision and everything else is detail:

| | Coarse-grained | Fine-grained |
|---|---|---|
| Transactional integrity | Business transaction stays inside one service; ordinary commits and rollbacks work | Transaction spans boundaries; eventual consistency and compensating updates |
| Deployment isolation | Changing one capability means testing and redeploying the others in the same service | A change touches one single-responsibility service; nothing else is retested |
| Blast radius | Larger deployment, more risk something unrelated breaks | Small, contained |

Worked contrast. A customer pays with an expired card. Inside one service, the whole insert rolls back and the customer is told. Split across an order service and a payment service, the order row is already inserted and unapproved, the data is inconsistent, and a compensating update is needed to repair it.

## Transaction scope

Coarse services get atomicity for free — ordinary database transactions with standard commits and rollbacks. Fine services must use eventual consistency: basic availability, soft state, and updates that converge rather than complete together. Fine-grained services cannot deliver the integrity a coarse-grained service gets for nothing.

The practical procedure:

1. Identify the business transactions that must be atomic.
2. Check whether each falls inside a single service boundary.
3. Where it does not, design the compensating path explicitly and accept eventual consistency.
4. Treat required atomicity as an argument for coarser services.

## Sagas and compensating transactions

Where two services genuinely need very different architecture characteristics *and* still require transactional coordination, a mediator can coordinate: it calls each participant, records success or failure, and on partial failure instructs every successful participant to undo.

Implementation typically holds each request in a pending state until the mediator signals overall success. Two warnings. Juggling asynchronous requests this way becomes complex quickly, especially when new requests arrive that depend on pending transactional state. And compensating transactions generate substantial coordination traffic at the network level.

A third, less obvious warning: **compensating updates are assumed to always work, and they do not.** A transactional workflow design must also state what happens when the update *and* its compensating update both fail.

The advice that precedes all of this: don't. Fix the service granularity instead. Multiple distinct saga patterns exist for different scenarios, and needing to choose between them is usually a sign the boundaries are wrong.

## Data ownership topologies

Three options, in increasing isolation.

**Shared/monolithic.** All services reach one database. Any service gets the data it needs directly with no synchronous call to another service — genuinely valuable in an asynchronous architecture. Costs: a database outage takes everything down; the database must scale to the combined concurrent load of independently scaling services, which many cannot; a schema change forces coordination across every service; and the shared database collapses everything into one unit for characteristics purposes, whatever the deployment diagram shows.

**Domain-grouped.** Services grouped into domains, one database each. Better fault tolerance — one domain's database failing leaves the others working, with the message channel queuing — plus scalability and change control scoped per domain. Cost: a service sometimes needs data from another domain and must call it synchronously.

**Per-service.** Highest fault tolerance, scalability and change control: an outage isolates to one service, a schema change touches one service, and the database *type* can change — relational to document, say — without affecting anyone. Costs: potentially expensive depending on the technology stack, and the most synchronous coupling of the three.

**Choosing.** Identify every data requirement of every service *before* choosing the topology — that is the deciding input, and it is the step that gets skipped. Prefer per-service only where services are mostly self-contained within their own bounded context. If services need too much synchronous communication, reevaluate the domain boundaries, combine domains, or move up to a shared topology. Weigh against change frequency: frequent schema change argues for narrower topologies even at operational cost.

**The sharing threshold.** Where services write the same tables, or an outside service must query directly for performance, up to **five or six** services may share a database or schema. That is a broader bounded context, not the absence of one. Beyond five or six, the change-control, scalability, elasticity, availability and fault-tolerance problems return in full.

Legitimate cases for sharing: payment processing split by payment type, or shipping split by shipping method — separate services that genuinely update and read the same data.

**Establishing truth.** With data distributed, decide explicitly how truth is established: nominate one domain as the source of truth for a fact and coordinate with it, or distribute through replication or caching. Do not leave this implicit.

**The upside.** Freed from one database, each team picks the storage suited to its own budget, structure, and operational and process characteristics — and can change it later without affecting anyone, because nobody is allowed to couple to implementation details.

## The shared-library antipattern

Where every service depends on a single shared library of database entity objects, any table change forces a change to that library and therefore a redeploy of every service — including services that never touch the changed table. Versioning helps a little; without detailed manual analysis nobody can tell which services a table change actually affects.

The fix:

1. Logically partition the database into well-defined data domains.
2. Publish one shared library per partition, matching exactly.
3. A table change then affects only the services using that partition's library.
4. For the unavoidable common partition everyone uses, lock those entity objects in version control so only the data team changes them.
5. Make the logical partitioning as fine-grained as possible while keeping the data domains well defined.

## Domain reuse versus operational reuse

A bounded-context architecture prefers duplication to coupling for domain concerns. But some things genuinely benefit from coupling: monitoring, logging, circuit breakers, authentication, service discovery.

Resolve this by splitting the two kinds of reuse rather than picking one policy for both. Put operational concerns into a component present in every service, owned by a shared infrastructure team, so upgrading the monitoring tool means updating one thing rather than negotiating with every service team. Connecting those components through a common control plane gives unified global control over cross-cutting operational concerns.

The trade-offs of that approach: it needs one implementation per platform, so a polyglot estate needs several; the shared component tends to grow large and complex over time; and independent teams produce drift between their copies.

This is an orthogonal concern — one with a distinct, independent purpose that must nonetheless intersect with the domain structure to form a complete solution. Recognizing orthogonality is what lets you find the intersection point causing least entanglement, rather than forcing the concern into a hierarchy where it does not fit.

## Migration sequencing

Going straight from a monolith to fine-grained services makes every piece of functionality a service, whether or not it needs to be one.

Move first to coarse-grained domain services. That intermediate step lets the team see which domains actually demand fine granularity. In a recycling business, accounting and recycling should stay domain services permanently; device assessment, which changes with every new device model and needs high agility, should split into one service per device type. Skipping the step means both get split.

**Not every portion of an application needs to be fine-grained.**

Two things make the exit easier if you are starting from a monolith you expect to distribute later: separate the database tables and other data assets along the same lines as the domain components, and keep code reuse minimal with shallow inheritance trees.

## Risks that all reduce to granularity

Four common failures, three of which are the same failure:

- **Services too small.** Grains of sand on a beach. The prefix refers to what the service does, not how big it is.
- **Excessive interservice communication.** Fine granularity plus tight bounded contexts guarantees some communication, whether for workflow or for another service's data. Too much is the same granularity error, fixed by combining services.
- **Excessive data sharing.** Sometimes necessary; too much damages change control, scalability, fault tolerance and agility — the things the style does well. Fix by consolidating services.
- **Code reuse through shared libraries.** Sharing functionality through custom libraries puts part of a bounded context outside it, so a change to shared code can break services in other contexts. Versioning mitigates and does not remove it.

Treat chatter, over-sharing and shared-library sprawl as symptoms of one underlying error. Consolidate services rather than optimizing the communication between them.
