# <System> extract / sync plan

**Prepared:** <date> · **Credential used:** <name and scope> · **Run as:** <schedule>

---

## 1. What this extract is

Scope:
Source endpoint(s):
Volume (expected):

**Consistency statement (one sentence, mandatory):**
> This extract is a <smear over approximately N minutes | point-in-time snapshot>.
> Downstream logic must not assume <...>.

## 2. Pagination

| Property | Value |
|---|---|
| Mechanism claimed by vendor | |
| Token diagnostic result | |
| Actual mechanism | |
| Page size requested / honoured | |
| Termination condition | on next-page token |
| Measured token lifetime | |
| Chunking strategy | |
| Checkpoint key | |
| Parallelisable | |

## 3. Filters

| Filter | Purpose | Verified against |
|---|---|---|

Cannot be filtered on (→ capability report):

Canary filter and its expected non-empty result:

## 4. Change detection and cadence

Method:
Cadence:
**Staleness window this implies:**
**Conflict rule** (which side wins when both changed in the window, on what evidence, who is told):

Bulk path exists separately from incremental: yes / no
If no — cold start and backfill route:

## 5. Reconciliation

| Check | Compares | Threshold | Owner |
|---|---|---|---|
| Continuity | | | |
| Sampling | | | |
| Vendor aggregate | | | |

Explicitly NOT used as a control total: the vendor's total-results count.

Soft-delete handling: get returns <...>, list returns <...>, we count <...>

## 6. Failure and restart

On token expiry:
On partial failure:
What makes a re-run safe:
Bound on every query:

## 7. Known gaps

| Gap | Consequence | Recorded in |
|---|---|---|
