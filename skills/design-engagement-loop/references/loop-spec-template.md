# Loop spec — output template and worked example

Read before writing the deliverable.

## Template

```markdown
# Loop spec: <product or feature>

## 0. Does this need a loop?
<Yes/No + one sentence. If no, stop here and say what the product needs instead.>

## 1. Intake
- Habit the business model requires:
- Problem users turn to this for:
- How they solve it today:
- Realistic expected frequency:
- Target behavior to make automatic:

## 2. Internal trigger
- User narrative: <one paragraph of prose — one person, one place, one moment>
- Why chain: <the five answers, ending in an emotion>
- Internal trigger: <the emotion>
- How often this user feels it:
- One-line loop sentence: "Every time the user <internal trigger>, he/she <first action>."

## 3. External trigger
- Owned trigger channel: <what it is, or NONE — and if none, how the loop is supposed to close>
- Permission moment: <where in the experience the user grants it>
- Single call to action on the trigger surface:
- Timing relative to the internal trigger:
- Acquisition triggers in use (paid / earned / relationship):

## 4. Action
- The simplest action taken in anticipation of reward:
- Full step sequence today, from intention to outcome: <numbered, including steps outside the product>
- Steps removed, and the resulting sequence:
- Scarcest resource for this user at this moment: <time / money / physical effort / brain cycles / social deviance / non-routine>
- What removes that specific obstacle:
- Motivator in play: <which of the three pairs, which pole>
- Biases applied, if any:

## 5. Variable reward
- Reward family: <tribe / hunt / self — and why that family matches the internal trigger>
- What actually varies:
- What stays reliable:
- What is left unresolved so the user returns:
- Variability type: <finite — with the content cost accepted / infinite — with the source of surprise named>

## 6. Investment
- The bit of work asked for:
- Placed after which reward:
- First-cycle version (small enough that almost anyone accepts):
- Escalation across later cycles:
- Stored value accrued: <content / data / followers / reputation / skill>
- How the accrual is made visible to the user:
- How this loads the next trigger, and when it fires:

## 7. Check
<The five questions, each answered in one line. Any question you cannot answer names the phase you have not designed.>

## 8. What to test first
- <ordered, with the measurement that would show it worked>
- Expected delay between loading a trigger and reengagement:

## 9. Autonomy check
- Anything auto-enabled that changes what others can see about a user? <must be no>
- Can the user decline every ask easily?
- Does any mechanic leave only "comply or quit"?
- Does a single lapse invalidate accumulated progress?
```

## Worked example — a reading app for long, intimidating texts

Compressed, to show the level of specificity expected.

**Internal trigger.** Narrative: a commuter with fifteen minutes on a train who feels vaguely that she should be reading more and has not opened the book in a month. Why chain ends at: *guilt at having abandoned something she values*, plus low-grade boredom in dead time. Frequency: daily.

**External trigger.** Owned channel: a daily notification, permission granted during a two-tap onboarding where she picks a plan. Single call to action: "Today's reading — 4 minutes." Timed to her usual commute window, not to a global send hour.

**Action.** Simplest action: open and read one short passage. Step sequence reduced from *find book → find place → decide how much to read → read* to *tap notification → passage is on screen*. Scarcest resource: brain cycles (deciding what and how much to read) plus non-routine. Removed by pre-selecting the passage and fixing its length. Alternate modality: audio for the same passage, one tap.

**Variable reward.** Family: self (completion and competence), with a secondary tribe channel from community responses. What varies: which passage arrives and how it lands against whatever she is currently dealing with. What stays reliable: the passage is always there, always short. Left unresolved: the next day's passage is unknown. Variability: finite in the underlying text, so ordering matters — interesting sections first — and infinite in the community layer.

**Investment.** Ask: highlight or note a line, offered *after* she finishes the passage and sees the completion mark. First cycle: a single tap to mark a passage. Escalates later to notes, plans, and shared highlights. Stored value: content — her own annotated history, which becomes a personal record she will not abandon. Visible as a growing marked-up archive and a chain of completed days. Loads the next trigger by scheduling tomorrow's passage and by notifying her when someone responds to a shared highlight.

**Autonomy check.** Highlights are private by default; sharing is an explicit action. Missing a day does not reset the archive, and after a miss the app offers a shorter plan rather than repeating the same prompt.

## Worth reading further

- A card deck of cognitive biases, one per card, built to spark product-team conversations about which principle applies to a given behavior — useful in the action phase (*Mental Notes*, from *Seductive Interaction Design* by Stephen Anderson).
- A lightweight research guide arguing for studying what people actually do rather than what they wish they did (*Just Enough Research*, Erika Hall).
- A three-step account of innovation as step-removal (*Something Really New*, Denis J. Hauptly).
