---
name: book-to-skills
description: "Turn a book into a working toolkit. Reads a book (PDF/EPUB/TXT/MD) end to end, harvests its durable know-how into a cited knowledge ledger, clusters that into task-shaped skills built with the skill-creator skill, then composes subagents out of those skills. Use whenever someone points at a book, textbook, manual, course, or long-form document and wants reusable capability from it: 'read this book and make skills out of it', 'extract the knowledge from <book> as skills', 'build an agent from this book', 'turn <book> into a subagent', 'mine this PDF for expertise', 'I want Claude to actually know this book'. Also use for book-length documentation sets and personal note archives. Triggers: book, ebook, PDF, EPUB, chapter, textbook, manual, extract knowledge, distill, make skills, build agent from book."
---
# Book → Skills → Subagents

Three-stage refinery. Book go in; cited knowledge ledger, task-shaped skills, and subagents that wield them come out.

```
book file ──▶ [0] intake ──▶ [1] harvest ──▶ [2] cluster ──▶ [3] charter
                                                                  │
              [6] register ◀── [5] compose agents ◀── [4] build skills
```

Point is middle: book organized for *reader* going front to back, skill organized for *agent* facing task. Chapters wrong unit. Never let book table of contents become skill list — that make summaries, not capability. Reorganize around jobs to be done.

## What this produces

All land in workspace so run resumable and auditable:

```
book-forge/<book-slug>/
├── source/            # converted text + segments + manifest.json (from scripts/book_ingest.py)
├── map.md             # structure, thesis, reading plan, segment→topic index
├── ledger.jsonl       # knowledge units, one JSON object per line, each cited
├── charters/          # one <skill-name>.md charter per candidate skill
├── agents/            # drafted subagent definitions
└── report.md          # final: what was built, what was dropped, coverage
```

Final deliverables live outside workspace: skills in `~/.agents/skills/<name>/` and agents in `~/.agents/agents/<name>/<name>.md`, both symlinked into `~/.claude/`. Author under `~/.agents/`; never write directly into `~/.claude/`.

## When not to use this

- Doc under ~30 pages: read it, write one skill direct. Refinery cost more than it give.
- Reference stuff looked up, not applied (API listings, constant tables): that go in `references/` file inside existing skill, not new skill.
- Fiction, memoir, polemic with no transferable procedure: say so plain before burning long read. Some books give one heuristic and nothing more; fine outcome to report, but user must hear early, not after six phases.

---

## Phase 0 — Intake

Find file, normalize it. No paste whole book into context; segment first.

```bash
python3 <skill-dir>/scripts/book_ingest.py "<path-to-book>" --out book-forge/<slug>/source
```

Handles PDF (`pdftotext -layout`, page anchors kept), EPUB/MOBI/AZW3 (`ebook-convert`), plain text/markdown. Writes `segments/seg-NNNN.md` (~24k chars each, page-anchored) plus `manifest.json` with detected headings.

Then read `manifest.json`, skim first and last segments plus any TOC, write `map.md`:

- **Thesis** — one claim book exist to defend, in one sentence.
- **Structure** — parts/chapters with segment ranges.
- **Yield forecast** — which segments look dense with procedure (harvest careful) and which look like narrative padding (skim). Books rarely uniform; front-load this judgment, save half the reading.
- **Reading plan** — segment order and grouping.

Report forecast to user before long read, plus estimated skill count. Cheapest moment to redirect.

## Phase 1 — Harvest

Read segments in order, extract **knowledge units** (KUs) into `ledger.jsonl` as you go. Append after each segment — never hold book's worth of extraction in working memory, never wait until end to write.

KU is one durable, transferable piece of know-how with citation. Schema, eight KU types with recognition cues, skip list, dedup rules all in **`references/knowledge-extraction.md`** — read before first segment.

Bar, one line: *would agent act different if it knew this?* If no, it background, not KU.

Provenance non-negotiable. Every KU carry `page` (or segment) plus short verbatim `anchor` of ≤25 words. Anchors exist so later phases can verify claim came from book not your priors, and so finished skills can cite. Quote minimal — restate everything else in own words.

## Phase 2 — Cluster

Ledger complete: ignore chapter boundaries entire, group KUs by **task they serve**. Cluster become candidate skill when it pass worthiness test in **`references/skill-charter.md`**; clusters that fail get merged, demoted to reference file, or dropped.

Target **3–8 skills per book**. Fewer mean you flattened distinct jobs into mush; more mean you sliced by topic not task, and descriptions will collide and misfire at trigger time. 400-page book that yield two real skills is legit result — say so, no padding.

Check collisions against skills already exist (`ls ~/.claude/skills/`, `ls ~/.agents/skills/`). If book sharpen existing skill, propose editing that skill instead of near-duplicate; two skills with overlapping descriptions degrade both.

## Phase 3 — Charter

Write one charter per surviving cluster to `charters/<skill-name>.md`. Charter is brief you hand to skill-creator: name, trigger contexts, procedure skill teaches, output format, which KUs back which section, and what belong in `references/` rather than `SKILL.md`. Template and rules: **`references/skill-charter.md`**.

**Show charter list to user, get approval before building.** Main checkpoint of whole pipeline — cheap to cut skill here, expensive after it built and evaluated.

## Phase 4 — Build with skill-creator

Build approved charters **one at a time**, using `skill-creator` skill for each:

```
Skill(skill="skill-creator", args="create a skill from the charter at book-forge/<slug>/charters/<name>.md")
```

Then follow skill-creator own process. What to carry in so it no need re-interview you:

- Charter answer its intent questions (what skill enables, when it triggers, output format) — say so and paste charter, no make user repeat.
- Write skill to `~/.agents/skills/<name>/` (this environment convention: skills authored there, symlinked into `~/.claude/skills/`).
- Evals worth running for skills with checkable outputs (produced artifact, fixed workflow, transformation). For judgment-shaped skills from book — critique, design taste, negotiation posture — quantitative assertions measure nothing; tell user that, iterate qualitative instead of faking rigor.
- Do run skill-creator description optimizer at end when several sibling skills came from one book. Sibling skills exactly the case where trigger descriptions bleed together, and that loop is what separate them.

Fidelity rules while skill being written:

- Every instruction trace to KU id **in the charter**, not in shipped skill. If you cannot cite it, it your opinion — cut it or mark explicit as addition beyond book.
- **Ship skill with no source in it.** Finished skill teach the method as method. Strip before install: book title, author name, "distilled from / adapted from" line, `[ku-NNN]` markers, ledger path, chapter numbers, and attributive prose ("the author's example", "Krug reports", "as X argues"). Rename branded concepts to what they do — "Krug's Third Law" become "cut half the words, then half again".
  Why: skill that cite a book read as book report and invite the model to defer to authority instead of apply rule. Practitioner do not preface advice with footnote. Provenance is real and must survive — it live in `ledger.jsonl` and `charters/`, which is where auditing happen. Reader who want the source read charter; model executing task should not carry it.
  Keep: mechanism, threshold, number, counterintuitive claim, and any dated-figure warning. Evidence that make rule credible stay, stripped of attribution — "a study of 16 screen-reader users found…" fine, "Theofanos and Redish (2003) found…" not. Same for named tests: "Nielsen's test" become "the substitution test", named after what it do.
  One thing not source, so keep it: **further-reading pointer**. Book the source recommend to *reader* is resource, not provenance — "Worth reading: Cialdini, *Influence*" stay. Line is whether name prop up a claim (strip) or point somewhere useful (keep).
  Strip with regex then read every hit — attributive prose leave behind dangling pronoun ("He reports being surprised"), orphan clause, and mangled sentence where two rules overlap. Grep for `\bhe (says|points|thinks|reports)|his own|the author` after, and reread each edited file. Budget this: strip is fast, repair is not.
  Verify before register: `grep -rniE '<author>|<book title>|ku-[0-9]|ch\.[0-9]|distilled|the author' <skill-dir>/` return nothing.
- Keep book mechanisms, thresholds, numbers. Drop era-bound anecdotes; 1994 case study is evidence, not instruction. Where number contested or dated, say so in skill instead of silent modernizing.
- Preserve author counterintuitive claims. Obvious parts of book are parts model already know; value concentrated in what surprised you.
- If skill-creator unavailable, author skill direct against its guide at `~/.claude/skills/skill-creator/SKILL.md` and note in `report.md` that evals skipped.

## Phase 5 — Compose subagents

Skills are capabilities; agent is *role* that hold several of them and know loop they run in. Compose agent only when two or more new skills fire together on recurring workflow — lone skill wrapped in agent add indirection and nothing else.

Design rules, frontmatter spec for this environment, composition patterns, body template: **`references/agent-composition.md`**.

Draft into `agents/`, get user approval, then install to `~/.agents/agents/<name>/<name>.md` and register, which symlinks it into `~/.claude/agents/`.

## Phase 6 — Register and report

```bash
python3 <skill-dir>/scripts/register.py --skill ~/.agents/skills/<name>      # validate + symlink
python3 <skill-dir>/scripts/register.py --agent ~/.agents/agents/<name>/<name>.md   # validate + symlink
python3 <skill-dir>/scripts/register.py --list
```

Then write `report.md`:

- Skills built, with KU ids and page ranges behind each.
- Agents composed and skills they hold.
- **What deliberately dropped and why** — most useful section. Tell user which parts of book still only in book, stop next run from re-litigating same rejections.
- Coverage: which segments produced no KUs, so thin extraction visible not hidden.

Finally, tell user how to invoke what was built: skill names trigger on description match, agents via Agent tool or by name.

---

## Running long

Full book is long job. Protect it:

- **Checkpoint after every segment.** Append KUs to `ledger.jsonl` immediate. If context compacted or session drop, `map.md` + `ledger.jsonl` + `charters/` enough to resume cold — on resume, read those three, find last cited segment, continue.
- **Delegate read when book big.** For books over ~20 segments, harvest can fan out to subagents (one per segment range, each appending to own `ledger-part-N.jsonl`, concatenated after). Only do this if user ask or book genuinely long — cold subagent re-derive context main session already have, so it pay off on volume, not on principle. Give each one `references/knowledge-extraction.md` and the map so output schema-identical.
- **No degrade under length.** Extraction quality decay across long read: later chapters get one-line KUs while early ones got five. Watch KU count per segment against yield forecast; if dense segment produced two KUs, go back.

## Failure modes worth naming

| Symptom | Cause | Fix |
|---|---|---|
| Skills mirror chapter titles | Clustered by topic, not task | Re-cluster in Phase 2 around jobs |
| Skill reads like book summary | KUs were *claims*, not *procedures* | Convert to imperative steps; drop what no convert |
| Twelve tiny skills | No worthiness test applied | Merge to 3–8; demote rest to references |
| Skills never trigger | Sibling descriptions overlap | Run skill-creator description optimizer across set |
| Instructions no one can trace | Priors leaked in | Enforce KU ids per instruction; cut orphans |
| Agent that just call one skill | Composition without workflow | Delete agent; skill is deliverable |