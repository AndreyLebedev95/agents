---
name: write-atomic-requirement-statement
description: Turns a decomposed scenario step, or a raw stakeholder ask, into a well-formed atomic requirement — one sentence, one verb, a rationale that isn't a smuggled solution, and a correct type classification (functional, non-functional, constraint, or technological). Use whenever asked to write a requirement properly, check whether a requirement is really atomic, add or interrogate a rationale, classify what type a requirement is, spot a solution disguised as a need ("I want an app that..."), or turn a vague ask ("make it user-friendly") into something with a real description behind it. Not for the actor/trigger/precondition/postcondition decomposition itself (see decompose-requirement-into-scenario), fit criteria or Given/When/Then (see derive-fit-criteria-and-acceptance-criteria), scope/completeness gap-checking (see flag-requirement-gaps-as-open-questions), or overall spec structure (see assemble-requirements-specification).
---

# Write Atomic Requirement Statement

A requirement description that reads confidently can still be doing none of its job: it can bundle two actions into one sentence, smuggle a chosen solution in as if it were the need itself, or carry a rationale so thin nobody could tell if it matters. This skill turns a rough step or stakeholder ask into a requirement that's actually a single, well-formed unit — one action, a real reason it exists, and an honest label for what kind of requirement it is.

## What "atomic" means

An atomic requirement is a single sentence with a single verb: "The product shall `<verb>` ...". If writing it naturally needs "and" to join two actions, it isn't atomic yet — split it. Atomic doesn't mean simple: a requirement can (and usually should) carry a rationale, a type, and eventually a fit criterion alongside it — those are components *of* the requirement, not reasons to split it further. Stop splitting once each piece names exactly one action and can't be usefully divided any further.

## Procedure

**1. Derive candidate requirements from the step.**
For each behavior step you're working from, ask: "what must the product actually do to accomplish this?" Each distinct answer is a candidate requirement. Then look at any qualifying term the step uses — "valid," "available," "authorized" — and ask what it actually means; that answer is often its own separate requirement (a constraint or a data-definition requirement), not just a detail of the first one.

**2. Check atomicity.**
Read the candidate description back. If it needs "and" to hold together, split it into two. If you land on a single verb and a single object, it's atomic — don't keep splitting past that point just for the sake of granularity; a step that only ever produces one requirement, or one that produces more than about six, is worth a second look (too coarse in the first case, possibly hiding a much bigger use case in the second) but neither is an automatic error.

**3. Write the rationale, always — never skip it because the description "seems obvious."**
Ask: why does this exist? Write the answer as the Rationale field. This does two jobs at once:
- **Solution check** — if the rationale names a *different* action than the description does, the description was a presumed solution, not the real need. Rewrite the description to match what the rationale actually establishes, and push the original description down to "one possible way to satisfy this," not the requirement itself.
- **Priority signal** — two requirements can read identically but carry very different rationales ("customer wants to see it" vs. "regulation requires it exists"), and those rationales — not the description — are what should drive priority. A requirement with a thin, trivial rationale is a weak candidate for high priority no matter how the description reads.

**4. Run the solution-smuggling test on the description itself.**
Read the verb and object. If it names a specific screen, device, vendor, or mechanism, ask what business need that mechanism was chosen to satisfy, and rewrite the description as *that* need instead. A useful rewrite trick for stakeholder-voiced asks: change "I want `<mechanism>`" to "I can `<capability>`" and see whether the capability still names a mechanism. If it does, ask "why" again. Keep the mechanism only if it's genuinely mandated by something outside your organization's control (a legal requirement, a fixed external format) — in that case it belongs in a separate constraint requirement, not folded into the description as if it were the need.

If it's a value/benefit statement ("so that I can..."), apply the same repeated-why treatment: keep asking why the stated value matters until an answer stops producing anything new, or until you notice the value, even if achieved, wouldn't actually resolve the underlying problem. A requirement whose value line stays weak or trivial after this is a candidate to discard or deprioritize, not to keep out of politeness.

**5. Classify the type.**
Every requirement is exactly one of:
- **Functional** — an action the product must do, remember, or process.
- **Non-functional** — a quality the functions must have (performance, usability, security, and so on).
- **Constraint** — a restriction on the solution itself, non-negotiable, global (a mandated platform, a budget, a partner system).
- **Project driver** — a business-level force behind the project (purpose, who cares).
- **Project issue** — a condition governing whether the *project* succeeds, not the product (risk, budget, timeline).

For non-functional requirements specifically, run the checklist in `references/nfr-checklist.md` — non-functional gaps are the easiest kind to miss because nobody asks for them by name (nobody says "please add a Security section"; they say "make it secure" or say nothing at all).

Give **technological requirements** special handling: a technological requirement exists only because of a chosen implementation technology, not because the business needs it (e.g., "establish a secure connection" only exists because you chose an internet-based architecture). Tag these separately, and don't let them into the requirement set until the business requirements are independently understood — otherwise a chosen technology quietly pre-empts business analysis that hasn't happened yet.

**6. Keep priority out of the description's wording.**
Don't use "must"/"should"/"could" inside the description to signal priority — readers can't tell if the word is doing real work or is just habit. Use one consistent form for every description ("The product shall...") and carry priority as its own separate attribute, set from the rationale (step 3), not from word choice.

**7. For permission/access requirements, write the restriction too.**
Whenever you write a requirement that grants a capability ("authorized users can access X"), also write its complement that bounds it ("*only* authorized users can access X"). Consider whether an overarching "the product shall not do anything beyond what's specified" requirement is warranted for this project — without it, an unspecified "helpful" addition can quietly become a new attack surface or scope creep that nobody agreed to.

## Decision rules

- **A single business rule usually fans out into several requirements.** "Maximum shift is eight hours" isn't one requirement — ask which use cases it touches (recording start/end times, alerting when a limit is approached, blocking a schedule that would exceed it) and write one requirement per resulting behavior.
- **Don't argue about which non-functional bucket something belongs in.** A requirement about, say, colorblind accessibility could plausibly be filed under usability, accessibility, or compliance — arguing about the filing wastes the time that should go to making sure it and its siblings were all found in the first place.
- **A constraint with no rationale and no fit criterion is suspect.** Demand both for every constraint. If nobody can supply them, challenge whether it's a real constraint or just an unexamined preference dressed up as one.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Requirement needs "and" to read naturally | Not yet atomic | Split into separate requirements |
| Description names a specific screen, device, or vendor | Solution smuggled into the requirement | Rewrite as the capability/outcome; keep the mechanism only if externally mandated, and move it to a constraint |
| "must"/"should" sits inside the description text | Priority conflated with description | Move priority to its own attribute |
| Two requirements share a description but got different priorities | Rationale was skipped or too thin | Write the rationale first — priority should follow from it |
| A financial or health-adjacent product has no populated Security requirements | NFR checklist wasn't run | Walk the eight-category checklist explicitly, don't wait for someone to ask |
| A constraint has no rationale and no fit criterion | Preference dressed up as a mandate | Challenge it — demand both or drop it as a constraint |

## Reference

`references/nfr-checklist.md` — the full non-functional requirement category breakdown with sub-items, for completeness-checking a requirement set. Read it whenever classifying or auditing non-functional requirements, not just when one obviously applies — the point of the checklist is catching the categories nobody thought to ask about.
