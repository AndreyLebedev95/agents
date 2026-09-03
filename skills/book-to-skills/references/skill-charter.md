# Clustering and Chartering — from ledger to skill briefs

Read at Phase 2. Cover: how group KU into candidate skill, which candidate earn skill, how name+describe, and charter format hand to skill-creator.

## Contents
- [Cluster by task, not by topic](#cluster-by-task-not-by-topic)
- [The worthiness test](#the-worthiness-test)
- [Sizing the set](#sizing-the-set)
- [Naming](#naming)
- [Writing the description](#writing-the-description)
- [SKILL.md vs references](#skillmd-vs-references)
- [Charter template](#charter-template)
- [Handing off to skill-creator](#handing-off-to-skill-creator)

## Cluster by task, not by topic

Sort ledger by question **"what someone try do when need this?"**

Mechanical way: each KU, write trigger situation in user voice — "I'm about to design a schema and don't know where to denormalize", "my review queue is backing up". Then group KU with same situation. Group = candidate skill. Chapter membership no matter, and mislead: good book spread one task over five chapter, cram three unrelated task in one.

Two sign cluster real:

- **KU types mix.** Healthy cluster have `framework` or `principle` for orient, `procedure`/`checklist` for do, `heuristic` for judgment call, `anti-pattern` for fail mode. Cluster of only `principle` KU = worldview, not skill — belong in reference file or agent system prompt.
- **Have natural output.** Can name artifact or decision skill make. "Understanding constraints" make nothing; "find and exploit the constraint in a workflow" make diagnosis + change plan.

## The worthiness test

Cluster become skill only if yes to all five:

1. **Recurring** — situation come again across project, not once?
2. **Non-obvious** — make model act different than default? If answer "just make more thorough", not skill.
3. **Bounded** — can say when trigger *and* when not? Unbounded skill either never fire or fire on everything.
4. **Actionable** — end in step, decision, or artifact, not in understanding?
5. **Not already covered** — check `~/.claude/skills/` and `~/.agents/skills/`. If existing skill cover 70%, propose edit that skill instead.

Failing cluster have three destination. **Merge** into neighbour cluster (most common). **Demote** to `references/*.md` file inside other skill — right home for taxonomy, table, background that get consulted not executed. **Drop**, and record in `report.md` so rejection visible and reviewable.

## Sizing the set

Aim **3–8 skills per book**.

Too few (1–2) usually mean distinct job squashed together and SKILL.md try teach whole discipline in one file. Too many (9+) almost always mean topic slicing: skill description overlap, and overlap description = main cause skill never trigger, because Claude cannot tell which one consult.

Dense practitioner manual can rightly give 8. Single-idea business book give one good skill + reference file, and honest move is build exactly that.

## Naming

Name the **job**, not subject: `find-workflow-constraints`, not `theory-of-constraints`.
`review-schema-for-denormalization`, not `database-design-principles`.

Kebab-case, 2–4 word, verb-first where read natural. Avoid book coined brand in name unless term truly load-bearing and widely used — skill named after trademark trigger on trademark, which not when user need it.

## Writing the description

Description = whole trigger mechanism. Write to answer *when do I consult this?* much more than *what is this about*.

- Lead with what it enable, then list concrete trigger phrase user would really type.
- Be somewhat pushy: model under-trigger skill. "Use whenever the user is designing, reviewing, or debugging X, even if they don't mention Y."
- **Differentiate sibling explicit.** Skill from one book share vocabulary and will collide. Say what each one *not* for: "for diagnosing an existing workflow — for designing a new one, use `<sibling>`."
- No put "when to use" only in body. Belong in description; body not load until after trigger decision made.

## SKILL.md vs references

Put in `SKILL.md`: procedure, decision rule, failure table, output format. Under ~500 line.

Put in `references/`: taxonomy, long table, worked example, per-domain variant, extended background. Reference them from SKILL.md with line saying *when* read them — unreferenced file = dead weight, and reference with no trigger condition get read every time, defeat purpose.

Put in `scripts/`: anything deterministic and repetitive skill would else re-derive each run. If book give formula or fixed transform, script it once.

## Charter template

Write to `charters/<skill-name>.md`:

```markdown
# Charter: <skill-name>

**Job:** <the task, one sentence, user's voice>
**Triggers when:** <situations, concrete phrasings>
**Does NOT cover:** <adjacent jobs; name sibling skills>
**Output:** <artifact or decision the skill produces>

## Draft description
<the frontmatter description, written out>

## Procedure the skill teaches
1. <step> [ku-014, ku-031]
2. <step> [ku-007]

## Decision rules
- <heuristic with its conditions> [ku-022]

## Failure modes
| Tell | Cause | Fix | KU |
|---|---|---|---|

## Bundled resources
- references/<file>.md — <what, and when the skill should read it> [ku-…]
- scripts/<file>.py — <what it does deterministically>

## Source KUs
ku-007, ku-014, ku-022, ku-031  (pages 44–91, 158)

## Beyond the book
<anything you are adding that the book does not support — kept explicit so it can be cut>

## Eval stance
<checkable outputs → propose evals; judgment-shaped → qualitative iteration, and say why>
```

`Beyond the book` section exist because temptation to helpfully fill half-covered topic is strong and invisible in final skill. Keep addition in labelled box let user decide: book doctrine or your synthesis.

## Handing off to skill-creator

Build one charter at a time. Invoke `skill-creator` and give up front:

- charter file path + contents (this answer its intent interview — say so, so it no re-ask user what charter already settle),
- target directory `~/.agents/skills/<name>/`,
- eval stance from charter, with reasoning, so it no manufacture assertion for judgment-shaped skill,
- sibling skill name from this book, so its description work draw boundary against them not overlap.

After last sibling built, run skill-creator description optimizer across set. Sibling skill from one book = highest-risk case for trigger collision, and this step fix it.