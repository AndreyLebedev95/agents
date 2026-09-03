---
name: elicit-architecture-characteristics
description: Turns requirements and stakeholder goals into the small set of architecture characteristics a system must actually support, each defined so it can be measured. Translates business language ("time to market", "mergers and acquisitions", "user satisfaction") into engineering characteristics, separates explicit from implicit ones, decomposes composites like agility into measurable parts, and caps the list with an unranked top three. Use whenever a new system or major feature is being designed, when requirements are being read for what they imply structurally, when a stakeholder demands "five nines" or "lightning fast" or "zero downtime", when a team disagrees about which quality attribute to optimize, when someone asks whether a concern is architectural or just design, when someone says "non-functional requirements" or "quality attributes", or when an older system is being reassessed. Use it even when the request is only "what should this system be good at" or "what are the -ilities here". For making the resulting characteristics measurable and enforced use govern-architecture-with-fitness-functions; for turning them into a topology use choose-architecture-style; for the stakeholder conversation itself use negotiate-architecture-decisions.
---

# Eliciting architecture characteristics

Architecture characteristics are the capabilities a system must have, as opposed to the behavior it must exhibit. Behavior comes from the domain; capabilities are what you are here to determine.

This is worth doing carefully because the characteristics you settle on drive every structural decision that follows. Get them wrong and you will build the wrong shape of system very competently.

Two things make this harder than it looks. The most important characteristics are frequently the ones nobody writes down, because everyone in the domain already assumes them. And stakeholders and engineers use different vocabularies for the same concerns, so the requirement arrives in a form you cannot act on.

## The output

A driving-characteristics list:

```
## Driving characteristics
1. <name> — <operational definition for THIS system, with numbers>
   source: explicit | implicit | translated from "<stakeholder's words>"
   [TOP 3]
...

## Others considered
<name> — <why it did not make the driving list>

## Deliberately under-served
<name> — <what we are accepting instead, and why>
```

Aim for at most seven driving characteristics with three marked as top. The cap is not arbitrary precision — it is a forcing function. Every characteristic a system supports adds design effort, implementation effort, maintenance, and often structure, and characteristics interact, so improving one degrades another. Trying to support them all produces a generic architecture that attempts every business problem, becomes unwieldy, and rarely works.

There is no best architecture, only a least-worst set of trade-offs. Say out loud which characteristics you are choosing not to serve.

## Procedure

### 1. Harvest from all three sources

Characteristics come from exactly three places, and only two of them are written down.

- **Explicit** — stated in the requirements. Look for numbers: user counts, response times, uptime targets, volumes, deadlines.
- **Translated** — the stakeholders' business concerns, which arrive in business language and must be converted.
- **Implicit** — what this domain assumes and never states.

Label every candidate with its source. The implicit ones especially need playing back to stakeholders for confirmation, since you inferred them.

The implicit set is where the expensive misses live. A firm doing high-frequency trading may never write "low latency" in any requirement, because every architect there already knows. Medical software reading diagnostics equipment will not specify data integrity. Ask directly: *what does this domain take for granted?*

### 2. Translate business concerns into characteristics

Stakeholders talk about mergers, user satisfaction, time to market and competitive advantage. Architects talk about interoperability, fault tolerance and elasticity. Neither can act on the other's vocabulary, so elicitation is largely translation. `references/translation-table.md` has the standard mappings.

Play every mapping back to the stakeholder. You are checking you translated *their* goal and not your preference.

### 3. Decode quantities and read past the exaggeration

Requirements state characteristics as domain facts. "Thousands of users, perhaps one day millions" is a scalability requirement that never uses the word.

Exaggerated language is a signal, not a literal claim. "I needed it yesterday" means time to market matters. "Lightning fast" means performance. "Zero downtime" means availability is critical. Read the characteristic underneath rather than the number on the surface.

Then ask a second question the first one hides: **what shape is the load?** Scalability is a growing number of concurrent users; elasticity is sudden bursts. They are different constraints with different designs. A hotel reservation system is scalable and predictably seasonal. A concert ticket system faces a flood the second tickets go on sale. A sandwich shop's traffic spikes at mealtimes even though no requirement says so.

Distributions matter more than totals. Given "1,000 students, 10-hour registration window", do not assume even spread — ask what the humans in this domain actually do. They procrastinate; design for 1,000 in the last ten minutes.

### 4. Filter through three criteria

A requirement is an architecture characteristic only if all three hold:

1. It specifies a **nondomain** design consideration — a capability, not a behavior.
2. It **influences structure**.
3. It is **critical or important to success**.

Criterion 2 is the discriminating one, so give it its own step.

### 5. Apply the design-versus-structure test

Ask: *could the current structure deliver this with better design?*

If yes, it is a design concern. Handle it in code and in governance, and keep it off the driving list. Security is usually here — encryption, hashing and salting inside a monolith are coding hygiene, and security only becomes architectural when the architect decides it needs special structure, such as a hardened service with stricter access protocols.

If no, it is an architecture characteristic and it constrains the style. Scalability is the clean example: past a certain point no amount of clever design makes a monolith scale, and the system must become distributed.

Weight operational characteristics heavily here — they are the ones that most often force structure.

Note that process concerns can qualify. If deployability and testability are high priorities, that alone justifies emphasizing modularity and isolation at the architecture level.

### 6. Decompose every composite

Some characteristics have no direct measure. Agility is really deployability plus modularity plus testability. Recurse until every part has an objective measurement.

The failure this prevents is serving one slice of a composite because it is the convenient one. "We must complete end-of-day fund pricing on time" reads as performance. It also requires availability (speed is worthless if the system is down), scalability (more funds arrive over time), reliability (must not crash mid-run), recoverability (must restart from 85% complete, not from zero) and auditability (fast wrong prices are still wrong). An architect who designs only for performance ships a system that fails for reasons nobody costed.

### 7. Write an operational definition for each

Characteristic names are imprecise, ambiguous and overlapping, so agreeing on the word is not agreeing on the requirement. Interoperability implies ease of integration and therefore published, documented APIs; compatibility is about conformance to industry standards. Learnability means either how easily users learn the software or how well it self-configures. Availability and reliability sound synonymous and are independent — IP is available and not reliable, since packets can arrive out of order or vanish.

So for each surviving characteristic, write what it means concretely *for this system*, with numbers. Do not import another organization's definition. Where an organization does this consistently, the definitions become its ubiquitous language.

Two rules for the numbers:

- **Pair performance with load.** A response-time target with no concurrency figure is meaningless. State a baseline unloaded, then the acceptable figure at the target user count.
- **Convert vernacular into units.** "Five nines" is 5 minutes 35 seconds of downtime per year, about one second a day. Stakeholders often do not know that. `references/measurement-reference.md` has the full table.

### 8. Cap the list and get an unranked top three

Ask a stakeholder which characteristics they want and the answer is always "all of them". The technique that breaks this:

1. List candidates in about seven slots. Six or eight work too — the point is a hard cap.
2. Keep implicit characteristics in a second column. Pull one into the driving list only when it needs special design.
3. When the list is full and a better candidate appears, move the displaced one to "others considered".
4. Have stakeholders collaboratively check the **top three, in any order**.

Do not attempt to rank the whole list. Stakeholders rarely agree on a full ordering, and forcing one wastes time and manufactures conflict. Agreeing on an unordered top three is achievable and sufficient to drive design decisions and trade-off analysis.

### 9. Test criticality by subtraction

Ask which single characteristic you would eliminate if forced. Repeat until removing anything would break the system. Explicit characteristics are the more likely casualties, since implicit ones tend to underpin general success.

Dropping something from the driving list does not mean building the system badly on that axis. It means not prioritizing it over the others.

### 10. Check the end-to-end path

A characteristic delivered in one stage and destroyed in another is not delivered. Code that can be modified in minutes gives no agility if testing takes weeks and release takes months — and testing and release environments are routinely left out of the assessment.

For each time-based characteristic — agility, deployability, testability, time to restore — trace the whole path from change to production and record the slowest stage as the real value.

## Guard against over-specifying

Overspecifying is as damaging as underspecifying. The mechanism is usually unnecessary brittleness: a hard dependency where graceful degradation would have done. For each characteristic, ask what happens when the thing it protects is unavailable — should the system fail, or run with reduced capability? If an external traffic service is down, should an ordering site fail, or just offer less efficient directions?

The cautionary case is a 1628 warship built to be both troop transport and gunship, with two gun decks instead of one and cannons twice the usual size. It capsized in the harbour firing its first salute.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Long list, generic design, nothing prioritized | No cap applied | Cap at ~7; force the top three |
| System fails on an axis nobody costed | Served one slice of a composite | Decompose before designing |
| Stakeholders answer "all of them" | Asked an unbounded question | Run the worksheet and the top-three exercise |
| Hard dependency where degradation would do | Overspecified | Ask "fail or degrade?" per dependency |
| Two teams mean different things by one word | No operational definition | Write definitions; adopt as shared language |
| Characteristic present in code, absent in production | Measured one stage | Trace change-to-production end to end |
| The critical characteristic was never written down | It is implicit in this domain | Ask what the domain assumes and never states |
| Design collapses under real traffic | Assumed uniform distribution | Ask what the humans actually do |
| Decision made without the implementation team | No cost information in the room | Bring tech lead, developers, ops and UX in |

## When to reach for a reference

- `references/translation-table.md` — business-concern-to-characteristic mappings, and the four characteristic categories with definitions. Read when generating candidates or when a stakeholder names something unfamiliar.
- `references/measurement-reference.md` — the nines-of-availability table with annual and daily downtime, front-end performance budgets, and the performance-with-scale rule. Read when a target must be quantified.
- `references/intake-template.md` — a four-section format for framing a design problem when the requirements arrive unstructured. Read when there is no usable problem statement to work from.
