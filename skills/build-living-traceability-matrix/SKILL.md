---
name: build-living-traceability-matrix
description: Generates a traceability matrix or coverage report as a derived view of the artifacts, regenerated on every build, rather than a document anyone maintains by hand. Covers the four-step generation pipeline, consolidating dispersed facts by scanning a perimeter into a keyed aggregate, selecting by stable criteria instead of naming artifacts, one message per view and the filtering that implies, serving several audiences from one tagged corpus, publishing immutable versioned snapshots for people who cannot read the repository, and keeping any derived store droppable so it never becomes a second source of truth. Use whenever someone needs an RTM, a requirements coverage report, or any matrix linking requirements to specs, components, tests or commits; when wiring such a report into CI; when someone is about to update a traceability matrix or coverage spreadsheet by hand; when a matrix has grown too large to read; or when a derived document is needed for auditors or stakeholders without repository access — even if they just say "can you pull together which tests cover which requirements". For deciding where the links live in the first place use design-traceability-scheme; for finding what has become orphaned or drifted use check-traceability-integrity.
---

# Building a living traceability matrix

A traceability matrix is not a document. It is a **query over the artifacts, rendered**. Everything here follows from that: if the matrix is generated on every build from the links that live on the artifacts themselves, it is true on the day it is read, and nobody maintains it. If it is a file somebody edits, it is a second source of truth that will disagree with the first, and the disagreement will be discovered by an auditor.

The first time you generate one, expect the output to be wrong in interesting ways. That is the point — the gap between the generated view and what the team believed was true is a set of findings about the system, not errors in the generator.

## The output

A generator committed alongside what it reads, wired into the build, producing:

```
# Traceability matrix — <scope>
Generated: <timestamp>   Version: <version>   Source: <commit>

| REQ-ID | Spec section | Components | Tests | Commits |
|--------|--------------|------------|-------|---------|
| ...    | ...          | ...        | ...   | ...     |

## Unmatched elements
<elements inside the perimeter carrying no key — reported, never skipped>

## What this matrix cannot see
<the blind spots, stated>
```

## The pipeline

Every generated document is the same four steps. Getting them in this order matters, because each one narrows what the next has to handle.

### 1. Select

Name the perimeter to scan, and say explicitly what is outside it. Name the key the dispersed facts share — the requirement identifier, usually.

**Express selections as criteria, never as lists of artifact names.** A view that lists the artifacts it covers by name or path is copy-and-paste under another name: it goes stale, it makes every change more expensive, and it depends on someone remembering to update it. Use criteria that stay true as artifacts move:

- a folder or module location
- a naming convention
- a marker or tag
- an entry in a registry you control
- the output of a tool

When no criterion can express the selection you want, add the missing marker to the artifacts. Do not fall back to a list.

### 2. Filter

Drop everything that does not serve this view's single objective. Filter aggressively by default and provide an explicit override, rather than trying to encode every case in the rule — the default-plus-exceptions form stays legible where a complete rule set does not.

Tune the default against the actual style of the codebase. The same construct means different things in different codebases, so a filter that works well in one will overreach in another.

### 3. Project

From each surviving item, extract only the fields this view uses. Resist showing everything you have; the extraction step is where a matrix becomes readable or unreadable.

### 4. Convert

Map items and their relationships into the output format, giving every dimension a declared meaning (see below).

Then **re-run the whole pipeline on every change** rather than updating the output. If rendering is complex, chain intermediate models rather than doing it in one pass.

The mechanics are never the hard part. The hard part is the editorial judgment inside steps 1 and 2 — what to select, what to drop, what to bring in from elsewhere.

## Consolidation: how the scan actually works

Knowledge that is conceptually one thing is stored as many small facts across many files. Recovering the whole is consolidation, and it works like a `GROUP BY`:

1. Define the perimeter to scan.
2. Choose the key the dispersed facts have in common.
3. Scan every element in the perimeter, adding each fact to a dictionary under its key.
4. Narrow the scan to the subset that serves this view rather than aggregating everything.
5. **Do not store the result.** Regenerate it, unless storage is needed purely as a cache.

The scattered facts stay authoritative. The consolidated view is a derived publication and has no authority of its own.

**Consolidation only sees facts that carry the key.** Elements missing the key are invisible to the scan — and that is itself a finding, not a gap to paper over. Report them in an "unmatched elements" section. A generator that silently skips what it does not recognize hides exactly what you built it to surface.

`scripts/build_matrix.py` implements this scan: it walks a perimeter, extracts markers by prefix, groups by key, and emits the matrix plus an unmatched-elements section. Read `references/generation-pipeline.md` when adapting it, or when the estate is too large for a single scan.

## Sources: read from whatever is already authoritative

Most of the chain already exists somewhere. The work is deciding, per fact, which tool is the sole authority, and extracting from there:

| Link | Usually authoritative | How to read it |
|---|---|---|
| REQ-ID → spec section | the specification files themselves | parse; tags or headings |
| REQ-ID → component | markers on the components | scan the perimeter |
| REQ-ID → test | markers or tags on the tests | scan the test perimeter |
| REQ-ID → commit | version control history | the log, filtered by convention |

Declare exactly one tool authoritative per fact and stop treating the others as sources. Extract through the tool's command line or API — search for an existing plugin first. Query a tool's internal database only as a last resort; it is not part of the API and can change without notice.

One link is nearly free and routinely missed: the history of a change names the files that changed *with* it, and those include the tests written alongside. That is a zero-cost connection from a change to its test coverage, needing no index — provided commits are scoped to one logical change.

Extraction is only ever as good as what was entered. Commit messages that say nothing yield nothing, which makes the commit convention a prerequisite rather than a nicety.

## Editorial rules

These are what separate a matrix people use from a matrix people stop opening.

**One view, one message, stated as a sentence with a verb.** "Every acceptance criterion has at least one passing test" is a message. "Requirements and tests" is a heading that carries none, leaving the reader to guess. At minimum, name the view after the message it makes.

**Too much information is as useless as no information.** A view rendering everything the tool can reach answers no question. Filter to what contributes — ideally five to nine items in any one view. Beyond that, filter or rank rather than shrinking the type.

**When you want to add something, make another view.** Adding one more dimension to a view that works is the slow version of the same failure. Because the view is generated, another one costs almost nothing — which is exactly the freedom hand-maintained documents never had.

**Give every dimension a declared meaning.** Position, layout, size and colour will be read as meaningful whether or not you intended them. Assign each deliberately — axes for direction or causality, proximity for similarity, colour for severity or status — and state the meanings, because a channel with an undeclared meaning is read as decoration.

**Group entries the way people think about them.** Mirror the reader's mental grouping rather than the file layout. But verify the omissions are deliberate: an element dropped for lack of a marker is a gap, not a filter.

**Describe by difference.** Where a view is read repeatedly, state what changed against the known baseline rather than restating the whole. Five to seven distinctive points describe a specific case more precisely than a full re-listing, and far more quickly.

## Serving several audiences

One well-tagged corpus yields a different report per audience. Each audience is a **query**, not a document — building one document per audience by hand produces documents that immediately disagree with each other.

The standard cuts:

- **Engineering** — the full matrix, plus unmatched elements
- **Sponsors** — in-progress and pending items, and the proportion of acceptance criteria currently passing
- **Newcomers** — the nominal path through each area
- **Auditors and compliance** — everything except work in progress, with acceptance criteria summarized first and the remainder in an addendum

Regenerate all of them from the same corpus on the same build. See `references/audience-views.md`.

## Publishing

Any document generated from a single source is a **snapshot of a moment** and must behave like one, or people will edit it and it becomes a competing source of truth.

- Treat it as immutable. Never edit a published matrix.
- Prefer formats that resist editing, and set locking flags where available. The goal is not security — it is making it easier to fix the source and republish than to patch the output.
- Identify the version on the document itself, and the commit it was generated from.
- Include a link to where the latest version lives.
- Link each entry back to its source location. Independently of the link, keep the wording verbatim from the source, so that even when a link breaks the text itself works as a search term that finds the origin.
- Route references through a registry you control where you can, so a broken target is repaired once rather than at every referring site. Where the target is outside your control, prefer a link to a *search* over a link to a path: a search built from stable criteria survives moves and renames, at the cost of the reader picking from a short result list.

## Storage and scale

**Derived knowledge is never a source of truth.** If cached for performance, it must be droppable and rebuildable from scratch at any moment. Keep a one-command rebuild path and exercise it.

Default to a full scan during the build. Only when the estate is genuinely too large for a sequential scan should consolidation become incremental, with each part's build pushing a contribution into a shared state — and then that shared state is *less trusted* than any individual contribution. When the aggregate disagrees with a contribution, trust the contribution; when it looks wrong, drop it and let it regrow.

Incremental consolidation introduces a staleness window and its own drift. Take it only when the full scan is genuinely impractical.

## Wiring it in

Keep the generator in the repository beside what it reads, and run it on every build or on a one-click build. That makes the matrix a standing mirror of the actual state — consultable in review, in planning, or at random.

Its main value is the unwelcome surprise. It shows the system as it is rather than as intended, which is why it must actually be looked at; a generated view nobody opens provides feedback to nobody.

Ship something crude early. The first output is feedback on two things at once — the generator's filtering, and the artifacts it read. Then alternate: fix the source, add markers where meaning is missing, improve the filtering, repeat. There is no end state, and treating it as a project to be finished misreads what it is.

**When the generated output reads badly, fix the source, not the output.** A derived view is a mirror. An unclear entry means an unclear name, a missing marker, or a structure that does not match how people think about it. Patching the output breaks the only property that made it worth building.

## Publish the blind spots

State what the matrix cannot see, beside the matrix, before anyone reads it — absence will otherwise be read as evidence:

- **Uncovered mechanisms.** Links created by a route the scan does not cover are simply missing.
- **Shared-state coupling.** A relationship neither side declares — another system reading your database directly — is undetectable from the artifacts and surfaces only in conversation.
- **Declared versus exercised.** The matrix shows the links present in the artifacts, not which are exercised in production. Label which one you are showing.

## Reference material

- `references/generation-pipeline.md` — the four steps worked end to end, consolidation as a keyed scan, incremental consolidation at scale, and the droppable-cache rule. Read when adapting the scanner or when a full scan stops being practical.
- `references/audience-views.md` — one corpus, many queries: the standard audience cuts, what each shows, and how to structure a long report so it can be skimmed. Read when a second audience needs its own view.
- `scripts/build_matrix.py` — perimeter scan, marker extraction by prefix, grouping by key, matrix and unmatched-elements output.
