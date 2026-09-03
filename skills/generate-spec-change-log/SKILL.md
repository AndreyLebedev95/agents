---
name: generate-spec-change-log
description: Derives a change log for a release or specification revision from structured commit history, then has a person review and edit the result before it is published. Covers the semi-formal commit shape that makes a log derivable at all, the scope vocabulary tested for coverage so no change is invisible, three sections shown only when non-empty, linking each entry to its commit, its issue and the version-to-version comparison, the append-only rule where a revised entry supersedes rather than overwrites, and the four parts of a rationale including the discarded options that are the part always missing. Use whenever a release is being cut and needs release notes, a specification has been revised and downstream readers need to know what moved, commit messages are too thin to derive anything useful from, a decision has been reversed and the record must show it rather than hide it, or someone asks how to structure commit messages so a log can be generated later — even if the ask is just "write up what changed in this release". For analyzing and justifying a single architecture decision with its trade-offs use record-architecture-decisions; for the traceability matrix use build-living-traceability-matrix.
---

# Generating a spec change log

A change log written from memory at the end of a release is a reconstruction, and it is wrong in the specific way reconstructions are wrong: it contains what people remembered and omits what they did not. A change log **derived** from the record of what actually happened contains what happened.

That makes this mostly an extraction job — with one deliberately human step at the end, and one prerequisite that decides whether the whole thing works.

## The prerequisite: check the input first

Generation from commits is only ever as good as the commits. If the history is unstructured, the log will silently under-report — it will look complete, and it will be missing whatever was committed off-convention.

**Check this before generating anything, and report it as a finding if it fails.** Producing a confident-looking log from unusable input is worse than saying the input is unusable, because nobody downstream can tell the difference.

```bash
# What fraction of commits in range follow the convention?
git log <range> --pretty=format:%s | \
  grep -cE '^(feat|fix|docs|style|refactor|perf|test|chore)(\([^)]+\))?: '
git log <range> --oneline | wc -l
```

If adherence is low, you have three honest options, in order of preference: fix the convention going forward and generate from the next release; generate what you can and label the gap explicitly; or write the log by hand and say that is what you did. Do not blend the three silently.

## The output

Two artifacts, and they are different in kind.

**The change log** — a generated skeleton, reviewed and edited by a person before publication:

```
## <version> (<date>)

### Breaking changes
- <subject> ([<commit>](<link>)), closes [#<issue>](<link>)

### New features
- <subject> ([<commit>](<link>))

### Bug fixes
- <subject> ([<commit>](<link>))
```

Sections appear **only when non-empty**. An empty "Breaking changes" heading trains readers to skip the heading, which is exactly the heading you cannot afford them to skip.

**The revision record** — one entry per specification decision, appended, never edited:

```
## <identifier> — <title>
Status:       Accepted | Superseded by <identifier>
Date:         <date>
Context:      <the situation at the time>
Decision:     <what was decided>
Rationale:    <why, including the assumptions that shaped it>
Alternatives: <what else was seriously considered, and why it lost>
Consequences: <what follows, including risks>
```

## Generating the change log

1. **Extract** the entries since the last tag, with their subjects, bodies and footers.
2. **Filter by type** into three groups: new features, bug fixes, breaking changes. Breaking changes come from the footer, not the type, so a commit can be both a feature and breaking — list it in both.
3. **Suppress empty sections** rather than printing an empty heading.
4. **Emit links** — each version to the comparison against the previous version, each entry to its commit, each entry to the issue it closes. A change log without links is a list of assertions; with links it is navigable evidence.
5. **Run it as part of the release**, not as a separate task someone remembers.
6. **Hand the result to a person to review and edit before publication.**

`scripts/build_changelog.py` does steps 1–4 and reports the off-convention commits it could not place, rather than dropping them.

### Why a person edits it

Generation produces the **skeleton**, not the document. Commit subjects are written for the next developer, not for whoever reads the release notes, and the two audiences want different things — a subject saying `fix(pricing): guard against null tier` needs rewriting for anyone outside the codebase.

The reviewer's job is specific:
- Rewrite subjects that only make sense to whoever wrote them
- Merge entries describing one user-visible change made in several commits
- Confirm every breaking change carries its migration path
- Check that nothing derived from the extraction is misleading in aggregate

What the reviewer must **not** do is add things that did not happen, or quietly drop things that did. The generated skeleton is the factual floor.

## The revision record

For a specification revision, the log of *what changed* is not enough on its own; you also need the record of *what was decided and why*. That record has one governing rule.

**Never edit an accepted entry. Supersede it.**

When a decision changes, add a new entry that references the one it replaces, and mark the old one superseded. The old entry stays, in full, saying what was true then. This is what turns the record into a history rather than a snapshot, and it is what lets a later reader see not just what is true but how it came to be — which is usually the question they actually have.

Editing an entry destroys exactly that, and the loss is invisible: the record still looks complete.

### The four parts of a rationale

Recording "why" is not recording a reason. A usable rationale has four parts, and the fourth is the one always omitted and the one that matters most later:

1. **The context at the time** — the stakes, the load, the current priority, the assumptions held, and the constraints coming from people rather than technology.
2. **The problem or requirement** that forced a choice.
3. **The decision itself with its main reasons** — the decision, not merely the solution that resulted.
4. **The alternatives seriously considered**, why they were not chosen, and under what different context they would be.

Design rationale is largely about the options that were discarded, and those are never visible in the artifact itself. If the fourth part is missing, a later reader cannot tell whether an alternative was rejected for a reason that still holds or one that expired years ago — and so they will not touch it.

Include the structuring assumptions. An assumption is usually the real reason a decision took the shape it did, and it is the thing most likely to have quietly stopped being true.

### When the rationale resists being written

If the rationale is hard to state, or two or three credible alternatives cannot be named, that is a finding about the **decision**, not about the writing. Either it was not deliberate, or the first workable option was taken without looking for a better one.

Both are worth surfacing at the time. Note that "we took the first workable option to reach the deadline" is itself a perfectly legitimate rationale — the difference is that once written down it becomes a known, revisitable choice rather than an accident nobody can distinguish from a considered design.

The hardest entries to write honestly are the ones where the decision was made for a poor reason: someone senior insisted, or a developer wanted the technology on their record. Those are the entries most worth having and the least likely to be written. There is no technique that fixes this, only the awareness that a suspiciously thin rationale often marks one.

## Publishing rules

A published change log is an **account of the past**, and that is a specific and useful status.

Knowledge recorded in the context of its moment, clearly dated, is permanently accurate *as an account* — even when the code it describes is long gone. It makes no claim to be current, so it needs no accuracy mechanism and never goes stale. That property is precisely what editing destroys.

So:

- Date it, and identify the version on the document itself.
- Treat it as immutable once published. Never revise a released change log; if something was wrong, say so in the next one.
- Include a link to where the latest version lives.
- Prefer a format that resists casual editing.

## Keep status off the record

The change log says what changed. It does not say how far along anything is.

Progress changes constantly while the record does not, and merging them means the record inherits the faster change rate — so it needs constant updating, and then nobody trusts either. Track execution on a separate overlay and leave the record alone.

The same applies to the transient material around a release: iteration artifacts, estimates, burndown data. Useful before and during, worthless after, and actively harmful once they accumulate into a store that makes the durable material harder to find. Delete them.

## Feeding the generator: what the commits must carry

If you are also designing the convention rather than working with one, `references/commit-convention.md` has the full shape. The three things that decide whether a log can be generated:

**A closed type list.** A small fixed set — feature, fix, documentation, formatting, refactoring, performance, tests, chores. An open list destroys the filtering that justified the formality.

**A scope list with coverage.** The scope names where the change landed. Its one property: every change that could possibly be committed falls under at least one scope. Test it by trying to name changes that fit no scope. An uncovered change is an *invisible* change — missing from every derived view, with nobody the wiser.

**Rationale in the body.** Not a restatement of the diff. Recorded at the moment of the change, so asking the history of a line answers "why is this like this" without a separate lookup.

Enforce the shape with a hook rather than by review. Reviewers do not catch format drift reliably, and the cost of drift is paid silently later.

## Reference material

- `references/commit-convention.md` — the commit shape, closed type list, scope families and the coverage test, footer rules for breaking changes and issue references, and the extraction commands. Read when the convention needs establishing or repairing.
- `references/revision-record.md` — the append-only entry format with supersession, the four parts of a rationale in full, and worked examples of good and thin entries. Read when recording a specification revision rather than generating a release log.
- `scripts/build_changelog.py` — extracts, groups by type, suppresses empty sections, emits linked markdown, and reports off-convention commits rather than dropping them.
