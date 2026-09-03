# Glossary format and worked splits

Read when producing the artifact. Contents: [entry template](#entry-template) · [banned synonyms](#banned-synonyms-table) · [splitting an ambiguous term](#worked-splitting-an-ambiguous-term) · [separating false synonyms](#worked-separating-false-synonyms) · [scenarios](#scenario-format) · [findings](#findings-section)

## Entry template

```markdown
### Rollout
**Context:** Delivery
**Means:** A planned, staged distribution of one artifact version to a target set of devices.
**Behaviours:** Is planned, started, advanced between phases, halted, resumed, rolled back, completed.
**Invariants:** Has at least one phase. Never targets a device that is not in its target set. Cannot advance past a phase whose success criteria have not been met.
**Relates to:** Consumes an Artifact. Targets a Fleet. Advances through Phases. Emits a Rollback when halted after any device has been updated.
**Not to be confused with:** Deployment, which is one device receiving one artifact. A Rollout is the plan; a Deployment is one instance of it happening.
**Public:** yes — appears in the operator API and in delivery events.
```

Fields earn their place:

- **Context** — without it, "one term one meaning" is unenforceable, because you cannot say what the meaning is scoped to.
- **Invariants** — the part nobody volunteers and the part that later prevents an illegal state.
- **Not to be confused with** — where the near-neighbour distinction lives. If you cannot fill this in for a term that has a near neighbour, you have not finished separating them.
- **Public** — marks terms whose renaming breaks consumers outside the boundary.

Omit a field only when it genuinely does not apply, and prefer writing "none known" over deleting the line — an empty invariants list is information.

## Banned synonyms table

Keep this flat and near the top. It is the part people consult in the middle of an argument, so it must be scannable.

| Do not use | Use instead | Why they are different |
|---|---|---|
| Policy | Regulatory rule / Insurance contract | Two unrelated concepts shared one word; ask "is this something we must obey, or something we sold?" |
| User | Visitor / Account | Visitors are observed and cannot act; accounts authenticate and hold permissions |
| Group | Fleet / Cohort | A Fleet is a durable membership set; a Cohort is a slice selected for one rollout and discarded after |

The third column carries the load. "Because we picked one" is not a reason and will be re-litigated within a month. Give the distinguishing question or the behavioural difference so the reader can classify a new case themselves.

## Worked: splitting an ambiguous term

**Before.** One entry, two meanings, quietly incompatible:

> **Policy** — a rule that governs behaviour. Sometimes refers to the contract sold to a customer.

Symptoms this produces: a `Policy` table with columns that are null for half the rows; two teams reporting different counts of "active policies"; a bug report that reads as nonsense until you work out which meaning the reporter had in mind.

**After.** Two terms, each complete, and the ambiguous word retired:

> **Regulatory rule** — a constraint imposed on us by law or by an internal control, which the system must enforce and cannot waive.
> *Invariants:* always has an effective date. Cannot be deleted, only superseded.
>
> **Insurance contract** — an agreement sold to a customer, defining cover, premium and term.
> *Invariants:* always has exactly one policyholder. Premium is never negative. Cover cannot start before the contract is signed.

Banned-synonym row:

| Policy | Regulatory rule / Insurance contract | Ask: is this something we must obey, or something we sold? |

Note the invariants only became statable *after* the split. That is the usual pattern — an ambiguous term cannot carry invariants, because any rule you write is false for the other meaning. Difficulty writing invariants is itself a signal that a term needs splitting.

## Worked: separating false synonyms

**Before.** Three words treated as interchangeable:

> **User / Visitor / Account** — someone who uses the system.

**Testing the pair.** For each pair, ask what one can do that the other cannot:

- Can a visitor authenticate? No. Can an account? Yes. → different.
- Does a visitor have permissions? No. → different.
- Is visitor data used for anything except analysis? No. → different.

Three behavioural differences, so both concepts survive:

> **Visitor** — an unidentified party whose interactions are recorded for analysis. Cannot authenticate, holds no permissions, has no durable identity across sessions.
>
> **Account** — an authenticated party that exercises system functionality under a set of permissions. Has a durable identity and an owner.
> *Not to be confused with:* Visitor, which is observed rather than acting.

"User" is retired as a banned synonym pointing at both, because it is the word that made the two invisible.

**When the test finds nothing.** If no pair yields a behavioural difference, the words really are synonyms. Pick one — the one the business uses most, not the one the code uses — and ban the rest. Record the decision so it is not reopened.

## Scenario format

For rules that will not compress into a definition:

```gherkin
Scenario: Reopening a closed ticket
  Given a ticket closed 3 days ago
  When the customer replies to it
  Then the ticket is reopened
  And it keeps its original priority

Scenario: Reopening a ticket closed too long ago
  Given a ticket closed 9 days ago
  When the customer replies to it
  Then a new ticket is created
  And it references the closed ticket
```

Guidelines that keep these useful:

- **Business language only** — same test as the definitions. No tables, no endpoints, no status codes.
- **One rule per scenario.** A scenario with three Whens is three scenarios.
- **Write the boundary cases as their own scenarios.** The pair above is the point: the rule is not "customers can reopen tickets", it is a rule with a seven-day edge, and the edge is where the disagreement lives.
- **Read them back to the person who gave you the rule.** They can confirm or correct these, which is why the format is worth the effort. Do not expect them to write the scenarios.
- **Name the scenario for the case, not the mechanism.** "Reopening a ticket closed too long ago" beats "Test reopen path 2".

## Findings section

Two kinds of entry, both valuable, neither a blocker:

```markdown
## Findings

### Undefined
- **Stalled** — used in three specs to describe a rollout, no two people gave the same threshold.
  Asked: A (delivery) said "no progress for an hour"; B (ops) said "any device reporting failure".
  Needs a decision from whoever owns rollout policy.

### Conflicts
- **Fleet** — Provisioning treats a fleet as a durable named set with an owner.
  Telemetry treats a fleet as whatever devices reported a matching tag in the last window.
  These are different concepts. Candidate resolution: two terms, or one term scoped to two contexts.
```

Record who said what. A conflict without attribution cannot be resolved, because there is nobody to go back to.
