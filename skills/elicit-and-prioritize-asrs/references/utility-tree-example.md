# Worked utility tree

A utility tree for a system in the healthcare space. Each leaf is a scenario, and each carries
`(business value, technical risk)` rated H/M/L.

Read this for the *shape*: note that the refinements are specific to this system rather than drawn
from a standard taxonomy, that every leaf is a scenario with a number in it rather than an attribute
name, and that the ratings spread rather than clustering at H.

| Quality attribute | Refinement | Scenario | Rating |
|---|---|---|---|
| Performance | Transaction response time | A user updates a patient's account in response to a change-of-address notification while the system is under peak load, and the transaction completes in less than 0.75 second. | (H, H) |
| | Throughput | At peak load, the system completes 150 normalized transactions per second. | (M, M) |
| Usability | Proficiency training | A new hire with two or more years' experience in the business can learn, in 1 week of training, to execute any of the system's core functions in less than 5 seconds. | (M, L) |
| | Efficiency of operations | A hospital payment officer initiates a payment plan for a patient while interacting with that patient, and completes the process with no input errors. | (M, M) |
| Configurability | Data configurability | A hospital increases the fee for a particular service. The configuration team makes and tests the change in 1 working day; no source code changes. | (H, L) |
| Maintainability | Routine changes | A maintainer encounters response-time deficiencies, fixes the bug, and distributes the fix with no more than 3 person-days of effort. | (H, M) |
| | | A reporting requirement requires a change to the report-generating metadata. The change is made and tested in 4 person-hours. | (M, L) |
| | Upgrades to commercial components | The database vendor releases a new major version, which is successfully tested and installed in less than 3 person-weeks. | (H, M) |
| | Adding a new feature | A feature tracking blood bank donors is created and successfully integrated within 2 person-months. | (M, M) |
| Security | Confidentiality | A physical therapist may see the part of a patient's record dealing with orthopedic treatment, but not other parts and no financial information. | (H, H) |
| | Resisting attacks | The system repels an unauthorized intrusion attempt and reports the attempt to authorities within 90 seconds. | (H, M) |
| Availability | No downtime | The database vendor releases new software, which is hot-swapped into place with no downtime. | (H, L) |
| | | The system supports 24/7/365 web-based account access by patients. | (M, M) |

## Things this example demonstrates

**Refinements are chosen, not inherited.** "Proficiency training" and "efficiency of operations" are
not standard usability sub-attributes; they are the two that matter for this system.

**"Configurability" appears even though it is not a catalogued attribute.** If it is what stakeholders
care about, it belongs in the tree. Build its scenario form with `model-a-new-quality-attribute` if it
needs one.

**Development-time leaves are measured in effort, not time-of-day.** Person-days, person-hours,
person-weeks, person-months — because the developers perform the response.

**One refinement can carry several leaves** (maintainability/routine changes has two) and the two
leaves can be rated differently. Do not force one scenario per refinement.

**The two (H,H) leaves are the marching orders** — transaction response time under peak load, and
role-scoped record confidentiality. Those get the most design attention and the earliest analysis. If
this tree had been ten (H,H) leaves instead of two, the finding to report would be that the system as
scoped may not be achievable.
