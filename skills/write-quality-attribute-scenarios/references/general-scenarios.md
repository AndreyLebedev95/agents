# General scenario parameter tables

A **general scenario** is system-independent: it lists, for each of the six parts, the values that
part can plausibly take for that attribute. A **concrete scenario** is the result of substituting
system-specific values. Hand a stakeholder the general scenario and let them tailor it.

## Contents

- [Availability](#availability) · [percentage-to-downtime table](#availability-targets-in-real-time)
- [Deployability](#deployability)
- [Energy efficiency](#energy-efficiency)
- [Integrability](#integrability)
- [Modifiability](#modifiability)
- [Performance](#performance)
- [Safety](#safety)
- [Security](#security)
- [Testability](#testability)
- [Usability](#usability)

---

## Availability

| Part | What it is | Candidate values |
|---|---|---|
| Source | Where the fault comes from | Internal or external: people, hardware, software, physical infrastructure, physical environment |
| Stimulus | A fault | Omission, crash, incorrect timing, incorrect response |
| Artifact | Which parts are responsible for and affected by the fault | Processors, communication channels, storage, processes, affected artifacts in the environment |
| Environment | Not just "normal" — also states already recovering | Normal operation, startup, shutdown, repair mode, degraded operation, overloaded operation |
| Response | Usually prevent the fault becoming a failure; others matter too | Prevent fault becoming failure; detect the fault (log it, notify appropriate entities); recover from it; disable the source of the events causing it; be temporarily unavailable while repair happens; fix or mask the fault, or contain the damage; operate in a degraded mode during repair |
| Response measure | Depends on how critical the service is | Time or time interval the system must be available; availability percentage; time to detect the fault; time to repair the fault; time interval in which the system may run degraded; proportion (e.g. 99%) or rate (e.g. up to 100/sec) of a class of faults the system prevents or handles without failing |

### Availability targets in real time

Only *unscheduled* outages count toward downtime. "High availability" conventionally means 99.999%
or better.

| Availability | Downtime / 90 days | Downtime / year |
|---|---|---|
| 99.0% | 21 hr 36 min | 3 days 15.6 hr |
| 99.9% | 2 hr 10 min | 8 hr 0 min 46 sec |
| 99.99% | 12 min 58 sec | 52 min 34 sec |
| 99.999% | 1 min 18 sec | 5 min 15 sec |
| 99.9999% | 8 sec | 32 sec |

Steady-state availability is `MTBF / (MTBF + MTTR)`. Read it as three questions: what will make this
system fail, how likely is that, and how long will repair take?

Categorize a detected fault on two axes before choosing a repair strategy: **severity** (critical,
major, minor) and **service impact** (service-affecting, non-service-affecting). Without this, every
fault gets the same escalation. Track the remaining capability after failure — the degraded operating
mode — as a requirement in its own right.

---

## Deployability

| Part | What it is | Candidate values |
|---|---|---|
| Source | The trigger for the deployment | End user, developer, system administrator, operations personnel, component marketplace, product owner |
| Stimulus | What causes the trigger | A new element is available to deploy — typically a request to replace an element with a new version (fix a defect, apply a security patch, upgrade a component or framework, upgrade an internally produced element); a new element is approved for incorporation; an existing element or set of elements must be rolled back |
| Artifact | What is to be changed | Specific components or modules, the platform, the user interface, the environment, or another system it interoperates with — so one element, several, or the entire system |
| Environment | Staging, production, or a specified subset of either | Full deployment; subset deployment to a specified portion of users, VMs, containers, servers or platforms |
| Response | What should happen | Incorporate the new components; deploy them; monitor them; roll back a previous deployment |
| Response measure | Cost, time, or process effectiveness for one deployment or a series | Cost as: number, size and complexity of affected artifacts; average or worst-case effort; elapsed clock or calendar time; money (direct outlay or opportunity cost); new defects introduced. Extent to which the deployment or rollback affects other functions or attributes. Number of failed deployments. Repeatability, traceability and cycle time of the process |

Deployment is the process from coding to real users interacting with the system in production. If it
is fully automated with *no human intervention*, it is continuous deployment — a pipeline with a
manual approval gate is not, and its response measure must include the human wait time.

Check before treating deployability as a driver at all: in a complex ecosystem with many
dependencies it may be impossible to release one part without coordinating the others, and embedded
systems, systems in hard-to-reach locations and non-networked systems are poor candidates.

---

## Energy efficiency

| Part | What it is | Candidate values |
|---|---|---|
| Source | Who or what requests energy conservation | End user, manager, system administrator, automated agent |
| Stimulus | A request to conserve energy | Total usage, maximum instantaneous usage, average usage |
| Artifact | What is to be managed | Specific devices, servers, VMs, clusters |
| Environment | Usually runtime, with special cases | Runtime, connected, battery-powered, low-battery mode, power-conservation mode |
| Response | What the system does to conserve or manage energy | Disable services; deallocate runtime services; change allocation of services to servers; run services at a lower consumption mode; allocate or deallocate servers; change levels of service; change scheduling |
| Response measure | Energy saved or consumed, and the effect on everything else | Maximum or average kilowatt load; average or total energy saved; total kilowatt hours used; time period the system must stay powered — **while still maintaining a required level of functionality and acceptable levels of other quality attributes** |

That final clause is part of the requirement, not a footnote. Every response in the list degrades
something else, so a measure without a functionality floor is trivially satisfiable.

---

## Integrability

| Part | What it is | Candidate values |
|---|---|---|
| Source | Where the stimulus comes from | Mission or system stakeholder; component marketplace; component vendor |
| Stimulus | What kind of integration | Add a new component; integrate a new version of an existing component; integrate existing components together in a new way |
| Artifact | What parts are involved | Entire system; a specific set of components; component metadata; component configuration |
| Environment | What state the system is in | Development; integration; deployment; runtime |
| Response | How an integrable system responds | Changes are completed, integrated, tested, deployed; components in the new configuration exchange information successfully and correctly, both syntactically and semantically; components collaborate successfully; components do not violate resource limits |
| Response measure | How it is measured | Cost as: number of components changed; percentage of code changed; lines of code changed; effort; money; calendar time. Plus **effects on other attributes' response measures, to capture allowable tradeoffs** |

Integration difficulty is a function of **size** (the number of potential dependencies) and
**distance** (the difficulty of resolving differences at each one). Distance comes in five kinds, and
only the first is catchable by tooling: syntactic, data-semantic, behavioral-semantic, temporal, and
resource. See `select-quality-attribute-tactics` for the full breakdown.

---

## Modifiability

| Part | What it is | Candidate values |
|---|---|---|
| Source | The agent causing the change — usually human, but the system may learn or self-modify, in which case the source is the system | End user, developer, system administrator, product line owner, the system itself |
| Stimulus | The change to accommodate (fixing a defect counts as a change) | A directive to add, delete or modify functionality, or to change a quality attribute, capacity, platform or technology; to add a new product to a product line; to change the location of a service |
| Artifact | What is modified | Code, data, interfaces, components, resources, test cases, configurations, documentation |
| Environment | The time or stage at which the change is made | Runtime, compile time, build time, initiation time, design time |
| Response | Make the change and incorporate it | Make the modification; test it; deploy it; self-modify |
| Response measure | Resources expended to make the change | Cost as: number, size and complexity of affected artifacts; effort; elapsed time; money (direct outlay or opportunity cost); extent to which the modification affects other functions or attributes; new defects introduced; how long the system took to adapt |

---

## Performance

| Part | What it is | Candidate values |
|---|---|---|
| Source | One or more users, an external system, or part of the system itself | External: user request; request from an external system; data arriving from a sensor or other system. Internal: one component requesting another; a timer generating a notification |
| Stimulus | Arrival of an event — a request for service or a state notification | **Periodic** (arrives at a predictable interval); **stochastic** (arrives per some probability distribution); **sporadic** (a pattern that is neither) |
| Artifact | The whole system or part of it | Whole system; a component within the system |
| Environment | The state when the stimulus arrives; unusual modes change the response | Normal mode; emergency mode; error-correction mode; peak load; overload mode; degraded operation mode; another defined mode |
| Response | The system processes the stimulus, which takes time — for computation, or because processing is blocked contending for shared resources. Requests can fail from overload or a failure anywhere in the chain | Returns a response; returns an error; generates no response; ignores the request when overloaded; changes the mode or level of service; services a higher-priority event; consumes resources |
| Response measure | Timing and capacity | **Latency** — maximum, minimum, mean or median time the response takes; **throughput** — number or percentage of satisfied requests over an interval or set of events; number or percentage of requests that go unsatisfied; **jitter** — variation in response time; usage level of a computing resource |

Order-of-magnitude anchors: computation in thousands of nanoseconds; disk access (solid state or
rotating) in tens of milliseconds; network access from hundreds of microseconds within a data centre
to upward of 100 ms intercontinental.

Systems with timing deadlines should measure jitter and deadline-miss rate, not just mean latency.

---

## Safety

| Part | What it is | Candidate values |
|---|---|---|
| Source | A data source, a time source, or a user action | A specific sensor; software component; communication channel; device such as a clock |
| Stimulus | An omission, a commission, or incorrect data or timing | **Omission**: a value never arrives; a function is never performed. **Commission**: a function is performed incorrectly; a device produces a spurious event or incorrect data. **Incorrect data**: a sensor reports incorrect data; a component produces incorrect results. **Timing failure**: data arrives too late or too early; an event occurs too late, too early or at the wrong rate; events occur in the wrong order |
| Environment | System operating mode | Normal operation; degraded operation; manual operation; recovery mode |
| Artifact | Part of the system | Safety-critical portions of the system |
| Response | The system stays in, or returns to, a safe state space, or continues degraded to prevent further injury or damage; users are advised; the event is logged | Recognize the unsafe state, then: avoid it; recover; continue in degraded or safe mode; shut down; switch to manual operation; switch to a backup system; notify appropriate entities; log the unsafe state and the response |
| Response measure | Time to return to a safe state; damage or injury caused | Amount or percentage of entries into unsafe states avoided; amount or percentage of unsafe states the system can recover from automatically; **change in risk exposure: size(loss) × prob(loss)**; percentage of time the system can recover; time spent in degraded or safe mode; amount or percentage of time shut down; elapsed time to enter and recover from manual operation or a safe or degraded mode |

Enumerating all four stimulus classes is what stops a hazard analysis from covering only the obvious
case.

---

## Security

| Part | What it is | Candidate values |
|---|---|---|
| Source | The attack may come from outside or inside the organization, from a human or another system, and may be previously identified (correctly or not) or unknown | Human; another system — inside the organization; outside it; previously identified; unknown |
| Stimulus | An attack | An unauthorized attempt to: display data; capture data; change or delete data; access system services; change the system's behavior; reduce availability |
| Artifact | The target of the attack | System services; data within the system; a component or resources; data produced or consumed by the system |
| Environment | The state of the system when the attack occurs | Online or offline; connected to or disconnected from a network; behind a firewall or open to a network; fully operational; partially operational; not operational |
| Response | Confidentiality, integrity and availability are maintained | Data or services protected from unauthorized access; not manipulated without authorization; parties to a transaction identified with assurance; parties cannot repudiate their involvement; data, resources and services available for legitimate use. And the system tracks activity: recording access or modification; recording *attempts* to access data, resources or services; notifying appropriate entities when an apparent attack is under way |
| Response measure | Frequency of successful attacks, time and cost to resist and repair, consequential damage | How much of a resource is compromised or ensured; accuracy of attack detection; time elapsed before an attack was detected; how many attacks were resisted; time to recover from a successful attack; how much data is vulnerable to a particular attack |

Security rests on three properties: **confidentiality** (data and services protected from
unauthorized access), **integrity** (not subject to unauthorized manipulation), **availability**
(available for legitimate use). Note availability appears here *and* as its own attribute — the same
event is legitimately both, which is exactly why arguing about categories is pointless.

To generate the stimuli, build an attack tree: the root is a successful attack, nodes are possible
direct causes, children decompose those further. The leaves are your stimuli.

A complete response covers more than prevention — assurance of identity, non-repudiation, and
activity tracking are all part of it.

---

## Testability

| Part | What it is | Candidate values |
|---|---|---|
| Source | A human or an automated test tool | Unit testers; integration testers; system testers; acceptance testers; end users — running tests manually or with automated tooling |
| Stimulus | A test or set of tests is initiated | Tests serve to: validate system functions; validate qualities; discover emerging threats to quality |
| Environment | Testing happens at various events or lifecycle milestones | Completion of a coding increment such as a class, layer or service; completed integration of a subsystem; complete implementation of the whole system; deployment into production; delivery to a customer; a testing schedule |
| Artifact | The portion under test, and any required test infrastructure | A unit of code corresponding to a module; components; services; subsystems; the entire system; the test infrastructure |
| Response | The system and its test infrastructure can be controlled to perform the tests, and results can be observed | Execute the test suite and capture results; capture the activity that produced the fault; control and monitor the state of the system |
| Response measure | How easily the system under test gives up its faults | Effort to find a fault or class of faults; effort to achieve a given percentage of state-space coverage; probability of a fault being revealed by the next test; time to perform tests; effort to detect faults; length of time to prepare test infrastructure; effort to bring the system into a specific state; **reduction in risk exposure: size(loss) × prob(loss)** |

Testability is the probability that, given at least one fault, the system fails on its next test
execution. Achieving it requires both **control** of a component's inputs and possibly its internal
state, and **observation** of its outputs and possibly its internal state.

The test harness is software in its own right, with its own architecture, stakeholders and quality
requirements — so "length of time to prepare test infrastructure" is a legitimate measure and the
harness is in scope for analysis.

---

## Usability

| Part | What it is | Candidate values |
|---|---|---|
| Source | Where the stimulus comes from | The end user, who may be in a specialized role such as system or network administrator. An external event arriving at the system, which the user may react to, can also be a source |
| Stimulus | What the end user wants | To use the system efficiently; learn to use it; minimize the impact of errors; adapt it; configure it |
| Environment | When the stimulus reaches the system | The user actions usability concerns always occur at runtime or at system configuration time |
| Artifact | What part is being stimulated | A GUI; a command-line interface; a voice interface; a touch screen |
| Response | How the system should respond | Provide the user with the features needed; anticipate the user's needs; provide appropriate feedback |
| Response measure | How it is measured | Task time; number of errors; learning time; ratio of learning time to task time; number of tasks accomplished; user satisfaction; gain of user knowledge; ratio of successful operations to total operations; amount of time or data lost when an error occurs |

Five areas, each with its own elicitation question: learning system features (what makes learning
easier?); using the system efficiently (what makes the user more efficient — suspend a task, do
other operations, resume?); minimizing the impact of user errors (cancel a command, undo its
effects?); adapting the system to user needs (can the user, or the system, adapt — autofill from past
entries?); increasing confidence and satisfaction (what signals the correct action is being taken —
feedback during a long-running task?).

Worth knowing when arguing for the work: attention to usability is one of the cheapest ways to
improve a system's quality — or more precisely, the user's *perception* of quality.
