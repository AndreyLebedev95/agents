---
name: select-quality-attribute-tactics
description: Picks the design decisions that control a given quality attribute and states what each costs on the others. Supplies tactic catalogs for ten attributes grouped by the goal each serves, and covers refining a tactic into a real mechanism, the super-tactics serving several attributes at once, and the tradeoffs a pattern silently imports because patterns bundle tactics. Use whenever a quality attribute target must be designed for, when a pattern was adopted and another attribute unexpectedly got worse, when someone asks how to structurally improve availability, performance, modifiability, security, testability or deployability, when a tradeoff must be made explicit, when a design needs a mechanism and no published pattern fits, or when someone asks what a decision will cost elsewhere. Use it even when the ask is only "how do we make this faster" structurally. Siblings — elicit-and-prioritize-asrs, write-quality-attribute-scenarios, evaluate-architecture-against-scenarios, choose-architecture-style for topology.
---

# Selecting quality attribute tactics

A **tactic** is a single design decision that influences a quality attribute response — it directly
affects how the system responds to some stimulus. Tactics are design primitives: catalogued, not
invented, and found over and over across different parts of a design.

This skill selects them for a target attribute and forces the cost onto the page.

## Tactic versus pattern, and why it matters

A **pattern** is a proven solution to a recurring design problem. It comprises multiple design
decisions and typically **bundles several tactics**. So adopting a pattern silently adopts whatever
tradeoffs those tactics carry.

That is the mechanism behind the most common surprise in this work: a pattern was adopted for one
attribute and a different attribute got worse, with no decision anyone can point to. Nobody chose
the tradeoff; the pattern brought it.

Two consequences:

- When a pattern's tradeoffs need unpicking, analyze at **tactic** granularity.
- Tactics are also how you fill the gap when no pattern solves your problem completely. You may need
  a high-availability high-security broker, not the textbook broker. Tactics give a systematic way to
  augment a pattern, and — where no pattern exists — to construct a design fragment from first
  principles while still knowing what properties it has.

## The output

```
## Target: <attribute> — <the scenario's response measure>
Structural concern inspected: <what this attribute makes you look at>

| Tactic | Refined mechanism | Serves | Degrades |
|---|---|---|---|
| <catalog tactic> | <the specific strategy chosen> | <attributes> | <attributes, with how> |

## Tradeoffs accepted
<attribute A> improves and <attribute B> degrades because both are sensitive to <decision>.

## Not architecture
<part of the attribute that process must deliver, not this design>
```

A row without a refined mechanism is not a design decision yet. A row with an empty "Degrades"
column is almost always an unfinished analysis rather than a free win.

## Procedure

### 1. Start from the response measure, not the attribute name

A tactic controls a *response to a stimulus*. With no response and no measure there is nothing to
control, and tactic selection degenerates into naming plausible mechanisms. If you have only an
attribute name, go to `write-quality-attribute-scenarios` first.

### 2. Go straight to the structural concern the attribute names

A system's ability to meet its quality attributes is substantially determined by its architecture,
and each attribute points at a specific structure. Use this to scope what you actually read:

| Target | Inspect |
|---|---|
| Performance | Time-based behavior of elements, their use of shared resources, and the frequency and volume of inter-element communication |
| Modifiability | How responsibilities are assigned to elements, and how coupling is limited so most changes hit few elements — ideally one |
| Security | How inter-element communication is managed and protected, which elements may access which information, and whether specialized elements such as an authorization mechanism form a perimeter |
| Safety | The designed-in safeguards and recovery mechanisms |
| Scalability of performance | Whether resource use is localized so higher-capacity replacements can be dropped in, and whether resource assumptions or limits are hard-coded |
| Incremental delivery | How inter-component usage is managed |
| Reusability elsewhere | Inter-element coupling — whether an extracted element comes out with too many attachments to its current environment to be useful |

### 3. Select candidates from the catalog by goal category

Read `references/tactics-catalog.md` for the target attribute. The catalog is organized by the goal
each group of tactics serves — for availability, detect / recover / prevent faults; for security,
detect / resist / react to / recover from attacks; and so on. Choosing the goal category first is
faster and less arbitrary than scanning tactic names.

Note that these lists are not closed. They were themselves derived from a model of each attribute,
so they can be extended the same way — see `model-a-new-quality-attribute`.

### 4. Refine every tactic into a concrete mechanism

A tactic is not a design until it is refined, and its applicability depends on context.

- "Schedule resources" is not a design. Shortest-job-first, round-robin, earliest-deadline-first,
  least-slack-first — those are designs.
- "Use an intermediary" is not a design. A layer, a broker, a proxy, a tier — those are.

Then check the context admits it. "Manage sampling rate" is right in some real-time systems, wrong in
others, and actively harmful in database or stock-trading systems where losing a single event is
unacceptable. A tactic pulled from a catalog without this check is how confident advice lands in the
wrong domain.

### 5. Prefer super-tactics, and count them once

Some tactics are so fundamental that they appear in the realization of almost every pattern and serve
several attributes simultaneously:

- **Encapsulate, restrict dependencies, use an intermediary, abstract common services** — nominally
  modifiability tactics, present almost everywhere.
- **Scheduling** — a load balancer is an intermediary that does scheduling.
- **Monitoring** — serves energy efficiency, performance, availability and safety at once.

Two uses. When one mechanism serves several *target* attributes, it is a cheap win and should be
identified first. And conversely: do not book the same mechanism as an independent win in each
attribute's analysis. Credit it once.

### 6. State the cost

Quality attributes are never achieved in isolation; achieving one always affects the others. Start
from the presumption that **almost every quality attribute negatively affects performance**, and make
the analysis prove otherwise rather than assuming.

The mechanism is usually indirection. Portability is achieved by isolating system dependencies, which
introduces process or procedure boundaries at runtime, which costs performance. The same shape
recurs: the development-time attributes are served by separating and encapsulating responsibilities,
while performance is served by putting things together — which is why they are in perpetual tension.

Fill the "Degrades" column for every row. If you cannot, you have not finished.

### 7. For development-time attributes, price both costs

Making a system more modifiable has two separate costs that get collapsed into one:

- the cost of **introducing** the mechanism
- the cost of **using** the mechanism

Waiting for a change request and editing source costs nothing to introduce and the full
edit-plus-revalidate cost each time. An application generator or UI builder may cost substantially to
acquire and almost nothing per use. Choose by the expected number of exercises, not by which sounds
more sophisticated.

## Decision rules

**Redundancy: match the scheme to the fault class.** The three voting schemes are not
interchangeable.

| Scheme | Protects against | Does not protect against |
|---|---|---|
| Replication (exact clones) | Random hardware failure | *Any* design or implementation error — there is no diversity embedded in it |
| Functional redundancy (design diversity) | Common-mode failures, where replicas fail identically because they share an implementation | Specification errors. Also costs more to develop and verify |
| Analytic redundancy (diverse inputs *and* outputs, separate requirement specifications) | Specification errors; also helps where some input sources are intermittently unavailable | — but needs a voter cleverer than majority rule or simple averaging: it may have to know which sensors are currently reliable, and may be asked to produce a higher-fidelity value than any single component can by blending and smoothing over time |

Keep voting logic a simple, rigorously reviewed and tested singleton, so the probability of error in
the voter itself stays low.

**Bind as late as possible — while the mechanism stays cost-effective.** Computers handle change more
cheaply and less error-prone-ly than people, so later binding is generally better. But the machinery
enabling late binding costs more to put in place. Bind as late as you can justify, no later.

**Decide the four modifiability questions before choosing modifiability tactics.** What can change
(functions, platform, environment, the qualities it exhibits, its capacity)? How likely is each? When
is the change made and by whom — implementation, compile, build, configuration, or execution time; by
a developer, an end user, an administrator, or the system itself? What does it cost? You cannot plan
for every potential change: the system would never be finished, or would be far too expensive, and
would suffer quality problems elsewhere. Decide explicitly which changes are supported and which are
not.

**For integrability, cut either the number of dependencies or the distance across them.** And be
careful with the word "decoupled": service orientation by itself reduces only *syntactic*
dependency. Components that know each other in detail and make assumptions about each other are
tightly coupled no matter what the transport is. See `references/tactics-catalog.md` for the five
kinds of distance.

**Instrument before optimizing.** It is not useful to optimize a portion of the system responsible
for a small percentage of total time. Log to find where time actually goes, then fix what dominates.
Design the remedy in advance so it is available: if a scalable resource pool exists and instrumented
data later shows it is the bottleneck, you increase the pool. If it does not exist, the options are
limited, mostly bad, and may mean considerable rework.

**Check the attribute is worth serving here at all.** Continuous deployment is impossible in a tightly
coupled ecosystem, on unreachable targets, or on non-networked systems. Spending on an attribute the
context forbids is worse than not spending.

**Separate architecture from process.** Some of any attribute is process, not structure. A strong
security architecture is worthless if people fall for phishing or choose weak passwords. Say which
part the design can deliver and which it cannot — it prevents both false blame and false confidence.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Adopted a pattern; an unrelated attribute regressed | The pattern's bundled tactics imported untested tradeoffs | Unpick the bundle; analyze at tactic granularity |
| Tactic named in the design doc, nothing implements it | Never refined into a mechanism | Refine to a specific strategy; verify the context admits it |
| Redundancy added; a systematic bug still took everything down | Replication used where design diversity was needed | Match the scheme to the fault class |
| One mechanism counted as a win in three analyses | Super-tactic double-booked | Identify it once, credit it once |
| "Decoupled" services are still expensive to change together | Only syntactic dependency addressed | Check data-semantic, behavioral-semantic, temporal and resource distance |
| Late-binding machinery built and never exercised | Mechanism cost exceeded its value | Price mechanism cost against per-exercise cost |
| Every tactic row shows a benefit and no cost | Tradeoff analysis not actually done | Presume a performance cost; make the analysis disprove it |
| Optimized the wrong component | Optimized before instrumenting | Log first; fix what dominates |

## Reference

`references/tactics-catalog.md` — every catalogued tactic for the ten attributes, grouped by goal
category, with the refinements each one admits, plus the five kinds of integration distance. Read it
at step 3 whenever selecting tactics. It is also the list a tactics-based questionnaire walks, so
`evaluate-architecture-against-scenarios` draws on it when auditing a design.
