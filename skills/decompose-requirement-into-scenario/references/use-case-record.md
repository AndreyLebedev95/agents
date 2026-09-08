# Use-case record schema

Use this when the decomposition needs to be a structured record rather than prose — e.g. feeding a spec-assembly step, a requirements database, or another skill.

## Fields

- **Business Event Name** — "[actor/system] + [decision or action]"
- **Business Use Case Name** — the response this record specifies
- **Trigger** — the specific data flow, message, or time/condition that starts it
- **Preconditions** — the prior business event(s) that must already have completed
- **Owning Actor** — whose decision is the trigger
- **Active Actors** — who else performs a step in the behavior (may be empty)
- **Interested Parties** *(optional)* — who cares about the outcome without doing anything in the flow
- **Normal Case Scenario** — numbered steps, in essence form, 3–10 steps
- **Alternatives** — business-offered choices along the way, each with its own resulting steps/outcome
- **Exceptions** — unwanted deviations along the way, each with its own resulting steps/outcome
- **Post/Exit Conditions** — one per branch (normal case, each alternative, each exception): what must be true when this branch concludes

## Worked example

**Business Event Name:** Member wants to renew a borrowed item
**Business Use Case Name:** Process renewal request
**Trigger:** Renewal Request (item ID + member ID)
**Preconditions:** The item must already be on loan to this member (i.e., a prior "Item Checked Out" event has occurred and not yet been closed by a return)
**Owning Actor:** Member (their decision to request renewal is the trigger)
**Active Actors:** Member
**Normal Case Scenario:**
1. Confirm the item is currently on loan to this member
2. Confirm no other member has an active hold on this item
3. Extend the due date by the standard loan period
4. Confirm the renewal to the member
**Alternatives:**
- Member requests renewal for multiple items at once → repeat steps 1–4 per item, report per-item results together
**Exceptions:**
- Another member has an active hold on the item → renewal is refused; member is told to return the item by the original due date
- Member has unpaid fines above the threshold that blocks renewals → renewal is refused; member is told the fine amount blocking them
- Item was already renewed the maximum number of times → renewal is refused; member is told to return the item
**Post/Exit Conditions:**
- Normal case: due date extended; confirmation recorded against the member's account
- Hold-blocked exception: due date unchanged; refusal reason recorded
- Fine-blocked exception: due date unchanged; refusal reason recorded
- Max-renewals exception: due date unchanged; refusal reason recorded

Notice every exception gets its own exit condition — "renewal refused" isn't one shared outcome, because a downstream reader (someone writing acceptance criteria, someone checking for missed cases) needs to know *which* refusal reason applies to verify the right thing happened.
