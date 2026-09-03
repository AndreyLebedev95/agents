---
name: audit-navigation-and-landing
description: Audits and designs site-level wayfinding — persistent navigation, sections and utilities, page names, "you are here" markers, breadcrumbs, tabs, search placement, deep-level navigation — and whether a Home or landing page answers what this is and where to start. Runs the trunk test on real pages. Use whenever someone asks about navigation, information architecture, site structure, menus, nav bars, breadcrumbs, page titles, or what belongs in a header or footer; asks whether their Home page, landing page, or tagline works; says users cannot find things or get lost; is reorganizing a site's sections or planning a hierarchy; or mentions the trunk test. Use it even when the person frames it as "the menu feels wrong" without saying navigation. For friction inside a single screen use review-screen-for-friction; for the wording of labels and taglines use edit-interface-copy; for watching real users navigate use run-diy-usability-test.
---

# Audit navigation and landing surfaces

## Why this is its own job

Navigation isn't a feature of a site — it *is* the site, the way the building, the shelves, and the registers
are the store. It compensates for the fact that web space has no sense of place, by embodying the hierarchy
and creating a sense of *there*. Without it there's no there there.

That's why navigation quality outranks most page-level polish in a review, and why "figuring out where I am"
is a far bigger problem online than in physical space.

## The five jobs, three of which get forgotten

Two are obvious: help people find what they're looking for, and tell them where they are. The other three
are what a real audit checks:

- **It tells them what's here.** Making the hierarchy visible tells people what the site contains. Revealing
  the content may matter more than guiding or situating them.
- **It tells them how to use the site.** Done right, it implicitly says where to begin and what the options
  are. It should be all the instruction needed — which is fortunate, since people ignore instructions anyway.
- **It signals whether you know what you're doing.** Every moment on a site, people run a mental tally: *do
  these people know what they're doing?* It's one of the main inputs to bailing out and to ever coming back.

Evaluate against all five, not just findability.

## What web space is missing

Three physical-space cues don't exist online, and navigation has to supply substitutes:

- **No sense of scale.** People can't tell how big a site is, so they can't tell when they've seen
  everything — which means they can't tell when to stop looking. (This is why visited-link colouring earns
  its keep: it's the only cue of ground covered.)
- **No sense of direction.** There's no left or right, only up and down a hierarchy.
- **No sense of location.** No spatial memory accumulates. Returning to something means remembering where it
  sits conceptually and retracing, not walking back. Hence the importance of a Home page as a fixed North
  Star, of bookmarks, and of Back being the most-used button in the browser.

## The store model

Finding something on a site follows the department-store pattern, and mapping your site onto it exposes
missing levels fast:

1. Decide whether to ask (search) or browse.
2. If browsing: read the department signs → read the aisle signs → scan the individual products.
3. On a wrong guess, back up and try another aisle, or start over in another department.
4. Leave when convinced it isn't here, or too frustrated to keep looking.

Identify your equivalents of department signs, aisle signs, and product labels. Check each level is readable
*from the level above it*, and that backing up is cheap.

People split into **search-dominant** users, who look for the search box on arrival, and **link-dominant**
users, who browse first and search only when out of likely links or frustrated. Everyone else decides based
on their frame of mind, how much of a hurry they're in, and whether the browsable navigation looks decent —
so both paths need to work.

## Audit procedure

### 1. Inventory the persistent navigation

Persistent (global) navigation is the set of elements on every page, in the same place, with the same look.
Sameness of position plus appearance gives instant confirmation the person is still in the same site — worth
more than it appears — and means they only have to learn it once.

It carries four things, plus Home:

- **Site ID.** Top of the page, upper-left in left-to-right languages. It represents the whole site, so it's
  highest in the logical hierarchy, and hierarchy is conveyed either by being the most prominent thing or by
  *framing* everything else. Since it shouldn't be the most prominent thing (except perhaps on the Home
  page), it goes at the top, framing. It needs brand-logo attributes — distinctive typeface, a graphic
  legible from button size to billboard size — and it must link Home, which everyone expects.
- **Sections** — the top level of the hierarchy, the primary navigation.
- **Utilities** — links outside the content hierarchy (Sign in, Help, Site Map, Cart, About Us, Contact Us),
  rendered slightly less prominent than the Sections, like store facility signs. **Cap them at four or
  five**: past that they get lost in the crowd, and the less-used ones belong in the footer text links.
- **Search.** Unless the site is very small and very well organized, every page needs a search box, or at
  minimum a link to a search page.
- **An explicit Home link** alongside the sections, in addition to the clickable Site ID. Having Home in
  sight at all times is the reset button — no matter how lost you get, you can start over.

**The one exception to "every page": forms.** On checkout, registration, subscription, feedback, and
preference pages, full navigation is a distraction. Replace it with a minimal version — Site ID, a Home link,
and any utilities that actually help complete the form.

**The search box formula:** a box, a button, and either the word *Search* or the magnifying glass. People
scan for exactly that pattern on arrival. Keep three things out of it:

- *Fancy wording.* They're looking for "Search" — not Find, Quick Find, Quick Search, or Keyword Search.
  (If "Search" labels the box, label the button "Go".)
- *Instructions.* "Type a keyword" reads the way "leave a message at the beep" reads today.
- *Options.* Scope selectors and field selectors in the persistent box cost more in figuring-out than they
  pay back. Do spell out the scope if there's any possible confusion about what's being searched — and offer
  scope-narrowing on the **results page**, where too many hits make it genuinely useful.

### 2. Check page names against four requirements

Page names are the street signs of the web. When things are going well nobody notices them; the moment
someone senses they may be headed the wrong way, they need to spot the name effortlessly.

- **Every page needs one.** Highlighting the entry in the navigation is tempting — it saves space and one
  layout element — and it is not enough.
- **In the right place.** In the visual hierarchy it should appear to frame the content unique to this page.
  That's what it names — not the navigation, not the ads, which are infrastructure.
- **Prominent.** Position, size, colour, and typeface together should say *this is the heading for the entire
  page*. Usually the largest text present.
- **Matching what was clicked.** Every site makes an implicit social contract: the name of the page will
  match the words I clicked to get there. Each violation costs a moment of thought; a major discrepancy, or
  many minor ones, erodes trust in the publisher's competence. Where space forces a compromise, the two must
  match as closely as possible **and** the reason for the difference must be obvious — "Gifts for Him" →
  "Gifts for Men" passes because they feel equivalent.

### 3. Check "you are here" markers

Highlight the current location in every navigation bar, list, and menu on the page — current section *and*
subsection.

The near-universal failure is subtlety. Designers favour subtle cues because subtlety signals sophistication;
users are in too much of a hurry to catch them. Apply **more than one** visual distinction — a different
colour *and* bold, say. A too-subtle indicator is worse than none: it adds noise while providing no signal.
General calibration: if a cue looks to you like it's sticking out like a sore thumb, it probably needs to be
twice as prominent.

### 4. Check breadcrumbs and tabs

**Breadcrumbs** show the path from Home to here and make backing up a level or going Home cheap. Three
implementation rules: put them at the **top** (this marginalizes them, like page numbers, which is what makes
them work); use **>** between levels (trial and error settled on it, probably because it suggests forward
motion down through levels); **boldface the last item**, which is the current page name and is therefore not
a link. Most useful in a large site with a deep hierarchy. Watch for the misuse: breadcrumbs appearing
*instead of* well-thought-out navigation rather than alongside it.

**Tabs** are self-evident, hard to overlook (unlike horizontal nav bars, which test participants miss
surprisingly often), and hard to mistake for anything but navigation — which gives exactly the
obvious-at-a-glance split you want between navigation and content. They're one of the few cases where a
physical metaphor in a UI actually works, and Treat it as them underused. But they only work if the
graphics create the illusion that the active tab is **in front**: it needs a contrasting colour or shade
*and* it has to physically connect with the space below it. That illusion matters more than the tab shape
itself.

### 5. Run the trunk test

The acid test. Imagine being blindfolded, driven around, and dumped on a page somewhere deep in the site.
When your vision clears you should be able to answer six questions without hesitation:

1. What site is this? (Site ID)
2. What page am I on? (Page name)
3. What are the major sections of this site? (Sections)
4. What are my options at this level? (Local navigation)
5. Where am I in the scheme of things? ("You are here")
6. How can I search?

How to run it:

- Choose a page **anywhere in the site at random** and print it.
- Hold it at arm's length or squint so you can't study it closely.
- As quickly as possible, find and circle each of the six.
- Repeat on other random deep pages. Then have other people try it.

Two things make it work, and skipping either breaks it. **The random deep page** is the point: people arrive
from search engines, social posts, and emailed links, having never seen your navigation scheme — the
experience is closer to abduction than to following a garden path. **The blur** is the point too: the
standard isn't whether you can work it out given time and scrutiny, it's whether these elements pop off the
page regardless. Judge on overall appearance, not detail.

Reference: `references/trunk-test.md` for the worksheet and how to sample pages.

### 6. Check that navigation exists below level two

The most common structural failure, especially in larger sites: a flowchart four levels deep, sample pages
for the Home page and two levels, and nothing below — where navigation quietly becomes ad hoc.

It happens for four honest reasons: multi-level navigation is genuinely hard to design in limited space;
there's rarely enough time even for the top two levels; it doesn't feel important because it isn't primary
or secondary; and nobody has thought the lower-level content through far enough to supply examples.

But users spend as much time on lower-level pages as at the top, and consistent top-to-bottom navigation
cannot be grafted on later. Treat a missing third level as a **blocking gap**, not a detail. The maxim: have
sample pages showing navigation for every potential level *before* anyone starts arguing about the colour
scheme.

### 7. For a Home or landing page, answer the four questions cold

Read `references/home-page-and-tagline.md` and work through it. Summary: the thing that gets squeezed out of
Home page compromises is conveying the big picture, and it's the one thing you can't afford to lose. The page
must answer — correctly, unambiguously, in the first few seconds — *what is this*, *what have they got here*,
*what can I do here*, and *why should I be here rather than somewhere else*.

## Judgment calls

**Click count is the wrong metric.** What matters is not how many clicks but how hard each one is — the
thought required and the uncertainty about whether it's the right choice. Rule of thumb: three mindless,
unambiguous clicks cost about what one click requiring thought costs. Reject "nothing more than N clicks
away" as a governing design rule. (Fewer clicks does gain value when the same path is drilled repeatedly or
pages load slowly.)

**Every link must give off a strong scent.** Read each label with no surrounding context and ask what the
destination contains. If the answer is uncertain, the scent is weak and people lose the trail — which
matters more than path length, because users satisfice: they click the *first* plausible option, not the
best one. Order and label so the first plausible option is also the right one.

**Depth is fine on small screens; ambiguity isn't.** Mobile hierarchies legitimately run three to five levels
deep. People keep tapping as long as they stay confident the thing is further down or behind that button.
Frequent or in-a-hurry items go close at hand; the rest can be several taps away with an obvious path.

**Honour deep links.** A link tapped in an email or a social post must land on the actual content, not on the
Home page with the person left to hunt for what they already chose.

## Failure modes

| Tell | Cause | Fix | KU |
|---|---|---|---|
| Flowchart four levels deep, comps for two | Lower-level nav treated as a detail | Sample pages for every level before visual design |
| Page name differs from the link that led there | Implicit contract broken | Match the wording, or make the difference obviously equivalent |
| Current-location marker uses one subtle cue | Preference for subtlety | Two distinctions; double the prominence |
| Breadcrumbs standing in for real navigation | Used as a substitute | Design the hierarchy; breadcrumbs supplement it |
| Active tab doesn't connect to the panel below | Tab shape without the front-ness illusion | Contrasting shade plus physical connection |
| Search box carries scope and field options | Options added "for power users" | Box + button + Search; scope on the results page |
| Eight utilities in the header | No cap applied | Four or five; rest to the footer |
| Home page can't say what the site is | Squeezed out by stakeholder promos | Restore the big picture first; test on outsiders |
| Deep link lands on the mobile Home page | Deep links not honoured | Send them to the content they tapped |

## Report format

```
## Trunk test — <page URL or name>
| Question | Answer found? | Notes |
|---|---|---|
| What site is this? | | |
| What page am I on? | | |
| Major sections? | | |
| Options at this level? | | |
| Where am I? | | |
| How do I search? | | |

## Gaps
### 1. <the missing or broken element>
**Where:** <element or level>
**What it costs:** <which of the five navigation jobs fails>
**Fix:** <the change>
```

Sample at least three random deep pages before concluding anything — a single page tells you about that
page, not about the navigation.

## References

- `references/trunk-test.md` — the six-item worksheet, how to pick the sample, and how to run it with other
  people.
- `references/home-page-and-tagline.md` — read when the target is a Home page, landing page, or tagline
  rather than a navigation system: the four questions, the three explicit-statement slots, entry points,
  taglines vs. mottoes, and the commons dynamic behind promo creep.
