---
name: derive-fit-criteria-and-acceptance-criteria
description: Attaches a testable fit criterion to a requirement and writes it up as Given/When/Then acceptance criteria that reuse the requirement's own precondition, trigger, and postcondition rather than re-deriving them from scratch. Use whenever asked to write acceptance criteria, give a requirement a fit criterion or pass/fail threshold, figure out how to actually test something, or turn a vague quality requirement ("should feel trustworthy," "must be fast") into something measurable. Not for the actor/trigger/precondition/postcondition decomposition itself (see decompose-requirement-into-scenario, which supplies this skill's raw material), the requirement's description/rationale/type (see write-atomic-requirement-statement), or deciding whether a requirement is in scope at all (see flag-requirement-gaps-as-open-questions).
---

# Derive Fit Criteria and Acceptance Criteria

"Fit criterion" and "acceptance criterion" name the same thing: a measurement that lets you sort any candidate solution into "meets this" or "doesn't," without an argument. A requirement without one isn't finished, however confidently it reads — if you can't measure it, you can't tell whether it's been satisfied, which means nobody downstream can either. Attach it the moment the requirement is written, not as an afterthought at test time — waiting means someone eventually has to reverse-engineer a threshold nobody agreed to, or ship something untestable.

Given/When/Then is just a different notation for the same information you already have from decomposition — it doesn't need separate derivation.

## Procedure

**1. Don't try to quantify a vague adjective directly.**
"User-friendly," "cool," "professional" resist direct measurement because the word itself carries no scale. Instead, work from the requirement's *rationale*: ask "why do you want this" repeatedly until you reach a concrete, observable consequence (e.g., not "friendly" but "customers don't call support to ask how to use it" or "customers pick it up without being shown how"). Then find a scale of measurement for *that* consequence, not for the original adjective.

If two stakeholders give different rationales for what looks like the same requirement, treat them as two different requirements — each needs its own fit criterion, because they're actually measuring different things.

**2. If the scale is obvious but the number isn't, ask directly.**
Once you know you're measuring, say, response time, but don't know the threshold, ask the stakeholder point-blank: "what would you consider a failure here?" That's often faster than trying to derive a number analytically.

**3. For genuinely subjective qualities, use a proxy or a standard — never a raw guess.**
Two legitimate paths:
- **Proxy behavior**: find an observable action correlated with the quality (does a shopper pick the item up and hold it? do they show it to a companion?), measure it across a representative panel, and set a percentage threshold with a tolerance.
- **Cited standard**: point to an existing external or internal standard as the benchmark instead of inventing a number.

Either way, the *number* itself must trace to evidence — a study, a standard, an explicit business decision — never just "that sounds about right." Note the evidence alongside the fit criterion so it can be checked later.

**4. Never demand 100%.**
Real populations always include below-average performers and edge cases. State thresholds as a percentage with an explicit, negotiated tolerance ("90% within 6 seconds") rather than "every user" or "never fails." Where a hard outer bound genuinely matters, add it alongside the percentile target rather than instead of it (e.g., "90% within 15 seconds, and never longer than 20").

**5. If agreement on a measure stalls, there are only two honest outcomes.**
Either several distinct requirements got lumped into one description — split them, and give each its own fit criterion — or the requirement itself is too vague or unrealistic to mean anything testable, in which case reject it outright. "Ship it unmeasured and figure it out later" is not a third option; an unmeasured requirement will get measured eventually, just by whoever happens to build it, against whatever standard they happen to pick.

**6. For a functional (action) requirement, the fit criterion is usually the precise postcondition, not a number.**
"The system shall record the transaction" doesn't need a numeric scale — it needs the postcondition spelled out precisely enough that completion vs. non-completion is unambiguous (what exactly got recorded, in what state, visible to whom). When correctness depends on matching an external source of truth rather than an internal computation you own outright, name that authority explicitly in the fit criterion ("recorded value shall match the value reported by `<the authoritative source>`") instead of just restating the action.

**7. Define every term the fit criterion depends on, once, centrally.**
A fit criterion built on an undefined term (what exactly counts as "active," "valid," "a session") isn't complete just because it has a number in it — if the term isn't defined somewhere every requirement can point to, different readers will silently supply different definitions. Treat an undefined term used in a fit criterion as an open question, not a shared understanding you can assume.

**8. Write Given/When/Then by copying, not re-deriving.**
- **Given** = the precondition already established for this requirement.
- **When** = the trigger already established for this requirement.
- **Then** = the full postcondition, stated as a set of observable, checkable facts — not a vague "it works."

Draft the GWT alongside the scenario/decomposition rather than after it's finished — a mismatch between what the GWT says and what the decomposition says is exactly the kind of thing that's cheap to catch early and expensive to catch after the fact. If a requirement later gets sliced into smaller pieces for implementation, slice its GWT along with it — expect one GWT per meaningful slice, not one giant GWT trying to cover an entire large story.

**9. Use the act of writing the fit criterion as a comprehension check.**
If you genuinely cannot state how you'd know this requirement was satisfied, that's a signal you don't understand it well enough yet — go back and clarify with whoever owns it rather than inventing a plausible-sounding number to fill the gap.

## Decision rules

- **Numeric vs. standard-based, by requirement type.** Performance and usability requirements are usually measured with numbers (time, rate, percentage). Look-and-feel, security, and cultural requirements are usually measured by citing a standard or running an approval/acceptance panel instead — forcing a number onto these often produces a fit criterion nobody can actually apply.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Fit criterion says "100% of users" / "never fails" | No tolerance applied | Restate with a percentage plus tolerance, or a hard bound alongside a softer target |
| Fit criterion just restates the description in other words | Derived from the description instead of the rationale | Re-derive from the rationale's concrete, observable consequence |
| Given/When/Then re-derives its own precondition/outcome from scratch, and it doesn't quite match the decomposition | Written independently instead of reused | Copy Given/Then directly from the requirement's own precondition/postcondition |
| A threshold number has no citation behind it | Guessed | Attach the evidence (a study, a standard, an explicit business decision) alongside it |
| The team argues endlessly over what measure to use | The requirement is either lumped or genuinely unmeasurable | Split it into separate requirements, or reject it outright |
