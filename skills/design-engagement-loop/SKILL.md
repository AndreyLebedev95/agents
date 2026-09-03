---
name: design-engagement-loop
description: Designs the engagement loop that brings people back to a product on their own — the trigger that fires, the smallest action, the reward that varies, and the user investment that loads the next trigger — and produces a written loop spec with a chosen mechanism and rationale per phase. Use whenever someone is designing for repeat use, retention, stickiness, daily engagement, or habit formation; asks how to get users to come back, what belongs in a notification or push, where a streak, reward, points, or badge system should go, whether to add gamification, or how onboarding should set up the second visit. Use it even when the request is only "how do we make this sticky" or "we need people using this every day", and even when nobody says the word habit. For a shipped product whose engagement is already weak or falling, use diagnose-weak-engagement instead. For whether the loop should be built at all, use screen-behavior-design-ethics. For finding the opportunity before there is a product, use find-habit-forming-opportunities. Not for screen-level clarity, wording, or navigation — those are review-screen-for-friction, edit-interface-copy, and audit-navigation-and-landing.
---

# Design an engagement loop

Products people return to unprompted are not lucky. They run a four-phase loop, repeatedly:

**trigger → action → variable reward → investment → (loads the next trigger)**

Each pass strengthens the association between a feeling the user already has and your product. Your job here is to specify that loop concretely — not to describe it, but to decide the actual mechanism at each phase and say why.

The deliverable is a loop spec. Read `references/loop-spec-template.md` before writing it.

## Step 0 — Screen: does this product need a loop at all?

Ask whether the business genuinely depends on ongoing, unprompted engagement, or whether a single purchase completes the relationship. Insurance policies, appliances, and one-off professional services do not need habits; they need sales, referral, and advertising. Forcing a loop onto a low-frequency product produces nagging and wastes the team's time.

If the honest answer is that this product does not run on repeat use, say so now and stop. That is a useful result.

## Step 1 — Intake

Answer these before designing anything:

1. What habit does the business model actually require?
2. What problem are users turning to this product to solve?
3. How do they solve it today, and why does that need replacing?
4. How frequently do you expect engagement — realistically?
5. What single user behavior do you want to make automatic?

If question 1 has no answer, loop design is the wrong project.

## Step 2 — Find the internal trigger

External triggers start habits. Internal triggers sustain them. An internal trigger is an emotion, thought, or existing routine that summons your product from memory with no prompt in the environment — the "what to do next" lives in the user's head as a learned association. A product still dependent on prompting has not formed a habit.

**Write a user narrative first.** One named person, one place, one moment, in prose that reads like a scene. Not a bullet list of needs. Circulate it for editing across roles — when everyone can relate to the same story, prioritization falls out of it instead of out of feature negotiation.

**Then ask why until you reach an emotion.** Users cannot name what motivates them, so surveys and direct questions fail here. Start from the narrative and repeat "why?" — usually about five times — until the answer is a feeling rather than a task.

> Why would she use email? To send and receive messages. Why? To share information quickly. Why? To know what is going on with her coworkers and family. Why? To know if someone needs her. Why? **She fears being out of the loop.**

That last answer is what you design for. Different starting narratives yield different chains — you are producing a hypothesis to test, not a proof.

**Aim at frequent, low-intensity discomfort.** Boredom, loneliness, frustration, confusion, indecisiveness, fear of losing a moment, fear of missing out. Negative emotions are the strongest internal triggers, and the discomfort is usually minor and below conscious awareness — which is exactly why the reaction is automatic. Positive-sounding needs normally decompose into relief of a negative state: entertainment relieves boredom, sharing good news maintains connection.

**State the pain in emotional terms, never as a missing feature.** A pain stated as a feature gap produces a feature. A pain stated as an emotion produces something people reach for.

**Design from what people do, not what they say.** Declared and revealed preferences differ systematically, and the gap between them is where the opportunity is, not a research error to reconcile.

## Step 3 — Design the external trigger

External triggers come in four kinds. Only one of them builds habits:

| Kind | Examples | What it does |
|---|---|---|
| Paid | advertising, search marketing | Acquires. Paying for reengagement is unsustainable for almost every business model |
| Earned | press, viral moment, store featuring | Acquires. Short-lived and unpredictable; requires staying in the limelight |
| Relationship | word of mouth, invitations, shares | Acquires. Powerful, but see the sharing caution below |
| **Owned** | app icon, subscribed email, push notification | **The only one that can prompt repeat engagement**, because it occupies space in the user's environment with their tacit permission |

So: **check whether any owned trigger exists at all.** If repeat visits depend on paid or earned triggers, the loop cannot close, and the whole design must include the moment where the user grants that permission — signup, install, opt-in — as a deliberate designed step, not an afterthought.

Then, on the trigger surface itself:

- **One next action.** A trigger carries the information for exactly one thing to do. More options force evaluation, and too many or irrelevant choices cause hesitation, confusion, or abandonment. An account-alert email that could offer balance checks, card deals, and goal-setting instead reduces to a single login click.
- **Lean on learned affordances.** Links are for clicking and icons are for tapping; that information is already embedded. Spend explicit wording only where the affordance is not already known.
- **Couple it in time to the internal trigger.** The trigger should arrive at or just before the moment the user's emotion fires — not on a schedule that suits your send calendar.

Complete this sentence as part of the spec: *"Every time the user [internal trigger], he/she [first action of the intended habit]."* Then ask where and when an external trigger can sit closest to that firing moment.

Useful stretch: list three conventional triggering channels, then three currently impossible ones. The impossible ones break channel assumptions and are sometimes closer than they look.

## Step 4 — Design the action

The action is the *simplest* behavior done in anticipation of a reward. Doing must be easier than thinking.

**Behavior needs three things at once: motivation, ability, and a trigger.** All three present, in sufficient degree, at the same moment — or nothing happens. This is why a missed phone call decomposes cleanly: buried in a bag (ability), assumed telemarketer (motivation), ringer silenced (trigger).

**Spend on ability before motivation.** This is the single highest-leverage rule in this phase. Raising desire is expensive and slow — people ignore explanatory text, they are multitasking, and they have little patience for being told why they should act. Reducing effort works better. The target is a product so simple that users already know how to use it.

**Remove steps.** Understand why people use the thing; lay out every step from intention to outcome, including steps outside your product; then delete steps until nothing more can go. Take a desire that has existed for a long time and use current technology to take out steps. Adoption tracks step count, not feature count.

**Attack the scarcest resource.** Difficulty is a function of six factors — time, money, physical effort, brain cycles, social deviance, and how far the action departs from existing routine. Simplicity is not absolute: it is whichever of these six the specific user is scarcest in at that moment. Federated login removes steps for the time-starved and adds anxiety, therefore brain cycles, for the privacy-wary. Ask what one missing thing would let this user proceed to the next step, and remove that.

Details, including the three core motivators and the four cognitive biases worth designing with: `references/motivation-and-ability.md`. Read it while working this phase.

Two things worth knowing here that read backwards:

- **A hard constraint can raise ability.** A limit that looks restrictive can cut brain cycles — capping message length removes the question of what to write and how much effort to spend, turning composition into a few taps.
- **Optimize for the action that predicts retention, not the one people do most.** If a rarer early behavior correlates with users still being active later, redesign the entry surface around that behavior even though the funnel currently pushes something easier.

On the entry surface, reduce to one or two calls to action and let the product persuade. Getting users to experience the service beats arguing them into it from outside.

Where the underlying content or task is long and daunting, chunk it into small daily units, put the interesting material first and the tedious parts later, and offer alternate modalities that remove effort for some users. When someone misses the first unit, offer an easier plan rather than repeating the same prompt.

## Step 5 — Design the variable reward

A feedback loop alone creates no desire. The fridge light comes on every time and nobody keeps opening the door. Craving appears only when the response is uncertain.

**The target is anticipation, not the payload.** Reward-region brain activity spikes *before* the payout, not on receiving it. What compels action is the need to relieve the craving. Making the reward bigger does less than making its arrival uncertain.

**Predictability kills attention.** Once a causal relationship is understood, the brain stores it and stops attending. Interest returns when something breaks the expected pattern. Sustaining engagement needs ongoing novelty, not a one-time delight.

**Three families of reward — pick from them deliberately:**

- **Tribe** — social: feeling accepted, attractive, important, included. Validation from other people, arriving unpredictably.
- **Hunt** — pursuit of resources and information. The chase itself is the compelling part.
- **Self** — mastery, competence, completion, consistency, sought for its own sake.

Read `references/reward-types.md` for the design patterns and cautions for each, and for the finite-vs-infinite variability decision.

Two constraints on this phase:

- **What varies must be the reward, never the product's reliability.** Users must be able to depend on the product as the solution; an unpredictable interface breaks ability instead of creating craving.
- **The reward must satisfy and still leave something open.** A reward that fully closes the loop ends the relationship; one that never satisfies extinguishes the behavior. Conflict, mystery, resolution — with the next question opened before the current one closes.

Decide now whether your variability is **finite** (it runs out once the user has seen it — a story, a game played to completion, consumed content) or **infinite** (other people supply the unpredictability — multiplayer, user-generated content, community response). Finite is not inferior, but it makes continuous content production a permanent cost line rather than a launch cost.

## Step 6 — Design the investment

The investment phase deliberately **increases** friction. That contradicts the usual rule that everything should be effortless, and the contradiction resolves entirely on timing.

**Ask for work only after the user has received a reward.** People primed by receiving something are primed to reciprocate — this holds even toward software, not just toward people. Placing the ask before the reward is one of the most common and most expensive mistakes in this whole method.

The investment is about *anticipation of longer-term rewards*, so it correctly carries no badge, star, or instant payoff. Following someone gives you nothing today; it makes tomorrow better.

**Why a bit of user work makes the product more valuable, even when it makes it objectively harder:** people irrationally value what they made themselves; they act consistently with what they have already done; and they change their preferences to avoid the discomfort of contradiction. Together these produce rationalization — the user builds reasons for behavior someone else designed. People who folded their own origami valued it about five times higher than uninvolved bidders, close to the valuation of expert work.

**Start tiny and escalate.** Small prior commitments massively raise compliance with larger later ones: 17% of residents accepted a large ugly yard sign cold, and 76% accepted it after having agreed to a small window sign two weeks earlier. Stage the investments you want into chunks, easiest first, escalating across successive cycles. If users are not investing, the ask is too large — halve it rather than pushing harder.

**Choose what accrues.** Stored value comes in five forms, all of them non-transferable, which is what makes leaving expensive:

| Form | What it is | Note |
|---|---|---|
| Content | items the user adds or aggregates | A library or archive of their own past |
| Data | information supplied actively or passively | Even a little entered information sharply raises return likelihood |
| Followers | a curated network, both directions | Who you follow improves what you receive; who follows you cannot be moved |
| Reputation | a quality score with economic consequence | Binds hardest in marketplaces |
| Skill | learned expertise | Also moves the user rightward on ability, since familiarity cuts the non-routine cost |

Pick the one your product structurally supports and deepen it rather than adding all five. Value the user cannot feel accruing does not bind them.

**Load the next trigger.** The second job of investment is to earn both the right and the timing to come back: get the connection or permission as part of the investment itself, then fire the trigger at the moment the internal trigger is most likely to arrive. A task app asks for calendar access during onboarding and then notifies right after a meeting ends — exactly when the anxiety about forgetting a follow-up fires. Prefer triggers generated by another person's action; those arrive naturally and unpredictably. Measure the delay between loading and firing, and shorten it.

## Step 7 — Close and check

Run the five questions. The first one you cannot answer concretely is the phase you have not designed:

1. What do users really want? What pain is the product relieving? *(internal trigger)*
2. What brings users to the service? *(external trigger)*
3. What is the simplest action taken in anticipation of reward, and how can it be made easier? *(action)*
4. Are users fulfilled by the reward yet left wanting more? *(variable reward)*
5. What bit of work do users invest? Does it load the next trigger and store value? *(investment)*

Then state what to test first, and how long a loaded trigger takes to bring users back.

## Rules that override local optimization

- **Preserve autonomy.** Reactance — the hair-trigger response to threats to autonomy — kills engagement regardless of product quality. Never auto-enroll users into anything that changes what others can see about them; a product that did this faced a revolt and reversed within weeks. Phrase asks so declining is easy: appending "but you are free to accept or refuse" to a request roughly doubled compliance across 42 studies and 22,000 participants. The manipulative default is usually also the worse-performing one.
- **Ride an existing behavior; do not demand a new discipline.** A product that requires an unfamiliar routine leaves users only two options — comply or quit — and they quit. Find something they already do voluntarily and enjoy, make that easier and more rewarding first, and introduce goal-specific features as engagement deepens. Watch for all-or-nothing mechanics: a system where one lapse invalidates progress guarantees churn.
- **Design around daily engagement** when habit is the whole strategy — plans, triggers, and content units all sized so daily is the default rather than an aspiration.
- **There is no habit timescale.** Formation ranges from a few weeks to more than five months depending on the behavior's complexity and its importance to the person. Design for repetition rate; reject any plan built on a fixed day count.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Points, badges, leaderboards added; engagement does not move | Reward family does not match the motivation that brought users | Name the internal trigger first, then pick a reward of the same family. If there is no reason for a second visit, mechanics cannot manufacture one — fix the product |
| Reengagement depends on campaigns and lifecycle email | No owned trigger exists | Design the permission-granting moment into the loop |
| Reward is generous but attention fades anyway | Finite variability, exhausted | Move the surprise to other users, or budget content production as a permanent cost |
| Signup, profile, or invitations requested before anything is delivered | Investment placed before the reward | Move every ask after the first reward |
| Onboarding funnel fully optimized, retention flat | The optimized action is not the one that predicts retention | Find the behavior correlated with staying and redesign around it |
| Users churn after one missed day | All-or-nothing mechanic on a behavior they do not independently want | Make lapses recoverable; attach to an existing voluntary behavior |
| Trigger surface offers several equally weighted actions | Trigger carrying more than one instruction | Cut to one call to action |
| Plan assumes "21 days to build a habit" | Universal timescale that does not exist | Design for frequency, not for a deadline |
