---
name: screen-behavior-design-ethics
description: Decides whether an engagement or persuasion mechanic should be built at all, using a two-question screen (would I use this myself, and does it materially improve users' lives) that places the work as facilitator, peddler, entertainer, or dealer — then returns a go/modify/stop call, the specific mechanics that must change, and a duty-of-care requirement list to settle before launch. Use whenever a team is about to ship an engagement mechanic and someone is uneasy; when anyone asks whether a growth tactic, dark pattern, auto-opt-in default, streak, compulsion loop, or addictive mechanic is acceptable; when a designer asks whether they are manipulating users or whether the product is good for the people using it; when a team debates a default that exposes user activity, an invitation flow, notification volume, or monetizing compulsion; when someone asks what responsibility they owe heavy users; or when a founder or employee is weighing whether to keep working on something. Use it even when the question arrives as "is this evil?" or "I feel weird about this feature". For designing the loop, use design-engagement-loop; for diagnosing weak engagement, use diagnose-weak-engagement; for whether an idea is commercially worth pursuing, use find-habit-forming-opportunities; for winning a usability argument with stakeholders, use settle-usability-arguments.
---

# Should you build this?

This answers **"should I attempt to hook users?"** — not "can I". It is a decision-support tool for the moment before code is written, and it is deliberately blunt: it produces a placement, a recommendation, and a list of things that must change.

It does not tell you which businesses are moral in general or which will succeed, and it does not decide what can become habit-forming.

## Step 1 — Refuse the framing that the word settles it

Manipulation, defined neutrally, is *an experience crafted to change behavior*. By that definition an enormous amount of respected work manipulates — a structured weight-loss program is one of the most successful mass-manipulation products ever built, and few people question its morality. Meanwhile the same word applied to a game or an ad reads as damning.

So the question is never *whether* the product manipulates. It is under what conditions doing so is legitimate.

Two failure modes to head off before the discussion starts:

- **"All persuasion is manipulation, so nothing matters."** The label is not the argument. Move to the two questions.
- **"Everyone does this, so it's fine."** Also not the argument. Move to the two questions.

Feeling unsettled while reading a persuasion method is a good sign — it means the person is taking the power seriously. It is a reason to think, not a verdict.

## Step 2 — Answer the two questions, in writing

1. **Would I use this product myself?**
2. **Will this product materially improve users' lives?**

Both are answered by the maker. Nobody else can decide whether you would use it, or what "materially improving a life" means for what you are building.

**If you find yourself squirming, qualifying, or justifying an answer — that is a failed answer, not a nuanced one.** Write down the qualification you wanted to add; it is usually the real finding.

One accepted exception to the first question: you would have used it at an earlier stage of your life. An education product for teenagers is a legitimate case. But the further you are from that former self, the weaker the claim and the lower the odds of success. And if you are building for someone else's problem entirely, you cannot claim to be a facilitator without having experienced that problem firsthand.

## Step 3 — Place the work and name the consequence

|  | **Improves lives** | **Does not / cannot claim** |
|---|---|---|
| **Would use it** | **Facilitator** | **Entertainer** |
| **Would not use it** | **Peddler** | **Dealer** |

**Facilitator.** You use it and you believe it makes users' lives better. Proceed. This quadrant has the highest chance of success precisely because you understand the need firsthand — the designer always has direct access to at least one real user. The obligation that remains is the duty of care in Step 5.

**Peddler.** You believe it improves lives but you would not use it. Not immoral — plenty of people work on solutions for others out of genuinely altruistic motives. But the odds of designing well for a customer you do not know firsthand are depressingly low, and the characteristic output is a holier-than-thou product that gamifies a chore nobody wants to do, with generic badges and points that hold no value for the people receiving them. Advertising is the most common instance: teams convince themselves users will love the campaign, and the distortion field keeps them from asking whether they personally would find it useful. Either get inside the users' problem — live with them, do the job yourself — or stop.

**Entertainer.** You use it but cannot in good conscience claim it improves lives. This is art, and art matters on its own terms. But habits formed around entertainment fade fast, because the brain wants continuous novelty; today's hit becomes nostalgia. Building on ephemeral desire is running on a rolling treadmill. The consequence is a business shape, and it should be named out loud: the sustainable business here is not the game or the song or the book but an effective distribution system that gets goods to market while they are hot and keeps the pipeline full of fresh releases.

**Dealer.** You would not use it and you do not believe it improves lives. In the absence of both, the only reason to hook users is to extract money. There is money in it and someone will take it — the question is whether that someone is you. Casinos and dealers offer a good time right up until the dependency takes hold, at which point the fun stops.

## Step 4 — Apply the hard line

**Habits are not addictions, and the difference is the design limit.**

A habit is a behavior done with little conscious thought; it can be healthy or unhealthy, and most people carry many useful ones. An addiction is a persistent, compulsive dependency that is *self-destructive by definition*.

A product that depends on creating and maintaining addiction means intentionally harming people, regardless of the business result. That is out of bounds, and no quadrant placement rescues it.

The test is **harm to the user** — not frequency, not automaticity, not how much time is spent. Frequent is not the same as harmful.

## Step 5 — Audit the mechanics, not just the intent

A facilitator-quadrant product can still ship coercive mechanics. Check each of these specifically:

**Defaults that change what others can see about a user.** A service auto-enabled a feature revealing who had viewed which questions and answers; users lost the anonymity they had relied on for personal or awkward topics, revolted, and the company reversed within weeks and made it opt-in. If a feature ships enabled "because adoption would be too low otherwise", that low adoption is information about the feature.

**Invitation and sharing flows that depend on the sender not noticing.** Tricking users into inviting friends or broadcasting to their networks produces initial growth followed by collapse — when people discover they were duped they vent and stop using the product. The test: *would the sending user describe accurately what happened if asked afterward?* If the flow depends on them not noticing, remove it. Sustainable relationship triggers require a sender who genuinely wants to share the benefit — the strongest version makes the invitation itself carry value to the recipient.

**Requests with no easy decline.** Reactance is the hair-trigger response to a threatened sense of autonomy, and it kills engagement independently of product quality. Affirming the freedom to refuse disarms it: appending "but you are free to accept or refuse" to a request roughly doubled the likelihood of a yes, across a meta-analysis of 42 studies and more than 22,000 participants — in person and over email alike. **The coercive default is usually also the worse-performing one**, which is worth saying to a team that thinks ethics is a tax on growth.

**Mechanics whose only options are comply or quit.** A product demanding an unfamiliar discipline, where one lapse invalidates the period, leaves users nothing but those two choices, and they choose the second. Products that change behavior successfully present an implicit choice between the user's old way and a more convenient new way of meeting a need they already have. People must *want* to use the service, not feel they have to.

**Trigger volume set by revenue targets rather than by user moments.** Check what determines send frequency. If the answer is a number the business needs rather than a moment the user has, that is the finding.

**Rewards that do not match why users came.** Bolting on points and badges to drive a metric, where the mechanic holds no value for the user, is the peddler failure appearing inside an otherwise sound product.

## Step 6 — Write the duty-of-care requirements before launch

Roughly **1 percent** of users of even the most habit-forming technologies — machine gambling included — develop pathological dependency, and it concentrates in people with a particular psychological profile. That is a small fraction, and it is not zero, and dismissing it as too small to matter dismisses real harm.

The relevant fact is that companies now hold the data that could identify those users. Whether they act on it is a question of corporate responsibility.

So, before shipping:

1. **Define what usage pattern would count as harmful for this specific product.** Not "a lot" — a pattern you could write a query for.
2. **Instrument for it.**
3. **Decide what the product does when it detects that pattern**, and write it down.

For the overwhelming majority of users this will never be a problem; most people can self-regulate. The duty-of-care list is not an argument against building. It is the condition under which a facilitator can proceed with a clean conscience.

## Step 7 — Write the call

```markdown
# Should we build this: <mechanic or product>

## The two questions
- Would I use it myself: <yes/no + the qualification you wanted to add>
- Does it materially improve users' lives: <yes/no + how you know>

## Placement
<Facilitator / Peddler / Entertainer / Dealer> — <one sentence on why>

## Recommendation
<Go / Modify / Stop>

## Mechanics that must change
<Specific. Each with the coercion it removes.>

## Duty of care, to settle before launch
- Harmful usage pattern for this product:
- How it will be instrumented:
- What the product does when it detects it:

## What this does not cover
<Legal and regulatory constraints, which are out of scope here and have moved
considerably; name who needs to review them.>
```

State the recommendation plainly, including the case where the honest answer is that the person should stop working on it.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| The team justifies a mechanic by pointing at a hypothetical user who might like it | Peddler quadrant with a distortion field | Ask each person whether *they* would use it this week. Treat evasion as a no |
| The discussion collapses into "everything is manipulation" | Treating the label as the argument | Restate manipulation neutrally, move to the two questions |
| Ethics review consists only of a legal check | Duty of care never defined | Write the harmful-usage definition and the product's response before launch |
| A feature ships auto-enabled because opt-in adoption would be low | Coercion dressed as a default | Make it opt-in. Low opt-in is information |
| Revenue design quietly targets the heaviest 1 percent | Dealer behavior inside a facilitator product | Separate revenue design from dependency; instrument for harm |
| Only the product's intent is reviewed, never its mechanics | Good intentions used as a blanket clearance | Run Step 5 mechanic by mechanic |

## A position you will encounter

Some practitioners hold that it is acceptable to deceive people if it is in their best interests, or if they have given implicit consent to be deceived as part of a persuasive strategy. Others in the field have proposed a formal ethical code of conduct instead.

Present this as a live disagreement rather than settled doctrine. The method above does not endorse the deception position; it puts the burden on the maker to answer both questions honestly and to name what changes.

## Scope note

This screen predates current regulation of dark patterns, engagement design aimed at minors, notification and consent rules on major platforms, and data-protection law. Those have moved considerably and are **out of scope here**. Passing this ethical screen is not a compliance review, and the output should say so and name who needs to run one.
