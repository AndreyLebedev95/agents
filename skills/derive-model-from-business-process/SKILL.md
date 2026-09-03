---
name: derive-model-from-business-process
description: Walks a business process end to end and derives the model from it — the event timeline, the commands and who or what triggers each, the automation policies, the decision inputs, the external systems, the aggregate groupings and the candidate boundaries. Runs as a facilitated group session or as a solo pass over a specification or a legacy codebase. Covers the ten-step derivation in order, why the successful path is laid out before the failure paths, marking the events that change phase because they predict boundaries, and the rule that every command must trace to an actor, a policy or an external system so gaps become visible. Use whenever turning a requirements document, RFC, ticket or verbal description into a model; when preparing or running an EventStorming session; when recovering how an undocumented or legacy system actually behaves; when exploring new requirements and wanting the edge cases the spec missed; when onboarding onto an unfamiliar domain; or when two stakeholders describe the same process differently — even when the ask is only "help me understand how this works". For the resulting terms use build-domain-glossary; for states and transitions use model-lifecycle-and-events; for consistency boundaries use design-aggregates-and-invariants; for sizing them use map-subdomains-and-boundaries.
---

# Deriving a model from a business process

You have a process and no model of it: a specification, a system nobody understands any more, or several people who each know part of it.

The temptation is to start from the nouns — list the entities, give them fields, draw the relationships. That produces a data schema and hides exactly what you needed: the rules, the ordering, the things that can go wrong, and the places where two people believe different things.

Starting from **what happens** instead surfaces all of that, because a timeline of occurrences cannot hide a gap the way a box-and-arrow diagram can.

## The output

A process model, built in layers:

- The **event timeline**, past tense, including alternative and failure paths
- **Pain points** and open questions marked where they arise
- **Phase divisions** at the events that change context
- **Commands**, imperative, each with its trigger
- **Policies** — automations, with their decision criteria
- **Read models** — what each decision needed to see
- **External systems** — what is outside this model
- **Aggregate groupings** — commands in, events out
- **Candidate boundaries**
- **Findings** — conflicts, gaps, and commands nobody could account for

## The ten steps

Each step enriches the previous one. The order is what makes it work — jumping ahead to aggregates before the events are laid out reliably produces a data model with event names on it.

### 1. Collect the events

Write down everything that happens, in the **past tense**. No ordering. No worrying about duplicates. No arguing about wording.

Keep going until the rate of new ones drops off sharply. Premature convergence is the main risk here — the last few events to surface are disproportionately likely to be the interesting ones, because they are the ones nobody thinks about.

### 2. Order them into a timeline

Put the events in the order they occur.

**Lay the successful path first**, end to end. Then branch the alternative and failure paths off it.

This ordering is deliberate. The successful path gives you a spine, and every step on that spine then raises the question of what else could have happened at that point — which is how the failure paths get found rather than remembered. Skipping straight to "all the cases" reliably produces a model with only the happy path in it, elaborately decorated.

While ordering: fix events that turn out to be wrong, remove genuine duplicates, and add what is obviously missing now that the sequence is visible.

### 3. Mark the pain points

Anywhere the process has bottlenecks, manual steps that should be automated, missing documentation, or missing knowledge — mark it explicitly and visibly.

Making these explicit means they can be returned to rather than mentioned once and forgotten. And do not confine this to the current step: whenever someone raises a concern at any point in the process, record it there and then.

### 4. Find the pivotal events

Look for events that mark a **change of context or phase**, as opposed to an ordinary step.

`cart-initialised`, `order-initialised`, `order-shipped`, `order-delivered`, `order-returned` are different in kind from the events between them. Draw a division at each.

These divisions are the earliest and strongest indicator of where model boundaries belong. That is a lot of value for a cheap step.

### 5. Add the commands

For each event or group of events, name what triggered it. Commands are **imperative** — `publish campaign`, `submit order`, `roll back release` — and sit before the events they produce.

Where a command is obviously issued by a particular role, attach it. Not all commands have an actor; the next steps account for the rest.

### 6. Find the policies

For each command with no actor, look for the **automation**: an event whose occurrence triggers that command.

Write the decision criteria on the policy itself. "Escalate on complaint received" is incomplete if the real rule is "escalate on complaint received, only for priority accounts" — and that condition is exactly the kind of thing that never makes it into a specification.

### 7. Add the read models

For each command issued by a person, ask what they were **looking at** when they decided. A screen, a report, a notification, a dashboard.

This sits before the command, because the decision depended on it. It also tends to expose data the system does not currently surface anywhere, which is a finding.

### 8. Add the external systems

Anything not part of the process being modelled: it may issue commands into it, or need to be notified of events out of it.

**By the end of this step, every command must be accounted for by exactly one of three things:** a role that issues it, a policy that triggers it, or an external system that calls it.

**A command still unattributed is missing knowledge.** Record it as a finding. Do not invent a plausible trigger — the invention will be adopted as fact and nobody will remember it was a guess.

### 9. Group into aggregates

Now organise related commands and events into aggregates. The operational definition is simple and precise:

> **An aggregate receives commands and produces events.**

Group by that — which commands come in and which events go out together — not by data affinity. Grouping by shared fields produces a schema; grouping by command-in/event-out produces units that own a coherent piece of behaviour.

Turning these into real consistency boundaries with invariants is `design-aggregates-and-invariants`.

### 10. Group into candidate boundaries

Finally, look for aggregates that are related — either because they implement closely related functionality, or because they are coupled to each other through policies. Those groups are the candidate model boundaries.

Sizing and classifying them is `map-subdomains-and-boundaries`.

## Variants

This is guidance, not a fixed ritual. Adapt it.

The most useful variant when starting cold: run **steps 1–4 across the whole domain** to get the big picture — a wide event landscape, the phase divisions, and a first read on where boundaries might go. Then run **all ten steps per business process** for the ones that matter.

For a solo pass over a written specification or a codebase, the steps work unchanged; you are asking the document the questions instead of a person. Be aware that the derivation is genuinely weaker without people in the room, because a document cannot be surprised by its own gaps. Mark what you inferred, distinctly from what was stated.

## What this is actually for

A completed pass gives you events, commands, aggregates and candidate boundaries — and if you go on to model the lifecycle with events, it hands you the blueprint.

Those are bonuses. **The real value is the process itself**: people sharing knowledge, aligning their mental models, discovering where their models conflict, and converging on shared terminology. Building the model together is what makes participants start using the same words, which no glossary handed down afterwards achieves.

That has a practical consequence: if you find yourself optimising for a tidy diagram, you have the priorities backwards. A messy wall that produced three genuine disagreements was a better session than a clean one that produced none.

Expect **co-creation, not extraction**. Much of what you need is tacit, and asking questions frequently does not retrieve an existing answer — it forces people to resolve ambiguities and gaps in their own understanding. That is most common in the areas the business considers its speciality, where the learning genuinely runs both ways.

## When to use it, and when not

Run it to:

- Build shared terminology
- Model a process and find aggregate and boundary candidates
- Explore new requirements and surface the edge cases the requirements missed
- **Recover domain knowledge that has been lost** — most acute in legacy systems facing modernisation, where the knowledge exists only in fragments across several people
- Find inefficiencies from the end-to-end view
- Onboard people onto an unfamiliar domain

**Do not run it when the process is simple or obvious.** A sequence of steps with no interesting logic or complexity will not repay the effort, and running it anyway teaches people that the technique is ceremony.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Only the happy path in the model | Stopped after step 2 | Branch the alternative and failure paths before going further |
| Commands with no trigger at the end | Step 8 not completed | Record each as missing knowledge — do not invent a trigger |
| Aggregates grouped by shared fields | Grouped by data affinity | Regroup by which commands come in and which events go out |
| Policies with no conditions | The criteria were never asked for | Every automation has conditions; find them |
| A tidy diagram nobody uses afterwards | Artifacts treated as the goal | The alignment is the point; make it a shared exercise |
| One or two people doing all the talking | Group dynamics not managed | Draw the quiet participants in with direct questions about the model |
| Ran it on a trivial process | Wrong tool for the job | Skip it |

## Bundled references

- `references/facilitation.md` — group composition and the size cap, the opening legend, energy management, handling breaks, remote sessions, and the question sets for drawing out invariants and edge cases. Read when a group session is being planned rather than a solo pass.

## Worth reading

- Alberto Brandolini, *Introducing EventStorming* — the origin and rationale of this process.
- Paul Rayner, *The EventStorming Handbook* — practical facilitation experience.
