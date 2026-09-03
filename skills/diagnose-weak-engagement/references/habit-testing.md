# Habit testing — identify, codify, modify

Read when there is a live product with real usage data. This is a build–measure–learn loop applied specifically to habit formation: it tells you who your devotees are, which parts of the product (if any) are habit forming, and why those parts change behavior.

Habit testing does not strictly require a live product, but drawing clear conclusions without a comprehensive view of how people use the system is hard. The steps below assume a product, users, and meaningful data.

## Step 1 — Identify

The opening question is: **who are the product's habitual users?**

**Define what devoted means before looking at your data.** How often *should* someone use this product? The answer changes everything downstream, and it is the step teams most often skip or fudge.

- Anchor on publicly available data from similar products or solutions.
- If no data exists, make an educated assumption — but be realistic and honest, and write it down as an assumption.
- **Do not set the bar from your own power users.** An overly aggressive prediction that only accounts for extreme users produces an unreachable threshold and hides real habit formation. You want a realistic guess at how often a *typical* user would interact.

Calibration examples: a social feed should expect habitual users multiple times per day. A product tied to an occasional external event — deciding what film to watch, say — should not expect more than once or twice a week, because the visits arrive on the heels of that event.

**Then count.** How many users, and which type, meet the threshold? Use cohort analysis, so changes in behavior across future product iterations are visible rather than averaged away.

**The 5 percent rule of thumb.** If at least 5 percent of users do not find the product valuable enough to use as often as you predicted, either you identified the wrong users or the product needs to go back to the drawing board. This is deliberately a low bar — the active rate needed to sustain a business is much higher. It answers "is any habit forming at all", not "is this working".

## Step 2 — Codify

You have a set of users who meet the criteria. Now find out what hooked them.

Users interact with a product in slightly different ways, and the way each one engages leaves a recognizable fingerprint even when there is a standard flow. What to sift for:

- Where they came from — acquisition source, referrer, invitation vs organic.
- Decisions made during registration — what they filled in, what they skipped, what they chose.
- Network size — how many connections, follows, friends, or collaborators they had, and when.
- The order in which they did things during the first sessions.
- What they did *not* do that churned users did.

**You are looking for a habit path: a series of similar actions shared by your most loyal users.**

Every product has a different set of actions that devotees take. The goal is to determine which of those steps is *critical* for creating devoted users, so the experience can be modified to encourage that behavior specifically.

The canonical finding: a social service discovered that once new users followed thirty other members, they hit a tipping point that dramatically increased the odds they would keep using the site. That number is specific to that product — the transferable part is the shape of the finding, a threshold on a single early behavior, not the number thirty.

Cautions when reading a candidate habit path:

- Correlation runs both ways. Users who were going to retain anyway may perform the behavior *because* they were engaged. The modify step is what tests causation — if pushing new users down the path moves retention, the path was causal; if it does not, it was a symptom.
- A habit path that only your largest, oldest, or most technical accounts can travel is not a path for new users.
- If no behavior distinguishes retained from churned users, the honest output is "not identifiable yet" plus a list of what to instrument. Do not invent one.

## Step 3 — Modify

Revisit the product and find ways to nudge new users down the same path devotees took. Typical changes:

- Updating the registration or onboarding funnel.
- Changing content or defaults so the critical behavior happens sooner.
- **Removing** a feature that pulls new users off the path.
- Increasing emphasis on an existing feature rather than building a new one.

The service that found the follow-thirty threshold rebuilt its onboarding to push new users to start following others immediately — rather than optimizing the action most new users were already performing, which turned out not to predict retention.

Then evaluate: track users by cohort and compare their activity against the habitual users' pattern. That comparison, over successive iterations, is what should guide how the product evolves.

Habit testing is continual — run it with every new feature and product iteration, not once.

## Related metrics worth reading as evidence

These are not part of the three steps but are diagnostic signals the same investigation can use:

- **Price sensitivity.** As users form routines around a product they depend on it and become less sensitive to price. How much agony a business goes through raising prices is therefore a measure of how habitual usage really is — painful increases signal a weak habit, not just a tough market.
- **Cohort payment curves.** Willingness to pay rises with habituation, so a monetization curve that dips and then climbs across cohort age is evidence the habit is forming. One service reported roughly 0.5% of users paying after the first month, about 11% by month 33, and about 26% by month 42. Asking for money before the routine exists suppresses both conversion and habit formation.
- **Invitation interval.** Where a user's normal activity naturally exposes other people, the time between joining and producing an invitation compounds: at a two-day cycle, twenty days yields roughly twenty thousand users; at a one-day cycle, over twenty million. Attack that interval before attacking top-of-funnel acquisition.

## What this method cannot tell you

- Whether the product *should* form habits — that is a separate ethical question.
- Whether an inherently infrequent product is failing. Run the frequency-and-utility screen first; a behavior that occurs a few times a year will fail habit testing by construction.
- Anything reliable from a product whose usage is mostly campaign-driven. Split prompted from unprompted sessions before any of the above.
