---
name: probe-vendor-contract-empirically
description: Establishes empirically what a third-party or purchased system actually does, as opposed to what its documentation claims, and records the difference. Covers writing your own generative and contract tests against services you consume rather than trusting the provider's, why a mock that conforms to the interface proves nothing and a harness must be able to misbehave, the thirteen out-of-spec behaviours it must inflict, instrumenting a service that will not instrument itself, why only a test message proves correctness where a heartbeat proves liveness, that hung is not crashed so every internal monitor reports healthy, and measuring residence time rather than the provider's own latency number. Use when documentation and observed behaviour disagree, before trusting a guarantee that matters, when setting up contract tests or a test harness against a bought core, when monitoring a vendor that will not instrument itself, when planning chaos or failure-injection work, or when the vendor is "up" but the integration is failing — even when the ask is only "how do we know their API really does that". For writing the reference use document-vendor-api-surface; for an announced version change use assess-vendor-version-change; for what the core cannot do at all use report-vendor-capability-gaps.
---

# Finding out what the vendor actually does

Documentation is a claim about behaviour. This skill is about converting claims into observations,
and recording where the two differ.

The governing fact: **once a service is live, its implementation is the specification** — including
behaviour nobody intended. A field that was never validated, merely received and stored, is now
part of the contract, and adding the validation the documentation always described is a breaking
change. So the thing to test is behaviour, and the thing to write down is behaviour.

## Where to spend the effort

You cannot test everything. Probe in this order:

1. **Guarantees you are about to build on.** Anything the design assumes and the vendor has not
   contracted in writing.
2. **Anything marked "observed" or "unknown"** in the API reference.
3. **Failure paths**, which are never exercised by ordinary use and are exactly where integrations
   break.
4. **Anything the vendor's own documentation hedges** — "typically", "should", "in most cases".

## The seven questions

Run these against every external call, every I/O, every resource use. Their power is separating
connection failure from response failure, and — crucially — separating outright failure from
*slowness*, the two cases most integration designs collapse into one:

1. What if it cannot make the initial connection?
2. What if it takes ten minutes to make the connection?
3. What if it connects and then gets disconnected?
4. What if it connects but no response ever comes?
5. What if it takes two minutes to respond?
6. What if ten thousand requests arrive at once?
7. What if a downstream resource it needs is unavailable?

Any question you cannot answer from observation is a probe to design.

## Procedure

### 1. Write your own contract tests — never use the provider's

Take the vendor's published specification and write **one test per case it claims to support**.
Then add randomised and generative inputs at the *boundaries* of the specification, not just the
happy examples.

Two properties make this work, and both are lost if the provider writes the tests:

- You are testing whether **your understanding** of the specification is correct, which is the
  thing that actually breaks. A provider's tests encode the provider's understanding.
- The gaps between documented and actual behaviour are found by inputs the provider did not think
  of, and the provider is definitionally the party who did not think of them.

Run the suite against the vendor's staging environment **on a schedule**, not once. A contract test
run once is a snapshot; run continuously it is a change detector, and it will catch the
undeclared changes that `assess-vendor-version-change` otherwise has to discover by incident.

Expect a high first-run failure rate. That is the point, and it is normal for most cases to fail
initially. Treat every first-run failure as **either a specification defect or a misunderstanding**
and resolve which — the resolution is the deliverable, not the pass.

### 2. Do not test against a mock

A mock can only be trained to produce behaviour that **conforms to the interface**. That makes it
useless for the failures that matter, because the failures that matter do not conform to anything.

A **test harness** runs as a separate server and is therefore not obliged to conform to any
interface at all: it can produce network errors, protocol violations and application-level nonsense
that no interface admits. A conventional integration environment has the same limitation as a
mock — it can only exercise in-spec behaviour, because the real system on the other end is trying
to be correct.

If every test of your integration passes against something that is trying to behave, you have
tested nothing about the boundary.

Work through the thirteen misbehaviours in `references/harness-misbehaviours.md`. The three
most commonly untested are: accepting the connection and never sending a byte; responding far
slower than any timeout; and delivering a stale response belonging to an earlier request — the last
being the one that produces *wrong answers* rather than errors.

### 3. Beware the test that asserts on its own inputs

The common failing in integration tests is overspecification: set up a request, issue it, then
assert about the response **using data from the original request**.

That verifies how the end-to-end loop happens to work right now. It does not verify that your side
conforms to the contract, nor that your side can handle **any response the vendor is allowed to
send**. A vendor release that changes the response in a permitted way will pass this test and break
production.

Assert against the contract, not against the round trip.

### 4. Stress both sides, with a pass/fail rubric decided first

As the consumer, test what happens when calls stop responding or become very slow. A harness that
mimics a back end **wilting under load** — rather than being absent — lets you verify graceful
degradation without a scale replica of anything.

Set the rubric in advance, so the result is a verdict rather than a discussion:

- **Pass:** slowdown, then fail-fast, then recovery once the far side returns.
- **Fail:** crash, hang, data loss, or failure to recover after the far side comes back.

Run caller and provider at **several different ratios**, not the one-to-one pairing a test
environment defaults to — capacity imbalance is invisible at one-to-one and is where production
lives. Take the maximum number of calls the caller could possibly make, double it, and aim it all
at the most expensive transaction.

### 5. Instrument what the vendor will not

You can measure a third-party request-reply service without its cooperation by **interposing a
proxy**: it records the caller's reply address and correlation identifier, substitutes its own,
forwards the request, and on the reply performs the measurement and passes the untouched message
onward.

This interposition is the only option when replies go to a caller-specified address, because
there is no fixed output channel to watch. Compute elapsed time from **when the request was
forwarded**, not from when a copy arrived at your recorder, or the measurement includes your own
queueing.

For a component you suspect of *consuming* messages and losing them, race the real path against a
bypass: duplicate each inbound message onto a reliable bypass channel, send the original through
the suspect chain, and reconcile the two on a correlation identifier with a timeout. If the bypass
copy arrives and the processed one does not, you have identified swallowed work — from outside,
without modifying the system you distrust.

### 6. Separate liveness from correctness

**A heartbeat, a status endpoint or a process check tells you a component is running and almost
nothing about whether it still processes work correctly.** That is exactly the shape of a silently
degraded dependency: up, responding, and returning stale or wrong results.

Only a **test message** — a real request through the normal path, with the result checked — proves
correctness.

And remember **hung is not crashed**: a stalled integration reports healthy on every internal
monitor, because the process is alive and the thread that would notice is the one that is stuck.

If you own the health route, make it report **identity and dependency state**, not just liveness:
application version, runtime version, host address, and the status of connection pools, caches and
circuit breakers. That turns it into a debugging artifact rather than a boolean. Start availability
false and flip it only when dependencies are actually ready, and drain by flipping the flag rather
than by removing the instance.

### 7. Design the probe properly

A usable monitor for a third-party service is a small specific machine, not a ping. Read
`references/probe-and-monitor-design.md`. In brief: two independent timers — a short timeout armed
on each request, and a longer interval between probes — and, on each reply, four assertions in
order: the correlation identifier matches the request just sent; the body deserialises to the
expected type; the field values fall in a plausible range; and the result matches the known-correct
answer for a fixed synthetic subject.

Assert correlation **first**, because a mismatched reply is a different and more alarming defect
than a slow one.

Two constraints people discover late:

**Send probes at raised priority.** If the probe queues behind your own application traffic, a
healthy vendor reads as unavailable — the timeout you record is your backlog, not their latency.
This is only safe because probe volume is tiny; the same trick at real volume would starve
application traffic.

**Synthetic probes cost money and pollute state.** The vendor may bill per call, making probe
frequency a line item. And a stateful vendor generally cannot distinguish your test data from real
data, so probing a system that creates records leaves them there. Establish both before probing,
and tag test traffic with a dedicated field the vendor echoes — never with a magic value in a
business field, which will eventually be processed as real.

### 8. Measure residence time, not processing time

A request's total time at a service is queue time plus processing time, and any commitment applies
to the whole of it. Measuring only processing time is why a service can believe all is well while
its consumers complain.

The asymmetry is structural: the queue is serial while processing is concurrent, so under load
queueing dominates. When a vendor quotes a latency number, **establish which one they are
measuring** — and measure the other one yourself, at your edge.

### 9. Where the stakes justify it, inject failures deliberately

Not every integration warrants this. Where one does, read `references/failure-injection.md`.

Four prerequisites must hold before injecting anything: the experiment cannot cause unrecoverable
business loss; the blast radius is bounded and victim selection is defined; end-to-end tracing
gives a success verdict per request; and the steady-state measurement can actually detect the
change you care about.

State the hypothesis as an **externally observable invariant**, and fix the **rejection criterion
in advance**. Deciding afterwards whether the result was acceptable is how an experiment becomes an
anecdote.

The reason to do this at all: a system that has not failed recently is not therefore safe. Constant
pressure toward efficiency, combined with nobody working at maximum sustainable effort, pushes a
system steadily toward its safety boundary — and the boundary is invisible until crossed. Rarely
exercised failure paths are exactly the ones that have quietly stopped working.

### 10. Record the difference

Every probed claim becomes a row: **documented value, observed value, verdict, date, method.**

The date matters more than it looks. An observation is a fact about one moment, and the vendor may
change behaviour without telling you. An undated observed-behaviour register slowly becomes a
second set of claims.

## Output format

```
# <System> observed-behaviour register

## Method
<what was probed, against which environment, over what period, with what credential>

## Findings
| # | Claim | Source | Documented | Observed | Verdict | Date | Method |
<verdict: confirmed / contradicted / unverifiable / undocumented-behaviour-found>

## Contradictions
<where documentation and behaviour disagree — the highest-value rows, listed
 separately because they are what someone has to act on>

## Undocumented behaviour we now depend on
<things that work but are not promised; feeds the API reference as "observed">

## Untestable claims
<what could not be established, why, and what we are assuming instead>

## Standing monitors
<probes now running, their cadence, cost, and what each would catch>
```

The **Untestable claims** section is not an admission of failure. It is the list of assumptions the
project is carrying, and making it explicit is most of this artifact's value.

## Failure modes

| Tell | What is actually happening | Fix |
|---|---|---|
| Integration "tested" only against a mock | A mock can only conform; failures do not conform | Replace with a misbehaving harness |
| Contract tests pass, production breaks | Tests assert on their own inputs | Assert against the contract, not the round trip |
| Vendor dashboard green, integration failing | Hung is not crashed | Test message, not heartbeat |
| Latency looks fine, users report slowness | Processing time measured, not residence time | Measure at your edge |
| Probe latency tracks your own load | Probes queued behind application traffic | Raise probe priority |
| Probe results are green and meaningless | Only liveness asserted | Add the four assertions on a fixed synthetic subject |
| Test records appearing in vendor reports | Probe polluted a stateful system | Tag test traffic; agree a test subject with the vendor |
| Monitoring bill rose unexpectedly | Vendor bills per call, probes included | Establish billing before setting cadence |
| No visibility into vendor call volume | The vendor will not instrument itself | Interpose and measure |
| Failure assumptions never validated | Failure paths never exercised | Designed experiment with a fixed rejection criterion |
| Messages disappear with no error | A component consumes then dies, non-transactionally | Race the real path against a reliable bypass |

## Related work

- Where these findings are written down as contract → `document-vendor-api-surface`
- Running this suite continuously to catch undeclared change → `assess-vendor-version-change`
- Turning "cannot be established" into a stated limit → `report-vendor-capability-gaps`
- Making the gateway stub reproduce what you observed → `design-vendor-anticorruption-layer`
- Verifying claimed delivery guarantees specifically → `pin-down-vendor-event-delivery`
