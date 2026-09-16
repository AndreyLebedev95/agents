# Elicitation checklists

## Contents
- [Thirteen categories to mine a requirements document](#thirteen-categories-to-mine-a-requirements-document)
- [Eleven business goal categories](#eleven-business-goal-categories)
- [The quality attribute workshop agenda](#the-quality-attribute-workshop-agenda)

---

## Thirteen categories to mine a requirements document

Significant requirements are never labelled. Work these categories, then **revisit every one asking
what is likely to change** — the anticipated change is separately architecturally significant, and it
is generally absent from the document even when the item itself is present.

1. **Usage** — user roles versus system modes, internationalization, language distinctions.
2. **Time** — timeliness and element coordination.
3. **External elements** — external systems, protocols, sensors or actuators (devices), middleware.
4. **Networking** — network properties and configurations, including their security properties.
5. **Orchestration** — processing steps, information flows.
6. **Security properties** — user roles, permissions, authentication.
7. **Data** — persistence and currency.
8. **Resources** — time, concurrency, memory footprint, scheduling, multiple users, multiple
   activities, devices, energy usage, soft resources (buffers, queues), and scalability requirements.
9. **Project management** — plans for teaming, skill sets, training, team coordination.
10. **Hardware choices** — processors, families of processors, evolution of processors.
11. **Flexibility** — of functionality, portability, calibrations, configurations.
12. **Named technologies and commercial packages** — plus anything known about their planned or
    anticipated evolution.
13. **Anticipated change to any of the above** — run categories 1–12 again through the question
    "what will change here over the system's life?"

---

## Eleven business goal categories

Use each as a conversation-starter with business stakeholders, so coverage can be claimed rather
than hoped for. The prompt shape that works: *"What are our ambitions about <category> for this
product, and how could the architecture contribute to meeting them?"*

1. Growth and continuity of the organization
2. Meeting financial objectives
3. Meeting personal objectives
4. Meeting responsibility to the employees
5. Meeting responsibility to society
6. Meeting responsibility to the state
7. Meeting responsibility to the shareholders
8. Managing market position
9. Improving business processes
10. Managing the quality and reputation of products
11. Managing change in the environment over time

For each important goal, the second half of the exercise is mandatory: have participants name a
quality attribute **and a response measure value** that, if architected in, would help achieve it. A
goal that produces no measure has not been converted into anything usable.

---

## The quality attribute workshop agenda

A facilitated, stakeholder-focused method to generate, prioritize and refine quality attribute
scenarios before the architecture is complete. It emphasizes system-level concerns and specifically
the role software plays in the system. It depends entirely on stakeholder participation — without the
right people in the room it produces nothing.

After introductions and an overview of the steps:

1. **Business/mission presentation.** The stakeholder representing the business concerns — typically
   a manager or management representative — spends about an hour on the system's business context,
   broad functional requirements, constraints, and any known quality requirements. The attributes
   refined later derive largely from what is presented here, so this is not a warm-up.

2. **Architectural plan presentation.** The architect presents the plans as they stand. A detailed
   architecture may not exist; broad system descriptions, context drawings or other partial artifacts
   are enough. The purpose is to let stakeholders see the current architectural thinking, to whatever
   extent it exists.

3. **Identification of architectural drivers.** The facilitators share the driver list they assembled
   from the previous two steps and ask stakeholders for clarifications, additions, deletions and
   corrections. Aim at consensus on a pared-down list covering overall requirements, business drivers,
   constraints and quality attributes.

4. **Scenario brainstorming.** Each stakeholder expresses a scenario representing their own concerns.
   Facilitators ensure every scenario addresses a quality concern by specifying an explicit stimulus
   and response — that check is what stops the list becoming a wish register.

5. **Scenario consolidation.** Ask stakeholders to identify scenarios very similar in content and
   merge those — **but only while the people who proposed them agree and feel their scenarios will
   not be diluted in the process.** Consolidating over someone's objection loses the concern and the
   person.

6. **Scenario prioritization.** Allocate each stakeholder a number of votes equal to **30% of the
   number of scenarios remaining after consolidation**, rounded up. Votes may be allocated any way
   the stakeholder sees fit — all on one scenario, one each across many, or anything between. Count
   the votes and rank accordingly.

   *Worked example:* 40 scenarios survive consolidation → each stakeholder receives 12 votes.

7. **Scenario refinement.** Elaborate the top-ranked scenarios into full six-part form — source,
   stimulus, artifact, environment, response, response measure. As they are refined, issues around
   their satisfaction will surface; record those. This step runs as long as time and resources allow,
   so expect to refine the top few rather than all of them.

### Outputs and what they are for

A list of architectural drivers plus a stakeholder-prioritized set of quality attribute scenarios.
Use them to:

- refine the system and software requirements
- understand and clarify the architectural drivers
- provide the rationale for design decisions made later
- guide the development of prototypes and simulations
- decide the order in which the architecture gets developed

### Participant sizing

For a large, enterprise-critical architecture, expect to enlist **10 to 25 stakeholders** — this is a
rule of thumb and nothing more. Stakeholders include developers, testers, integrators, maintainers,
performance engineers, users, and builders of systems that interact with this one. Their job is to
articulate the specific quality goals the architecture must meet for the system to be considered a
success.
