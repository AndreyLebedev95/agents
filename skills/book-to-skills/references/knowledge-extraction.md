# Knowledge Extraction — harvesting a book into a KU ledger

Read this before harvest first segment. It say what count as knowledge unit, how spot each type, what skip, how write ledger.

## Contents
- [The knowledge unit](#the-knowledge-unit)
- [Schema](#schema)
- [The eight types](#the-eight-types)
- [Three-pass protocol](#three-pass-protocol)
- [What to skip](#what-to-skip)
- [Deduplication and conflict](#deduplication-and-conflict)
- [Quality bar](#quality-bar)
- [Worked example](#worked-example)

## The knowledge unit

KU = **one transferable know-how, stated so agent can act on it, with citation back to page**.

Three tests, all must pass:

1. **Action test** — agent behave different knowing this? Definition that only label thing = fail. Definition that change what you look for = pass.
2. **Transfer test** — hold outside book example? "Toyota reduced batch size at Takaoka" = fact. "Batch size drives cycle time; halve batch before adding capacity" = KU.
3. **Non-triviality test** — competent model already do this untold? Then skip. Books full of table stakes; value live in specific, counterintuitive, quantified.

Third test the one people skip, and it what split real ledger from paraphrased summary. Be ruthless: book giving 40 KUs of real substance = great book. Ledger of 300 KUs = ledger of restated sentences.

## Schema

One JSON object per line in `ledger.jsonl`:

```json
{
  "id": "ku-014",
  "type": "heuristic",
  "title": "Halve batch size before adding capacity",
  "claim": "Cycle time falls with batch size; capacity added upstream of a bottleneck only grows WIP.",
  "procedure": ["Locate the constraint by queue length", "Halve batch size at the constraint", "Re-measure cycle time before any capex"],
  "conditions": "Applies to repetitive flow with a stable constraint; not to one-off project work.",
  "evidence": "Plant case study, ~30% cycle-time reduction",
  "confidence": "high",
  "anchor": "An hour lost at a bottleneck is an hour lost for the entire system.",
  "page": "p.158",
  "segment": "seg-0009",
  "tags": ["flow", "constraints", "process-design"]
}
```

Required: `id`, `type`, `title`, `claim`, `anchor`, `page`/`segment`.
`procedure` required for `procedure`, `framework`, `checklist` types.
`conditions` matter more than look — heuristic without applicability envelope = how skill end up giving confident wrong advice in next-door domain.

`confidence`: `high` (author state as rule and back it), `medium` (asserted, thin support), `low` (aside, speculation, author hedge). Carry forward — low confidence KUs may still go in skill, but flagged.

## The eight types

| Type | What it is | Recognition cues |
|---|---|---|
| `principle` | Law domain obey | "always", "fundamentally", stated as invariant |
| `procedure` | Ordered sequence make outcome | numbered steps, "first… then…" |
| `heuristic` | Decision rule under uncertainty | "if X, prefer Y", rules of thumb, thresholds |
| `framework` | Named model, parts + relations | diagrams, 2×2s, named stages, acronyms |
| `checklist` | Items to verify, order no matter | bulleted "make sure", pre-flight lists |
| `anti-pattern` | Failure mode + tell + fix | "the most common mistake", war stories with moral |
| `metric` | What measure, and number that matter | formulas, thresholds, ratios, benchmarks |
| `vocabulary` | Distinction that change seeing | coined terms, "there are two kinds of…" |

`anti-pattern` = highest yield, most missed. Books teach much by naming failure as by prescribe success, and agent that spot failure mode early worth more than one reciting happy path. Hunt these on purpose: every war story got moral, moral = KU.

`vocabulary` = second most undervalued. Distinction reader not draw before ("load-bearing vs. decorative complexity") change what agent notice. Include only when distinction got consequence — mere synonym not KU.

## Three-pass protocol

**Pass 1 — Map (skim, cheap).** Already done in Phase 0. TOC, intro, conclusion, chapter summaries. Give thesis, structure, yield forecast. No extract yet; you not know book vocabulary until you see its shape.

**Pass 2 — Harvest (segment by segment).** Each segment: read, extract KUs, append to ledger, note open questions + forward refs. Keep running count, compare to forecast. Segment forecast dense but yield two KUs = you read too fast, or forecast wrong — decide which before move on.

**Pass 3 — Consolidate (whole ledger).** After last segment: merge dupes, resolve contradictions, promote recurring themes, demote one-offs, re-run non-triviality test with fresh eyes. Books repeat core claims every chapter; consolidation where fifteen restatements collapse into one strong KU with five citations.

## What to skip

- Story and anecdote, except moral (become `anti-pattern` or `heuristic`).
- Author biography, acknowledgements, credentialing, "why I wrote this book".
- Motivation and persuasion — chapter arguing topic matter. Agent need method, not sales pitch.
- Restatements of same claim later. Cite them onto existing KU instead.
- Era-bound stuff: tool versions, org charts, market conditions of decade. Keep mechanism, drop instance.
- Anything competent model already do by default (non-triviality test).

## Deduplication and conflict

Before append KU, scan ledger for same claim. If found, add new page to existing KU citations and strengthen its `evidence` — no second entry.

When book contradict itself (common in edited volumes, and books written over years), keep both, link with `conflicts_with` field, record conditions each apply. If conditions not stated, say so. Skill that quietly pick one side of unresolved tension teach false confidence.

When book contradict well-established current practice, keep book version as KU and add `note` flagging divergence. Phase 3 decide what do about it; harvest job = fidelity, not arbitration.

## Quality bar

Before close harvest, spot-check five random KUs:

- Can you act on it without re-read book? If no, `procedure` too thin.
- Does `anchor` really support `claim`, or you drift past text?
- Survive non-triviality test on second look?
- `conditions` filled, or you smuggle universal claim book never made?

If two of five fail, extraction too shallow — re-harvest densest segments before clustering. Clustering bad KUs make confident, useless skills.

## Worked example

Source passage (paraphrased): chapter argue teams add reviewers to catch defects, but defect detection per reviewer drop sharp past third, while scheduling delay grow linear; author recommend three reviewers and hard 24-hour SLA, and describe team that cut review latency 60% by going six reviewers to three.

Yields **three** KUs, not one:

1. `metric` — "Reviewer marginal yield collapses after three" (claim: detection per added reviewer fall sharp past 3; delay grow linear). Confidence high.
2. `heuristic` — "Cap reviewers at three, enforce a 24-hour SLA" (procedure: cap; set SLA; escalate instead of add reviewers). Conditions: routine change review, not security-critical or irreversible changes.
3. `anti-pattern` — "Adding reviewers to fix a quality problem" (tell: review latency rising while defect escape rate flat; fix: cut reviewer count, fix upstream cause).

*Not* KU: team name, 60% figure as promise (belong in `evidence`, not `claim`), and chapter argument that code review matter at all.