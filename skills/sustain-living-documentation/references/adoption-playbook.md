# Adoption playbook

Read when introducing the practice to a team.

## Contents
- [The two-hour starter increment](#the-two-hour-starter-increment)
- [Sequencing by social cost](#sequencing-by-social-cost)
- [Eliciting what deserves recording](#eliciting-what-deserves-recording)
- [The three-step path](#the-three-step-path)
- [The two standard objections](#the-two-standard-objections)
- [Migrating existing documentation](#migrating-existing-documentation)
- [What going official costs](#what-going-official-costs)

## The two-hour starter increment

Adoption succeeds on a demonstrated result, not an argument. So the first increment must be small enough to finish and commit in one sitting.

A specific set that fits in roughly two hours, including building the custom markers and verifying that search and rendering work:

1. **A readme** saying what the project is and who it is for.
2. **A decision record** as one file at the project root, recapping the three to five main decisions since inception.
3. **A marker on the key landmarks** — the handful of elements that matter most — made useful through editor search.
4. **A guided-tour marker** with five to seven ordered steps through one end-to-end path.
5. **The single most important sketch**, as a text diagram inside the decision record.

Everything on that list is deliberately doable and committable in a short sitting. A team has done exactly this — a decision record with five past decisions, three landmark markers, and a five-step guided tour — in two hours, including creating the two markers and checking that search worked and the rendering was right.

The aim is two reactions, and the second matters more:

- Interest in the approach — "I like this, I'm hooked."
- People noticing how unfinished their own structure looks once it is made visible — "I now realize how sloppy and half-finished this is."

That second reaction is the real payoff, and it arrives after two hours of work.

**Sizing notes.** Keep the guided tour to five to seven stops, ten at the outside. Number the steps with gaps — ten, twenty, thirty — so a step can be inserted later without renumbering. Give each step a description of its role *in this route*, which is a different thing from the element's own documentation: the element's documentation says what it is, the step description says what it does here.

## Sequencing by social cost

Techniques differ in how much agreement they need before anyone can start. Start with the cheapest.

| Technique | Social cost | Why |
|---|---|---|
| Markers in artifacts | One person, locally, no permission | Lightweight, reversible, part of ordinary work |
| A decision record file | One person, though better agreed | A file in the repository; nobody objects to it existing |
| A readme improvement | One person | Same |
| Naming or structural convention | Team agreement | Everyone has to follow it or it means nothing |
| A generated view | Team decision | Needs shared conventions, a place in the build, agreement on what it says |
| An automatic check that fails the build | Team decision, plus tolerance for interruption | It will stop someone's work at some point |
| Blocking changes to an area | Requires real authority | It will stop someone's work deliberately |

Work down this list as appetite grows. Attempting the bottom rows first is the most common way an adoption stalls: the discussion becomes about the policy rather than the demonstrated benefit.

## Eliciting what deserves recording

### The question sequence

Ask in this order, taking notes and sketching on a shared surface as they talk so they can correct your understanding:

1. What is the project called, what is its purpose, and who is it for?
2. What is the ecosystem — external systems and actors, overall inputs and outputs?
3. What is the execution style, and what is it built on?
4. **What is the core of it, in your opinion?**
5. Should everyone know that?
6. So should we record it?
7. Separately: how is the code organized?

The first three answer easily. The fourth routinely surprises people who have worked on the thing for months — and their answer, once they find it, is exactly the knowledge nobody has written down. Let the silence do its work.

The value is not only the record produced. The person answering usually learns something about their own project, which is often the larger benefit.

### The risk question

Asking people directly what needs documenting produces vague answers. Ask instead:

> Imagine this team is gone and a new one picks the work up a year from now. What risks do you see that they would degrade the system?

The fictitious framing makes it easy to answer, and what comes back is specific: the deliberate design decision that the artifacts do not show, the one a newcomer would break with a single conditional in the wrong place.

Then filter the answers:

- **Discard** whatever a competent practitioner would already know. There is no need to write down what professionals are expected to do; that is not documentation, it is noise.
- **Keep** the deliberate design intent that is invisible from the artifacts.
- **Record each keeper** as a record entry: date, decision, rationale, consequence. Three sentences is enough.

## The three-step path

1. **Create awareness.** An all-audience talk that is informative and entertaining, showing how life could be better rather than explaining how to do things. Listen to the feedback at the end and again a few days later to gauge whether there is appetite. If there is not, try again in some weeks, or go undercover instead.

2. **Find the real need.** Spend time with the team, or one influential member, identifying what knowledge most deserves recording. Propose quick wins as short backlog items or as improvement-time work. Retrospectives are a natural slot. Focus on real needs that several people find important — a demonstration against a need nobody has lands nowhere.

3. **Build and demo.** Build something useful in a short period and demo it like any other task. Collect feedback, improve, and decide collectively whether to expand now or later.

## The two standard objections

### "Markers are not meant for documentation — I don't like adding code that doesn't execute"

Deprecation markers are exactly that, and they are already in use throughout the codebase. That usually settles it.

The useful reframe underneath: the real choice is between a free-text comment and a structured marker. Comments are weak and should be avoided; but if the information is important enough to record at all, it is important enough to earn its own structured marker.

### "We do it already"

Often partly true. The operative word is **deliberate**.

Doing some of these things by accident is fine; doing them on purpose is better, and which practices to use is the team's choice to make explicitly rather than by drift. The approach should be a mix: practices already in place, some pushed further, some new ones worth trying, adjusted over time.

A variant worth handling separately: "we have all the knowledge we need." The person saying this is usually the one who was there first. Ask whether everyone else would say the same.

## Migrating existing documentation

Existing documentation is a starting point, not an embarrassment. It avoids the blank page and forces a review of old knowledge in a new light.

Mine every written source — documents, reports, emails, meeting minutes, forum posts, entries in company tools — and apply one test to each piece:

> Does this still sound relevant after all this time?

Then move what passes to its natural home:

| Old content | New home |
|---|---|
| Vision and goals | The readme |
| Pseudo-code, sequence diagrams | A text diagram, or a reference to the check that exercises the same scenario |
| Descriptions of modules and elements | Into the artifacts themselves, as markers or structured comments |
| Explanatory notes about settings | Next to the configuration they explain |
| Decisions and their reasons | The decision record |

Then deprecate or delete the original, leaving a redirection or an explanation of how to find the knowledge now. Retire the old gradually as the new takes over rather than in one cut.

**One honest consequence.** Content concentrated in a few documents becomes distributed across the codebase. That is usually right — knowledge belongs near where it is needed — but some overview material genuinely reads better held together, and forcing it apart is a real loss. Notice when that applies rather than distributing everything on principle.

## What going official costs

Sponsorship brings dedicated time and sometimes people. That is genuinely valuable.

It also brings visibility and closely monitored progress, with pressure to deliver something demonstrable quickly. That pressure endangers the effort, because this is inherently experimental — you must try things, decide some do not apply here, and adapt others. Under scrutiny, those adjustments read as failures while they are happening.

Three specific traps once it is official:

- **Volume metrics.** A percentage of documentation coverage means nothing, and pursuing it produces documentation made in order to exist.
- **Deferred benefits.** The payoff often arrives months later, so measurement over a quarter shows nothing.
- **Mismatched expectations.** What helps the team may not be what the sponsor wanted. Ask what would actually make them happy — the answer is usually making previously hidden knowledge legible to non-developers, so they can judge from facts rather than from reports.

The recommended order stands: undercover experiments first, official ambition only after you have found what works in this environment.
