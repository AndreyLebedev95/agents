# Mobile, touch, and flat design

Read when reviewing a mobile site or app, or when the design is flat.

## Contents
- [The tradeoff frame](#the-tradeoff-frame)
- [No cursor, no hover, no clue](#no-cursor-no-hover-no-clue)
- [Flat design](#flat-design)
- [Space and depth](#space-and-depth)
- [The three minimums](#the-three-minimums)
- [Speed](#speed)
- [Apps: learnability, memorability, delight](#apps-learnability-memorability-delight)

## The tradeoff frame

Start here, because it changes how you write every mobile finding. Design is constraints plus tradeoffs, and
most serious usability problems are the result of a **poor decision about a tradeoff** — not of nobody having
thought about it. The failing is that the user's experience didn't get enough weight on the scale.

Example: a news app that breaks stories into too-small chunks, each slow to load, each requiring a
scroll past the same photo. It wasn't an oversight — it was almost certainly a compromise, possibly over ad
page views or how the CMS segments content. He simply stopped using the source.

So when you find a serious mobile problem, reconstruct the constraint it was serving and re-argue the
tradeoff. Reporting the symptom alone gets answered with "we know, we had to".

And the tie-breaker for every space-driven tradeoff: **managing real-estate challenges shouldn't be done at
the cost of usability.**

## No cursor, no hover, no clue

Capacitive touch screens can't sense a finger above the glass, only when it lands. That's why there's no
cursor — and no hover. Every interface feature that depended on hover simply does not exist for these users:

- tool tips
- buttons that change shape or colour when pointed at
- menus that drop open to reveal their contents without forcing a choice

Each has to be replaced with something static or tap-triggered. Enumerate the hover-dependent cues in the
design and check that no affordance is signalled by hover alone.

This is also why identifying what's tappable resurfaced as a problem in mobile design after being largely
solved on the desktop web.

## Flat design

Affordances require visual distinctions. Flat styling moves in the opposite direction — removing visual
distinctions to reduce clutter. It looks good and it does reduce clutter, but it tends to take with it not
just the distracting decoration but also the useful information the more textured elements were carrying.

The key mechanism: **affordance cues are usually multi-dimensional**. It's the *position* of something (in
the navigation bar) *and* its *formatting* (reversed type, all caps) that together say "menu item". Removing
several dimensions from the palette makes everything harder to differentiate.

You may not get to reject flat design — it may be imposed. The finding to write is therefore not "don't be
flat" but "this affordance lost its only remaining signal". Enumerate what's still available — position,
size, spacing, weight, capitalization, contrast, grouping — and require the design to spend those to
compensate. Verify affordances are *perceivable*, not merely inferable.

## Space and depth

Small screens legitimately produce deeper hierarchies than their desktop equivalents — three, four, five
levels. That's fine. With a small screen, more tapping or scrolling is inevitable if the same information is
to be reachable at all.

What must hold is confidence: the user keeps going as long as they continue to feel sure that what they want
is further down the screen or behind that button. This is the mindless-click rule applied to mobile — depth is
acceptable, ambiguity is not.

The corresponding prioritization rule: things used in a hurry or frequently go close at hand; everything else
can be several taps away **provided there is an obvious path**.

**Watch for Mobile First misread.** Mobile First is right as a discipline for forcing you to determine what
is genuinely essential. It's wrong when interpreted as choosing features by what people would want *while out
and about* — the assumption that mobile users are "on the move" and only need on-the-move features. People
use these devices sitting on the couch and expect to do everything. Everybody wants to do *some* things, and
summed across users that amounts to everything. If you see a mobile feature set that was scoped from an
on-the-go scenario, that's the finding.

## The three minimums

Even where there's no budget to mobilize a site at all, three things must hold:

1. **Allow zooming.** Never block pinch-zoom on small text. A site that actively resists being read on a
   phone is worse than one that merely wasn't designed for it.
2. **Honour deep links.** Tapping a link in an email or a social post must land on the actual content — not
   on the mobile Home page, leaving the person to hunt for the thing they already chose.
3. **Always offer the full site.** The current convention is a Mobile Site / Full Site toggle at the bottom
   of every page. This matters most where features or information exist only in the desktop version; people
   will happily zoom around a small viewport in exchange for access, and some prefer desktop pages on
   landscape tablets.

On maintaining two versions: separate mobile and desktop versions — "two sets of books" — at least doubles
the effort and guarantees either that updates lag or the versions drift apart. Scalable/responsive design is
a lot of work and hard to do well, but the alternative is worse.

## Speed

Speed is a usability attribute, not a performance footnote. On mobile it makes everything feel better, and
slow performance means frustration for the user and lost goodwill for the publisher.

Two specifics worth checking:

- Mobile download speeds are **unreliable**. Once someone leaves Wi-Fi for cellular, performance varies
  widely. Responsive solutions must not ship code and images larger than the user's screen actually needs.
- The failure mode is **habit-forming**. Example: a news app whose alerts he valued, but which loaded
  every top-story photo before showing the alert's own detail — so he trained himself to open a competitor
  instead every time an alert arrived. A slow path doesn't just annoy; it permanently reroutes people.

## Apps: learnability, memorability, delight

**Learnability.** One or two onboarding screens at first launch, usually impossible to find again, plus a
help page that's one paragraph or an email address — that suffices only for apps doing very few things.
Anything with substantial functionality, especially functions departing from platform conventions, needs
more.

The recurring failure is **conceptual levels**: users don't grasp that there are levels (lists, items within
lists, settings) and can't navigate between them. And since help usually lives behind that navigation,
failing to learn it locks them out of the thing that would teach it. A Catch-22 worth checking for
explicitly.

Note the diagnostic trap: good reviews and strong sales do not disprove a learnability problem — they hide
it. example app had a well-made ten-screen tour *and* an interactive tutorial built from its own data
model, and no participant in his demo tests ever completed its primary task.

**Memorability.** Once someone has figured it out, will they remember next time? The best way to make
something easy to relearn is to make it extremely clear and easy to learn the first time — memorability is
bought by learnability, not by separate effort.

Tell: an interface that hides its controls to maximize the content area, so the entry gesture has to be
rediscovered every session. People will invest effort on first use but not on every use; given how cheap
apps are, an unmemorable one just gets dropped.

**Delight.** Delight — fun, surprising, impressive, captivating, clever, magical — usually comes from
marrying something people would love to do but don't imagine is possible with a bright idea about how new
technology can do it. In a competitive market, doing something well isn't enough; you have to do it
incredibly well. But delight is the extra-credit assignment: pursuing it must not displace making the thing
usable. If a review finds a delightful app that people can't operate, say so plainly.
