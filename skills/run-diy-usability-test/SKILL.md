---
name: run-diy-usability-test
description: Plans and runs cheap do-it-yourself usability testing end to end, then converts what was observed into a committed, capacity-bounded fix list. Covers cadence, how many participants, loose recruiting, what to test and when, task writing, the session timetable, facilitator behaviour and prompts, observer handling, the debrief method, severity triage, and the remote, unmoderated, and mobile variants. Use whenever someone asks how to test a design or site with real users, how many people they need, who to recruit, what tasks to give them, what to say or not say during a session, how to run a debrief, or what to do with the findings; when they ask whether to run a focus group; when they wonder if three participants is enough; or when a design question needs settling with evidence instead of opinion. Use it even when the request is framed as "can we get some user feedback on this". For judging a design by inspection use review-screen-for-friction; for winning organizational support for testing use settle-usability-arguments; for accessibility conformance in a real browser use chrome-devtools-mcp:a11y-debugging.
---

# Run a DIY usability test

The premise: usability testing used to mean a lab, a one-way mirror, a professional facilitator, and enough
participants for statistical significance — $20,000 to $50,000 a round. Discount usability testing brought
that to $5,000–$10,000, which is still enough that it doesn't happen often enough. This skill is the version
you run with no time and no money, and the whole design of it is aimed at one thing: **keeping it simple
enough that you actually keep doing it.**

## First: is this even a usability question?

Two ways this goes wrong before it starts.

**Focus groups are not usability tests.** A focus group is five to ten people around a table talking about
their opinions, past experiences, and reactions to concepts. A usability test is **one person at a time
trying to use something** to do typical tasks while you watch. The difference is watching people use things
versus listening to them talk about things.

Focus groups answer *are we building the right thing* — audience wants and needs, whether the value
proposition is attractive, how people solve this problem today, how they feel about competitors. Those are
planning-stage questions, and focus groups belong there. They cannot tell you whether what you built works
or how to improve it. Usability tests belong throughout the whole process.

**Some attributes aren't testable this way.** Of the seven commonly listed — useful, learnable, memorable,
effective, efficient, desirable, delightful — three sit inside the working definition of usability:
**learnable, effective, efficient**. *Useful* and *desirable* are marketing questions, best settled before
the project starts with interviews, surveys, and market research instruments. A test session may give you a
sense that a participant found something desirable, but that's all it is: a sense.

## Why the cheap version is the right version

- **Testing one user is 100% better than testing none.** Even the worst test with the wrong user shows you
  important things. And testing one user *early* beats testing fifty near the end — a simple test while
  there's still time to act on it is almost always worth more than an elaborate one after.
- **If you make it a big deal, you won't do it early enough or often enough** to get the value.
- **Changes to a live thing are harder than the conventional wisdom claims.** Some percentage of users
  resist almost any change, and apparently simple changes often have far-reaching effects. Mistakes caught
  early save trouble later.
- **You can't see your own work freshly after a few weeks.** You know too much. The only way to find out if
  it works is to watch other people try. One way to picture it: testing is like out-of-town visitors — showing them
  around, you notice things about your own town you'd stopped seeing, and discover that what you take for
  granted isn't obvious to everybody.

## The round

### Cadence

**One morning a month.** Test three users, debrief over lunch, leave having decided what you'll fix before
the next round. That's the whole commitment.

- **Pick a fixed day** — the third Thursday — and make it the designated testing day. Do not schedule
  against milestones and deliverables ("we'll test when the beta's ready"): schedules slip and testing slips
  with them. There will always be something you can test.
- A morning is about as much as most teams can actually afford; anything more complicated gets skipped when
  things get busy.
- Three participants will surface enough problems to keep you busy fixing for a month.
- A predictable slot greatly increases the chance team members show up to watch, which is a large part of
  the value.
- Under Agile the cadence tightens — perhaps two users every two weeks. The invariant is a fixed schedule
  adhered to, not the specific number.

### How many participants

**Three.** Two objections will be raised, both true, both irrelevant:

- *Too small a sample to prove anything.* Correct — the purpose isn't to prove anything. Proving requires
  quantitative testing with a large sample, a rigorously followed protocol, and a lot of data analysis. This
  is a **qualitative** method whose purpose is to *im*prove what you're building. The output is actionable
  insight, not proof.
- *It won't find all the problems.* Correct — you'll never find all the problems in anything, and it
  wouldn't help if you did, because of this: **you can find more problems in half a day than you can fix in
  a month.**

That last line is the load-bearing one. Fix capacity, not discovery, is the binding constraint. Three users
will hit many of the most significant problems for the tasks you're testing, and it's far more important to
do **more rounds** than to wring everything out of each one.

### What to test, and when

It is never too early.

- **Before you design anything:** test *competitors' sites* — actual competitors, or just sites with the
  style, organization, or features you're planning to use. Three participants doing typical tasks on one or
  two of them teaches a lot without building anything.
- **Before a redesign:** test the existing thing, so you learn both what's broken *and what's working* — so
  you don't break it.
- **Then everything the team produces, in order:** rough sketches → wireframes → page comps → prototypes →
  actual pages. With only a rough sketch, the task is simply "look at this and tell me what you think it
  is."

### Recruiting

**Recruit loosely and grade on a curve.** Try to find people like your audience, but don't get hung up on
it. Loosen the requirements, then make allowances during analysis: when someone has a problem, ask *would
our users have that problem, or was it only a problem because they didn't know what our users know?*

Recruiting to a narrow profile ("male accountants aged 25–30 with one to three years of computer experience
who recently bought expensive shoes") costs more work and usually more money. If that means you test less,
it's a bad trade. And if you're just starting, the thing probably has flaws that will trip up almost anyone.

Where to find people: user groups, trade shows, Craigslist, Facebook, Twitter, customer forums, a pop-up on
your own site, friends and neighbours.

Where the thing genuinely requires domain knowledge — a currency exchange site for money managers — recruit
*some* people who have it. Not all, since many of the most serious problems hit anybody. And deliberately
include some participants from outside the target audience, for three reasons:

- Designing so that only your target audience can use it is a mistake anyway; even within a specialist
  audience, a small but non-trivial number won't know your terminology, and you usually need to support
  novices as well as experts.
- **We're all beginners under the skin.** Scratch an expert and you'll often find someone muddling through
  at a higher level.
- Experts are never insulted by something clear enough for beginners. Everyone appreciates clarity — real
  clarity, not something dumbed down.

Incentives, as of 2014: roughly $50–$100 for an hour with average web users, up to several hundred for busy
highly-paid professionals. **Adjust for inflation.** Offer somewhat more than the going rate: it signals you
value their time and improves the odds they show up — remember an hour-long session usually costs them
another hour of travel.

Call them **participants**, never "test subjects" — it makes clear you're testing the site, not them.

### Setup

You need a quiet room where you won't be interrupted (an office or conference room), a table and two chairs,
a computer with Internet, mouse, keyboard, and microphone; screen-sharing software so observers can watch
from another room; and screen-recording software. You may never look at the recording, but it's worth having
to check a detail or cut a short clip for a presentation.

For the observation room: a computer with Internet and screen sharing, a large monitor or projector, and
external speakers.

No lab. No one-way mirror. No cameras (except on mobile — see the reference).

### Observers

**As many as possible** — team, stakeholders, managers, executives. For many people, watching is a
transformative experience that changes how they think about users: they finally get that users aren't like
them. If you have any budget for testing, It is worth spend it on the best snacks you can to lure
people in.

**In the break after each session, every observer writes down the three most serious problems they saw.**
They can take as many notes as they like, but the short list is required — the debriefing's purpose is
identifying the most serious problems so they get fixed first, not cataloguing everything.

### Writing tasks

Read `references/session-script.md` for the wording. In brief:

1. List what people need to be able to do with whatever you're testing.
2. Choose enough to fill about **35 minutes** of a one-hour session — allowing that some people finish
   faster than you expect.
3. **Word each task carefully** so it's unambiguous what you want them to do.
4. **Embed any information they'd need but wouldn't have** — demo account credentials, for example.
5. **Let participants choose some of the details.** "Find a book you want to buy, or one you bought
   recently" beats "find a cookbook for under $14": it raises their emotional investment and lets them bring
   their own knowledge of the content, which produces more revealing results.

### Running the session

Full timetable and script in `references/session-script.md`. The one-hour shape:

| Block | Time | Purpose |
|---|---|---|
| Welcome | 4 min | Explain how this works so they know what to expect |
| Questions | 2 min | A few about them — relaxes them, gauges their savviness |
| Home page tour | 3 min | "Look around and tell me what you make of it" |
| **Tasks** | **35 min** | The heart of it |
| Probing | 5 min | Your questions and the observation room's |
| Wrapping up | 5 min | Thank, pay, show out |

The four things the introduction must establish: we're testing the site, **not you**, and you can't do
anything wrong here; this is probably the one place today where mistakes don't matter; tell us honestly what
you think, you won't hurt our feelings; and please think out loud.

**Facilitating.** Almost anyone can do it — it takes the courage to try and a little practice. If you're
choosing someone else, pick someone patient, calm, empathetic, and a good listener; never someone you'd
describe as "not a people person" or "the office crank."

Beyond keeping them comfortable and on task, **your main job is keeping them thinking out loud.** Watching
what they do plus hearing what they think is what lets observers see through someone else's eyes and
understand why something obvious to them is confusing to a user. When they go quiet, prompt: *"What are you
thinking?"* — and for variety, *"What are you looking at?"*, *"What are you doing now?"*

**Influence nothing.** No leading questions, no clues, no assistance unless they're hopelessly stuck or
extremely frustrated. Note how high that threshold is — hopelessly stuck, not merely struggling. Struggle is
the data. When they ask for help: *"What would you do if I wasn't here?"*

Save probing questions for the end block, so nothing during the tasks biases them.

**Three stopping conditions for a task**: they finish it, they get really frustrated, or **you stop learning
anything new** from watching them muddle through. The third is the one facilitators miss.

## The debriefing

Do it **immediately after, over lunch**, while it's fresh in the observers' minds. Order the good pizza to
encourage attendance. Full detail in `references/debrief-and-triage.md`.

1. **Make a collective list.** Go round the room; each observer names the three most serious problems they
   saw per session (nine each, from three sessions). Write them on a whiteboard or easel pad, adding a
   checkmark for each "me too". **No discussion at this stage** — you're only listing. And only **observed**
   problems: things that actually happened in a session.
2. **Choose the ten most serious.** Start from the ones with the most checkmarks; informal voting is fine.
3. **Rate them.** Number 1 to 10, worst first, and copy to a fresh list with space between items.
4. **Create an ordered fix list.** Starting at the top, write a rough idea of how you'll fix each one in the
   next month, who will do it, and what resources it needs.

**Stop the moment you've allocated all the time and resources available for the next month.** You've got
what you came for: the group has decided what needs fixing and committed to fixing it. Stopping at capacity
is the point of the exercise — not cataloguing.

## Triage rules

These are what keep a debrief from producing a list nobody acts on.

**Focus ruthlessly on fixing the most serious problems first.** Serious problems routinely get found and
then not fixed — deferred because "that functionality is all changing soon, we can live with it", or passed
over in favour of a batch of easy wins. That is why serious usability problems survive on large, well-funded
sites. Block both evasions explicitly.

**You don't have to fix it perfectly.** You have to do something — often just a tweak — that moves it out of
the category of "serious problem". This is what makes a month-sized list achievable; fixes scoped larger
don't ship.

**Keep a separate low-hanging-fruit list**, with a strict definition: things one person can fix in **under
an hour without needing permission from anyone who isn't in the room**. Keeping it separate is what stops
easy wins from crowding out the serious list.

**When users don't get something, take something away rather than adding an explanation.** The reflex is to
add instructions; very often the right fix is to remove what's obscuring the meaning, since the addition is
itself another distraction.

**Discount feature requests.** Be suspicious of "I'd like it better if it could do X". In the probing block,
ask them to describe how it would work — almost always they finish the description with "but now that I
think of it, I probably wouldn't use that." Participants aren't designers. Genuinely good ideas announce
themselves: your immediate reaction is *why didn't we think of that?*

**Ignore kayak problems.** Someone who goes momentarily astray and rights themselves immediately hasn't
found a problem worth fixing — like rolling a kayak that comes back up quickly. Ignore it when all three
hold: everyone who hits it notices quickly they're off track, they recover without help, and it doesn't
faze them. General form: if the second guess is always right, that's good enough.

**Ignore colour comments** unless three of four participants reach for a word like "puke".

**Classify each problem into one of three types**, because the fixes differ:

- **Unclear on the concept** — they don't know what to make of it, or think they do and are wrong. Fix the
  big-picture message before anything else.
- **The words they're looking for aren't there** — you failed to anticipate their words, or used yours
  instead of theirs. Adopt their vocabulary.
- **Too much going on** — it's right there and they don't see it. Either reduce the page's overall noise or
  turn up the volume on what must be seen so it pops out of the visual hierarchy.

## Failure modes

| Tell | Cause | Fix | KU |
|---|---|---|---|
| "We launch in two weeks, let's do some testing" | Testing as a disaster check | Test earlier and smaller; expect the argued-about thing to be irrelevant |
| Testing booked to settle an aesthetic argument | Wrong use of the instrument | It usually reveals the argument didn't matter — colour of the drapes in a room with no windows |
| A focus group booked to answer "does this work" | Wrong instrument | Focus groups answer pre-build questions |
| Testing slips with the schedule | Cadence tied to milestones | Fix a calendar day; there's always something to test |
| Facilitator helps, hints, or leads | Discomfort watching someone struggle | "What would you do if I wasn't here?" — struggle is the data |
| Debrief produces a long flat list | No severity forcing function | Three worst per observer, top ten, rated, stop at capacity |
| "That's changing soon, we can live with it" | Evasion at triage time | Name it; most serious first |
| Team adds instructions after a confusing session | Reflex to add | Remove what obscures before adding |
| Three participants dismissed as unscientific | Purpose misunderstood | The aim is to improve, not to prove |
| Everything observed goes on the list | No kayak filter | Drop problems people recover from unaided and unfazed |

## Output format

**Before a round** — the plan:

```
## Round <N> — <date>
**Testing:** <what: competitor site / sketch / prototype / live pages>
**Participants:** 3 — profile: <loose profile>, incentive: <amount>
**Setup:** <room, sharing, recording>
**Observers invited:** <who>

### Tasks (≈35 min)
1. <task, worded exactly as it will be read, with any credentials embedded>
2. ...
```

**After a round** — the fix list:

```
## Round <N> debrief
### Fix this month
| # | Problem (observed) | Type | Fix | Owner | Resources |
|---|---|---|---|---|---|
| 1 | | concept / words / too much | | | |

### Low-hanging fruit (<1 hr, one person, no permissions)
- ...

### Deliberately not fixing
- <kayak problems and why>
```

## References

- `references/session-script.md` — the introduction wording, block-by-block timetable, facilitator prompt
  lines, and worked task examples. Read before facilitating a session.
- `references/debrief-and-triage.md` — the four-step debrief in full and every triage rule with its
  threshold. Read before running a debrief.
- `references/mobile-and-remote.md` — read when testing on a phone or with remote participants: rig choices,
  camera vs. mirroring, and the remote and unmoderated variants. Contains dated tooling claims, flagged as
  such.
