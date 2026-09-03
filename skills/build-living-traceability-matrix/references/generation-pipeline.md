# The generation pipeline

Read when adapting the scanner, or when a single full scan stops being practical.

## Contents
- [The four steps in detail](#the-four-steps-in-detail)
- [Consolidation as a keyed scan](#consolidation-as-a-keyed-scan)
- [Handling elements without the key](#handling-elements-without-the-key)
- [Decoupling the extractor](#decoupling-the-extractor)
- [Scale: when to go incremental](#scale-when-to-go-incremental)
- [The derived store rule](#the-derived-store-rule)
- [Tooling notes](#tooling-notes)

## The four steps in detail

### Select

Two decisions: the **perimeter** and the **key**.

The perimeter is the set of artifacts scanned. State what is outside it as explicitly as what is inside — a matrix that silently omits a whole module is worse than one that says it does not cover it.

The key is the property the dispersed facts share, and it is what makes consolidation possible at all. Usually the requirement identifier.

Express the selection as a criterion, never a list. The five stable criteria:

| Criterion | Example | Survives |
|---|---|---|
| Folder or module | everything under the claims module | file renames |
| Naming convention | every test whose name contains "Acceptance" | moves |
| Marker or tag | every element carrying the requirement marker | renames and moves |
| Registry entry | whatever the registry resolves this alias to | target relocation |
| Tool output | every file the compiler processed, from its log | most things |

A list of paths is none of these. It is copy-and-paste, it goes stale, and it depends on someone remembering to update it.

### Filter

Drop what does not serve this view's single objective.

Set the default to exclude everything not clearly relevant, accept that the default is wrong in some cases, and provide an explicit marker to override it in either direction. Encoding every case into the filter rule produces something unmaintainable; default-plus-exceptions stays legible.

The default has to be tuned to the codebase. Constants used to hide technical literals should mostly be hidden; constants used in a public interface may be exactly what the view is about. The same construct, opposite treatment.

### Project

From each surviving item, take only the fields this view uses.

The temptation is to include everything already extracted since it costs nothing to carry. Resist it — the projection step is where a matrix becomes readable or not.

### Convert

Map the items and their relationships into the output.

Where rendering is complex, chain intermediate models rather than doing it in one pass: extract → normalized model → presentation model → output. Each stage stays testable.

## Consolidation as a keyed scan

The algorithm, in full:

```
dictionary = {}
for element in perimeter:
    keys = extract_keys(element)
    if keys:
        for key in keys:
            dictionary[key].add(fact_about(element))
    elif suppressed(element):
        record_suppressed(element)
    else:
        record_unmatched(element)
```

That is the whole of it. The scattered facts remain authoritative; the dictionary is a derived publication with no authority of its own.

Narrow the scan to the subset that serves the need. Reconstituting every relationship in a codebase and then filtering the render is slower and produces worse output than scanning narrowly in the first place.

## Handling elements without the key

This is where most generators go wrong, and the failure is silent.

An element inside the perimeter carrying no key is invisible to the aggregate. There are exactly two honest treatments:

1. **Explicitly suppressed** — the element carries a marker saying it is deliberately out of scope. Count it, and report the count.
2. **Unmatched** — report it by name in its own section.

There is no third option. A generator that skips unrecognized elements produces a matrix that looks complete and is not, which is worse than no matrix because it buys trust.

This is also why **detection beats declaration** as a design stance. Where the routes by which a link can be created are few enough to enumerate, detect them all and include everything found by default, requiring an explicit marker to suppress an entry. Declaration-only coverage puts the burden on memory; detect-and-silence puts it on the tool and makes every exclusion visible and reviewable.

## Decoupling the extractor

Match markers structurally, never by importing their definitions:

- by namespace or package prefix
- by unqualified name
- by a meta-marker, itself matched by simple name

A generator holding a compile-time reference to the marker library is welded to it: the markers cannot move, be renamed, or be defined per team without breaking the tool. The bundled scanner matches by regex over several plausible syntaxes for exactly this reason.

## Scale: when to go incremental

**Default to a full scan during the build.** For most systems, walking every element in sequence in a batch is entirely practical and produces a report ready for publication.

Go incremental only when the estate is genuinely too large for a sequential scan. Then each part's build pushes a partial contribution into a shared consolidation state.

Three consequences, all of which must be accepted deliberately:

- The shared state is **derived information and less trusted than any individual contribution**. When the aggregate disagrees with a contribution, trust the contribution.
- When it looks wrong, **drop it and let it regrow** from the contributions. There is no repair procedure.
- It introduces a staleness window — the aggregate reflects whenever each part last built, not now.

One warning worth heeding: if you find yourself loading a syntax tree into a graph database to run complex queries, you have become a vendor of documentation tools. That is a different job than the one you started.

## The derived store rule

Derived knowledge is never a source of truth. If it is cached for performance:

- it must be droppable at any moment
- it must be rebuildable from scratch from the authoritative sources
- it must never be edited
- keep a one-command rebuild path, and exercise it, because a rebuild path that has never been run does not work

## Tooling notes

**Parsers.** Some give you only the structural model; some also give you the comments. If the view needs prose attached to elements, you need the latter. Check before committing to a parser.

**Rendering.** Layout complexity varies enormously, roughly in this order: tables; markers pinned on a fixed background; templates evaluated with extracted content; simple one-dimensional flows; pipelines and sequences; trees; containment with automatic layout; rich layout with both containment and direction. Pick the simplest that carries the message.

**Attractiveness.** Generated output is rarely beautiful. If the artifact's job is to persuade or to sell, generation is the wrong choice and it deserves a designer. If its job is to be true, generation is the only choice.

**Build integration.** Keep the generator in the repository beside what it reads. Run it on every build, or on a one-click on-demand build. A generator living on someone's laptop is not part of the mechanism.
