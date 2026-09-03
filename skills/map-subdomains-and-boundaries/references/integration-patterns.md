# Integration patterns between boundaries

Read when labelling edges on a context map, or when an existing relationship has started to fail. Contents: [selection](#selecting-a-pattern) · [partnership](#partnership) · [shared kernel](#shared-kernel) · [conformist](#conformist) · [anticorruption layer](#anticorruption-layer) · [open-host service](#open-host-service) · [separate ways](#separate-ways) · [translation mechanics](#translation-mechanics) · [when a pattern stops fitting](#when-a-pattern-stops-fitting)

## Selecting a pattern

Ask two questions in order.

**1. Can either side succeed without the other?**

- Neither → cooperation. Partnership if communication is strong; shared kernel if it is blocked.
- One can → customer–supplier. Continue to question 2.
- Both can, and neither wants to → separate ways, unless the area is core.

**2. Where does the power sit, and can the downstream live with the upstream's model?**

- Upstream, and the model is acceptable → conformist.
- Upstream, and the model is not acceptable → anticorruption layer.
- Downstream (the supplier wants to protect consumers) → open-host service.

The protocol — REST, messaging, shared library, file drop — is a consequence, not the decision. Two teams with the same protocol and different relationships need different contracts.

## Partnership

**Shape.** Coordination is ad hoc and two-way. Either team announces a change and the other adapts. Neither dictates the contract language; both cooperate on integration problems, because neither benefits from blocking the other.

**Requires.** Well-established collaboration, high commitment, frequent synchronisation, and continuous integration of both sides' changes to keep the feedback loop short.

**Fits badly.** Geographically distributed teams, where the synchronisation this depends on is exactly what is hardest.

**Watch for.** Partnership between boundaries owned by the *same* team tends to erode the boundary over time, because ad hoc coordination has no forcing function to keep the contract explicit. A shared kernel is sometimes the better choice there, precisely because it makes the contract a thing that exists.

## Shared kernel

**Shape.** A limited part of the model is implemented in both boundaries, designed for the needs of all of them and kept consistent across all of them. A change to it takes effect everywhere immediately.

**Cost.** It couples the lifecycles of every participant, and it contradicts one-boundary-one-team, since the shared part is effectively developed by several teams. Treat it as a deliberate exception requiring justification.

**The applicability test.** Cost of duplication versus cost of coordination. Adopt it only when integrating the divergent changes both sides would otherwise make costs more than coordinating one shared codebase.

Integration cost rises with volatility, so this test tends to be satisfied by the most volatile areas — the core subdomains.

**Keep the scope minimal.** Ideally only the integration contracts and the data structures intended to cross the boundary. The smaller the shared surface, the smaller the blast radius of a change.

**Mechanics.** In a monorepo, the same source files referenced by both. Otherwise a dedicated project consumed as a library. Either way, **every change must trigger integration tests for every dependent boundary** — a boundary running against a stale version of the shared model is how this pattern produces data corruption rather than merely coupling.

**Legitimate uses.**
- Communication or geography rules out partnership, and implementing closely related functionality without coordination would produce desynchronised models and arguments about whose design is better.
- Temporarily, while gradually decomposing a legacy system.
- Between boundaries owned by one team, to keep an explicit contract that ad hoc integration would erode.

## Conformist

**Shape.** The downstream accepts the upstream's model as given, surrendering some autonomy.

**Justified when.** The upstream contract is an industry standard; it is a well-established model; or it is simply good enough for what the downstream needs.

**Not a failure.** Conforming to a good model is cheaper than translating from it, and translation is not free. The question is whether the model is good, not whether you had a choice.

## Anticorruption layer

**Shape.** The downstream translates the upstream's model into one that suits it.

**Three conditions, any one sufficient.**

1. **The downstream is a core subdomain.** Its model needs room, and adhering to a foreign one distorts the modelling of the problem you most need to get right.
2. **The upstream model is inefficient, inconvenient or messy.** Most common with legacy systems. Conform to a mess and you risk becoming one.
3. **The upstream contract changes often.** With a translation in place, that churn hits only the translation, not your model.

**Secondary benefit.** It keeps foreign concepts out of the downstream's vocabulary, which keeps that vocabulary smaller and its model simpler.

**Scale note.** A translation layer consumed by several downstreams becomes a boundary in its own right — one whose whole purpose is reshaping models for easier consumption.

## Open-host service

**Shape.** The supplier separates its implementation model from its public interface. The public protocol is expressed in an integration-oriented language, deliberately *not* the supplier's own internal terms.

**Buys.**
- The internal model evolves freely, as long as it can still be projected onto the published contract.
- Several versions of the public contract can be exposed simultaneously, letting consumers migrate gradually rather than in lock-step.

**It is the mirror of an anticorruption layer** — same translation, performed by the supplier instead of the consumer. Choose it when the supplier is motivated to protect consumers; choose the anticorruption layer when it is not.

**The common failure** is publishing internal events as the integration contract. That exposes the implementation model no matter how carefully the public data structures were designed — see the event guidance in `model-lifecycle-and-events`.

## Separate ways

**Shape.** No integration. The functionality is implemented independently in each boundary.

**Justified by.**
- **Communication cost.** Organisational size or politics make agreement more expensive than duplication.
- **Generic and locally integrable.** A logging framework should not be exposed as a service; the integration complexity would exceed the cost of using it in both places.
- **Model divergence.** The models differ so much that conforming is impossible and translating would cost more than writing the function twice.

**Hard exclusion: core subdomains.** Duplicating those contradicts the entire reason for investing in them, and guarantees the two copies diverge in exactly the area where divergence is most expensive.

## Translation mechanics

Translation logic is the same whether the consumer or the supplier performs it.

**Stateless** — translation on the fly, as requests pass:

- *Synchronous*: embed the transformation in the codebase — on incoming requests when publishing a contract, on outgoing calls when protecting yourself. Or offload it to an API gateway, which additionally makes serving several contract versions manageable.
- *Asynchronous*: an intermediary subscribes to the source's messages, transforms them, and forwards them. It can also filter, sparing the target boundary messages it does not care about.

**Stateful** — translation that needs its own storage. Required when the transformation must aggregate: batching incoming requests for throughput, or unifying several fine-grained messages into one.

## When a pattern stops fitting

Relationships decay, and the pattern has to follow.

| Change | Effect | Move to |
|---|---|---|
| One side moves to a distant office | Partnership's synchronisation assumption breaks | Customer–supplier |
| Teams are added | One boundary cannot have two teams | Split the boundary per team |
| Integration keeps failing between two teams who cannot collaborate | Coordination cost now exceeds duplication cost | Separate ways — unless the area is core |
| A supporting or generic area becomes core | Duplication is no longer acceptable | Integrate; customer–supplier, since one team must now own it |
| Upstream's internal changes keep breaking consumers | Implementation model is the contract | Open-host service |
| Every consumer of one upstream has built a translation layer | Organisational problem, not a technical one | Address the team relationship, not the code |
