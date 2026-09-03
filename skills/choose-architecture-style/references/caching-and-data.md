# Caching and data topologies

Read when the style depends on caching, or when data placement is the open question.

## Replicated versus distributed caching

**Replicated.** Each processing unit holds its own in-memory grid, synchronized across all units sharing the same named cache. Extremely fast and highly fault tolerant — no central server, therefore no single point of failure.

**Distributed.** One external cache server that units read over a protocol. Consistency is high because the data lives in one place. Performance is worse due to remote access latency, and the cache server is a single point of failure; mirroring it reintroduces a consistency risk if the primary fails before data reaches the mirror.

| Decision criterion | Replicated | Distributed |
|---|---|---|
| Optimizes | Performance | Consistency |
| Cache size | Small (< 100 MB) | Large (> 500 MB) |
| Type of data | Relatively static | Highly dynamic |
| Update frequency | Relatively low | High update rate |
| Fault tolerance | High | Low |

**How to decide, in order:**

1. **Check cache size first.** Past roughly 100 MB per unit, memory pressure inside the VM or container limits how many instances can start, which destroys elasticity — the thing the architecture was for.
2. **Check update rate.** If it exceeds what the replication engine can keep up with, consistency across units breaks and you need a distributed cache. Compute the collision rate below.
3. Otherwise decide by what the data is *for*: consistency, or performance and fault tolerance.

**Do not pick one model for the whole application.** Both apply in most systems, and different processing units should use different models. Inventory counts, which must be consistent, warrant a distributed cache; reference data like name/value pairs, product codes and descriptions warrants a replicated cache for fast lookup.

## The data-collision formula

In active/active replicated caching, two instances can update the same data inside the replication window and each overwrite the other, leaving both caches wrong.

```
CollisionRate = N × (UR² / S) × RL
```

- **N** — number of instances sharing the named cache
- **UR** — update rate per second
- **S** — cache size in rows
- **RL** — the caching product's replication latency in milliseconds

**Worked baseline.** 20 updates/second, 5 instances, 50,000 rows, 100 ms latency → 72,000 updates an hour and about **14.4 collisions**, or 0.02%. Low enough that replication is viable.

**Sensitivity.** Each factor moves it differently, which is what makes the formula useful rather than decorative:

| Change | Collisions/hour | Percentage |
|---|---|---|
| Baseline | 14.4 | 0.02% |
| Replication latency 100 ms → 1 ms | 0.1 | 0.0002% |
| Instances 5 → 2 | 5.8 | 0.008% |
| Cache size 50,000 → 10,000 rows | 72.0 | 0.1% |

Cache size is the only inversely proportional factor: **shrinking the cache raises the collision rate.**

**Using it honestly.** Replication latency depends on network type and physical distance between units, is almost never published, and must be measured in your own production environment — 100 ms is a planning figure only. Establish the *maximum* update rate at peak usage, not the average, and compute minimum, normal and peak collision rates.

The failure it predicts: two instances each holding 500 units of inventory, one selling 10 and writing 490, the other selling 5 and writing 495 before replication, then each overwriting the other. Both end wrong, and neither shows the correct 485.

## Near-cache: do not

A near-cache pairs a distributed backing cache with a per-unit front cache holding a smaller subset, evicted by most-recently-used, most-frequently-used, or random replacement. Random replacement is the right choice when no analysis favours recency or frequency.

Each front cache stays in sync with the backing cache but **not with the other units' front caches**, so units sharing a data context hold different subsets and exhibit inconsistent performance and responsiveness. Not recommended in a space-based architecture.

## Warm start without the database

Processing units synchronize by named cache. A unit joining broadcasts through the caching provider to find others holding the same named cache; the first to respond sends it the contents, so the new instance is in sync without reading the database — which is what makes elastic startup fast.

Each instance keeps a member list of the addresses and ports of all instances sharing that cache, updated automatically as instances arrive and disappear. An update in one instance replicates asynchronously to the rest, typically in under 100 ms.

This requires at least one running instance still holding the named cache. Otherwise the data must come from the database through the read path.

## The three data topologies

For any distributed architecture, the same three options with the same trade-off shape.

**Monolithic.** One central database all services query. Any service gets what it needs directly with no synchronous call to another service — genuinely valuable in a decoupled asynchronous style. Costs: a database outage takes every service down; the database must scale to the combined concurrent load of independently scaling services, which many cannot; a schema change forces coordination across multiple services; and the shared database collapses everything into a single architecture quantum.

**Domain-grouped.** Services grouped into domains, one database each. Better fault tolerance — one domain's database failing leaves the others working, with the event channel queuing — plus scalability and change control scoped per domain. Cost: a service sometimes needs data from another domain and must call it synchronously.

**Dedicated (database-per-service).** Highest fault tolerance, scalability and change control: an outage isolates to one service, a schema change touches one service. Costs: potentially very expensive depending on the technology stack, and the most synchronous coupling of the three.

**Choosing.** Identify every data requirement of every service *before* choosing — that is the deciding input. Prefer dedicated only where services are mostly self-contained. If they need too much synchronous communication, reevaluate the domain boundaries, combine domains, or move up to monolithic. Weigh against change frequency: frequent schema change argues for narrower topologies even at operational cost.

**A useful property of the asynchronous channel**: it acts as a backpressure point. Each processor scales independently regardless of whether the others do, and when a downstream domain's database is unavailable, the channel queues events until it returns.

## Matching the database to the architecture

Choosing the wrong database type or topology negates an architecture's best characteristics. Four axes, in order:

**1. Topology fit against the style.** Monolithic databases give consistency and transactional support and cost scalability and fault tolerance. Distributed topologies give scalability and change control and cost data integrity, consistency and performance. Microservices needs database-per-service to hold the bounded context; service-based architecture is far more flexible.

**2. Match strengths to strengths.** Scalability and elasticity are the strengths of microservices, event-driven and space-based architectures — and also of key-value and columnar databases. Those pairings amplify each other.

**3. Match the actual data structure.** Relational data — a hierarchy of interdependent relationships — fits a relational database. Key-value pairs in a relational database is a misalignment that makes both the database and the architecture inefficient. JSON event or request payloads fit a document store. Because data structures vary within one architecture, prefer polyglot databases wherever feasible.

**4. Check the read/write ratio.** High write volume over infrequent reads favours a columnar database. High read volume favours key-value, document or graph. Roughly equal favours relational or NewSQL. Misaligning this produces poorly performing systems.

## Data abstraction versus data access

The difference is how much the callers know about the schema.

With a **data access layer**, callers reach the database only indirectly but remain coupled to its underlying structures. With a **data abstraction layer**, callers are decoupled from the schema by separate contracts, so the in-memory or in-service model can differ from the database model.

Prefer abstraction where independent evolution matters. Because the read and write components hold transformation logic, they can buffer a database change — a changed column type, a dropped column or table — until the callers are updated. Incremental database change then does not force lockstep application change.

## One cloud placement warning

Two deployment choices silently invert the characteristics a caching design assumed:

- Deploying services **across regions, or even across availability zones**, can decrease or entirely cancel the performance and data-integrity benefits of both replicated and distributed caches.
- **Co-locating** services, containers or pods on the same virtual machine significantly increases performance and adversely affects scalability, fault tolerance, availability and elasticity.

Check the physical placement of anything that relies on replication latency, and price what co-location cost in resilience.
