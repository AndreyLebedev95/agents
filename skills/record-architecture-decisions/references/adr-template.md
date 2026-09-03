# The decision record template

Read when actually writing or filing one.

## The template

A short text file, usually one to two pages, in a lightweight markup format or a wiki template. Keep it consistent and concise. Extending it is fine — an Alternatives section analyzing rejected options is a good addition — as long as the extension is applied consistently.

```markdown
# <NNN>. <Short descriptive title>

## Status
<Proposed | Accepted | Superseded by NNN | Request For Comments, Deadline DD MMM YYYY>

## Context
<What situation is forcing this decision. The alternatives considered, concisely.>

## Decision
We will <X>.

<Technical justification.>

<Business justification.>

## Consequences
<Impacts, good and bad.>
<The trade-off analysis performed during the decision.>

## Compliance
<How this will be measured and governed. Manual, or the specific fitness function.>

## Notes
Author:
Approved:
Approval date:
Superseded date:
Last updated:
Modified by:
```

**Titles** are numbered sequentially with a short phrase, specific enough to remove ambiguity about the decision's nature and context. *"42. Use of Asynchronous Messaging Between Order and Payment Services"* — not *"42. Messaging"*.

## A complete worked example

```
ADR 76. Separate Queues for Bid Streamer and Bidder Tracker Services

STATUS
Accepted

CONTEXT
The Bid Capture service, upon receiving a bid, must forward that bid to the Bid
Streamer service and the Bidder Tracker service. This could be done using a single
topic (pub/sub), separate queues (point-to-point) for each service, or REST via the
Online Auction API layer.

DECISION
We will use separate queues for the Bid Streamer and Bidder Tracker services.

The Bid Capture service does not need any information from the Bid Streamer service
or Bidder Tracker service (communication is only one-way).

The Bid Streamer service must receive bids in the exact order they were accepted by
the Bid Capture service. Using messaging and queues automatically guarantees the bid
order for the stream by leveraging first-in, first-out queues.

Multiple bids come in for the same amount. The Bid Streamer service only needs the
first bid received for that amount, whereas the Bidder Tracker needs all bids
received. Using a topic would require the Bid Streamer to ignore bids that are the
same as the prior amount, forcing the Bid Streamer to store shared state between
instances.

The Bid Streamer service stores the bids for an item in an in-memory cache, whereas
the Bidder Tracker stores bids in a database. The Bidder Tracker will therefore be
slower and might require backpressure. Using a dedicated Bidder Tracker queue
provides this dedicated backpressure point.

CONSEQUENCES
We will require clustering and high availability of the message queues.

This decision will require the Bid Capture service to send the same information to
multiple queues.

Internal bid events will bypass security checks done in the API layer.

UPDATE: Upon review at the January 14 review board meeting, the board decided that
this was an acceptable trade-off and that no additional security checks are needed
for bid events between these services.

COMPLIANCE
We will use periodic manual code reviews to ensure that asynchronous messaging is
being used between the Bid Capture service, Bid Streamer service, and Bidder
Tracker service.

NOTES
Author: Subashini Nadella
Approved: Review Board Members, 14 JAN
Last Updated: 14 JAN
```

Three things to notice. The Context names all three alternatives in two sentences. The Decision gives four independent reasons, each traceable to a system property rather than a preference. And Consequences records an accepted downside plus the record of who accepted it — which is what stops that downside being re-raised as an objection later.

## Status semantics

| Status | Meaning |
|---|---|
| Proposed | Must be approved by a higher-level decision maker or governing body |
| Accepted | Approved and ready for implementation |
| Superseded by NNN | Changed by a later decision |
| Request For Comments, Deadline <date> | Circulating for feedback before proposal |

A **Proposed** record is never superseded — it is modified until accepted. Supersession always assumes the prior status was Accepted.

**Mark supersession in both directions:**

```
ADR 42. Use of Asynchronous Messaging Between Order and Payment Services
Status: Superseded by 68

ADR 68. Use of REST Between Order and Payment Services
Status: Accepted, supersedes 42
```

The link and history trail is what lets you avoid the inevitable *"but what about messaging?"* question on ADR 68.

**Request for Comments** is worth adding as a status. Circulate the draft with an explicit deadline for reviewers, then at the deadline analyze the comments, make any necessary adjustments, and set the status to Proposed — or Accepted, if you have the authority to approve it.

## Approval criteria

The Status field forces a conversation with your lead that is otherwise avoided: which decisions can you approve yourself, and which need a higher-level architect, a review board, or another governing body?

Three good starting places:

**Cost.** Include software purchase or licensing fees, additional hardware, and the overall level of effort. Estimate the effort as *hours to implement × the organization's standard full-time-equivalency rate* — the project owner or manager usually holds the rate. Agree a threshold: for example, *costs exceeding $5,000 must be approved by the review board*.

**Cross-team impact.** Anything affecting other teams or systems goes to the governing body regardless of cost.

**Security.** Anything with security implications goes up regardless of cost.

Once the criteria and limits are agreed, **document them well**, so that every architect creating a record knows when they can and cannot approve their own decisions.

## Storage

Each decision gets its own file or wiki page.

Keeping them in the same repository as the source code is tempting — the team can version and track them like code. In larger organizations, avoid it. Not everyone who needs to see a decision has access to that repository, and decisions with context outside the application (integration decisions, enterprise decisions, decisions common to every application) do not belong in one application's repository.

Store instead in a dedicated repository everyone can access, a wiki using a template, or a shared directory accessible by a wiki or document-rendering tool.

Structure by scope:

```
application/
    common/          decisions applying to all applications
    app1/            decisions specific to app1
    app2/            decisions specific to app2
integration/         decisions about communication between applications,
                     systems or services
enterprise/          global decisions impacting all systems and applications
```

Examples of the outer scopes. Enterprise: *"All access to a system database will only be from the owning system"*, preventing databases being shared across systems. Common: *"All framework-related classes will contain an annotation or attribute identifying the class as belonging to the underlying framework code."*

The directory names here are recommendations. Choose whatever fits the organization, as long as the names are consistent across teams. In a wiki, each directory becomes a navigational landing page and each record a page within it.

## Tooling

Command-line tooling exists for managing records — numbering schemes, locations, supersession logic. Worth adopting once the collection grows past the point where a human maintains the numbering reliably.
