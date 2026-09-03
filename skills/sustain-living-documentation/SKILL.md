---
name: sustain-living-documentation
description: Diagnoses why documentation is decaying and makes a documentation or traceability practice survive adoption. Covers why naming an owner does not fix a rotting artifact and what ownership should attach to instead, automation as what forces declared knowledge to stay honest, enforcing the few decisions that outlive the people who made them, markers attached to the side that gets deleted so they need no cleanup, raising the standard only for new work rather than attempting completeness, a starter increment small enough to commit in one sitting, why coverage metrics for documentation discredit the effort, and what to delete. Use whenever a matrix, glossary, diagram, runbook or process document has gone stale or is trusted by nobody; when introducing such a practice to a team; when deciding who should own it; when someone proposes a documentation coverage target; when retrofitting onto legacy; or when work on the tooling is outgrowing the work it serves — even if the ask is only "how do we stop our docs going out of date". For designing a traceability scheme use design-traceability-scheme; for running the checks use check-traceability-integrity.
---

# Sustaining living documentation

Documentation decays for mechanical reasons, not moral ones. Nobody is insufficiently committed. Something in the design of the artifact made staying accurate depend on a person remembering, and people do not.

So the work here is diagnostic before it is motivational: find the specific mechanism by which each artifact goes wrong, and change that. General exhortations to keep documentation current have never worked anywhere and will not work here.

## The output

Either a **rot diagnosis** — per artifact, not in general:

```
## <artifact>
Keeps it accurate today:  <the actual mechanism, or "a person remembering">
Decay mechanism:          <which one>
Fix:                      <generate | propagate | check | enforce | delete | accept>
Owner of the mechanism:   <who owns the generator or check, not the updating>
```

Or an **adoption plan**, sized to what one person can commit in a single sitting.

Both end with what to **stop** doing. A plan that only adds is not a plan.

## Diagnose per artifact

Ask one question of each artifact, and take the answer literally:

> **What keeps this accurate today?**

If the honest answer is "someone is supposed to update it", you have found the decay mechanism and there is no need to look further.

`references/rot-mechanisms.md` has the full diagnostic table. The recurring ones:

| Tell | Mechanism | Fix |
|---|---|---|
| Accurate for three weeks, then not | Accuracy rests on diligence | Generate it, or add a check that fails |
| The practice quietly stopped | A step in it was a chore | Find the transcription step and remove it |
| Other teams ignore the decision | It was communicated, not enforced | Escalate to a mechanism for the few that matter |
| Links break constantly | Perishable values written into the document | Replace each with a pointer to where it lives |
| Stale transitional tags everywhere | Markers on the side that survived | Attach to the side that gets deleted |
| Nobody trusts any of it | One stale item taught them not to | Fix the mechanism first; trust returns slowly |

## The central correction: own the mechanism, not the updating

The usual response to a rotting artifact is to assign someone to own it. This does not work, and the reason is worth being precise about, because the intuition behind it is sound and the conclusion is wrong.

Keeping duplicated knowledge consistent through care and dedication fails in practice. It is not a discipline failure to be corrected with more diligence or clearer accountability — it is a **design failure**, and adding a name to it changes nothing about the design. The named owner now performs, on a schedule, the same unrewarded transcription that was failing before, and they stop for the same reasons.

What ownership should attach to:

- the **generator** that derives the artifact
- the **check** that fails when two things disagree
- the **convention** and whatever enforces it
- the **decision** about what is deliberately not tracked

Never the manual updating. Someone genuinely does need to own this — the instinct that an unowned chain rots is correct — but what they own is the machinery, and their job is to notice when the machinery stops being run rather than to keep a spreadsheet current.

There is a related trap in the same family. **Any step consisting of copying information from one place to another will lapse**, regardless of who is accountable, because it is a chore and chores stop. Treat sustainability as a design constraint: find the step people will quietly stop doing, and automate it or design it away. Asking harder is not an option that has ever worked.

## Why execution is what keeps things honest

The strongest available mechanism is to move the knowledge into something that is *executed constantly*.

A declaration a tool runs dozens of times a day cannot be wrong for long, because anything wrong in it stops the work. That constant use is what forces it to stay true — and it makes the automation a reconciliation mechanism for the process it describes. A description that is never executed has nothing forcing it to remain correct, which is exactly why written process documents rot and executed ones do not.

So, in order of preference: make it executed; failing that, make it generated; failing that, make it checked; failing that, accept that it will decay and either delete it or say plainly that it is a point-in-time account.

Two conditions on this. The declaration must describe desired state rather than a sequence of steps, or it is a script and reads like one. And it must genuinely be run often — something executed once a quarter has almost none of this property.

## Enforce what will outlive the people

Long-running efforts outlast the tenure of whoever started them. You can never be sure that other teams — remote ones, ones in another department — read the documentation, read the emails, or were listening when it came up at standup. And when a decision is not respected the cost is real.

So for the few decisions whose violation actually causes harm, escalate from communication to mechanism:

1. State it in the record, with its rationale
2. Mark it in the artifacts themselves
3. Add an automatic check
4. Make the check fail the build, where that is safe
5. Block the change outright — and ensure whoever hits the block **learns the reason at that moment**

That last clause is what makes blocking humane rather than merely obstructive: the person who is stopped should understand why, on the spot, and ideally learn something.

**Reserve the upper rungs for the few decisions that matter.** Enforcing everything produces a system nobody can work in, and the response is that the enforcement gets removed wholesale — including the parts that were load-bearing.

## Make markers biodegradable

A marker describing a transitional state should live on the artifact that **disappears when the transition completes**, not on the one that survives. Then the deletion removes the marker, with no cleanup task to remember and no stale label left behind.

Mark the component being replaced as superseded, rather than marking its replacement as a replacement — once it has succeeded, the replacement is simply the system, and the tag is meaningless.

Where the surviving side must also be marked, accept that the cleanup is now a task. There is a compensation worth knowing: a temporary tag still present long after it should have gone is a visible signal that the initiative was never finished. That is information, if you read it.

## Adoption: start small, start alone

**Start undercover.** Introduce it as ordinary professional work, without seeking authorization and without announcing a change of approach. Record decisions at the moment you make them. Use slack time or a genuine request to build one small mechanism. Talk about benefits, never about the theory.

Make it official only after you know what works *here*. The reason is specific rather than political: an official programme is monitored and pressured to show visible progress quickly, while this is inherently experimental — you must try things, discard some, and adapt others. Under scrutiny, those necessary adjustments read as failures.

Sponsorship does bring dedicated time, which is real. That is the trade.

**Sequence by social cost.** Techniques differ in how much agreement they need. A marker added to an artifact can be started by one person, locally, without permission, and is reversible. A generated view is a team decision — it needs shared conventions, a place in the build, and agreement on what it says. Start with the first kind.

**Keep the first increment to one sitting.** `references/adoption-playbook.md` gives a starter set that fits in about two hours including building the markers and checking that search and rendering work. The aim is two reactions, and the second matters more: interest in the approach, and people noticing how unfinished their own structure looks once it is made visible.

**Elicit what deserves recording by asking the right question.** Asking people what needs documenting produces vague answers. Ask instead:

> Imagine this team is gone and a new one picks the work up a year from now. What would they break by accident?

The fictitious framing makes it easy to answer, and what comes back is precisely the design intent the artifacts do not show. Then discard whatever a competent practitioner would already know — that needs no documentation — and keep the rest.

## Retrofit marginally

Do not attempt completeness on an existing system. That is how the effort dies.

Declare instead that from now on, every new piece of work meets a higher standard. Over time this covers the parts of the old system that actually matter, because those are the parts being touched — and the rest can be left alone deliberately rather than as a failure.

Where new work can be segregated into its own bounded area, do that: declare the demanding standard once at the boundary so it applies to everything inside, and enforce it automatically. Meeting a high standard inside a boundary is achievable in a way that meeting it everywhere is not. This is also the answer when someone genuinely needs full documentation of part of an old system — rebuild that part inside such a boundary.

## Measuring it

**Refuse coverage metrics for the effort.** A percentage of documentation coverage means nothing, and pursuing it produces documentation made in order to exist — which discredits the whole approach and gets it cancelled.

Two further traps come with visibility: the benefits often arrive months later, so measurement over a quarter shows nothing; and the adjustments the techniques need in a new context get read as failures while they are happening.

Measure by delivery instead — decisions made faster because the knowledge was at hand, or problems found because producing the view exposed them. And ask sponsors what would actually make them happy, since what helps the team may not be what they expected. Usually the answer is making previously hidden knowledge legible to non-developers, so they can judge from facts rather than from reports.

## Know when to stop and what to delete

**Documentation whose existence proves an unfixed problem.** A troubleshooting guide records that someone judged the traps important enough to write down, and thereby records that nobody is fixing them. Before documenting a problem, ask whether the same effort would fix it. Where it genuinely would not, name which honest reason applies — budget allocated to documentation but not to the code, a fix that is expensive or needs coordination across teams, the team lacking the knowledge. Some of those are legitimate. Naming which one separates a considered decision from an evasion.

**The mechanism outgrowing the work.** Building generators is more fun than delivering, and effort drifts. Require that each improvement to the mechanism yield a demonstrable short-term benefit in delivery, quality or user satisfaction. Watch for perfectionism, which in this area is procrastination wearing a good motive.

**Documentation that makes people afraid to change things.** When "we'd have to update all the docs" appears in a discussion about a change, the documentation has inverted its purpose — it is protecting itself rather than the system. That is a defect in the documentation, not a cost of the change.

**Knowledge still in flux.** Never automate something whose shape is still moving; the mechanism will be rewritten faster than it pays back. And if existing automation is making change harder rather than easier, delete some of it.

**Transient material.** Diagrams drawn to think through one problem, and everything about planning — stories, estimates, burndown data — are useful before and during, and worthless after. Delete them. Keeping them produces a store of stale material that makes the useful material harder to find. Where a transient artifact is worth keeping, retell it as a dated account rather than leaving it as apparently current.

**Promote only what has proven itself.** Most knowledge matters only at the moment it is created. Exchange it in the cheapest interactive way first, wait, and promote to a durable form only what has repeatedly proven useful, is critical, or must be widely known.

## Publishing is not knowing

A written record is never sufficient, because not everyone reads it. Knowledge everybody is supposed to have needs active circulation as well as a persistent form: present it to each team in scheduled working time rather than as optional reading, and ask people questions at intervals to find out whether it actually landed. Discovering a gap that way is far cheaper than discovering it in every subsequent discussion.

There is a compounding payoff when this works. Knowledge that lives in the artifacts and is generated from them lets everyone see the state of the system and decide accordingly, without going through the few people who hold it. Knowledge kept with designated specialists makes them the bottleneck and the single point of failure — which is the situation the whole practice exists to escape.

## Reference material

- `references/rot-mechanisms.md` — the decay mechanisms as a diagnostic table, each with its tell, its cause and its fix. Read when working out why a specific artifact is decaying.
- `references/adoption-playbook.md` — the two-hour starter increment, the elicitation questions, sequencing by social cost, the two standard objections and their answers, and how to migrate existing documentation without a blank page. Read when introducing the practice to a team.
