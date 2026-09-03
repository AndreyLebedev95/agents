# Agent Composition — turning a skill set into a subagent

Read at Phase 5, after book skills exist. Skill = capability. Agent = role holding many capabilities, know loop they run in.

## Contents
- [When an agent is warranted](#when-an-agent-is-warranted)
- [Composition patterns](#composition-patterns)
- [Anatomy of the agent file](#anatomy-of-the-agent-file)
- [Frontmatter](#frontmatter)
- [Writing the body](#writing-the-body)
- [Model and permissions](#model-and-permissions)
- [Anti-patterns](#anti-patterns)
- [Verification](#verification)

## When an agent is warranted

Make agent only when **two+ new skills fire together on recurring workflow**, and workflow have shape skills alone no encode: order, stop condition, standard of done, stance.

One skill do job? Ship skill. Agent wrapping one skill = cold start + context boundary + name to remember, for nothing.

Ask: *what this agent refuse to do?* Role you cannot draw boundary around = no role. Answer "nothing, just good at book topic"? You describing skills you already built.

Most books give **one** agent. Dense manual with truly separate practices maybe two. Book giving four agents = book whose skills sliced by topic — go back Phase 2.

## Composition patterns

**Specialist** — default. One role, 2–5 sibling skills, one loop. "Reviews workflow for constraints, produces diagnosis and change plan." Best when book teach one discipline from many angles.

**Pipeline** — agent run skills in fixed order, each stage feed next. Fit when book method truly sequential (diagnose → design → validate). State handoff artifact between stages explicit, else stages blur.

**Critic** — agent apply book standards to work someone else made; output = findings, not changes. Books heavy in `anti-pattern` KUs compose naturally into critics. Keep read-only: critic that edits lose independence that made it useful.

**Orchestrator** — hold few skills, route to others, integrate results. Build only when book method truly coordinate distinct roles; else overhead. Rare from one book.

## Anatomy of the agent file

This environment store agents one per directory, authored under `~/.agents/` and symlinked
into `~/.claude/` — same convention as skills, so source of truth live one place:

```
~/.agents/agents/<agent-name>/<agent-name>.md      <- write here
~/.claude/agents/<agent-name>                      <- symlink, made by register.py --agent
```

Never write straight into `~/.claude/agents/`. `register.py --agent` make the link, and it
skip linking for any file already outside `~/.agents/agents/`.

## Frontmatter

```yaml
---
name: workflow-constraint-analyst        # kebab-case, matches directory and filename
description: Diagnoses flow constraints in a delivery process and produces a change plan.
permissionMode: auto                     # as used by the other agents in this environment
skills:                                  # skills loaded for this agent
  - find-workflow-constraints
  - design-constraint-experiments
model: opus                              # opus | sonnet | haiku | inherit
tools: Read, Grep, Glob, Bash            # optional; omit to inherit all tools
---
```

Rules that matter:

- `name` must match directory and filename, must be unique across `~/.claude/agents/`. Spell model names exact — typo like `sonet` fail silent.
- `description` = what orchestrating model read when deciding to delegate. Write as dispatch criterion: what agent take in, what it return. This agent trigger surface, same as skill description.
- `skills` list skill names as registered in `~/.claude/skills/` (this environment symlink them from `~/.agents/skills/`). Verify each name resolve before install — misspelt entry = agent run without its knowledge.
- `tools`: narrow only when role truly read-only (critic). Else omit; over-narrow make agents that fail halfway.

## Writing the body

Body = system prompt. Carry what skills cannot: identity, loop, standard of done, boundary. Keep short — depth live in skills; duplicate here = two copies drifting.

```markdown
You are a <role>. <One or two sentences of stance — what this role cares about and what it
is skeptical of, drawn from the book's thesis.>

## Operating loop
1. <intake — what you need before starting, and what to do if it is missing>
2. <apply skill A to produce X>
3. <apply skill B to X, producing Y>
4. <check against the standard of done>

## Standard of done
- <the book's own bar for quality, made checkable>

## Boundaries
- <what you do not do; which agent or skill handles that instead>
- <what you escalate to the user rather than deciding>

## Output
<the exact shape of what you return — a report structure, a diff, a findings list>
```

Two things earn place, usually missing:

**Intake failure handling.** State what agent do when invoked without what it need. Existing `frontend-developer` agent here do this well: no plan → it stop and ask. Agent that improvise past missing input make confident work against invented requirements.

**The stance.** Book point of view = thing generic model no have. "You are skeptical of adding capacity before measuring flow" worth more than paragraph restating skills — it change agent defaults, only reason to have role.

## Model and permissions

- `opus` for judgment-heavy roles: critique, design, diagnosis, anything where book teach taste.
- `sonnet` for mechanical apply of well-specified procedure at volume.
- `inherit` when agent should track whatever parent session run.

Set `permissionMode` to match other agents here unless role need narrower. Critic that only read = good candidate for restricted `tools` list, not permission change.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| One agent per chapter | Chapters are not roles | One agent per workflow, or none |
| Agent wrapping one skill | Indirection with no gain | Ship the skill |
| Body restates the skills | Two copies that drift | Body holds loop + stance only |
| No boundary section | Agent accepts everything, does it badly | Name what it refuses |
| Skills list with unverified names | Silent knowledge loss at runtime | Check each resolves first |
| "Expert in <book title>" | Not a dispatch criterion | Describe input → output |

## Verification

Before declare agent done:

1. `python3 <skill-dir>/scripts/register.py --agent <path>` — frontmatter, name match, every listed skill resolve.
2. Dry-run on realistic task from book domain, read transcript. Check it truly consult skills; agent whose skills never load = system prompt wearing costume.
3. Confirm boundary hold — hand it something just outside remit, see if it decline or improvise.