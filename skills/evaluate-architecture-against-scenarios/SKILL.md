---
name: evaluate-architecture-against-scenarios
description: Walks an architecture's high-priority quality attribute scenarios through its design and reports where it will not deliver. Produces typed findings — risks, non-risks, sensitivity points, tradeoff points — grouped into risk themes mapped to the business goals each threatens. Covers the nine-step stakeholder evaluation (ATAM), the internal peer version running in under a day, and the tactics questionnaire that catches requirements met in letter but defeated in substance. Use when an architecture must be checked against its quality requirements before commitment, when an evaluation or structured design review must be run or scoped, when an inherited system must be assessed against what it claims to be good at, or when a technical risk must reach management in terms it cares about. For a risk matrix by impact times likelihood, risk storming or alignment audits use analyze-architecture-risk; for enforcing agreed rules in a build, govern-architecture-with-fitness-functions.
---

# Evaluating an architecture against its scenarios

Quality attributes are predictable from an architecture *before the system exists*. If certain
architectural decisions are known to produce certain quality attributes, those decisions can be made
deliberately — and afterwards, an examination can confirm whether they were made and predict the
qualities that follow. Without that, designing an architecture would be making largely random
decisions, building, testing, and hoping.

This skill is that examination. It determines the degree to which an architecture is fit for the
purpose intended, by analysing alternatives against prioritized scenarios.

## Findings are the deliverable. Fixing is not.

The output is an identification of the risky portions of the architecture. **Fixing those risks is
explicitly not an output.** Once identified, fixing is its own cost/benefit decision, made by the
people who own the code and the schedule.

This is not timidity. An evaluation that starts proposing and applying fixes loses the independence
that made it worth running, and it quietly takes on decisions that belong to the project.

What the method does insist on: a problem confirmed as real must be **either fixed or explicitly
accepted** by the designers and the project manager. Without that forcing step, a known risk simply
evaporates between the report and the next release.

## The output

```
## Scope and confidence
Artifacts analysed: <what existed, and how mature>
Ceremony: <full stakeholder | internal peer | single-attribute questionnaire>
Scenarios examined: <n of m>, selected by <criterion>

## Findings
Risks         R1..Rn  — decisions that may lead to undesirable consequences
Non-risks     N1..Nn  — decisions analysed and deemed safe
Sensitivities S1..Sn  — decisions with a marked effect on a response
Tradeoffs     T1..Tn  — one decision where two responses move in opposite directions

## Risk themes
<theme> — from R<x>, R<y>, R<z>
  Threatens business goal: <goal as stated by the project>

## Per-scenario records
<one analysis record per scenario examined — see references/finding-record-template.md>

## Accept-or-fix decisions outstanding
R<n> — awaiting explicit decision from <designer / project manager>
```

Stating artifact maturity is not a disclaimer. Accuracy and confidence vary with how mature the
artifacts were, so an early analysis is legitimate — but its confidence must be *reported*, not
implied.

## Procedure

### 1. Settle four contextual factors before starting

Leaving any of these implicit is what makes evaluations go wrong:

- **What artifacts are available?** There must be something that both describes the architecture and
  is readily available. If the system is already operational, architecture recovery and analysis
  tooling can help discover the architecture, find design flaws, and test whether the as-built system
  conforms to the as-designed one.
- **Who sees the results?** Some evaluations run with the full knowledge and participation of all
  stakeholders; others are performed privately. Decide which, before anyone speaks freely under the
  wrong assumption.
- **Which stakeholders will participate?** Identifying the individuals needed and assuring their
  participation is critical, not administrative.
- **What are the business goals?** The evaluation must answer whether the system will satisfy them.
  If they have not been explicitly captured and prioritized beforehand, spend a portion of the
  evaluation doing that — you cannot map risk themes to goals that nobody has written down.

### 2. Size the exercise against exposure

Risk is probability × impact, and the cost of the evaluation must stay below the value it provides.

- **Impact** scales with the system. A system costing millions or billions, or carrying
  safety-critical implications, has large risk impact. A console game costing tens or hundreds of
  thousands has considerably smaller impact.
- **Probability** falls with precedent. Long, deep organizational experience in this domain lowers
  the probability of producing a bad architecture, relative to a first attempt in an unfamiliar one.

Evaluations act like insurance: how much you need depends on your exposure and your risk tolerance.
This is why "we should evaluate more thoroughly" is not automatically the right answer.

### 3. Choose the ceremony

| Ceremony | When | Cost |
|---|---|---|
| **Full stakeholder evaluation** (9 steps, 4 phases) | Unprecedented or high-exposure system; external objectivity needed; evaluators have no prior familiarity with it | ~1–2 days + 2 days + a week of follow-up |
| **Internal peer evaluation** (8-step agenda) | Regular review of what has changed since last time, or a previously unexamined part | Couple of hours to a full day |
| **Single-attribute tactics questionnaire** | One attribute needs auditing; any stage of design, including very early | ~30–90 minutes per attribute |
| **Design peer review** | At a design milestone, like a code review | Several hours to half a day, fixed |

Agendas for all of these are in `references/evaluation-methods.md`.

Evaluators should be highly skilled in the domain and in the attributes under evaluation, and
excellent organizational and facilitation skills are also a must — this is a facilitated exercise,
not a document review.

### 4. Run the four universal steps, whatever the ceremony

1. **Understand the current state of the architecture** — through shared documentation, a
   presentation by the architect, or both.
2. **Determine the drivers** to guide the review. Typically the high-priority quality attribute
   scenarios — **not** purely functional use cases. They may already be documented, or be developed
   by the review team or additional stakeholders.
3. **For each scenario, determine whether it is satisfied.** Two distinct questions: does the
   architecture satisfy *this* scenario, and will any of the *other* scenarios under consideration
   now fail because of decisions in the portion being reviewed? Reviewers may pose alternatives to
   any risky aspect — and those alternatives get the same analysis, not a free pass.
4. **Capture the potential problems** exposed. This list is the basis for follow-up.

### 5. Cap the architecture presentation at one hour

Deliberately. The constraint is the mechanism: requiring the architecture to be presented in an hour
or less produces a presentation that is concise and usually understandable. Treating it as an
administrative nicety and letting it run produces neither.

Expect the module and component-and-connector views, plus context diagrams and the deployment view —
these are useful in almost every evaluation. Other views if they carry information relevant to the
important quality requirements.

A side effect worth noticing: the business goals presented are frequently being seen by some
participants for the first time, and the captured description outlives the evaluation to become part
of the project's record.

### 6. Analyse each high-priority scenario and type every finding

Ask the architect to explain how the architecture supports the scenario, and probe for the
architectural approaches used. Then record findings in five categories — keeping them distinct is
what makes the output actionable rather than a list of worries:

- **Risk** — a decision that may lead to undesirable consequences given the stated requirements.
  These are the primary output and the basis of the mitigation plan.
- **Non-risk** — a decision that, on analysis, is deemed safe. **Record these too**: they document
  what was checked and found sound, which is how a later reader knows the silence was examined.
- **Sensitivity point** — a decision with a marked effect on a quality attribute response.
- **Tradeoff point** — where two or more responses are sensitive to the *same* decision, and one
  improves while the other degrades. A tradeoff presupposes two sensitivities sharing a decision; a
  bare cost is not a tradeoff.
- **Risk theme** — see step 9.

Worked example, on heartbeat frequency:

- The frequency determines the time to detect a fault → **sensitivity**.
- Some frequency assignments produce unacceptable response values → **risks**.
- Higher frequency improves availability but consumes more processing time and communication
  bandwidth, potentially reducing performance → **tradeoff**.

Number findings across the whole evaluation (S1…, T1…, R1…, N1…) so the reasoning text can cite them.

### 7. Keep it back-of-the-envelope — and stop when the inputs are absent

The analysis is **not meant to be comprehensive.** The goal is to elicit enough architectural
information to establish *some* link between the decisions made and the requirements to be satisfied.
A rudimentary analysis that finds the link is the deliverable; an exhaustive one is a different
project.

And when the inputs for an analysis do not exist, say so and stop. If the architect cannot
characterize the number of clients and cannot say how load balancing will be achieved by allocating
processes to hardware, **there is little point proceeding to any performance analysis** — record the
missing precondition as the finding. A confident verdict derived from absent inputs is worse than no
verdict.

For well-known approaches, ask how the architect overcame the approach's known weaknesses, or how
they gained assurance that the approach sufficed. The aim is to be convinced that *this instantiation*
is appropriate for the requirements it targets.

### 8. Scale analysis depth by three factors

- **Importance of the decision** — decisions serving a driving requirement shape critical portions
  and deserve more care.
- **Number of potential alternatives** — more alternatives can absorb more time.
- **Good enough versus perfect** — when two alternatives do not differ dramatically in their
  consequences, it is more important to choose and move on than to be certain the best was chosen.

### 9. Group risks into themes and map them to business goals

Group the discovered risks by common underlying concern or systemic deficiency:

- Several risks about inadequate or out-of-date documentation → a theme that documentation is given
  insufficient consideration.
- Several about inability to function under hardware or software failure → a theme about insufficient
  attention to backup capability or high availability.

A theme can indict the architecture, or the architecture *process and team* — say which.

Then, for each theme, name which of the business goals presented at the start it threatens.

This step is what makes the findings act. What would otherwise look to a manager like an esoteric
technical issue becomes, unambiguously, a threat to something the manager is on record as caring
about. It also closes the loop back to the opening presentation, which gives the exercise closure.

### 10. Compare the architect's view against the stakeholders' — the gap is a finding

If you ran both a utility tree and a stakeholder brainstorm, do not treat them as redundant:

- The **utility tree** shows how the *architect* perceived and handled the drivers.
- The **stakeholder brainstorm** takes the pulse of the wider community: what system success means to
  *them*. A maintainer proposes a modifiability scenario; a user proposes ease of operation; a QA
  person proposes replicating the state leading up to a fault.

Compare the two prioritized lists. Agreement indicates good alignment. Additional driving scenarios
usually turn up — and **a large discrepancy is itself a risk to record**, because it means the
stakeholders and the architect disagree about the system's important goals.

This is why the two exercises must not be collapsed into one to save time.

## Decision rules

**Ask how a tactic is realized, never whether the requirement is met.** A requirement can be strictly
satisfied by a mechanism that provides none of its intent. One healthcare system had a requirement
that no data pass over the network in the clear, and satisfied it by XOR-ing all data before sending
— nothing went in the clear, and the result could be cracked by a schoolchild with modest ability.

A bare "Y" in a supported column would have passed that system. So the mechanism and rationale
columns of a tactics questionnaire are mandatory, not optional: record the specific decisions, where
they are or will be located in the code base, the risk of using or not using the tactic, and the
rationale including implications for cost, schedule and evolution. **Record the risk of *not* using a
tactic as well as using it.**

**The architect must willingly participate.** This is the cardinal rule. An evaluation conducted over
the architect's objection is not this method being applied, whatever it is called.

**Internal teams are less objective — use that knowledge deliberately.** A peer team hears fewer new
ideas and fewer dissenting opinions, which may compromise the value of the results. Outside evaluators
are less likely to fear raising sensitive problems, or problems invisible because of organizational
culture or "we've always done it that way". And — whether justified or not — managers tend to listen
more to problems found by an expensive outside team than to their own staff. If a known problem needs
management attention, an external evaluation is the instrument. This is understandably frustrating for
staff who have raised the same problem for months; acknowledge it rather than pretending otherwise.

**If there is no architecture to evaluate, continue anyway.** Discovering that what exists is a stack
of class diagrams or vague text masquerading as an architecture does not abort the exercise. The
deliverables become the articulated set of quality attributes, a whiteboard architecture sketched
during the session, and a set of documentation obligations for the architect — repeatedly enough to
justify the exercise. Related: if the architecture under review turns out to have been superseded by
one nobody mentioned, back up to the architecture presentation; the business goals, utility tree and
scenarios all remain valid.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| The report is a list of worries | Findings not typed | Separate risks, non-risks, sensitivities, tradeoffs, themes |
| Management ignores the findings | Risks left as technical issues | Group into themes; map each to a business goal on record |
| Requirement passed review; the mechanism was worthless | Asked whether met, not how realized | Ask for the mechanism and the assurance behind it |
| Confident performance verdict from nothing | Analysis run without its inputs | Stop; record the missing precondition as the finding |
| Evaluation found only what the architect already knew | Architect's own tree used as the sole source | Brainstorm with stakeholders separately; treat divergence as a risk |
| Evaluation ran long and delivered late | Ceremony mismatched to exposure | Choose ceremony by exposure; cap the presentation at an hour |
| A known risk silently disappeared | No explicit accept-or-fix decision | Force explicit acceptance by designers and project manager |
| "Everything looks fine" with nothing recorded | Non-risks not written down | Record non-risks; silence and safety are different claims |
| Report implies more confidence than the artifacts supported | Artifact maturity not stated | State what you analysed and how mature it was |

## References

- `references/evaluation-methods.md` — the nine-step stakeholder method with phases, durations, team
  roles and participant counts; the eight-step internal peer agenda; and the four-step tactics-based
  questionnaire. Read at step 3, once you know the ceremony.
- `references/finding-record-template.md` — the per-scenario analysis record and the findings
  numbering convention. Read at step 6.

To walk a tactics-based questionnaire you need the attribute's tactic list; the catalog lives in
`select-quality-attribute-tactics`.
