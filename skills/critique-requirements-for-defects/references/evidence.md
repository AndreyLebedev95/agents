# The cost of unclarified requirements

Read this when you need to justify spending review time on a requirements artifact to someone who thinks a defect-hunting pass is pedantry or a waste of schedule.

## The core asymmetry: defects get exponentially more expensive to fix the later they're caught

Across analyses of real corporate software projects, the relative cost to fix a defect traced back to a false assumption in the requirements phase climbs sharply with every phase the project moves through before the defect is caught — not linearly, but by roughly an order of magnitude at each major transition (requirements → design → build → post-release). A defect that costs one unit to fix while it's still just words on a page can cost many times that once it's embedded in a design, and dramatically more once it's shipped and someone has to patch a live system and everything built on top of it.

This is the entire economic case for attacking requirements early: the review itself is cheap relative to literally every later point at which the same defect could instead be caught.

And this estimate is almost certainly conservative. It only counts projects that were completed at all — a meaningful fraction of large projects are never finished, and poor requirements definition is a major contributor to that outcome. Cost-to-fix data collected only from finished projects necessarily excludes the most expensive failure mode of all: the project that never shipped.

## Real reviews find ambiguity at real density

This isn't a hypothetical concern reserved for edge cases. A requirements review of a single eight-page section of a real production specification — one section out of several hundred making up the full document — turned up over a hundred distinct ambiguities, each interpreted at least two different ways by different reviewers looking at the same text. Extrapolated across a document of that size, the implied number of downstream decisions resting on unclarified requirements runs well into six figures. Guessing correctly on that many independent decisions is not a realistic strategy.

## Direct questioning narrows visible ambiguity, but leaves a lot invisible

Even a thorough round of direct clarifying questions — the obvious, default way to reduce ambiguity — leaves a surprising amount on the table. In one large-scale exercise, a simple, ambiguous product requirement produced cost estimates spanning many orders of magnitude on first read. After a full sequence of specific, well-chosen clarifying questions (covering timeline, scope, capacity, materials, environment, distance, speed, reliability, and cost), the estimate range narrowed enormously — and still spanned roughly 500x, because one variable nobody happened to ask about (in this case, production volume) got silently and independently resolved differently by every person answering. The lesson isn't that direct questions don't work — it's that they only close the gaps someone thought to ask about, and there is always at least one gap nobody thought to ask about.

## When an unstated assumption becomes a design decision, the failure can be catastrophic

A requirements defect frequently doesn't look like a gap in a document — it looks like a perfectly reasonable design decision made downstream, built on an assumption that was never written down as a requirement and so was never reviewed, tested, or challenged. The decision is locally sound engineering; the failure shows up only once the unstated assumption turns out to be false, often at a scale far beyond the original document review.

Two well-documented examples of this pattern, both involving assumptions about product usage that were never stated as explicit requirements and never verified:

- A vehicle fuel tank's mounting position was a sound engineering decision given an unstated assumption that rear-impact collisions at a certain severity would not occur. When that assumption proved false in the field, the resulting litigation and recall costs ran into the hundreds of millions of dollars — without counting the human cost.
- A building-materials product line was developed and marketed on an unstated assumption that a particular material was environmentally safe for everyone exposed to it. When that assumption proved false, the resulting liability ran into the tens of thousands of individual claims and billions of dollars, and eventually bankrupted the manufacturer.

Neither failure originated in a design flaw in the conventional sense. Both originated in an assumption that was true enough to seem safe to leave unstated — exactly the kind of assumption a systematic requirements review is built to surface before it gets built on.
