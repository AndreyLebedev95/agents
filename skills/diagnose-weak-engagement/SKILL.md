---
name: diagnose-weak-engagement
description: Diagnoses why people stop coming back to a shipped product — which of the four engagement phases (trigger, action, reward, investment) is the binding constraint — and proves it from cohort data using identify/codify/modify habit testing. Returns an ordered diagnosis with evidence, a habit-path analysis, and a change plan with what to measure next. Use whenever retention is flat or falling, cohort curves decay, users churn after onboarding, an app is uninstalled after one session, notifications get ignored, or a redesign failed to move retention; when a team is arguing about which feature would fix engagement; or when someone asks what to measure to know whether a habit is forming, how many habitual users are enough, or how to find the activation moment, aha moment, or magic number. Use it even when the question is just "why aren't users coming back". For designing a loop that does not exist yet, use design-engagement-loop. For whether the loop should exist at all, use screen-behavior-design-ethics. For picking what to build, use find-habit-forming-opportunities. Not for screen-level confusion or clarity problems (review-screen-for-friction) and not for running sessions with real participants (run-diy-usability-test).
---

# Diagnose weak engagement

Something ships, people try it, and they do not come back. Your job is to name **which single phase of the loop is the binding constraint**, prove it, and say what to change — not to produce a list of everything that could be better.

The loop being diagnosed:

**trigger → action → variable reward → investment → (loads the next trigger)**

Work in this order. Steps 1–3 are cheap and often end the investigation.

## Step 1 — Separate prompted from unprompted usage

Before reading any number: sessions attributable to campaigns, ads, lifecycle email, or push blasts are not evidence of a habit. A habit means people arrive on their own.

Split the traffic. If unprompted return usage is near zero, the loop has not closed, and every engagement number above it is measuring your marketing spend. That is the finding — do not proceed to optimize phases until it is addressed.

## Step 2 — Check the product can be habitual at all

Plot the target behavior on two axes: **how often it occurs** and **how useful it seems relative to the user's current solution** (not relative to nothing).

The threshold curve slopes down but never touches the utility axis. That asymmetry is the whole point:

- An **inherently infrequent** behavior never becomes automatic, no matter how much value it delivers. It stays a conscious decision.
- A behavior with **minimal perceived benefit** can still become habitual purely on frequency.

So frequency is the axis that cannot be substituted. If frequency is structurally low — the product is used a few times a year by its nature — the correct diagnosis is *this product does not run on habit*, and the fix is sales, referral, and advertising rather than loop repair. Say that plainly instead of tuning notifications.

## Step 3 — Five-question triage

Ask these in order. The first one you cannot answer concretely names the broken phase. This is the fastest diagnostic available and it is worth doing before touching data.

1. What do users really want? What pain is the product relieving? *(internal trigger)*
2. What brings users to the service? *(external trigger)*
3. What is the simplest action taken in anticipation of reward, and how could it be made easier? *(action)*
4. Are users fulfilled by the reward yet left wanting more? *(variable reward)*
5. What bit of work do users invest? Does it load the next trigger and store value? *(investment)*

Answers like "users want a great experience" are non-answers. Push for the specific emotion, the specific action, the specific bit of work.

## Step 4 — Triage the failing action

Pick the one behavior that is not happening — not "engagement", a specific action at a specific moment. Three things must be present simultaneously for any behavior: motivation, ability, and a trigger. If any is missing or inadequate, nothing happens.

Test in this order:

1. **Trigger** — was a cue present at that moment at all?
2. **Ability** — how many steps? Which of the six resources is scarcest for this user at this moment: time, money, physical effort, brain cycles, social deviance, or how far the action departs from their existing routine?
3. **Motivation** — did they want the outcome then?

Fix the missing ingredient. Adding more of the ingredients already present is the most common wasted quarter in engagement work — more motivational copy on a screen whose problem is six steps, more steps removed from a screen nobody was triggered to open.

Ability is usually the cheapest and highest-return of the three. Raising motivation is slow and expensive: people ignore explanatory text, they are multitasking, and they have little patience for being told why they should act.

## Step 5 — Audit each phase against its failure signature

Read `references/phase-failure-signatures.md` — the per-phase tells, causes, and cheapest check for each. Use this when there is no usable data and the diagnosis must be made by inspection, and as a cross-check when there is.

## Step 6 — Habit testing on live data

When there is a live product with real usage, run the three-step loop. Full procedure, including how to set the frequency definition and what a habit path looks like in data: `references/habit-testing.md`.

**Identify.** Define what a devoted user looks like — how often one *should* use this product — and do it **before** looking at your own numbers, anchored on comparable products. Then count how many and which users meet that threshold, by cohort.

**Codify.** Among those habitual users, find the **habit path**: the series of similar actions your most loyal users share. Where they came from, what they decided at registration, how many connections they have, the order in which they did things. Every product has a different set; the goal is to find which step is critical for producing devotees.

**Modify.** Change the product to move new users along that same path — registration funnel, content, emphasis on an existing feature, or removing a feature. Then compare each new cohort against the habitual pattern. Repeat with every feature and iteration.

The example worth carrying: a social service found that new users who followed thirty other accounts crossed a tipping point that sharply raised the odds they kept using it, and rebuilt onboarding around following rather than around the action most new users were performing.

## Step 7 — Test what the team is afraid to test

Teams systematically under-send triggers out of an untested fear of annoying users. A trigger that carries genuine meaning at the right moment can be received as a gift: one team that feared uninstalls from a single seasonal greeting notification instead watched users photograph and share it.

Run the experiment rather than arguing about it. Send the message the team is afraid to send, to a bounded population, at a moment when it would carry meaning, and measure uninstalls, complaints, and shares — not internal discomfort. Escalate from evidence and stop where the metrics turn.

This is not a licence for volume. The finding is that *meaningful* triggers tolerate more frequency than teams expect, not that all triggers do.

## Step 8 — Write the diagnosis

Output structure:

```markdown
# Engagement diagnosis: <product>

## Binding constraint
<One phase. One sentence on why it, and not the others.>

## Evidence
<The unprompted/prompted split. The frequency-utility placement. The specific
triage answers that failed. What the cohort data shows.>

## Habit path
<What the retained users have in common, or "not identifiable — here is what
to instrument to find it".>

## Change plan
<Ordered. Each item: the change, the phase it addresses, and the single metric
that would show it worked.>

## What not to do
<The plausible fixes that address a non-binding phase, and why they will not move retention.>
```

Naming one binding constraint is the discipline. A diagnosis that lists eight improvements across four phases is a wish list, and teams act on wish lists by picking the easiest item.

## Decision rules

- **The 5 percent signal.** If fewer than roughly 5 percent of users engage at the frequency you defined as devoted, either you identified the wrong users or the product needs rethinking. Treat this as a rule of thumb for whether any habit exists at all — a sustainable business needs a far higher active rate, so it is a floor for signal, never a target.
- **Set the frequency target before looking at your data**, anchored on comparable products. Defining it from your own extreme users produces an unreachable bar and hides real habit formation. Several times daily for a social feed; once or twice weekly for something tied to an occasional event. Where no comparable data exists, state the assumption explicitly and honestly.
- **There is no habit timescale.** Formation ranges from a few weeks to more than five months, driven by the behavior's complexity and how much it matters to the person. Judge by repetition rate, and reject any plan or forecast built on a fixed day count.
- **Funnel optimized, retention flat** → suspect the optimized action is not the one that predicts retention. Find the early behavior that correlates with users still being active later and compare it against what the entry surface currently pushes.
- **Price increases that hurt** are evidence that usage is not actually habitual. How much agony a business goes through raising prices is a read on the strength of the habit.
- **Low switching from a competitor is usually not a feature gap.** Users overvalue what they already do; a new entrant needs a dramatic improvement — roughly an order of magnitude, as a rule of thumb — because switching cost is cognitive. Even small interface differences force relearning and make an objectively equal alternative feel inferior. If the team's pitch is a feature comparison, that is the diagnosis.
- **Recent cohorts regress first.** Newly formed habits are the ones most likely to be abandoned, because old routines remain and reactivate when attention lapses. A decay concentrated in your newest cohorts is expected behavior, not necessarily a regression in the product.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Engagement holds only while campaigns run | No owned trigger; reengagement depends on paid or earned channels | Build the permission moment and an owned channel — only owned triggers can prompt repeat use |
| Notifications sent but ignored | Not coupled to the moment the internal trigger fires, or the surface carries several competing actions | Time triggers to the emotional moment; one call to action per trigger |
| Signup completes, first session never repeats | Investment asked before any reward was delivered | Move every ask after the first reward, and stage it smaller |
| Strong launch, decay over weeks, content team exhausted | Finite variability, exhausted | Accept content production as a permanent cost line, or move the source of surprise to other users |
| Gamification added, nothing moved | Reward family does not match the motivation that brought users | Match reward type to the internal trigger; if there is no ongoing itch, mechanics cannot create one |
| Sharp drop right after a feature that changed a default or visibility | Reactance — a threatened sense of autonomy | Make it explicitly opt-in rather than defending the default |
| Users churn after one missed day or a broken streak | All-or-nothing mechanic on a behavior they do not independently want | Make lapses recoverable; attach to a behavior they already do voluntarily |
| Team cannot say what accrues to a user over time | No stored value — nothing makes leaving expensive | Pick one of content, data, followers, reputation, or skill and make its growth visible |
| No behavior distinguishes retained from churned users | Habit path not identified | Run the codify step properly before changing anything |
| Diagnosis lists improvements across all four phases | Constraint not identified | Return to the five-question triage and name one |
