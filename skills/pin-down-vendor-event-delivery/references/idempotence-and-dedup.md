# Idempotence, deduplication and the retry window

Read at steps 4-5, and any time someone proposes retrying a vendor call that changes state.

Contents: [why this is the hinge](#why-this-is-the-hinge) · [classify before retrying](#classify-before-retrying) ·
[the two routes to idempotence](#the-two-routes-to-idempotence) · [sizing the dedup history](#sizing-the-dedup-history) ·
[choosing the key](#choosing-the-key) · [the vendor's dedup window](#the-vendors-dedup-window) ·
[the ambiguous timeout](#the-ambiguous-timeout) · [checklist](#checklist)

## Why this is the hinge

Almost every safety property at an event boundary reduces to one question: **can this be delivered
twice, and does that matter?**

If duplicates are harmless, at-least-once delivery is fine and most of the machinery below is
unnecessary. If duplicates are harmful, then every retry, every failover, every replay and every
redelivery after a crash is a potential duplicate side effect — and duplicates are not an edge case
in these systems, they are the normal consequence of the delivery guarantee you were given.

The failure here is quiet and expensive: a duplicate payment, a duplicate policy, a duplicate
adjustment. None of them raises an error.

## Classify before retrying

Every vendor operation goes in exactly one bucket, and the bucket must be recorded:

**Inherently idempotent.** Repetition is meaningless by nature — a read, a quote request, an
informational notification, setting a value to an absolute state. Replay freely.

**Idempotent only via deduplication.** The operation would duplicate, but something in front of it
discards repeats. This is *conditional* idempotence, and the condition is now part of your
contract: the key it deduplicates on, the window it remembers, and what it does past that window.
Treating this bucket as if it were the first is the single most common route to a duplicate
transaction.

**Not idempotent.** Retry is simply not available. Record what you do instead after an ambiguous
timeout — which is where reconciliation stops being optional.

A vendor operation is in bucket two far more often than its documentation suggests, because
"idempotent" in vendor documentation usually means "we deduplicate", not "repetition is
meaningless".

## The two routes to idempotence

Both work. Their costs are not comparable, and choosing without knowing which cost you are buying
is how teams end up with the wrong one.

**Route 1 — explicit deduplication.** The receiver retains a history of identifiers and discards
anything it has seen. Cost: **memory**, plus the operational question of whether that history
survives a restart.

**Route 2 — redefine the message so repetition is meaningless.** Carry absolute state rather than a
delta ("balance is 500", not "add 50"). Cost: **message size**, and the loss of the ability to
express an increment.

Route 2 is underused. Where you control the message shape — which you often do on your own side of
the anti-corruption layer, even when you do not control the vendor's — it removes the problem
rather than managing it, and it removes the entire class of state described in the next section.

## Sizing the dedup history

The required history length is not a guessed time period. It is **exactly the number of messages
the sender may have unacknowledged in flight.**

The consequence is a coupling that surprises people: a sender that stops waiting for per-message
acknowledgement in order to gain throughput directly enlarges the receiver's memory requirement.
Two teams tuning independently — one for throughput, one for memory — can each make a locally
correct decision and break the system between them.

Decide explicitly whether the history survives a receiver restart. If it does not, you accept
duplicates across restarts, and that must be a stated decision rather than a discovered one.

## Choosing the key

**Use a dedicated identifier minted for deduplication.** Ask whether the vendor assigns a unique
message identifier distinct from any business field, and prefer it.

**Never deduplicate on a business key.** Putting a unique constraint on an order number is
efficient and looks elegant, but it loads one field with two meanings — *this is order X* and *this
delivery is a repeat*. The moment the business legitimately allows a second message with the same
key (amending an existing order is entirely normal), the mechanism rejects valid traffic, and the
fix requires changing the message structure under production load.

**Never accept content-derived deduplication.** A hash of the request body cannot distinguish an
intended repeat from a retry, and the same payload can legitimately be meant twice — two identical
charges on the same day, two identical adjustments. A vendor that deduplicates by content silently
drops your second legitimate transaction and returns success. The only escape is perturbing the
payload with a meaningless difference, which is a workaround worth recording as a capability gap.

## The vendor's dedup window

Three properties, all of which must be obtained rather than assumed:

**Duration.** Typically a few minutes — around five is a common recommendation — with the timer
reset on each hit so a retried request gets a fresh window. That is the entire guarantee.

**What happens past it.** Nothing good and nothing loud: there is no cached entry, so the request
executes again as though new. No error, no warning, a clean success, and a second effect. This is
the precise mechanism by which a queued retry becomes a duplicate payment, and it is why **a retry
queue that can hold work longer than the vendor's dedup window is a defect**. Check your queue's
maximum age against that window explicitly.

**What the response contains.** The cached response from the *first* execution, deliberately frozen
— keeping it current as the underlying data changed would be more confusing than serving it stale.
So the body describes state at the moment of the original call, and other parties may have changed
the record many times since. **Never write a deduplicated retry's response into your system as
current state.** Treat it as confirmation that the work happened, then re-read.

## The ambiguous timeout

The bucket that matters. You sent a state-changing request and got no answer. The work may or may
not have happened, and your timeout ended your wait without cancelling anything — the far side
never learned you left.

Options, in order of preference:

1. **Retry under an idempotency key**, if the operation is in bucket two and you are inside the
   window. Cheapest and safest.
2. **Query for the effect** before retrying, if the vendor offers a way to ask "did this happen?"
   Requires an identifier you supplied and the vendor stored.
3. **Reconcile later**, if neither is available — record the uncertainty explicitly in your own
   store as an unresolved outcome, and resolve it against a periodic extract.
4. **Do nothing and hope.** Never acceptable for a financial or legal effect, but sometimes the
   honest choice for a low-value notification. Make it a decision, not an omission.

The critical design point: option 3 requires the uncertainty to be **representable in your data
model**. If your records can only be "sent" or "failed", there is nowhere to put "we do not know",
and the system will silently pick one — usually the wrong one. Make the unknown state explicit
before you need it.

## Checklist

- [ ] Every vendor operation classified into one of the three buckets
- [ ] For bucket two: key, window duration, and past-window behaviour recorded
- [ ] Retry queue maximum age checked against the vendor's dedup window
- [ ] Dedup key is a dedicated identifier, not a business key, not a content hash
- [ ] Dedup history sized from the sender's unacknowledged in-flight window
- [ ] Decided and recorded whether dedup history survives restart
- [ ] Deduplicated-retry responses never written back as current state
- [ ] An "outcome unknown" state exists in the data model
- [ ] Reconciliation exists for bucket three operations
