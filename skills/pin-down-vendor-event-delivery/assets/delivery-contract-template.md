# <System> event delivery contract

**Feed:** <webhook / queue / topic / change feed> · **Prepared:** <date>
**Verdict key:** `S` stated by vendor in writing · `O` observed but unpromised · `A` absent

---

## Summary

What this feed can be relied on for:
What it cannot be relied on for:
What we must build because of that:

## Guarantees

| Property | Vendor states | Observed | Verdict | Evidence |
|---|---|---|---|---|
| Arrival (at-most / at-least / exactly once) | | | | |
| Ordering, and the scope it holds in | | | | |
| Timeliness / latency bound | | | | |
| Retry duration and buffer location | | | | |
| Behaviour when producer buffer fills | | | | |
| Subscription survives consumer downtime | | | | |
| Event published during subscribe (race) | | | | |
| Replay: retention duration | | | | |
| Replay: per-subscription message cap | | | | |
| Dedup key, who mints it | | | | |
| Dedup window duration | | | | |
| Past-window behaviour | | | | |
| Correlation field available | | | | |
| Sequence field consecutive (not just ascending) | | | | |
| Failure channel for our handler | | | | |
| Poison message destination | | | | |
| Filter is an authorization boundary | | | | |

Maximum tolerable downtime, computed from retention and cap: <...>
Actual observed recovery time: <...>

## Idempotence classification

| Operation | Inherent / via dedup / none | Dedup key | Window | On ambiguous timeout |
|---|---|---|---|---|

## Required compensations

| Absent guarantee | What we build | Sized how | Owner |
|---|---|---|---|

## Backfill and cold start

Route for history predating the subscription:
Route for events outside the replay window:
Cadence of reconciliation:

## Open questions

| # | Question | Blocks | Owner | Asked | Answer |
|---|---|---|---|---|---|
