---
name: find-habit-forming-opportunities
description: Finds and screens product opportunities that people would return to on their own — hunting in four places (your own unmet needs, nascent behaviors among early adopters, new enabling technology, and interface shifts) and then screening each candidate on frequency against perceived utility, the routine it must displace, and the improvement multiple it needs. Returns a shortlist with a pursue/park/kill call and the reason recorded. Use whenever someone is looking for a product idea or a new bet; asks whether an idea has legs or whether users would come back; asks whether something is a vitamin or a painkiller; is weighing a niche behavior that looks like a toy; asks where the opportunity is in a new platform, device, or interface shift; is deciding whether to enter a market that already has an entrenched incumbent; or asks whether their product needs to be habit-forming at all. Use it even when the request is only "is this idea any good?" in a repeat-use context. For designing the loop once the bet is made, use design-engagement-loop. For a shipped product with weak engagement, use diagnose-weak-engagement. For the ethical go/no-go, use screen-behavior-design-ethics. Not for usability evaluation of an existing design (review-screen-for-friction) or for testing with participants (run-diy-usability-test).
---

# Find habit-forming opportunities

Two jobs, usually done together: **generate** candidate opportunities, and **screen** them so the weak ones die cheaply and the reason is recorded.

Generation is where most teams are weakest — they survey markets and never observe behavior. Read `references/opportunity-hunting.md` when generating; the screen below is what to run on whatever comes out.

## Generating candidates

Four hunting grounds, in rough order of yield:

**1. Your own unmet needs.** You always have direct access to at least one user. Reframe the question from *"what problem should I solve?"* to **"what problem do I wish someone else would solve for me?"** Track your own workarounds — the notepad, the manual step, the spreadsheet, the thing you do twice because no tool does it once. Notice where an existing product forces you to specify more than you care about. Build the version you would use.

**2. Nascent behaviors among early adopters.** Find something a small group already does enthusiastically without being told to, and ask whether the need underneath is narrow or fundamental.

**3. New enabling technology.** Wherever something suddenly makes a behavior easier, possibilities open. Ask specifically where the shift makes cycling through an engagement loop faster, more frequent, or more rewarding.

**4. Interface change.** Often no technology change is needed at all — only a change in how people interact with what already exists. Historically the largest returns here came from small teams solving common interaction problems, not hard technical ones.

When the list is thin, run the field exercise in the reference: a week of logging your own triggers, then three people outside your social circle showing you their phone's first screen.

## Screening a candidate

### 1. Does it need to be habit-forming at all?

Not every business does. Where a single purchase completes the relationship — a policy bought, an appliance installed, a one-off service delivered — the money goes to sales, referral, and advertising, not to loop design. Ask whether the business model requires ongoing unprompted engagement before assuming it does.

### 2. Plot frequency against perceived utility

Two axes: **how often would this behavior occur**, and **how useful does it seem relative to the user's current solution** — not relative to nothing.

The threshold curve slopes down but never touches the utility axis, and the asymmetry is the whole finding:

- An **inherently infrequent** behavior never becomes automatic no matter how much value it delivers. It stays a conscious decision every time.
- A behavior with **minimal perceived benefit** can still become habitual purely on frequency.

**Frequency is the axis that cannot be substituted.** Very frequent search is barely better than its rivals per query and is still a habit; one-stop retail is far less frequent and clears the bar on utility instead. If frequency is structurally low for your candidate, the honest call is that this product does not run on habit — which is information, not a rejection.

The scale is deliberately unmarked: there is no universal answer to how frequent is frequent enough, and it is specific to each business and behavior. What is known is that higher frequency is better, and that habit formation has no fixed timescale — it ranges from a few weeks to more than five months depending on the behavior's complexity and how much it matters to the person. Reject any plan built on a fixed day count.

### 3. Name the routine it must displace

Users overvalue what they already do, and companies overvalue what they have built. A new entrant that is merely better does not move a habituated user — the rule of thumb offered is that it must be roughly **nine times better**, because old habits die hard and products demanding a high degree of behavior change fail even when their benefits are clear and substantial.

The reason is that switching cost is cognitive, not functional. A demonstrably faster keyboard layout, patented in 1932, never displaced the incumbent, because switching means relearning to type. Two search engines with near-identical results: adapting to the challenger's pixel placement is what makes it *feel* inferior, not the technology. Milliseconds matter, but they do not hook users.

So:

- Describe the user's **current routine step by step**, including the parts outside anyone's product.
- Find where your candidate **removes a step**, rather than adding a better one.
- If you cannot remove a step, expect to need advertising rather than habit.

If the pitch for the candidate is a feature comparison, that is the finding.

### 4. Do not kill it on the vitamin objection alone

The standard investor screen — build a painkiller, not a vitamin — misfires on this category. Habit products routinely launch looking like nice-to-haves that appeal to emotional rather than functional needs, and become must-haves only once the habit exists, **because a habit is a behavior whose absence causes discomfort**. The discomfort is better described as an itch than as pain: a small mental irritation that persists until scratched.

Nobody ever woke at 3am needing to update a status. The need was manufactured by repetition, and then it was real.

This is not a licence for an idea with no value proposition. It is a warning against a screen that reliably rejects this whole category.

Related: **design from revealed preferences, not declared ones.** What people say they want differs systematically from what they do, and research aimed at aspiration ("cinema-quality home movies") narrows the design space to products nobody uses, while research aimed at actual behavior ("watching cat videos") expands it. The gap between the two is the opportunity, not a research error to reconcile.

### 5. Sanity-check the business shape

- **First-to-mind wins.** The competitive prize is becoming the automatic answer to a recurring internal state before deliberation happens. A better product that is not first-to-mind never gets compared.
- **Growth compounds through usage frequency.** Where a user's ordinary activity naturally exposes other people, the interval between joining and producing an invitation compounds hard: at a two-day cycle time, twenty days yields roughly twenty thousand users; at a one-day cycle, over twenty million. Attack that interval before top-of-funnel acquisition.
- **Monetization comes after the routine.** Willingness to pay rises with habituation, so plan to convert after the habit exists — if the unit economics can carry unmonetized users. One service saw roughly 0.5% paying after month one, ~11% by month 33, ~26% by month 42.
- **Price insensitivity is the proof.** As users form routines they depend on a product and stop comparing on price. How much agony a business goes through to raise prices is a measure of how habitual its usage really is.

## Output

```markdown
# Opportunity shortlist: <domain or brief>

## Candidates

### <candidate>
- Where it came from: <own need / nascent behavior / enabling tech / interface change>
- Underlying human desire: <stated so it would have been true decades ago>
- Realistic frequency: <and how estimated>
- Perceived utility vs current solution:
- Habit-zone placement: <above / below / structurally infrequent>
- Routine it displaces: <the current step sequence>
- Step it removes:
- Improvement multiple needed, honestly:
- Call: <pursue / park / kill> — <reason, recorded so it is not re-litigated>

## Not pursued, and why
<so the same ideas do not come back next quarter without new information>
```

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| The pitch is a feature comparison against an incumbent | Betting a marginal improvement will break an established habit | Describe the current routine; find the step you remove, not the feature you add |
| Idea killed because "nobody is asking for it" | Judging a habit product by declared preference | Check revealed behavior, and check the vitamin-to-painkiller pattern |
| Idea pursued despite inherently rare use | Frequency screen skipped | Accept that this product needs sales and referral, not a loop |
| Opportunity dismissed because only a small odd group does it | Nascent behavior mistaken for a niche market | Ask whether the underlying need is broad. The dismissals have historically been wrong in the cases that mattered |
| Team generates ideas by surveying markets, never by observing behavior | No direct line to any real user | Start with the team's own workarounds and three strangers' home screens |
| Plan assumes a fixed number of days to build the habit | A universal timescale that does not exist | Plan for repetition rate |
