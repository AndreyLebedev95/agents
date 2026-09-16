---
name: elicit-and-prioritize-asrs
description: Discovers the quality requirements that actually shape an architecture and ranks them, when the spec lacks them and stakeholders cannot state them. Mines a spec against thirteen categories of significant information, runs the stakeholder workshop with its 30-percent voting rule, converts business goals into quality requirements, brackets an unstatable target by proposing absurd values, and builds the utility tree rating each requirement on business value against technical risk. Use when design must start before requirements settle, when a spec must be mined for what is architecturally significant, when a stakeholder says "I don't know what that requirement should be", when business goals must become technical requirements, or when someone asks which requirements are architecturally significant. Siblings — write-quality-attribute-scenarios, select-quality-attribute-tactics, evaluate-architecture-against-scenarios. For characteristic names with an unranked top three, use elicit-architecture-characteristics.
---

# Eliciting and prioritizing architecturally significant requirements

An **architecturally significant requirement** is one that will have a profound effect on the
architecture — the architecture might well be dramatically different in its absence. You cannot
design a successful architecture without knowing these, and they are almost never handed to you.

Note what "requirements" means here: the set of properties that, if unsatisfied, will make the
system a failure. Whether anyone documented them is a separate question, and usually the answer is
no.

## The admission test

A requirement qualifies only if **both** hold:

1. **Profound impact on the architecture** — including it would likely produce a different
   architecture than omitting it.
2. **High business or mission value** — because satisfying it may come at the expense of not
   satisfying others, it has to matter to important stakeholders.

Significant requirements often but not always take the form of quality attribute requirements. The
more *difficult* and the more *important* a quality requirement is, the more likely it qualifies.

## The output

```
## Architecturally significant requirements
<ID> <one-line statement>
     source: requirements document <section> | stakeholder <role> | business goal <n>
     impact: <what would be structurally different without this>
     value:  <whose success depends on it>

## Utility tree
Utility
├── <Quality attribute>
│   └── <refinement relevant to this system>
│       ├── <scenario> (business value H/M/L, technical risk H/M/L)
│       └── <scenario> (…, …)

## Gaps and assumptions
<unresolved item> — needs <who decides>
<assumption made> — because <stakeholder unavailable / not yet decided>

## Stakeholders not reached
<role> — <what they would have been asked about>
```

The last two sections are load-bearing. A prioritized list that hides which stakeholders never spoke
invites everyone to treat it as settled when it is not.

## Procedure

### 1. Mine whatever document exists — then mine it again for change

The obvious place to look is the requirements document or the user stories. Look there, but expect
two specific failures rather than being surprised by them:

- **Most of the content does not affect the architecture.** The bulk of a typical specification
  covers features and functionality, which shape the architecture least.
- **Much of what you need was never an observable of the specified system**, so it was never in
  scope for the document at all. Requirements deriving from the development organization's own
  business goals, developmental qualities like teaming assumptions, and — in an acquisition context
  — anything representing the *developer's* interests rather than the acquirer's.

Significant requirements are never labelled as such, so this is archaeology. Work the thirteen
categories in `references/elicitation-checklists.md`.

Then do the step almost everyone skips: **revisit every category asking what is likely to change
over time.** The anticipated change to an item is separately architecturally significant, and it will
not be in the document even when the item itself is.

Where you find "the system shall be modular" or "shall exhibit high usability" or "shall meet users'
performance expectations" — these are not requirements, because they are not falsifiable. Treat each
as an invitation to start a conversation, and hand it to `write-quality-attribute-scenarios`.

### 2. Interview stakeholders as a co-author, not a recipient

Stakeholders frequently do not know what their quality requirements are. This is not obstruction and
no amount of nagging will instil the insight. You are expected to help set them, and projects that
recognize this collaboration are much more likely to succeed than those that do not.

What you uniquely bring:

- **Comparative experience** — which responses similar systems have actually exhibited, and which
  are reasonable to expect here.
- **Fast feasibility feedback** — which responses are straightforward, which are problematic, which
  are prohibitive.
- **A price** on the expensive ask. A stakeholder asking for 24/7 availability is not being
  unreasonable; they just have not seen the bill. Showing the cost lets them trade availability
  against affordability, which is a decision only they can make.
- **The upside.** You are the only person in the conversation who can say "I can deliver an
  architecture that will do better than what you had in mind — would that be useful?" Ask it.

**Do not insist on precise quantitative targets.** If you insist, you will get numbers, and they
will be arbitrary; some will be difficult to satisfy and will actively detract from the system's
success. A range you trust beats a number you extracted.

### 3. When a stakeholder cannot state a target, bracket it

"I don't know what that requirement should be" is usually true as a feeling and false as a fact,
especially for someone experienced in the domain. Eliciting the something they do know beats
inventing the number yourself.

Play dumb and walk down from an absurd value:

> — How quickly should the system respond to this transaction request?
> — I don't know.
> — So… 24 hours would be fine?
> — No!
> — An hour?
> — No!
> — Five minutes?
> — No!
> — Ten seconds?
> — …I suppose I could live with something like that.

Stop at the first grudging acceptance. That brackets the requirement, and a range is enough to
choose mechanisms — 24 hours versus 10 minutes versus 10 seconds versus 100 milliseconds mean
entirely different architectural approaches.

### 4. Run the workshop when stakeholders can be assembled

A facilitated, stakeholder-focused session that generates, prioritizes and refines quality scenarios
before the architecture is finished. The agenda and the voting arithmetic are in
`references/elicitation-checklists.md`. Two details that carry the method:

- **Consolidate only with consent.** Merge similar scenarios only while the people who proposed them
  agree and feel their scenario will not be diluted.
- **Each stakeholder gets votes equal to 30% of the post-consolidation scenario count**, spendable
  however they like — all on one scenario, spread across many, anything between.

### 5. Elicit business goals explicitly, against categories

Business goals are the reason the system is being built, and they frequently lead directly to
significant requirements. Architects usually absorb them by osmosis. Osmosis has its merits, but
capture them explicitly, because they imply requirements that otherwise go undetected until it is too
late or too expensive to address them.

Hold a session with the architect and key business stakeholders:

1. **Elicit** the important goals, using the eleven categories as conversation-starters so you can
   claim coverage rather than hope for it. Elaborate each as a structured scenario, consolidate
   near-duplicates, and have participants prioritize.
2. **Convert.** For each important goal, have participants name a quality attribute *and a response
   measure value* that, if architected in, would help achieve it.

Use each category as a prompt: "What are our ambitions about market share for this product, and how
could the architecture contribute to meeting them?"

### 6. Classify each business goal by how it touches the architecture

Three relationships, and the middle one is why this step exists:

1. **The goal leads to a quality requirement.** Every quality requirement originates in some higher
   purpose describable as added value. Wanting to differentiate from competitors and capture market
   share may produce what looks like an unreasonably fast response-time requirement. Knowing the goal
   behind a stringent requirement lets you question it meaningfully — or marshal the resources to
   meet it.
2. **The goal affects the architecture while inducing no quality requirement at all.** No
   requirements specification captures these, and no manager would allow the motivation to be written
   down. An architect once presented a draft; the manager insisted a database be added — not for any
   technical reason, but because the organization had a database unit of highly paid staff who were
   unassigned and needed work. An architecture delivered without it would have been just as deficient,
   from that manager's point of view, as one missing an important function.
3. **No architectural influence.** "Reduce cost" might be realized by lowering the thermostat.

Hunt case 2 deliberately. It is invisible to every requirements process and it is the reason
technically sound designs get rejected for reasons nobody can point at.

### 7. Build the utility tree and rate every leaf

When the primary sources are unavailable — which is common, for ordinary organizational reasons —
the architect records what they believe the critical requirements to be, top-down:

- **Root:** `Utility` — the overall goodness of the system.
- **Level 2:** the major quality attributes the system must exhibit. Bare attribute names are
  acceptable *here and nowhere else*, because they are explicitly placeholders pending refinement.
- **Level 3:** refinements relevant to *this* system. Performance might become "data latency" and
  "transaction throughput", or "user wait time" and "time to refresh web page". Choose the ones that
  fit your system, not a standard breakdown.
- **Leaves:** the specific requirements, written as full six-part scenarios.

Then rate each leaf on two axes, H/M/L each:

| | H | M | L |
|---|---|---|---|
| **Business value** | A must-have | Important, but its omission would not fail the project | Nice to have, not worth much effort |
| **Technical risk** | Keeps you awake at night | Concerning, but not high risk | You are confident you can meet it |

`references/utility-tree-example.md` has a worked tree to imitate.

### 8. Run the two checks on the finished tree

- **An attribute or refinement with no scenario under it** is not necessarily an error or an omission
  to rectify. It is a signal to go and investigate whether there are unrecorded scenarios in that
  area.
- **(H,H) leaves deserve the most attention** — they are the most significant of the significant
  requirements. But a *very large number* of (H,H) leaves is itself a finding: it is cause for concern
  about whether the system is achievable at all. Say so rather than presenting it as a work plan.

### 9. Hunt the implicit, and confirm ownership

Two sweeps that catch expensive misses:

- **Implicit requirements.** Ask what this domain takes for granted. Every system has performance
  requirements even when none are expressed — a word processor may state none, yet waiting a second
  to see a typed character appear is plainly unacceptable. Absence of a stated requirement is a gap
  to fill, not evidence that the attribute does not matter.
- **Ownership.** You may not be responsible for every quality requirement. When a stakeholder omits
  an attribute you expected, question the omission — but accept an answer that names a real
  non-software control, and record it as a stated assumption about the environment rather than as a
  gap.

### 10. Keep the channel open, and get ahead of change

Requirements change constantly whether captured or not, so apply these methods repetitively rather
than once. Better than keeping up is staying a step ahead: when you get wind of a coming change,
take preliminary design steps for it as an exercise to understand the implications. If it will be
prohibitively expensive, say so early — that is a valuable contribution in itself. More valuable
still is proposing the change that would do almost as well against the goal without breaking the
budget.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| The requirements list is all features | Document mined without the category checklist | Work the thirteen categories, then their anticipated change |
| A stakeholder's number later proved arbitrary and costly | Quantitative target demanded rather than bracketed | Play dumb; take the accepted range |
| A design is rejected for a reason no requirement mentions | A business goal shaped the architecture without inducing a requirement | Elicit goals explicitly; classify all three ways |
| Everything is high priority | Single-axis ranking, or none | Rate business value and technical risk separately |
| The domain's critical attribute was never mentioned | Implicit requirement everyone assumes | Ask what the domain takes for granted; confirm ownership |
| Tree is full of (H,H) leaves and presented as a plan | Infeasibility read as ambition | Report it as a finding about achievability |
| The list goes stale within a month | Channel closed after handoff | Apply the methods repetitively; stay a step ahead |
| Attribute names sit at the leaves | Tree never refined to scenarios | Leaves must be scenarios; names are placeholders only |

## References

- `references/elicitation-checklists.md` — the thirteen requirements-document categories, the eleven
  business goal categories, and the workshop agenda with its voting arithmetic. Read at step 1, 4
  or 5.
- `references/utility-tree-example.md` — a worked utility tree across seven attributes with rated
  scenario leaves. Read at step 7.
