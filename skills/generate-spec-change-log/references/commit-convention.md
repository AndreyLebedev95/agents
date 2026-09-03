# Commit convention

Read when the convention needs establishing or repairing.

## Contents
- [The shape](#the-shape)
- [Types](#types)
- [Scopes and the coverage property](#scopes-and-the-coverage-property)
- [The body: rationale, not restatement](#the-body-rationale-not-restatement)
- [The footer](#the-footer)
- [Enforcement](#enforcement)
- [Extraction commands](#extraction-commands)
- [Repairing a codebase with no convention](#repairing-a-codebase-with-no-convention)

## The shape

```
<type>(<scope>): <subject>

<body>

<footer>
```

Header required; body and footer optional but each preceded by a blank line.

Three things follow from the structure, and they are why the formality earns its cost:

- **Shorter to write and read.** `fix(ui): change the submit button to green` beats "This is a fix on the UI area to change the colour of the submit button to green."
- **Impossible to leave incomplete** in the parts that are required.
- **Machine-readable**, which is what makes a derived change log possible at all.

## Types

Keep the list small and closed. An open list destroys the filtering that justified the formality.

| Type | Meaning |
|---|---|
| feat | a new feature |
| fix | a bug fix |
| docs | documentation-only change |
| style | change not affecting meaning — whitespace, formatting, semicolons |
| refactor | a change that neither fixes a bug nor adds a feature |
| perf | a change that improves performance |
| test | adding missing tests |
| chore | build process, tooling, auxiliary libraries |

Only three of these normally reach a published change log — features, fixes, and breaking changes. The rest are extracted and held back; readers of release notes do not want the chore list. Keep them in the record anyway, because they are what makes the history queryable.

## Scopes and the coverage property

The scope names **where in the system** the change landed. It is context-specific and can denote:

| Kind | Examples |
|---|---|
| Environment | production, staging, development |
| Technology | a queue, a protocol, the build |
| Feature area | pricing, authentication, monitoring, reporting, shipping |
| Product | a product line or catalogue segment |
| Integration | a named external system |
| Business action | create, amend, revoke, dispute |

More than one scope is allowed where a change genuinely spans them.

### The property that matters

Draft the scope list with everyone who commits, operations included. Then test it:

> **Every change that could possibly be committed falls under at least one scope.**

Test it by trying to name changes that fit no scope, and adding scopes until none remain. Revisit whenever a new area of the system appears.

This is worth the effort because an uncovered change is an **invisible** change. It will be missing from every derived view and nobody will know it is missing — the log looks complete. A scope list with genuine coverage is also what makes it possible to reason about the impact of a release: "what did this release touch" becomes a query rather than an investigation.

## The body: rationale, not restatement

The body carries **why**, not what. The diff already says what.

Recording the reason at the moment of the change has two payoffs:

- Asking the history of a line answers "why is this like this" without any separate lookup or document.
- The commit's co-changed files include the tests written alongside it — a zero-cost link from a change to its test coverage, needing no index.

The second only holds if commits are scoped to **one logical change**. A commit bundling ten unrelated things makes its co-changed files meaningless as evidence of anything, and cannot carry ten rationales usefully either.

Writing the message is itself worth something before anyone reads it. It forces three questions: is this one change or several that should be split? Is it clear? Is it actually done — should tests have been added or modified alongside?

## The footer

**Breaking changes.** Declare every one in the footer, opening with the words "breaking change", followed by the explanation and the migration path. A breaking change without a migration path is incomplete; the generator flags it, but flagging is not fixing.

Note that a breaking change is orthogonal to type — a feature can be breaking. List it in both sections.

**Issue references.** Reference the tracker identifier of any related issue. This is the link that lets a change log entry point back at the request that caused it.

## Enforcement

Enforce with a hook, not by review.

Reviewers do not catch format drift reliably — it is exactly the kind of thing that gets waved through under time pressure, and the cost is paid silently much later when a derived log under-reports. A hook rejecting a malformed message costs the author fifteen seconds and is not subject to anyone's judgment on a Friday afternoon.

Collective work and peer pressure help, but they are not the mechanism.

## Extraction commands

```bash
# Subjects since the last release
git log <last-tag>..HEAD --pretty=format:%s

# Features only
git log <last-tag>..HEAD --grep '^feat' --pretty=format:%s

# Everything touching one scope
git log --grep '^[a-z]*(pricing)' --pretty=format:'%h %s'

# Adherence rate — run this before generating anything
total=$(git log <range> --oneline | wc -l)
ok=$(git log <range> --pretty=format:%s | \
     grep -cE '^(feat|fix|docs|style|refactor|perf|test|chore)(\([^)]+\))?!?: ')
echo "$ok / $total follow the convention"

# Which requirement identifiers were touched
git log <range> --pretty=format:%s%n%b | grep -oE 'REQ-[0-9]+' | sort -u

# What changed alongside a given file — the free test link
git log --format='%h %s' --name-only -- path/to/file
```

## Repairing a codebase with no convention

You cannot retrofit a convention onto history that has already happened, and attempting it produces fiction.

The workable path is marginal: **raise the standard for new work from now on.** Adopt the convention going forward, generate the log from the first release after adoption, and for the current release either generate what you can and label the gap explicitly, or write it by hand and say that is what you did.

Over time this covers the parts of the history that matter, because those are the parts being changed. Do not blend generated and hand-written material silently — a reader who cannot tell which is which will trust both equally, and be wrong about one of them.
