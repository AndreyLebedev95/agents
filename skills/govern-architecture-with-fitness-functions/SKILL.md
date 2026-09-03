---
name: govern-architecture-with-fitness-functions
description: Makes architecture characteristics measurable and enforces them automatically, so structure does not decay under schedule pressure. Covers the metrics that matter (cyclomatic complexity with real thresholds, lack of cohesion, afferent and efferent coupling, distance from the main sequence), fitness functions as executable governance in the build and in production, structural rules with ArchUnit, NetArchTest, PyTestArch, TSArch and JDepend, chaos engineering, and the ways teams game a metric. Use whenever an architecture decision needs enforcing, when someone asks how to stop layer violations or dependency cycles or import sprawl, when modularity or coupling or complexity is drifting, when a code base must be assessed before a migration or technical-debt review, when a standard exists that nobody follows, when someone asks what to automate in CI to protect the architecture, or when someone asks how to measure agility, testability, deployability or structural decay. Use it even when the request is only "how do we stop this getting worse". For deciding which characteristics deserve governing use elicit-architecture-characteristics; for risks that have not materialized use analyze-architecture-risk. Not for reviewing a diff — that is code-review-expert.
---

# Governing architecture with fitness functions

Architecture decays because urgency beats importance. Modularity is the archetype: it matters enormously and neglecting it costs nothing today, so under schedule pressure it always loses. Governance is the practice of encoding the important concerns into the substrate so they stop having to compete for attention.

A **fitness function** is any mechanism giving an objective integrity assessment of an architecture characteristic, or a combination of them. It is not a framework to install. It is a lens on tools that already exist — metrics, monitors, unit-test libraries, linters, chaos engineering. The phrase "any mechanism" is load-bearing: verification techniques vary as widely as the characteristics do.

## The output

A governance plan:

```
## <characteristic or decision being protected>
Measure:      <what is measured, and the baseline value on THIS code base>
Mechanism:    <the specific check — tool, assertion, or observation>
Runs:         build | production | version control | manual (with reason)
Fails when:   <the condition, expressed against the baseline>
Gaming path:  <how this could be satisfied without achieving the intent, and the second-order check>
```

Where the mechanism is code, produce the code.

## Procedure

### 1. Start from the characteristics, and make them measurable

Take the driving characteristics. Where one has no direct measure, decompose it until every part does — agility becomes deployability, modularity and testability. Govern the decomposed measures, not the original word.

Three things make characteristics resist definition: they are not physics and their meanings are vague; definitions vary even between departments in one organization; and many are composites. Decomposition solves all three.

### 2. Baseline before you threshold

Establish the current value of each metric on *this* code base and record it. Then govern against movement from the baseline rather than against an industry number.

This matters because no code-level metric distinguishes essential complexity — the problem is genuinely hard — from accidental complexity, where the code is worse than it needs to be. An absolute threshold cannot know which it is looking at. A regression from a known baseline is a much stronger signal, and it is one you can act on without an argument about whether the domain is inherently complicated.

Absolute thresholds still have value as a secondary signal. `references/metrics.md` has the ones worth knowing.

### 3. Name a detection mechanism for every decision

An architecture decision with no compliance mechanism is a suggestion. Decisions that are documented and communicated but never verified get violated by teams acting on locally reasonable motives, and the violation silently removes whatever characteristic the decision existed to protect.

So for each decision, write down what will detect a violation. If nothing can, either build something or drop the decision — an unenforceable rule is worse than no rule, because it creates the illusion of governance.

Keep this proportional. Decisions protecting a driving characteristic need automation; cosmetic conventions do not.

### 4. Write the check as an ordinary test

Structural rules are assertions. They belong in the project's own test framework, running in the continuous build alongside functional tests, because that is where developers already look when something fails.

`references/cookbook.md` has worked checks by tool. The common ones:

- **Dependency cycles** — components referencing each other in a loop destroy modularity, since no component can be reused without dragging the others along, and the code base drifts toward a big ball of mud.
- **Layer access rules** — define each layer by package, then assert which layers may access which.
- **Module compliance** — assert every namespace in the repository falls under a declared module, so a new top-level directory triggers an alert.
- **Dependency caps** — assert no module exceeds a chosen count of incoming plus outgoing references.
- **Pairwise restrictions** — assert two specific modules never reference each other.
- **Structural distance** — assert each package sits within tolerance of the ideal abstractness/instability balance.

### 5. Prefer build-time detection to review for anything that accrues

Code review catches cycles too late. Modern IDEs offer to auto-import a class the moment it is referenced, and developers swat that dialog away reflexively; a week of that before review has already done the damage.

The general rule: any violation that accumulates in small increments needs build-time detection, not periodic inspection. Review is for judgment, not for counting.

### 6. Ask how each metric could be gamed

Once developers learn how compliance is measured, some satisfy the measure instead of the intent. The canonical case is unit tests written with no assertions — the code is touched, coverage rises, nothing is verified.

For each metric, name the path that satisfies it without achieving the intent, and add a second-order check on that path. Assert that every unit test contains at least one assertion.

This stops accidental erosion. Determined rule-breakers will still find a way, and that is an acceptable limit — governance targets drift, not subversion.

### 7. Reach outside the code when the code cannot answer

Some properties are invisible to static analysis:

- **Rate of change** — whether something meant to be stable actually is. Source the check from version-control history: measure churn per area over a window and alarm on a rise. Nothing in the code says how often it changes.
- **Runtime interaction** — which services actually call which. Have every service log its outgoing calls with target and protocol, then analyze the logs. This only works if logging is consistent, which a shared library providing one logging API can enforce at compile time. Alternatively, have each service register its interservice calls to a configuration service at startup and query that for a full call map.
- **Boundary violations across integrated systems** — read each integration point's logs over a window and assert every operation conforms to the permitted operation/target pairs.
- **Contract erosion** — record which fields in each published contract are never read by any consumer. Unused fields are the measurable form of stamp coupling; removing them shrinks payloads, cuts bandwidth, and eliminates changes that would otherwise ripple to consumers who never cared.

### 8. Govern in production where that is the only honest place

Some characteristics can only be verified against real conditions. Production fitness functions inject the failure and check the system endures it — the discipline exists because losing control of operations to a cloud provider left no other way to know.

Build the specific failure your environment actually exhibits rather than generic chaos. `references/production-governance.md` covers the pattern set. The framing that matters: it is not whether something will break but when, and anticipating those breakages is what makes systems robust.

Also sweep for orphans. In an evolving architecture teams migrate to newer services and leave old ones running, and in the cloud those cost money.

### 9. Where nothing can be automated, tag for context

Some rules cannot be verified at all — no test can tell whether a component labelled a validator is actually validating. The fallback is metadata: tag the component's entry-point class with its architectural role. Tags perform no function; they tell the next developer what kind of thing they are modifying, which discourages loading it with work that belongs elsewhere.

Because a component spans multiple classes, define a second marker for the entry-point class so the role tag has somewhere to attach.

This provides context, not enforcement. Use it where automation is impossible, not where it is merely inconvenient.

### 10. Design the rules with the people they constrain

A rule developers do not understand gets worked around. Someone with a legitimate local concern — performance, usually — reads an unexplained constraint as an arbitrary obstacle and routes around it, in good faith.

So design governance collaboratively, and make sure the purpose of each check is understood before it is imposed. The point is not ceremony; it is that governance is a reminder mechanism, in the way pilots and surgeons use checklists — not because they are forgetful, but because details slip when a detailed job is done repeatedly.

## What metrics cannot tell you

- **No metric separates essential from accidental complexity.** Every high score is a question: is this hard because the problem is hard, because the code is poor, or because a large method should have been several? Interpret before acting.
- **Coverage is a floor, not a proof.** 100% with weak assertions gives no confidence.
- **Code metrics cannot see the dependencies that decide operational characteristics.** However performant the code, if the database does not match the characteristic the effort fails. Scope, not code quality, decides operational outcomes.
- **Averages hide the failures that matter.** Measure maximums and percentiles; better, model the characteristic over time and alarm on deviation from the prediction, where a breach means either the model or the system is wrong and both are worth knowing.

One current note worth acting on: cyclomatic complexity is especially worth running against generatively-produced code, which tends to solve problems by brute force and so introduces accidental complexity.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Decision documented, routinely violated | No detection mechanism named | Name one per decision, or drop the decision |
| Coverage high, confidence low | Tests without assertions | Assert every test contains an assertion |
| Cycles everywhere despite reviews | Review runs after a week of drift | Cycle detection in the build |
| Developers route around a rule | Imposed without explaining purpose | Design with the team; explain before imposing |
| Metric breach triggers reflex refactor | Threshold treated as a verdict | Interpret: essential, accidental, or partitioning |
| Alarm never fires until the outage | Average-based monitoring | Percentiles plus model-deviation alarms |
| Contract change breaks unknown consumers | Static coupling ungoverned | Track contract churn and never-read fields |
| Cache-based system runs out of memory at scale | Memory footprint ungoverned | Per-instance memory plus instance-count functions |
| A core meant to be stable keeps changing | Volatility invisible to code analysis | Fitness function over version-control churn |
| Integration boundary quietly violated | No boundary check | Log-reading assertion on operation/target pairs |
| The source tree drifted from the design | Directory structure ungoverned | The source tree *is* the logical architecture — assert it |
| Numbers refuse to move despite effort | Not an implementation problem | Treat it as an alignment problem and look wider |

## When to reach for a reference

- `references/metrics.md` — formulas, thresholds and how to read each score: cyclomatic complexity, lack of cohesion in methods, abstractness, instability, distance from the main sequence with the zones of pain and uselessness, afferent and efferent coupling. Read when choosing what to measure or interpreting a result.
- `references/cookbook.md` — worked checks by tool and platform. Read when writing an actual assertion.
- `references/production-governance.md` — the production fitness-function pattern set and when a characteristic can only be verified live. Read when build-time checks cannot cover it.

## Further reading

- *Building Evolutionary Architectures*, Neal Ford et al. — the origin and full treatment of fitness functions, and how to build architectures that change gracefully over time.
- *Chaos Engineering*, Casey Rosenthal and Nora Jones — production governance in depth.
