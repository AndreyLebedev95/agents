---
name: choose-architecture-style
description: Chooses the architecture style and topology for a system and says what it will cost — running the scoping tree from characteristics to monolith or distributed, finding quantum boundaries, then selecting among layered, modular monolith, pipeline, microkernel, service-based, event-driven, space-based, SOA and microservices on their real disqualifying conditions rather than reputation. Also covers the fallacies of distributed computing, sync versus async, queues versus topics, orchestration versus choreography, event payloads and data topology. Use whenever a topology must be chosen or justified, when comparing microservices against anything, when deciding monolith versus distributed, when planning a migration between styles, when someone asks whether event-driven or space-based or a modular monolith fits, when choosing between REST and messaging, when asking whether serverless is an architecture, or when asking what style an existing system really is and whether it still fits. Use it even when the request is only "what architecture should we use". For which characteristics matter first use elicit-architecture-characteristics; for sizing services inside the chosen style use decompose-system-into-components; for writing the decision down use record-architecture-decisions.
---

# Choosing an architecture style

A style is a compressed label for five things at once: **component topology** (how components and dependencies are organized), **physical architecture** (monolithic or distributed), **deployment** (granularity and cadence), **communication style** (in-process calls or network protocols), and **data topology** (one database or partitioned). It also carries assumed default characteristics, beneficial and detrimental.

Compare styles on those five dimensions and on their trade-offs. Never on the name — style names are labels, not instructions. They emerge when someone combines new ecosystem capabilities to solve a nagging problem and enough others copy it that a name becomes useful, which makes each name a reaction to what came before rather than a specification. "Microservices" was named against the large-service, heavy-orchestration styles of its time; it is not an instruction to build the smallest possible services.

Almost any generic style can be implemented in almost any problem domain — that is what generic means. The exceptions are domains needing special operational characteristics. **So the real differences between styles are in how well each supports the characteristics, not in which domain it suits.**

## The output

```
## Chosen style: <name>  (or: <name> with <name> embedded for <part>)
Quanta:        <count, and where the boundaries fall>
Data topology: <choice, per quantum>
Communication: <synchronous | asynchronous, per boundary, with the reason>
Because:       <the characteristics that forced it>
Costs:         <the trade-offs being accepted>
Under-served:  <characteristics deliberately not prioritized>
Watch for:     <the named risks this style brings>
```

## Before you start

Do not choose until you have: the domain, at least a general understanding of its major aspects; the architecture characteristics from characteristics analysis; the data architecture, including any legacy data design the system must interact with; the cloud model, and how much data will be stored and moved, since movement carries real cost; organizational and cost factors; and the team's engineering maturity.

That last one is not optional. Styles presume practices. A style whose philosophy assumes automated machine provisioning, testing and deployment will likely fail against a manual operations group and little testing. Just as problem domains lend themselves to styles, so do engineering practices — raise the practice or choose a style the practice can support.

And check the company's financial position, not just its problem. Extreme cost-cutting aligns badly with the expensive styles. Aggressive expansion through acquisition aligns badly with monolithic styles that cannot evolve.

## Procedure

### 1. One set of characteristics, or several?

This is the first and most consequential question. Can the system succeed with a single set of architecture characteristics, or does it need more than one group?

One group implies a monolithic architecture, which closes off most of the remaining choices. More than one implies distributed.

### 2. If distributed, find the quantum boundaries

An **architecture quantum** is an independently deployable artifact with high functional cohesion, low external implementation static coupling, and synchronous communication with other quanta. It is the boundary within which a set of characteristics — especially operational ones — applies.

Find the boundaries by clustering. Run characteristics analysis across the domain, group the characteristics by which part demands them, and look for clusters that pull against each other. **Characteristics that counteract one another are a signal to separate, not a problem to solve inside one design.**

A worked case: an electronics recycling business produced three clusters — public-facing (scalability, availability, agility), back office (security, data integrity, auditability), and device assessment (maintainability, deployability, testability, because the business model depends on re-pricing new device models fast). Fast deployability fights auditability; the UI's scalability need is nothing like the back office's. Three quanta.

Counting quanta correctly matters more than it sounds, because two things silently collapse them:

- **A shared database.** Services sharing a coupling point are one quantum. A legacy system on a single database is by definition a quantum of one, so it can have exactly one set of characteristics.
- **A blocking synchronous call.** Two quanta communicating synchronously become dependent and fuse into one — the caller is down when the callee is down, slow when it is slow, and cannot scale unless it scales. Asynchronous messaging alone does not save you: a request-reply interaction where the caller cannot proceed without the answer is the same fusion.

Count quanta by asking what cannot proceed when something else is unavailable.

### 3. Check the shape

Some problems already have the shape of a style. Customizability maps onto a core-plus-plug-ins topology. A domain of many discrete independent operations maps onto many discrete processors.

Some are actively mismatched. Highly scalable systems struggle inside large monoliths, because a highly coupled code base cannot support many concurrent users. A problem with heavy semantic coupling maps badly onto a highly decoupled architecture — an insurance application of multipage forms, each depending on the context of the previous ones, is intrinsically coupled and is better served by an intentionally coupled style.

Treat heavy semantic coupling in the domain as an argument *against* a decoupled style, not as something the architecture should fix. Semantic coupling is inherent in the problem; no pattern prevents a change in the domain rippling through the system, because that is a change in requirements.

### 4. Shortlist and compare against the catalog

`references/style-catalog.md` has all nine styles on a fixed template — partitioning, quantum count, topology, data topology, cloud fit, risks, governance, team fit, stated ratings, and explicit use / do-not-use conditions.

Read the **do-not-use conditions first**. Ruling styles out is faster and more reliable than ranking them.

Also settle the top-level partitioning, since it determines the style family and how you will identify components: **technical** partitioning organizes by capability (presentation, business rules, persistence) and **domain** partitioning by workflow. Technical partitioning separates cross-cutting concerns cleanly and costs you the domain, which gets smeared across every layer so that one workflow change touches all of them. Domain partitioning models how the business works and costs duplicated customization code. Neither is more correct; the industry trend is toward domain partitioning for both monolithic and distributed architectures.

Remember Conway's Law here. Organizations are constrained to produce designs that copy their own communication structures, so a structure the organization cannot communicate along will not survive. If you need a structure the current team topology cannot produce, plan the team change that makes it possible — that is a deliberate architecture decision, not an HR one.

### 5. For distributed candidates, price the fallacies

Distributed architectures are more powerful and carry a fixed set of costs that are always underestimated. Walk all eleven in `references/distributed-fundamentals.md` and state how this system handles each.

The two that most often decide feasibility:

- **Latency.** Get the actual production round-trip figure, and the 95th-to-99th percentile, not the average. A system averaging 60 ms may have a 95th percentile of 400 ms, and it is that long tail that kills performance. Multiply by the hop count of your longest workflow: at 100 ms per hop, a ten-call business function adds a full second.
- **Transport cost.** This is money, not latency. Distributed architectures cost significantly more in hardware, servers, gateways, firewalls, subnets and proxies.

### 6. Choose data topology, then communication

Data topology follows the family. A monolith generally takes a single database developed and deployed in lockstep. A distributed architecture takes either a shared database, domain-grouped databases, or one per service.

Then communication. **Default to synchronous; go asynchronous only where something forces it.** Synchronous presents fewer design, implementation and debugging challenges. Asynchronous buys performance and scale at the cost of data synchronization, deadlocks, race conditions and debugging difficulty — and error handling, which is the genuinely hard part.

What forces asynchrony is usually a characteristics mismatch across the boundary: a service that can process one payment every 500 ms will time out under synchronous calls when many workflows complete at once, and a queue turns that into a survivable buffer. Note the limit — a queue absorbs *bursts*, not sustained excess.

`references/communication-patterns.md` covers queues versus topics, request-reply, orchestration versus choreography, and event payload design.

### 7. Re-check the boundaries

Choosing synchronous communication can change the quantum boundaries that static coupling established. The two kinds of coupling interact, so this is not a one-pass tree.

### 8. State what you are accepting

Name the trade-offs and the under-served characteristics explicitly. An option with no found disadvantage means the analysis is incomplete, not that you found a free lunch.

## Coupling vocabulary you need for this

- **Semantic coupling** — inherent in the problem. Not negotiable.
- **Implementation coupling** — what the team chose: one database or several, monolith or distributed. Barely touches semantics, dominates architecture decisions. This is the negotiable part.
- **Static coupling** — the wiring; which services depend on what. Two services sharing a coupling point are in the same quantum.
- **Dynamic coupling** — the forces involved when quanta communicate at runtime.

Two things are coupled if changing one might break the other.

**Bounded context** is the decoupling idea underneath the domain-partitioned styles: everything about one portion of the domain is visible internally and opaque outside it. Before it, architects reused entities holistically across an organization and the shared artifacts produced tight coupling, harder coordination and more complexity. Each domain defines its own version of an entity and reconciles differences at communication points. The duplication is the point, not an oversight.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Nobody can name the style | Architecture by Implication — it was never chosen | Assume layered; check whether layered actually fits |
| Most requests pass through layers doing no work | Architecture Sinkhole | Measure the ratio; change style above ~80% |
| Splitting bought no scalability | Every request still passes one chokepoint | Count chokepoints before crediting a decomposition |
| Async messaging, everything still fails together | Shared database, or blocking request-reply | Recount the quanta |
| Bandwidth cost dominating | Stamp coupling — fat payloads | Measure payload × rate; send only what is needed |
| Event loop that never terminates | Poison event | Draw the derived-event graph and find the cycle |
| Hundreds of tiny events nobody can follow | Swarm of Gnats | Key event granularity to outcomes |
| Consumers cannot act on an event | Anemic event | Carry prior and new values on state changes |
| Integration bus quietly became the architecture | Accidental SOA | Keep encapsulation boundaries around orchestration |
| Reuse programme produced paralysis | Reuse is implemented via coupling | Duplicate the volatile; reuse the plumbing |
| Cache-based system inconsistent at scale | Update rate exceeds replication latency | Compute the collision rate; consider a distributed cache |
| Style chosen, practices cannot support it | Engineering maturity ignored | Raise the practice or change the style |
| Ideal design rejected on cost | Company's financial position ignored | Screen styles on cost profile before evaluating |

## Two definitional notes

**Serverless is not a style.** Functions triggered on request with resources allocated on demand describes exactly what a microservice is — a single-purpose, separately deployed unit. It is a deployment model for microservices. Cloud microservices need not be serverless; containerized deployment is equally available.

**"Service" has suffered semantic diffusion.** An entity service in orchestration-driven SOA differs in virtually every way from a microservice, which differs again from a domain service in service-based architecture. Read the term from context rather than assuming.

## When to reach for a reference

- `references/style-catalog.md` — all nine styles on a fixed template with use and do-not-use conditions. Read once a shortlist exists, and again to rule one out.
- `references/distributed-fundamentals.md` — the eleven fallacies, latency percentiles, stamp coupling and its fixes, and data-loss prevention. Read whenever a distributed style is on the shortlist.
- `references/communication-patterns.md` — synchronous versus asynchronous, queues versus topics, request-reply, orchestration versus choreography, mediator selection, CQRS, broker topology, event payloads, error handling. Read when the communication decision is live.
- `references/caching-and-data.md` — replicated versus distributed caching with thresholds, the collision formula, the three data topologies, and database-type selection. Read when the style depends on caching or data placement is the open question.

## Further reading

- *Building Microservices* (2nd ed.), Sam Newman.
- *Building Micro-Frontends* (2nd ed.), Luca Mezzalira — for the frontend half of a distributed architecture.
- *Software Architecture: The Hard Parts* — granularity and distributed data in depth.
- *Chaos Engineering*, Casey Rosenthal and Nora Jones — for verifying a distributed design survives what you assumed it would.
