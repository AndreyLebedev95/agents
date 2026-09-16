# Evaluation method agendas

## Contents
- [Full stakeholder evaluation](#full-stakeholder-evaluation) — nine steps over four phases
- [Evaluation team roles](#evaluation-team-roles)
- [Internal peer evaluation](#internal-peer-evaluation) — eight steps, under a day
- [Tactics-based questionnaire](#tactics-based-questionnaire) — one attribute, 30–90 minutes

---

## Full stakeholder evaluation

Designed so that evaluators need **no prior familiarity** with the architecture or its business
goals, and so that the system **need not be built yet**. May be held in person or remotely.

### Participants

Three groups, with distinct jobs:

- **Evaluation team** — external to the project under evaluation. Usually **three to five people**,
  each assigned one or more named roles (a single person may hold several). May be a standing unit, or
  assembled from a pool for the occasion; may work for the same organization as the development team,
  or be outside consultants. In any case they must be recognized as competent, unbiased outsiders with
  no hidden agendas.
- **Project decision makers** — empowered to speak for the project or to mandate changes to it.
  Usually the project manager, plus a customer representative if an identifiable customer is paying.
  **The architect is always included**, and a cardinal rule is that the architect must willingly
  participate.
- **Architecture stakeholders** — those whose ability to do their job depends on the architecture
  delivering. Developers, testers, integrators, maintainers, performance engineers, users, and
  builders of interacting systems. Their job is to articulate the specific quality goals the
  architecture must meet for the system to be considered a success. Expect to enlist **10 to 25** for
  a large enterprise-critical architecture — a rule of thumb and nothing more. Unlike the other two
  groups, they do not attend the whole exercise.

### Phases

| Phase | Activity | Participants | Typical cumulative time |
|---|---|---|---|
| 0 | Partnership and preparation | Evaluation team leadership and key project decision makers | Informally as required, perhaps over a few weeks |
| 1 | Evaluation | Evaluation team and project decision makers | 1–2 days |
| 2 | Evaluation (continued) | Evaluation team, project decision makers, and stakeholders | 2 days |
| 3 | Follow-up | Evaluation team and evaluation client | 1 week |

**Phase 0 — Partnership and preparation.** Team leadership and key decision makers work out the
details. The project briefs the evaluators so the team can be supplemented with the right expertise.
Agree logistics: timing, meeting technology, a preliminary stakeholder list **by name, not just by
role**, when the final report is delivered and to whom. Handle formalities — statement of work,
nondisclosure agreements. The team examines the architecture documentation to understand the
architecture and its major design approaches. The team leader explains what the manager and architect
will be expected to present in phase 1, and helps construct those presentations if needed.

**Phases 1 and 2 — Evaluation.** Steps 1–6 run in phase 1 with the team and the project's decision
makers (typically the architecture team, project manager and client). In phase 2, with all
stakeholders present, step 1 is repeated so newcomers understand the method and their role, steps 2–6
are recapped along with the current findings, and steps 7–9 are carried out.

Between them sits a **hiatus of about a week**: the team summarizes what it learned and interacts
informally with the architect. More scenarios may be analysed, or phase 1 questions clarified.

The analogy for why phase 2 is not redundant: phase 1 is testing your own program against your own
criteria; phase 2 is handing it to an independent QA group who will subject it to a wider variety of
tests and environments.

**Phase 3 — Follow-up.** The team produces and delivers the final report, which may be a formal
document or simply a set of slides. It is circulated to key stakeholders first to catch errors of
understanding, then delivered to the client.

### The nine steps

1. **Present the method.** The evaluation leader explains the process everyone will follow, answers
   questions, and sets context and expectations. Describe the steps in brief and the outputs.

2. **Present the business goals.** A project decision maker — ideally the project manager or customer
   representative — gives a system overview from a business perspective, covering: the system's most
   important functions; any relevant technical, managerial, economic or political constraints; the
   business goals and context as they relate to the project; the major stakeholders; and the
   architectural drivers, emphasizing the architecturally significant requirements.

3. **Present the architecture.** The lead architect presents at an appropriate level of detail —
   which depends on how much has been designed and documented, how much time is available, and the
   nature of the behavioral and quality requirements. Cover technical constraints: operating system,
   prescribed platforms, other systems this must interact with. Most importantly, describe the
   architectural approaches (patterns, tactics) used to meet the requirements. Architectural views are
   the primary vehicle: context diagrams, component-and-connector views, module decomposition or
   layered views, and the deployment view are useful in almost every evaluation and the architect
   should be ready to show them. **Cap this at one hour** — the constraint is what produces a concise,
   understandable presentation.

4. **Identify the architectural approaches.** Catalogue the patterns and tactics used, exploiting the
   known ways each affects particular attributes: a layered pattern tends to bring portability and
   maintainability, possibly at the expense of performance; publish-subscribe is scalable in the
   number of producers and consumers; active redundancy promotes high availability.

5. **Generate a quality attribute utility tree.** The goals named or implied in step 2 — "modifiability",
   "high throughput", "portable to a number of platforms" — establish context and direction but are not
   specific enough to tell whether the architecture suffices. Modifiable in what way? Throughput how
   high? Ported to what platforms, in how much time? The answers are scenarios. **The architect rates
   technical difficulty or risk (H/M/L); the project decision makers rate business importance.**

6. **Analyse the architectural approaches.** Examine the highest-ranked scenarios one at a time,
   asking the architect to explain how the architecture supports each. Team members — especially the
   questioners — probe for the approaches used. Document the relevant decisions and identify and
   catalogue their risks, non-risks and tradeoffs. For well-known approaches, ask how the architect
   overcame known weaknesses or gained assurance the approach sufficed. Analysis is not meant to be
   comprehensive; the key is enough information to link decisions to requirements. By the end, the team
   should have a clear picture of the most important aspects of the architecture, the rationale for key
   decisions, and the findings list.

7. **Brainstorm and prioritize scenarios.** Ask stakeholders for scenarios that are operationally
   meaningful with respect to their own roles. Where step 5 captured how the architect saw the drivers,
   this takes the pulse of the wider community — what success means to them. Brainstorming works well
   in larger groups, where one person's ideas stimulate others'. Then: stakeholders merge scenarios
   they feel represent the same behavior or concern, and vote. **Each stakeholder gets votes equal to
   30% of the scenario count, rounded up** (40 scenarios → 12 votes each), allocated however they see
   fit. Compare the result against the step-5 utility tree: agreement indicates alignment, and a large
   discrepancy is itself a risk.

8. **Analyse the architectural approaches (again).** Same activity as step 6, on the highest-ranked
   newly generated scenarios — typically the top five to ten, as time permits. Ideally dominated by
   the architect explaining scenarios in terms of approaches already discussed.

9. **Present the results.** Group risks into risk themes by common underlying concern or systemic
   deficiency, and for each theme identify which business goals from step 2 are affected. Present: the
   architectural approaches documented; the scenarios and their prioritization; the utility tree; the
   risks and non-risks; the sensitivity points and tradeoffs; and the risk themes with the business
   goals each threatens.

### Outputs

1. A concise presentation of the architecture (the one-hour constraint does this).
2. Articulation of the business goals, often being seen by some participants for the first time, and
   surviving as part of the project's record.
3. Prioritized quality attribute requirements expressed as scenarios.
4. A set of risks and non-risks. **The risks are the primary output.**
5. A set of risk themes, identifying systemic weaknesses in the architecture, or in the architecture
   process and team.
6. A mapping of architectural decisions to quality requirements, serving as the rationale for those
   decisions.
7. A set of identified sensitivity points and tradeoff points.

There are also intangible results worth not ignoring: a sense of community among the stakeholders,
open communication channels between architect and stakeholders, and better shared understanding of the
architecture's strengths and weaknesses. Hard to measure, no less real.

---

## Evaluation team roles

| Role | Responsibilities |
|---|---|
| **Team leader** | Sets up the evaluation; coordinates with the client and makes sure their needs are met; establishes the evaluation contract; forms the team; sees that the final report is produced and delivered |
| **Evaluation leader** | Runs the evaluation; facilitates scenario elicitation; administers the prioritization process; facilitates evaluation of scenarios against the architecture |
| **Scenario scribe** | Writes scenarios in a sharable, public form during elicitation; captures the agreed wording of each one, **halting discussion until the exact wording is captured** |
| **E-scribe** | Captures proceedings electronically: raw scenarios, the issues motivating each scenario (often lost in the wording of the scenario itself), and each scenario's analysis results; generates the adopted-scenario list for distribution |
| **Questioner** | Asks probing quality attribute–based questions |

---

## Internal peer evaluation

For a project-internal context, reviewed by peers on a regular basis, using the same concepts as the
full method. Convened and led by the project architect, carried out entirely by people internal to
the organization.

Scope it to **what has changed since the last review** — in the architecture or in the drivers — or to
a previously unexamined portion. Because the scope is limited, many steps can be omitted or shortened.
Duration depends on the number of scenarios examined, which depends on the importance of the system:
anywhere from a couple of hours to a full day.

| Step | Notes |
|---|---|
| 1: Present the method steps | If participants know the process, this may be omitted |
| 2: Review the business goals | Participants are expected to understand the system and its business goals and priorities. A brief review ensures they are fresh and that there are no surprises |
| 3: Review the architecture | Participants are expected to be familiar with the system, so present a brief overview using at least the module and component-and-connector views, highlighting changes since the last review, and trace one or two scenarios through the views |
| 4: Review the architectural approaches | The architect highlights the approaches used for specific quality concerns — typically folded into step 3 |
| 5: Review the utility tree | **A utility tree should already exist.** Review it and update it if needed with new scenarios, new response goals, or new priorities and risk assessments |
| 6: Brainstorm and prioritize scenarios | A brief activity to establish whether any new scenarios merit analysis |
| 7: Analyse the architectural approaches | Mapping the highly ranked scenarios onto the architecture. **Consumes the bulk of the time.** Focus on the most recent changes, or a part not previously analysed. If the architecture changed, reanalyse the high-priority scenarios in light of those changes |
| 8: Capture the results | Review existing and newly discovered risks, non-risks, sensitivities and tradeoffs, and discuss whether new risk themes have arisen |

**No final report**, but a scribe captures the results, which are shared and serve as the basis for
risk remediation.

The honest cost: the team, being internal, is typically less objective than an external one, so you
hear fewer new ideas and fewer dissenting opinions, and that may compromise the value of the results.
In exchange it is inexpensive, easy to convene, and low-ceremony enough to deploy whenever a project
wants an architecture sanity check.

---

## Tactics-based questionnaire

The lightest method. Focuses on a **single quality attribute at a time**. Usable by the architect for
reflection and introspection, or to structure a question-and-answer session between an evaluator and
an architect or group of designers. Typically **around one hour per attribute** (30–90 minutes), and
usable at any point in the lifecycle, including very early ones — with the caveat that accuracy and
confidence vary with artifact maturity.

Transform each tactic for the attribute into a question ("Does the system support the detection of
intrusions?", "Does the system support the verification of message integrity?"), then for each one
record four things:

1. **Supported** — Y if the tactic is supported in the architecture, N otherwise.
2. **Design decisions and location** — if Y, describe the specific decisions made to support the
   tactic, and enumerate where those decisions are, or will be, manifested: which code modules,
   frameworks or packages implement it. Useful for auditing and architecture reconstruction later.
3. **Risk** — the risk of implementing the tactic, rated H / M / L.
4. **Rationale** — the rationale for the decision, **including a decision *not* to use the tactic**,
   and a brief explanation of the implications for cost, schedule, evolution and so on.

Addressing the full set of questions forces a step back to the bigger picture, which is where the
value comes from — it is more powerful than the simplicity suggests.

**Columns 2 and 4 are not optional.** One healthcare system was asked "does the system support data
encryption?" It had a requirement that no data pass over the network in the clear, and met it by
XOR-ing all data before sending. Strictly compliant; crackable by a schoolchild. A bare "Y" would have
passed it. Recording the mechanism is what caught it, in minutes, for almost no cost.

Tactic lists per attribute are in the `select-quality-attribute-tactics` skill's catalog.
