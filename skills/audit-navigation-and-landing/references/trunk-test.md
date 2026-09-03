# The trunk test

acid test for navigation. Source:.6.

## The premise

Imagine you've been blindfolded, locked in the trunk of a car, driven around for a while, and dumped on a
page somewhere deep in the bowels of a site. When your vision clears, a well-designed page lets you answer
six questions without hesitation.

The abduction framing isn't a joke — it's the correction to a real design assumption. When designing pages
it's tempting to imagine people arriving at the Home page and following the neat paths you laid out. In
reality they're dropped into the middle of a site from a search engine, a social post, or a friend's email,
having never seen the navigation scheme.

The blindfold matters too. Your vision should be slightly blurry, because the true test isn't whether you
can work it out given enough time and close scrutiny. The standard is that these elements pop off the page
so clearly that it doesn't matter whether you're looking closely. You want to be relying solely on the
overall appearance of things, not the details.

## How to run it

**Step 1.** Choose a page anywhere in the site at random, and print it.

**Step 2.** Hold it at arm's length, or squint, so you can't really study it closely.

**Step 3.** As quickly as possible, find and circle each of these:

- Site ID
- Page name
- Sections (primary navigation)
- Local navigation
- "You are here" indicator(s)
- Search

**Step 4.** Try it on your own site. Then ask some other people to try it too. The results are often
surprising.

## Picking the sample

One page tells you about that page, not about the navigation. Sample at least three, chosen to stress
different things:

- A **deep content page** — three or more levels down, ideally one that gets external traffic.
- A **section front** — the level most likely to have been designed carefully.
- A **leaf page in a neglected corner** — an old press release, a policy page, a support article. Ad hoc
  navigation shows up here first.

If the site has a mobile layout, run the same three at mobile width. Loss of the "you are here" marker and
of local navigation is the common casualty.

## Worksheet

```
Page: ____________________________________  Level: ____  Sampled because: ____________

| # | Question                            | Element              | Found? | Time to find | Notes |
|---|-------------------------------------|----------------------|--------|--------------|-------|
| 1 | What site is this?                  | Site ID              |        |              |       |
| 2 | What page am I on?                  | Page name            |        |              |       |
| 3 | What are the major sections?        | Sections / primary   |        |              |       |
| 4 | What are my options at this level?  | Local navigation     |        |              |       |
| 5 | Where am I in the scheme of things? | "You are here"       |        |              |       |
| 6 | How can I search?                   | Search box or link   |        |              |       |

Verdict: PASS / PASS WITH HESITATION / FAIL
Worst gap: ______________________________________________
```

"Pass with hesitation" is a real result and worth recording separately from a pass — hesitation at arm's
length means failure at speed.

## Reading the results

Each failed question maps to a specific fix:

| Failed | Usual cause | Fix |
|---|---|---|
| Site ID | Logo too small, or absent below the top level | Top-left, framing the page, brand-logo attributes |
| Page name | Relying on the highlighted nav entry instead | Give the page a real name, framing its unique content, usually the largest text |
| Sections | Primary nav dropped or collapsed on deep pages | Persistent navigation must be genuinely persistent |
| Local navigation | Never designed below level two | Design navigation for every level before visual design |
| "You are here" | Marker too subtle | Two visual distinctions; double the prominence |
| Search | Box missing, or only on the Home page | Box on every page, or at minimum a link to a search page |

If the same question fails across all three sampled pages, that's a structural gap, not a page defect —
report it as one finding about the navigation system, not three about pages.
