# Operating a model where events are the source of truth

Read only when events are becoming the source of truth rather than a notification mechanism. Contents: [what changes](#what-changes) · [the store](#the-event-store) · [projections](#projections) · [replay and time travel](#replay-and-time-travel) · [performance](#performance-and-when-to-snapshot) · [scaling](#scaling) · [concurrency](#concurrency-done-better) · [deletion](#deleting-data-from-an-append-only-store) · [backfilling history](#backfilling-history-for-existing-data) · [the cheap substitutes](#why-the-cheap-substitutes-fail) · [costs](#the-costs-worth-weighing)

## What changes

Ordinary modelling persists the current state and emits selected events. Here, **all** changes to state are expressed as events, and the events are the truth from which state is derived.

That is the whole difference, and it is bigger than it sounds: it means no state transition can occur without a corresponding recorded event, because appending the event *is* the transition.

## The event store

The store is append-only. It permits no modification and no deletion — data migration being the recognised exception — and it needs only two operations:

```
Fetch(instanceId)                                  -> all events for one entity
Append(instanceId, newEvents[], expectedVersion)   -> or a concurrency failure
```

The `expectedVersion` argument is the concurrency control: you state the version your decisions were based on, and if events were appended since, the store rejects the write.

This is not novel machinery. A financial ledger is the same idea — an append-only log of transactions from which the current balance is projected.

## Projections

State is produced by applying events in sequence. A projection implements an apply rule per event type it cares about and ignores the rest.

Two things follow that make this worth the trouble:

**Many projections from one stream.** A search view can accumulate every name and phone number an entity ever had. An analysis view can count how many times a given event occurred and derive a status from the last meaningful one. They read the same events and disagree about which matter.

**New projections work on old events.** A projection added a year from now replays events already recorded. You do not need to have anticipated it, and you do not need to re-instrument anything. This is the single largest practical benefit.

When projections are materialised into queryable stores rather than built in memory, the read models are disposable: a correct implementation can wipe any projection entirely and rebuild it. They are also read-only — no operation writes to a projection directly. Only the event stream is truth.

## Replay and time travel

Because the version counts modifications, applying only the first N events yields the state at version N.

- **Analysing decisions.** Reconstruct exactly what the system knew when it decided, rather than inferring it from the current state.
- **Retroactive debugging.** Revert an aggregate to the state it held when a defect was observed, and step forward.

## Performance and when to snapshot

Rebuilding state costs compute that grows with stream length. The figures worth holding, as rules of thumb rather than guarantees:

- The performance hit becomes noticeable **only past roughly 10,000 events per aggregate**.
- In most systems, an aggregate's average lifespan stays **under about 100 events**.

Benchmark your own projection against your expected lifespan before assuming there is a problem. The gap between those two numbers is why the concern is usually theoretical.

**Snapshotting** — caching a projection and applying only later events on top — is an optimisation that must be justified. Below 10,000 events per aggregate it is accidental complexity.

Before implementing it, **re-examine the aggregate's boundary.** An aggregate genuinely accumulating that many events is more often too large than genuinely long-lived, and fixing the boundary solves the performance problem and several others.

## Scaling

Every operation happens in the context of a single aggregate, so the store shards cleanly by aggregate id: all events for one instance live in one shard. There is no cross-shard query in the write path.

## Concurrency, done better

Classic optimistic concurrency throws whenever the data you read was overwritten, with no information about *what* overwrote it.

With the events available you can see exactly what was appended between your read and your write, and decide **on domain grounds** whether those events actually conflict with your operation or are irrelevant, in which case it is safe to proceed. That is a genuine improvement over blanket rejection, and it is only possible because the intermediate steps were recorded.

## Deleting data from an append-only store

When regulation requires physical deletion, the store cannot simply be edited.

Put sensitive fields into events in **encrypted** form, and hold the encryption key in an external key-value store keyed by the aggregate's id. Deleting the key renders that content unreadable in every event, satisfying the deletion requirement without mutating the log.

## Backfilling history for existing data

Converting existing state into an event-based model has no clean answer, because the fine-grained past does not exist. Two honest options:

**Generate an approximate stream.** Infer a plausible sequence per instance that projects to exactly the current state — initialised, contacted, order submitted, payment confirmed. Verify it by projecting and comparing against the original data, which is easy and reliable.

*Cost:* it can never represent the real history. You cannot know how many attempts, reversals or corrections actually occurred, and the stream looks authoritative while being fiction. Anyone analysing it later will draw wrong conclusions with full confidence.

**Model an explicit migration event.** Emit one event per instance carrying the legacy state wholesale:

```json
{ "lead-id": 12, "event-id": 0, "event-type": "migrated-from-legacy",
  "first-name": "Shauna", "status": "converted",
  "last-contacted-on": "2020-05-27T12:02:12.51Z", "converted-on": "2020-05-27T12:38:44.12Z" }
```

*Buys:* the absence of history is undeniable. Nobody can mistake the stream for a complete record.
*Costs:* legacy traces stay in the store permanently, and every projection must handle the migration event forever.

Prefer the explicit migration event unless you have a specific reason not to. A model that lies quietly is worse than one that admits a gap.

## Why the cheap substitutes fail

Three approaches look like they give you history for less. Each fails in a specific way worth knowing before someone proposes it:

**A logfile beside the database.** This is a transaction across two storage mechanisms. When the database transaction rolls back, nobody deletes the log lines already written. The trail is not consistent; it is eventually *in*consistent, in a way that surfaces only when someone relies on it.

**A log table written in the same transaction.** Infrastructurally consistent, and still fragile: it depends on every engineer, now and later, remembering to write the record. And with state as the source of truth, nothing enforces the log's content or format, so the schema degrades into whatever people happened to write.

**A database trigger copying rows into a history table.** This removes the manual step, and it captures only which fields changed — never *why*. That missing intent is precisely what makes new projections impossible later. "Status went from A to B" cannot answer "how many were halted by an operator versus by a threshold", and no amount of retrospective analysis recovers it.

## The costs worth weighing

Three real ones, all worse when a simpler design would have sufficed:

- **Learning curve.** It differs sharply from ordinary state management. Unless the team has done it, budget for the adjustment.
- **Evolving the model.** Events are immutable, so changing an event's schema is not like changing a table's. This is a substantial topic in its own right.
- **Architectural moving parts.** Projections, a read side, a relay, checkpoints. The design is genuinely more complicated.

Adopt it when deep insight into behaviour matters for an area the business competes on, when an audit log of every change is legally required, or when the system moves money and the flow must be traceable. Those are the cases where the costs are repaid.
