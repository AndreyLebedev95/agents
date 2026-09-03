---
name: edit-interface-copy
description: Cuts and rewrites interface and page text so it survives scanning — applies "omit half the words, then half of what's left", kills happy talk and instructions, formats for headings and bullets, sharpens link and button labels so they name their destination, and writes taglines, welcome blurbs, and FAQ entries. Use whenever someone asks to tighten, shorten, trim, or rewrite page copy, microcopy, button or link labels, headings, instructions, error messages, form help text, empty states, section intros, FAQs, or a tagline; when text on a product surface reads like a brochure or a mission statement; when a page feels wordy or daunting; or when users are missing something that is written right there on the screen. Use it even when the person just says "make this less wordy" without mentioning UX. Explicitly not for articles, documentation, blog posts, or long-form prose, which should stay long — use technical-writer for those. For layout, hierarchy, and affordances use review-screen-for-friction; for navigation structure use audit-navigation-and-landing.
---

# Edit interface copy

## The premise

Most of the words on a typical page are taking up space, because nobody is going to read them. And just by
being there, the extra words suggest you might *need* to read them to understand what's going on — which
makes the page look more daunting than it actually is.

That matters more than it sounds, because perceived effort suppresses use independently of real effort: if
something requires a large investment of time, **or merely looks like it will**, it's less likely to be used
at all. Shrinking the visible surface is doing real work, not cosmetics.

## Scope: what to cut and what to leave alone

This skill is for **interface and supporting text**: labels, buttons, headings, microcopy, instructions,
errors, form help, empty states, section fronts, welcome text, FAQs, taglines.

It is explicitly **not** an argument that articles, news stories, reports, or product descriptions should be
shorter than they are. Note so directly. People revert to reading on document-like pages. Don't apply
the cut to prose someone came to read.

## The procedure

### 1. Count, then cut half

> **Get rid of half the words on each page, then get rid of half of what's left.**

The second half is deliberate overstatement, and Note so: removing half the words is a realistic goal
he manages on most pages without losing anything of value; the instruction to remove half of *what's left*
is there to force ruthlessness. Report both counts.

Three things the cut buys, worth checking you actually got them:

- Lower noise level on the page.
- The useful content becomes more prominent.
- The page gets shorter, so more of it is visible at a glance without scrolling.

### 2. Kill the happy talk

Happy talk is introductory text that welcomes people and tells them how great this is, or announces what
they're about to see in the section they just entered.

**The test is auditory.** If you're not sure whether something is happy talk, read it closely and listen —
you can actually hear a small voice in the back of your head going *"blah blah blah blah blah."* That's the
diagnosis.

Distinguish it from good promotional copy: happy talk conveys no useful information and says **how great we
are**; good promotional copy explains **what makes us great**. The first goes; the second may stay.

Its favoured habitat is section fronts — pages that are just a list of links to the pages in that section,
with no content of their own, which creates a temptation to fill them. analogy: a book publisher
adding a paragraph to the table of contents saying "This book contains many interesting chapters about ___,
___, and ___. We hope you enjoy them."

Its other habitat is Home page paragraphs starting "Welcome to...".

Happy talk is small talk — content-free, a way of being sociable. Most people don't have time for small
talk; they want to get to the point.

### 3. Attack the instructions

The main thing to know about instructions is that **nobody reads them** — at least not until repeated
attempts at muddling through have failed. And even then, if they're wordy, the odds of finding the needed
information in them are low.

So the objective is always to **eliminate instructions entirely** by making the thing self-explanatory, or
as close as possible. Treat the existence of an instruction as a design defect to be removed, not a text to
be improved.

Where they're genuinely unavoidable, cut to the bare minimum. worked example trims a survey preamble
from 103 words to 34:

> Please help us improve the site by taking 2–3 minutes to complete this survey.
>
> NOTE: If you have comments or concerns that require a response, don't use this form. Instead, please
> contact Customer Service.

Note what survived: how long it takes, and the one thing that would otherwise waste someone's time.

Related, from the triage side: when it's obvious people aren't getting something, the reflex is to add an
explanation. Very often the right move is to **take away** what's obscuring the meaning instead — the
addition is just another distraction.

### 4. Format what's left for scanning

Users scan for words and phrases matching the task at hand, their standing interests, and hardwired trigger
words. Formatting is what makes those findable.

- **Use plenty of headings.** Well-written headings act as an informal outline of the page: they tell people
  what each section is about, or intrigue them, and either way let them decide what to read, scan, or skip.
  Use **more headings than you'd think**, and put more time into writing them.
  - With more than one level, make the distinction between levels **impossible to miss** — larger size, or
    more space above.
  - **Don't let headings float.** Every heading must sit closer to the section it introduces than to the one
    it follows. Tell: equal or greater whitespace below than above. repeats this in his short list of
    absolute rules, which is unusual for him.
- **Keep paragraphs short.** Long ones present a "wall of words" — daunting, harder to keep your place in,
  harder to scan than a series of shorter ones. The topic-sentence/detail/conclusion structure you were
  taught does not apply; **single-sentence paragraphs are fine**. Examine any long paragraph and there is
  almost always a reasonable place to break it in two.
- **Use bulleted lists.** Almost anything that can be a bulleted list probably should be. The mechanical way
  to find candidates: look for any series of items separated by commas or semicolons. Leave a little extra
  space between items.
- **Highlight key terms.** Bold the most important ones where they **first appear**. Skip ones that are
  already links. Don't highlight too many things or the technique stops working.

### 5. Make every label name its destination

Links that clearly and unambiguously identify their target give off a strong **scent of information** and
keep people confident they're on the right track. Ambiguous or poorly worded ones break the trail — and that
matters more than path length, because people click the *first plausible* option rather than comparing.

Test each label by reading it with **no surrounding context** and asking what the destination contains. If
the answer is uncertain, rewrite it to name the destination.

And apply the page-name contract: the name of the page will match the words that were clicked to get there.
Where space forces a compromise, they must match as closely as possible **and** the reason for the difference
must be obvious — "Gifts for Him" → "Gifts for Men" passes.

### 6. Replace clever, internal, and marketing-derived names

Cute names, marketing-induced names, company-specific names, and unfamiliar technical names all force people
to decode the label before they can act on it. "Job-o-Rama" where "Jobs" would do.

Method: list every label someone has to interpret in order to navigate. For each, ask whether an outsider
would call it that. Where the name came from marketing, internal jargon, or history, replace it with the
plainest term — and accept the loss of cleverness as the price.

Names sit on a continuum from *obvious to everybody* to *truly obscure*, and there are genuine tradeoffs —
brand, politics, "that's what it's always been called in our newsletter". This is a bias, not an absolute:
**push the tradeoff further toward obvious than instinct suggests.**

Specific case worth knowing: search should be labelled **Search** — not Find, Quick Find, Quick Search, or
Keyword Search — because that's the word people scan for. If "Search" labels the box, label the button "Go".

### 7. Front-load the distinguishing word

Screen-reader users scan **with their ears**: they're as impatient as sighted users, don't listen to every
word, and hear the **first few words** of a link or line before moving on — often at a very rapid speech
rate. A keyword a sighted user would catch anywhere on the page is simply missed if it isn't at the start of
the link or line.

So put the distinguishing word first, in link text and in line openings. This costs nothing and helps
everyone scanning quickly, by eye or by ear.

### 8. Where a hard choice survives, write guidance that earns its place

Some choices genuinely can't be made mindless. Then — and only then, after simplification has failed — write
guidance that is:

- **Brief** — the smallest amount of information that helps.
- **Timely** — placed so it's encountered exactly when it's needed, not in a help page or a preamble.
- **Unavoidable** — formatted so it will actually be noticed.

The model is the London kerb painted **LOOK RIGHT** with an arrow: brief, encountered at the instant you
need it, and unavoidable because you glance down when stepping off a kerb. Canonical digital forms: a tip
adjacent to a form field, a "What's this?" link, a tooltip.

### 9. Taglines, welcome blurbs, and FAQs

Read `references/taglines-and-faqs.md` when writing these rather than editing body text. The short version:

- A **tagline** is six to eight words stating a **value proposition**. Apply the substitution test — if any other
  organization in the world could use it unchanged, rewrite. A **motto** states an ideal and tells a stranger
  nothing about what the thing is.
- A **welcome blurb** is a terse description of the site in a prominent block. **Never a mission statement.**
- **FAQs** must be questions people actually ask — this week's top five from Support — kept current and
  answered candidly. The counterfeit is Questions We Wish People Would Ask, which depletes goodwill rather
  than building it.

## The standard

Self-evident is the target: understood with no conscious effort. Where the thing is genuinely original or
inherently complicated, the floor is self-explanatory — a little thought, but only a little, produced by
appearance, well-chosen names, and small amounts of carefully crafted text working together. There is no
tier below that.

Notice that text is only one of the three ingredients. Sometimes the right edit is fewer words *and* a
layout change, and it's worth saying so.

## Failure modes

| Tell | Cause | Fix | KU |
|---|---|---|---|
| Section front opens "Welcome to..." | Happy talk filling an empty page | Delete it; a list of links is a fine page |
| Instructions added to fix confusion | Explanation preferred to redesign | Make it self-explanatory; failing that, cut to the minimum |
| "Job-o-Rama" style label | Internal or marketing naming | The plainest outsider word |
| Search box labelled "Quick Find" | Fancy wording on a scanned pattern | "Search" |
| Key terms bolded throughout | Highlighting overused | Bold sparingly, at first appearance |
| Heading equidistant between sections | Floating heading | More space above than below |
| Link reads "click here" or "more" | No scent of destination | Name the destination in the link |
| Tagline could belong to any competitor | Motto written instead of tagline | A differentiated value proposition |
| An article got cut in half | Rule applied outside its scope | Documents are exempt; restore it |
| Comma-separated series left inline | Bullet candidate missed | Convert to a list |

## Output format

Return the rewritten text first, then the accounting:

```
### Rewritten
<the new text, formatted as it should appear>

### Before → after
Words: <n> → <m>  (<pct>% cut)

### What went, and why
- <cut>: happy talk / instruction / redundant / decoded label / wall of words
- <kept, and why it survived the cut>

### Not a copy problem
- <anything that needs a layout or structure change instead>
```

That last section matters. The halve-the-words rule is often reached for when the real problem is hierarchy or
noise — say so rather than cutting words that weren't the issue.

## References

- `references/scanning-format.md` — the heading, paragraph, list, and highlighting rules with bad/better
  contrasts, plus screen-reader front-loading. Read when formatting a body of text rather than a label.
- `references/taglines-and-faqs.md` — read when writing a tagline, welcome blurb, or FAQ set.
