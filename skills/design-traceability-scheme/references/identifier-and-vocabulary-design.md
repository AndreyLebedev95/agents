# Identifier and vocabulary design

Read when designing the identifier scheme, the tag vocabulary, or the commit convention.

## Contents
- [Identifier properties](#identifier-properties)
- [The name volatility ordering](#the-name-volatility-ordering)
- [Constants versus contract literals](#constants-versus-contract-literals)
- [Tag vocabulary](#tag-vocabulary)
- [Commit type and scope vocabulary](#commit-type-and-scope-vocabulary)

## Identifier properties

Every link in the chain is built on the identifier, so its properties bound what the chain can do.

**Searchable.** Names are often the only surviving record of what the original authors knew, and their value depends entirely on being findable. An identifier that cannot be located by a plain text search cannot be traced — the reverse query is the whole mechanism.

Test the scheme before adopting it, not after: search a sample identifier across the codebase and the wider corpus. Reject any scheme producing large numbers of false hits. Prefer forms distinctive enough that a plain search finds all and only their occurrences.

**Stable.** See the ordering below. Anchor identifiers at the stable end.

**Single-purpose.** An identifier that also encodes status, ownership or priority will change when any of those change, and every reference to it breaks. Encode one thing.

## The name volatility ordering

Different classes of name decay at very different rates. This ordering is worth internalizing because it decides where a scheme can be anchored.

| Class | Typical lifetime | Examples |
|---|---|---|
| Business domain vocabulary | Decades | selling, purchasing, settlement, claim adjustment |
| Structural / functional names | Years | the business process, the capability |
| Application and system names | Years, but they get decommissioned | |
| Organizational, legal, marketing names | One to three years | company names, subsidiaries, brands, trademarks, department names |
| Project code names | Shortest of all | chosen by fashion, replaced by fashion |

Open an old book about your trade and most of the vocabulary still means what it meant. Compare an organization chart against one from three years ago and very little survives — often through reorganizations that changed the names without changing the underlying work at all.

Two consequences:

- **Never let a volatile name appear in more than one place.** One occurrence is a rename; many occurrences is a project.
- **Prefer descriptive over evocative** for anything long-lived. An arbitrary evocative name gets replaced when the fashion turns; a dull descriptive name outlasts it and describes itself into the bargain, so the name is itself a piece of documentation.

The same ordering picks the organizing axis for a document set: a business process outlasts an application, which outlasts a project.

## Constants versus contract literals

Two rules that look contradictory and are not. The difference is who depends on the name.

**Internal cross-references → declare once, reference the declaration.** When the same identifier is written into several markers, a rename means finding every mention. Declaring it once as a constant and referring to that everywhere makes renames free and typos impossible. Pair each constant with its display name so the human-readable form also lives in one place.

**Published contracts → restate as literals, out of refactoring's reach.** Identifiers that outside parties depend on cannot be renamed freely once published. Protect them with a check that restates the contract as literal values, as an outside consumer would see them, deliberately positioned so that automated refactoring will *not* update it.

Then any rename breaks the check instead of breaking a consumer. This is defensive documentation: it stops the change and teaches the person making it, at the moment they make it, why that name is fixed. Someone newly joined who renames a contractual constant is halted by a failing check and learns the constraint on the spot.

Implementation notes:
- Verify both directions — the literal must be accepted as input and produced as output.
- Use parameterized checks rather than a loop, so a failure names the offending value.
- Make the failure message explain that the name is contractual, not accidental. The message is the documentation.

This is the one place where duplication is correct and refactoring assistance is unwanted.

## Tag vocabulary

Tags on specification items carry three kinds of knowledge with three different lifetimes. Keeping them distinct is what stops a tag set decaying into near-synonyms.

| Family | Purpose | Lifetime |
|---|---|---|
| Process | in progress, owner, iteration, goal of the current work | Temporary — deleted when the work completes |
| Curation | acceptance criterion, nominal case, variant, negative, exception, core | Stable, intrinsic to the item |
| Domain | the business area the item belongs to | Stable, intrinsic to the item |

**Tags are documentation and must themselves be documented.** Keep a file listing every valid tag with a text description, collocated with the items it tags. Then add an automated check that fails when a tag appears in use but is not declared, and flags tags declared but no longer used. Without it the vocabulary drifts and every query over it quietly under-reports.

**Delete process tags when their work completes** rather than letting them accumulate. A stale "in progress" tag is worse than no tag, because it is read as current.

**Pick one polarity per marker and record the decision.** For any property you can mark the case that holds it or the case that violates it, but not both. Letting individuals choose produces a codebase where the *absence* of a marker means nothing, which destroys the marker's value entirely. Two viable strategies:

- Mark the desired case everywhere, and let absence imply the opposite. Use when you want to drive adoption.
- Make the desired case the default, declared once at the module, and mark only deviations. Use when markers are considered noise — the deviation then reads as conspicuous, which is usually what you want.

**Declare module-wide properties once, at the module.** Properties holding uniformly across every member belong on the grouping, creating an "unless stated otherwise" default that members inherit. Note that groupings are more numerous than the obvious ones: a package's direct members versus everything beneath it, a type over its members, source folders, subprojects, the closure of a type's subtypes, and the set of everything carrying a given marker.

**Serve every audience from one tagged corpus.** One well-tagged body of items yields a different report per audience without maintaining separate documents — each audience is a query over the tags. Building one document per audience by hand produces documents that immediately disagree with each other.

## Commit type and scope vocabulary

### Shape

```
<type>(<scope>): <subject>

<body>

<footer>
```

The header is required. The body carries the rationale — not a restatement of the diff. The footer carries breaking changes and issue references.

Structuring it this way makes messages shorter to write, impossible to leave incomplete in the required parts, and machine-readable. `fix(ui): change the submit button to green` is shorter to write and to read than the equivalent English sentence, and a tool can filter on it.

### Types

Keep the list small and closed. An open list destroys the filtering that justified the formality in the first place.

| Type | Meaning |
|---|---|
| feat | a new feature |
| fix | a bug fix |
| docs | documentation-only change |
| style | change not affecting meaning — whitespace, formatting |
| refactor | a change that neither fixes a bug nor adds a feature |
| perf | a change that improves performance |
| test | adding missing tests |
| chore | build process, tooling, auxiliary libraries |

### Scopes

The scope names *where in the system* the change landed. It is context-specific and can denote:

- **Environment** — production, staging, development
- **Technology** — a queue, a protocol, the build
- **Feature area** — pricing, authentication, monitoring, reporting, shipping
- **Product** — a product line or catalogue segment
- **Integration** — a named external system
- **Business action** — create, amend, revoke, dispute

More than one scope is allowed where a change genuinely spans them.

**The coverage property.** Draft the scope list with everyone who commits, operations included, and then test it: try to name changes that fall under no scope, and add scopes until none remain. Every change that could possibly be committed must fall under at least one scope.

This matters because an uncovered change is an *invisible* change — it will be missing from every derived view and nobody will know. A scope list with genuine coverage is what makes it possible to reason about the impact of a release. Revisit the list whenever a new area of the system appears.

### Footer

- Declare every breaking change in the footer, opening with the words "breaking change", followed by the explanation and the migration path.
- Reference the tracker identifier of any related issue.

### Enforcement

Enforce the shape with a hook rather than by review. Everything derived from the convention silently under-reports whatever was committed off-convention, and reviewers do not catch format drift reliably.

### Why the rationale goes in the body

Recording the reason at the moment of the change means the history of a line answers "why is this like this" without any separate lookup. It also gives a second link for free: the commit's co-changed files include the tests written or modified alongside the change, which is a zero-cost connection between a change and its test coverage, needing no index at all.

That only holds if commits are scoped to one logical change. A commit bundling ten unrelated things makes its co-changed files meaningless as evidence of anything.
