# Choosing the event type that crosses a boundary

Read when deciding what a component publishes to others. Contents: [why it matters](#why-the-choice-matters) · [event notification](#event-notification) · [event-carried state transfer](#event-carried-state-transfer) · [domain event](#domain-event) · [side by side](#the-same-fact-three-ways) · [selection rules](#selection-rules) · [events vs commands](#events-versus-commands) · [structure](#message-structure)

## Why the choice matters

Events are not a substance you pour over a system to decouple it. Applied carelessly they turn a modular monolith into a distributed one, where every component depends on every other's internals and nothing can be changed alone.

The choice of event *type* is what decouples or couples the system. It is a design decision about the contract, not a serialisation detail.

## Event notification

**Carries.** The fact that something happened, an identifier, and usually a link. Deliberately not the detail.

```json
{
  "type": "paycheck-generated",
  "event-id": "537ec7c2-d1a1-2005-8654-96aee1116b72",
  "timestamp": 1615726445,
  "payload": { "employee-id": "456123", "link": "/paychecks/456123/2021/01" }
}
```

**How consumers use it.** They react by fetching what they need from the producer.

**Buys.** The smallest possible public surface. The producer's internal model stays private, and changes to it rarely break anyone.

**Costs.** A round trip per event, and temporal coupling — the consumer cannot proceed while the producer is unavailable.

**Reach for it when** the consumer must see the producer's *latest* state, not a snapshot from whenever the event was emitted. The notification says "something changed, come and look", and the subsequent query returns current truth.

## Event-carried state transfer

**Carries.** The changed state — either a full snapshot of the entity, or only the fields that changed when the structure is large.

```json
{
  "type": "customer-updated",
  "customer-id": "01b18d56-b79a-4873-ac99-3d9f767dbe61",
  "payload": {
    "first-name": "Carolyn", "last-name": "Hayes", "phone": "555-1022",
    "status": "follow-up-set", "follow-up-date": "2021/05/08", "version": 7
  }
}
```

**How consumers use it.** They maintain a local cache of the producer's data and read from it.

**Buys.** This is asynchronous data replication. Consumers keep functioning when the producer is down, and components needing data from several sources stop querying them repeatedly.

**Costs.** The consumer's copy is eventually consistent, and you have deliberately published a data model that consumers will come to depend on.

**Reach for it when** the consumer can tolerate slightly stale data, and especially when it would otherwise query the producer constantly.

## Domain event

**Carries.** A business occurrence, modelled as closely as possible to how the business understands it, with the data describing *that occurrence*.

```json
{ "type": "ticket-escalated", "ticket-id": "c9d286ff", "escalation-reason": "missed-sla",
  "escalation-time": 1628970815 }
```

**How consumers use it.** They react to a meaningful business fact.

**What it cannot do.** It is not sufficient to maintain a cache of the entity. Even a rich domain event does not describe the entity's state, and other events the consumer does not subscribe to touch the same fields. Treating a stream of domain events as replication produces a cache that is wrong in ways nobody notices.

**The intent differs too.** Notifications exist to ease integration. Domain events exist to *model the domain* — they are worth having even when nobody subscribes, which is exactly the case in a system where they capture every internal state transition.

**Reach for it sparingly across boundaries**, and prefer designing a dedicated set of public domain events over exposing the internal ones.

## The same fact, three ways

A person gets married:

```javascript
notification = {
  type: "marriage-recorded",
  person-id: "01b9a761",
  payload: { person-id: "126a7b61", details: "/01b9a761/marriage-data" }
};

stateTransfer = {
  type: "personal-details-changed",
  person-id: "01b9a761",
  payload: { new-last-name: "Williams" }
};

domainEvent = {
  type: "married",
  person-id: "01b9a761",
  payload: { person-id: "126a7b61", assumed-partner-last-name: true }
};
```

Read what each loses:

- The **notification** carries nothing but the fact and a pointer. Any consumer needing detail must ask.
- The **state transfer** says the last name changed. It cannot say why — marriage and divorce are indistinguishable. A consumer needing the reason is stuck.
- The **domain event** says exactly what happened in business terms. But it cannot maintain a copy of the person record, because it only describes this occurrence.

## Selection rules

Ask about the consumer, not the producer:

| The consumer... | Send |
|---|---|
| must read the producer's latest write | notification, then it queries |
| can work from eventually consistent data | state transfer |
| needs to react to a business occurrence, not track state | domain event (public, purpose-designed) |
| needs several of the above | more than one event type; do not compromise on one |

Two further rules:

- **Never expose the internal event set as the contract.** If consumers are subscribing to events you designed to capture internal state transitions, you have published your implementation. Project the model consumers need inside the producer and publish that instead.
- **Watch for two consumers building the same projection.** They are now coupled to each other through your internals, duplicating the same logic in two places where it will drift. Move that projection into the producer.

## Events versus commands

Both travel as messages, and they are not the same thing:

- A **command** describes an operation that has to be carried out. Its target may **refuse** it — invalid, or contrary to a rule.
- An **event** describes a change that has already happened. A recipient **cannot cancel** it. The only way to overturn an event is a compensating action, which is itself a command.

This is why events are named in the past tense and commands in the imperative — the naming keeps the asymmetry visible in every conversation about the flow.

## Message structure

A workable envelope separates metadata from payload:

```json
{
  "type": "delivery-confirmed",
  "event-id": "14101928-4d79-4da6-9486-dbc4837bc612",
  "correlation-id": "08011958-6066-4815-8dbe-dee6d9e5ebac",
  "delivery-id": "05011927-a328-4860-a106-737b2929db4e",
  "timestamp": 1615718833,
  "payload": { "confirmed-by": "17bc9223-bdd6-4382-954d-f1410fd286bd",
               "delivery-time": 1615701406 }
}
```

- **event-id** — lets consumers deduplicate, which they must, since delivery is at-least-once.
- **correlation-id** — ties events arising from one originating action together, which is what makes a distributed flow debuggable at all.
- **timestamp** — the business time of the occurrence, distinct from when the message was delivered. Events arrive out of order; consumers need the former to reason correctly.
