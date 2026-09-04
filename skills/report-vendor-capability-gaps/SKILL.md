---
name: report-vendor-capability-gaps
description: Produces the integration capability report for a purchased or third-party core — what it cannot do, on what evidence, at what workaround cost, and what must be built on your side regardless of what the vendor promises. Covers mining the vendor's own non-standard operations as its register of what its model cannot express, reading a workaround inventory as an expressiveness gap register, why a chosen API pattern defines a set of impossibilities and not just a set of features, the limits that appear as silence rather than as errors, and the boundary failure modes — slow responses, drained pools, unbounded results, uncancellable work — that belong in the report because they constrain what can be promised. Use before requirements are written against a bought core, when scoping or estimating an integration, when a proposed requirement may not be supportable, during a build-versus-configure argument, or when a vendor demo has just made everything look possible — even when the ask is only "can the core do this". For documenting what the API does offer use document-vendor-api-surface; for the translation layer use design-vendor-anticorruption-layer; for verifying vendor claims empirically use probe-vendor-contract-empirically; for whether to buy or where a boundary belongs use map-subdomains-and-boundaries.
---

# Reporting what a bought core cannot do

This report exists to be read **before** requirements are finalised, because a purchased core's
limits decide what can be specified at all. Written afterwards it is an autopsy; written
beforehand it is the most valuable document in the project.

The discipline is unnatural in one specific way. Vendor documentation, vendor demos and vendor
sales conversations are all organised around what the system *can* do. The gaps do not appear as
errors or as missing pages — they appear as **silence**. Nothing in the material says "you cannot
ask this question"; the question simply has no page. So the method below is mostly about finding
evidence of absence, which you cannot do by reading forward through the docs.

## What counts as a gap

Four kinds, and teams reliably find only the first:

1. **Operations not exposed** — the thing you want to do has no call.
2. **Questions not answerable** — the data exists but cannot be queried, filtered or aggregated
   the way you need.
3. **States not representable** — your domain has a distinction the core's model cannot hold.
4. **Guarantees not made** — the operation exists but promises nothing you can build on.

The fourth is the most commonly missed and the most expensive. An operation that works in the
demo and guarantees nothing is not a capability; it is a capability-shaped risk.

## Procedure

### 1. Read the vendor's non-standard operations first

Before anything else, list every operation that does not fit the system's own standard verb set —
the specially named actions, the "execute", "process", "perform" endpoints, the operations whose
names contain a preposition.

This list is the vendor's own register of what its model could not express. Their designers hit
the same wall you are about to hit, and each of these operations is where they gave up on the
model and bolted something on. Two things follow:

- It is the fastest route to the shape of the core's real limits.
- **None of the standard-method guarantees carry over to any of them.** Idempotence, atomicity,
  error semantics, filterability — none can be assumed for an operation outside the standard set.

An operation name containing a preposition usually marks a combination the model cannot compose:
the vendor needed a relationship the resource layout does not support and expressed it in the
verb instead.

Treat a single generic "do an action" endpoint as the extreme case. It does not remove the
limitation; it moves the entire contract into an undocumented payload where nothing can be
validated, versioned or discovered.

### 2. Collect the workaround inventory

Every manoeuvre the team has already invented against this core is a gap that has already been
found and not written down. Sweep for them: the double-write, the sleep-then-poll, the
reconciliation job, the field being used for something other than its name, the spreadsheet
someone maintains, the nightly script nobody owns.

Each one is an entry in the expressiveness gap register, and each carries its own cost that is
currently invisible because it is spread across people rather than shown in a budget.

### 3. Establish what the chosen pattern makes impossible

A system's design pattern defines a set of impossibilities, not just a set of features. This is
the step that turns a features list into a limits list, and it is done by asking what the shape
forbids rather than what it offers.

The recurring cases worth checking explicitly:

- **A remote-procedure-only core leaves nowhere to put the translation layer except your own
  code.** There is no intermediate stage where mismatch can be absorbed, so the entire
  anti-corruption burden lands inside your application and cannot be deployed separately.
- **Direct database access is an interface the vendor never agreed to.** A packaged application
  generally will not run against any schema but its own, and the vendor reserves the right to
  change that schema at every release. Reading their tables is an unversioned, unannounced
  interface that will break on an upgrade they consider non-breaking. Record it as a capability
  with no versioning guarantee, and force the question of whether the schema is contracted before
  anything is built on it.
- **One business operation is many calls.** A packaged system's API is usually its internal API,
  so an operation that is one action to the business is several calls to the core, with partial
  states in between and no transaction spanning them.

### 4. Enumerate the unaddressable and the unanswerable

Work through these explicitly; each has produced a late, expensive surprise often enough to be
worth a checklist. `references/limit-discovery-questions.md` holds the full interrogation list —
read it here and again at step 5, since these are the limits that produce no error message and no
missing page, so reading the documentation forward will never surface them:

- **Sub-objects with no identifier** cannot be referenced, tracked or changed independently.
- **Data readable but not writable** — including records that entered under looser validation
  rules and can now be read but never updated, because saving them re-runs validation they fail.
- **Fields you cannot filter on.** Filters are hermetic: you cannot filter on anything the
  resource does not physically carry, no matter how derivable the value is.
- **History the revision granularity cannot answer.** What the core versions decides which
  questions about the past are answerable at all.
- **Map or dictionary keys that cannot be removed**, only set to null.
- **Stateless operations that leave no record**, so the core cannot tell you afterwards what it did.
- **Anything you cannot address individually** must be rewritten whole, which means concurrent
  writers lose each other's changes.

### 5. Find the semantic gaps

These are the gaps that survive every technical review because everything appears to map.

**Semantic dissonance** — the same word meaning different things on each side — is not a format
problem, and no schema tooling will find it. Two systems can agree perfectly on the shape of a
message and disagree completely on what it means. Hunt these by asking what the vendor's term
means in *their* business process, not by comparing field types.

**Enumerations that partition the space differently have no total mapping.** If their status set
and yours carve reality along different lines, there is no correct translation — only a lossy
one. When you find yourself wanting a default or "other" bucket in a mapping, that bucket is a
capability gap, and it belongs in this report rather than being quietly absorbed in code.

### 6. Cost each gap honestly

Costs that are routinely left out:

- **The asynchronous tax.** Replacing a synchronous call with a messaged interaction is not
  one-for-one: a single call becomes a request message, a request channel, a reply message, a
  reply channel, correlation, and the handling for a reply that never arrives. Cost per artifact,
  not per call.
- **Middleware bridging.** If the vendor offers a queue or topic rather than an HTTP interface,
  establish whether it is the same product you already run. Two messaging systems generally do not
  interoperate even when both claim the same specification, because the specification constrains
  the API rather than the wire format. Bridging is built as adapter pairs, one per channel, so the
  effort scales with channel count.
- **No bulk path.** Event streams are for the delta, not the initial load. If there is no bulk
  export distinct from the event feed, cold starts and backfills have no supported route — a hard
  constraint, not an inconvenience.
- **Bespoke endpoints.** An endpoint the vendor builds specially for you is *less* stable than
  their public one: fewer other consumers protecting it, less test coverage, no place in the
  compatibility policy. Price it as higher risk.

### 7. Add the failure-mode section

The report must say what happens to *us* when the core misbehaves, because that determines what
can honestly be promised to users. Read `references/boundary-failure-modes.md` and pull the
mechanisms that apply.

The framing that matters most: **the vendor outage is the easy case.** A refused connection
returns in milliseconds and every language surfaces it clearly, so programmers handle it. A
vendor that is merely *slow* blocks the calling thread, and a blocked thread processes nothing
else, so your capacity falls until the whole service is down. Rank the risks accordingly — a
report whose risk section only covers outages has covered the failure that will not hurt you.

Three rules to apply while writing this section:

- **Safety is not composable.** Two calls that each meet the latency budget will not both meet
  it. A per-call vendor SLA is never sufficient evidence for a composite operation.
- **Abandoning a call does not cancel the work.** Your timeout ends your wait; the far side never
  learns you left, and it continues, completes, and may change state you have stopped watching for.
- **"Astronomically unlikely" is an argument about frequency, not impossibility.** It does not
  remove an entry from the register; it sets its priority.

### 8. Write each entry as a constraint on specification

Every row states: the gap, the evidence, the confidence, the workaround, the workaround's cost,
and — the point of the whole document — **what this forbids anyone from specifying.**

That last column is what makes the report usable by the person writing requirements. Without it
the report is a list of technical grumbles; with it, it is a boundary on the solution space.

## Output format

```
# <System> integration capability report

## Summary for specification
<the three to five limits that most constrain what can be built; one line each>

## Constraint register
| # | Gap | Kind | Evidence | Confidence | Workaround | Cost | Forbids specifying |

## Semantic gaps
<terms that do not survive the crossing; enumerations with no total mapping>

## Failure modes at this boundary
<what happens to us when the core is slow, wrong, or partially available,
 and the protection that must exist on our side regardless of vendor promises>

## Costs not on anyone's budget
<asynchronous tax, bridging, absent bulk path, workaround labour>

## Open questions blocking specification
<with owner and date asked>
```

The **Summary for specification** goes first because the audience for the first page is whoever
is writing requirements, and they may read nothing else.

## Failure modes of this report

| Tell | What is actually happening | Fix |
|---|---|---|
| The report lists features, not limits | The docs were read forward; gaps appear as silence | Mine non-standard operations and workarounds |
| "The core supports it" with no evidence | A demo was mistaken for a capability | Require evidence and confidence on every row |
| Requirements were written before the report | The sequencing that gives the role its value was skipped | The report precedes specification sign-off |
| A vendor SLA is quoted as proof of safety | Composability assumed | Apply the composition arithmetic |
| The risk section covers only outages | Slow failure not modelled | Add slow-response mechanisms and their tells |
| The integration is one line in the estimate | Asynchronous tax and bridging invisible | Cost per artifact |
| Nobody can list the integration points | The inventory does not exist | That absence is the first finding |

## Related work

- What the API **does** offer, in reference form → `document-vendor-api-surface`
- Designing the layer that absorbs these gaps → `design-vendor-anticorruption-layer`
- Establishing empirically whether a claimed capability is real → `probe-vendor-contract-empirically`
- Event and webhook guarantees specifically → `pin-down-vendor-event-delivery`
- Bulk read limits specifically → `plan-vendor-data-extraction`
- Whether to buy this at all, or which boundary owns it → `map-subdomains-and-boundaries`
