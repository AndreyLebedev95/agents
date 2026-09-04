---
name: assess-vendor-version-change
description: Assesses what a third-party or purchased system's version change, patch or deprecation actually breaks, and plans the migration and the mixed-version window. Covers the absence of any industry definition of backward compatible, why additive changes are the vendor's definition of safe and the consumer's commonest break, the bug fix that is a breaking change with no version bump, latency and semantic drift that ships inside a version because it changes no field, why pinning buys a point in time rather than a feature set, detecting undeclared changes by scheduled metadata diffing, and the mixed-version test almost nobody runs. Use when a vendor announces a release, deprecation or sunset, when deciding which version to pin, when a supposedly compatible patch broke something, when negotiating a notice period, when planning an upgrade window, or when a payload changed shape without a version bump — even when the ask is only "they say it's backwards compatible, are we fine". For documenting the surface use document-vendor-api-surface; for testing vendor behaviour use probe-vendor-contract-empirically; for what the core cannot do use report-vendor-capability-gaps.
---

# Assessing a vendor's version change

Someone has told you a change is coming and that it is compatible. The word "compatible" is doing
enormous work in that sentence and it is not load-bearing.

## Start here: there is no industry definition of backward compatible

No single answer exists. What counts as a compatible change is a **policy each provider sets**
according to what its users tolerate, and several mutually incompatible policies are all
defensible. A provider serving banks may freeze every version and require opt-in for anything new.
One serving startups may inject new behaviour continuously and call all of it compatible.

So "we maintain backward compatibility" asserts nothing until you have their definition. **Get it
in writing, as a list of change classes they consider compatible.** Everything else in this skill
is an audit against that list — and if they cannot produce one, that absence is the headline
finding of your assessment.

## The changes that look safe and are not

Work through these explicitly. Each sits inside almost every vendor's "compatible" bucket and each
breaks real consumers.

### Additive changes — the vendor's definition of safe, the consumer's commonest break

**Adding a field** to an existing resource, or **adding a whole new resource type**, is compatible
by nearly every policy. Both break consumers:

- New fields inflate every response, **multiplied by page size on list calls**. A client with a
  fixed buffer, a strict schema validator, a fixed-width staging table, or a downstream file layout
  fails on data it never asked for.
- A strict parser configured to reject unknown fields — a security-conscious default — fails
  immediately.
- A new enum value in an existing field arrives at a consumer whose mapping has no case for it.

Ask specifically: *does your compatible bucket include adding fields and enum values? What is the
largest response we should size for?*

### The bug fix delivered without a version bump

Vendors treat bug fixes as compatible, reasoning that nobody depends on a crash. That covers only
the loud case. Three quieter ones break you with no notice:

- **A call that wrongly succeeded starts failing.** It returned a nonsensical result for two years;
  now it correctly returns an error, and integration code that ran fine begins failing validation
  on inputs it always sent.
- **A calculation is corrected and the numbers change.** Your reconciliation, your reports and
  possibly your ledger disagree with the vendor from that release onward, with no field having
  changed shape.
- **A default changes** to what it "should always have been."

None of these produce a version bump under most policies. They are only findable by behavioural
testing or by noticing your own numbers moved.

### Drift that ships inside a version because it changes no field

Shape-identical changes are almost always classed as compatible, and three of them are severe:

- **Latency.** 100 ms becoming 150 ms is invisible; 100 ms becoming 10 seconds justifies changing
  your programming model. A "compatible" release can blow every timeout you set, exhaust a
  connection pool, and force you from synchronous to asynchronous.
- **Result stability.** Where a call is backed by a changing computation, the same request starts
  returning different answers — legitimately, and without notice.
- **Semantics.** The field is the same, its meaning is not.

Latency is the one to raise explicitly in the assessment, because it is the one that turns a
compatible release into an outage and nobody's compatibility policy covers it.

### A newly imposed constraint breaks you somewhere else

When a vendor introduces a restriction inside an existing version — a rate limit, a content policy,
a new approval step — it has two enforcement routes with different failure locations:

- **Reject the call.** Immediate error at the call site. Loud, easy to diagnose.
- **Accept the call, defer the work.** Success at the call site and failure *later*, at whatever
  step reads back what you just wrote.

The second is the dangerous one, because the symptom appears in an unrelated component and the
investigation starts in the wrong place. When assessing a new constraint, always ask which
enforcement route it uses.

## Reading the version number

**A semantic version number reports the vendor's compatibility policy, not an objective property.**
Major means what *their policy* calls incompatible; minor, what they call a compatible feature
change; patch, what they call a compatible fix. So everything in the section above rides in on a
minor bump — a new field, a new resource type, a tightened validation rule, a corrected
calculation, a tenfold latency change.

**Pinning buys a point in time, not a feature set.** Every chronological scheme has the same hard
property: a version is a snapshot of the whole interface at one instant, so pinning means accepting
every change up to that instant and none after. **You cannot cherry-pick** — hold older behaviour
while taking a fix or field added later. This is the exact shape of the argument you will have with
the vendor when you need one correction from a later version, so know it going in.

Identify which of three strategies the vendor runs, because each sets a different standing cost on
your side. `references/compatibility-checklist.md` has the classification and what each one bills
you. Put that recurring cost in the integration capability report — an upgrade cadence is a
permanent commitment of your team's time, and it belongs in a budget rather than in a surprise.

## Procedure

1. **Obtain the vendor's written compatibility definition.** No definition is itself the finding.
2. **Classify the announced change** against `references/compatibility-checklist.md`, including the
   classes the vendor considers safe.
3. **Locate the change on the stack of agreements** an interface actually is — connection handling,
   request framing, content encoding, message syntax, message semantics, and authentication. Saying
   "it accepts HTTP" settles very little; identify which layer is moving and whether the break is
   unilateral.
4. **Check for drift** that changes no field: latency, result stability, semantics.
5. **Determine the enforcement route** for any new constraint — immediate rejection, or deferred
   failure elsewhere.
6. **Test, do not reason.** Run your own contract tests against their new version before agreeing
   it is compatible. Reasoning about compatibility from a changelog has a poor record; see
   `probe-vendor-contract-empirically`.
7. **Plan the mixed-version window** — see below. It always exists.
8. **Set up detection** for undeclared changes, so the next one is not discovered by an incident.
9. **Compute the aggregate change rate**, not this one change's cost.

## The mixed-version window always exists

A clean cutover is not merely hard to organise — **it is impossible in principle.** Even if every
component could switch at the same instant, every channel would first have to be drained of
in-flight messages in the old format. Some rarely-used consumers never convert at all.

So both versions coexist for a window, and the window is a thing to design rather than to endure.
Read `references/mixed-version-operation.md`. The essentials:

- Put a **format version in the messages themselves** — the version of the format, not of the
  application. Its purpose is debuggability rather than automatic bridging.
- **Run the mixed-version test almost nobody runs:** create entities through the new path and read
  them back through the old one. This is where the failures actually are, and it is skipped because
  both paths pass their own tests.
- For schema change, **expand then contract**: apply only additive changes before the code rollout,
  where the criterion is that nothing added in this phase may be used by the running version. Add
  shims in both directions for anything being split or merged. Clean up only after no old instances
  remain.
- For a migration too slow for a deployment window, **trickle then batch**: deploy code that reads
  both shapes first, convert each record as it is touched, then batch-migrate the cold remainder
  later — safely, because no old instances remain by then.

One caution that recurs on long-lived systems: **a store that has been in production for years
holds records the current application could not possibly create.** Users predating a required
field, accounts holding nulls where the current code marks the field mandatory. A migration that
assumes every record is producible by today's code will fail on the oldest and most sensitive data.
Test the migration against the *oldest* records you have, not a fresh sample.

## Detecting the changes you are not told about

The hardest part of vendor management is learning that something changed without being told. There
is a working answer: **schedule a metadata extraction and diff it.**

1. Find the vendor's metadata surface — a schema or interface description document, a describe or
   reflection endpoint, a system catalogue, or a published field dictionary.
2. Extract it on a schedule and store each extraction as a versioned snapshot.
3. Diff consecutive snapshots and alert on any change.

The extraction points usually already exist for other reasons, so this is cheap. And it produces
something valuable beyond the alert: **a diff that never appeared in a vendor notification is
evidence their deprecation policy is not operating**, which is exactly what you need when
renegotiating a notice period. Argue that case with dated diffs rather than with impressions.

## Computing the real change rate

Change rate is the quantity people forget to compute. A partner that revises its format once every
couple of years is individually harmless — but a few dozen such partners produce a change every
month or week. **The maintenance load is set by the aggregate, not by any one vendor's behaviour.**

Multiply the number of sources by each source's change frequency. Build the integration to absorb a
steady stream of format changes rather than occasional ones, and give each source its own
translator so one vendor's change cannot touch another's path.

Before assuming you can escape this by mandating a format: check whether your commercial position
actually allows it. If the deal promised the vendor minimal change on their side, it does not.

## Output format

```
# Change impact assessment: <system> <version/change>

## Verdict
<safe as claimed | breaking despite the claim | unknown until tested>

## The vendor's compatibility definition
<quoted, with date and source — or "none provided", which is the finding>

## Classified changes
| Change | Vendor's class | Our class | Mechanism of breakage | Evidence |

## Drift check
| Latency | Result stability | Semantics |

## Blast radius
<what breaks, where, and whether it fails at the call site or somewhere else>

## Migration plan
<expand/contract or trickle/batch; the mixed-version window and its duration;
 the mixed-version test result>

## Detection
<metadata diffing in place; what it would have caught>

## Negotiation position
<notice period, evidence from past undeclared changes, what to demand>
```

## Failure modes

| Tell | What is actually happening | Fix |
|---|---|---|
| "It's backwards compatible" accepted at face value | No shared definition exists | Get the written definition, then audit against it |
| A field was added and clients broke | Strict parsing or fixed buffers meet an additive change | Test additive changes explicitly; size for growth |
| Behaviour changed with no version bump | A bug fix or semantic drift shipped inside a version | Metadata diffing plus behavioural contract tests |
| Numbers stopped reconciling after an upgrade | A calculation was corrected | Compare outputs across versions, not just schemas |
| Timeouts started firing after a "compatible" release | Latency drift | Include latency in the compatibility check |
| Upgrade planned as an instant cutover | In-flight work ignored | Plan the mixed-version window |
| New records unreadable by the old path | The mixed-version test was never run | Run it before the rollout |
| A new constraint broke an unrelated feature | Deferred enforcement fails away from the call site | Ask which enforcement route the constraint uses |
| Migration failed on the oldest records | The store holds records today's code cannot create | Test against the oldest data |
| Deprecation notice arrived after the break | The policy is not operating | Present dated diffs; renegotiate notice |

## Related work

- The baseline this assessment diffs against → `document-vendor-api-surface`
- Testing rather than reasoning about compatibility → `probe-vendor-contract-empirically`
- Recording the upgrade cadence as a standing cost → `report-vendor-capability-gaps`
- Absorbing format churn in one place → `design-vendor-anticorruption-layer`
- Version changes affecting event payloads → `pin-down-vendor-event-delivery`
