# Tactics catalog

Tactics grouped by the goal each category serves. Every entry needs refining into a concrete
mechanism before it is a design decision.

These lists are not closed — they were derived from a model of each attribute and can be extended
the same way (see `model-a-new-quality-attribute`).

## Contents
- [Availability](#availability) — detect / recover / prevent faults
- [Deployability](#deployability) — manage the pipeline / manage the deployed system
- [Energy efficiency](#energy-efficiency) — monitor / allocate / reduce demand
- [Integrability](#integrability) — limit dependencies / adapt / coordinate, plus the five distances
- [Modifiability](#modifiability) — increase cohesion / reduce coupling / defer binding
- [Performance](#performance) — control resource demand / manage resources
- [Safety](#safety) — avoid / detect / contain / recover
- [Security](#security) — detect / resist / react / recover
- [Testability](#testability) — control and observe state / limit complexity
- [Usability](#usability) — support user initiative / support system initiative
- [Super-tactics](#super-tactics)

---

## Availability

Goal: keep faults from becoming failures, or at least bound the fault's effects and make repair
possible. These are often supplied by infrastructure such as a middleware package, so the architect's
job is frequently choosing and assessing the right combination rather than implementing it.

### Detect faults

- **Monitor** — a component watching the health of other parts: processors, processes, I/O, memory.
  Can detect failure or congestion in the network or other shared resources, including from a
  denial-of-service attack. It orchestrates the other detection tactics: initiating self-tests,
  detecting faulty timestamps or missed heartbeats. *Refinement:* when implemented as a counter or
  timer that is periodically reset, it is a **watchdog**; the monitored process resets the counter as
  its signal that it is working.
- **Ping/echo** — an asynchronous request/response pair between nodes, determining reachability and
  round-trip delay. The echo also proves the pinged component is alive. Requires a time threshold
  telling the pinger how long to wait before declaring a timeout.
- **Heartbeat** — periodic message exchange between a monitor and a monitored process. Differs from
  ping/echo in *who initiates* the health check — the monitored component rather than the monitor.
  Where scalability matters, piggyback heartbeats onto other control messages to cut transport and
  processing overhead.
- **Timestamp** — detects incorrect *sequences* of events, chiefly in distributed message-passing
  systems. Assign a local clock value immediately after the event. Sequence numbers can substitute,
  since distributed timestamps may be inconsistent across processors.
- **Condition monitoring** — check conditions in a process or device, or validate assumptions made
  during design; checksums are the common example. The monitor must itself be simple and ideally
  provably correct, or it introduces new errors.
- **Sanity checking** — check the validity or reasonableness of specific operations or outputs, based
  on knowledge of internal design, system state, or the nature of the information. Most often
  employed at interfaces, examining a specific information flow.
- **Voting** — compare results from multiple sources that should agree, and decide which to use.
  Depends critically on the voting logic (keep it a simple, rigorously reviewed singleton) and on
  having multiple sources. Three schemes, **not interchangeable**:
  - *Replication* — exact clones. Effective against random hardware failure. Cannot protect against
    design or implementation errors, since there is no diversity.
  - *Functional redundancy* — design diversity, addressing common-mode failures where replicas share
    an implementation and so fail identically. Still vulnerable to specification errors, and more
    expensive to develop and verify.
  - *Analytic redundancy* — diversity in inputs and outputs as well as internals, using separate
    requirement specifications, so it tolerates specification errors and copes when some inputs are
    intermittently unavailable. Needs a sophisticated voter: it may have to know which sensors are
    currently reliable and to produce a higher-fidelity value than any single component by blending
    and smoothing over time.
- **Exception detection** — detect a condition that alters the normal flow of execution.
  *Refinements:* system exceptions (divide by zero, bus and address faults, illegal instructions —
  these vary by processor architecture); **parameter fence**; **parameter typing**; **timeout**.
- **Self-test** — a component tests itself, typically on a schedule or on demand from a monitor.

### Recover from faults

*Preparation and repair:*

- **Redundant spare** — a standby ready to take over.
- **Rollback** — revert to a previous known good state.
- **Exception handling** — handle the detected exception rather than propagating a failure.
- **Software upgrade** — in-service change. *Refinements:* function patch, class patch, hitless
  in-service software upgrade.
- **Retry** — repeat the operation, on the assumption the fault was transient.
- **Ignore faulty behavior** — deliberately disregard messages or events known to be spurious.
- **Graceful degradation** — drop less critical function to keep the critical function running.
- **Reconfiguration** — remap the logical architecture onto the resources still functioning.

*Reintroduction:*

- **Shadow** — run a recovered component in shadow mode before restoring it to service.
- **State resynchronization** — bring a returning component's state back in line.
- **Escalating restart** — restart at the smallest scope that fixes it, escalating only as needed.
- **Nonstop forwarding** — keep forwarding while control-plane state is rebuilt.

### Prevent faults

- **Removal from service** — take a component out deliberately. *Refinements:* software
  rejuvenation, therapeutic reboot.
- **Transactions** — bundle state changes so they cannot partially apply.
- **Predictive model** — monitor state to predict onset of a fault and act before it occurs.
- **Exception prevention** — eliminate the conditions that raise exceptions.
- **Increase competence set** — widen the set of states a component can handle without failing.

---

## Deployability

Goal: get changes into production quickly and safely, and get them back out again.

### Manage the deployment pipeline

- **Scale rollouts** — deploy to a growing subset rather than everything at once.
- **Roll back** — return to the prior release.
- **Script deployment commands** — make the deployment repeatable and traceable rather than manual.

### Manage the deployed system

- **Manage service interactions** — handle multiple versions coexisting in production.
- **Package dependencies** — ship an element with what it needs so deployment does not depend on
  matching the target's state.
- **Feature toggle** — ship the code inert and enable it separately, decoupling deploy from release.

Related patterns: structuring services (including microservice architecture); complete replacement of
services; partial replacement — **canary testing**, **A/B testing**; and the rolling upgrade.

---

## Energy efficiency

Goal: manage or reduce energy consumption **while maintaining a required level of functionality and
acceptable levels of other attributes** — the floor is part of every tactic here.

### Monitor resources

- **Metering** — measure consumption per resource.
- **Static classification** — classify resources by consumption characteristics ahead of time.
- **Dynamic classification** — classify at runtime as behavior changes.

### Allocate resources

- **Reduce usage** — consume less for the same demand.
- **Discovery** — find available resources to shift work onto.
- **Schedule resources** — order work to reduce energy, not just latency.

### Reduce resource demand

Shares its tactics with performance — managing demand rather than assuming it fixed: **manage event
arrival**, **limit event response**, **prioritize events** (potentially letting low-priority events
go unserviced), **reduce computational overhead**, **bound execution times**, **increase efficiency
of resource usage**. All increase energy efficiency by doing less work.

Note the distinction from *reduce usage*: reduce usage assumes demand stays the same, while these
tactics explicitly manage and reduce the demand itself.

Related patterns: sensor fusion, kill abnormal tasks, power monitor.

---

## Integrability

Goal: reduce the cost and risk of adding new components, reintegrating changed components, and
integrating sets of components to meet evolutionary requirements. Achieved either by reducing the
**number** of potential dependencies or the **distance** across them.

### Limit dependencies

- **Encapsulate** — the foundation all the others build on, so seldom seen alone. Introduce an
  explicit interface and ensure all access passes through it, eliminating dependencies on internals.
- **Use an intermediary** — break a direct dependency. *Refinements:* layer, broker, proxy, tier.
- **Restrict communication paths** — limit which elements may talk to which.
- **Adhere to standards** — reduce distance by conforming to something both sides already implement.
- **Abstract common services** — replace several similar dependencies with one general one.

### Adapt

- **Discover** — find the counterpart at runtime rather than binding it earlier.
- **Tailor interface** — add, hide or adapt capabilities of an existing interface without changing it.
- **Configure behavior** — change behavior through configuration rather than code.

### Coordinate

- **Orchestrate** — a control element directs the interaction of components that do not know each
  other.
- **Manage resources** — mediate access to a shared resource among components.

### The five kinds of distance

Integration difficulty is a function of **size** (the number of potential dependencies) and
**distance** (how hard it is to resolve differences at each one). Only the first kind is catchable by
tooling — which is why "it compiles" is weak evidence of integrability.

| Distance | What must be agreed | Detectability |
|---|---|---|
| **Syntactic** | Number and type of shared data elements | Type mismatches are easy to observe and predict — a compiler can catch them. Differences in bit masks are similar in nature but often harder; expect to rely on documentation or code scrutiny |
| **Data semantic** | What the values *mean*, even when types match — one side's altitude in metres against the other's in feet | Typically difficult to observe and predict. Metadata helps; otherwise compare interface documentation or check the code |
| **Behavioral semantic** | Behavior, particularly states and modes — a data element may be interpreted differently during startup, shutdown or recovery. Also control assumptions, such as each side expecting the *other* to initiate | Sometimes captured explicitly in protocols; often not |
| **Temporal** | Assumptions about time — one element emitting at 10 Hz where the other expects 60 Hz; or one expecting event A to follow B, the other expecting A within no more than 50 ms of B | Formally a subcase of behavioral semantics, called out separately because it is so important and so subtle |
| **Resource** | Assumptions about shared resources — one element requiring exclusive device access where another expects shared; two elements needing 12 GB and 10 GB on a 16 GB machine; three elements each producing 3 Mbps into a 5 Mbps channel | Not typically mentioned in any programming-language interface description, which is exactly why it surfaces late |

**Dependencies are not only syntactic.** Components can be coupled *temporally* or by *resources*
(competing for finite memory, bandwidth, CPU, an external device, or a timing dependency) or
*semantically* (sharing knowledge of a protocol, file format, unit of measure, or metadata). Temporal
and semantic dependencies are frequently not well understood, explicitly acknowledged or properly
documented — and missing or implicit knowledge is always a risk on a large, long-lived project.

**Service orientation reduces only syntactic distance.** Services know each other through published
interfaces, and if the interface is a good abstraction, changes ripple less. But supposedly decoupled
components that hold detailed knowledge of each other and make assumptions about each other are in
fact tightly coupled, and changing them later may well be costly. For integrability purposes,
"interface" must mean much more than an API: it must characterize *all* relevant dependencies,
including the unstated implicit ones that add time and complexity to integration, modification and
debugging.

Related patterns: service-oriented architecture, dynamic discovery.

---

## Modifiability

Goal: reduce the cost and risk of making changes. Driven by coupling, cohesion, module size, and the
binding time of the modification.

### Increase cohesion

- **Split module** — when a module carries responsibilities that change for unrelated reasons.
- **Redistribute responsibilities** — move responsibilities so that the ones changing together live
  together.

### Reduce coupling

- **Encapsulate** — introduce an explicit interface; eliminate dependence on internals.
- **Use an intermediary** — layer, broker, proxy, tier.
- **Abstract common services** — factor the duplicated functionality that keeps forcing the same
  change in two places.
- **Restrict dependencies** — limit which modules may depend on which.

### Defer binding

Later binding is generally better, because computers handle change more cheaply and less
error-prone-ly than people do — but the machinery enabling late binding costs more to put in place.
Bind as late as possible *while the mechanism remains cost-effective*.

| Bind at | Tactics |
|---|---|
| Compile or build time | Component replacement (e.g. in a build script or makefile); compile-time parameterization; aspects |
| Deployment, startup or initialization | Configuration-time binding; resource files |
| Runtime | Discovery; interpret parameters; shared repositories |

Related patterns: client-server, plug-in (microkernel), layers, publish-subscribe.

---

## Performance

Goal: reduce latency and increase throughput. Latency has two sources — **processing time and
resource usage**, and **blocked time**, which comes from resource contention, unavailability of
resources, or dependency on other computation.

### Control resource demand

- **Manage work requests** — *refinements:* manage event arrival; manage sampling rate (right for
  some real-time systems, wrong for others, and actively harmful in database or stock-trading systems
  where losing a single event is unacceptable); limit event response; prioritize events.
- **Reduce computational overhead** — *refinements:* reduce indirection; co-locate communicating
  resources.
- **Periodic cleaning** — reclaim degraded state on a schedule.
- **Bound execution times** — cap the time any one request may consume.
- **Increase efficiency of resource usage** — better algorithms and data structures at the hot spots.

### Manage resources

- **Increase resources** — more or faster hardware.
- **Introduce concurrency** — process independent work in parallel.
- **Maintain multiple copies of computations** — e.g. behind a load balancer.
- **Maintain multiple copies of data** — *refinements:* data replication; caching.
- **Bound queue sizes** — trade dropped work for bounded latency.
- **Schedule resources** — needs a chosen scheduling policy: first-in/first-out; fixed-priority
  scheduling (semantic importance, deadline monotonic, rate monotonic); dynamic priority scheduling
  (round-robin, earliest-deadline-first, least-slack-first); static scheduling.

Related patterns: service mesh, load balancer, throttling, map-reduce.

---

## Safety

Goal: keep the system out of an unsafe state space, return it there, or limit the damage on entry.

### Unsafe state avoidance

- **Substitution** — replace a potentially unsafe computation with a safe one.
- **Predictive model** — predict onset of an unsafe state and act first.

### Unsafe state detection

- **Timeout** · **Timestamp** · **Condition monitoring** · **Sanity checking** · **Comparison**

### Containment

- **Redundancy** — spares and the voting schemes above.
- **Limit consequences** — bound what a failure can affect.
- **Barrier** — prevent propagation across a boundary (e.g. firewalls in the physical sense).

### Recovery

Acts to place the system in a safe state. Three tactics:

- **Rollback** — revert to a saved known good state, the *rollback line*, on detecting a failure.
  Often combined with checkpointing and transactions so the rollback is complete and consistent.
  Once the good state is reached, execution continues — potentially with retry or degradation so the
  failure does not immediately recur.
- **Repair state** — repair an erroneous state, effectively widening the set of states the component
  handles competently, then continue. A vehicle's lane-keep assist monitoring whether the driver is
  staying in lane and actively returning the vehicle between the lines is this tactic. **Inappropriate
  as a means of recovery from unanticipated faults.**
- **Reconfiguration** — recover from component failure by remapping the logical architecture onto the
  resources still functioning. Ideally full functionality is maintained; where it is not, partial
  functionality may be maintained in combination with degradation.

---

## Security

Goal: maintain confidentiality, integrity and availability under attack.

### Detect attacks

- **Detect intrusion** · **Detect service denial** · **Verify message integrity** · **Detect message
  delivery anomalies**

### Resist attacks

- **Identify actors** · **Authenticate actors** · **Authorize actors** · **Limit access** · **Limit
  exposure** · **Encrypt data** · **Separate entities** · **Validate input** · **Change credential
  settings**

### React to attacks

- **Revoke access** · **Restrict login** · **Inform actors**

### Recover from attacks

- **Audit** — keep a record sufficient to reconstruct what happened.
- **Nonrepudiation** — ensure parties cannot deny their involvement.

Plus the availability tactics, since recovery from attack is recovery.

**A caution specific to this attribute.** Asking whether a security tactic is "supported" invites a
yes that means nothing. One system met a requirement that no data pass over the network in the clear
by XOR-ing everything before sending it — strictly compliant, and crackable by a schoolchild. Always
record the *mechanism* and the assurance behind it, never just that the tactic is present.

---

## Testability

Goal: make the system reveal its faults easily — and make a bug easier to replicate and to trace to
a root cause.

### Control and observe system state

- **Specialized interfaces** — deliberate test access. *Refinements:* set, get, report, reset.
- **Record/playback** — capture data crossing an interface and replay it. *Refinements:* record;
  playback.
- **Localize state storage** — make the state needed to reach a condition reachable in one place.
- **Abstract data sources** — substitute test data for production sources.
- **Sandbox** — run isolated from real consequences.
- **Executable assertions** — encode expected state in the code so violations surface.
- **Component replacement** — swap a component for a test double.
- **Preprocessor macros** — conditionally compile test access.
- **Aspects** — weave in observation without editing the component.

### Limit complexity

- **Limit structural complexity** — the coupling and cohesion work, done for testability's sake.
- **Limit nondeterminism** — remove sources of run-to-run variation, without which a failing test is
  not a usable signal.

Related patterns: dependency injection, strategy, intercepting filter.

---

## Usability

Goal: let the user accomplish the task, and support them while they do.

### Support user initiative

- **Cancel** — abandon a command already issued.
- **Undo** — reverse a command's effects.
- **Pause/resume** — suspend a long task, do something else, return to it.
- **Aggregate** — apply one operation across a set rather than item by item.

### Support system initiative

- **Maintain task model** — know what the user is trying to do, to anticipate and assist.
- **Maintain user model** — know this user, including for customization.
- **Maintain system model** — know the system's own expected behavior, so it can tell the user what
  to expect (progress and completion estimates).

Related patterns: model-view-controller, observer, memento.

---

## Super-tactics

Tactics so fundamental and pervasive that they appear in the realization of almost every pattern and
serve several attributes at once. Do not expect a tactic to live in only one attribute's list.

- **Encapsulate**, **restrict dependencies**, **use an intermediary**, **abstract common services** —
  nominally modifiability tactics, present almost everywhere.
- **Scheduling** — appears across performance, energy efficiency and availability. A load balancer is
  an intermediary that does scheduling.
- **Monitoring** — serves energy efficiency, performance, availability and safety.

Identify these first: where one mechanism serves several target attributes it is a cheap win. But
credit it only once — booking the same mechanism as an independent success in each attribute's
analysis overstates the design.
