---
name: model-a-new-quality-attribute
description: Builds the specification-and-design portfolio for a quality attribute no standard catalog covers — an invented or organization-specific concern, or one measuring the architecture itself. Captures concrete scenarios from the stakeholders whose concern created the need, generalizes them into a general scenario, builds a parameter model whose closed parameter list is what gives it power, and derives a finite tactic list from those parameters. Also covers why standard attribute lists work only as checklists and never as taxonomy, attributes of an architecture itself such as buildability and conceptual integrity, and inheriting a physical system's attributes for embedded software. Use when a stakeholder concern has no standard definition, when a team argues whether something is a real quality attribute or a sub-quality of another, when a published list lacks the concern that matters, or when someone asks how to measure something unmeasurable. For the ten catalogued attributes use write-quality-attribute-scenarios.
---

# Modelling a new quality attribute

The well-known quality attributes each come with a portfolio: a definition, a general scenario, and a
collection of techniques for achieving them. Those ten only begin to scratch the surface of what a
real system might need.

This skill builds the same portfolio for an attribute that has none — "manageability",
"buildability", "observability", "development distributability", or a word your organization made up
last quarter and genuinely cares about.

## First: stop the taxonomy argument

Quality attribute names, by themselves, are largely useless. At best they are invitations to begin a
conversation.

So when a team is arguing about whether *portability* is really a kind of *modifiability*, or whether
*functional correctness* belongs under *reliability*, or whether *maintainability* contains
*modifiability* or the reverse — that effort is close to wasted and should be spent elsewhere. The
published standards spent real time on these questions and still landed somewhere arbitrary:
`references/attribute-catalogs.md` documents where.

Attributes are also not a taxonomy, however much the lists claim to be. A taxonomy requires every
member to sit in exactly one place, and attributes refuse: a denial-of-service attack belongs to
security, availability, performance *and* usability simultaneously, and all four communities are
partly right.

The way out is not a better name. It is a scenario.

## The output

```
## <attribute name> — working definition
<what it means for this organization, in one sentence>
Sub-attributes: <the refinements you decomposed it into>

## Concrete scenarios
<6-part scenarios gathered from stakeholders>

## General scenario
| Part | What it is | Candidate values |
(each part generalized from the concrete instances above)

## Model
<attribute> is a function of:
  1. <parameter> — moved by: <architectural decisions>
  ...
These are the only parameters that affect <the response> within this model.

## Tactics
<tactic> — affects <parameter> — costs <other attribute>
```

The closure claim in the model section is not boilerplate. It is the thing that makes the model worth
having, and if you cannot make it honestly, say what the model does not cover.

## Procedure

### 1. Capture concrete scenarios first

Interview the stakeholders whose concerns created the need for this attribute — individually or as a
group.

Work with them to build **attribute characterizations** that refine what the attribute means. Do this
in your own words; there is no authority to defer to. Example: development distributability decomposes
into *software segmentation*, *software composition* and *team coordination*.

Then craft specific, concrete scenarios that capture what they mean. Concrete first — the temptation
is to define the attribute abstractly and derive scenarios from the definition, and it produces a
definition nobody can apply.

### 2. Generalize the collection into a general scenario

Once you have a set of concrete scenarios, look across them: the set of stimuli you collected, the
set of sources, the set of responses, the set of response measures, the artifacts, the environments.

Construct the general scenario by making **each of the six parts a generalization of the specific
instances you collected**. That is the whole operation — the general scenario is not invented, it is
abstracted from real instances, which is why step 1 comes first.

Use the table shape from `write-quality-attribute-scenarios` so the result drops into the same
workflow as the catalogued attributes.

### 3. Find or build a model

By "model" nothing elaborate is meant: just **an understanding of the set of parameters the attribute
is sensitive to, and the set of architectural characteristics that influence those parameters.**

Find one if it exists — much cheaper than building one. Otherwise derive the parameters from your
scenarios: from the stimuli and their sources, the responses and their measures, the artifacts and
their properties, the environment and its characteristics.

Worked models to imitate:

- **Modifiability** is a function of how many places in the system must change in response to a
  modification, and the interconnectedness of those places.
- **Throughput** is a function of transactional workload, the dependencies among the transactions, and
  how many transactions can be processed in parallel.
- **Latency**, in a generic queuing model, is a function of exactly seven parameters: arrival rate,
  queuing discipline, scheduling algorithm, service time, topology, network bandwidth, routing
  algorithm.
- **Integration difficulty** is a function of *size* — the number of potential dependencies — times
  *distance* — the difficulty of resolving differences at each dependency, which itself decomposes
  into syntactic, data-semantic, behavioral-semantic, temporal and resource distance.

### 4. Close the parameter list, and say so out loud

Two claims make a model useful, and they are separate:

- **"These are the only parameters that can affect the response within this model."** This is what
  gives a model its *power*. An open-ended parameter list bounds nothing and predicts nothing.
- **"Each parameter can be moved by architectural decisions."** This is what makes it useful *to an
  architect*. In the queuing model: the routing algorithm can be fixed or load-balancing, a scheduling
  algorithm must be chosen, the topology can change by dynamically adding or removing servers.

State both explicitly. If you cannot honestly close the list, scope the model down until you can, and
name what falls outside it — a small honest model beats a large vague one.

### 5. Derive the tactics from the parameters

Now the design problem becomes tractable:

1. **Enumerate the model's parameters.**
2. **For each parameter, enumerate the architectural characteristics — and the mechanisms achieving
   them — that can affect that parameter.**

Four ways to source those mechanisms:

- Revisit a body of mechanisms you already know, and ask of each one how it affects this parameter.
  (The existing tactic catalogs are exactly such a body — start there.)
- Search for designs that have successfully dealt with this attribute. Search on the name you gave
  the attribute, **and also on the sub-attribute terms you coined in step 1** — those often match
  published work where your coined name does not.
- Search publications and blog posts on the attribute and try to generalize their observations and
  findings.
- Find experts in the area and interview them, or simply write and ask for advice.

### 6. Check the result is finite and small

It will be, and this is the payoff: the number of parameters is bounded and, for each parameter, the
number of architectural decisions affecting it is limited. So the mechanism list comes out finite and
reasonably small.

If your tactic list is sprawling or arbitrary, the fault is upstream — the parameters were not closed
in step 4, or the tactics were invented rather than derived.

This is also the method by which the published tactic sets were themselves produced. Which means they
are extensible and correctable the same way, rather than closed lists to be deferred to.

## Using standard attribute lists

Use them as **checklists**, never as structure.

Good for: confirming no important stakeholder need was overlooked, and — more usefully — as the seed
for your own checklist of the attributes of concern in your domain, your industry, your organization,
your products. They can also seed the search for measures, though the names themselves give little
clue how to measure anything. If "fun" turns out to matter in your system, no list tells you how to
know whether you have enough of it.

Three drawbacks to expect:

1. **No list will ever be complete.** You will inevitably be asked to design for a stakeholder
   concern no list-maker foresaw.
2. **Lists generate more controversy than understanding.** See the taxonomy argument above.
3. **They purport to be taxonomies** and are not.

And do not fool yourself that a checklist removes the need for deeper analysis. It tells you what to
ask about, not what the answer is.

## Attributes that measure the architecture itself

A category routinely left out of requirements entirely, because it is about neither the running system
nor the development project:

- **Buildability** — how well the architecture lends itself to rapid, efficient development. Measured
  by the cost, in money or time, to turn the architecture into a working product meeting all its
  requirements.
- **Conceptual integrity** — consistency in the design, demanding that the same thing be done the same
  way throughout. **Less is more.** There are countless ways components can send information to each
  other — messages, data structures, event signalling — and an architecture with conceptual integrity
  features a small number of them, providing alternatives only where there is a compelling reason.
  Likewise all components should report and handle errors the same way, log events the same way,
  interact with the user the same way, sanitize data the same way.
- **Marketability** — some architectures carry meaning independent of the qualities they bring, and
  the *perception* of an architecture can be at least as important as its actual properties. Many
  organizations have felt compelled to build cloud-based or microservice-based systems whether or not
  that was the correct technical choice. When this is a real driver, **name it as one**, rather than
  letting it operate disguised as a technical argument — an undisclosed marketability requirement
  produces a technical debate nobody can win.

## Two special cases worth knowing

**Development distributability.** Where globally distributed teams build the system, the binding
constraint is coordination. Design so that coordination among teams is minimized — major subsystems
exhibiting low coupling — and achieve that **for the data model as well as the code**. The cost driver
is negotiation: teams working on modules that communicate may need to negotiate those interfaces, and
when one module is used by many others each owned by a different team, communication and negotiation
become disproportionately burdensome. So **the architectural structure and the social and business
structure of the project need to be reasonably aligned.** Scenarios for this attribute concern the
compatibility of the system's communication structures and data model with the coordination mechanisms
of the organizations doing the development.

**Embedded software inside a physical system.** Physical systems are designed to meet their own litany
of attributes — weight, size, electric consumption, power output, pollution output, weather
resistance, battery life. Trace the influence both ways:

- *Outward:* software using computing resources inefficiently may require more memory, a faster
  processor, a bigger battery, or an additional processor — which adds power consumption, weight,
  physical profile and expense to the whole system.
- *Inward:* software performance is fundamentally constrained by the processor that runs it. No amount
  of design will usefully run a whole-earth weather model on an ageing laptop.

Also check whether a **non-software control is the effective one**: physical security is probably more
important and more effective than software security at preventing fraud and theft. Understand the
attributes important for the entire system, work with the system architects and engineers rather than
optimizing the software in isolation, and introduce the scenario technique to them if they are not
already using it — it works unchanged on system attributes.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Weeks spent deciding whether X belongs under Y | Taxonomy mistaken for specification | Refuse the argument; write scenarios instead |
| The model has an open-ended parameter list | Parameters never closed, so nothing is bounded | State the closure claim, or scope the model down until you can |
| The tactic list is sprawling or arbitrary | Tactics invented rather than derived from parameters | Derive from the parameter list; use the four sources |
| The attribute is named but still unmeasurable | Generalized before enough concrete scenarios existed | Gather concrete scenarios first; generalize from instances |
| A standard list adopted wholesale; the real concern still missing | Checklist treated as the definition of the space | No list is complete; keep your own domain checklist |
| Embedded software optimized while the whole system got worse | System-level attributes never inherited | Work with the system engineers; trace outward and inward |
| A technical debate nobody can win | An undisclosed marketability or perception requirement | Name it as a requirement so it can be traded off openly |

## Reference

`references/attribute-catalogs.md` — the eight product-quality characteristics of the main published
standard along with its documented inconsistencies, the named non-catalog attributes, and the
physical-system attribute list. Read it at step 1 when checking coverage, and never as a source of
structure.
