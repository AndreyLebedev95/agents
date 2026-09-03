# Phase failure signatures

Per-phase tells, causes, and the cheapest check for each. Use this when diagnosing by inspection — no usable data, or data that has not been split yet — and as a cross-check when data exists.

Work the phases in loop order. A failure in an early phase produces symptoms that look like failures in later ones: if nobody is triggered, the reward looks broken; if the action is too hard, the reward looks unattractive.

---

## Trigger phase

**Tell: engagement tracks marketing spend.**
Cause: no owned trigger. Paid, earned, and relationship triggers acquire users; only owned triggers — an icon on the home screen, subscribed email, a notification the user permitted — can prompt repeat engagement often enough to build a habit, because only they occupy the user's environment with their tacit permission.
Cheapest check: list every channel that produces a return visit and classify it. If none is owned, that is the diagnosis.

**Tell: notifications sent, ignored, or muted.**
Cause: the trigger is not coupled in time to the moment the internal trigger fires — it is on a send schedule that suits the company.
Cheapest check: for the last week of sends, ask what emotional state the recipient was plausibly in at that moment. If the answer is "unknown", the timing is the problem.

**Tell: users cannot say why they would open the product.**
Cause: no internal trigger identified — the product is attached to a task, not to a feeling. Habits are sparked by external triggers but sustained by internal ones, and the association takes weeks or months of frequent use to form.
Cheapest check: ask five users what they were feeling immediately before they last opened it. If nobody can answer, run the why-chain from scratch.

**Tell: the trigger surface has several equally weighted actions.**
Cause: a trigger carrying more than one instruction. More choices force evaluation, and too many or irrelevant options cause hesitation, confusion, or abandonment.
Cheapest check: count the calls to action on the last email or notification sent. More than one is the finding.

**Tell: the team is afraid to send more triggers and has never tested it.**
Cause: untested assumption, usually wrong in the conservative direction for meaningful triggers.
Cheapest check: one bounded send, measured on uninstalls and shares.

---

## Action phase

**Tell: the funnel is fully optimized and retention is flat.**
Cause: the optimized action is not the one that predicts retention. The most-performed action on a surface is not necessarily the one that builds the habit.
Cheapest check: find which early behavior correlates with users still being active later, and compare it with what the entry surface currently pushes.

**Tell: users drop at a specific step and the team has added explanation there.**
Cause: an ability problem being treated as a motivation problem. Raising motivation is expensive and slow; people ignore instructional text, are multitasking, and have little patience for explanations of why they should act.
Cheapest check: count the steps from intention to outcome, including steps outside your product. Compare against competitors. Then ask which of the six resources — time, money, physical effort, brain cycles, social deviance, non-routine — is scarcest for this user at this moment, and whether the added explanation addresses it. It almost never does.

**Tell: the product works for one segment and not another, with the same funnel.**
Cause: the scarce resource differs by person and context. Federated login removes steps for the time-starved and adds anxiety, therefore brain cycles, for the privacy-wary. There is no one-size-fits-all simplification.
Cheapest check: name the scarce resource separately per segment.

**Tell: the product demands an unfamiliar routine.**
Cause: high non-routine cost. Users have only two options — comply or quit — and motivation fades. Products that succeed at behavior change attach to a behavior the user already performs voluntarily and make that easier first.
Cheapest check: is the core action something the user did before your product existed, in any form?

**Tell: one missed day invalidates progress.**
Cause: all-or-nothing mechanic. A user who forgets one entry finds the rest of the period a write-off and stops.
Cheapest check: what happens in the product after a two-day gap? If the answer is "the streak or plan is void", that is the churn mechanism.

---

## Reward phase

**Tell: strong launch, decay over weeks, content team exhausted.**
Cause: finite variability. The source of surprise runs out once the user has seen it.
Cheapest check: could a user predict roughly what they will find on their next visit? If yes, variability is exhausted. Either accept continuous content production as a permanent cost or move the source of unpredictability to other users.

**Tell: gamification added, no change in behavior.**
Cause: reward family mismatched to the motivation that brought the user. Points, badges and leaderboards work only when they scratch the actual itch, and fail entirely when there is no ongoing itch at all.
Cheapest check: state the internal trigger the reward is supposed to relieve, and check the reward is the same family — tribe, hunt, or self. Also check the *rate*: a reward too rare or too small reinforces nothing.

**Tell: the reward is reliable and generous, and nobody comes back.**
Cause: no variability. A predictable feedback loop creates no desire; craving comes from anticipation of an uncertain reward, not from the reward itself.
Cheapest check: what about the outcome is uncertain? If nothing, that is the finding.

**Tell: users complete a session and have no reason to open it again.**
Cause: the reward fully closes the loop. It must satisfy while leaving something unresolved — the next question opened before the current one closes.
Cheapest check: at the end of a session, what is the user curious about?

**Tell: the product's *function* is what varies.**
Cause: variability applied to the wrong thing. Users must be able to depend on the product as a reliable solution; an unpredictable interface or unreliable core breaks ability instead of creating craving.
Cheapest check: is the uncertainty in what they get, or in whether it works?

---

## Investment phase

**Tell: signup, profile completion, or invitations are requested before anything is delivered.**
Cause: investment placed before the reward. The ask must come after a reward, when the user is primed to reciprocate — reciprocation extends even to software, not just to people.
Cheapest check: walk the first session. Where is the first ask, and where is the first reward?

**Tell: an investment step underperforms and the team is adding incentives to it.**
Cause: the ask is too large for current motivation and ability. Investment is still gated by both.
Cheapest check: halve the ask before redesigning it. Stage investments as escalating chunks across successive cycles, easiest first.

**Tell: the team cannot say what accrues to a user over time.**
Cause: no stored value. Nothing makes leaving expensive.
Cheapest check: name which of content, data, followers, reputation, or skill accrues. Then ask whether the user can *feel* it accruing — stored value the user cannot perceive does not bind them.

**Tell: users return only when reminded manually or by campaign.**
Cause: investment does not load the next trigger. Investment should earn both the right and the timing to come back — the permission granted as part of the work itself, the trigger fired when the internal trigger is most likely to arrive.
Cheapest check: after a user's last action, what future trigger did that action create? If none, that is the gap.

**Tell: investment exists but produces no attitude change — usage stays flat.**
Cause: the work does not improve the user's own experience next time. Effort that benefits only the company does not produce the valuation shift; the mechanism is that people overvalue what they built, act consistently with what they have already done, and adjust preferences to avoid contradiction.
Cheapest check: does the next session get measurably better because of what the user put in?

---

## Cross-phase

**Tell: sharp drop immediately after a feature that changed a default or made something visible.**
Cause: reactance. Autonomy threatened. A product that auto-enabled identity-revealing view tracking faced a user revolt and reversed within weeks.
Cheapest check: did the feature ship enabled? Make it opt-in; a low opt-in rate is information about the feature.

**Tell: decay concentrated in the newest cohorts.**
Cause: expected. Recently acquired habits are the first to go, since old routines remain and reactivate when attention lapses.
Cheapest check: compare decay by cohort age before treating it as a regression.

**Tell: the pitch against a competitor is a feature comparison.**
Cause: betting a marginal improvement will break an established habit. Switching cost is cognitive; even small interface differences force relearning and make an objectively equal alternative feel inferior.
Cheapest check: describe the user's current routine step by step and find where you remove a step rather than add a better one.
