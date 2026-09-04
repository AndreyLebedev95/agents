---
name: document-vendor-api-surface
description: Produces the reference document for a third-party or purchased core system's API — the resource and method inventory, the identifier contract, field semantics, the auth model, error and retry semantics, rate limits, and the call ordering the vendor never documents. Covers reading a vendor's API shape as evidence of its internal model, the four states of a field and where they silently collapse, what standard method names do and do not guarantee, identifier stability and reuse, what a signature or shared secret actually proves, and marking every row as contracted, observed or unknown so nobody builds on an accident. Use when starting an integration against a bought core, when writing or reviewing a vendor API reference, when onboarding onto an existing integration nobody documented, or when a vendor hands over a PDF and a sandbox and someone has to turn it into something engineers can build against — even when the ask is only "how does their API work". For what the core cannot do at all use report-vendor-capability-gaps; for getting bulk data out correctly use plan-vendor-data-extraction; for the webhook or event side use pin-down-vendor-event-delivery; for testing whether the vendor's claims are true use probe-vendor-contract-empirically.
---

# Documenting a vendor's API surface

You are writing the document engineers will build against for a system you cannot change. The
job is not to summarise the vendor's documentation. It is to separate three things that the
vendor's documentation deliberately blurs:

- what the vendor **contracts** to keep true,
- what is currently **observed** to be true but is not promised,
- what nobody has established at all.

That distinction is the entire value of the artifact. A reference that does not make it is worse
than no reference, because it launders the vendor's marketing into something your team treats as
a guarantee.

## The governing insight

A purchased system's API is a projection of its internal data model, not a contract someone sat
down and designed. The schema, the file formats and the API all descend from the same internal
model. Read backwards, that gives you an analytic tool: **the oddities of a vendor's API are
evidence about its internals.** A field that must be sent twice, an entity that cannot exist
without a parent, a status with no setter — these are internal constraints leaking outward.

Two consequences shape everything below. Awkwardness in the API predicts what the core cannot
represent internally. And because the API mirrors the internal model, a vendor's internal
refactor tends to surface as an interface change no matter how loudly they call it internal.

## Procedure

### 1. Inventory the surface, and check whether it factors

List every operation. Then check whether the method list factors cleanly into *method × resource*
(a small set of verbs applied uniformly across resources) or whether it is a flat list of
special-purpose operations.

This matters more than it looks. A factoring surface is cheap to document and predictable to
extend. A flat list means each operation carries its own semantics, documentation cost scales
with the operation count, and there is no basis for inferring anything about an operation you
have not read. Say which shape you are dealing with in the first paragraph of the reference.

Note separately every operation that does *not* fit the standard verbs. Those are the places the
vendor's own designers found the model could not express the operation — the most informative
part of the surface. Record them here; `report-vendor-capability-gaps` mines them further.

### 2. Extract the identifier contract before anything else

Everything downstream — your mapping table, your reconciliation, your idempotence — rests on
identifiers. Get this wrong and the rest of the reference is built on sand.

Read `references/identifier-and-field-contract.md` for the full interrogation. The five parts you
must land:

1. **Format**, and whether a numeric-looking id is actually a token. An id that looks numeric will
   be parsed as arithmetic somewhere, losing leading zeros or overflowing.
2. **Scope of uniqueness** — ids are unique within a scope, and the scope is rarely stated.
3. **Mutability of encoded parts.** Decompose the id and mark each part mutable or immutable. Any
   part that encodes a mutable fact is scheduled renumbering: when the fact changes, the id
   changes, and your mapping table needs a second natural key that does not.
4. **Reuse after deletion.** Ask explicitly. The answer is more often yes than teams expect.
5. **Error distinguishability** — if a malformed id and a deleted id return the same error, you
   cannot triage, and every "not found" becomes an investigation.

A deep hierarchy makes a leaf identifier unusable on its own: if addressing a record requires the
whole ancestor path, your storage must carry the path, not the leaf.

### 3. Build the field-semantics table

This is where silent data loss lives. For every field you will read or write, record:

- **Which of four states it can be in** — a value, empty, null, or absent. These are four, not two,
  and the collapse between them usually happens inside *your* deserializer, invisible in the
  vendor's traffic. Most silent loss on read and most unintended overwrites on write trace here.
- **Whether zero is representable.** If the zero value is overloaded to mean "unset", a legitimate
  zero cannot be expressed at all.
- **Whether it is output-only.** Output-only fields swallow writes and return success — the write
  is accepted, ignored, and reported as fine.
- **Its unit.** Unitless numeric fields at a hand-off seam are the classic loss mechanism; a number
  with no unit in the contract is a number two teams will interpret differently.
- **Whether an example format in the docs is being treated as a parse contract.** A string field
  with an example format in its documentation is an unversioned parse contract: you will write a
  parser against the example, and the vendor never promised the example.
- **Whether the name is deliberately generic.** A conspicuously generic field name is usually
  reserved room the vendor intends to use later.

Two rules that save more time than anything else in this section:

**Never carry a field's name or meaning from one vendor endpoint to another.** The same name on
two endpoints is not evidence of the same meaning. Map per endpoint.

**A vendor term that matches one of yours is the most dangerous kind of match.** An exact name
collision suppresses the question "do these mean the same thing?" precisely when it most needs
asking. Treat matching names as false friends until someone has proven the semantics identical.

### 4. Establish what the methods actually guarantee

A method's name tells you nothing. Test and record, per operation:

- **Idempotence.** Does retrying it produce the same state? Note that a conventional delete is
  deliberately *not* idempotent — a retried delete reports a failure for work that already
  succeeded, which is exactly what a network retry produces.
- **Atomicity.** Does a partial failure leave partial state?
- **Read-your-writes.** Can you immediately read back what you wrote? Read the method names for
  hints — asynchrony in the naming usually means no.
- **Side effects.** A name says nothing about side effects, and side effects are what make an
  operation unsafe to retry.
- **Unknown-field handling.** If an unknown field name is ignored rather than rejected, a
  misspelled update returns success and changes nothing. Assert on read-back, never on status code.
- **Whole-resource writes.** A full-resource write erases every field the client does not know
  about — including fields the vendor added after your data structures were generated. And a
  replace cannot distinguish create from update, so success tells you nothing about which happened.
- **Field masks.** If the vendor infers the mask from the payload rather than taking it explicitly,
  clearing a field is indistinguishable from not touching it.

### 5. Record required call ordering

A vendor documents each call in isolation and almost never documents the required order, the
states each call assumes, or which call must have succeeded first. That ordering is a real part
of the contract, discovered only by failure — and it is what makes vendor release notes dangerous,
because a reordering they consider internal breaks every caller.

Add an explicit ordering column: for each operation, its preconditions, the calls that must
precede it, and whether that ordering is documented or was discovered by the team. The second
category is the one to flag; it is unprotected by any promise.

Related: data the vendor split onto its own endpoint cannot be set in the same call as its parent,
so "create a customer with an address" may be two calls with a window in between where the record
is legal to the vendor and invalid to you.

### 6. Document the auth model

Read `references/auth-and-error-semantics.md`. The points that most often go unrecorded:

- **What the credential proves.** A shared secret or HMAC delivers origin and integrity but never
  non-repudiation — the holder of the secret could have manufactured the request, and both ends
  hold it. The decisive question is key provenance, not algorithm name.
- **What the signature covers.** A signature covers a declared list of components, as bytes. It
  does not cover the request's meaning, and anything outside the declared list is unprotected.
- **Rotation shape.** One key per identity means rotation is a hard cutover with no overlap window
  — an operational fact that has to be designed for long before the rotation date.
- **Scope and expiry**, and whether the credential's visibility is bounded by what it can see.

### 7. Document error semantics and retriability

Group the vendor's errors into three buckets: safely retriable, definitely not retriable, and the
middle bucket — *you do not know whether the work happened*. The middle bucket is the one that
matters, and it is the one vendor documentation never labels.

Two things to record explicitly:

- **Errors that lie.** If the vendor returns one error class for conditions you must distinguish,
  you cannot build a correct retry policy, and you must say so rather than guessing.
- **Generic error responses.** If a caller's malformed input and a genuine vendor fault return the
  same response, a user's typo can trip protective machinery meant for vendor outages. Note where
  application failure and system failure are indistinguishable.

Never parse a prose error message into a contract. Prose is not an interface; parsing it
manufactures a contract the vendor never made and will change without notice.

### 8. Mark every row

Go through the finished reference and mark each row **contracted**, **observed**, or **unknown**.

The reason this matters: once a service is live, its implementation *is* its specification,
including behaviour nobody designed. An unvalidated field can never be validated later without
breaking someone. So observed behaviour is real and worth recording — but it is not a promise, and
the difference decides what your team is allowed to depend on.

Prefer "unknown" to a guess. An honest gap prompts someone to go find out; a confident guess does
not.

## Output format

Produce the reference with these sections. Keep the marking column throughout.

```
# <System> API reference

## Shape and scope
<factoring or flat; what this reference covers; what it deliberately excludes>

## Identifier contract
<the five parts, per identifier type>

## Resources and operations
<per operation: purpose, preconditions, required predecessors, idempotence,
 atomicity, side effects, marking>

## Field semantics
<per field: type, four-state behaviour, zero handling, output-only, unit,
 format contract status, marking>

## Required call ordering
<sequences, with documented-vs-discovered marked>

## Auth model
<credential type, what it proves, what the signature covers, scope, expiry,
 rotation shape>

## Error semantics and retry
<the three buckets, the errors that lie, rate limits and their dimensions>

## Open questions
<every "unknown" row, gathered, with who can answer it>
```

The **Open questions** section is not filler. It is the part that gets acted on, and gathering the
unknowns in one place is what turns the reference from a document into a piece of work with a
next step.

## Failure modes

| Tell | What is actually happening | Fix |
|---|---|---|
| Docs describe each call in isolation; nobody can state preconditions | Ordering is real contract and is never written down | Add the ordering column, mark documented vs discovered |
| A no-op update returns success | Unknown field names are ignored, not rejected | Assert on read-back, not on status code |
| Writes silently disappear | Output-only fields swallow writes and return success | Mark output-only fields in the field table |
| Fields vanish after an update | A full-resource write erased fields the client did not know about | Use field masks; never write back a structure you generated |
| An integration built in a low-code tool cannot be reviewed | The semantics live in property fields no diagram shows | Export the configuration to text before writing the reference |
| Nobody can say what the vendor guarantees | Documentation claims were recorded as contract | Apply the contracted/observed/unknown marking |
| "Their API is fine, it's just badly documented" | The API's awkwardness is internal constraint leaking | Treat each oddity as a hypothesis about a limitation |

## A caution on bespoke endpoints

When a vendor offers to build an endpoint specifically for you, the instinct is to treat it as a
win. It is the opposite as far as this document is concerned: a bespoke endpoint is less stable
than the vendor's public one. It has fewer other consumers to protect it, less test coverage, and
no place in the vendor's compatibility policy. Record it as higher risk, not lower, and say so
explicitly — this is the single finding most likely to be argued with.

## Related work

- What the core **cannot** do, as a constraint on specification → `report-vendor-capability-gaps`
- Getting bulk data out correctly → `plan-vendor-data-extraction`
- Event, webhook and queue guarantees → `pin-down-vendor-event-delivery`
- Verifying any claim in this reference → `probe-vendor-contract-empirically`
- Building the translation layer on top → `design-vendor-anticorruption-layer`
- Assessing an announced vendor change → `assess-vendor-version-change`
