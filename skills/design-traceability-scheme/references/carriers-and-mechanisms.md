# Carriers and accuracy mechanisms

Read when choosing where a specific link lives, or which mechanism keeps it true.

## Contents
- [The five carriers](#the-five-carriers)
- [Choosing among them](#choosing-among-them)
- [The four accuracy mechanisms](#the-four-accuracy-mechanisms)
- [The non-mechanism](#the-non-mechanism)
- [Pairing carrier with mechanism](#pairing-carrier-with-mechanism)

## The five carriers

Ranked by how well the attachment survives ordinary change.

### 1. A structured marker inside the artifact

An annotation, attribute, or decorator in the host language.

**Survives:** rename (it is attached to the element, not its name), move (it travels with the element), delete (it goes with it, leaving nothing to clean up).

**Gains:** the compiler checks it, the editor autocompletes and searches it, and it constrains nothing about how anything is named. Because it is structured, tools can parse it — which is what makes curation, consolidation, publishing and reconciliation possible at all. Free text in a comment forecloses every one of those.

**Costs:** requires modifying the artifact, which rules it out for code you cannot touch. Cannot carry nuance — fears, taste, political pressure, the texture of an argument. Those need prose somewhere else, and pretending otherwise produces a marker catalogue nobody can interpret.

**Design notes:**
- Name the marker for what the element *is*, never for the document it feeds. A marker meaning "include this in the matrix" is noise in the artifact, because an element is not intrinsically a member of a document. Name it for the property, and let membership follow from a query. The document can then change without touching a single marker.
- Document each marker at its definition: a short description plus a link to an authoritative explanation. Every element carrying it is then one hover away from the full account, and people learn the vocabulary while working rather than being sent to a separate document.
- Where several properties always travel together, define a marker that carries them all, so one declaration implies the set. The bundle must name a real concept — a convenient bag of unrelated properties teaches nothing.
- Do not couple the extraction tool to the marker definitions. Match by namespace prefix, by bare name, or by a meta-marker recognized by simple name. A tool that imports the marker types is welded to them: the markers cannot move, be renamed, or be defined per team.

### 2. A naming or structural convention

Package and folder names, prefixes and suffixes, file layout.

**Survives:** nothing automatically. One typo and the classification silently ends. The compiler does not care.

**Gains:** free, and applicable to an existing codebase without modifying a single file — which is often the only option on legacy. Does not disrupt teams that will not accept markers.

**Costs:** can categorize, but cannot carry rationale, alternatives or nuance. If you need those, this route is already exhausted.

**Design notes:**
- Enforce with static analysis, since nothing else will.
- Generate something visible from every convention you rely on, and make the generator *fail loudly* on an element matching no convention rather than skipping it. Break the convention and the document breaks — which both rewards adherence and reports the violation without anyone policing it. A generator that silently ignores what it does not recognize hides exactly the violations you built it to catch.
- Watch for noise: a convention that restates what the container already says adds no information and pushes names out of the domain language. If everything in a services package is suffixed "Service", drop the suffix.
- Record the conventions at the entry point of the repository even when everyone knows them — what each is, what it means, and the rules it implies, including the ones that must not be broken. Conventions living only in habit are invisible to newcomers, to tools, and to anyone auditing whether they still hold. Where a convention is adopted from a published standard, link to it rather than restating it.

### 3. A small purpose-built notation

A domain-specific syntax for what neither markers nor conventions can express.

**Survives:** depends entirely on what you build. Usually needs its own tooling to stay honest.

**Costs:** you now maintain a language. Justified only when the expression genuinely cannot fit in the host technology.

### 4. Sidecar files

One companion file per artifact, holding what the artifact's format cannot.

**Survives:** poorly. The pairing breaks as soon as anyone renames or moves one of the two without the other, because the file manager does not know they are related and will not stop a one-sided change.

**Use when:** there is no other option — the artifact format has nowhere to put the metadata and cannot be modified.

### 5. An external register

A database, spreadsheet, matrix file, or registry holding links to artifacts it does not live inside.

**Survives:** poorly, for the same reason as sidecar files, at larger scale. Nothing stops an artifact being renamed, moved or deleted without the register being updated.

**Use as the fallback when:** the artifacts cannot be touched at all.

**Use as the first choice when:** the metadata is maintained in bulk, across many artifacts at once, by people who are not the artifacts' owners. A quality or compliance role filling in a column across hundreds of items, using the bulk fill and interpolation a spreadsheet provides, without involving the artifact owners and without risk of corrupting the artifacts — this is a legitimate design, not a compromise. Choose it deliberately in that case, and pair it with a check for the desynchronization it invites.

## Choosing among them

Work down the list and take the first that fits:

1. Can you modify the artifact, and does the host technology have a structured marker mechanism? → **marker**
2. Can you not modify the artifact, but does a structure already encode the classification? → **convention** (and document it)
3. Is the metadata maintained in bulk by a separate role? → **external register** + a desynchronization check
4. Does the artifact format have nowhere to put it and cannot be changed? → **sidecar** or **register**, and expect the pairing to break

Then, whichever you chose, write down the rename / move / delete behaviour. That line is the useful part of the decision.

## The four accuracy mechanisms

In descending order of desirability.

### 1. Single authoritative source, read directly

The artifact is its own documentation and the audience can read it. Nothing to keep in sync, nothing to publish.

*Example:* a dependency manifest is the natural authoritative record of dependencies, and needs no derived document while only developers care.

### 2. Single sourcing with automated publishing

One authoritative home. Derived views are generated and versioned on every build, and never edited.

*This is where a traceability matrix belongs.* The links live on the artifacts; the matrix is a published snapshot of a query over them.

### 3. Redundant sources with propagation

Duplication is permitted because a reliable tool updates every copy: rename refactoring chasing every reference, include and substitution directives, a constant referenced from many sites.

Note the middle category this creates. Between fully generated documents and hand-maintained ones sit documents still updated by a person but where the tooling does the labour — a rename propagating, a deletion failing to compile. This is the cheapest option available whenever full generation is not, and it is routinely overlooked because the choice gets framed as generated-or-manual.

### 4. Redundant sources with reconciliation

Duplication that cannot be propagated is checked automatically and frequently instead. Failure of the check is the signal.

Two properties are non-negotiable:

- **It must fail from either side.** Change statement A without B and it fails; change B without A and it fails too. A check that only detects movement on one side leaves the other free to drift silently, which is the failure it was built to prevent.
- **It must actually be able to fail.** A check that hardcodes its expected value instead of reading it from the source passes regardless of whether the two sides agree. That is the worst outcome available, because it buys trust while providing no coverage. Prove it: change one side alone and confirm it goes red.

## The non-mechanism

**Human dedication.** Duplicated knowledge kept consistent by people being careful.

In practice this does not work. It is not a discipline problem to be solved with more diligence or a clearer owner — it is a design failure, and naming an owner reproduces it with a name attached.

Two corollaries worth stating plainly:

- Ownership should attach to the *mechanism* — the generator, the check, the convention and its enforcement — never to the manual updating.
- Any step consisting of copying information from one place to another will lapse, regardless of accountability, because it is a chore. Find that step and automate it or design it away.

## Pairing carrier with mechanism

| Carrier | Natural mechanism | Watch for |
|---|---|---|
| Marker in artifact | 1 or 2 — the artifact is authoritative, views are generated | Markers that go unused as elements are added; generate something that fails on unmarked elements |
| Convention | 2, with static analysis enforcing the convention | Silent typos; make the generator fail on unmatched elements |
| Purpose-built notation | 2 | Tooling burden |
| Sidecar | 4 — reconcile the pair | One-sided renames |
| External register | 4 — reconcile register against artifacts, both directions | Entries pointing at things that no longer exist, and artifacts absent from the register |
