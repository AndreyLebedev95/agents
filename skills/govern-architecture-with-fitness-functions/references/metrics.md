# Metrics reference

Read when choosing what to measure, or when interpreting a score. Every metric here needs interpretation; none is a verdict.

## Contents
- [Cyclomatic complexity](#cyclomatic-complexity)
- [Lack of cohesion in methods](#lack-of-cohesion-in-methods)
- [Afferent and efferent coupling](#afferent-and-efferent-coupling)
- [Abstractness, instability, distance](#abstractness-instability-distance)
- [Process metrics](#process-metrics)
- [The general limitation](#the-general-limitation)

## Cyclomatic complexity

Measures complexity at function, class or application level by applying graph theory to decision points.

```
CC = E − N + 2P
```

E is edges (possible decisions), N is nodes (lines of code), P is connected components (fan-out calls to other methods). For a single function with no fan-out, P is 1, giving the simpler `CC = E − N + 2`. A function with no conditionals scores 1; one conditional gives 2, because there are two possible execution paths.

**Thresholds.** The industry generally treats under 10 as acceptable. That is very high. Prefer under 5, which indicates cohesive, well-factored code. One combined metric holds that past CC 50, no amount of test coverage rescues the code.

For calibration on how bad it gets: a single commercial C function of over 4,000 lines, with liberal use of GOTO to escape deeply nested loops, scored over 800.

**Reading a high score.** Ask three questions in order:

1. Is the function complex because the *problem domain* is complex? An algorithmically complex problem yields complex functions, and that is essential complexity.
2. Is it complex because of *poor coding*? That is accidental complexity.
3. Is the code *partitioned poorly*? Could one large method be broken into smaller logical chunks, distributing the work and the complexity into well-factored methods?

Only the second and third are defects.

**Two things worth knowing.** Test-driven development lowers average CC as a side effect, because writing the smallest code to pass a small test produces small, cohesive methods. And CC is especially worth running against generatively-produced code, which tends toward brute-force solutions and therefore accidental complexity.

## Lack of cohesion in methods

Read it as: *the sum of sets of methods not shared via shared fields.*

A class whose methods split cleanly into groups, each touching a different private field, scores high — meaning those groups are only incidentally coupled and could be separate classes with no behavioral change.

**Use it** before a restructuring, a migration, or a technical-debt assessment. High-scoring classes are candidates that were never one class. Shared utility classes are the classic offender and the classic headache during architecture migrations.

**Limit.** It detects only *structural* lack of cohesion. It cannot tell whether pieces belong together logically, so a high score is a question, not a verdict. Confirm by checking whether each field/method group could stand alone without affecting behavior.

## Afferent and efferent coupling

- **Afferent (Ca)** — incoming connections to a code artifact. Also called fan-in.
- **Efferent (Ce)** — outgoing connections to other artifacts. Also called fan-out.

Because calls and returns form a graph, both are computable by tooling on virtually every platform, which makes coupling far more precise than cohesion.

The names are notoriously confusable, differing only in the vowels that sound most alike. Two mnemonics: *a* comes before *e* in the alphabet as *incoming* comes before *outgoing*; and the *e* in efferent matches the *e* in *exit*.

## Abstractness, instability, distance

```
A = Σma / (Σmc + Σma)          Abstractness
I = Ce / (Ce + Ca)             Instability
D = |A + I − 1|                Distance from the main sequence
```

**Abstractness** is the ratio of abstract artifacts (interfaces, abstract classes) to all artifacts. Visualize the extremes: an application of 5,000 lines all in one main() method has a numerator of 1 and a denominator of 5,000, giving almost 0. At the other end, a code base so layered in abstraction that nobody can tell what to do with a class named for four design patterns at once.

**Instability** measures volatility. High instability breaks more easily when changed, because the artifact depends on many others — a class delegating to many other classes is highly susceptible to breakage when any of the called methods change.

**Distance** measures how far a component sits from the ideal balance of the two. Both A and I fall between 0 and 1, so graphing them gives a unit square with an ideal line running corner to corner. Components near the line have a healthy mixture of these competing concerns.

Two zones matter:

- **Zone of Pain** — lower left, concrete and stable. Too much implementation, not enough abstraction: brittle and hard to maintain.
- **Zone of Uselessness** — upper right, abstract and unstable. Abstraction nobody can use.

This is one of the very few holistic structural metrics available. It is most useful when getting familiar with an unfamiliar code base, preparing a migration, or assessing technical debt. As a fitness function, assert distance against an ideal of 0.0 with a project-dependent tolerance — 0.5 is a reasonable starting point.

## Process metrics

- **Testability** — code coverage, on every platform. A floor, not a proof.
- **Deployability** — percentage of successful deployments, deployment duration, issues raised by deployments.

Each team should arrive at its own mix of quantitative and qualitative measures.

## The general limitation

These tools are extremely blunt compared to the analysis available in other engineering disciplines. Every one of them requires interpretation, and none can distinguish essential from accidental complexity. That is precisely why establishing a baseline on your own code base and governing against movement from it beats importing someone else's number.

And structural metrics reveal only what is in the code. They cannot evaluate dependent components outside it: however performant or elastic the code is, if the database does not match those characteristics the effort fails. Scope decides operational characteristics, and code metrics cannot see scope.
