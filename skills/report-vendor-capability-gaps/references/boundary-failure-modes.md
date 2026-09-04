# Failure modes at an integration boundary

Read when writing the report's failure-mode section, or whenever someone claims a vendor's SLA
makes an integration safe.

Contents: [the governing asymmetry](#the-governing-asymmetry) · [how a boundary failure reaches you](#how-a-boundary-failure-reaches-you) ·
[the failure catalogue](#the-failure-catalogue) · [what protection must exist on your side](#what-protection-must-exist-on-your-side) ·
[the arithmetic that kills SLA arguments](#the-arithmetic-that-kills-sla-arguments) · [diagnostic signatures](#diagnostic-signatures)

## The governing asymmetry

Network failures come in two shapes with opposite consequences.

**Fast failure.** Connection refused, a reset because nothing is listening. Returns to the caller
in single-digit milliseconds. Every language surfaces it clearly as an exception, so programmers
handle it. This is the failure everyone designs for.

**Slow failure.** A full listen queue, a dropped acknowledgement, a peer that accepts the
connection and then takes minutes to answer. The calling thread blocks. A blocked thread processes
no other work, so capacity falls. Enough blocked threads and the service is down — not because the
vendor is down, but because the vendor is slow.

**The vendor outage is the easy case.** A report whose risk section covers only outages has
covered the failure that will not hurt you. Rank by slowness.

## How a boundary failure reaches you

The durations a blocked thread waits are set by the operating system, not by your application, and
they are much longer than intuition suggests:

- A reset from an unused port on the same switch returns in **under ten milliseconds**.
- A connection attempt sitting in a **full listen queue** blocks inside the kernel until the remote
  application accepts or the OS connection timeout fires. Those timeouts are measured in **minutes**
  — a thread can block for ten minutes merely trying to connect.
- Once connected, a **write** can block for **tens of minutes** as buffers fill.
- A **read** on an established connection where the peer never answers can block **indefinitely**.

Two structural facts make this worse:

**Default timeouts are usually infinite.** Many remote-call protocols and client libraries ship
with no timeout at all. The absence is not visible in the code, only in production.

**The layer where a failure shows is not the layer where it lives.** Layered protocols hide the
failure: a problem in the network or in the far side's storage arrives at your code as an
application-level error of some unrelated shape, or as nothing at all.

**A middlebox can reap idle connections and tell neither end.** A firewall, NAT or load balancer
keeps its own table of established connections with a last-packet timestamp and drops entries idle
past its timeout — an hour is a common setting. The protocol has no provision for a third party
tearing down a connection, and unreachable notifications are often suppressed deliberately, so both
endpoints still believe the connection is alive. The next call on a pooled connection blocks
forever. The signature is a hang that recurs at a fixed interval after idle periods.

**The vendor's client library is the least-hardened code in your process.** A vendor may harden the
server software it sells widely; its client library rarely gets the same treatment, and it runs
inside your process with your threads. The prime hazard is blocking: internal pools, unbounded
reads, its own serialization. A callback-style interface is especially opaque — nothing in the
signature says which thread runs your callback, how many run concurrently, or what happens if
yours throws. Wrap such libraries in your own bounded worker pool rather than letting their
threading model become yours.

## The failure catalogue

Each entry: mechanism, tell, and what it means for the capability report.

**Blocked threads.** The proximate cause of most user-visible outages. Threads wait on a resource
that never becomes available. *Tell:* low CPU across web, application and database tiers while
nearly every request-handling thread is busy for many seconds. Low CPU with high thread occupancy
means the threads are not working, they are waiting.

**Cascading failure.** A crack in one layer triggers one in the caller. The transmission mechanism
is almost always a **resource pool**: calls into the failing provider never return, threads holding
pooled connections block forever, and every other thread then blocks waiting to check out a
connection that will never come back. This means **two** timeouts are needed and teams routinely
set only the first: a timeout on the remote call, *and* a bound on how long a thread may wait to
check out a connection.

**Chain reaction.** In a load-balanced layer, losing one node raises each survivor's own load by far
more than the redistributed share suggests. In an eight-node farm each carries 12.5%; after one
dies the remaining seven carry 14.3% each — a ~15% increase in that server's load. In a two-node
cluster the survivor's load doubles. If the first failure was load-related, every survivor is now
closer to the same failure, and the interval between failures accelerates.

**Slow responses — four distinct mechanisms.** Telling them apart from outside is what makes an
incident diagnosable.
- *Excessive demand:* every handler busy, no slack to accept work.
- *Memory leak:* presents as **high CPU that is entirely garbage collection** rather than
  transaction work. That distinction is the tell separating it from genuine load.
- *Network congestion:* rare on a LAN, real across a WAN, worse the chattier the protocol.
- *A slow downstream:* the slowness is inherited, and propagates upward layer by layer.

**Unbounded result sets.** The standard shape — query, loop over results, build an object per row —
has no upper bound, so the far side decides how much memory you allocate. A table that should never
have exceeded a thousand rows accumulated more than ten million; selecting all of them exhausted
the heap and crashed the process, whereupon the next instance picked up the same work and crashed
identically, rolling through the whole fleet. Development and test data are always small, so this
is invisible until production. Reframed correctly it is a **handshaking failure**: the caller
allowed the other system to dictate terms. The caller should always state how much it will accept.

**Unbalanced capacities.** The front end can always overwhelm the back end, and the imbalance is
usually *correct* engineering — sizing every downstream service to absorb the entire front end
would leave it idle almost always. The consequence is that the caller structurally retains the
ability to flood the provider, and the trigger is a **change of mix**, not a change of volume: a
promotion can multiply the fraction of requests that touch one vendor call without changing total
traffic at all. Test environments hide this by running near one-to-one ratios.

**Scaling effects.** Any many-to-one relationship works at the ratio you tested and breaks at the
ratio you deploy. Development runs on one machine, test on one or two, production on many, so the
tested ratio is never the production ratio. These cannot be tested out; they must be designed out.

**Exclusive shared resources.** A shared resource that can serve several consumers at once is not a
stability risk — saturation is answered by adding more. The dangerous shape is one allocated for
*exclusive* use while a client processes a unit of work: a lock manager, a coordinator, a
single-writer vendor endpoint. Contention scales with both client count and transaction rate, so it
worsens quadratically, and the terminal form is data integrity loss rather than mere slowness.

**Dogpiles.** Independent callers synchronise themselves and produce a transient spike you must buy
capacity for. Two mechanisms: **startup load is qualitatively different from steady-state load** (a
farm booting together all connect, load seed data and run with cold caches, so most requests become
downstream queries until the working sets warm), and scheduled work on round numbers of the clock.
Fix with randomised clock slew on scheduled jobs, randomised increasing backoff rather than fixed
retry intervals, and staged rather than simultaneous restarts.

**A cache in front of a slow vendor can be the failure.** The textbook protection for an undersized
vendor is a read-through cache. The defect is structural, not functional: if the cache lookup is a
critical section and the vendor call happens *inside* it, exactly one thread can be in the miss
path at a time. When the vendor stops responding, that thread never returns and every other thread
calling the cache blocks behind it. The mechanism added to reduce vendor load becomes the mechanism
that converts vendor slowness into a total hang. Also: an unbounded cache does not merely waste
memory — it makes the collector work ever harder to free space, so the cache itself causes the
slowdown it was meant to prevent.

**Uncancellable work.** Your timeout ends *your* wait. The far side never learns you left and
continues, completes, and may change state you have stopped watching for. Every timeout on a
state-changing vendor call therefore leaves an unknown-outcome record that something must reconcile.

**Self-inflicted spikes.** Your own organisation manufactures the traffic that kills the
integration — a marketing send, a batch job, a fleet-wide configuration pull. Worth a line in the
report because the vendor's rate limit is sized against your *average*, and marketing does not read
the capability report.

**Automation amplifies.** Control-plane automation acts on a *belief* about the system's state. When
that belief is wrong it acts confidently and fast, and by the time a human perceives the problem it
is a recovery job rather than an intervention.

## What protection must exist on your side

State these in the report as requirements, not suggestions — they are the price of the integration
regardless of what the vendor promises.

**Timeouts on everything, plus a pool checkout bound.** Both. The second is the one that stops a
cascade jumping the gap.

**A per-integration-point connection pool** with a runtime-settable maximum. Give each integration
point its own pool rather than sharing one across back ends. The maximum and the checkout block
time should be changeable at runtime, because that pool is the only available throttle when a
vendor degrades and you cannot wait for a release. Setting the maximum to zero disables the
capability cleanly and lets the application degrade to a stated user-visible message.

**A circuit breaker per integration point per process.** It must be scoped to one process — sharing
breaker state across instances would be more efficient but makes the breaker itself a shared
resource and a new failure mode. Trip on **fault density, not fault count**: five faults over five
hours and five faults in thirty seconds mean entirely different things, and a leaky-bucket counter
(increment on fault, decrement on a timer) distinguishes them cheaply. Track failure types
separately, with a lower threshold for call timeouts than for connection-refused. Decide the
open-circuit fallback with business stakeholders and write it down as a degraded-mode requirement —
that decision is theirs, not engineering's. Log every state transition; breaker state changes are a
leading indicator worth trending.

**Bulkheads.** Partition capacity so one failure destroys part of the system rather than all of it.
The granularity ladder runs from thread pools inside a process, through instance and server
boundaries, to whole farms and zones. The case that matters for a shared core: when two of your
systems both call one vendor service, dedicate capacity to each rather than pooling, so one
consumer cannot starve the other.

**Fail fast.** A slow failure response is the worst outcome available — all the resource
consumption of a real transaction and none of the value. Before starting work, validate parameters,
work out which connections and integration points the transaction will need, check them out
up front, and verify the relevant breakers are closed. If any is unavailable, fail immediately and
completely so the caller can get on with something else.

**Bound every queue, and choose the overflow policy deliberately.** An unbounded queue consumes all
memory, and as its length grows so does response time without limit. Once bounded, a full queue
leaves exactly four options and all are unpleasant: drop the newest, drop something already queued
(prefer dropping oldest where value decays with age), refuse the caller, or block the caller.
Blocking *is* back pressure, and it only works safely with a finite consumer pool.

**Shed load at the edge.** Anything with an open interface has zero control over its demand.
Services usually collapse *before* the listen queue fills, and the cause is almost always
contention for a pooled resource. Reject early rather than timing out slowly — a quick rejection is
better than a slow timeout.

**A governor on automation.** Limit the rate at which automated action can be taken against the
integration, and apply resistance only in the unsafe direction. List the actions the automation can
take, mark each safe or unsafe, define the safe range, and apply increasing delay outside it rather
than a hard stop — keeping humans available without putting them in the loop for everything.

**Steady state.** Every mechanism that accumulates a resource needs a matching mechanism that
recycles it. The reason is not tidiness: a system needing regular manual crank-turning keeps
administrators logged into production, and every human touch there is an opportunity for unforced
error. The bar to aim for is surviving one release cycle with no human intervention.

**"Let it crash" has three preconditions** and a slow-starting bought core fails all of them:
limited granularity (something can die without taking the process with it), fast replacement
(restart time decides feasibility), and supervision separate from the calling system. Measure the
actual restart time before proposing this.

## The arithmetic that kills SLA arguments

Safety is not a composable property. Two services that are each safe alone do not compose into a
safe system.

Worked: a client enforces a 50 ms timeout. Each provider responds in 20 ms on average with an
observed 99.9th percentile of 30 ms. Calling either is comfortably safe. Calling both in sequence
still averages inside the 50 ms budget — but a sizable share of calls breach it, because the tails
add. The mean is reassuring and irrelevant; the tail is what times out.

Use this whenever someone offers a per-call vendor SLA as evidence that a composite operation is
safe. It is the single most reliable way to move that conversation.

Related: **outage probabilities do not multiply.** Independent-failure arithmetic assumes
independence that coupled layers do not have. Two components each "99.9% available" sharing a
network, a dependency or a deployment do not give you 99.8%.

## Diagnostic signatures

Worth memorising; each identifies its cause from outside.

| Signature | Cause |
|---|---|
| Low CPU everywhere, nearly all request threads busy > 5s | Blocked threads waiting on a pool or a remote call |
| High CPU that is entirely garbage collection | Memory leak, not load |
| A burst of wrapped exceptions that abruptly **stops** | Not recovery — the pool just emptied and callers now wait forever |
| Hangs recurring at a fixed interval after idle periods | A middlebox reaping idle connections |
| Instances crashing in a rolling sequence, each picking up the last one's work | Unbounded result set plus transactional retry |
| Vendor dashboard green, integration failing | Hung is not crashed; internal monitors report healthy |
| Your latency fine, users report slowness | You are measuring processing time, not residence time |

**Residence time, not processing time.** A request's total time at a service is queue time plus
processing time, and the commitment applies to the whole of it. Measuring only your own processing
time is why a service can believe all is well while its consumers complain. The asymmetry is
structural: the queue is serial while processing is concurrent, so under load queuing dominates.
When assessing a vendor's latency claim, establish which one they are quoting.
