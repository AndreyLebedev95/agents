---
name: decompose-requirement-into-scenario
description: Splits a functional requirement or business event into its actor, trigger, precondition, normal-case behavior, postcondition, and error paths (alternatives vs. exceptions), using a fixed use-case shell. Use whenever asked to decompose a requirement into its parts, find the trigger or precondition behind something, write out a normal case and its exceptions, turn a business event into a use case, or figure out who the real actor is behind a piece of functionality — even if the user just says "break this down," "what happens if X fails," or "what has to be true before this can run." Not for writing the atomic "the system shall..." requirement sentences themselves (see write-atomic-requirement-statement), attaching fit criteria or Given/When/Then (see derive-fit-criteria-and-acceptance-criteria), checking scope or completeness (see flag-requirement-gaps-as-open-questions), or assembling a full specification document (see assemble-requirements-specification).
---

# Decompose Requirement into Scenario

A requirement that only says what the system should do, without saying what sets it off, what has to already be true, and what happens when things go wrong, isn't finished — it's a headline. This skill turns one requirement or business event into a complete record: actor, trigger, precondition, the normal-case behavior, the postcondition, and the error paths. That record is what every downstream step (writing atomic requirement statements, deriving acceptance criteria, checking for gaps) actually operates on.

## The shape you're filling in

Every decomposed requirement is one **business event responding through a use case**, with these six parts:

| Field | What it answers | Common mistake |
|---|---|---|
| **Business event** | What real-world happening does this respond to? | Naming a screen or a process step instead of the actual outside happening |
| **Trigger** | What specific data/request/moment starts this? | Naming a symptom instead of the real signal |
| **Precondition** | What must already be true — specifically, what earlier event must have already completed? | Inventing a vague guard condition instead of naming the prior event |
| **Actors** | Who decided this should happen, vs. who just carries out the steps? | Letting whoever currently operates a screen absorb the "actor" label |
| **Behavior** | What are the normal-case steps, described as what must be achieved, not how? | Baking a specific tool/device/UI into the step description |
| **Postcondition** | What must be true when this successfully finishes — for every branch, not just the happy one | Only stating the outcome for the normal case |
| **Error paths** | What alternatives (wanted choices) and exceptions (unwanted but real failures) can happen along the way? | Lumping wanted choices and real failures into one bucket |

## Procedure

**1. Name and classify the business event.**
Name it as "[the outside actor or system] + [what they decided/what happened]" — e.g., "Customer orders coffee," not "Order processing." This form forces you to name a real external actor rather than a vague subject.

Classify it as one of:
- **External** — an outside actor does something and sends a signal in.
- **Time-triggered** — a clock or calendar interval arrives; there is no human/system actor to name, only a schedule.
- **Conditional** — an internal threshold, already-held data crossing a business rule, sets it off.

(These three categories aren't perfectly disjoint in every source — some formal models collapse "conditional" into a variant of the other two. If your project has already committed to a two-way or three-way split, follow that; otherwise use all three and don't force a conditional event into an external/time-triggered box it doesn't fit.)

**2. State the real trigger, not its symptom.**
The trigger is the specific data flow, message, or time/condition that starts the work — not the deeper problem it's a sign of. If a stated trigger looks like a workaround for something upstream ("customer calls because they ran low"), ask *why* the precondition that produced it existed ("why did they run low? why were they allowed to?"). If that produces a more essential business event, use that one instead — but only if it actually changes what this requirement needs to cover. Don't chase "why" past the point where the answer stops changing your model.

**3. State the precondition as a prior event, not a guess.**
A precondition names the state left behind by *other* business events that must already have happened — not an invented, generic-sounding guard. "The passenger must have a reservation" is a real precondition because reservation-creation is itself a separate, earlier event. If you can't name which prior event produced the precondition, you don't have a real precondition yet — you have a placeholder.

**4. Split the actors.**
List the actor whose decision *is* the trigger, separately from actors who merely participate in the behavior. The person or system currently carrying out the steps by hand is not automatically "the actor" — ask whose decision actually initiated the event. A clerk operating a screen is often just the current implementation, not the essential actor; note that distinction so it doesn't get baked into the requirement as a fixed fact about the world.

**5. Write the normal-case behavior in essence, not mechanism.**
Describe each step as what must be achieved, stripped of any specific technology, device, or UI choice — ask "why do they want that" repeatedly until the answer stops naming a mechanism and starts naming the underlying need. Two exceptions:
- If a detail is mandated by a party outside your organization's control (a legal requirement, an external system's fixed format), it survives as an accepted constraint — don't strip it, just don't confuse it with the essential behavior.
- If a requirement's only justification is a technical constraint that no longer exists (carried over from a legacy system with nobody able to say *why* it's still needed), that's a fossil, not essence — flag it as an open question rather than silently reimplementing it.

Keep the normal case to roughly 3–10 steps. If you're closing in on twenty, that's a signal the use case is actually more than one business event, or the steps are written at the wrong level of detail — split before continuing, don't just keep listing steps.

**6. Get agreement on the normal case before hunting for exceptions.**
Chasing failure modes before the happy path is settled derails agreement on the core behavior before it exists. Only once the normal case is accepted, walk each step and ask:
- What happens if this step can't complete, or completes with a wrong result?
- What could prevent reaching this step at all?
- Could an external party or the underlying technology fail here?
- Could the person involved misread what's needed, or take the wrong action, or simply not respond?

Then do a second pass over the same steps asking a different question: could someone *deliberately* misuse or defraud this step (not just accidentally fail it)? That's a distinct concern from ordinary exception-hunting and easy to skip if you only ask "what could go wrong by accident."

**7. Separate alternatives from exceptions.**
Alternatives are choices the business deliberately offers (checkout now vs. add to cart) — they're part of normal behavior, not error handling. Exceptions are unwanted-but-inevitable deviations (a dead connection, missing data, a timeout) that threaten the outcome. Filing both together hides which paths actually need failure-recovery behavior.

**8. State the postcondition for every branch, not just the happy one.**
The postcondition is what must be true when the use case completes — normal case and every exception, each stated separately. A use case is properly bounded when it starts exactly at the trigger and ends only once (a) any data it needed has been read or written and (b) the actual business outcome has been achieved.

**9. Check the boundary.**
Two use cases can legitimately share stored data — that's normal. But if one needs *live* output from the other's processing (not something already sitting in a data store), they're actually one use case and should be merged. And if what you've written already covers more than one business event, split it before moving on.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Trigger reads as an internal system action | Confused the trigger with the deeper event it signals | Restate as the external actor/time/condition demanding a response |
| Precondition is a vague guess ("system must be ready") | Invented instead of derived | Name the specific prior event this depends on |
| Normal case has 20+ steps | Use case too large, or steps too fine-grained | Split into more than one use case, or raise the abstraction level |
| Exceptions surfaced before the normal case was agreed | Skipped happy-path-first ordering | Get explicit agreement on the normal case first |
| Alternatives and exceptions filed as one list | Vocabulary conflated | Alternatives are wanted choices; exceptions are unwanted deviations — split them |
| Actor is "whoever operates the screen" | Implementation detail mistaken for the essential actor | Ask whose decision actually initiated the event |
| A step names a specific product, screen, or vendor | Mechanism baked into the "essential" behavior | Strip to the underlying need; keep the mechanism only if externally mandated |

## Reference

`references/use-case-record.md` has the full field-by-field schema (with a worked example) for writing this up as a structured record rather than prose — read it when you're producing output that needs to be machine-parseable or handed to another skill/tool downstream.
