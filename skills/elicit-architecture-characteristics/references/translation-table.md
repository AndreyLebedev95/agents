# Translation table and characteristic catalog

Read when generating candidate characteristics, or when a stakeholder names a concern you cannot act on.

## Contents
- [Business concern to characteristic](#business-concern-to-characteristic)
- [The four categories](#the-four-categories)
- [Standard category definitions](#standard-category-definitions)
- [Terms that overlap](#terms-that-overlap)

## Business concern to characteristic

Stakeholders state goals in business terms. These are the standard mappings — a starting point to confirm against the domain, not a lookup to apply blindly.

| Business concern | Architecture characteristics |
|---|---|
| Mergers and acquisitions | Interoperability, scalability, adaptability, extensibility |
| Time to market | Agility, testability, deployability |
| User satisfaction | Performance, availability, fault tolerance, testability, deployability, agility, security |
| Competitive advantage | Agility, testability, deployability, scalability, availability, fault tolerance |
| Time and budget | Simplicity, feasibility |

Note how often agility, testability and deployability recur. Agility is composite — decompose it before designing for it.

## The four categories

Use these as a prompt list when generating candidates, not as a taxonomy to complete. No universal standard exists; every organization interprets the terms itself, and new characteristics appear as the ecosystem changes.

**Operational** — the ones that most often force structural change, so weight them heavily.

| Term | Definition |
|---|---|
| Availability | How much of the time the system must be available; 24/7 requires the ability to come back up quickly after any failure |
| Continuity | Disaster recovery capability |
| Performance | Measured through stress testing, peak analysis, frequency-of-use analysis, response times |
| Recoverability | How quickly the system must be back online after a disaster; backup strategy, duplicate hardware |
| Reliability / safety | Whether the system must be fail-safe or is mission critical in a way that affects lives or large sums; usually a spectrum, not a binary |
| Robustness | Handling error and boundary conditions while running — loss of connection or power |
| Scalability | Performing and operating as users or requests increase |

**Structural** — the architect's responsibility for code quality.

| Term | Definition |
|---|---|
| Configurability | How easily end users can change configuration through interfaces |
| Extensibility | How well the architecture accommodates extending existing functionality |
| Installability | Ease of installing on all necessary platforms |
| Leverageability / reuse | Extent to which common components can serve multiple products |
| Localization | Support for multiple languages in entry and query screens and data fields |
| Maintainability | How easily changes and enhancements can be applied |
| Portability | Ability to run on more than one platform |
| Upgradeability | Ease and speed of upgrading to a newer version on servers and clients |

**Cloud-provider**

| Term | Definition |
|---|---|
| On-demand scalability | The provider's ability to scale resources dynamically with demand |
| On-demand elasticity | The provider's flexibility as demand spikes |
| Zone-based availability | Separating resources by computing zone for resilience |
| Region-based privacy and security | The provider's legal ability to store data from particular countries; many jurisdictions restrict where citizens' data may reside |

**Cross-cutting**

| Term | Definition |
|---|---|
| Accessibility | Access for all users, including those with disabilities such as colourblindness or hearing loss |
| Archivability | Constraints on archiving or deleting data after a period |
| Authentication | Ensuring users are who they say they are |
| Authorization | Ensuring users can access only certain functions, by use case, subsystem, page, business rule or field |
| Legal | Legislative constraints — data protection law, financial-records law, regulations on how the application is built or deployed, reservation of rights |
| Privacy | Ability to encrypt and hide transactions from internal employees, including DBAs and network architects |
| Security | Encryption in the database and for network communication between internal systems; authentication for remote access |
| Supportability | Level of technical support needed; extent of logging and other debugging facilities |
| Usability / achievability | Level of training required for users to achieve their goals |

Any such list is necessarily incomplete, and a project may invent characteristics from factors unique to it.

## Standard category definitions

A published international standard organizes characteristics as performance efficiency (time behavior, resource utilization, capacity), compatibility (coexistence, interoperability), usability (appropriateness recognizability, learnability, user error protection, accessibility), reliability (maturity, availability, fault tolerance, recoverability), security (confidentiality, integrity, nonrepudiation, accountability, authenticity), maintainability (modularity, reusability, analyzability, modifiability, testability) and portability (adaptability, installability, replaceability).

That standard also lists functional suitability — functional completeness, correctness and appropriateness. Exclude it. Functional suitability describes the motivational requirements for building the software, not the capabilities the architecture must provide.

Since no standard can be imposed, build the organization's own list with objective definitions and hold everyone to it. An unshared definition produces confident miscommunication.

## Terms that overlap

Watch for these specifically, because both parties will believe they agree:

- **Interoperability vs compatibility.** Interoperability implies ease of integration with other systems, and therefore published, documented APIs. Compatibility is about conformance to industry and domain standards.
- **Learnability** means either how easily users learn the software, or how well the system self-configures and self-optimizes from its environment.
- **Availability vs reliability.** Independent, not synonymous. IP is available and not reliable: packets may arrive out of order and the receiver may have to ask again.
- **Scalability vs elasticity.** Scalability is a growing number of concurrent users over time. Elasticity is withstanding sudden bursts. Some systems are scalable and not elastic; elastic systems usually need scalability too, but not the reverse.
