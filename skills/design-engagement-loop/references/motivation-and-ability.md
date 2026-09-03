# Motivation and ability — working the action phase

Read while designing or repairing the action phase of a loop.

## Contents
- [The three-ingredient test](#the-three-ingredient-test)
- [The three core motivators](#the-three-core-motivators)
- [The six elements of simplicity](#the-six-elements-of-simplicity)
- [Removing steps](#removing-steps)
- [Four biases worth designing with](#four-biases-worth-designing-with)
- [Chunking a daunting task](#chunking-a-daunting-task)

## The three-ingredient test

A behavior occurs when motivation, ability, and a trigger are present at the same moment and in sufficient degree. If any one is missing or inadequate, the user does not cross the action line and nothing happens.

This makes failure diagnosable. For any action that is not happening, exactly one of the three is the binding constraint:

1. **Trigger** — was a cue present at that moment at all?
2. **Ability** — how many steps, how much time, money, effort, or thought does it take?
3. **Motivation** — does the user want the outcome *at that moment*?

Fix the missing ingredient rather than adding more of the ones already present. This diagnoses a single discrete action, not a whole product — so name the specific behavior before applying it.

The canonical decomposition is an unanswered phone call. Buried in a bag: ability. Assumed to be a telemarketer: motivation. Ringer silenced: trigger. Same outcome, three unrelated causes, three unrelated fixes.

## The three core motivators

Motivation is the energy for action. It reduces to three pairs, each with a positive and a negative pole:

| Seek | Avoid |
|---|---|
| Pleasure | Pain |
| Hope | Fear |
| Social acceptance | Rejection |

Both poles are levers. Fear and rejection are genuinely powerful — a public-health campaign showing the consequences of not wearing a helmet works on avoidance — but they carry ethical and brand cost, so treat them as deliberate choices rather than defaults.

What motivates one audience will not motivate another. Pick the pair against a specific target user, not against the design team's assumptions about people in general.

Note the division of labor: the internal trigger is the frequent everyday itch; the motivator is the promise of the desirable outcome — the satisfying scratch. They are not the same thing and both must be present.

## The six elements of simplicity

Task difficulty is a function of six factors:

- **Time** — how long the action takes.
- **Money** — its fiscal cost.
- **Physical effort** — the labor involved.
- **Brain cycles** — mental effort and focus required.
- **Social deviance** — how accepted the behavior is by others present.
- **Non-routine** — how much it departs from what the user already does.

The operative move is not "make it simpler" in general. **Simplicity is a function of whichever resource the specific user is scarcest in at that moment**, and that differs by person and context. There is no one-size-fits-all simplification: federated login removes steps for the time-starved and adds anxiety — and therefore brain cycles — for the privacy-wary.

So the question to ask, per user segment and per moment, is: *what is the one thing that is missing that would let this user proceed to the next step?* Remove that specific obstacle.

Worked prompts:

- Is the user short on time?
- Is the behavior too expensive?
- Is the user exhausted after a long day?
- Is the product too difficult to understand?
- Is the user somewhere the behavior would look inappropriate?
- Is the behavior so far from their normal routine that its strangeness puts them off?

## Removing steps

Three-step method:

1. Understand why people use the product or service. State the underlying desire in terms that would have been true decades ago — the durable human want, not the feature.
2. Lay out every step the customer must take to get the job done, including steps that happen outside your product.
3. Remove steps until you reach the simplest possible process.

Any product that significantly reduces the steps to complete a task enjoys high adoption. The historical pattern in online publishing is a clean demonstration: self-hosting with domains, DNS, and a content system → register an account and post → type a short status → tap once to share a photo. At each step removal, the share of people creating rather than only consuming rose.

The framing worth keeping: *take a human desire that has been around a long time, and use current technology to take out steps.*

**A constraint can raise ability.** A hard limit that critics read as restrictive can increase the user's capacity to act by cutting the brain cycles required — a length cap removes the question of what to produce and how much effort to spend. This only works when the scarce resource is mental effort or time. A constraint that blocks the user's actual goal is friction, not simplification.

**Entry surfaces:** optimize for getting people into the product, not for persuading them outside it. Reduce to one or two clear calls to action, replace explanatory copy that demands comprehension with the shortest statement of what the user gets, and move persuasion inside where the reward can do it.

## Four biases worth designing with

Motivation and ability move on perception as well as on fact. These are tendencies, not laws — the exceptions to the rational model — so test rather than assume the effect transfers.

**Scarcity.** Identical items are valued more when supply appears low. Cookies in a near-empty jar were rated more valuable than identical cookies in a full one. The second half of that experiment is the more useful finding: a product that starts scarce and becomes abundant ends up valued *lower* than one that was always abundant.

**Framing.** Context changes perceived pleasure independent of objective quality, and not only self-reported pleasure — as stated wine prices rose from $5 to $90, enjoyment rose and so did activity in pleasure-associated brain regions, though the wine was identical throughout. A world-class violinist busking in a subway station goes unnoticed.

**Anchoring.** People fixate on one attribute and stop comparing. A discount label on a three-pack can carry the whole decision while an undiscounted five-pack of the same thing is cheaper per unit.

**Endowed progress.** Motivation rises as people believe they are nearing a goal, so granting progress up front raises completion. Two groups needed the same eight purchases for a free car wash: one got a blank eight-square card, the other a ten-square card with two squares already punched. The pre-punched group had an **82 percent higher completion rate**. Applied to profiles and onboarding: start the user partway, show advancement, and omit the numeric scale so the goal always looks near without ever quite arriving.

There are hundreds of such biases; these four are the ones with the most direct product application. Manufactured scarcity that is untrue is deception, not design.

## Chunking a daunting task

When the underlying content or task is long and intimidating:

- Split it into units small enough to finish in a few minutes.
- Structure them as a named plan with **daily** as the unit — not weekly, not self-paced.
- Put the interesting material first and the tedious material later. Reordering this way measurably raises completion.
- Offer alternate modalities where they remove effort for some users (audio instead of reading, for instance).
- When someone misses the first unit, offer an easier plan rather than repeating the same prompt.

The point is to keep attention on the small task at hand and avoid the intimidation of the whole, which is what makes people give up.
