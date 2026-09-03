---
name: settle-usability-arguments
description: Turns unwinnable design arguments into decidable ones, and gets usability work accepted inside an organization. Covers why debates about what users like cannot be settled by opinion, how to rewrite a general preference question into a specific testable one, how to get executives to care by putting them in the room for one session, why ROI cases are a weak opening move, and where the line sits between helping persuade users and helping manipulate them. Use whenever a team is deadlocked over a design choice; when someone asks "do users prefer X or Y" or "what do most users like"; when asking how to convince a boss, stakeholder, or executive to fund research or testing or take users seriously; when weighing an expert opinion, a survey, or a focus group against a test; when stakeholders are fighting over Home page or landing page space; or when someone is asked to make a product feel more desirable and is unsure whether that is the job. For actually running the test that settles the question use run-diy-usability-test; for judging the design yourself use review-screen-for-friction.
---

# Settle usability arguments

Two related problems: the team can't agree, and nobody will fund finding out. Both come from the same root —
treating design questions as matters of preference — and both have the same cure.

## Part 1 — The deadlocked argument

### Recognize it by its shape

This is called these **religious debates**, because they resemble arguments about religion and politics: people
expressing strongly held personal beliefs about things that can't be proven, ostensibly in the interest of
agreeing how to do something important. Like most religious debates, they rarely result in anyone changing
their point of view.

The tell is simple: **the question is phrased generally, about what users like.** *Do people like carousels?
Are mega menus better? Should stories be one long page or several short ones?*

Besides wasting time, these arguments create tension, erode respect between team members, and often stop the
team making decisions at all.

### Name the three forces, without blaming anyone

Understanding why the argument is inevitable is what lets you defuse it without making an enemy.

**Personal taste projected outward.** Everyone on a web team is also a web user, with strong feelings about
what they like. It's very hard to check those at the door. And there's a natural tendency to project: to
assume most users are like us. Not that *everyone* is — we know some people hate what we love, there are even
some on our own team — but not *sensible* people, and not many of them.

**Professional taste, at a brain-chemical level.** People probably have the jobs they do because of who they
are. Designers became designers partly because they get visceral pleasure from elegant type and subtle visual
cues; developers tend to like complexity, enjoy figuring out how things work and reverse-engineering them.
There are endorphins involved. And because the reaction is happening at that level, it's genuinely difficult
for either to imagine that everybody doesn't feel the same way. So designers want sites that look great and
developers want sites with ingenious features, and the collision shows up when priorities get set.

**Hype versus craft.** Above both sits a larger clash: the hype culture (upper management, marketing,
business development) makes whatever promises are needed to attract funding, deals, and users; the craft
culture (designers, developers) carries the burden of delivering on them. This produces apparently arbitrary
edicts from above. Example: asking about a puzzling Home page feature and being told "Oh, that. It
came to our CEO in a dream, so we had to add it."

None of these is bad faith. Say so out loud — it's what makes the reframe land instead of sounding like a
rebuke.

### Refuse the premise: there is no Average User

The belief that most users are like us is enough to deadlock a meeting. Underneath it is a more insidious
one: **that most users are like anything at all.**

When the clash of opinions stalemates, the conversation usually turns to finding some external authority — an
expert opinion, published research, a survey, a focus group — to determine what the Average Web User is
really like. The problem is there is no Average User.

> **ALL WEB USERS ARE UNIQUE AND ALL WEB USE IS BASICALLY IDIOSYNCRATIC**

Watch people carefully and listen to them articulate their intentions and their reasoning, and individual
reactions turn out to depend on so many variables that describing users in terms of one-dimensional likes and
dislikes is futile and counterproductive.

The real damage the myth does is that it frames good design as **figuring out what people like** — which
makes every question binary. Pull-downs are good or bad. Carousels are good or bad. Black or white.

There are no simple right answers to most design questions, at least not the important ones. What works is
good, integrated design that fills a need — carefully thought out, well executed, and tested.

(This is not relativism. There *are* things you should never do and things you should rarely do. They're just
not the things teams argue about.)

### Rewrite the question

The move that ends the argument. Not:

> *Do most people like pull-down menus?*

But:

> *Does **this** pull-down, with **these** items and **this** wording, in **this** context, on **this** page,
> create a good experience for most people **who are likely to use this site**?*

Five qualifiers: the specific element, its specific contents, its specific wording, its position in this
context and page, and this site's actual likely users. Add all five. Then notice what's happened — the
rewritten question **cannot be settled by opinion, or by research about users in general.** It has moved from
the realm of what's right and wrong, and what people like and dislike, into the realm of **what works and
what doesn't**.

And there's only one way to answer it: use the team's collective skill, experience, creativity, and common
sense to build some version of the thing — even a crude version — then watch a few people carefully as they
try to figure out what it is and how to use it. There's no substitute.

Note the division of labour: **testing decides between candidates; it doesn't generate them.** The team's
judgment is still doing the design. Say this explicitly, because "let's just test it" otherwise sounds like
a vote of no confidence in the people arguing.

Then hand off to `run-diy-usability-test`.

### Two related tie-breakers

**Clarity trumps consistency.** Consistency is worth striving for and gets cited as an absolute — people win
a lot of design arguments just by saying "we can't do that, it wouldn't be consistent." The rule: if you can
make something **significantly** clearer by making it **slightly** inconsistent, choose clarity. The
asymmetry is the whole rule.

**Home page turf fights are a commons problem, not a taste dispute.** Anything prominently promoted on a
Home page gets substantially more traffic, so every stakeholder wants a slot. The promoted section captures
the entire gain; the loss in overall effectiveness is shared by everyone. So adding one more thing is
individually rational and collectively fatal, and every stakeholder reasons identically — preferably before
someone else does. Framed as a shared-resource allocation problem it becomes settleable; framed as taste it
never does. Offer substitutes: cross-promotion from other popular pages, and taking turns in the same slot.

## Part 2 — Getting the work funded

### The tactic that actually works

**Get your boss, and their boss, to watch a usability test — in person.**

Tell them you're going to be doing some testing and it would be great for the team's morale if they could
poke their head in for a few minutes. In experience, executives often become fascinated and stay
longer than they planned, because it's the first time they've seen anyone try to use their site — and the
picture is rarely as pretty as they'd imagined.

**In person matters.** The difference between watching a test live and hearing a presentation about it is the
difference between watching a game as it happens and hearing the recap on the evening news. Live creates
memorable experience; recaps don't.

Fallbacks, in order:

1. Clips of test highlights inside a presentation.
2. If there's no presentation: a clip under three minutes on the intranet, with an intriguing description
   emailed round. Even executives watch short videos.

### The first test: don't ask permission

Do the first one on your own time. Keep it incredibly simple and informal, and find volunteer participants
so it costs nothing.

Then make sure **something improves as a result**. Pick an easy target — something you already know has at
least one serious problem that can be fixed quickly without a lot of sign-offs. Renaming a poorly labelled
button is the archetype. Test it, fix it, publicize it.

If there's a simple way to measure the improvement, use it: test something generating a lot of support calls,
then show the drop in calls on that issue afterwards.

### Test the competition as the entry event

Testing competitors' sites is useful anyway before starting a project — and it's an excellent way to drum up
support, because everybody loves learning about the competition and **nobody has anything personally on the
line**. It makes a good brown-bag lunch event.

### Present findings live, not as a report

Abandon the "big honking report" after years of writing them. A live presentation lets people ask
questions and voice concerns in the moment; a written document doesn't. Teams doing Agile or Lean have no
time for written reports anyway. Reserve writing for the short list of agreed fixes.

### Why ROI is a weak opening move

The two standard recommendations are: demonstrate ROI (prove a change produced savings or revenue), and speak
management's language (learn the current vexing corporate problems and frame your work in their vocabulary —
pain points, KPIs, whatever is trending).

Both are fine and worth doing if you can. But an ROI case tied to costs and revenues is a lot of work, and
unless it's rigorously implemented **there will always be someone who claims the gain was caused by something
else**. Learning to speak business fluently is its own project.

Compare the cost: getting one executive into a room for twenty minutes requires no attribution argument at
all. Start there; build the ROI case later if you still need it.

### Posture

Two things The source material is emphatic about, and they're load-bearing rather than decorative:

**Empathize with management — genuinely.** Not in the "how do I figure out what motivates these people so I
can get them to do what I want" sense, but in the "understand the position they find themselves in" sense,
with real emotional empathy. Empathy is virtually a professional requirement for this work; apply it upward
too. The effect is often surprising.

**Keep some humility.** In the business world almost everyone is a very small cog in a large collection of
cogs. You want enthusiasm to be infectious, but going around as though you're bringing the truth to the
unwashed masses does not work. Your primary role is to **share what you know**, not to tell people how things
should be done.

### Don't argue about titles

When someone says "I'm in UX" or "usability is so 2002 — it's all UX now", smile and ask three questions:

1. How are you learning about users?
2. How are you testing whether people can use what you're building?
3. How do you get changes to actually happen?

If they do none of those, they need your help. If they do, learn from them. It isn't what we call ourselves
that matters — it's the attitude we bring and the skills we contribute.

(Background if useful: **UCD** focused on designing the right product and making sure it was usable. **UX**
claims the user's needs at every stage of the life cycle — from seeing an ad, through purchase and delivery
tracking, to returning it at a branch. A dozen specialties now sit under that umbrella and few people
understand what each contributes.)

## Part 3 — The line

Usability is at heart a **user advocate** job. Which means some requests are not the job.

Three requests that look similar and aren't:

| Request | Verdict |
|---|---|
| "Help us make this better for users" | The job |
| "Help us persuade users to do X" | Legitimate, **as long as it isn't deceptive**. The think-aloud protocol often gives real insight into why persuasion succeeds or fails |
| "Help us make people *think* it's desirable" | Manipulation. Not part of the job |

The third often arrives disguised as the second. The signal is that they aren't asking for help determining
whether something is desirable, or even for help making it *more* desirable — they're asking how to make
people *think* it is.

**Desirability is not a usability-test question anyway.** You may get a sense during a session that a
participant finds something desirable, but that's all it is: a sense. Whether something is desirable is a
market research question, answered with market research instruments — as is whether it's *useful*, which
should be settled before the project starts.

The gradient is worth knowing, because it's gradual:

- Relatively benign: a slightly hidden checkbox, checked by default, that signs you up for a newsletter.
- Closer to the dark: tricking someone into installing an unwanted browser toolbar, and changing their
  default search and home page settings while they aren't looking.
- Over the line: phishing, scamming, identity theft.

If people ask you to do any of this, it's not part of your job. The users are counting on you.

None of this is an argument against influence as a subject. Worth reading: Cialdini's *Influence* and Weinschenk's work on
what neuropsychology teaches about motivation and decision making. The distinction is between understanding
persuasion and practising deception.

## And: rules can be bent

Nothing here is an argument against breaking or bending the rules. There are even products where you *want*
the interface to make people think — to puzzle or challenge them. The only requirement: **know which rule
you're bending, and at least think you have a good reason.**

That's also the fair way to lose an argument. If the team decides to keep the thing you flagged, and they can
name the rule and the reason, they've done the work. Say so and move on.

## Failure modes

| Tell | Cause | Fix | KU |
|---|---|---|---|
| "Do most people like pull-downs?" | Question at the wrong altitude | Rewrite with all five qualifiers |
| Survey or expert opinion sought as tiebreaker | Belief in the Average User | No Average User exists; test the specific thing |
| "Let's test it" lands as a vote of no confidence | Division of labour left unstated | Testing decides between candidates; the team still designs |
| Executive read the report and moved on | Recap instead of the live game | Get them in the room for one session |
| Buy-in campaign opens with an ROI model | Expensive, attribution-contestable | Start with a watched session and a publicized quick fix |
| Argument won by "it wouldn't be consistent" | Consistency treated as absolute | Slight inconsistency for significant clarity |
| Home page fight framed as taste | Wrong frame | Name it as a commons problem with a fixed budget |
| Accessibility pitched with a population statistic | Invites blanket skepticism | Lead with what it concretely changes for someone |
| Asked to test whether users find it desirable | Wrong instrument, possibly wrong intent | Market research question — and check what's actually being asked |
| Advocacy delivered as evangelism | No humility | Share what you know; don't announce the truth |

## Output format

```
### The question as asked
<verbatim>

### Why it can't be settled as posed
<which force is driving it; the Average User problem>

### The decidable version
<the rewritten question, all five qualifiers explicit>

### Cheapest way to answer it
<what to build, how crude, who to watch — hand off to run-diy-usability-test>

### Getting it accepted
<the specific tactic, and what to do if it's refused>
```

## References

- `references/buy-in-tactics.md` — the organizational tactics in full, ordered by cost, with the empathy and
  humility framing and the books Recommended.
- `references/ethics-line.md` — read when the request involves influencing, persuading, or increasing
  desirability: the three-way split, the manipulation gradient, and how to decline the third without
  moralizing.
