# Distributed fundamentals

Read whenever a distributed style is on the shortlist. These are the costs that are always underestimated, and the arithmetic that decides feasibility.

## The eleven fallacies

Eight were named in 1994 and all still hold. Three more are worth adding.

**1. The network is reliable.** It is not. A healthy service can be unreachable, or can process a request and return nothing because the response was lost. This is why timeouts and circuit breakers exist. The more a system leans on the network, the less reliable it is.

**2. Latency is zero.** A local call costs nanoseconds or microseconds; a remote call costs milliseconds. See the arithmetic below — this is usually the fallacy that decides feasibility.

**3. Bandwidth is infinite.** Irrelevant inside a monolith, dominant between services. See stamp coupling below.

**4. The network is secure.** The threat surface grows by magnitudes moving from monolith to distributed. Every endpoint must be secured, including interservice calls, and that is part of why synchronous distributed styles are slow.

**5. The topology never changes.** It changes constantly. A "minor" overnight network upgrade can invalidate every latency assumption and trip all your timeouts and circuit breakers simultaneously, with no deployment to blame.

**6. There is only one administrator.** A large company has dozens of network administrators. Coordination cost is part of the price of distribution.

**7. Transport cost is zero.** This is money, not latency. Distributed architectures cost significantly more in hardware, servers, gateways, firewalls, subnets and proxies. Analyze your current server and network topology for capacity, bandwidth, latency and security zones before committing, so this does not arrive as a surprise.

**8. The network is homogeneous.** Infrastructures mix vendors. Not every combination is fully tested under every load, packets get lost, and that feeds back into every other fallacy.

**9. Versioning is easy.** Versioning contracts is reasonable and drags in decisions teams do not anticipate: version per service or per system; how far through the architecture versioning must reach; how many versions to support at once (teams accidentally end up honouring dozens); and whether deprecation happens system-wide or service by service.

**10. Compensating updates always work.** The pattern where a coordinator reverses a multi-service update on partial failure is assumed reliable and is not. A transactional workflow design must state what happens when the update *and* its compensating update both fail.

**11. Observability is optional.** Logging is useful in a monolith and critical in a distributed architecture, which has many communication failure modes that cannot be debugged without comprehensive interaction logs. Treat it as a driving characteristic, not an operational add-on.

## Latency arithmetic

Get the actual production round-trip figure — a network administrator usually has it — and get the **95th to 99th percentile**, not the average.

A system averaging 60 ms may have a 95th percentile of 400 ms. It is that long tail that kills performance in a distributed architecture.

Then multiply by hop count. At 100 ms average per hop, a business function spanning ten chained service calls adds a full second. Use that number, not the average, to decide whether a fine-grained decomposition is feasible.

## Stamp coupling

A service returning its full payload when the caller needs a fraction of it consumes bandwidth out of all proportion to the information transferred.

The arithmetic at scale: a 500 KB response of 45 attributes, called 2,000 times a second so the caller can read a 200-byte name, burns **1 GBps**. Returning only the needed 200 bytes costs **400 Kbps** — a factor of about 2,500.

Fixes, in rough order of preference:

- Private API endpoints scoped to the caller
- Field selectors in contracts
- A query layer that lets the caller specify the shape it needs
- Value-driven or consumer-driven contracts
- Internal messaging endpoints

Whichever technique, the principle is that services transmit only the necessary data. Recheck bandwidth afterwards, since bandwidth pressure feeds back into latency and reliability.

One caveat for broadcast architectures: consumer-driven contracts, the usual fix, are hard to apply where the publisher cannot know which processors will respond.

## Preventing data loss in asynchronous flows

Messages get lost at exactly three points, each with its own mechanism. None of the three covers another.

**1. Producer to broker.** The producer publishes and crashes before acknowledgment, or the broker acknowledges and crashes before a consumer takes the event. Fix with *persistent message queues* — the broker writes the event to disk or a database as well as memory, so it survives a restart — plus *synchronous send*, where the producer blocks until the broker confirms persistence.

**2. Broker to consumer.** The consumer takes the event off the queue and crashes before processing it. Fix with *client acknowledge mode*: by default auto-acknowledge removes the event the moment it is read, whereas client acknowledge leaves it in the queue with the client ID attached so no other consumer can take it.

**3. Consumer to database.** The consumer cannot persist because of a data error. Fix with an ordinary database transaction and commit, plus *last participant support*, which removes the event from the queue only after confirming all processing completed and the data is persisted.

Protocol notes. Under a publish-subscribe protocol with exchanges, events are published to an exchange that forwards to a per-consumer queue using binding rules. Topic-based messaging APIs use topics rather than two-step forwarding and require consumers to be configured as **durable subscribers** — guaranteed to receive the event, with the topic holding it while the consumer is down. Streaming brokers use entirely different techniques; consult their own documentation.
