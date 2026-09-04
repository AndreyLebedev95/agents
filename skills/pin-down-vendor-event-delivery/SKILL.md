---
name: pin-down-vendor-event-delivery
description: Turns a vendor's webhook, queue, topic or change-feed offer into a stated delivery contract — ordering, duplication, replay window, dedup key, correlation, failure channel — and specifies the receiver-side compensation each missing guarantee forces on you. Covers why a delivery guarantee says nothing about ordering or timing, why scaling consumers is what destroys ordering, the floor and ceiling on any replay window and how both end replay silently, why a durable subscription is a shared name rather than an identity, the two routes to idempotence and what each costs, the difference between a message id, a correlation id and a sequence number, deduplication windows measured in minutes, and the failure channels a callback API leaves you no way to report into. Use when a vendor offers webhooks or a queue or a change feed, when designing a consumer for a vendor event stream, when duplicate or out-of-order events appear, when asking whether events can be replayed or backfilled, or when deciding between polling and subscribing — even when the ask is only "they'll send us events, is that fine". For bulk or historical extraction use plan-vendor-data-extraction; for the request/response surface use document-vendor-api-surface; for the translation layer use design-vendor-anticorruption-layer.
---

# Pinning down a vendor's event delivery

"We'll send you webhooks" is not a contract. It is an offer to send you something, sometimes, in
some order, possibly more than once, with no stated way to get back what you missed.

Your job is to convert it into a table where every guarantee is either **stated by the vendor**,
**observed but unpromised**, or **absent** — and where every absent guarantee has a named
compensation on your side. An absent guarantee with no compensation is a defect you have agreed to
ship.

## The eight questions

Everything below hangs off these. If you take nothing else, take these:

1. Does an event mean it *happened*, or that it *probably happened*?
2. In what scope, if any, is order preserved?
3. Can the same event arrive twice, and how would we know?
4. If we are down for an hour, what happens to events published meanwhile?
5. How far back can we replay, expressed as two numbers, not as the word "durable"?
6. What key do we deduplicate on, and who mints it?
7. Where does a message go when our handler fails?
8. How do we get the events that predate the subscription, or that fell outside the replay window?

Question 8 is the one most often discovered late, and it is usually answered by a bulk extract
rather than by the event stream at all — see `plan-vendor-data-extraction`.

## Procedure

### 1. Split "guaranteed delivery" into two questions

A delivery guarantee says the message eventually arrives. It says nothing about *when*, and
therefore nothing about **order** relative to other messages. Messages sent in sequence can and do
arrive out of sequence.

Record arrival and ordering as separate rows. Treat ordering as unspecified unless the vendor names
the scope it holds in ("per aggregate", "per partition key", "per tenant").

Also establish what the guarantee excludes. Reliability is counted in nines and each extra nine
costs exponentially more, so ask: for how long do they retry, where is the message buffered
meanwhile, and what happens when that buffer fills? During a long outage a producer buffers to its
own local disk — which was never sized for it — so a high-rate producer can exhaust the disk in
hours. That is why systems expose a retry timeout that silently bounds how long messages are held,
sometimes to minutes.

### 2. Establish the ordering scope, and remember it is yours to lose

Order survives exactly **one consumer instance**. Run instances in parallel and messages come out
of order — and nothing reports it, because each individual message was processed correctly.

The mechanism is worth internalising because it makes the trade-off concrete: throughput is capped
by the slowest stage, the fix is to run several competing consumers on that stage, and competing
consumers process out of order. There are only two remedies — run exactly one instance, or add a
resequencing stage.

Worse, the one stage you most want to parallelise on a vendor feed is **deduplication**, and it is
the one that cannot be, because deduplication requires shared state across the instances that would
be doing the parallel work.

Note also that the concurrency semantics of multiple consumers on one channel are frequently left
undefined by the specification the vendor implements, so the behaviour is per-provider and does not
port between environments. Ordering is never an inherited property; it is designed for or lost.

### 3. Get the replay window as two numbers

A subscriber is not simply connected or disconnected. There is a third state — **inactive**:
disconnected but still subscribed — and it is what makes a broker retain messages published during
the gap. Without it, missing messages requires nothing more dramatic than being briefly down.

Establish, in order:

1. Does the subscription survive your downtime at all?
2. What happens to an event published while a subscription is being established? (This race is
   resolved implementation-specifically, and a receiver that subscribes an instant after a publish
   simply never gets that message.)
3. **The retention duration and the per-subscription message cap.** Both. Either one ends replay
   silently — retention ends it by time, the cap ends it by volume, and neither raises an error.

An honest replay guarantee is a pair of numbers. The word "durable" is not an answer. Compute your
maximum tolerable downtime from those two numbers and check it against your actual recovery times.

**A durable subscription is a shared name, not an identity.** It is keyed by something like topic
plus client id plus subscription name, and the code to *create* one is identical to the code to
*resume* one — only the broker knows which happened. So a different application reusing those
values inherits your backlog and receives everything you missed, with no error on either side. A
copied config file, a cloned deployment, or a second environment pointed at production is enough.
Give every consumer a distinct subscription identity and treat the name as a credential.

### 4. Pin the deduplication story

Read `references/idempotence-and-dedup.md`. The parts that most often go unasked:

**The window is minutes, not forever.** A typical deduplication retention is around five minutes,
with the timer reset on each hit. Present the same key after the window lapses and there is no
cached entry — so the vendor executes the request again as new. No error, no warning, a clean
success, and a second payment. This is the exact gap that turns a safe retry into a duplicate
charge, and it is why a retry queue that can hold work longer than the dedup window is a defect.

**The response to a deduplicated retry is frozen.** It is the cached response from the first
execution, deliberately not refreshed as the underlying data changes. So it describes the state at
the moment of the original call, and another party may have changed the record several times since.
Never write a retry response into your system as current state.

**Content-derived deduplication is dangerous.** Deduplication must key off a client-chosen request
identifier, never a hash of the body — the same payload can legitimately be meant twice (two
identical charges, two identical adjustments on the same day). A vendor that deduplicates by
content drops your second legitimate transaction and returns success, and the only escape is
perturbing the payload with a meaningless difference.

### 5. Classify every operation for idempotence before allowing any retry

Three buckets, documented separately:

- **Inherently idempotent** — a notification, a quote request, a read. Replay freely.
- **Idempotent only via deduplication** — which means the vendor's dedup key, window and retention
  are now part of *your* contract, and everything in step 4 applies.
- **Not idempotent** — record what you must do after an ambiguous timeout, because "retry" is not
  available. This is where reconciliation earns its place.

Then choose your own idempotence route knowing the costs differ in kind. Explicit deduplication
requires retaining a history of identifiers, and **the required history length is exactly the
number of messages the sender may have unacknowledged in flight** — so a sender that stops waiting
for per-message acknowledgement to gain throughput directly enlarges your memory requirement.
Decide explicitly whether that history survives a restart. Alternatively, redefine the message so
repetition is meaningless (carry absolute state rather than a delta), which costs message size
instead of memory.

**Do not deduplicate on a business key.** Putting a unique constraint on an order number is
efficient and looks elegant, but it loads one field with two meanings: *this is order X* and *this
delivery is a repeat*. The moment the business legitimately allows a second message with the same
key — amending an existing order, which is entirely normal — the mechanism rejects valid traffic.

### 6. Pin correlation

Three different fields, routinely conflated:

| Field | Property | What it is for |
|---|---|---|
| Message id | unique, not comparable (often a GUID) | identifying one message |
| Correlation id | unique *enough* to match a reply to its request | resuming the right task |
| Sequence number | **consecutive**, not merely ascending | detecting gaps |

Only the third detects loss, because a gap is the only evidence something is missing. Test whether
a vendor's ordering field is genuinely consecutive by looking for gaps during a quiet period — many
"sequence" fields are merely ascending, which cannot prove completeness. If it is not consecutive,
name the alternative completeness evidence: a per-window count, a reconciliation endpoint, or a
periodic full extract.

Two constraints:

- **A correlation identifier is only unique inside the scope that minted it.** A requestor's id
  needs to be unique only across its own outstanding requests. Put a gateway or shared reply path
  in the middle and identifiers from different requestors collide, producing what look like random
  mis-delivered replies. An intermediary must mint its own.
- **Never use the transport's message id as a correlation key.** It is neither stable nor reliably
  echoed, and correlating on it tells you which request message a reply answers without telling you
  which business task to resume.

Prefer correlating on **your own business key**, echoed by the vendor in a field they agree to
carry. Where the vendor will not carry one, you own the map between their identifier and yours —
say so explicitly, because that map is a piece of infrastructure someone has to run.

### 7. Establish the failure channels

Two distinct channels with different owners:

- A **dead message** is one the messaging system itself cannot deliver, judged from the header.
- An **invalid message** is one delivered perfectly well that the receiver cannot process, judged
  from the body.

The asymmetry that matters: **dead-message handling is whatever the infrastructure provides, and
you inherit it. Invalid-message handling is yours.** Design the second; discover and document the
first.

Note that no message is inherently valid or invalid — validity is the receiver's context. Two rules
follow: receivers with different validity expectations must not share a channel, and a message
valid for one receiver on a channel must be valid for all of them.

**If the callback signature has no way to signal failure, handler bugs become silent data loss.**
When an exception in your handler cannot roll anything back, the provider simply proceeds to the
next message and the failed one is gone — at a volume equal to your defect rate. Establish the
failure channel *before* subscribing. Tell: a rising exception count in the handler with no
corresponding growth anywhere else.

### 8. Choose polling or push deliberately

You get rate control or efficiency, not both.

**Polling** lets the consumer take work only when ready, so overload becomes a queue rather than a
collapse — at the cost of burning cycles checking an empty channel. **Push** consumes nothing while
idle but hands you messages at the arrival rate with no throttle.

This matters most **at recovery**: an outage produces a backlog that is then delivered as fast as
the vendor can push it, precisely when your system is least able to absorb it. If the vendor only
pushes, the throttle has to be yours.

### 9. Specify the compensations

For every guarantee marked absent, name what you build:

| Absent | Compensation |
|---|---|
| Exactly-once | dedup store, keyed on the vendor's id, sized from the in-flight window |
| Ordering | version/timestamp check with last-writer-wins, or a resequencing buffer with a timeout |
| Replay beyond the window | a bulk extract path, and the cadence at which it runs |
| A failure channel | your own poison-message store, with an owner and an alerting rule |
| Completeness evidence | periodic reconciliation against a count or a full extract |
| Backfill for pre-subscription history | an initial load, distinct from the stream |

## Traps worth checking explicitly

**Echo loops.** A system that both publishes to and subscribes from the same change feed receives
its own event, applies it, emits another, and loops without bound. Nothing in the mechanism
prevents this. The only defence is provenance on every message plus an origin check by every
subscriber.

**Throttling by dropping loses data when messages are partial updates.** Ignoring anything arriving
within N milliseconds of the last accepted message is safe only if every message carries full
state. On a feed where each update carries only changed fields, time-based dropping silently
discards updates no later message will repeat. Merge successive messages into an accumulating
record instead.

**Expiry plus a slow consumer is an outage.** Expiry does not delete a message; it moves it to the
dead letter channel. A consumer that cannot keep up quietly converts its backlog into dead-letter
growth, which is unbounded storage on shared infrastructure — enough, in practice, to bring down a
broker and take unrelated components with it.

**Expiring a reply is the dangerous case.** If a reply expires, the requester never learns whether
the request was received at all, and an unanswerable question is worse than a failure.

**Subscription filters are not an authorization boundary.** Systems authorize access to a channel
but generally not the consumer's *selection criteria*, so any consumer permitted on the channel can
widen its filter. Using filters to keep one tenant's or partner's messages from another is security
theatre; only separate channels with separate access control actually exclude anyone.

**A broadcast feed can be read by an extra party undetectably.** On a point-to-point channel an
eavesdropper consumes messages, so they go missing and it is noticed quickly. On a broadcast
channel nothing changes at all.

**A reference in a payload is a promise the sender cannot keep.** An identifier that must be
dereferenced back to the source requires a synchronous callback — reintroducing exactly the
coupling the async channel removed — and by the time the message is consumed the referenced entity
may no longer exist.

## Output format

```
# <System> event delivery contract

## Summary
<what this feed can and cannot be relied on for, in three lines>

## Guarantees
| Property | Vendor states | Observed | Verdict (stated/observed/absent) | Evidence |
| Arrival | | | | |
| Ordering (and scope) | | | | |
| At-most / at-least / exactly once | | | | |
| Replay: retention duration | | | | |
| Replay: per-subscription cap | | | | |
| Behaviour while consumer offline | | | | |
| Dedup key and window | | | | |
| Correlation field | | | | |
| Completeness evidence | | | | |
| Failure channel | | | | |

## Idempotence classification
| Operation | Inherent / via dedup / none | If ambiguous timeout, do this |

## Required compensations
| Absent guarantee | What we build | Owner |

## Backfill and cold start
<the route for everything the stream cannot reach>

## Open questions
```

## Related work

- Bulk and historical extraction, and the cold-start route → `plan-vendor-data-extraction`
- The request/response surface → `document-vendor-api-surface`
- Translating the events into your model → `design-vendor-anticorruption-layer`
- What the feed cannot tell you at all → `report-vendor-capability-gaps`
- Testing whether the stated guarantees hold → `probe-vendor-contract-empirically`
