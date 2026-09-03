# Accessibility basics

Read when accessibility is in scope for a review.

This file is deliberately short. own chapter is a ramp, not a manual — it points outward to WebAIM and
to dedicated books. For conformance auditing in a real browser, hand off to
`chrome-devtools-mcp:a11y-debugging`. What follows is the part that changes how you *review*.

## The premise

Unless you've made a blanket decision that people with disabilities aren't part of your audience, you can't
call something usable unless it's accessible.

## The three-second test

Increase the browser's **Text Size** setting. Not Zoom — Zoom enlarges every site regardless, so it tests
nothing. Only a design that has moved past fixed-size fonts responds to Text Size, and responding is a decent
indicator that some effort went into accessibility at all. Note almost every site he visits still fails
this.

## The highest-leverage work is not the accessibility work

The usual claim is that accessibility improvements benefit everyone. The more useful direction is the
reverse: **making something more usable for everyone is one of the most effective ways to make it work for
people with disabilities.**

Whatever confuses most users will almost certainly confuse users with accessibility issues — people don't
become smarter because they have a disability — and they'll have a harder time recovering from that
confusion. Take the last confusing error message you hit on submitting a form, and imagine solving it
without being able to see the page.

So the order matters: test often and smooth out what confuses everyone **first**. Applying accessibility
guidelines rigorously to a site that isn't clear to begin with leaves it unusable anyway.

## Screen-reader users scan with their ears

Blind users are just as impatient as sighted ones and don't listen to every word — they listen to just
enough to decide whether to keep listening, often at a very rapid speech rate. They hear the **first few
words** of a link or line and move on.

The review consequence is concrete: a keyword a sighted user would catch anywhere on the page is *missed*
unless it sits at the start of the link or line. Front-load the distinguishing word in link text and line
openings. Never rely on a keyword appearing mid-link to be found.

(Observed in a study of 16 blind users working with screen readers.)

## The low-hanging fruit list

Without becoming an expert, this list gets most of the way there:

- **Alt text on every image.** An empty (null) alt attribute for images screen readers should ignore;
  helpful, descriptive text for the rest.
- **Headings used correctly.** `h1` for the page title or main content heading, `h2` for major sections,
  `h3` for subheadings — and CSS to control how each level looks. The heading elements convey the logical
  organization to screen readers and make keyboard navigation possible.
- **Forms wired to labels.** Use the HTML `label` element to associate each field with its text label, so
  people know what they're being asked for.
- **A "Skip to Main Content" link at the top of every page.** Imagine listening to the global navigation for
  twenty seconds — or two minutes — before reaching the content, on every page.
- **All content reachable by keyboard.** Not everyone can use a mouse.
- **Significant contrast between text and background.** Never light grey on dark grey.
- **An accessible template or theme.** If the site is built on one, check it was designed to be accessible.

## Two cautions when reporting

**Automated validators behave like grammar checkers, not spell checkers.** They do catch genuine omissions —
missing alt text — but they bury those in vague "you may be doing something wrong" warnings and long lists
of things to check that they admit may not be problems. That's discouraging for people new to the subject
and makes the work look larger than it is. Don't paste validator output into a review; extract the real
findings.

**Don't lead with the population statistic or the benefits-everyone argument.** Both backfire with
developers. A percentage-of-population figure reads as advocacy exaggeration to a team of able-bodied
twenty-somethings, and once one claim sounds inflated they discount the rest. "It helps everyone" is
undermined by closed captioning being the only example ever offered — it lands like crediting the space
programme with Tang. Lead instead with what it concretely changes for someone: blind people with a computer
can now read almost any newspaper or magazine on their own.

Two fears are worth addressing directly when they surface: developers fear more work bolted onto an already
impossible schedule, especially as a top-down initiative with reports and task forces; designers fear
"buttered cats" — cases where accessible design and good design for everyone else are in direct opposition,
forcing a worse experience for the majority. counter-example is a Chicago taxi sign with Braille
embossed on an overlaid sheet of Plexiglas, so both audiences got full-size text instead of each getting
half the space. The opposition is not inevitable.
