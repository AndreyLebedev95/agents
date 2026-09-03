# Communication patterns

Read when the communication decision is live. These are patterns, not styles — any distributed architecture can use any of them, and the choice must be re-analyzed per workflow rather than settled once organization-wide.

## Contents
- [The default](#the-default)
- [Responsiveness is not performance](#responsiveness-is-not-performance)
- [Events versus messages](#events-versus-messages)
- [Queues versus topics](#queues-versus-topics)
- [Request-reply](#request-reply)
- [Orchestration versus choreography](#orchestration-versus-choreography)
- [Choosing a mediator technology](#choosing-a-mediator-technology)
- [Event payload design](#event-payload-design)
- [Error handling in asynchronous flows](#error-handling-in-asynchronous-flows)
- [CQRS](#cqrs)
- [Broker topology](#broker-topology)

## The default

Default to synchronous; go asynchronous only where necessary. Synchronous presents fewer design, implementation and debugging challenges. Asynchronous buys performance and scale at the cost of data synchronization, deadlocks, race conditions and debugging difficulty.

What forces asynchrony is a characteristics mismatch across the boundary. Two quanta with different operational characteristics communicating synchronously means the caller inherits the callee's limits: a service handling one payment every 500 ms will start failing the moment many workflows complete at once. A queue absorbs that. But note the limit — a queue buffers *bursts*, not sustained excess; under sustained overload it only delays the failure.

The deeper reason to care: synchronous communication between two architecture quanta fuses them into one. They become dependent, so they share one set of architecture characteristics whether you intended that or not.

## Responsiveness is not performance

Two different things, and conflating them wastes optimization effort.

**Responsiveness** is how fast the user is told the action was accepted. **Performance** is how fast the work actually finishes.

Worked: a comment taking 3,000 ms to validate costs the user 3,100 ms synchronously (50 ms latency each way) and 25 ms asynchronously — while the system still takes 3,025 ms end to end. Nothing about the work got faster. Optimizing the validation itself, by parallelizing the parsing engines or caching, would be a performance improvement.

So ask whether the user needs information back, or only an acknowledgement. Where only an acknowledgement is needed, make it asynchronous rather than optimizing the work.

The cost is the guarantee. Synchronously the user knows it posted; asynchronously they have a promise. If the work later fails — profanity rejection, a trade that cannot execute — there must be a path back to the user, which requires knowing who they are. **Error handling is the hard part of asynchronous design**, and it is what makes the difference between a cheap win and a liability.

## Events versus messages

Four tests separate them, and the distinction is not cosmetic — it is what makes the architecture decoupled.

| | Event | Message |
|---|---|---|
| What it says | Something already happened | A command or query: something needs doing |
| Response | Usually none required | Usually required |
| Recipients | Broadcast to many | Almost always one |
| Channel | Topic, stream, notification service | Queue or messaging service guaranteeing one recipient |

The trap: **broadcasting a command over a publish-subscribe channel does not make it an event**. "Turn to page 145" is a message even when the whole class hears it.

Event-driven architectures are mostly events and legitimately use messages — to request data from another processor, or in mediated topologies to control processing order.

## Queues versus topics

Broadcasting to a topic buys **architectural extensibility** — a new consumer subscribes with no change to producer or infrastructure — and **producer decoupling**, since the producer does not know who consumes.

It costs **data-access control** (a topic is easy to wiretap; a queue is not, because stealing from a queue is detected when the intended consumer stops receiving), forces **one homogeneous contract** on all consumers, and in many implementations blocks **per-consumer monitoring and autoscaling**.

Point-to-point queues invert every one of these. With queues, each consumer can have its own contract carrying only what it needs, each queue is independently monitorable and scalable, and the producer knows exactly who it talks to — which is tighter coupling and better security.

Choosing: if consumers will be added often and their identity is not the producer's business, prefer a topic. If consumers need different contracts, or the payload is sensitive, or each consumer must scale independently, prefer queues.

**One important check before ruling out topics on the monitoring argument**: verify whether it is intrinsic to the pattern or specific to your broker. Some protocols separate the exchange the producer sends to from the queue the consumer listens on, which restores per-consumer monitoring and programmatic load balancing. Ruling out a whole pattern over a vendor limitation is a common and expensive mistake.

## Request-reply

Where a processor genuinely needs an immediate answer, asynchronous architectures use request-reply (pseudosynchronous) messaging: each channel is two queues, a request and a reply.

**Correlation ID (preferred).** The producer sends to the request queue and remembers the message ID, then does a blocking wait on the reply queue with a message selector filtering for correlation ID equal to that message ID. The consumer echoes the original message ID as the correlation ID on its response, so the producer picks up only its own reply and ignores other messages sharing the queue.

**Temporary queue.** The producer creates a per-request queue, names it in the reply-to header, waits on it with no selector needed, and deletes it when the reply arrives.

Prefer the correlation ID. The temporary-queue technique is simpler and forces the broker to create and immediately delete a queue per request, which slows it significantly at high volume and concurrency.

Note that request-reply reintroduces the quantum fusion that asynchrony was meant to avoid, if the caller cannot proceed without the answer.

## Orchestration versus choreography

**Orchestration advantages.** A centralized workflow, so as complexity rises one component owns state, behavior and boundary conditions. Error handling, a major part of most domain workflows, is helped by having a state owner. Recoverability: the orchestrator sees workflow state and can retry through a short-term outage. State management: workflow state becomes queryable, giving other workflows a place to read transient state.

**Orchestration disadvantages.** Responsiveness — all communication passes through the orchestrator, a potential throughput bottleneck. Fault tolerance — it is a single point of failure for the workflow, addressable by redundancy at the cost of complexity. Scalability — coordination points cut potential parallelism. Coupling between the orchestrator and the domain components.

**Choreography advantages.** Responsiveness, from fewer chokepoints and more parallelism. Scalability, from the absence of coordination points. Fault tolerance, since multiple instances can run — multiple orchestrators are possible but more sensitive, because all communication must still pass through them. Decoupling.

**Choreography disadvantages.** No workflow owner, making errors and boundary conditions harder to manage. No centralized state holder. Harder error handling, because each domain service must carry more workflow knowledge. Harder recoverability, with nothing to attempt retries.

**The trade-off in one line:** workflow control and error-handling capability against performance and scalability.

Expect a hybrid. Dynamic processing inside a complex flow is very hard to model declaratively, so most real systems orchestrate the general path and choreograph the atypical errors and exceptional conditions.

## Choosing a mediator technology

Choose by the nature of the workflow, not by preference. Getting it wrong is expensive in both directions.

| Workflow | Technology class |
|---|---|
| Simple error handling and orchestration | Integration and routing frameworks, with flows written as ordinary program code |
| Heavy conditional processing, multiple dynamic paths, complex error-handling directives | A process-execution-language engine — powerful, hard to learn, usually authored through its GUI tools |
| Long-running transactions requiring human intervention mid-flow | A business process management engine |

The third row is the one people get wrong. A mediator cannot stop, wait for a senior approver, and resume days later; a process engine can. Conversely, using a process engine for simple flows wastes months on something a routing framework handles in days.

Since events rarely fall into one complexity class, classify each event as **simple, hard or complex**, route everything through a simple mediator, and have it either handle the event itself or forward the initiating event to the heavier mediator. Decide explicitly whether the simple mediator retains responsibility for knowing when the delegated workflow completed, or hands off entirely including client notification.

## Event payload design

Two options, with cleanly inverted trade-offs. Decide **per event type**, not once for the system.

| Criterion | Data-based payload | Key-based payload |
|---|---|---|
| Performance and scalability | Good | Bad — every consumer must query |
| Contract management | Bad | Good |
| Stamp coupling | Bad | Good |
| Bandwidth utilization | Bad | Good |
| Works with restricted database access | Good | Bad |
| Overall system fragility | Bad | Good |

It reduces to **scalability and performance against contract management and bandwidth**.

Choose data-based where the event needs extreme scale and performance, or where consumers cannot reach the data at all — under strict bounded contexts or database-per-service. Choose key-based where the underlying data changes frequently during processing, or where contract churn would be costly.

The hidden cost of data-based payloads: they create a second system of record, so data goes stale. A customer correcting an order immediately after placing it leaves the database right and in-flight events wrong — and because event timing cannot be controlled, newer values may be processed *before* older ones and then be overwritten by them.

**Three payload failure modes:**

- **Anemic events** carry too little for consumers to decide what to do, and querying the database does not rescue them. A `profile_updated` event carrying only a customer ID leaves consumers unable to know which fields changed, whether they need to act, or what the prior values were — and databases typically do not retain prior values. For state changes, include both new and prior values.
- **Swarm of Gnats** is the opposite error at the *event* rather than payload level: one processor emitting too many small derived events for what is really one action. It saturates the system with events about the same thing, proliferates further small events downstream, and eventually makes the flows impossible for anyone to understand. Bundle multiple field changes from one user action into a single event carrying before and after values.
- **Over-coarse events** force every consumer to subscribe, open the payload and decide whether it applies, wasting bandwidth and processing on consumers who need not act. Split into one derived event per distinct outcome, so consumers subscribe only to what concerns them.

The rule that resolves both granularity errors: **key event granularity to outcomes** — the outcome of the processing or the state change.

**Two design habits worth keeping.** Model both success and failure as separate derived events, and graduated outcomes as graduated events, because different downstream processors care about different results. And emit **extensible derived events** — advertise what you did even when nobody is listening. An unlistened event costs almost nothing and leaves a built-in hook, so future functionality arrives as one new processor with no changes to any existing one.

**Watch for poison events**: a derived event triggered and responded to in a continuous loop between services. Draw the derived-event graph and look for cycles; at each processor, ask whether advertising this particular action closes one.

## Error handling in asynchronous flows

Delegation, containment and repair. When a consumer hits an error, it immediately hands the error to a separate workflow-processor service and moves to the next message. Responsiveness is preserved because the consumer never stops to diagnose — if it did, it would delay not just the failed message but every message behind it.

The workflow processor then diagnoses and attempts programmatic repair, resubmitting to the original queue where the consumer sees it as a new message. Where it cannot determine the problem, it routes to a queue feeding a human dashboard; the operator fixes and resubmits, usually via the reply-to header.

**The cost is sequence.** A message pulled out for repair and resubmitted is processed after messages that arrived behind it. Where order matters within a context — all trades in one account must execute in sequence, a sell before a buy — this silently corrupts the workflow.

Preserving order per context: when a message errors, record its context key; divert all subsequent messages carrying that key into a temporary FIFO queue; once the erroneous message is repaired and processed, dequeue the held messages and process them in order.

## CQRS

Command-Query-Responsibility-Segregation splits a single application-to-database interaction into two: writes go to one datastore — usually a database, sometimes a durable queue — which synchronizes, usually asynchronously, to a second database serving reads.

Apply it where read and write volumes differ starkly, or where reads must be isolated from writes for security or other reasons. The payoff is that reads and writes can be given different architecture characteristics and, if needed, different data models.

## Broker topology

In event-driven choreography the topic or queue is typically owned by the sender, so the infrastructure supporting a service includes its broker.

**Single broker.** Centralized discovery — every processor knows where to subscribe — a single place for logging, monitoring and governance, and the least possible infrastructure. Costs fault tolerance, since the broker failing stops the entire workflow, and throughput, since it can be swamped as volume grows.

**Domain broker.** Each group of related services gets its own broker, mirroring the architecture's domain partitioning. Buys better isolation, alignment with domain boundaries, and more scalability, elasticity and fault tolerance. Costs harder discovery of queues and topics, more infrastructure and expense, and more moving parts to maintain.

Neither is a best practice. The choice balances discovery against domain isolation, and it deserves the same weight as the service topology decision.
