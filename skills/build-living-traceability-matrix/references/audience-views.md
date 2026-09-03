# Audience views

Read when a second audience needs its own view of the same corpus.

## Contents
- [One corpus, many queries](#one-corpus-many-queries)
- [The standard cuts](#the-standard-cuts)
- [Structuring a long report](#structuring-a-long-report)
- [Reporting change rather than state](#reporting-change-rather-than-state)

## One corpus, many queries

A well-tagged body of items yields a different report per audience without maintaining separate documents. Each audience is a **query over the tags**, evaluated on the same build.

The alternative — one hand-maintained document per audience — produces documents that immediately disagree with each other, and the disagreement is discovered by whichever audience is least equipped to resolve it.

This only works to the extent that the metadata exists to select on. Curation is possible exactly as far as the tagging goes; where a cut you need cannot be expressed, the fix is to add the missing tag to the items, not to hand-build the view.

## The standard cuts

| Audience | Query | Shows |
|---|---|---|
| Engineering | everything, plus unmatched elements | The full matrix. This is the only cut where unmatched elements belong up front — they are work items. |
| Sponsors and management | in-progress and pending items; the proportion of acceptance criteria currently passing | Progress and its shape. Not the full matrix, which reads as noise at this level. |
| Newcomers | the nominal path through each area | One end-to-end route per area, ordered. Enough to orient, not enough to overwhelm. |
| Auditors and compliance | everything except work in progress | Acceptance criteria summarized first, the remainder in an addendum. Compliance audiences want completeness, but completeness in the order they will check it. |
| Domain experts with little time | the key examples and the contested items | The handful of cases where a decision is genuinely at stake. |

Regenerate all of them on the same build from the same corpus. A cut that is generated weekly while another is generated per build will diverge, and you will have reinvented the problem.

## Structuring a long report

A matrix of any size will be skimmed, not read. Structure for that:

- **Headings that say what the section contains**, not what it is about, so a reader can decide from the heading alone whether to open it.
- **Mark optional sections as optional.** Readers who cannot tell what is skippable read nothing.
- **Split narrative from reference.** A part meant to be read through, and a part meant to be consulted when a specific question arises. Never require the reference part to be read in order.
- **Five to nine items in any one view.** Beyond that, filter or rank. This is a limit on a single view, not on the underlying data — the data can be complete while any one view of it is not.

Where a set is too large to show whole, mark the subset that actually matters and let the generator fall back to it: show everything while the set is small — around seven items — and only the marked core above that.

## Reporting change rather than state

For any view read repeatedly — a matrix regenerated every build, a coverage report at every stage gate — restating the whole thing each time buries the change in the restatement.

Describe by **difference against the known baseline**. Five to seven distinctive points describe a specific case more precisely and far faster than a full re-listing, because the reader already holds the baseline and only needs the delta.

Practically, for a regenerated matrix:

- What entered the matrix since the last run
- What left it
- Which links broke
- Which requirements changed coverage state
- The unmatched elements that are new

Keep the full matrix available and link to it. Lead with the difference.

The prerequisite is knowing what the audience already holds, which is easy in conversation and hard in writing. Learn it from the questions people actually ask, and from whoever fields their requests.
