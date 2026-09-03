#!/usr/bin/env python3
"""Validate and register skills and agents produced by the book-to-skills pipeline.

Usage:
    register.py --skill ~/.agents/skills/<name>          # validate + symlink into ~/.claude/skills
    register.py --agent ~/.agents/agents/<n>/<n>.md      # validate + symlink into ~/.claude/agents
    register.py --list                                   # show registered skills and agents
    register.py --skill <dir> --check-only               # validate without symlinking
    register.py --agent <file> --check-only              # validate without symlinking

Skills and agents are authored under ~/.agents/ and symlinked into ~/.claude/ so that
the source of truth lives in one place outside the tool's own config directory.
"""
import argparse
import re
import sys
from pathlib import Path

HOME = Path.home()
SKILLS_LINK_DIR = HOME / ".claude" / "skills"
AGENTS_DIR = HOME / ".claude" / "agents"
AGENTS_SRC_DIR = HOME / ".agents" / "agents"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VALID_MODELS = {"opus", "sonnet", "haiku", "inherit", "fable"}

errors: list = []
warnings: list = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_frontmatter(path: Path) -> dict:
    """Minimal YAML front-matter reader: scalars, quoted scalars, and '- ' lists."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        err(f"{path}: no YAML frontmatter (file must start with '---')")
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        err(f"{path}: frontmatter is not closed with '---'")
        return {}
    data, key = {}, None
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line.lstrip()[2:].strip().strip("\"'"))
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            data[key] = value.strip("\"'") if value else []
    return data


def registered_skill_names() -> set:
    names = set()
    for base in (SKILLS_LINK_DIR, HOME / ".agents" / "skills"):
        if base.is_dir():
            names |= {p.name for p in base.iterdir() if (p / "SKILL.md").is_file()}
    plugins = HOME / ".claude" / "plugins" / "marketplaces"
    if plugins.is_dir():
        names |= {p.parent.name for p in plugins.glob("*/plugins/*/skills/*/SKILL.md")}
    return names


def check_skill(path: Path, check_only: bool) -> None:
    if not path.is_dir():
        err(f"{path}: not a directory")
        return
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        err(f"{path}: missing SKILL.md")
        return

    fm = parse_frontmatter(skill_md)
    name = fm.get("name", "")
    desc = fm.get("description", "")

    if not name:
        err("frontmatter: missing `name`")
    elif not NAME_RE.match(str(name)):
        err(f"frontmatter: name '{name}' must be lowercase kebab-case")
    elif name != path.name:
        err(f"frontmatter: name '{name}' does not match directory '{path.name}'")

    if not desc:
        err("frontmatter: missing `description` — the skill will never trigger")
    else:
        if len(desc) < 60:
            warn(f"description is only {len(desc)} chars; add concrete trigger phrases")
        if len(desc) > 1400:
            warn(f"description is {len(desc)} chars; long descriptions dilute triggering")

    body_lines = skill_md.read_text(encoding="utf-8", errors="replace").split("---", 2)[-1].splitlines()
    if len(body_lines) > 500:
        warn(f"SKILL.md body is {len(body_lines)} lines (>500); move detail into references/")
    if len(" ".join(body_lines).split()) < 60:
        err("SKILL.md body is essentially empty")

    body = "\n".join(body_lines)
    for ref in (path / "references").glob("*.md") if (path / "references").is_dir() else []:
        if ref.name not in body:
            warn(f"references/{ref.name} is never mentioned in SKILL.md — it will never be read")
    for scr in (path / "scripts").glob("*.py") if (path / "scripts").is_dir() else []:
        if scr.name not in body:
            warn(f"scripts/{scr.name} is never mentioned in SKILL.md")

    if errors or check_only:
        return

    SKILLS_LINK_DIR.mkdir(parents=True, exist_ok=True)
    link = SKILLS_LINK_DIR / path.name
    if link.is_symlink() or link.exists():
        if link.is_symlink() and link.resolve() == path.resolve():
            print(f"already registered: {link} -> {path}")
            return
        err(f"{link} already exists and points elsewhere; resolve manually")
        return
    link.symlink_to(path)
    print(f"registered skill: {link} -> {path}")


def check_agent(path: Path, check_only: bool = False) -> None:
    if not path.is_file():
        err(f"{path}: not a file")
        return
    fm = parse_frontmatter(path)
    name = fm.get("name", "")

    if not name:
        err("frontmatter: missing `name`")
    elif not NAME_RE.match(str(name)):
        err(f"frontmatter: name '{name}' must be lowercase kebab-case")
    else:
        if path.stem != name:
            err(f"frontmatter: name '{name}' does not match filename '{path.stem}'")
        if path.parent.name != name and path.parent != AGENTS_DIR:
            warn(f"directory '{path.parent.name}' does not match agent name '{name}'")

    if not fm.get("description"):
        err("frontmatter: missing `description` — nothing can decide to delegate to this agent")

    model = fm.get("model")
    if isinstance(model, str) and model and model not in VALID_MODELS:
        err(f"frontmatter: model '{model}' is not one of {sorted(VALID_MODELS)}")

    skills = fm.get("skills") or []
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
    known = registered_skill_names()
    for s in skills:
        if s not in known:
            err(f"skills: '{s}' does not resolve to an installed skill")
    if skills:
        print(f"skills referenced: {', '.join(skills)}")

    body = path.read_text(encoding="utf-8", errors="replace").split("---", 2)[-1]
    if len(body.split()) < 25:
        err("agent body is essentially empty — no role, loop, or boundary")
    if not errors:
        print(f"agent OK: {path}")

    if errors or check_only:
        return

    # Symlink into ~/.claude/agents, mirroring how skills are registered. Agents
    # authored directly under ~/.claude/agents need no link and are left alone.
    try:
        path.parent.relative_to(AGENTS_SRC_DIR)
    except ValueError:
        return
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    link = AGENTS_DIR / path.parent.name
    if link.is_symlink() or link.exists():
        if link.is_symlink() and link.resolve() == path.parent.resolve():
            print(f"already registered: {link} -> {path.parent}")
            return
        err(f"{link} already exists and points elsewhere; resolve manually")
        return
    link.symlink_to(path.parent)
    print(f"registered agent: {link} -> {path.parent}")


def do_list() -> None:
    print("== skills ==")
    if SKILLS_LINK_DIR.is_dir():
        for p in sorted(SKILLS_LINK_DIR.iterdir()):
            if (p / "SKILL.md").is_file():
                target = f" -> {p.resolve()}" if p.is_symlink() else ""
                print(f"  {p.name}{target}")
    print("== agents ==")
    if AGENTS_DIR.is_dir():
        # iterdir + explicit glob, because rglob does not descend into symlinked
        # directories and agents are symlinked in from ~/.agents/agents
        for p in sorted(AGENTS_DIR.iterdir()):
            if not p.is_dir():
                continue
            for md in sorted(p.glob("*.md")):
                target = f" -> {md.resolve()}" if p.is_symlink() else f" ({md})"
                print(f"  {md.stem}{target}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", help="path to a skill directory")
    ap.add_argument("--agent", help="path to an agent .md file")
    ap.add_argument("--check-only", action="store_true", help="validate without symlinking")
    ap.add_argument("--list", action="store_true", dest="do_list")
    args = ap.parse_args()

    if args.do_list:
        do_list()
        return
    if args.skill:
        check_skill(Path(args.skill).expanduser().resolve(), args.check_only)
    elif args.agent:
        check_agent(Path(args.agent).expanduser().resolve(), args.check_only)
    else:
        ap.error("one of --skill, --agent, or --list is required")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        sys.exit(1)
    print("validation passed" if not warnings else "validation passed with warnings")


if __name__ == "__main__":
    main()
