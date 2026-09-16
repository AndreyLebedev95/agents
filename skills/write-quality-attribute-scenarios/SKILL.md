---
name: write-quality-attribute-scenarios
description: Turns an untestable quality requirement into a concrete six-part scenario — source, stimulus, artifact, environment, response, response measure — so it can be designed for and falsified. Supplies parameter tables for ten attributes so stakeholders tailor a scenario rather than invent one. Use whenever a requirement names an "-ility" with no number, when someone asks for "five nines" or "lightning fast" or "real-time", when a spec lists features but no quality requirements, when an attribute needs a response measure or pass/fail threshold, when acceptance criteria are needed for a performance, availability or security requirement, or when a team argues whether something is "really" a performance or an availability problem. Use it even when the ask is only "how would we test this requirement". Siblings — elicit-and-prioritize-asrs (ranking), select-quality-attribute-tactics (design), evaluate-architecture-against-scenarios (audit), model-a-new-quality-attribute (uncatalogued).
---

# Writing quality attribute scenarios

A quality attribute is a measurable or testable property of a system, used to indicate how well it
serves its stakeholders beyond its basic function. Measurability is in the definition. So a quality
attribute requirement that nobody can measure is not a weak requirement — it is not a requirement.

This skill converts stated wishes into six-part scenarios that a designer can target and a tester
can falsify.

## Why the bare adjective fails

"The system shall be modifiable" says nothing. Every system is modifiable with respect to one set
of changes and not modifiable with respect to another. The same holds across the board: a system is
robust against some faults and brittle against others, secure against some attacks and open to
others. There is no fix that keeps the sentence and adds rigor — the sentence has to be replaced by
a scenario with a context and a number.

Treat every such sentence as an invitation to start a conversation, not as a requirement you have
received. That reframing is the whole job.

## The output

For each requirement, produce this:

```
## <short name>
Source:            <the entity that generated the stimulus>
Stimulus:          <the event arriving at the system or the project>
Artifact:          <the precise target — not "the system">
Environment:       <the state or mode the scenario occurs in>
Response:          <what the system, or the developers, do about it>
Response measure:  <the number that decides whether this was achieved>
```

Then, separately:

```
## Unresolved
<part that could not be filled> — needs <who or what decides it>

## Discharged outside the software
<attribute> — <the non-software control that covers it, and the assumption this creates>
```

The unresolved list is not a failure. A scenario with an honest gap is more useful than one with an
invented number, because the gap has an owner and the invented number does not.

## Procedure

### 1. Refuse the categorization argument

If the discussion is about which attribute a concern belongs to — is a denial-of-service attack an
availability problem, a performance problem, a security problem or a usability problem? — stop it.
Every claimant is partly right, and the argument produces no design. The scenario form is
deliberately insensitive to category, so writing the scenario dissolves the question.

Related trap: the specialist communities each have their own word for the same arriving occurrence.
Performance says "event", security says "attack", availability says "fault", usability says "user
input". These frequently describe one occurrence in four vocabularies. Translate each into
"stimulus" before concluding you have four separate requirements.

### 2. Decide whether the attribute is runtime or development-time

This decides who performs the response and in what units it is measured, so get it right early.

- **Runtime** — availability, performance, security, safety, usability, energy efficiency. The
  system performs the response; measures are in time, rate, percentage, resource usage.
- **Development-time** — modifiability, testability, deployability, integrability. *The developers*
  perform the response; measures are in effort, labor, elapsed calendar time, artifacts touched,
  defects introduced.

A modifiability response is "the developers implement the modification without side effects, then
test and deploy it", measured in person-days. Writing it in milliseconds is a category error that
survives review surprisingly often.

### 3. Tailor a general scenario; never hand over a blank page

Read `references/general-scenarios.md` and pull the parameter table for the attribute in question.
Present its parts with their candidate values and have the stakeholder substitute system-specific
ones.

This ordering matters more than it looks. Tailoring an existing scenario is far easier for a
stakeholder than generating one from nothing, and asking someone to invent a scenario from thin air
is the most common reason elicitation stalls.

### 4. Fill all six parts, and fight for environment and artifact

Four parts get filled almost automatically: source, stimulus, response, response measure. Two get
dropped: **environment** and **artifact**. They are also the two that make a requirement
discriminating rather than generic.

- **Environment** — which mode or state? Normal operation, startup, shutdown, overload, degraded
  operation, repair mode. Or states where the system is not running at all: in development, in
  testing, refreshing its data, recharging between runs. Also: before or after code freeze? First
  failure of a component, or the fifth successive failure? These get treated differently, and if
  your requirement does not say which one it means, it cannot be argued with.
- **Artifact** — refuse "the system". A failure in a data store is treated differently from a
  failure in the metadata store. Modifications to the user interface may warrant faster response
  times than modifications to the middleware. Name the part.

A requirement that applies equally to every system and every state is a requirement nobody can fail.

One or two parts may legitimately be omitted early on. The value of knowing all six exist is that
you decide whether each is relevant, rather than skipping it silently.

### 5. Where the spec has functions but no quality requirements, annotate the functions

Quality attributes do not stand alone; they pertain to the functions. So when handed a feature list
with no quality requirements, do not start over — convert the list into elicitation prompts.

Take "when the user presses the green button, the Options dialog appears", then add:

- a performance annotation: how quickly does the dialog appear?
- an availability annotation: how often may this function fail, and how quickly is it repaired?
- a usability annotation: how easy is this function to learn?

Repeat for each attribute that matters for that function. This turns an existing document into a
source of requirements instead of an obstacle.

### 6. Write the response measure in the attribute's own units

Use the measurement vocabulary from `references/general-scenarios.md`. Some rules that catch most
errors:

- **Include the legitimate failure responses, not only success.** A performance scenario's valid
  responses include returning an error, generating no response, ignoring the request when
  overloaded, changing mode or level of service, and servicing a higher-priority event. A scenario
  that only permits success is incomplete and will be "met" by a system that drops load.
- **Pair latency with a load figure.** A response time with no concurrency or arrival figure is
  unmeasurable. Classify arrival as periodic (predictable interval), stochastic (per a probability
  distribution) or sporadic (neither) — this is the language performance scenarios are written in.
- **Convert vernacular targets into real time.** "Five nines" is 5 min 15 sec of downtime per year.
  Stakeholders frequently do not know that. The table is in the reference file.
- **Availability excludes scheduled downtime only if the agreement says so.** Confirm; do not
  assume. Where it is excluded you get the genuinely odd but correct situation where the system is
  down, users are waiting, and no availability requirement is violated.
- **Energy efficiency measures need a functionality floor.** "Energy saved" alone is trivially
  satisfiable by switching things off. State the level of functionality and the acceptable levels of
  other attributes that must be maintained while saving it.
- **When no threshold can be named but the cost of failure can**, use risk exposure —
  size(loss) × prob(loss) — as the measure. This lets a requirement be stated as a reduction in
  expected loss instead of an activity count, and it is a real measure, not a dodge.

### 7. Record what you could not fill, and who owns it

Two distinct cases, and they are not the same finding:

- **Unresolved** — nobody has decided yet. Name the part and the decision-maker.
- **Discharged outside the software** — the attribute is genuinely covered by something that is not
  your architecture. This is legitimate: a concern that looks glaringly absent may be fully handled
  by a non-software control. When a stakeholder omits an attribute you expected, question the
  omission; if the answer names a real external control, record it as a stated assumption about the
  environment rather than as a gap.

  Record it, because the assumption is the *environment* part of the scenario doing the work. An
  air-gapped system behind physical security has no software security requirement until the day
  someone networks it, at which point the requirement reappears and nobody remembers why it wasn't
  there.

Also separate what the architecture can deliver from what process must deliver. A strong security
architecture is worthless if people fall for phishing or choose weak passwords. Saying which half is
which prevents both false blame on the design and false confidence in it.

## Vocabulary that changes what you write

**Fault, error, failure.** A failure is a deviation from specification that is *externally visible*.
Its cause is a fault. The states in between are errors. If code containing a fault executes and the
system recovers with no observable deviation, no failure occurred. Apply the observability
criterion: if a failure *could* have been observed, it is a failure, whether or not anyone observed
it. And define time-to-repair as time until the failure is no longer observable — which might be an
imperceptible delay, or the time for an engineer to fly to a remote mine site.

**Availability against its neighbours.** Availability is reliability plus recovery, and it subsumes
robustness and anything else involving a notion of unacceptable failure — so do not track those
separately without saying how they differ. It is distinct from security (though a denial-of-service
attack is designed to destroy availability), from performance (it can be genuinely hard to tell a
failed system from an egregiously slow one), and from safety (which is about staying out of a
hazardous state and limiting damage on entering one).

**Scalability is a kind of modifiability.** It is making the system easy to change in one particular
way. Write it twice — once as a performance scenario, once as a modifiability scenario — because a
performance-only scenario misses the cost-of-change measures that are usually the real constraint.

**Say "responsibilities", not "functional requirements".** The functional/non-functional split does
not survive contact with real systems: requiring a username and password is plainly a computation
the system performs, yet is the purpose of no system, and engine control cannot be implemented
correctly without timing behavior. Once you say "this set of responsibilities", three questions
become answerable — what are its timing constraints, what modifications are anticipated for it, and
which class of users may execute it.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| The requirement would apply to any system | Environment and artifact left blank | Fill both; name the mode and the precise target |
| Team debating which attribute owns an issue | Categorization mistaken for analysis | Write the scenario; concede all claimants are partly right |
| One occurrence logged as several requirements | Each community used its own word for one stimulus | Translate to "stimulus", then dedupe |
| Modifiability measured in milliseconds | Development-time attribute treated as runtime | Developers perform the response; measure effort |
| Scenario only describes success | Failure responses omitted | Add error, no response, ignore-if-overloaded, degraded mode |
| A latency target with no load figure | Arrival pattern never characterized | Classify periodic / stochastic / sporadic; state the load |
| "The system shall be modular" passed review | Untestable sentence accepted as a requirement | Treat it as the start of a conversation |
| Energy target met by disabling the feature | No functionality floor | State the functionality and other attributes to maintain |

## Reference

`references/general-scenarios.md` — six-part parameter tables for the ten catalogued attributes,
plus the availability percentage-to-downtime table. Read it in step 3 whenever you are writing a
scenario for any of those attributes, and in step 6 for the measurement vocabulary. For an attribute
that is *not* in that file, use `model-a-new-quality-attribute` to build its scenario form first.
