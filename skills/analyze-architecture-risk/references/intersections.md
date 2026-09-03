# The nine intersections

Read when validating an architecture rather than scoring risk. Each one is a yes/no alignment question. Where the answer is no, the architecture does not work yet, however good the design.

## Contents
- [1. Implementation](#1-implementation)
- [2. Infrastructure](#2-infrastructure)
- [3. Data topologies](#3-data-topologies)
- [4. Engineering practices](#4-engineering-practices)
- [5. Team topologies](#5-team-topologies)
- [6. Systems integration](#6-systems-integration)
- [7. The enterprise](#7-the-enterprise)
- [8. The business environment](#8-the-business-environment)
- [9. Generative AI](#9-generative-ai)
- [Availability conversion](#availability-conversion)

## 1. Implementation

*Does the code deliver the characteristics the architecture assumed?*

Three sub-checks: operational concerns, structural integrity, and constraints.

**Operational concerns.** The damaging misalignment is not a bad decision on either side but **two good decisions aimed at different goals**.

Worked case: a microservices order system needing up to half a million concurrent customers. Tight bounded contexts forced order placement to call inventory synchronously, hurting responsiveness and coupling the two — so the team introduced an in-memory replicated cache. It worked. At around 80,000 concurrent customers the cache's memory requirements produced out-of-memory conditions across all the virtual machines and the system crashed. The architecture optimized for scalability and elasticity; the implementation optimized for responsiveness and decoupling. Nobody did anything obviously wrong.

The check: state which characteristics the architecture was chosen to deliver, in writing, where the implementation team can see them. When the team solves a problem, ask which characteristic the solution optimizes and whether it trades away a driving one. Treat any local optimization consuming a resource that scales with instance count as a scalability decision, not a performance one.

**Structural integrity.** Because logical components are realized as directory structures or namespaces, the source repository's structure **is** the logical architecture. Without guidance, knowledge and governance, developers create directories and namespaces as they please, producing an architecture that is difficult to maintain, test and deploy, and therefore less reliable and harder to evolve. Enforce with automated governance tooling plus communication between architect and team.

**Constraints.** A constraint is a governing rule describing a restriction required for the architecture to achieve its goals — limiting communication to one protocol, requiring a specific database type. If the implementation does not adhere, the architecture fails, so identifying and communicating constraints is part of the job.

Worked case: a layered architecture chosen for a tight budget and frequent database change needs two constraints — all database logic resides in the persistence layer, and the presentation layer must traverse all layers rather than reaching persistence directly. UI developers calling the database directly for speed, and backend developers merging business and database logic for easier maintenance, each ignored one. The database changes the style was chosen to make cheap now touch every layer.

## 2. Infrastructure

*Can the deployment actually provide the operational characteristics?*

**Capability in the style is not delivery in the system.** Architects are routinely blamed for architectural failures actually caused by this gap, and the cause is almost always a lack of communication with the people who run it. This gap is what produced the DevOps movement.

The historical lesson: an ecommerce site of 1998 spent heavily on a famous mascot and not on infrastructure. When orders arrived the site was slow, transactions were lost and deliveries were delayed; it closed after a disastrous Christmas rush, selling the mascot as its last valuable asset. Too much success can kill a business, and that lesson is what produced elastic scale.

The deeper point from the microservices era: **operational concerns are handled better by operations.** Older styles built scalability, performance and elasticity into the architecture itself and became vastly more complex as a result. A collaborative relationship with operations lets architects simplify their designs and delegate what operations does best.

Two cloud placement choices that silently invert characteristics:

- Deploying services **across regions, or even availability zones**, can decrease or entirely cancel the performance and data-integrity benefits of in-memory replicated caches and distributed caches.
- **Co-locating** services, containers or pods on the same virtual machine significantly increases performance and adversely affects scalability, fault tolerance, availability and elasticity.

Check: verify with the infrastructure team that each operational characteristic the design assumes is actually provided. Treat a strong rating on a style as a ceiling infrastructure can lower.

## 3. Data topologies

*Does the database type and topology match the style?*

Choosing wrong negates the architecture's best characteristics. Monolithic databases give consistency and transactional support and cost scalability and fault tolerance. Distributed topologies give scalability and change control and cost data integrity, consistency and performance.

Four axes to check, in order:

1. **Topology fit.** Fine-grained service architectures need database-per-service to hold the bounded context; without it, change control becomes extremely hard and fault tolerance, scalability, elasticity, maintainability, testability and deployability all suffer. Coarse-grained service architectures are far more flexible.
2. **Strength matching.** Align the database type's strengths with the architecture's. Scalability and elasticity are strengths of microservices, event-driven and space-based architectures — and also of key-value and columnar databases.
3. **Data structure.** Relational data fits a relational database. Key-value pairs in a relational database is a misalignment that makes both inefficient. JSON event or request payloads fit a document store. Because structures vary within one architecture, prefer polyglot databases where feasible.
4. **Read/write priority.** High write volume over infrequent reads favours columnar. High read volume favours key-value, document or graph. Roughly equal favours relational or NewSQL.

## 4. Engineering practices

*Do the team's practices and pipeline support this style?*

Separate two things. **Process** is how teams are formed and managed, how meetings are conducted and workflows organized — the mechanics of how people organize. **Engineering practices** are the process-agnostic techniques and tools for developing and releasing: continuous integration, continuous delivery, test-driven development.

Architecture is largely separable from process and **not** separable from engineering practices. A style presumes a level of practice: a philosophy that assumes automated machine provisioning, testing and deployment will likely fail against a manual operations group and little testing.

Process still matters at the margin. Iterative processes fit architecture's nature better — building a modern distributed system under a heavyweight sequential process creates a great deal of friction. Agile methods shine particularly when *migrating* between styles, because tight feedback loops and techniques like incremental replacement and feature toggles support gradual change better than planning-heavy processes.

Check: list the practices the style presumes, check each against what the organization actually does today, and either raise the practice or choose a style the practice can support.

Misalignment here is measurable rather than merely noticeable. A business need for fast time to market translates to agility, which decomposes into maintainability, testability and deployability — all three influenced by engineering practices and all three measurable. When those numbers refuse to move, treat it as an alignment problem rather than an implementation one.

An honest note about why this is hard: software development's Achilles' heel is estimation, because traditional estimation practices do not accommodate the exploratory nature of the work or the unknowns that arise while building. Civil engineers can predict structural change far more accurately than software engineers can predict the equivalent.

## 5. Team topologies

*Can this team structure produce and maintain this architecture?*

Teams, like architectures, are domain-partitioned or technically partitioned, and the two must agree.

A **domain-partitioned team** owns a domain area end to end, from UI to database, cross-functional with specialization inside it. **Technically partitioned teams** each own one technical function — UI teams, backend-processing teams, shared-services teams and database teams align neatly with layered architecture, while business-function teams and data-synchronization teams align with space-based architecture.

Where the team topology is misaligned, teams struggle to implement and maintain the architecture and the system is unlikely to meet its business goals. The tell is that even the simplest changes are challenging.

The four team types worth knowing: **stream-aligned** teams own a single stream of work scoped to a business domain and exist to move fast delivering value — every other type exists to remove friction from them. **Enabling** teams bridge a capability gap, doing the research that is important but not urgent. **Complicated-subsystem** teams hold deep expertise in a genuinely specialized part and exist to reduce others' cognitive load. **Platform** teams provide internal self-service APIs, tools and services as a compelling internal product, carrying governance concerns like quality and security.

Remember the underlying constraint: organizations are constrained to produce designs that copy their own communication structures. Read the current architecture as evidence of the current communication structure, and where you need a structure the organization cannot communicate along, plan the team change that makes it possible.

Watch also for the organizational consequence of architectural centralization: when the architecture puts a single engine at its heart, the team owning it accrues political power and eventually becomes a bureaucratic bottleneck.

## 6. Systems integration

*What else must this talk to, and at what cost?*

Systems rarely live in isolation. Inadequate attention here produces static and dynamic coupling that leaves architectures unable to scale, unresponsive and inflexible.

Four questions before integrating:

1. Is the system being called actually available?
2. Does it scale and perform to the level the calling system's requirements demand?
3. Which communication protocols and what kind of contracts will sit between them?
4. Does the integration preserve each system's architecture quantum, or fuse them?

## 7. The enterprise

*Is it aligned with organization-wide standards and principles?*

Every enterprise — the whole collection of systems and products in a company, department or division — has standards and guiding principles covering security practices, platforms, technologies, documentation and diagramming.

Where an architect ignores them, the usual outcome is that the solution, **however technically effective, is deemed a failed one-off and scrapped.** Establish the standards before designing, not after; where one genuinely blocks the design, negotiate the exception explicitly rather than proceeding around it.

## 8. The business environment

*Does the architecture match the company's position and direction?*

The business environment directly influences architecture and never stops changing. Ask where the company actually is: cutting costs severely to stay afloat, expanding aggressively, pivoting quarterly in a volatile market, or stable.

- A company under extreme cost-cutting aligns badly with the expensive styles, which cost a great deal to create and maintain.
- A company expanding aggressively through mergers and acquisitions is served badly by monolithic styles that cannot evolve and adapt.

The recurring problem here is unknown change. Systems start with **known unknowns** — things the team knows it must learn. They also encounter **unknown unknowns**: things nobody knew would arise. These are the nemeses of software systems, and they are why every big-design-up-front effort suffers — an architect cannot design for what nobody knows exists.

Since all architectures become iterative anyway because of unknown unknowns, the only choice is whether to recognize it early. Do not attempt to design for unknown unknowns; design so that discovering one is survivable. Prioritize portability, scalability, evolvability and adaptability, which buy flexibility against unforeseen change.

A newer frame worth knowing but not yet established practice: treat business changes as stressors and the architectural responses as residues, on the theory that accumulating enough residues eventually addresses changes the architect could not predict.

## 9. Generative AI

*How does incorporating language models affect the architecture?*

**When building a model into an architecture**, use abstraction and modularity so one model can be swapped for another quickly, and so guardrails and evaluations can be applied around whichever is in place. Because output quality is not verifiable by inspection, the architecture must be able to gather samples and metrics and compare engines — observability tooling exists for this.

Worked case: anonymizing résumés to reduce bias and focus on skills. Is the model accurate? Does it strip too much? Does it leave demographic information in place? None of those can be answered without comparing samples and metrics across engines. Treat model replaceability as a design requirement, not a future refactor.

**When using a model to help with architecture work**, the current honest assessment: architecture-shaped prompts — *are there risk areas in this architecture, how should I address this risk, are there common antipatterns here, should I use orchestration or choreography* — have not yielded much success. Asking which style suits a situation rarely produces the right answer, because everything is a trade-off. Models understand knowledge and lack the wisdom to decide, and the context that wisdom requires is so large that it is faster for an architect to solve the problem themselves than to teach a model the problem plus its extended environment. The nine intersections are the measure of how large that context is.

What does show promise is tooling that removes mechanical work: interpreting an architecture diagram directly and describing the architecture from it, so no export to a machine-readable format is needed before asking simple questions like whether it can spot bottlenecks; and translating a diagram or a pseudolanguage description into executable governance code.

This assessment is dated to early 2025 and expected to change rapidly. Re-check it rather than treating it as permanent.

## Availability conversion

For intersection 6, and any external dependency.

| Uptime | Downtime per year | Downtime per day |
|---|---|---|
| 99.0% | 87 hrs 46 min | 14 min |
| 99.9% | 8 hrs 46 min | 86 sec |
| 99.99% | 52 min 33 sec | 7 sec |
| 99.999% | 5 min 35 sec | 1 sec |

A service-level agreement is usually a legally binding contractual commitment; a service-level objective usually is not. Convert, decide whether that downtime is acceptable for this workflow, and record the figure on the architecture diagram so the assumption stays visible.
