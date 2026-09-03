# Style catalog

Nine styles on a fixed template. Read the **Do not use** line first — ruling styles out is faster and more reliable than ranking them.

A note on the ratings: they are stated where the source material states them explicitly in prose. Where a characteristic is not rated here, no rating was available; do not infer one.

## Contents
- [Layered](#layered)
- [Modular monolith](#modular-monolith)
- [Pipeline](#pipeline)
- [Microkernel](#microkernel)
- [Service-based](#service-based)
- [Event-driven](#event-driven)
- [Space-based](#space-based)
- [Orchestration-driven SOA](#orchestration-driven-soa)
- [Microservices](#microservices)
- [Quick comparison](#quick-comparison)

---

## Layered

Also called n-tiered. Monolithic, **technically partitioned**, quantum always 1.

**Topology.** Horizontal layers, usually Presentation, Business, Persistence, Database. Three for small systems, five or more for large. Deployment variants: all layers in one unit with an external database; presentation split out as its own unit; or everything including an embedded or in-memory database in one unit, common for mobile and on-premises products.

**Open and closed layers.** A closed layer cannot be skipped — a request must pass through it. *Layers of isolation* — where a change in one layer does not affect the others, and any layer can be replaced — only works if the layers on the main request path are closed. Opening a layer so presentation can reach persistence directly is faster and couples them, making the architecture brittle and expensive to change. Document which layers are open and closed and why; failing to do so produces tightly coupled, brittle architectures that are hard to test, maintain and deploy.

To enforce a restriction the current layering cannot express, extract the restricted assets into a new layer and mark it *open*, so callers may pass through or bypass it while the closed layer above shields what you are protecting.

**Data topology.** Single monolithic database.

**Cloud.** Limited — deploy one or more layers with a provider. The technical partitioning suits split deployment, but latency between on-premises and cloud hurts, because workflows traverse most layers.

**Common risks.** No fault tolerance: one out-of-memory condition anywhere crashes the whole unit. Availability limited by high mean time to recovery, with startup from about 2 minutes for small applications to 15 minutes or more for large ones. The **Architecture Sinkhole**: requests passing layer to layer with no business logic performed. Every layered architecture has some; measure the percentage — around 20% is acceptable, 80% means the style is wrong for this domain.

**Governance.** Excellent. The original structural testing tools were built with this style in mind, and layer rules are directly expressible as assertions.

**Teams.** Works with any topology. The limit is that platform teams face increasingly difficult work as the monolith strains database connections, memory, performance or concurrent users.

**Ratings (as stated).** Cost and simplicity are the primary strengths. Testability two stars — mocking or stubbing a whole layer helps. Responsiveness three stars, achievable with caching and multithreading but capped by the lack of parallelism, closed layering and sinkholes. Deployability low: a three-line change redeploys everything and rides along with dozens of other changes. Elasticity and scalability one star. Every rating degrades as the code base grows.

**Use for.** Small simple applications and websites. Tight budget and time. Feasibility-driven delivery where speed matters more than longevity. As a starting point while the right style is undecided — in which case keep code reuse minimal and inheritance trees shallow, to preserve modularity and make the later migration feasible.

**Do not use for.** Large applications, or anywhere maintainability, agility, testability and deployability must hold as the system grows. Domain-driven design fits it poorly, because a single domain lives in every layer at once.

---

## Modular monolith

Monolithic, **domain-partitioned**, quantum typically 1.

**Topology.** A single deployment unit with one database, partitioned into modules by domain or subdomain rather than technical capability. Each module is one-to-many components, realized as a namespace or directory.

**Data topology.** Single database.

**Cloud.** Poorly suited — the monolithic nature cannot exploit on-demand provisioning, though small systems can still use managed storage, database and messaging services.

**Common risks.** Growing too big — the four warning signs are changes taking too long, changing one area unexpectedly breaking another, team members getting in each other's way, and slow startup. Over-reuse dissolving module boundaries into an *unstructured monolith*: code so interdependent it cannot be unravelled. Excessive intermodule communication, which indicates the domains were drawn badly — redraw them rather than optimizing the plumbing.

**Governance.** Strong. Module namespaces make compliance checks, dependency caps and pairwise access restrictions automatable.

**Teams.** Requires domain-aligned cross-functional teams. Teams organized by technical specialty work badly here, because every domain requirement then needs heavy cross-team coordination.

**Ratings (as stated).** Cost, simplicity and modularity are the primary strengths. Deployability and testability two stars — better than layered thanks to modularity, still constrained by monolithic ceremony and risk. Elasticity and scalability one star. No fault tolerance; availability limited by MTTR in minutes.

**Use for.** Tight budget and time. A new system whose architectural direction is unclear — start here and migrate to service-based or microservices rather than jumping straight to distributed. Domain-focused cross-functional teams. Systems where most changes are domain-based. Teams practising domain-driven design.

**Do not use for.** Systems needing high scalability, elasticity, availability, fault tolerance, responsiveness or performance. Systems where most changes are technically oriented, such as repeatedly replacing the UI or database technology — a domain partition makes those touch every module, and layered is the better choice.

---

## Pipeline

Also called pipes and filters. Usually monolithic, **technically partitioned**, quantum always 1.

**Topology.** Unidirectional point-to-point pipes connecting single-purpose filters. Filters are self-contained, independent, generally stateless, and do exactly one task; a composite task becomes a sequence of filters rather than one bigger filter. Four filter types:

- **Producer** — the source; outbound only. A UI, or an external request.
- **Transformer** — accepts input, optionally transforms some or all of it, forwards it. This is *map*.
- **Tester** — accepts input, tests it against criteria, optionally produces output; can act as a switch that stops the flow. This is *reduce*.
- **Consumer** — the termination point; persists the result or displays it.

Keep pipe payloads small for performance.

**Data topology.** Varies widely — from one monolithic database to one per filter.

**Cloud.** Well suited. Filters can deploy as serverless functions, containerized functions, an orchestrated workflow with each filter a function in the chain, or all in one unit.

**Common risks.** Overloaded filters doing more than one thing. Bidirectional communication, which means either the style is wrong or the filters are too complex and the functionality is demarcated badly. Mid-pipeline error recovery — once a pipeline has started, exiting and recovering from an error is genuinely difficult, so identify fatal error conditions *before* defining the architecture. Contract drift between filters.

**Governance.** Filter roles cannot be checked automatically, so role tagging is the practical technique.

**Teams.** Independent of team topology. Enabling teams can add an experimental filter tapping the same data without disturbing the existing flow.

**Ratings (as stated).** Cost, simplicity and modularity are the primary strengths — any filter can be modified or replaced without touching the others. Deployability and testability average, slightly above layered because of filter modularity. Elasticity and scalability one star. No fault tolerance; availability limited by monolithic MTTR in minutes. Deploying filters as separate units with asynchronous pipes lifts elasticity, scalability and fault tolerance substantially, at direct cost to simplicity and overall cost.

**Use for.** Systems of any complexity with distinct, ordered, deterministic one-way processing steps. Tight time and budget. Widely used in document-interchange transformation, database extract-transform-load, and orchestration and mediation tools.

**Do not use for.** High scalability, elasticity or fault tolerance in the monolithic form. Anything needing back-and-forth communication between stages. **Nondeterministic workflows** — possible by loading the pipeline with tester filters, but it overcomplicates a simple style and damages maintainability, testability, deployability and reliability. Event-driven architecture is the right style for those.

---

## Microkernel

Also called plug-in architecture. Monolithic, quantum always 1 (all requests pass through the core), and uniquely **either domain- or technically partitioned** — most are technically partitioned, and the domain-partitioned case arises through strong domain-to-architecture isomorphism, where the domain itself is shaped as core plus variants.

**Topology.** A core system plus plug-ins. The core is defined two ways: the minimal functionality required to run the system, and the happy path — the general processing flow with little or no custom processing. The operative move is to **take the application's cyclomatic complexity out of the core and put it in plug-ins**. A long if/else chain over customer-, device- or jurisdiction-specific cases becomes one plug-in per case plus a registry lookup, so adding a case means adding a plug-in and updating the registry, with no change to the core.

The core can internally be layered, a modular monolith, or split into domain services. The presentation layer can be embedded, be a separate UI over core backend services, or itself be a microkernel.

**Plug-in connection.** Four options. *Compile-based*: simplest to manage, but any change redeploys the whole application. *Runtime-based*: added or removed without redeploying, managed by a module framework. *Shared library* named after the plug-in. *Package or namespace* in the same code base — the simplest approach, using the convention `app.plug-in.<domain>.<context>` so the second node marks it as a plug-in bound by plug-in rules, the third groups by domain, and the fourth locates the case.

Plug-ins can also be invoked remotely as standalone services. That buys decoupling, scalability, throughput, runtime replacement without a special framework, and asynchronous invocation. It costs: the architecture becomes distributed, which makes it hard to ship as an on-premises product; complexity, cost and deployment topology all grow; and an unresponsive plug-in fails the request outright under a synchronous protocol. **It does not buy a second quantum** — every request still passes through the monolithic core.

**Registry and contracts.** The registry holds each plug-in's name, data contract and access details; it can be an in-memory map or a full discovery service. Contracts should be standard across a domain of plug-ins. Where plug-ins come from a third party and you do not control the contract, write an adapter between theirs and your standard, so the core never carries per-plug-in special cases.

**Data topology.** Usually a single relational database owned by the core, which passes data to plug-ins rather than letting them reach the database — deliberate decoupling, so a schema change touches only the core. Plug-ins may own private data stores, external or embedded.

**Cloud.** Three coarse options: all in the cloud; data only in the cloud with the system on-premises; or core on-premises with plug-ins in the cloud. The third looks modular and is usually prohibitive — plug-in calls are frequent and data-heavy, so the added latency dominates.

**Common risks.** A **volatile core**, usually caused by misjudging the core's volatility; the core is meant to be stable after initial development, since isolating change to plug-ins is the entire benefit. **Plug-in interdependence**: plug-ins should talk only to the core. Dependency-free plug-ins avoid transitive dependency management entirely; once plug-ins depend on each other, the core must resolve conflicts such as two plug-ins requiring different versions of the same library.

**Governance.** Core-volatility fitness functions over version-control churn, rate of change in the core, contract tests where plug-ins support different versions, and topology structure checks.

**Teams.** Excellent for enabling teams — plug-ins allow A/B tests and experiments — and for complicated-subsystem teams, since specialized processing isolates into a plug-in.

**Ratings (as stated).** Simplicity and overall cost are the main strengths; scalability, fault tolerance and elasticity the main weaknesses, from monolithic deployment. Testability, deployability and reliability three stars, because change is isolated to plug-ins — more so with runtime-based plug-ins. Modularity and evolvability three stars. Responsiveness three stars: these applications stay small, suffer less from sinkholes, and can be sped up by unplugging unneeded functionality.

**Use for.** Product-based applications shipped as an installable third-party product. Any domain requiring per-location, per-client or per-jurisdiction customization. Products emphasizing user customization and feature extensibility. Especially valuable where rules engines have grown into a big ball of mud — per-jurisdiction rules become independent plug-ins, so a rule change no longer requires an army of analysts, developers and testers.

**Do not use for.** Systems whose core functionality is itself volatile. Cases where the plug-ins must interact heavily with one another.

**The spectrum.** All microkernels support plug-ins; not all plug-in systems are microkernels. Where a system sits depends on how much standalone functionality the core holds. A *pure* microkernel has almost none — a linter parses source into a syntax tree and is useless until someone writes rules against it. A web browser supports plug-ins and works fine without them. The question that decides which you should build is **the volatility of the core**.

---

## Service-based

Distributed, **domain-partitioned**, quanta one or more. The most pragmatic distributed style, and a hybrid variant of microservices.

**Topology.** A separately deployed UI, a small number of separately deployed coarse-grained domain services, and optionally a monolithic database. Services deploy like monolithic applications and do not require containerization. Each domain service is internally layered (API facade, business, persistence) or subdomain-partitioned, with the API facade orchestrating the business request internally at class level rather than across the network — that internal-versus-external orchestration is one of the significant differences from microservices.

UI variants: one monolithic UI, a few domain UIs, or one per service. Splitting it raises scalability, fault tolerance and agility.

**Data topology.** Uniquely for a distributed style, a single monolithic database works — services can use ordinary queries and joins, and because there are few services, exhausting database connections is rarely an issue. It can be split as far as one database per domain service; if split, verify no other service needs that data.

**Cloud.** Works well. Domain services are containerized rather than serverless because of their scope.

**Common risks.** Interservice communication — domains should be as independent as possible with coupling concentrated at the database level, and heavy communication means either the domains were partitioned wrongly or the style does not fit. More than about **12 services** starts causing problems with testing, deployment, monitoring, database connections and schema changes.

**Governance.** Check that changes do not span multiple domain services; if they do, the boundaries are wrong or the style is wrong. Govern the volume of interservice communication. Keep orchestration at the UI or API-gateway level.

**Teams.** Needs domain-aligned cross-functional teams; technically organized teams work badly. Less suited to enabling teams than other distributed styles, because the services are coarse.

**Ratings (as stated).** No five-star ratings, but four stars for agility, testability, deployability, fault tolerance and availability — a failing service does not take the others down, because services are self-contained and do not typically call each other. Scalability three stars and elasticity two: coarse services replicate more functionality than needed when scaled, making scaling less cost- and resource-efficient; the norm is a single instance per service except where throughput or failover demands more. Simplicity and cost are the differentiators against the more powerful distributed styles.

**Use for.** Teams wanting real modularity without granularity and service-coordination complexity. Domain-driven design, which it fits naturally. Systems needing ordinary database transactions in a distributed setting — it supports them better than any other distributed style, because transaction scope sits inside a coarse service. Organizations for whom the more powerful distributed styles cost too much or offer more power than they need. Also an excellent stepping stone toward microservices.

**Do not use for.** Workloads where fine-grained independent scaling is the point, or where deployment isolation per capability matters more than transactional integrity.

---

## Event-driven

Distributed, asynchronous, primarily **technically partitioned** — a domain spreads across multiple event processors tied together by brokers, contracts and topics, so a domain change usually touches several. Quanta one to many.

**Topology.** Four components: the **initiating event** that starts the flow, the **event broker** that carries it, the **event processor** that accepts and processes it, and the **derived event** it triggers to advertise asynchronously what it did. Other processors respond with their own derived events; the flow ends when all processors are idle and all derived events are consumed. The broker is usually federated — multiple domain-based clustered instances, each holding all the event channels for its domain — using topics, topic exchanges or streams with publish-and-subscribe.

The governing rule is the relay race: once a processor hands off an event it is out of that race entirely, free to react to others, and each processor scales independently.

**Mediator variant.** Where control matters more than decoupling, an event mediator accepts the initiating event, knows the required steps, and sends derived *messages* point-to-point to dedicated queues. Processors respond to the mediator and do not advertise to the rest of the system. Deploy multiple mediators by domain, both to avoid the single point of failure and to raise throughput.

**Data topology.** Monolithic, domain-grouped, or dedicated per processor. See `caching-and-data.md`.

**Cloud.** An excellent match — the decoupling suits cloud asynchronous services and elastic infrastructure.

**Common risks.** Nondeterministic side effects: processors unexpectedly triggering derived events, or failing to respond when they should. Static coupling through event payload contracts — the architecture is dynamically decoupled and contracts couple it statically, and changing one is daunting because you do not know who consumes it. Creeping synchronous communication, which signals the style does not fit. State management: it is hard to know when an initiating event has been fully processed, since occasionally you can identify a final endpoint and subscribe the initiating processor to it, but usually you cannot.

**Governance.** Mostly observability-based: contract change rate, never-read contract fields, and detection of synchronous calls.

**Teams.** Complicated-subsystem teams work well — complex processing isolates into its own processor, and coordination is limited to contracts and derived events. Platform teams work well if broker and channel infrastructure is treated as platform. Stream-aligned teams struggle as the system grows, because one workflow change touches multiple processors and their derived events. Enabling teams work badly, because experiments inside a stream disrupt the stream team's grasp of the overall flow.

**Ratings (as stated).** Performance, scalability and fault tolerance four to five stars — performance from asynchronous communication plus highly parallel processing; scalability from programmatic load balancing of processors (competing consumers, consumer groups) added as load rises; fault tolerance from decoupled processors delivering eventual consistency, so work can complete later. Four rather than five because of the database. Evolutionary five stars: new features arrive as new processors hooked to already-flowing derived events, with no infrastructure or existing-processor changes. Simplicity and testability rate low, because nondeterministic dynamic flows can generate event tree diagrams with hundreds or thousands of scenarios.

**Use for.** Any problem centred on responding to things happening, internal or external. Systems needing high responsiveness, performance, scalability, fault tolerance and elasticity. Unknown and spiky volumes.

**Do not use for.** Workflows where certainty of outcome and end-to-end testability matter more than throughput. Systems needing strong consistency. Cases where most processing is really request-based — microservices is the better answer there.

---

## Space-based

Distributed, **technically partitioned** (a domain spreads across processing units, data pumps, readers, writers and the database). Quanta variable: because processing units never talk to the database synchronously, the database is not part of the quantum equation, so quanta are delineated by UI-to-processing-unit associations, with any units communicating synchronously — directly or through the processing grid — falling in the same quantum.

**The problem it solves.** In a standard browser → web server → application server → database flow, load creates a bottleneck at the web tier first. Scaling web servers is easy and cheap and just moves the bottleneck to the application tier, which is harder, and then to the database, which is hardest. The result is a triangle, and in any high-volume application the database is the final limit on concurrent transactions.

**Topology.** Named after tuple space — parallel processors communicating through shared memory. It replaces the central database as a synchronous constraint with replicated in-memory data grids. Data lives in memory, replicated across all active processing units; a unit that updates data sends the change asynchronously to the database through a **data pump**, usually messaging with persistent queues. Processing units start and stop dynamically with load. Because no central database sits in the transaction path, the bottleneck is gone and scalability becomes near-infinite.

Eight artifacts: **processing units** (application functionality plus an in-memory data grid and replication engine), **virtualized middleware** (infrastructure managing and coordinating the units), **messaging grid** (input requests and session state), **data grid** (synchronization and replication between units), **processing grid** (orchestration when a request spans multiple units — optional), **deployment manager** (starts and tears down instances as load changes), **data pumps** (send updates asynchronously), **data writers** (perform the database updates), **data readers** (read from the database and deliver to units at startup).

**Data topology.** Flexible, because transaction processing is independent of the database. Choose monolithic if reporting and analytics matter or downstream systems read the database; domain-based if the data partitions cleanly, which also gives better synchronization time and consistency.

**Cloud.** Excellent, including a genuine hybrid split unavailable in other styles: processing units and virtualized middleware in the cloud, physical databases and data on-premises. The asynchronous data pumps and eventual-consistency model make the cross-boundary synchronization work, so transactional processing runs in elastic cloud infrastructure while physical data management, reporting and analytics stay on-premises.

**Common risks.** **Frequent database reads** — the style works by keeping transactional data in cache, with reads only for archived data or a cold start; if volumes are so large that most data must be archived and re-read, or units crash or redeploy frequently, this is the wrong architecture. **Synchronization delay** — under high concurrent load the data pumps bottleneck and updates take a long time to reach the database, a real problem if downstream systems need fresh data. **Data loss in the pump**, mitigated by persisted queues and client-acknowledgment mode in the writers, at the cost of responsiveness and consistency. **High data volumes** — all transactional data sits in each unit's memory, so volumes must stay low, especially as instances multiply, or units run out of memory and crash. **Data collisions** — see the formula in `caching-and-data.md`.

**Governance.** Memory consumption per unit, synchronization time, pump queue depth, database read frequency — plus the characteristics the style was chosen for.

**Teams.** Most effective with technically partitioned teams aligned to functionality, pumps, readers/writers and database. Enabling teams fit well because pumps, readers, writers and middleware are shared cross-cutting artifacts. Complicated-subsystem teams fit well because data collisions and asynchronous synchronization errors are genuinely specialist work. Stream-aligned teams struggle, since one stream change can touch units, pumps, readers, writers, cache contracts, orchestrators and the database.

**Ratings (as stated).** Elasticity, scalability and performance all five stars — the driving characteristics, and this is the only style that maximizes all three together, capable of millions of concurrent users. Simplicity is low, from caching plus eventual consistency in the system of record. Testability one star, because simulating hundreds of thousands of concurrent users at peak is complicated and expensive, so most high-volume testing ends up happening in production under real extreme load, at real risk. Cost is high: complexity, caching product licences, and the resources to sustain the scale.

**Use for.** High spikes in user or request volume, and throughput above roughly **10,000 concurrent users**. Treat it as a specialized style, chosen when responsiveness, scalability and elasticity must all be maximized. Concert ticketing, where volume jumps from hundreds to tens of thousands the moment tickets go on sale and sells out in minutes — the deployment manager can be configured to pre-start units just before the sale. Online auctions, where bidder counts are unknowable and units can be devoted per auction for bidding consistency.

**Do not use for.** Anything below that scale. The complexity and cost are not recoverable at ordinary volumes.

---

## Orchestration-driven SOA

Distributed, the most technically partitioned general-purpose architecture ever attempted, and — despite being distributed — **a single quantum**. Two reasons: it typically uses one or a few databases, and the orchestration engine is a giant coupling point, so no part can have characteristics different from the mediator that orchestrates everything. It therefore manages to find the disadvantages of both monolithic and distributed architectures.

**Included for what it teaches, not to build.**

**Topology.** A taxonomy of services with layered responsibilities: **business services** (coarse-grained entry points, defined by business users as signatures with no code), **enterprise services** (fine-grained shared implementations intended as reusable building blocks), **application services** (one-off, single-implementation, owned by one team), and **infrastructure services** (monitoring, logging, authentication, authorization) — stitched together by an orchestration engine and message bus that also acts as an integration hub, handling transactional coordination and message transformation. All requests route through the engine, including internal calls.

**Data topology.** One or a few relational databases, with transactionality often pushed out of the database into declarative configuration on the bus.

**Ratings (as stated).** Deployability and testability score disastrously, both because they are poorly supported and because they were not goals when the style was built. Elasticity and scalability are supported, through heavy vendor investment in session replication and similar techniques. Performance was never a highlight, because each business request is split across so much of the architecture. Simplicity and cost stand in the inverse of the relationship architects want.

**Why it failed, and what transfers.** Three lessons worth carrying:

1. **Reuse is implemented via coupling.** A canonical shared entity ripples every change to every consumer, forcing coordinated deployments and holistic testing — and it must carry every attribute any consumer needs, so every consumer inherits complexity it does not want.
2. **Technical partitioning taken to the extreme grinds domains to dust.** Adding one address line to a checkout workflow touched dozens of services across several tiers plus a schema, because the domain concept was spread so thin.
3. **Some features cannot be cleanly abstracted away.** Declarative transaction management failed because developers could not know runtime transactional behavior, and because failure-mode edge cases kept producing inconsistencies humans had to untangle. Too many leaks in an abstraction prevent it from being reliable.

**What is still useful.** An integration bus provides both an integration hub (communication, protocol and contract transformation) and an orchestration engine — genuinely what integration-heavy environments need, especially where legacy systems must interact with modern ones, combining results and aggregating behavior. The layers of indirection also allow services to be implemented as integration points, packaged software, or bespoke code interchangeably.

**The risk when using those parts.** **Accidental SOA** — the bus gradually and unintentionally encapsulates the whole architecture until you have built this style without deciding to. Keep explicit encapsulation boundaries around what the orchestration layer may own, and watch transactional boundaries.

**It was rational in its era.** With commercial per-machine operating system and database licensing, the alternatives were economically inconceivable. Judge inherited architectures against the constraints of their time.

---

## Microservices

Distributed, decidedly **domain-partitioned**, with the most distinct quanta of any modern architecture — it exemplifies what the quantum measure evaluates.

**Topology.** Small single-purpose services, each in its own process in a virtual machine or container, each containing everything it needs to operate independently including its database. An API gateway for routing and cross-cutting concerns. Sidecars wired into a service mesh for operational reuse. Either a monolithic frontend or micro-frontends.

**The philosophy.** It physically models the bounded context: each service owns its logical components, classes, schema and database, and is coupled to nothing outside. Because reuse requires coupling, and decoupling is the goal, it chooses **duplication** instead — a shared Address class, normal in a monolith, is duplicated per context.

**The API layer.** Carries request routing and cross-cutting concerns — security, monitoring, logging, naming services — and nothing else. It must not act as a mediator or orchestrator: all business logic belongs inside a bounded context, and mediators are a technically partitioned pattern.

**Operational reuse.** Split domain reuse from operational reuse rather than picking one policy for both. Monitoring, logging, circuit breakers and service discovery go into a sidecar present in every service, owned by a shared infrastructure team, so upgrading the monitoring tool means updating the sidecar once. Wiring sidecars into a service plane forms a service mesh, giving unified global control. Service discovery — detecting and locating services, and spinning up instances by request volume — is typically part of the mesh and often hosted in the API layer.

**Communication.** *Protocol-aware heterogeneous interoperability*: protocol-aware because with no central hub each service must know or discover how to call another, so teams standardize; heterogeneous because each service can use a different stack, fully supporting polyglot environments; interoperability because services do call each other over the network. Choreography suits simple flows and preserves decoupling; orchestration suits complex flows where error handling and coordination dominate. Watch for **Front Controller** — a nominally choreographed service quietly accumulating coordination on top of its own domain responsibilities.

**Data topology.** Database-per-service. This is the only style that *requires* breaking apart the data: neither monolithic nor domain-grouped databases are options, because of fine granularity, bounded context and the number of services. Up to five or six services may share within a broader bounded context.

**Cloud.** Sometimes called cloud-native — on-demand provisioning of machines, containers and databases fits it directly, though container orchestration platforms make on-premises deployment practical too.

**Common risks.** Services too small (grains of sand). Excessive interservice communication. Excessive data sharing. Shared code libraries, which put part of a bounded context outside it. Three of the four reduce to granularity.

**Governance.** Static coupling via bill of materials and dependency tooling; dynamic coupling via consistent logging or startup registration.

**Teams.** Needs domain-aligned cross-functional teams; technically partitioned teams work badly. Platform and enabling teams typically own the sidecars and service mesh, freeing stream-aligned teams from operational concerns. Stream-aligned teams struggle when a stream crosses several bounded contexts — a signal to realign the boundaries or change style.

**Ratings (as stated).** Notably high on automated deployment and testability — the style could not exist without the automation of operational concerns. High fault tolerance from independent single-purpose services. High scalability, elasticity and evolvability, with some of the most scalable systems ever written built this way. **Performance is the weak point**: many network calls, a security check at every endpoint adding latency, and data latency when a request needs several services and therefore several database calls. The style's performance patterns — intelligent data caching and replication to avoid network calls — exist for this reason, and it is also why it often prefers choreography to orchestration.

**Use for.** Systems with a high degree of functional and data modularity, where each capability manages its own data. A medical monitoring system with one service per vital sign is the clean case: a crashed blood-pressure service leaves every other vital sign monitored, maintenance on one has a small enough testing scope to be confident in, and a new vital sign can be added without touching the others.

**Do not use for.** Anything where transactions across services would be the dominant feature. Anything where performance under many coordinated calls is the governing characteristic. Organizations without the automation maturity the style presumes.

---

## Quick comparison

| Style | Physical | Partitioning | Quanta | Strongest | Weakest |
|---|---|---|---|---|---|
| Layered | Monolithic | Technical | 1 | Cost, simplicity | Elasticity, scalability, deployability |
| Modular monolith | Monolithic | Domain | 1 | Cost, simplicity, modularity | Elasticity, scalability, fault tolerance |
| Pipeline | Monolithic | Technical | 1 | Cost, simplicity, modularity | Elasticity, scalability, fault tolerance |
| Microkernel | Monolithic | Either | 1 | Simplicity, cost, extensibility | Scalability, elasticity, fault tolerance |
| Service-based | Distributed | Domain | 1+ | Agility, testability, deployability, fault tolerance, cost | Elasticity, fine-grained scalability |
| Event-driven | Distributed | Technical | 1–many | Performance, scalability, fault tolerance, evolvability | Simplicity, testability |
| Space-based | Distributed | Technical | Variable | Elasticity, scalability, performance | Testability, simplicity, cost |
| Orchestration-driven SOA | Distributed | Technical | 1 | (historical) | Deployability, testability, performance, cost |
| Microservices | Distributed | Domain | Many | Deployability, testability, fault tolerance, scalability, evolvability | Performance, cost |
