# Reward types — choosing and designing the variable reward

Read when choosing, strengthening, or repairing the reward phase.

## Contents
- [Why variability at all](#why-variability-at-all)
- [Tribe](#tribe--social-rewards)
- [Hunt](#hunt--pursuit-of-resources-and-information)
- [Self](#self--mastery-competence-completion)
- [Stacking all three](#stacking-all-three)
- [Finite vs infinite variability](#finite-vs-infinite-variability)
- [Sharing is itself a reward](#sharing-is-itself-a-reward)
- [When rewards fail](#when-rewards-fail)

## Why variability at all

Predictable feedback creates no desire. Intermittent reinforcement dramatically increased lever-pressing in pigeons compared with a reward on every press, and the same mechanism runs in people: variability raises activity in the brain's reward region and drives the search for more.

Two facts shape every decision below:

- **Craving comes from anticipation, not receipt.** Reward-region activity spikes in anticipation of a payout rather than on getting it. Design the anticipation gap, not a bigger payload.
- **Understood patterns stop being attended to.** A child delighted by a new dog stops noticing it once its behavior is predictable. Products need ongoing novelty, not one delightful moment.

## Tribe — social rewards

The search for rewards driven by connectedness: feeling accepted, attractive, important, included. Validation from other people, arriving on an unpredictable schedule.

Design patterns:

- Make the reward for a behavior **visible to others**, not private. Observing someone rewarded for a behavior changes the observer's own beliefs and actions.
- **Segment so the visible earners are peers or near-peers** — people like the viewer, or only slightly more experienced, so they read as role models rather than distant stars. This is why interest- and demographic-level segmentation matters in social products.
- **Keep the arrival unpredictable.** Guaranteed validation stops being a reward. Nobody knows how many upvotes an answer will attract, and that uncertainty is what turns a mundane contribution into an engaging one.
- **Make points represent something real.** Where reputation scores stand for actual contribution to a community the contributor cares about, they work; empty game mechanics do not.

A worked variant: an online game with a hostile player community introduced player-conferred honor points for sportsmanlike conduct. The count was highly variable and could only be awarded by other players, which made it a coveted status marker and simultaneously signalled which players to avoid. The reward mechanism doubled as a moderation mechanism.

Requires enough population density in a segment for peers to be visible at all.

## Hunt — pursuit of resources and information

The oldest of the three. Persistence hunting — running prey to exhaustion over hours before any reward exists — is the evolutionary root: the pursuit itself drives the behavior.

Design patterns:

- **Mix genuinely valuable items into the stream at an unpredictable rate** rather than front-loading the best. A feed of mixed mundane and relevant content produces an uncertain payoff per unit of scrolling, which is the entire mechanism.
- **Make one more unit of pursuit cost nearly nothing** — a scroll, a flick, an automatic load rather than a click and a wait.
- **Show a partial reveal at the boundary.** Content cut off at the fold gives a glimpse of what is ahead; relieving that curiosity requires only continuing. Curiosity, not obligation, should drive the next step.

Requires enough content density that the hit rate is non-zero. A stream that is reliably empty extinguishes the behavior.

## Self — mastery, competence, completion

Intrinsic rewards: the drive to gain a sense of competency, to conquer an obstacle, to finish a thing — pursued even when the process is visibly unpleasant, as anyone watching someone swear their way through a jigsaw can confirm. Adding mystery to the goal makes the pursuit more enticing.

Design patterns:

- **Break the task into units small enough to give feedback within seconds.** Interactive coding lessons that return pass/fail on a single function turn a tedious learning path into a game; writing whole programs before any feedback does not.
- **Make each unit's outcome genuinely uncertain** — sometimes success, sometimes failure. Learning is full of errors, and that variability is an asset here rather than a defect.
- **Show progression and unlock capability** as competence rises.
- **Give the user a reachable completion state** rather than an infinite backlog. An email client that manufactures more frequent moments of a cleared inbox delivers a feeling of mastery that clients with identical functionality do not — partly by deferring low-priority items out of sight and resurfacing them later.

**Streaks** apply endowed progress to retention: a visible chain of completed days makes skipping feel like breaking something already built, and pairs well with an explicit per-session completion affirmation. Keep the unit small enough that the streak is genuinely sustainable — a streak that is easy to break and impossible to repair converts directly into abandonment.

## Stacking all three

Many of the most habitual products deliver all three at once. Email is the canonical case:

- Uncertainty about who is writing, plus social obligation to reply → **tribe**
- Uncertainty about opportunities or threats in the contents → **hunt**
- The fluctuating unread count as a task to conquer → **self**

Auditing an existing product against all three separately often reveals a reward channel already latent in it. Strengthen the latent one before inventing a new mechanic.

## Finite vs infinite variability

**Finite variability** becomes predictable with use. A story with a resolved plot, a game played to completion, consumed content of any kind. Once seen, the source of surprise is gone — and a rewatch never reaches the original level of engagement.

**Infinite variability** sustains itself with use, almost always because *other people* supply the unpredictability: multiplayer play, user-generated content, community response, creation rather than consumption.

Finite-variability businesses are not inferior. They operate under a different constraint: continuous content production is a permanent cost line, not a launch cost, which is precisely why studio models exist — a deep-pocketed backer funds a portfolio, uncertain which title becomes the hit.

Two consequences worth stating explicitly in a spec:

- **Do not franchise a hit by reskinning it.** The reskin inherits the exhausted variability, not the novelty. A social-game company cloned its breakout title into several near-identical products; players lost interest and the stock fell over 80 percent within eight months of a peak valuation.
- **Content consumption is finite; content creation is infinite.** A platform where contributors post work for feedback from other contributors changes as its community's trends change, and never runs out.

Even infinite variability does not hold users forever — the next thing arrives — but it does not require reinvention just to keep pace.

## Sharing is itself a reward

Disclosing information about oneself is intrinsically rewarding and engages reward-associated mechanisms; in one line of research people were willing to forgo money in order to disclose about themselves.

So a share action is not only a growth mechanism, it is a reward for the sharer — especially when the shared item portrays them favorably. Design the shared artifact so that sending it flatters the sender, place the action where the user has just experienced something worth attaching their name to, and do not gate sharing behind registration; unregistered users still drive growth.

This is distinct from dark-pattern sharing: the sender must want the share and must know it happened.

## When rewards fail

Variable rewards are not fairy dust sprinkled on a product to make it attractive. The reward must fit the narrative of why the product is used and align with the user's internal trigger.

The instructive failure: a Q&A site paid cash bounties for answers, peaked around 14 million monthly visitors, and lost them; a competitor paying nothing but running an upvote system grew. People do not come to a knowledge community to earn a wage — if that were the trigger, they would be better off working an hourly job — and as a game mechanic the payouts arrived far too rarely and too small to reinforce anything. Peer recognition was more frequent and more salient.

The same failure explains most disappointing gamification. Points, badges, and leaderboards work only when they scratch the actual itch, and fail entirely when there is no ongoing itch at all — when the product gives no reason to return, no mechanic can manufacture one.

Checks before adding any reward:

1. State the internal trigger this reward is supposed to relieve.
2. Confirm the reward is the same family (tribe / hunt / self) as the motivation that brought the user.
3. Check the rate: frequent and salient enough to reinforce, or too rare and too small?
4. If the product has no reason for a second visit, stop and fix the product.
