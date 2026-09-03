---
name: record-architecture-decisions
description: Analyzes an architecture decision honestly and records it so it survives. Covers the trade-off method — enumerate options, hunt the disadvantages of the front-runner, build the matrix, then weight the factors for this context — the three decision antipatterns, what makes a decision architecturally significant, the full ADR structure with supersession trails, using ADRs as documentation and as the filter for proposed standards, diagramming conventions, and what generative AI can and cannot contribute. Use whenever a choice between credible options must be made or justified, when a team keeps relitigating something already decided, when a decision needs documenting or approving, when someone asks how to write an ADR or whether a choice is architectural or merely technical, when a standard is being proposed, when reconstructing why an inherited system is the way it is, or when an architecture must be diagrammed or presented. Use it even when the ask is just "which of these two should we use, and why". For the conversation that gets a decision accepted over an objection use negotiate-architecture-decisions; for choosing among styles use choose-architecture-style; for assessing risk across a whole architecture use analyze-architecture-risk.
---

# Recording architecture decisions

Everything in architecture is a trade-off. If a choice appears to have no downside, the downside has not been found yet — and trade-off analysis cannot be performed once and reused as a standing default, because each situation changes the variables.

Two consequences follow, and they shape everything here.

**Why beats how.** An experienced practitioner can reconstruct how an unfamiliar architecture works by reading it, but cannot reconstruct *why* it was built that way. The reasoning — the trade-offs weighed, the alternatives rejected — is the part that is lost, so it is the part that must be written down. Every trade-off analysis generates a great deal of context that does not appear in the resulting solution.

**Most decisions are not binary.** They sit on a spectrum between extremes. This is why comprehensive definitions in this field are so hard to write, and it yields a useful test: **an architecture decision is one where each of the options carries significant trade-offs.**

## The output

A decision record. Seven sections:

```
# <NNN>. <Short descriptive title>

## Status
Proposed | Accepted | Superseded by <NNN> | Request For Comments, Deadline <date>

## Context
What situation is forcing this decision, and what alternatives exist.

## Decision
We will <X>.
<Technical justification.>
<Business justification.>

## Consequences
<Impacts, good and bad. The trade-off analysis performed.>

## Compliance
<How this will be measured and governed — manual, or which fitness function.>

## Notes
Author, approval date, approved by, superseded date, last modified, modified by.
```

## Is this even your decision?

A decision is **architecturally significant** if it affects any of: the system's **structure**, its **non-functional characteristics**, its **dependencies**, its **interfaces**, or its **construction techniques**.

- *Structure* — the architecture pattern or style. Deciding to share code between services affects the bounded context and therefore the structure.
- *Characteristics* — a technology choice affecting performance is an architecture decision when performance matters, even though it names a specific product.
- *Dependencies* — coupling points between components and services, which drive scalability, modularity, agility, testability and reliability.
- *Interfaces* — how services are accessed and orchestrated, and the contracts, versioning and deprecation strategies that go with them.
- *Construction techniques* — platforms, frameworks, tools and even processes that are technical in nature but affect the architecture.

A hit on any one makes it yours, **regardless of whether it names a technology**. The common error is assuming that a decision mentioning a specific product is automatically merely technical.

Then check the other direction: does the decision *guide* the team's technical choice, or *make* it for them? "Use a reactive frontend framework" guides. "Use React" makes the choice. If it makes the choice, restate it one level more abstract as the constraint that actually matters. Naming a specific technology is legitimate only when that product is the only way to preserve a required characteristic.

## Timing

Decide at the **last responsible moment**: the point where enough information exists to justify and validate the decision, but not so late that teams are held up or you slide into permanent analysis.

Find it by asking when the **cost of deferring exceeds the risk of deciding**. Cost is low early and rises with time spent; risk is high early and falls as understanding grows. The decision point is where the curves cross.

Then verify implementability with the people who will build it. No architect knows every detail of every technology, and this is how you find out early. A decision to replicate reference data into a read-only cache in every service turned out to need more in-process memory than some services had available — discovered only through close collaboration.

## The trade-off method

### 1. Enumerate the options concretely

As topologies or diagrams, not as names. Do not frame as a binary; if a decision is presented as A versus B, name the axis A and B sit on and describe at least one intermediate position.

### 2. List the advantages

This happens automatically and needs no method.

### 3. Hunt the disadvantages of the front-runner

Deliberately, and do not stop until you have found some. The default failure is knowing the benefits of everything and the trade-offs of nothing.

Worked: broadcasting bids to a topic looks obviously better than point-to-point queues — architectural extensibility, producer decoupling. The analysis is not finished until it surfaces data-access exposure (a topic is easy to wiretap, a queue is not), the forced homogeneous contract, and the loss of per-consumer monitoring and autoscaling.

### 4. Separate intrinsic trade-offs from product-specific ones

A disadvantage may belong to the pattern, or only to the product implementing it. Before recording it as a trade-off of the *approach*, check whether another implementation removes it. Otherwise you rule out a whole pattern over a vendor limitation.

### 5. Build the matrix

Score each option against each factor. `references/trade-off-analysis.md` has two worked examples.

### 6. Weight the factors — this is the step that gets skipped

A matrix showing one option winning five factors to two says nothing until you ask whether the factors carry equal weight. **Generic trade-off analysis is not useful; it becomes valuable only when applied in a specific context.**

For a team with code across several platforms that cares little about performance or scale, the two factors favouring the losing option dominate everything else and it becomes the right answer — with the bonus that the team already knows which issues it must mitigate.

### 7. Reduce to a ranked question in the problem's own terms

*"Which matters more here, extensibility or security?"* Answer it from the business drivers, and record which driver decided it.

## Writing the record

**Context** answers *what situation is forcing me to make this decision?* It states the circumstances and concisely names the alternatives considered — and in describing the context it also documents that area of the architecture. If the alternatives need detailed analysis, add an Alternatives section rather than bloating Context.

**Decision** states the choice in an affirmative, commanding voice. *"We will use asynchronous messaging between services."* Never *"I think asynchronous messaging would be the best choice"*, which leaves it unclear whether a decision was made at all or only an opinion offered. Then the full justification — **both technical and business**.

The business justification is not decoration. "Decouple the functional areas so each uses fewer resources and can be deployed separately" is technical. The business justification answers why the business should pay: deliver functionality faster and improve time to market, or reduce the cost of releasing features. The four that carry weight are **cost, time to market, user satisfaction, and strategic positioning** — pick the one this audience actually holds.

And use its absence as a filter: **if the decision provides no business value, reconsider whether to make it at all.**

**Consequences** describes the overall impact, good and bad, which forces you to weigh whether the negatives outweigh the benefits. Record the trade-off analysis here. This is what prevents the argument six months later — a team member objecting to fire-and-forget messaging on error-handling grounds is raising a concern you already settled with stakeholders, and the objection only recurs because the settlement was not written down.

**Compliance** states how the decision will be measured and governed: manual, or automated, and if automated, how the fitness function will be written and what code changes it needs.

**Notes** carries metadata — worth keeping even when the records live in version control, which does not capture approval or supersession semantics.

## Status and the supersession trail

Three statuses. **Proposed** — awaiting approval by a higher-level decision maker or a review board. **Accepted** — approved and ready to implement. **Superseded** — changed by a later record.

A Proposed record is never superseded; it is modified until accepted.

Mark supersession **in both directions**:

```
ADR 42. Use of Asynchronous Messaging Between Order and Payment Services
Status: Superseded by 68

ADR 68. Use of REST Between Order and Payment Services
Status: Accepted, supersedes 42
```

The two-way link is what preserves the historical record of what was decided, why it was right at the time, and why it changed — and it pre-empts the inevitable *"but what about messaging?"* on the replacement decision.

Consider a fourth status for circulation: **Request For Comments** with a stated deadline. Circulate the draft, analyze the comments at the deadline, adjust, then set Proposed or Accepted.

## Settle the approval threshold before you need it

The Status section forces a conversation that otherwise gets avoided: which decisions can you approve alone, and which need a higher-level architect or a review board?

Three good starting places: **cost, cross-team impact, and security.**

Estimate cost as the hours to implement multiplied by the organization's standard full-time-equivalency rate, which the project owner or manager holds, including licensing and hardware. Agree a threshold above which a decision must be Proposed and externally approved. Route anything with cross-team impact or security implications upward regardless of cost.

Then document the criteria, so every architect writing a record knows when they may self-approve.

## Where to store them

Each decision gets its own file or page. Keeping them in the application's own source repository is tempting and, in larger organizations, wrong for two reasons: not everyone who needs to read a decision has access to that repository, and decisions whose context is broader than the application do not belong there.

Store them in a dedicated repository everyone can access, a wiki, or a shared directory rendered by a document tool. File by scope:

```
application/common/     decisions applying to every application
application/<app>/      decisions specific to one application
integration/            communication between applications, systems or services
enterprise/             global decisions affecting everything
```

Keep the names consistent across teams and file each record under the narrowest scope that actually contains it.

## Three uses beyond recording a choice

**As the architecture documentation.** No agreed standard exists for documenting software architecture, though diagramming standards are emerging. Context describes the area needing the decision and the alternatives; Decision gives the reasons, which is by far the best form of architecture documentation; Consequences records the trade-offs.

**As the filter for standards.** Few developers like standards, and standards are often about control rather than purpose. Writing one as a decision record changes that: Context states the situation forcing adoption, and Decision states not only what the standard is but **why it must exist**. That is a filter — if you cannot justify it, it is probably not a standard worth setting or enforcing. Consequences applies a second filter by forcing you to think through the implications. And developers who understand why a standard exists are more likely to follow it and less likely to challenge it.

**Retroactively, on inherited systems.** Records are worth writing for decisions already in production, because they establish whether a decision was the *right* one. Start with the significant ones and question each: a group of services shares a database — why, is there a good reason, should the data be broken apart?

Part of this is investigative. Often the person who made the decision has long since left and nobody knows, in which case identify the alternatives, analyze the trade-offs of each, and attempt to validate or invalidate the existing decision. Either outcome is useful: the exercise builds up the rationale for the system and surfaces architectural inefficiencies. The invalidated decisions are your refactoring backlog.

## What a language model can and cannot contribute

Models produce the most probable answer given the prompt, and reach for best practices. **Probability and best practices have no place in architecture decisions**, which require analyzing trade-offs and applying a specific business and technical context.

The hard part is translating business concerns — time to market, sustained growth — into architecture characteristics such as maintainability, testability and deployability. That translation is not obvious, takes years of experience, and is what the subsequent analysis rests on.

Worked: one payment-processing service versus one per payment type reduces to maintainability against performance. A single service performs better; multiple services are more maintainable. If the business's priority is time to market, maintainability dominates and separate services win — a conclusion that depends entirely on the business context, not on the general question.

So: do the business-to-characteristics translation yourself. Use a model to **enumerate candidate trade-offs as a check for ones you missed**, then verify each against your context. Never accept a probability-weighted or best-practice answer as the decision.

## Be the arbiter, not the evangelist

Two reasons to build a reputation for objective trade-off analysis rather than advocacy.

Evangelism is dangerous long-term, because **yesterday's best practice becomes tomorrow's antipattern.** Decisions are made on current factors with incomplete knowledge; the ecosystem keeps evolving; circumstances eventually weaken or invalidate the decision. Social capital invested in evangelizing a solution goes down with it.

And decision makers are not looking for enthusiastic advocacy but for sober objectivity. The architect known as the go-to person for an objective analysis becomes the one they trust when the decision is critical.

Expect the asymmetry: architects rarely get credit for good decisions and always get blamed for bad ones.

One phrase to retire. **"Best practice"** implies a clear duty to apply something whenever the situation arises. "Better practice" would at least invite argument. The superlative exists so that people can stop thinking and always reach for the same solution — the opposite of trade-off analysis. Downgrade it, and say what it is better *than*.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| Decision deferred indefinitely | Fear of choosing wrong | Decide at the last responsible moment; verify with the team |
| Same debate every few months | Justification missing | Record technical *and* business justification |
| Nobody knew the decision existed | It lived in an email | Link to a single system of record |
| Successor reverses a decision and breaks production | Rationale never recorded | The Decision section carries the why |
| Matrix says A, context demands B | Factors unweighted | Weight before reading the count |
| Standard nobody follows or believes in | Set without a stated why | Draft every standard as a record; kill the unjustifiable |
| Option looks free of downsides | Analysis incomplete | Keep hunting; check intrinsic versus product-specific |
| Decision framed as A or B | False binary | Name the axis; describe an intermediate position |
| Team disputes a settled trade-off | Consequences omitted the analysis | Record the trade-offs, not just the choice |
| Org-wide default adopted once, never re-tested | A one-time standards settlement | Treat a prior analysis as evidence, not a rule |
| Diagram misread in a review | No key, or view changed without context | Add a key; keep representational consistency |
| Four hours in a diagramming tool, unwilling to change it | Attachment grows with time invested | Keep early artifacts ephemeral |

## Never put the decision in an email body

Email is a good communication tool and a poor document repository. Putting the decision in the body creates multiple systems of record — one copy per email — usually omits the justification, which restarts the endless-debate problem, and makes it impossible to know whether everyone received a later revision.

State only the nature and context, then link:

> "Hi Sandra, I've made an important decision regarding communication between services that directly impacts you. Please see the decision using the following link…"

Note the second half of that first sentence. *"Directly impacts you"* is also the litmus test for **who to notify at all** — if a decision does not directly impact someone, do not send it to them.

## When to reach for a reference

- `references/adr-template.md` — the full template with a complete worked example, status semantics, approval criteria, and storage structure. Read when actually writing or filing one.
- `references/trade-off-analysis.md` — the matrix method with two worked comparisons, the weighting step, and a case showing how a hidden trade-off gets found. Read when the comparison is non-trivial.
- `references/diagramming.md` — representational consistency, semantic layering, standards comparison, and the diagram guidelines. Read when the decision must be drawn or presented.

## Further reading

- *Release It!* (2nd ed.), Michael Nygard — architectural significance, and the origin of the decision-record practice.
- *Building Evolutionary Architectures*, Neal Ford et al. — for the Compliance section, and governing decisions as the system changes.
