# Measurement reference

Read when a characteristic target must be turned into a number, or when a stakeholder states a target in vernacular.

## Availability, in units people can reason about

The "nines" vernacular hides what is being asked for. Convert before discussing it.

| Uptime | Downtime per year | Downtime per day |
|---|---|---|
| 90.0% (one nine) | 36 days 12 hrs | 2.4 hrs |
| 99.0% (two nines) | 87 hrs 46 min | 14 min |
| 99.9% (three nines) | 8 hrs 46 min | 86 sec |
| 99.99% (four nines) | 52 min 33 sec | 7 sec |
| 99.999% (five nines) | 5 min 35 sec | 1 sec |
| 99.9999% (six nines) | 31.5 sec | 86 ms |

Hold the conversation in hours, minutes and seconds. It replaces vernacular with quantified metrics, and it frequently settles the question by itself: a global trading system with two hours between markets when no trading occurs plainly does not need five nines, and 86 seconds of average daily unplanned downtime is visibly acceptable in that context.

Check any stated target against the domain's own idle windows before accepting it.

## External dependencies

Availability you do not control is settled by finding the published commitment rather than by design. A service-level agreement is usually a legally binding contractual commitment; a service-level objective usually is not. Convert the percentage to annual downtime, decide whether that is acceptable for this workflow, and record the figure on the architecture diagram so the assumption stays visible.

## Performance

State performance against load, never alone. Establish a baseline figure with no particular scale, then the acceptable figure at a specific concurrent user count. Characteristics interact, so a response-time target without a concurrency figure cannot be met or missed.

Prefer specific budgets over one general number:

- **First contentful paint** and **first CPU idle** — perceived responsiveness on web and mobile.
- **Page weight (K-weight) budgets** — a maximum byte count for libraries and frameworks on a page. This follows from physics: only so many bytes cross a network at a time, especially for mobile devices on low-bandwidth connections. A page-weight budget constrains application design, not just tuning.

The named front-end metrics are current but the tooling around them changes quickly; the practice of budgeting a specific measure is the durable part.

## Measuring, once the system exists

Averages hide the failures that matter. If a boundary condition makes 1% of requests take ten times longer, a high-traffic average will not show it. Measure maximums and percentiles too.

Stronger practice sets no arbitrary target at all: measure the characteristic over time, build a statistical model, and alarm when live metrics fall outside the prediction. A breach then means either the model is wrong or the system is wrong, and both are worth knowing.

## Process characteristics

The measurable constituents of agility:

- **Testability** — code coverage, available on every platform. Coverage is a floor, not a proof: 100% coverage with weak assertions gives no confidence in correctness.
- **Deployability** — percentage of successful deployments, how long a deployment takes, issues raised by deployments.

Each team should pick the mix of quantitative and qualitative measures reflecting its own priorities.
