---
name: model-lifecycle-and-events
description: Models the lifecycle of a domain concept as named states and legal transitions — each with its trigger, guard and resulting event — and produces the state diagram and event vocabulary everything downstream refers to by name. Covers why a status field records where something is but never how it got there, making every state change a past-tense event emitted by a guarded command rather than an assignment, projecting state from an event stream and replaying a prefix to reach any past state, the three event types and which may cross a boundary, splitting private from public events, publishing reliably through an outbox, and compensating actions. Use whenever designing or documenting a lifecycle, workflow, status field or state machine; when asking which transitions are legal and what guards them; when something reached a state nobody thought reachable; when history, audit or "how did it get into this state" matters; when naming events or deciding their payloads; when deciding which events other components may consume; or when designing rollback, cancellation or compensation — even when the ask is only "what statuses should this have". For which objects the transitions belong to use design-aggregates-and-invariants; for whether this is warranted use choose-business-logic-pattern; for terminology use build-domain-glossary.
---

# Modelling lifecycle states and events

A status column tells you where something is. It cannot tell you how it got there, and it silently destroys the evidence every time it changes.

That matters twice over. It matters to the business, because the interesting questions are historical — how many attempts preceded success, how long each stage took, whether pursuing this any further is worth it. And it matters to the model, because a lifecycle expressed as an assignable field has no place to put the rules about which transitions are *legal*. Anyone can write any value.

The fix for both is the same: name the states, name the transitions, and make each transition a guarded command that emits a past-tense event.

## The output

A state model. This is the artifact other work refers to by name, so it has to be complete enough to settle arguments.

**1. States.** Named, with which are initial and which are terminal.

**2. A transition table.** One row per legal transition — nothing else is legal:

| From | Command | Guard | Event emitted | To |
|---|---|---|---|---|
| Planned | `start rollout` | artifact is signed; at least one phase defined | `rollout-started` | Canary |
| Canary | `advance phase` | phase success criteria met; no open incident | `phase-advanced` | Broad |
| Canary | `halt rollout` | — | `rollout-halted` | Halted |
| Halted | `roll back` | at least one device updated | `rollback-started` | RollingBack |

**3. Explicitly illegal transitions.** The ones people will try. Stating that `Completed → Canary` is not reachable is as load-bearing as any legal row, because it is the claim a reviewer can check.

**4. Event vocabulary.** Every event, past tense, with its payload and whether it is private or public.

**5. A diagram.** States as nodes, transitions as labelled edges. Mermaid `stateDiagram-v2` renders anywhere and diffs in review:

```
stateDiagram-v2
    [*] --> Planned
    Planned --> Canary: start rollout
    Canary --> Broad: advance phase
    Canary --> Halted: halt rollout
    Broad --> Completed: advance phase
    Broad --> Halted: halt rollout
    Halted --> RollingBack: roll back
    RollingBack --> RolledBack: rollback completes
    Completed --> [*]
    RolledBack --> [*]
```

**6. The history questions** the model must be able to answer.

### How the states are represented

The transition table says which moves are legal. What stops an *illegal* state existing in the first place is how the states are represented, and the default representation defeats the whole exercise.

A single record carrying the lifecycle in flags — `isValidated`, `isPriced`, an optional `amountToBill` — fails three ways: the states are implicit so every reader needs conditional code; data belonging to one state must be made optional because other states lack it; and nothing ties a field to the flag governing it, so `{ status: Placed, amountToBill: 500 }` is constructible and meaningless.

Give each state its own type carrying exactly its own data, then define the concept as a closed choice across them. A state with no data of its own needs no type, just a case. Then a step can demand the state it requires, and the ordering in your transition table stops being a convention people respect and becomes something that is checked.

`make-illegal-states-unrepresentable` covers this in full, including how to gate a state so only the transition that grants it can construct it.

## Step 1 — Ask what history is worth

Before designing anything, write down the questions the business will ask about the past. How many retries preceded success? How long did each phase take? Which devices failed and were they the same ones as last time? Was this halted by a human or by a threshold?

**If that list is non-empty, current state alone is the wrong model.** If it is genuinely empty — and for some concepts it is — a status field with guarded transitions is enough, and you can skip the event-sourcing sections here.

Do not apply the pattern by default. Deciding how much machinery the area deserves is `choose-business-logic-pattern`.

## Step 2 — Lay out the events on a timeline

Collect what happens, in past tense, then order it.

**Lay the successful path first**, end to end. Then branch the alternative and failure paths off it. Doing the happy path first is not politeness — it gives you the spine that the exceptions attach to, and it makes the missing exceptions visible, because every step on the spine raises the question of what else could have happened there.

Then mark the events that represent a **change of phase or context** rather than an ordinary step. `cart-initialised`, `order-shipped`, `order-delivered`, `order-returned` are of a different character to the steps between them. Those pivots partition the lifecycle, and they are also the strongest early indicator of where a model boundary belongs.

For deriving this from a specification, a legacy system or a group of people, use `derive-model-from-business-process`.

## Step 3 — Give every transition a command, a guard and an event

For each edge in the model:

- **Command**, imperative: `halt rollout`, `register device`. It is a request, and it can be refused.
- **Guard**: what must be true for it to be accepted. This is the actual content of "legal transition" — a transition with no guard is one that is always legal, which should be a deliberate statement rather than an omission.
- **Event**, past tense: `rollout-halted`, `device-registered`. It records something that already happened and cannot be refused.

The tense convention is not style. An event that has happened cannot be cancelled or rejected — the only way to overturn one is to issue a compensating command that produces a further event. Naming events in the past tense keeps that asymmetry visible in every discussion.

### Account for every command

By the time the model is done, each command must be triggered by exactly one of three things:

1. **A role** — a person or system actor issues it.
2. **A policy** — an observed event automatically triggers it. Write the decision criteria on the policy itself: "escalate on complaint received, only for priority accounts."
3. **An external system** — something outside this model calls it.

**A command with no trigger is missing knowledge, not a detail to fill in later.** Record it as a finding. Inventing a plausible trigger is how a wrong model gets locked in, because nobody afterwards remembers it was a guess.

## Step 4 — Make state changes happen by emitting events

Where history matters, the aggregate never assigns a state field. A command validates its preconditions against the current state and, if they hold, **appends an event**; the projection logic is what mutates the fields.

```
execute(RequestEscalation cmd):
    if not state.isEscalated and state.remainingTimePercentage <= 0:
        append(new TicketEscalated(id, cmd.reason))     # not: isEscalated = true
```

This is the mechanism that guarantees no transition can happen without a recorded event. An assignment can be added anywhere by anyone; an append is the only path to a state change, so the record cannot drift from reality.

Each operation then follows a fixed script:

1. Load the events.
2. Project them into a state representation used for decisions.
3. Execute the command — it checks its guard against that state and appends new events.
4. Commit the new events with the version the decision was based on.

The version counts modifications, which gives you something valuable for free: **applying only the first N events reconstructs the state at version N.** That is how you analyse why the system decided what it decided, and how you revert an aggregate to the exact state it held when a defect was observed.

One stream also supports **many projections**, and new ones can be added later against events already recorded — a search view accumulating every historical value a field ever held, an analysis view counting occurrences. Projections ignore the events they do not care about. Nothing needs re-instrumenting.

If events are becoming the source of truth, read `references/event-sourcing-operations.md` before committing to it.

## Step 5 — Decide which events leave the boundary

An event's payload and its intent differ depending on who it is for. There are three kinds, and picking the wrong one is what turns an event-driven system into a distributed mess:

- **Event notification** — says only that something happened; the consumer fetches the detail. Minimal public surface.
- **Event-carried state transfer** — carries the changed state, as a full snapshot or only the changed fields. It is asynchronous replication: consumers hold a local cache and keep working when the producer is down.
- **Domain event** — describes a business occurrence as faithfully as possible. It carries the data describing *that occurrence*, not the entity's state, and is not sufficient to cache the entity, because other events the consumer does not subscribe to touch the same fields.

The same fact, three ways:

```
notification:    { type: "marriage-recorded", person-id: "01b9", details: "/01b9/marriage-data" }
state transfer:  { type: "personal-details-changed", person-id: "01b9", new-last-name: "Williams" }
domain event:    { type: "married", person-id: "01b9", partner-id: "126a", assumed-partner-last-name: true }
```

The state-transfer message cannot say *why* the name changed — marriage or divorce look identical. The domain event says what happened but could not maintain a cache. Neither is better; they answer different questions.

Full selection guidance is in `references/event-types.md`.

### Split private from public, deliberately

**Do not let other components subscribe to your internal event set.** Events designed to capture every internal state transition are your implementation model. Exposing them couples every subscriber to your internals, and it gets worse: when two subscribers each project the same view from your raw events, they become coupled *to each other* by duplicating the same logic.

Instead, project the model consumers need inside the producer and publish that as the integration-facing contract, decoupled from the internal one. Then:

- **Private events** — internal state transitions. Change freely.
- **Public events** — the deliberately designed set others may consume. Change like an API.

Mark which is which in the vocabulary, and pick the type per consumer from its consistency need: **eventually consistent consumer → state transfer; consumer that must read your latest write → notification plus a query.**

## Step 6 — Publish reliably

Raising an event and pushing it to a bus inside the aggregate's own method dispatches it **before the new state is persisted**. A subscriber can act on a fact the database does not yet reflect, and if the transaction then rolls back, the event is already gone and cannot be retracted.

Moving the publish into the surrounding layer, after the commit, is better and still broken: if the bus is down or the process dies between commit and publish, the change is durable and the notification never happens.

**The outbox fixes both.** Commit the new state and the new events in one atomic transaction, then have a relay read the committed events, publish them, and mark or delete them. Relational stores use a dedicated outbox table; stores without multi-document transactions embed pending events in the aggregate's own record. The relay either polls for unpublished events — needing indexes to keep the load down — or is pushed to by tailing the store's change stream.

**Delivery is at-least-once, not exactly-once.** A relay that dies after publishing but before marking will publish again. Every consumer must be idempotent.

### The idempotence trap worth knowing

An operation that updates one row in one database can still behave like a distributed transaction, because it also communicates success to its caller. If the update commits but the response is lost, the caller assumes failure and retries — and a *relative* update (`visits = visits + 1`) applies twice.

The fix is to make effects absolute rather than relative: have the caller read, compute and pass the final value; or pass the value it read and apply the update only where the stored value still matches.

## Step 7 — Model the processes that span aggregates

When a flow crosses several aggregates — activation triggers a submission, whose confirmation or rejection changes the original — do not merge them into one aggregate to make the transaction fit. Those are different entities with different responsibilities, possibly in different boundaries.

Two shapes, and the distinction is sharp:

- **Saga** — matches events to commands, and issues compensating actions when a step fails. Long-running in *transactions*, not necessarily in time; one may last seconds or years. Instantiated implicitly by observing one triggering event.
- **Process manager** — holds the state of a sequence and decides what comes next. **If the flow contains branching logic choosing a course of action, it is a process manager.** It has no single source event and must be started explicitly.

Process managers are commonly implemented as aggregates themselves, with their own state and their own events.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Cannot answer how something reached its state | Status field only | Model the transitions as events |
| An entity is in a state nobody thought reachable | Transitions were assignments, not guarded commands | Build the transition table; state the illegal ones |
| Audit trail written to a logfile beside the database | Two-storage transaction; the log survives a rollback | Outbox — commit state and events together |
| History table populated by a database trigger | Captures which fields changed, never why — and the missing intent is what makes future projections impossible | Record the business event, not the field diff |
| Subscriber acts on a fact the database does not have yet | Event published before commit | Outbox |
| Reprocessing an event changes the result | Consumer not idempotent under at-least-once delivery | Make effects absolute, not relative |
| Every consumer subscribes to every internal event | Implementation model exposed as the contract | Project in the producer; publish a designed public set |
| Two consumers independently build the same projection | They are coupled to each other through your internals | Move the projection into the producer |
| Rebuilding state is slow | Stream far longer than the concept warrants | Check the aggregate boundary before adding snapshots |
| A "saga" full of if-else branches | It is a process manager | Give it explicit state and an explicit start |

## Bundled references

- `references/event-types.md` — the three event types with selection rules, payload shapes, and what each cannot do. Read when deciding what crosses a boundary.
- `references/event-sourcing-operations.md` — projections, replay, version semantics, snapshot thresholds and when they are premature, sharding, deletion under privacy rules, and the two ways to backfill history with what each costs. Read only when events are becoming the source of truth.

## Related

For representing the states themselves so contradictory combinations cannot be built, use `make-illegal-states-unrepresentable`. For the steps of a *process* — what each consumes, produces, depends on and how it fails — use `model-workflow-as-type-pipeline`; that skill covers the pipeline, this one covers the entity's states and the events recording them, and a long-running workflow needs both.

## Worth reading

- Greg Young, *Versioning in an Event Sourced System* (2017) — on evolving event schemas, the hardest part of this.
- Hohpe & Woolf, *Enterprise Integration Patterns* (2003) — the origin of the process-manager and messaging patterns.
- Chris Richardson, *Microservice Patterns* (2019) — worked saga, process manager and outbox implementations.
