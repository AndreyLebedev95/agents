# The debrief and triage

Read before running a debrief.

## Why the debrief is where testing succeeds or fails

Whenever you test you'll find serious usability problems. **They aren't always the ones that get fixed.**
Two evasions do most of the damage: "yes, that's a real problem, but that functionality is all going to
change soon and we can live with it until then", and — faced with a choice between one serious problem and a
lot of simple ones — going for the low-hanging fruit.

This is why you can run into serious usability problems on large, well-funded sites. The maxim exists to
block it:

> **FOCUS RUTHLESSLY ON FIXING THE MOST SERIOUS PROBLEMS FIRST**

The structural fact underneath: **you can find more problems in half a day than you can fix in a month.**
You will always find more than you have resources to fix, so the scarce thing is fix capacity, and the
debrief is where it gets allocated.

## Timing

Do it **as soon as possible** after the tests — The default is over lunch immediately afterwards, while
everything is fresh in the observers' minds. Order the really good pizza from the expensive place to
encourage attendance.

## The four steps

### 1. Make a collective list

Go round the room. Each observer says what they thought were **the three most serious problems** they
observed — of the nine they wrote down, three per session. Write them on a whiteboard or easel pad.

Typically several people will say "me too" to some of them; track that with checkmarks.

Two rules for this step:

- **No discussion.** You're only listing. Discussion here is how a debrief turns into a two-hour meeting
  that decides nothing.
- **Only observed problems** — things that actually happened during one of the sessions. Not things someone
  thinks might be a problem, not pet grievances brought into the room.

The three-per-session limit set during the breaks is what makes this step work. Observers may take unlimited
notes; the short list is the required artifact.

### 2. Choose the ten most serious

Start with the ones that got the most checkmarks. Informal voting is fine.

### 3. Rate them

Number them 1 to 10, 1 being the worst. Copy them to a new list with the worst at the top, leaving some room
between them.

### 4. Create an ordered fix list

Starting at the top, write down for each: a rough idea of **how** you're going to fix it in the next month,
**who's** going to do it, and **what resources** it will require.

**When you've allocated all the time and resources available for fixing usability problems in the next
month, STOP.** You've got what you came for. The group has decided what needs to be fixed and committed to
fixing it.

That stopping rule is the design of the whole exercise. A debrief that ends with twenty items and no owners
has produced nothing.

## The triage rules

### Fix it out of "serious", not perfectly

You don't have to fix each problem perfectly or completely. You just have to do something — often just a
tweak — that takes it out of the category of "serious problem".

This is what makes a month-sized list achievable. Fixes scoped as full redesigns don't ship, and the problem
survives another round.

### Keep a separate low-hanging-fruit list

A second list, for things that aren't serious but are **very easy** to fix. The definition is strict, and the
strictness is the point:

> Something **one person** can fix in **less than an hour**, **without getting permission from anyone who
> isn't at the debriefing**.

Keeping it separate is what stops easy wins from crowding out the serious list — which is exactly the
evasion named at the top of this file.

### Resist the impulse to add things

When testing makes it obvious that users aren't getting something, the team's first reaction is nearly
always to **add** something — an explanation, some instructions. Very often the right solution is to **take
something away** that's obscuring the meaning, rather than adding yet another distraction.

Practically: before writing "add helper text" as a fix, list what could be removed instead, and check
whether the message is genuinely absent or merely buried.

### Take feature requests with a grain of salt

Participants often say "I'd like it better if it could do X". Be suspicious.

The test is cheap and happens during the probing block: **ask them to describe how that feature would
work.** Almost always, by the time they finish describing it they say something like "but now that I think
of it, I probably wouldn't use that."

Participants aren't designers. They may occasionally have a great idea — and when they do you'll know
immediately, because your first thought will be *why didn't we think of that?*

### Ignore kayak problems

In any test you'll see several cases where someone goes astray momentarily but gets back on track almost
immediately without help. Like rolling over in a kayak: as long as it rights itself quickly enough, it's part
of the fun. No harm, no foul.

Ignore the problem when **all three** hold:

1. Everyone who has the problem notices quickly that they're no longer headed the right way,
2. They recover without help, and
3. It doesn't seem to faze them.

General form of the threshold: **if the user's second guess about where to find things is always right,
that's good enough.**

Record the ones you deliberately dropped. It stops the next round re-litigating them.

### Ignore colour comments

People love commenting on appearance, especially colour, and almost nobody leaves because a site doesn't look
great. Ignore colour comments — unless three out of four participants reach for a word like "puke" to
describe the scheme, at which point it's worth rethinking. (Reportedly this happening exactly once; they
changed the colour.)

### Classify before fixing

Sort each surviving problem into one of three types, because the fix differs:

| Type | What you saw | Fix |
|---|---|---|
| Unclear on the concept | They don't know what to make of it, or are confidently wrong | Fix the big-picture message first — nothing else helps until this does |
| The words aren't there | They looked for a word you didn't use | Adopt their vocabulary, not yours |
| Too much going on | It's right there and they don't see it | Reduce overall noise, or turn up the volume so it pops out of the hierarchy |

The first type is the expensive one and is usually mistaken for the third.

## A note on what the round is worth

Don't try to wring everything out of a single round. It's much more important to **do more rounds** than to
extract maximum value from each one — which is the same reason three participants is enough.
