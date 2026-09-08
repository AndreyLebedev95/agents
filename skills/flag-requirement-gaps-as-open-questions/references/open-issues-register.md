# Open issues register

## Fields per entry

- **Issue number** — unique, stable
- **Cross-reference** — every requirement, business event, use case, or glossary term this issue affects
- **Summary** — one statement of the uncertainty
- **Stakeholders involved** — who needs to weigh in or be informed
- **Action to be taken** — what happens next, even if that's just "awaiting input from `<stakeholder>`"

## Worked example

**Issue #14**
Cross-reference: REQ-0231 (renewal fine threshold), REQ-0233 (renewal refusal message)
Summary: The fine amount that blocks a renewal was given as "a small amount" by the branch manager and as "$5" by the finance lead — these don't agree, and no one has confirmed which is authoritative, or whether it varies by branch.
Stakeholders involved: Branch manager, finance lead
Action to be taken: Finance lead to confirm the authoritative threshold and whether it's branch-specific, by the next requirements review.

## Assumption vs. open issue — closing rules side by side

| | Assumption | Open issue |
|---|---|---|
| What it represents | A belief taken as true for now, to let work proceed | A known unknown, tracked but not necessarily blocking |
| Can it still be open at release? | No — it must resolve into a requirement, a constraint, or be dropped as irrelevant before the spec ships | Yes, if the risk of leaving it open has been explicitly accepted by the stakeholders involved |
| What "resolved" looks like | Converted into a requirement or constraint (or removed) | The action-to-be-taken has actually been taken, and the cross-referenced items updated accordingly |
| Wrong-register symptom | An "assumption" that's really just an unexamined guess nobody plans to verify | An "open issue" that's actually blocking release but nobody has flagged it as blocking |

If you're not sure which register a gap belongs in: are you currently *presuming* something true so you can keep working (assumption), or do you *know* you don't know something and need someone else to decide (open issue)?
