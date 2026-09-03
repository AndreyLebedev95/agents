---
name: map-subdomains-and-boundaries
description: Maps a business domain into subdomains, decides where the model boundaries belong, and names the contract on every edge between them. Covers classifying each area as core, supporting or generic and deriving build/buy/outsource and staffing from that; distilling subdomains down to coherent use-case sets; sizing a boundary between the language-consistency ceiling and the integration-overhead floor; the seven integration patterns chosen by team relationship rather than technology; and reading a context map for the organisational problems it exposes. Use whenever deciding which module, service or context owns what; asking which areas deserve real engineering investment versus an off-the-shelf product; when the same concept needs conflicting models in different places; when one change keeps touching several components; when two teams keep colliding on one codebase; when assessing an inherited or legacy estate; or when deciding how two contexts should integrate — even when the ask is only "where should we draw the line". For sizing by coupling, connascence, cohesion and data isolation use decompose-system-into-components; for the overall topology and style use choose-architecture-style; for the terms inside a boundary use build-domain-glossary; for how much modelling machinery an area deserves use choose-business-logic-pattern.
---

# Mapping subdomains and boundaries

Two different questions get confused here, and separating them is most of the work.

**Which areas of the business is this system serving, and what is each one worth?** You do not get a vote on this. It follows from the company's strategy, and your job is to find out what is already true.

**Where do the model boundaries go?** This one you design. It follows from where mental models conflict, how much you currently know, who owns what, and what has to deploy independently.

Confusing them makes teams argue about business facts as though they were design choices, and accept design choices as though they were business facts.

## The output

Three artifacts, in order:

1. **Subdomain map** — each area of activity, its type, and the implementation strategy that follows.
2. **Boundary set** — the named model boundaries, which subdomains each holds, which team owns it, and the terms it owns.
3. **Context map** — every boundary as a node, every edge labelled with its integration pattern and direction, plus the organisational findings the map exposes.

## Part 1 — Classify the areas

### Three types, and what each one buys

| Type | Differentiating? | Complexity | Volatility | Strategy | The problem is |
|---|---|---|---|---|---|
| **Core** | yes | high | high | build in-house, best people, most advanced techniques | interesting |
| **Generic** | no | high | low | buy or adopt | already solved |
| **Supporting** | no | low | low | build cheaply, or outsource | obvious |

The type is a property of the business strategy, not of the technology. An area can be core without involving software at all — a jeweller's designs are core and their online shop is generic, and no amount of engineering changes that.

The type is what licenses effort. Core subdomains change constantly, so their solutions must be easy to evolve, and they should sit close to the people who hold the knowledge. Supporting subdomains are a reasonable place to train people up. Generic ones you should not be writing at all.

### Classifying

Start from departments and organisational units as coarse candidates, then open each one up — **types differ inside one department**, and stopping at the department boundary is the most common way to miss a core subdomain.

A customer service department looks generic at a glance. Opened up, it usually contains a generic help desk and phone system, a supporting shift scheduler, and — if the company is any good — a genuinely core routing algorithm that decides which agent gets which case. Classify the whole department as generic and you outsource the one thing that differentiates it.

Three cross-checks when the type is unclear:

- **Side-business test.** Could this be sold as a standalone business? Would anyone pay for it on its own? Then it is core.
- **Build-versus-integrate test.** For supporting versus generic: if hacking your own would genuinely be simpler and cheaper than integrating an existing product, it is supporting.
- **Shape of the logic.** Data entry, validation and format conversion signal supporting. Complex algorithms, or processes orchestrated by rules and invariants, signal core.

### Distilling

Keep opening areas up until you reach a **coherent set of use cases** — one actor, one closely related set of data, a strong functional relationship where changing one requirement is likely to affect the others. That is the natural stopping point.

Stop early when further splitting produces only sub-parts of the same type as the parent, and stop entirely on business functions the software does not touch. Distil core subdomains hard; relax for the rest, where finer granularity buys no new decision.

### Re-run this periodically

Types move, and each direction has a tell:

- **Core → generic**: a product appears on the market that does it better and cheaper. The advantage became a commodity.
- **Generic → core**: the company decides an in-house version will beat what everyone else buys.
- **Supporting → generic**: an off-the-shelf or open-source equivalent covers it.
- **Supporting → core**: **the logic is getting more complicated.** Supporting areas are simple by definition, so ask why. Complexity that does not affect profit is accidental and should be cut. Complexity that increases profit means the area has become core — it must move in-house, and it can no longer be duplicated across teams.
- **Core → supporting**: the complexity stopped paying for itself and gets cut back; now outsourceable.
- **Generic → supporting**: integration cost exceeded the benefit and the work came back in-house.

**Design pain is the signal.** When adding features to an area is increasingly painful, the usual cause is that the area changed type and the design no longer fits its complexity. Treat that as a call to reassess the business, not just to refactor.

## Part 2 — Place the boundaries

### The boundary is where the language stops being consistent

A boundary exists to keep one model coherent. When experts in different areas hold genuinely different mental models of the same term, that is the boundary — do not reconcile them.

Trying to build one model that serves every problem produces the wall-sized diagram that is suitable for everything and effective for nothing. It does not remove complexity; it relocates it into three new forms: filtering out the details you do not need, finding the ones you do, and keeping the whole thing consistent.

### Sizing: a ceiling and a floor

**Ceiling.** A boundary cannot be wider than the span over which the language stays consistent. Past that you have conflicting models inside one boundary.

**Floor.** Below the ceiling you may decompose further, but every split adds integration overhead. Small is not automatically better.

Legitimate reasons to split below the ceiling: a new team, a non-functional requirement, separating deployment lifecycles, scaling one function independently.

**Size is an output, not a target.** Of all the heuristics for placing a boundary, its size is among the least useful. Make the boundary a consequence of the model it encloses, not the model a consequence of a size you wanted.

### Start wide

Boundaries get invalidated when the domain is poorly understood or the requirements churn — which is exactly the profile of a core subdomain early on. Since refactoring a *logical* boundary costs far less than refactoring a *physical* one, begin wide and split as knowledge accumulates.

When a boundary holds a core subdomain, deliberately include the subdomains it interacts with most — core, supporting or generic — as insurance against being wrong about where the lines go.

Expect insight to be disruptive. Initial simplicity in a domain is usually deceptive; as functionality is added, edge cases, invariants and rules surface, and those discoveries are often large enough to require rebuilding the model and its boundaries. Design for that rather than against it.

### Ownership and physicality

- **One boundary, one owning team.** Never two. A team may own several boundaries; a boundary may not have several teams. Shared ownership breeds implicit assumptions about each other's model; sole ownership forces the integration contract to be made explicit.
- **A boundary is a physical thing** — its own service or project, built, versioned and deployed independently, free to use whatever technology suits it. Subdomains inside one boundary are logical only: namespaces, modules, packages.
- **Architecture is chosen per subdomain, not per boundary.** One boundary can hold subdomains of different types needing different approaches. Imposing one architecture across the whole boundary produces accidental complexity.

### Boundary defects

| Tell | What it means | Fix |
|---|---|---|
| One change always touches several boundaries | Coherent functionality was split across them; they now change and deploy in lock-step | Re-draw around coherent use cases on the same data |
| Boundaries are chatty — cannot complete an operation without calling each other | Ineffective model | Re-draw for autonomy |
| A boundary has accumulated logic for unrelated problems | It lost focus as the system grew | Extract a boundary aimed at one problem |
| An aggregate has been split across boundaries | Worse than suboptimal | Never split one; see `design-aggregates-and-invariants` |

The compounding problem with all of these: re-drawing boundaries is expensive, so in practice bad ones are left alone and accumulate debt. That is why the wide-first rule matters — it keeps the expensive mistake unmade for longer.

### How wide can a boundary legitimately be?

A boundary is the **largest valid monolith**, and that is a real design option, not a failure — it is not the same thing as a ball of mud, because it still protects one coherent model.

At the other end, an aggregate is the **narrowest possible** boundary, and splitting one across services causes real damage.

Between those, aligning with **subdomains is the safe default**: a subdomain describes what the business does rather than how, so its description is a simple interface over complex logic, and its coherent use cases change together. Go narrower only when a non-functional requirement forces it.

For sizing by coupling, connascence, cohesion and data isolation — a different and complementary lens — use `decompose-system-into-components`.

## Part 3 — Name the contract on every edge

Boundaries are not independent; they have to integrate, and every touchpoint is a contract. **Which contract shape fits is decided by how the two teams relate, not by the technology.**

### Cooperation — both teams succeed or fail together

- **Partnership.** Coordination is ad hoc and two-way; either side notifies the other of a change and both adapt. Needs frequent synchronisation and continuous integration, so it fits colocated teams and fits distributed ones badly.
- **Shared kernel.** A small shared model both sides own and co-evolve. This contradicts one-boundary-one-team and must be a deliberate exception. Justify it only when integrating divergent changes would cost more than coordinating one shared codebase — which, since integration cost rises with volatility, means it lands naturally on core subdomains. Keep the shared scope to the integration contracts and the data structures that actually cross, and make every change trigger integration tests in all dependents.

### Customer–supplier — one side can succeed without the other

- **Conformist.** The downstream accepts the upstream's model. Right when the upstream contract is an industry standard, well established, or simply good enough.
- **Anticorruption layer.** The downstream translates instead of conforming. Choose it when the downstream is a core subdomain and a foreign model would distort its modelling; when the upstream model is inefficient, inconvenient or messy, as with legacy systems; or when the upstream contract changes often, so the churn is absorbed by the translation rather than the model. **Conform to a mess and you risk becoming one.**
- **Open-host service.** The supplier protects consumers by separating its internal model from its public contract, expressed in an integration-oriented language rather than its own internal terms. That decoupling lets the internal model evolve freely and lets several versions of the public contract run at once for gradual migration. It is the mirror of an anticorruption layer — the supplier does the translating.

### Separate ways — no integration at all

Legitimate when collaboration costs exceed duplication costs: politics make agreement expensive; the function is generic and trivially integrated locally (a logging library has no business being exposed as a service); or the models differ so much that a translation layer would cost more than writing the function twice.

**The one hard exclusion is core subdomains.** Duplicating those defeats the reason you invested in them.

### Reading the map

Plotting the edges gives three readings. The first two are obvious — which components exist, and who collaborates with whom. The third is the one people miss:

- Every downstream consumer of one team builds an anticorruption layer → the map is telling you about that team, not the software.
- Every separate-ways decision clusters on one node → same.
- A core subdomain implemented by an outsourced company, or duplicated in two places → strategic defect.
- Integration between two components fails frequently → the relationship pattern is wrong for the collaboration that actually exists.

Charting is genuinely hard when a boundary spans several subdomains: one pair of boundaries can legitimately carry two different integration patterns at once. Label edges per subdomain when that happens rather than forcing one label.

Make each team responsible for keeping its own edges current.

### When the organisation changes, the patterns move

Because one boundary can have only one owning team, adding teams splits wide boundaries. Distance does the rest: partnership assumes strong communication, so moving one side to a distant office pushes the relationship toward customer–supplier. Where communication problems are severe enough that integration keeps failing, duplicating can become cheaper than continuing to coordinate — provided the area is not core.

## Bundled references

- `references/integration-patterns.md` — the seven patterns in full, with selection conditions, costs, and the conditions under which each stops being appropriate. Read when labelling context-map edges or when a relationship has started failing.
- `references/legacy-assessment.md` — charting an estate that already exists: the decoupled-lifecycle test, the strategic smells, aligning modules before moving anything, and the strangler migration with the one rule it is allowed to break. Read when the system is not greenfield.

## Worth reading

- Eric Evans, *Domain-Driven Design* (2003) — the origin of the boundary and context-mapping patterns.
- Nick Tune, *Architecture Modernization* — applying this to brownfield estates.
