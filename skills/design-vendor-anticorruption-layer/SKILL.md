---
name: design-vendor-anticorruption-layer
description: Designs the translation layer between a third-party or purchased system's model and your own domain model, and specifies where it sits so the vendor's vocabulary cannot reach the domain. Covers why an adapter or a wrapper interface is not by itself an anti-corruption layer, the four levels at which translation happens and why each needs its own stage, why mapping code belongs outside both the domain and the transport, enumerations that partition the space differently and so admit no total mapping, filtering inbound and enriching outbound, and the arithmetic deciding whether a shared canonical model is worth building at all — it breaks even at three systems and costs two translations per message forever. Use when building against a bought core whose model does not match yours, when vendor types or exceptions are turning up in domain code, when designing an integration module or gateway, when someone proposes a canonical or common data model, when deciding where mapping code should live, or when an integration has become hard to change — even when the ask is only "how should we wrap this". For deciding whether the relationship should be an anticorruption layer, conformist or open-host in the first place use map-subdomains-and-boundaries; for documenting the vendor's API surface use document-vendor-api-surface; for event and webhook guarantees use pin-down-vendor-event-delivery.
---

# Designing the layer between a vendor's model and yours

You are past the question of *whether* to translate. (If that is still open — whether to conform to
the vendor's model, translate against it, or ask them to publish a contract — that is a
relationship decision, and `map-subdomains-and-boundaries` settles it.) This is about building the
thing once the answer is "translate."

## The two failures this design exists to prevent

**Conforming.** Adopting the vendor's model wholesale because it is already there. The vendor's
model is shaped by their internal implementation and their other customers, and it will distort
yours permanently.

**Fake separation.** Believing you have a boundary when you have a rename. This is the more common
failure and the harder one to see, because it passes review.

> **An abstraction layer over the vendor's API is not an anti-corruption layer.** Wrapping their
> API in your own interface so you "could swap vendors later" leaves the dependency intact and
> merely renamed: your domain objects now hold references to *your* abstracted interface instead of
> theirs, and still cannot be used in any context that does not involve the vendor at all.

Real separation needs a **third component** — a mapper — that references both sides while neither
side references it. Neither the domain nor the vendor layer knows it exists. That asymmetry is the
whole thing; everything below is how to build it.

## The governing stance

Absorb the vendor's model. Do not try to make it conform, and do not adopt it.

Asking the vendor to change their model is a losing move, and so is forcing your domain onto their
shape. The mismatch is real and permanent, so the design question is not how to eliminate it but
**where to put it** — in a place you own, can test, and can change at your own pace.

## Procedure

### 1. Locate the mismatch at a level

Coupling is not one thing, and fixing it at one level does nothing for the others. Classify each
cross-system dependency:

| Level | Removed by |
|---|---|
| Transport protocol | a common channel or adapter |
| Location | routing |
| Data types and representation | a common representation |
| Data format and **semantics** | a shared model — the only level requiring agreement between *people* |

The diagnostic value is immediate: when a change in the vendor forces a change in your code, name
the level it travelled on before proposing a fix. Teams routinely solve the first three with
middleware and then wonder why changes still propagate — because only the fourth was ever the
problem.

### 2. Split translation into stages, one per layer

Build one translator per layer rather than one translator per integration. Chaining them lets any
one layer be swapped without touching the others, and lets the lower layers be reused for every
document from the same source.

Read `references/translation-levels.md` for what belongs at each stage. Two structural rules:

**The adapter is not the layer.** An adapter's message format is dictated by the implementation it
adapts — a database-level adapter typically requires field names identical to the vendor's table
and column names. That format is driven entirely by the vendor's internals and is precisely the
wrong format to integrate anything else with. So the correct shape is always two parts: a
mechanical outer edge that speaks the vendor's dialect, and a translator that converts it to your
model. An adapter alone leaves vendor vocabulary in your system wearing a new coat.

**Split the translation in two, near-domain and near-wire.** Reference resolution, datatype
coercion and stripping of unnecessary detail belong on the application side; structural remapping
onto the vendor or shared format belongs on the wire side. This buys a real property: when the
vendor changes its format, verify the change is absorbable in the wire-side stage alone. The price
is an extra component and a change to a domain object needing edits in two places — if that becomes
routine, generate the near-domain mapper rather than collapsing the layers.

### 3. Give the mapping code its own home

Mapping code has no correct owner on either side, and putting it in the domain object fails for
three reasons. It mixes plumbing with business logic. It forces the domain object to know the
vendor. And — decisively — **the same domain entity participates in several message types combined
with different other entities, so no single class can own its mapping.**

Key the mapper by **message type**, not by entity. This is the rule people most often get wrong,
and getting it wrong is what makes the layer accrete special cases until it is unmaintainable.

### 4. Build the concept mapping table

For each vendor concept, record your concept, the transformation, and what is lost.

Hunt two specific things that pass every technical review:

**Semantic dissonance.** Two systems can agree perfectly on format and disagree completely on
meaning. One system's "well" is a single drilled hole; another's is several holes under one piece
of equipment. Both are valid; a field-by-field mapping between them is silently wrong. No schema
tool will find this — format mismatches fail loudly, semantic mismatches pass every check and
corrupt your counts. Find them by asking what the term means in *their* business process.

**Enumerations that partition differently.** If their status set and yours carve reality along
different lines, there is no total mapping — only a lossy one. Any time you reach for a default or
"other" bucket, that bucket is a capability gap and belongs in the capability report, not silently
in code.

Two rules carried from surface documentation, because they bite hardest here:

- Never carry a field's name or meaning from one vendor endpoint to another. Map per endpoint.
- A vendor term matching one of yours is the most dangerous kind of match — it suppresses the
  question "do these mean the same thing?" exactly when it needs asking.

### 5. Decide the shared-model question with arithmetic

Read `references/canonical-model-economics.md` before agreeing to build a canonical model.

The arithmetic: direct translation between every pair needs **N(N−1)** translators; going through a
common model needs **2N**. Two systems: 2 direct against 4 canonical. Three: 6 either way. Six: 30
against 12.

**The break-even is three.** Below three a canonical model is strictly more work. At three it is a
wash. Only above three does it pay — and it pays more the more message types each system publishes,
because the count multiplies. (The growth is quadratic, not exponential; the distinction matters
when someone justifies a large upfront model by invoking runaway growth that is not there.)

And the honest downside, which the endorsements omit: **the canonical model that tries to be the
enterprise data model is the one that fails.** The goal of a model that works equally well for
every application is not achievable — it either bloats to satisfy everyone or quietly favours
whichever system was loudest. The one change that makes it tractable is scope: model only the data
that actually crosses the wire, never the data inside the applications. Its real payoff is forcing
one name onto "account", "payer", "contact" — it is a semantics negotiation, not a technical
artifact, so sell it on shared vocabulary and replaceability rather than elegance.

Also weigh the permanent cost: two translations per message, forever, on every path. Check whether
any latency budget survives that, and carve out direct translation for the paths that do not.

### 6. Shape the boundary: filter inbound, enrich outbound

The correct shape is a matched pair — strip on the way in, add on the way out, keep the internal
model as small as it can be.

**The inbound filter is where field-level authorisation actually happens.** A packaged system
typically has no notion of who is asking and returns the whole record regardless: a payroll
interface answering "when did this person start" by also returning salary and national insurance
number. The vendor will not filter that; your filter is the only place it can happen. Document
which fields it suppresses and for whom.

**Enrichment belongs in your layer, and here is the test.** When the receiving system needs fields
the producer does not hold, there are four places to solve it and three push the problem into a
system you do not control. The decisive tell: if adding the lookup upstream changes what the
message *means* — "Doctor Visit" quietly becoming "Notify Insurance" — that location is wrong. An
event that acquires a recipient has become a command.

**Every enrichment is a synchronous dependency**, whatever transport expresses it. The enricher
cannot publish until its lookup returns, so each one adds its source's latency to the flow and caps
the flow's availability at that source's. Count the lookups on the critical path and add their
latencies — that is the flow's floor. For each, define what happens when it fails: fail the
message, emit partial, or park it. A lookup that fails leaves a message neither deliverable nor
discardable, and that state needs an owner.

### 7. Establish the invariants, and make them greppable

A boundary rule nobody can check is a boundary rule that will be broken during the next deadline.
State each as something a person or a script can verify:

- **No domain import from the integration package.** Any hit is a real dependency the architecture
  diagram does not show.
- **No vendor exception type outside the gateway.** Wrapping the vendor's method calls is the easy
  half; their libraries also throw their own exception types, and if those propagate, application
  code catches them and the claimed independence is an illusion. Grep for the vendor library's
  exception class names and error-code constants; any hit outside the gateway is the tell that the
  wrapper is fake.
- **Vendor-shaped messages exist only on one side.** Messages between an application and its own
  translator are *private*; only the translated message is *public*. This rule matters because the
  leak never happens by decision — it happens when somebody notices the pre-translation message is
  already on a channel and subscribes to it because the field they want is right there. Name which
  channels are public and which are private, prohibit subscription to private ones, and check
  periodically. Treat any consumer reading a vendor-shaped message directly as a defect, not a
  shortcut.

### 8. Make the gateway stubbable on day one

Define one gateway per external party, named for the party rather than the protocol, and **declare
its interface separately from the implementation that speaks the protocol.**

`references/layer-hardening-checklist.md` lists what the stub must be able to inflict and doubles as
the review checklist for an existing layer — read it when specifying the stub, or when auditing a
layer someone else built.

The second half is what teams skip and what actually matters here: you generally cannot exercise a
vendor freely. Sandboxes are unrepresentative or absent, calls may be metered, and the error paths
are exactly the ones you cannot trigger on demand. A separately-declared interface lets a stub take
the vendor's place — and the stub must reproduce the vendor's **error and timeout** behaviour, not
just its happy path, or it is a mock that proves nothing.

## Design output

```
# Anti-corruption layer design: <system>

## Stance
<what is absorbed, what is refused, and why translating beats conforming here>

## Stage decomposition
<per stage: level handled, inputs, outputs, what a change here does NOT touch>

## Concept mapping table
| Vendor concept | Our concept | Transformation | Lost in translation | Confidence |

## Unmappable
<enumerations with no total mapping; concepts with no counterpart — these go to
 the capability report, they are not code problems>

## Shared-model decision
<N, the arithmetic, the decision, and the paths carved out for direct translation>

## Boundary shape
<inbound filter and what it suppresses; outbound enrichment, its latency floor,
 and the failure behaviour of each lookup>

## Invariants
<each rule, and the exact command that checks it>

## Stub plan
<the gateway interface, and which vendor error and timeout behaviours the stub reproduces>
```

## Failure modes

| Tell | What is actually happening | Fix |
|---|---|---|
| Domain code imports the integration package | No real separation; the mapper does not exist | Introduce a mapper both sides are ignorant of |
| Vendor exception types reach callers | The wrapper is cosmetic | Catch and re-throw at the gateway; grep to verify |
| Mapping logic lives in domain objects | Mapping given a home it cannot have | Move to a mapper keyed by message type |
| A canonical model proposed for two systems | Arithmetic not applied | Direct translation until three |
| The shared model keeps growing | It is being extended to internal data | Re-scope to what crosses the wire |
| An enum mapping has an "other" bucket | The partitions differ; no total mapping exists | Escalate as a capability gap |
| An event acquired a recipient | Enrichment pushed upstream turned it into a command | Own enrichment in your layer |
| A consumer subscribed to a pre-translation channel | Private/public distinction never stated | Name the channels; treat as a defect |
| Every small change costs two edits | Near-domain and near-wire split without generation | Generate the near-domain mapper |
| The chain is elegant and slow | Each hop costs a full marshal/unmarshal round trip | Collapse stages on hot paths deliberately |

## A note on latency

A layer decomposed into many small, individually elegant stages pays for its flexibility with a
throughput cost proportional to the number of hops, because each hop costs a full conversion out of
and back into an internal format. That cost is invisible in a diagram where every arrow looks free.
Decompose for clarity, then measure, then deliberately collapse stages on the paths that cannot
afford them — and write down which ones you collapsed and why, so the next person does not
"restore" them.

## Related work

- Whether to translate at all, versus conform or ask for an open contract → `map-subdomains-and-boundaries`
- What the vendor's surface actually is → `document-vendor-api-surface`
- Where the gaps are unmappable rather than awkward → `report-vendor-capability-gaps`
- Event and webhook delivery guarantees → `pin-down-vendor-event-delivery`
- Making the stub reproduce real misbehaviour → `probe-vendor-contract-empirically`
