# Designing probes and monitors for a system you do not own

Read at steps 5-8. Contents: [passive versus active](#passive-versus-active) ·
[the monitor as a small machine](#the-monitor-as-a-small-machine) · [the four assertions](#the-four-assertions) ·
[probe priority](#probe-priority) · [cost and pollution](#cost-and-pollution) ·
[interposition](#interposition-measuring-without-cooperation) · [residence time](#residence-time) ·
[what to alert on](#what-to-alert-on)

## Passive versus active

**Passive** monitoring watches real traffic. Free, representative, and blind when traffic is low —
which is exactly when a quiet failure goes unnoticed.

**Active** monitoring injects a synthetic request and checks the result. It is the **only** way to
detect a dependency that is up but producing garbage, and the only option for a component never
built to be observed.

You want both. Passive tells you what your users are experiencing; active tells you whether the
dependency is correct when nobody is looking.

## The monitor as a small machine

A usable monitor for a third-party service is not a ping. It runs **two independent timers**:

- a **timeout timer**, armed on each request and cancelled on reply — measured in seconds;
- a **send interval** between probes — measured in tens of seconds to about a minute.

They are independent on purpose. Coupling them means a slow reply delays the next probe, and your
sampling rate silently drops exactly when you most want data.

On expiry of the timeout, emit a timeout status and start the next send interval rather than
waiting for a reply that may never come.

Use **one fixed synthetic subject** — a known test identifier whose correct answer does not change
— so results are comparable across runs. A probe whose expected answer drifts cannot distinguish a
vendor fault from a data change.

## The four assertions

On each reply, assert in this order. Order matters because it determines what the alert says.

1. **The correlation identifier matches the request just sent.** Assert this first: a mismatched
   reply is a different and far more alarming defect than a slow one — it means replies are being
   crossed, and any conclusion drawn from the payload is unsafe.
2. **The body deserialises to the expected type.** Catches content-type changes and infrastructure
   error pages returned with a success status.
3. **The field values fall in a plausible documented range.** Catches a service that is answering
   but computing nonsense.
4. **The result matches the known-correct answer** for the fixed synthetic subject. This is the
   only assertion that detects a silently degraded dependency returning stale or wrong data.

Most monitoring stops after a liveness check, which is assertion zero. Assertions 3 and 4 are what
make the monitor worth building.

## Probe priority

**Send probes at raised priority, or you will be measuring your own backlog.**

If the probe queues behind your application traffic, a perfectly healthy vendor reads as
unavailable, because the time you record is your own queue depth rather than their latency. During
an incident this is actively harmful: it points the investigation at the vendor when the problem is
yours.

This is safe **only because probe volume is tiny**. The same trick applied to real volumes of
high-priority traffic would starve application messages and cause the outage it was meant to detect.
Keep probe volume negligible and say so where the priority is configured, so nobody later "fixes"
the inconsistency by raising the priority of something else.

## Cost and pollution

Two costs nobody budgets for:

**Billing.** The vendor may bill per call, which makes probe frequency a literal line item.
Establish before probing whether probe calls are excluded, and if not, price the cadence. A
one-minute interval is over forty thousand calls a month.

**State pollution.** A stateful vendor generally cannot distinguish your test data from real data.
Probing a system that creates records leaves those records there — in their reports, their
reconciliations, and potentially their downstream feeds to other parties.

Mitigations, in order of preference:

1. **Agree a test subject with the vendor**, ideally one they exclude from reporting.
2. **Use a read-only probe** where one exists that still exercises the interesting path.
3. **Tag test traffic with a dedicated field the vendor echoes** — never with a magic value in a
   business field. Magic values in business fields are eventually processed as real data by
   somebody, and the failure is embarrassing and hard to trace.
4. Where the service supports a caller-specified reply address, use **a distinct test reply
   channel** as the tag. This needs no message change at all, which makes it the cleanest option
   when available.

## Interposition: measuring without cooperation

To measure a request-reply service that will not instrument itself, interpose a proxy that swaps
the return address:

1. Store the caller's reply address and correlation identifier.
2. Replace both with your own and forward the request.
3. On the reply, restore both, take the measurement, and forward the message **untouched**.

This is the only approach available when replies go to a caller-specified address, because there is
no fixed output channel to tap.

Persist the request-side record — you need it to pair with the reply anyway — and **compute elapsed
time from when the request was forwarded**, not from when a copy reached your recorder, or the
measurement is skewed by your own queueing.

To detect a component that consumes messages and loses them, race the real path against a bypass:
duplicate each inbound message onto a reliable bypass channel, send the original through the
suspect chain, and reconcile on a correlation identifier with a timeout. Bypass copy arrives,
processed copy does not, timeout fires: you have identified swallowed work from outside, without
modifying the system you distrust. Note that a delivery guarantee does not protect you here — the
message *was* delivered before it was lost.

## Residence time

A request's total time at a service is **queue time plus processing time**, and any latency
commitment applies to the whole of it.

Measuring only your own processing time is the specific error that lets a service believe all is
well while its consumers complain it is slow. The asymmetry is structural rather than incidental:
the queue is serial while processing is concurrent, so under load queueing time ultimately
dominates.

When a vendor quotes latency, establish **which one they are quoting**. Then measure the other one
yourself, at your edge, because that is the number your users experience.

## What to alert on

Alert on the assertion that failed, not on "the probe failed" — the distinction is what makes the
page actionable at three in the morning:

| Failing assertion | What it means | Urgency |
|---|---|---|
| Correlation mismatch | Replies are crossed | Highest — data may be wrong right now |
| Timeout | Unavailable or very slow | High |
| Deserialisation | Contract changed, or an infrastructure error page | High |
| Range | Answering, computing nonsense | High, and easily missed |
| Known-answer mismatch | Silently degraded — stale or wrong data | Highest |

Trend the probe latency separately from the alerts. A steadily rising probe time is the clearest
early warning of a vendor in trouble, and it usually precedes any threshold breach by days.
