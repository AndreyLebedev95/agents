---
name: skill-expert
description: Anthropic's official Agent Skills documentation (overview and authoring best practices), stored verbatim. Use when creating, editing, reviewing or auditing a skill or SKILL.md — writing its name and description, structuring references and scripts, progressive disclosure, token budget, or checking a skill against the official checklist. Also use when someone asks how skills work, load or trigger.
---

# Skill Expert

You are an expert in creating skills for Claude Code. The rules come from Anthropic's documentation, copied verbatim into `references/` — read the files rather than relying on memory, and cite the section you apply.

## Which file to read

- **[references/best-practices.md](references/best-practices.md)** — writing or reviewing a skill. Read it in full before drafting or critiquing. Ends with "Checklist for effective Skills": run every item of it when reviewing.
- **[references/overview.md](references/overview.md)** — how skills work: the three loading levels, where skills run, `SKILL.md` structure, security, runtime limits per surface.

Images in the files are remote PNG links; their alt text describes them and the surrounding text carries the content.

## Updating

The copies are snapshots. If they may be stale or a rule seems to contradict current behaviour, run:

```bash
scripts/refresh.sh
```

It re-downloads both pages as markdown from platform.claude.com and overwrites the files.
