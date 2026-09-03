# Trade-off analysis

Read when the comparison is non-trivial. The method, two worked examples, and one case showing how a hidden trade-off gets found.

## The method

1. **Determine all the contextualized factors that make a difference for this solution.** This list is highly specific to the organization and the solution — it depends on your knowledge of the technology landscape, team capabilities, budgets, and everything else that informs the options.
2. **Score each option against each factor** in a matrix.
3. **Weight the factors** for this context.
4. **Read the weighted result.**

Step 3 is the one that gets skipped, and skipping it is the single most common failure in trade-off analysis. See the weighting section below.

## Worked example 1: shared library versus shared service

A common conundrum in distributed architectures. Should common behavior be a library compiled into each service at build time, or a service other services call at runtime?

The pertinent factors:

**Heterogeneous code.** If solutions are written on multiple platforms, the service is easier: callers reach it over the network, so the implementation platform is irrelevant. The library needs a version per technology stack, kept in sync, greatly adding to complexity. → *service*

**High code volatility.** Where the shared code changes often, callers of a service get new functionality as soon as it deploys. A library change means recompiling and redeploying every service. → *service*

**Ability to version changes.** Versioning is much easier in the library — version differences resolve at compile time and the team builds just what it needs. For the service, version information must be determined at runtime, which complicates every interaction. → *library*

**Overall change risk.** Once library code is changed and successfully compiled into the service, you can have high confidence it will work. The service may change with no compile-time verification, raising the likelihood of a runtime fault at invocation. → *library*

**Performance.** Calls to shared functionality in a library are in-process. Service calls are network calls, much slower because of latency and other factors. → *library*

**Fault tolerance.** Runtime access to a service always suffers potential network issues. Once the library is compiled, tested and deployed, you can have high confidence it is stable. → *library*

**Scalability.** Same reasoning as performance: latency between services diminishes scalability, while in-process access does not. → *library*

| Factor | Shared library | Shared service |
|---|---|---|
| Heterogeneous code | − | + |
| High code volatility | − | + |
| Ability to version changes | + | − |
| Overall change risk | + | − |
| Performance | + | − |
| Fault tolerance | + | − |
| Scalability | + | − |

Five to two for the library — **for these factors and in this context.** It may or may not be the solution to the problem at hand. What the exercise has produced is not an answer but a clear picture of the forces at play, which the team now shares.

## Worked example 2: queue versus topic

A distributed architecture must send trade information to both a notification service and an analytics service. Queue or topic?

**With queues,** every consumer needs a separate queue. That is useful if the two consumers need different information, since you can send different messages to each. The producer is aware of every system it communicates with, which makes it harder for another — potentially rogue — service to listen in, so it is better where security is high on the priority list. Each queue is independent, so it can be monitored and scaled separately. But the producer is tightly coupled to its consumers: it knows exactly how many there are, and adding a third means reworking the producer.

| Queue advantages | Queue disadvantages |
|---|---|
| Supports heterogeneous messages for different consumers | Higher degree of coupling |
| Allows independent monitoring of queue depth | Producer must connect to multiple queues |
| More secure | Requires additional infrastructure |
| | Less extensible — must add queues for more consumers |

**With topics,** extensibility is the clear advantage: any new consumer subscribes without touching existing behavior. The downsides follow from the same property — every consumer must consume the same message, which invites stamp coupling, and every consumer can read the entire message, which raises the question of whether everyone should be able to.

| Topic advantages | Topic disadvantages |
|---|---|
| Low coupling | Homogeneous message for every consumer |
| Producer generates just one message | Cannot monitor or scale individual consumers |
| More extensible and evolvable | Less secure |
| | Fewer scalability options |

Now return to the organizational goals. If security matters more, queues. If the organization is growing rapidly and other services will want this data, extensibility dominates and topics win.

**One check before ruling out topics on the monitoring argument**: verify whether that limitation is intrinsic to the pattern or specific to your broker. Some protocols separate the exchange the producer sends to from the queue the consumer listens on, which restores per-consumer monitoring and programmatic load balancing. A trade-off that belongs to the product rather than the approach should not rule out the approach.

## Weighting: the step that decides the answer

The common failure is understanding the trade-offs correctly and not knowing how to weight them for the current context.

Take the shared library matrix above. Five positives to two — but do all the criteria carry equal weight?

Imagine a team with code on several platforms, not overly concerned with performance or scale, wanting a clean way to manage shared behavior. Now the first two factors carry far higher priority than the other five, and the team should choose the **shared service**. As a bonus, they already know exactly which issues they will have to mitigate, because the matrix listed them.

Architects rely on experience to build the criteria, and must also weight them to find the correct fit. **Generic trade-off analysis is not very useful. It becomes valuable only when applied in a specific context.**

## Why you cannot do this once

Two problems with trade-off analysis as a one-time exercise.

There are often dozens or even hundreds of variables, technical and otherwise, contributing to a decision: complexity, team experience, budget, team topology, schedule pressure. The list does not end. Subtle differences in those variables push a particular analysis one way or the other.

So it is dangerous to make sweeping, semi-permanent decisions based on assumptions that may not be valid for future applications of the same solution. Teams love standards, and it would be convenient to hold one big settlement deciding defaults for style, communication and shared functionality — but every situation requires re-evaluating those trade-offs. Teams that default to one communication pattern for all distributed workflows discover it works sometimes and fails spectacularly at other times.

The real job is trade-off analysis, not making permanent perfect decisions.

## Finding a hidden trade-off

When a decision seems to have no trade-offs, keep looking.

Consider code reuse. Surely purely beneficial — the more code an organization reuses, the less it must write. Two factors dictate how effective reuse will be, and architects reliably find the first and miss the second.

**Abstraction.** If the code can be abstracted and used from multiple call points, it is a candidate for reuse. This one is obvious.

**Low volatility.** When a team reuses a module that is always changing, it creates churn in the entire system. Every time the shared code changes, all callers must coordinate around that change — and even when it is not a breaking change, the team must still verify that nothing broke. Reuse code inappropriately and teams end up chasing breaking changes all over the architecture.

That is the hidden trade-off: **effective reuse requires good abstraction *and* low volatility.**

Which explains why the most successful reuse targets are plumbing — technology frameworks, libraries, platforms. The portion of most applications that changes fastest is the domain, the motivation for writing the software in the first place, so domain concepts are terrible candidates for reuse. It is also the reasoning underneath bounded contexts, where no context reuses another's implementation details.

And it produces one request that cannot be satisfied. Organizations frequently ask for both a highly decoupled architecture *and* a high degree of institutional reuse, so teams are not constantly rewriting code. Those two things are fundamentally incompatible, because **the way a system implements reuse is via coupling.**
