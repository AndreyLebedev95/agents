---
name: review-screen-for-friction
description: Reviews an existing page, screen, or component for the needless thinking it demands — question marks, ambiguous affordances, broken visual hierarchy, noise, clutter, hard choices, and goodwill-depleting behaviour — and returns ordered findings with concrete fixes. Use whenever someone asks for a usability review, UX critique, heuristic evaluation, or design feedback; hands over a screenshot, URL, mockup, Figma frame, or component and asks "is this confusing?" or "does this work?"; asks what to cut from a busy screen; asks whether something reads as clickable or tappable; or asks why users are missing something that is right there on the page. Use it before shipping a screen when nobody has looked at it as a stranger would, even if the user did not say the word "usability". For navigation, page names, breadcrumbs, and Home pages use audit-navigation-and-landing; for the wording itself use edit-interface-copy; for testing with real people use run-diy-usability-test; for winning the argument afterwards use settle-usability-arguments. This is critique of something that already exists — for creating visual design direction or building UI, use frontend-design or frontend-ui-engineering instead.
---

# Review a screen for friction

## What this skill is for

Finding the places a screen forces a person to think when they shouldn't have to, and saying exactly what
to change. Not scoring it, not redesigning it, not admiring it.

The unit of judgment is **the question mark**, not a rule violation. A screen can break no guideline and
still be full of question marks; a screen can break a guideline and be perfectly clear. Judge the thinking
demanded, then use the rules below to explain where it comes from.

## The standard you are measuring against

Self-evident: the person understands what it is and how to use it with no conscious effort at all. Where the
thing is genuinely original or inherently complicated, the floor drops to self-explanatory — a little
thought, but only a little, produced by appearance, well-chosen names, and small amounts of carefully
crafted text working together. There is no third tier below that.

Calibrate to a person of average or below-average ability and experience, uninterested in the subject,
trying to get something done — not to a motivated expert. Something is usable when that person can
accomplish their goal without it being more trouble than it is worth.

And assume they are moving fast. Designers picture someone poring over the page; the reality is closer to a
billboard passing at 60 mph. Real users **scan** rather than read, **satisfice** by clicking the first
plausible option rather than the best one, and **muddle through** with a wrong model of how it works rather
than understanding it. Every finding should survive all three.

## Procedure

Work in this order. The early passes catch the expensive problems; the later ones catch the cheap ones, and
you want to know the expensive ones first.

### 1. Walk it as a user and narrate the thought balloons

Pick a real task someone would come here to do. Move through the screen doing it, and say the internal
monologue out loud, sentence by sentence.

A screen that works produces declaratives: *"There's the search box. That's the price. There's the thing I
want."* A screen that doesn't produces questions: *"Is that a button? Which of these am I? Why is this here?
Where did they put it?"*

Every question mark is a finding. Write down the question in the user's voice — that phrasing is what makes
the finding land later.

Do this before you look at anything analytically. Once you start checking rules you stop being able to read
the screen as a stranger.

### 2. Zone the page — the $25,000 Pyramid test

Glance at the screen for a few seconds, point at each region in turn, and name it aloud as a category:
*things I can do here*, *today's top stories*, *products they sell*, *things they want to sell me*,
*navigation to the rest of the site*.

Take your first answer. Any region you cannot name is an undefined area.

This matters more than it looks: eye-tracking shows people decide in their **initial glances** which regions
are likely to hold useful information and then rarely look at the others at all — banner blindness is only
the extreme case. Content placed in a region the user has written off is invisible no matter how good it is.
So region-level placement outranks content quality as a finding.

### 3. Check the visual hierarchy against its three traits

The visual cues must accurately portray the relationships between the things on the screen:

- **Prominence tracks importance.** The most important thing is the largest, boldest, most distinctively
  coloured, most surrounded by white space, or nearest the top — or some combination.
- **Logical relatedness is shown visually.** Things that belong together are grouped, share a style, or sit
  in a defined area.
- **Containment is shown by nesting.** Every heading visually spans exactly what it governs, and nothing
  more.

A good hierarchy preprocesses the screen for the reader. Without one they fall back to word-by-word scanning
and have to construct the structure themselves — much slower work.

A *slightly* wrong hierarchy is the one people miss: a heading positioned so it appears to cover sections
that aren't part of it. The reader can decode it, but it costs them, exactly like a carelessly constructed
sentence. Cheap to fix, easy to overlook, because it breaks no explicit rule.

Related and worth checking here: no heading should float. It must sit closer to the section it introduces
than to the one it follows. Tell: equal or greater whitespace below the heading than above it.

### 4. Check affordances statically — no hover, no cursor

Read the screen with no pointer and no hover states. Can you tell what is clickable?

Clickability has to be carried by **shape** (buttons, tabs), **location** (in a menu bar), and **formatting**
(one colour, underlining). Cursor change is too slow to rely on even on desktop — it requires deliberately
moving the pointer around — and on touch screens there is no cursor at all.

Any element where the user has to *decide* whether it's clickable is a defect. "Nothing bad happens if they
click it" is not a defence: that decision gets made constantly, and the cost compounds across a session.

Affordances are the visual clues that suggest how a thing can be used — the border that says you can type in
this box, the raised edge that says press this. They don't all have to hit you in the face; they have to be
visible enough that people notice the ones they need. By definition they are the last thing you should hide.

If the design is flat, read `references/mobile-and-touch.md` before writing the affordance findings — flat
styling removes dimensions from the palette and the compensation is specific.

### 5. Classify the noise, because each kind has a different fix

- **Shouting** — everything competing for attention at once. Cause: nobody made the hard call about what is
  most important. Fix: make that decision, then build a hierarchy that leads to the winner. Do not fix
  shouting by turning individual things down.
- **Disorganization** — elements strewn about, not aligned. Cause: no grid. Fix: impose one.
- **Clutter** — simply too much stuff, low signal-to-noise. Fix: cut volume.

Naming which kind it is is most of the value; teams routinely apply the clutter fix to a shouting problem
and wonder why it didn't help.

Then run the **guilty until proven innocent** pass: assume every element on the screen is visual noise and
require each one to state a specific contribution to the user's task. Delete what can't. Do this before
considering anything to add.

### 6. Check the choices

Every choice on the screen should be mindless — *animal, vegetable, or mineral?* — answerable with almost no
thought and no uncertainty about whether the answer was right.

The click count doesn't matter; the click difficulty does. Roughly, three mindless unambiguous clicks cost
about what one click that requires thought costs. So do not report "this is too many clicks deep" as a
finding on its own — report the ambiguous click. (Fewer clicks does gain value when the same path is drilled
repeatedly or pages load slowly.)

Two specific things to hunt:

- **Self-classification.** Choices that ask the user which *kind of user* they are — home office vs. small
  business, subscriber vs. member vs. neither — force them to map themselves onto your internal segmentation
  with no confident answer and no feedback. Watch for the moment this converts their question from "which do
  I pick?" into "how much do I even want this?" Fix: rephrase around what they want to *do*; if the branch
  is unavoidable, stage it across screens so each screen shows only what is relevant to the prior selection.
- **Choices that genuinely can't be made mindless.** These get guidance that is **brief** (the smallest
  amount that helps), **timely** (placed exactly at the moment of need, not in a help page), and
  **unavoidable** (formatted so it will be noticed). The London kerb painted LOOK RIGHT with an arrow is the
  model. Guidance is the fallback after simplification has failed, never the first move.

### 7. Run the goodwill lens

Beyond "is it clear?", ask "does this behave like a mensch?" Every visitor arrives with a finite reservoir of
goodwill; each problem lowers it, and a single one — a registration form opening with dozens of fields — can
empty it outright.

Read `references/goodwill-audit.md` when the complaint is about trust or tone, or when the screen asks for
something (data, money, signup). Otherwise just check the common depleters inline: hidden prices, hidden
support numbers, punishing the user for formatting data their way, asking for information you don't need,
faux sincerity, marketing sizzle in the task path.

### 8. Check the four things that are always true

book answers almost everything with "it depends". These four are stated absolutely:

- Never small **and** low-contrast type. (Large low-contrast or smallish high-contrast survive; both are
  still discouraged.)
- No labels inside form fields, unless *all* of these hold: the form is exceptionally simple; the labels
  disappear on typing and reappear when the field is emptied; they can never be confused with answers;
  there's no way to submit the label along with the input; and they're fully accessible.
- Preserve a noticeable difference between visited and unvisited link colours. Any colours you like, but
  distinct — the browser tracks this by URL, so it also tells the user two differently worded links go to the
  same place.
- No floating headings.

Then the **three-second accessibility test**: increase the browser's *Text Size* setting (not Zoom — Zoom
enlarges everything regardless). Only a design that has moved past fixed-size fonts responds, and responding
is a decent proxy for whether accessibility got any attention at all.

If accessibility is in scope, read `references/accessibility-basics.md`.

### 9. Order the findings and drop the noise

Sort by how much thinking each one costs, most expensive first. Then apply two filters:

**Drop kayak problems.** A user who goes momentarily astray and rights themselves immediately hasn't found
a problem worth reporting. Ignore it when all three hold: they notice quickly they're off track, they
recover without help, and it doesn't faze them. General form — if the second guess is always right, that's
good enough.

**State each fix as the smallest change that removes it from "serious".** You are not designing the perfect
version; you are moving the problem out of the serious category, often with a tweak. Fixes scoped larger
than that don't ship.

## Judgment calls

**Clarity trumps consistency.** Consistency is worth striving for, but it's not absolute: if a *slight*
inconsistency makes something *significantly* clearer, choose clarity. Note the asymmetry — it doesn't run
the other way. This is also the sentence that ends the "we can't do that, it wouldn't be consistent"
objection.

**Conventions by default.** Departing from an established pattern is justified only if the replacement is
either (a) so self-explanatory there's no learning curve at all, or (b) adds enough value to be worth the
learning curve it imposes. Innovating requires first understanding the value of what you're replacing, which
is routinely underestimated — the classic case being a hand-built scrollbar that ignores the thousands of
hours of tuning inside the standard one.

**Never report "too creative".** Creativity, innovation, and aesthetic ambition are unbounded above the
usability floor. Usability is a floor, not a ceiling. If a bold choice is also clear, it isn't a finding.

**Double the cues you think are already loud.** Designers favour subtlety because subtlety signals
sophistication; hurried users miss it. If a cue looks to you like it sticks out like a sore thumb, it
probably needs to be twice as prominent. A too-subtle indicator is worse than none — it adds noise while
providing no signal.

**"They'll figure it out" is not a defence.** Muddling through often works, and it is still a finding:
it's inefficient and error-prone, and people who actually get it find more, see the full offering, can be
steered, and feel smart — which is what brings them back.

**Assume the flaw was decided, not overlooked.** There is almost always a plausible rationale and a
well-meant intention behind every usability flaw — that's why it survived review. Most serious problems are
poor *tradeoff* decisions made under a real constraint (revenue, CMS structure, an org boundary), where the
user's experience didn't get enough weight. So reconstruct the constraint and re-argue the tradeoff rather
than reporting the symptom and implying carelessness.

**Real-estate pressure never justifies a usability cost.** When a space-saving move costs usability, the
move is wrong — that's the tie-breaker, not a starting position for negotiation.

**Study good work.** More is learned from excellent things with minor flaws than from obviously broken ones,
and mockery teaches nothing. Designing something even half right is hard. Keep the tone of a colleague who
respects the work.

## Failure modes in the review itself

| Tell | What went wrong | Correction |
|---|---|---|
| A confusing area gets an explanation added | Reflex to add rather than remove | Try removal first — the explanation is one more distraction |
| Every wobble is written up | No severity threshold applied | Drop kayak problems |
| Finding reads "too many clicks" | Counting instead of weighing | Report the ambiguous click, not the depth |
| Finding reads "inconsistent with the other page" | Consistency treated as absolute | Only a finding if the inconsistency costs clarity |
| Findings phrased as taste | Reviewer's preference leaked in | Every finding names a question the user has to answer |
| Tone is contemptuous | Assumed carelessness | Assume a decided tradeoff under constraint |
| Flat restyle blamed generically | Missed the specific mechanism | Name which affordance dimension was lost |

## Report format

Lead with the worst thing. Keep each finding to four parts so it can be acted on without a meeting:

```
### 1. <the question the user is left asking, in their voice>
**Where:** <element or region>
**Why it costs:** <the mechanism — scanning, satisficing, hierarchy, affordance, noise, goodwill>
**Smallest fix:** <the change that takes it out of "serious">
```

Then, if there were any, a short **Not worth fixing** list naming the kayak problems you deliberately
dropped, so nobody re-litigates them next round.

If you were asked for a quick read rather than a full review, run steps 1, 2, and 4 only and say so — those
three catch most of the expensive problems.

## References

- `references/mobile-and-touch.md` — read when the target is a mobile site or app, or when the design is
  flat: hover loss, tap depth, zoom and deep-link and full-site minimums, speed, app learnability and
  memorability, delight.
- `references/goodwill-audit.md` — read when the complaint is about trust or tone rather than confusion, or
  when the screen asks the user for data, money, or a signup.
- `references/accessibility-basics.md` — read when accessibility is in scope. Deliberately short: it leads
  with "fix what confuses everyone first" and stops at the low-hanging fruit. For conformance auditing in a
  real browser, hand off to `chrome-devtools-mcp:a11y-debugging`.
