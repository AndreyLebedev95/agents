# What counts as a breaking change

Read at steps 2-4. This is the audit list to run a proposed vendor change against, and the
classification of the three vendor versioning strategies.

Contents: [the always-safe forms](#the-always-safe-forms) · [the breaking forms](#the-breaking-forms) ·
[the disputed middle](#the-disputed-middle) · [the six agreements](#the-six-agreements) ·
[three vendor strategies](#three-vendor-strategies) · [questions for the vendor](#questions-for-the-vendor)

## The always-safe forms

A short list, and it is short for a reason. These break a consumer only if the consumer is doing
something already unwise:

- Adding a **wholly new endpoint** that nothing calls yet.
- **Relaxing** a validation rule so previously-rejected input is now accepted.
- Accepting a **new optional** request field with a default preserving existing behaviour.
- **Performance improvement** that does not change results or ordering.

Everything else deserves examination.

## The breaking forms

These break consumers regardless of how the vendor classifies them:

1. **Removing** a field, endpoint, or enum value.
2. **Renaming** anything a consumer references.
3. **Changing a type** — a number becoming a string, a scalar becoming an object, a value becoming
   a list.
4. **Making an optional request field required.**
5. **Tightening validation** so previously-accepted input is now rejected. This is the one most
   often shipped as a "fix", and it breaks integrations that have been sending the same data for
   years.
6. **Changing a default value.**
7. **Changing the meaning** of an existing field while keeping its shape.
8. **Changing error codes or the conditions** that produce them.
9. **Changing ordering** where a consumer relied on it — whether or not it was ever promised.

## The disputed middle

The commercially interesting part. Every one of these sits in most vendors' "compatible" bucket,
and every one breaks real consumers. These are what your assessment exists to catch.

**Adding a field to an existing resource.** Inflates every response, multiplied by page size on
list calls. Breaks fixed buffers, strict schema validators that reject unknown fields, fixed-width
staging tables, and downstream file layouts.

**Adding a new enum value to an existing field.** Arrives at a consumer whose mapping has no case
for it. If your translation layer has a default or "other" bucket, it will silently swallow this;
if it does not, it will throw.

**Adding a whole new resource type.** Usually harmless, but changes discovery responses and any
logic that enumerates types.

**A bug fix.** Three sub-cases, all quiet:
- A call that wrongly succeeded now correctly errors — code that ran for years starts failing on
  inputs it always sent.
- A calculation is corrected and the numbers change — your reconciliation and reports disagree with
  the vendor from that release onward.
- A default is changed to what it "should always have been".

**Latency change.** 100 ms to 150 ms is invisible. 100 ms to 10 seconds blows every timeout,
exhausts connection pools, and can force a change of programming model — all with no field altered.

**Result stability.** Where a call is backed by a changing computation, the same request begins
returning different answers, legitimately and unannounced.

**A newly imposed constraint** inside an existing version — a rate limit, content policy, or
approval step. Note the enforcement route: rejecting the call fails loudly at the call site;
accepting and deferring the work fails later, somewhere else, at whatever reads back what you wrote.

## The six agreements

An interface is a layered stack of agreements, and a breaking change is any unilateral break from
one of them. Naming the layer is what turns "it broke" into a diagnosis:

1. **Connection handshaking and duration** — how a connection is established and how long it lives.
2. **Request framing** — where one message ends and the next begins.
3. **Content encoding** — compression, character set, transfer encoding.
4. **Message syntax** — the structure of the payload.
5. **Message semantics** — what the fields mean.
6. **Authentication and authorisation** — who may do what.

Choosing a common transport settles some of these and *not* the ones that matter most. "This
interface accepts HTTP" says almost nothing about layers 4, 5 and 6, which is where the expensive
breaks live.

Where machine-readable specifications exist, diff old against new mechanically rather than reading
release notes. Release notes describe what the vendor *meant* to change.

## Three vendor strategies

Classify the vendor from its version labels and release history. Each hands you a different
standing cost, and that cost belongs in the capability report as a recurring commitment.

**Perpetual stability.** Versions are frozen and numbered; every compatible change is injected into
the version you are already on. *Your integration survives indefinitely but drifts underneath you.*
The risk is silent behaviour change, not breakage — so your defence is behavioural monitoring and
metadata diffing, not upgrade planning.

**Agile instability.** Exactly one current and one preview version exist at a time. *You are
committed to a continuous upgrade cadence*, and falling behind is not an option the vendor
supports. Your defence is automation: contract tests that run against the preview version
continuously.

**Semantic versioning.** Versions are labelled by the vendor's own compatibility policy. *Your risk
is trusting the label.* A minor bump carries every item in the disputed middle above. Your defence
is auditing each release against this checklist regardless of the number.

For whichever applies: get the **deprecation window** in writing, and count how many releases fit
inside it. A ninety-day window against a two-week release cadence is a very different commitment
from a ninety-day window against an annual one.

## Questions for the vendor

Ask in writing; record answers with dates.

1. What is your written definition of a backward-compatible change? May we have the list?
2. Does that list include adding fields to existing resources? Adding enum values?
3. How are bug fixes classified, and are corrected calculations announced?
4. Do you commit to any latency envelope, and does a change to it constitute a breaking change?
5. Is the result of any call backed by a computation that may change?
6. What is the deprecation notice period, and has it ever been exercised? Give an example.
7. How many releases occur inside that notice period?
8. Can we pin a version? For how long is a pinned version supported?
9. When a new constraint is introduced, does it reject at the call site or defer the failure?
10. Is there a machine-readable specification we can diff between releases?
11. Is there a preview or staging version we can test against before release?
12. What changed in the last twelve months that was not in the release notes?

Question 12 is the useful one. The answer, or the inability to answer, tells you what the
compatibility policy is actually worth.
