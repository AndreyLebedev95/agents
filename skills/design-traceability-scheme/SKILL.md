---
name: design-traceability-scheme
description: Designs where each link of a traceability chain lives and what keeps it accurate — the carrier for each link, the mechanism that keeps it true, and what happens to it under rename, move and delete. Covers the four accuracy mechanisms ranked by desirability, the five places metadata can attach ranked by how well each survives refactoring, the intrinsic-versus-extrinsic test that decides placement, identifier stability and searchability, the direction references must run, and tag and commit-scope vocabularies with coverage as their test. Use whenever someone is setting up requirements traceability or a REQ-ID scheme, deciding what should carry a requirement identifier, choosing between annotations, naming conventions, sidecar files and an external register or spreadsheet, designing commit conventions meant to be queried later, or asking why a previous traceability effort went stale — even if they only say "we need to link requirements to tests" or "how do we keep this matrix from rotting". For generating the matrix itself use build-living-traceability-matrix; for finding what has become orphaned use check-traceability-integrity; for recording and justifying a single decision use record-architecture-decisions.
---

# Designing a traceability scheme

A traceability chain is a set of claims that the same fact is stated in two places — that this requirement is the one this component implements, that this test exercises that requirement, that this commit served it. Every one of those claims is duplicated knowledge, and duplicated knowledge diverges unless something forces it not to.

So the design work is not drawing the chain. It is answering, link by link, two questions: **what carries this link**, and **what makes it fail loudly when it stops being true**. A scheme that cannot answer the second question for a link does not have that link. It has a hope.

## The output

A scheme document, one row per link:

```
## <link>  (e.g. REQ-ID → component)
Carrier:        <where the link physically lives>
Mechanism:      <what keeps it accurate — generation, propagation, or a check>
On rename:      <what happens to the link>
On move:        <what happens to the link>
On delete:      <what happens to the link>
Blind spot:     <what this link cannot see>
```

Plus the vocabularies — identifiers, tags, commit types and scopes — written where the people who commit will see them.

## Before designing anything: what actually needs tracing

Tracing costs something on every change forever, so it needs justifying per fact rather than as a policy. A fact earns a place in the chain if it is of interest over a long period, **or** matters to many people, **or** is critical if lost. If none of the three holds, leaving it out is the right answer, not a gap.

Then classify what survives by **rate of change**, because volatility decides which mechanisms are even available:

| Changes | Viable approach |
|---|---|
| Almost never | Write it once by hand; duplication is tolerable because nothing will need updating |
| With each release | Hand-maintained but tool-assisted — renames propagate, deletions fail to compile |
| Continuously | Must be derived from the artifacts, or reconciled by an automated check |

The most common design error is picking a mechanism suited to a slower rate of change than the fact actually has. A matrix maintained by hand is a perfectly good answer for knowledge that changes twice a year and a guaranteed failure for knowledge that changes twice a week.

Most of what you need already exists somewhere — in the code, the tests, the configuration, the version history, the tracker. Before designing a place to record something, find where it is already recorded and what is actually wrong with it. Usually it is one of these, and each has a different remedy:

- **Inaccessible** — present but unreadable by the audience → build extraction and publication
- **Too abundant** — buried in volume → build curation and filtering
- **Fragmented** — one concept spread across many places → build consolidation
- **Implicit** — all but the marker that names it → add the marker
- **Unrecoverable** — obfuscated past reading → reverse-engineer or rewrite
- **Unwritten** — only in people's heads → hold the conversation and capture it

Diagnose before building. Extraction machinery pointed at an unwritten fact produces an empty report.

## Step 1 — Decide placement with the intrinsic/extrinsic test

For each link, ask whether the fact is *intrinsic* to the element — part of what it is — or *extrinsic*, describing a relationship between it and something else.

Two questions settle it:

- If this element were deleted, should the fact vanish with it, needing no edit anywhere? → intrinsic
- Could the fact change while the element itself is unchanged? → extrinsic

Attach intrinsic facts to the element. Hold extrinsic facts in whatever owns the relationship. This is not fussiness: extrinsic knowledge attached to an element makes that element churn for reasons that have nothing to do with it, and that churn is the largest hidden maintenance cost in any traceability scheme.

Worked through the usual chain:

- **"This component implements REQ-42"** — intrinsic. It is part of what the component is for. Put it on the component.
- **"This test exercises REQ-42"** — intrinsic to the test. Put it on the test.
- **"REQ-42 is covered by three tests"** — extrinsic to every one of them. Do not store it. Derive it by querying for the marker.
- **"REQ-42 is currently at 60% complete"** — extrinsic to everything, and volatile. It belongs on a status overlay, never on the requirement or the matrix.

When a decision genuinely needs an extrinsic fact, there is a move that keeps the placement clean: mark each element with an *intrinsic* attribute, and make the selection separately, through that attribute. Marking one implementation as "the default" forces a foreign choice onto it; marking each with the technology it actually uses is intrinsic, and the selection happens elsewhere.

The governing question, when a case is unclear: *how would this declared knowledge have to change when I change the element?* The right placement is the one that requires the least work then.

## Step 2 — Choose the carrier

Five places metadata can attach, ranked by how well the attachment survives ordinary change. Read `references/carriers-and-mechanisms.md` when weighing a specific choice; the summary:

1. **A structured marker in the artifact itself** — annotation, attribute, decorator. Best: it survives renames, moves with the element, is deleted with it, is checkable by the toolchain and searchable by the editor, and constrains nothing about naming.
2. **A naming or structural convention** — free, works on code you cannot modify, but one typo silently ends the classification and no compiler cares.
3. **A small purpose-built notation** — when neither of the above can express what you need.
4. **A sidecar file per artifact** — breaks the moment anyone renames or moves one of the pair without the other, because nothing knows the two are related.
5. **An external register** — a database, a spreadsheet, a matrix file. Furthest from what it describes and most easily desynchronized.

Whatever you choose, write down what happens on rename, move and delete. A scheme that has never been asked that question will answer it in production.

**The external register is not always the fallback.** It is the correct first choice when the links are maintained in bulk across many artifacts by people who are not the artifacts' owners — a compliance or quality role filling in a column across two hundred items, using the fill and interpolation a spreadsheet gives them, without involving developers and without risk of corrupting the artifacts. That is a real and common situation, and choosing the register for it deliberately is better than choosing it apologetically. Just accept the consequence: nothing stops someone renaming, moving or deleting an artifact without touching the register, so this choice obliges you to add the check that detects exactly that.

Prefer, in general, the encoding your toolchain validates. What the toolchain enforces cannot be wrong — if it were, the build would fail. What is merely named can drift. Free text can say anything, and does. Push each fact as far up that ordering as the technology allows, and reserve prose for what neither can carry: rationale, rejected alternatives, nuance.

## Step 3 — Choose the accuracy mechanism

Four arrangements, in descending order of desirability, and one that is not a mechanism at all:

1. **Single authoritative source, read directly.** The artifact is its own documentation. Nothing to keep in sync. Available whenever the audience can read the artifact.
2. **Single source with automated publishing.** One authoritative home; every derived view generated and versioned on each build. This is where a traceability matrix belongs.
3. **Redundant sources with propagation.** Duplication permitted because a reliable tool updates every copy — rename refactoring, include directives, a constant referenced from many places.
4. **Redundant sources with reconciliation.** Duplication that cannot be propagated is instead checked automatically and frequently. Failure of the check is the signal. This is the fallback when two artifacts must independently state the same thing.

And the one to refuse:

> **Human dedication.** Knowledge duplicated in several places, kept consistent by people being careful.

This does not work, and it is worth being precise about why, because the usual response to a rotting matrix is to assign someone to own it. That is the same anti-pattern with a name attached. It is not a discipline failure to be corrected with more diligence or clearer accountability — it is a design failure, and adding an owner changes nothing about the design. What an owner should own is the **mechanism**: the generator, the check, the convention and its enforcement. Never the manual updating.

There is a related trap in the same family. Any step that consists of copying information from one place to another will quietly stop being done, no matter who is accountable for it, because it is a chore and chores lapse. Treat sustainability as a design constraint: find the step people will stop doing, and automate it or design it away rather than exhorting anyone.

## Step 4 — Fix the direction of the references

References are dependencies and obey the same rule: **point from the more volatile thing to the more stable thing.** A reference from a stable document into a volatile one breaks every time the volatile end moves — and it breaks the document people trusted most.

Across a project that gives a specific direction:

```
artifacts (code, tests, config)  →  requirements & constraints  →  goals  →  vision
```

Never the reverse. There is a reason requirements sit on the stable side: a decision you cannot change is, from where you stand, a requirement; one you can change is your design. Requirements are therefore structurally more stable than the designs that satisfy them, which is what makes them the right thing to anchor a chain on.

The practical consequence is the one most schemes get backwards: **do not put component or test names into requirement documents.** Have the artifacts declare which requirement they serve, and recover the reverse direction — "what implements REQ-42" — by querying for the marker. Structured markers make that query free; that reverse traversal is what makes traceability and impact analysis possible at all, and it needs no parallel index to maintain.

## Step 5 — Design the identifier

The identifier is the thing every link is built on, so its properties decide what the chain can do.

- **Searchable.** A name that cannot be found by a plain text search cannot be traced. Test the scheme before adopting it: search a sample identifier across the codebase and see whether you get all and only its occurrences. Reject schemes that produce large numbers of false hits.
- **Drawn from the stable end of the naming spectrum.** Name volatility has a known ordering. Business domain vocabulary lasts decades. Organizational, legal and marketing names — company names, brands, department names, project code names — change every one to three years, often through reorganizations that leave the actual work untouched. Arbitrary evocative names are the most volatile of all, because they are chosen by fashion. Dull descriptive names outlast them and describe themselves into the bargain.
- **Referenced as a constant internally.** Where the same identifier appears in several markers, declare it once and refer to that declaration, so a rename costs nothing and typos are impossible.
- **Restated as a literal where it forms a contract.** This is the deliberate exception. Identifiers that outside parties depend on cannot be renamed freely once published. Protect them with a check that restates them as literal values, positioned so that automated refactoring will *not* update it. Then a rename breaks the check instead of breaking a consumer, and the person making the change learns at that moment why the name is fixed. This is the one place where duplication is correct and refactoring assistance is unwanted.

## Step 6 — Design the vocabularies

**Tags.** Tags attached to specification items carry three kinds of knowledge with different lifetimes, and mixing them is why tag sets decay:

- *Process* tags — in progress, owner, iteration. Temporary. Deleted when the work completes.
- *Curation* tags — acceptance criterion, nominal case, variant, negative, exception, core. Express importance.
- *Domain* tags — the business area the item belongs to.

Tags are documentation and must themselves be documented: keep a file listing every valid tag with its description, collocated with what it tags. Then add a check that fails when a tag appears in use but not in that list, and flags tags declared but no longer used. Without that, the vocabulary drifts into a set of near-synonyms nobody can query reliably.

Pick one polarity per marker and record the decision. You can mark the case that holds a property or the case that violates it, but not both — letting people choose means the absence of a marker means nothing, which destroys the marker entirely. Either mark the desired case everywhere and let absence imply the opposite, or make the desired case the default and mark only deviations so they stand out.

Where a property holds uniformly across every member of a module, declare it once at the module and treat individual markers as exceptions to that default.

**Commit messages.** Structure them so they can be queried later:

```
<type>(<scope>): <subject>

<body — the rationale, not a restatement of the diff>

<footer — breaking changes, issue references>
```

Keep the type list small and closed: a feature, a fix, documentation-only, formatting-only, a refactoring that neither fixes nor adds, a performance change, adding missing tests, build and tooling chores. An open list destroys the filtering that justified the formality.

The scope names where in the system the change landed, and it can denote an environment, a technology, a feature area, a product, an integration, or a business action. **The scope list has one property to maintain: every change that could possibly be committed falls under at least one scope.** Test it by trying to name changes that fit no scope, and adding scopes until none remain. An uncovered change is an invisible change — and a scope list with that coverage is what makes it possible to reason about what a release actually touched.

Enforce the shape with a hook rather than by review. The convention only pays off if it is actually followed; everything derived from it silently under-reports whatever was committed off-convention.

Put the rationale in the commit body at the moment of the change. Then asking the history of a line answers "why is this like this" without a separate lookup — and the commit's co-changed files include the tests written alongside it, which is a zero-cost link from a change to its test coverage that needs no index at all. This only works if commits are scoped to one logical change; a commit bundling ten things makes its co-changed files meaningless as evidence.

## Step 7 — Prefer detection to declaration

A chain that only records what somebody remembered to declare will miss things, and will miss them silently. Wherever the ways a link can be created are few enough to enumerate, **detect all of them and include them by default, requiring an explicit marker to suppress an entry.** Declaration-only coverage puts the burden on memory; detect-and-silence puts it on the tool, and makes every exclusion visible and reviewable.

The same logic applies to what the tooling does with things it does not recognize. A generator that silently skips unmatched elements hides exactly the violations it exists to catch. Make it report them.

And prefer declaring intent over enumerating consequences. Marking elements with the role they play lets a checker derive the permitted and forbidden relationships; enumerating each pairwise restriction is tedious, impossible at fine grain, and describes only the *consequence* of the design rather than the design — so it goes stale silently as elements are added.

## Step 8 — Write down what the scheme cannot see

Publish the blind spots with the scheme, before anyone reads a report produced from it, because absence will otherwise be read as evidence. Three recur:

- **Uncovered mechanisms.** Links created by a route the extraction does not scan are simply missing.
- **Shared-state coupling.** A relationship neither side declares — another system reading or writing your database directly — is effectively undetectable from the artifacts and surfaces only in conversation.
- **Declared versus exercised.** The scheme shows the links that exist in the artifacts, not which are actually exercised in production. These are different claims and should never be presented as one.

## When not to build this

Do not build the mechanism while the shape of the knowledge is still moving; it will be rewritten faster than it pays back. Automation is justified by repetition and by making change safer — if maintaining it is becoming the drag, the right move is to remove some of it. Wait until you can see the repetition, then decide explicitly which parts stay manual rather than letting that be an omission.

## Reference material

- `references/carriers-and-mechanisms.md` — the five carriers and four accuracy mechanisms in full, with trade-offs and failure behaviour. Read when choosing where a specific link lives or which mechanism a link gets.
- `references/identifier-and-vocabulary-design.md` — identifier stability and searchability, the name volatility ordering, constants versus contract literals, tag families and lifetimes, and commit type and scope vocabularies with the coverage test. Read when designing the identifier scheme or either vocabulary.
