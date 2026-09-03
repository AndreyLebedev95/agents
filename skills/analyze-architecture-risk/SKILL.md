---
name: analyze-architecture-risk
description: Finds and quantifies where an existing architecture will break, and checks what it is not aligned with. Produces a risk matrix scored by impact times likelihood across the system's critical characteristics and its domains, adds direction of travel from measurement, runs risk storming — the three-phase exercise that surfaces the risks one architect always misses — and audits the nine intersections an architecture must align with: implementation, infrastructure, data, engineering practices, teams, integration, enterprise, business and generative AI. Use whenever a design is about to be committed to, when someone asks what could go wrong or whether an architecture will hold or will scale, when auditing or inheriting a system, at the end of an iteration or after a major feature, when preparing a risk-storming session, when an external dependency's reliability matters, when a system fails for reasons that were not in the design, or when a technically sound architecture keeps getting rejected. Use it even when the ask is only "review this architecture". For enforcing rules already agreed use govern-architecture-with-fitness-functions; for designing rather than reviewing use choose-architecture-style.
---

# Analyzing architecture risk

Two questions, and most reviews only ask the first.

**Where will this break?** Answered by scoring risk across the characteristics that matter and the domains that carry them.

**What is this not aligned with?** Answered by auditing the intersections. An architecture can be internally excellent and still fail because the infrastructure cannot deliver what the style promised, or the team structure cannot produce the design, or the enterprise will not accept it.

## The output

```
## Risk assessment
                    | domain A | domain B | domain C | total
characteristic 1    |    6 ▲   |    3 ●   |    2 ▼   |  11
characteristic 2    |    9 ▲   |    4 ●   |    3 ●   |  16
...
total               |   15     |    7     |    5     |
▲ worsening  ● unchanged  ▼ improving

## Alignment findings
<intersection> — aligned | at risk: <the specific gap>

## Mitigation plan
<risk> — option A: <change>, <cost>  |  option B: <cheaper partial change>, <cost>
```

Row totals say what *kind* of risk dominates. Column totals say *where* to spend effort. The two answers are usually different and both are actionable.

## Scoring risk

Risk assessment is otherwise a clash of opinions, with one architect calling something high and another medium. Two dimensions, multiplied:

**Impact** if the risk occurs × **Likelihood** of it occurring, each scored low (1), medium (2) or high (3).

| Score | Band |
|---|---|
| 1–2 | Low |
| 3–4 | Medium |
| 6–9 | High |

Colour the cells green, yellow and red, and add shading so the matrix survives grayscale rendering and readers who cannot distinguish the colours.

Three rules that matter more than the arithmetic:

- **Score impact first, likelihood second.** Scoring in this order stops a comforting likelihood estimate from suppressing analysis of a severe impact. A central database has high impact if it goes down, which alone places it at 3, 6 or 9; establishing that it runs clustered on highly available servers then brings likelihood to low and settles it at 3.
- **If likelihood is unknown, rate it high (3)** until it can be confirmed.
- **Unknown or unproven technology is automatically 9.** The matrix cannot be applied to something nobody understands. See the note below — this rule earns its keep.

The multiplication does not remove subjectivity from the two inputs. It removes it from combining them, and forces the two dimensions to be argued separately, which is where the real disagreement usually is.

## Choosing criteria and contexts

**Criteria** (the rows) are the system's most critical architecture characteristics. There is no point analyzing performance risk when the critical characteristics are scalability, elasticity and data integrity.

**Contexts** (the columns) are domains or subdomains. Not services — service level is usually too fine-grained and misses the risk arising from communication and coordination *between* services, which is where distributed systems actually fail.

## Direction, not just level

A static assessment shows the level of risk and not whether it is improving or deteriorating. Adding direction requires continuous objective measurement, so that trends can be observed per criterion.

Notate with an upright triangle for worsening risk (tip pointing toward the higher number), an inverted triangle for lessening risk, and a circle for unchanged. Always include a key — symbols alone confuse readers.

This changes the story an assessment tells. Data integrity worsening across three domains points at a database problem nobody has named yet. Security and availability improving in two domains confirms earlier work is landing. Neither is visible in a snapshot.

## Filter for the audience

When presenting to stakeholders, filter out the low and medium cells and show only the high-risk areas. Improving the signal-to-noise ratio delivers a message people can act on; the full grid delivers a message people skim.

## Risk storming

No architect can determine a system's overall risk alone. Working solo you will overlook risk areas, and very few architects know every part of the system. Risk storming is a collaborative exercise assessing risk within one dimension, run in three phases.

**Include senior developers and tech leads, not only architects.** They carry the implementation risk, and the exercise teaches them the architecture — which is a second benefit worth having on its own.

**Restrict each session to a single criterion or context** wherever possible, so attention stays focused and nobody is confused about which risk is being rated. If several dimensions must be covered at once, write the criterion beside the number on each note and discuss them separately.

### Phase 1 — Identification, alone

The facilitator sends an invitation carrying the architecture diagram or its location, the risk criteria and context to be analyzed, and the logistics. Participants then analyze **individually**, using the matrix, and write each rating on a green, yellow or red note by band.

The individual phase is not a scheduling convenience. It exists so that participants do not influence each other and nobody's attention is redirected away from part of the architecture before they have looked at it themselves. Doing identification collaboratively anchors the whole group on whatever is said first.

### Phase 2 — Consensus, together

Participants place their notes on a large shared diagram, and every discrepancy is argued to agreement.

**Treat every lone dissenting rating as information, not noise.** Never average the ratings; ask the outlier for their reasoning before arguing with their number. Three things happen, and all three are valuable:

- The outlier is talked down. Someone rating a load balancer high on impact grounds accepts a medium once others establish it is clustered.
- The outlier talks everyone else up. If the majority missed something real, the minority view should prevail.
- The outlier reveals experience nobody else has. A participant rating a component 9 because they had watched that technology crash repeatedly under comparable load surfaces a risk that would otherwise have appeared in production.

### The unknown-technology rule

When any participant does not know a technology in the architecture, that area is automatically rated 9.

This is not a formality. The canonical case is a developer rating a cache component 9 while nobody else saw any risk there; asked why, they answered *"What's a Redis cache?"* The fact that a participant did not recognize a component **is** the finding — the architect may need to change the technology or budget for training, and neither option is visible without the question being asked.

### Phase 3 — Mitigation, costed

Mitigating risk usually means changing parts of an architecture that had been considered finished, and it usually costs money. So involve business stakeholders with the authority to decide whether the cost outweighs the risk — and **arrive with more than one option at different price points**.

The pattern that works: clustering and splitting a database to mitigate an availability risk costs $50,000 and gets rejected as not worth it; splitting into two domain-based databases costs $16,000, still reduces the risk, and gets accepted. Presenting only the expensive option leaves the risk standing.

**Verify each mitigation actually removes the failure** rather than relocating it. A good practice applied is not the same as a risk removed. Worked chain: a diagnostics engine capped at 500 requests/second under seasonal load — asynchronous queues added a backpressure point, and users still waited and timed out; prioritized channels helped, and still left wait times; caching the high-volume question category so those requests never reach the engine at all finally removed it. Keep asking whether the specific failure can still occur.

Prefer eliminating demand over buffering it, where the domain allows. And prefer **structural separation over a check on a shared path**: where only one class of user may reach a resource, per-call authorization on a shared gateway leaves real risk, while giving each user class its own gateway means unauthorized calls can never arrive.

### Cadence

Risk storming is not a one-time process. It continues through the system's lifecycle. Frequency depends on the rate of change, any architecture-refactoring effort, and the pace of incremental development — typically after a major feature, or at the end of every iteration.

The same matrix also works on user stories during grooming: rate the impact if a story is not completed within the iteration and the likelihood it will not be, and the high-risk stories can then be tracked and prioritized.

## Auditing the intersections

An architecture only works if it aligns with everything around it. Walk all nine and record a finding for each — treat them as yes/no alignment questions, not general topics. Where the answer is no, the architecture does not work yet, however good the design.

`references/intersections.md` has each one with the specific failure it produces. The short form:

1. **Implementation** — does the code deliver the characteristics the architecture assumed?
2. **Infrastructure** — can the deployment actually provide the operational characteristics?
3. **Data topologies** — does the database type and topology match the style?
4. **Engineering practices** — do the team's practices and pipeline support this style?
5. **Team topologies** — can this team structure produce and maintain this architecture?
6. **Systems integration** — what else must this talk to, and at what cost?
7. **The enterprise** — is it aligned with organization-wide standards and principles?
8. **The business environment** — does it match the company's position and direction?
9. **Generative AI** — how does incorporating language models affect the architecture?

The one that catches people: **a capable style delivers nothing if the infrastructure does not support it.** Architects are routinely blamed for failures actually caused by this gap.

## Third-party availability

Availability you do not control cannot be engineered away. Find the published commitment instead — a service-level agreement is usually legally binding, a service-level objective usually is not — and convert the percentage to annual downtime so the number means something. 99.99% is 52 minutes 33 seconds a year; 99.9% is 8 hours 46 minutes.

Then decide whether that downtime is acceptable for this workflow, and record the figure on the architecture diagram so the assumption stays visible.

## Judging an inherited architecture

Every architecture is a product of the capabilities and costs available when it was built. Before critiquing one, establish when it was designed and what the constraints were then, and separate decisions that were **correct-then-and-wrong-now** from decisions that were **always wrong**. Only the second category is a design error; the first is drift.

Two biases to filter for in yourself and others:

- **A recurring pet objection.** Someone burned once by a rare failure re-raises that concern on every subsequent design. The tell is an objection that is specific, vivid, historical and disproportionate to its probability. Ask for probability and impact, not the story. This is not licence to dismiss experience-based risk — the test is whether the concern is calibrated.
- **Stale expertise.** Someone who stopped maintaining a technology area keeps deciding with the criteria that were valid when they last worked in it, while believing the information is current. Distinct from the first: that is a mis-calibrated fear, this is a mis-dated fact base.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Risk debate is opinion versus opinion | No quantification | Score impact and likelihood separately, multiply |
| Assessment looks fine, things get worse | Snapshot with no direction | Add continuous measurement and direction symbols |
| Real risk found only in production | One architect assessed alone | Risk storming with developers included |
| Group anchored on the first rating | Identification was collaborative | The individual phase must come first |
| Mitigation rejected, risk left standing | Only one costly option offered | Bring a cheaper partial mitigation |
| Good practice applied, failure still possible | Mitigation relocated the risk | Re-ask whether the specific failure can still occur |
| System fails on an axis the design covered | Implementation optimized a different characteristic | Audit the implementation intersection |
| Architecture blamed for an infrastructure failure | No collaboration with operations | Audit the infrastructure intersection |
| Cache benefits vanished in production | Cross-region or cross-zone placement | Audit physical placement against replication assumptions |
| Technically excellent solution scrapped | Enterprise standards ignored | Audit the enterprise intersection early |
| Simple changes are always hard | Team topology misaligned with architecture | Audit the team intersection |
| Same pet objection on every design | Uncalibrated experience-based fear | Ask for probability and impact, not the story |
| Decisions made on knowledge that aged out | Stale expertise | Re-date the fact base |

## When to reach for a reference

- `references/risk-storming.md` — the full facilitation guide: invitation contents, phase mechanics, note banding, worked consensus cases, and the mitigation negotiation. Read when actually running or preparing a session.
- `references/intersections.md` — the nine intersections with the specific failure each produces, the integration questions, and the availability conversion table. Read when validating an architecture rather than scoring risk.

## Further reading

- *Residues: Time, Change, and Uncertainty in Software Architecture*, Barry O'Reilly — residuality theory, which treats business change as stressors and architectural responses as residues. Emerging rather than established; worth watching.
