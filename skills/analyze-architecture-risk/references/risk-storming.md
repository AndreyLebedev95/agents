# Risk storming: facilitation guide

Read when actually running or preparing a session.

## Why it is collaborative at all

Two reasons, and both are structural rather than cultural. An architect working alone will overlook risk areas — not through carelessness, but because attention is finite and the diagram is large. And very few architects have full knowledge of every part of the system, which means the person best placed to see a given risk is frequently not the architect.

## Who to invite

Architects, plus senior developers and tech leads. The developers are not there as an inclusiveness gesture: they carry the implementation risk and see the parts of the system that never make it onto a diagram. The exercise also teaches them the architecture, which is a real second benefit.

## Scope: one dimension per session

Restrict each session to a single criterion (*"where are our security risks?"*) or a single context (*"what is at risk within customer registration?"*).

Where staffing or timing forces multiple dimensions into one session, have participants write the specific criterion next to the risk number on each note, and discuss the criteria separately. Otherwise three people rating the same component 6 may be rating three different risks — one availability, two performance — and the consensus discussion becomes incoherent.

## Phase 1: Identification

Individual, and deliberately so.

**Step 1.** The facilitator sends every participant an invitation containing:

- the architecture diagram, or where to find it
- the risk criteria and context to be analyzed
- date, time and location, physical or virtual
- any other logistics

**Step 2.** Participants analyze the architecture risks **individually**, using the impact × likelihood matrix.

**Step 3.** Participants classify each risk as low (1–2), medium (3–4) or high (6–9), and write the numbers on small green, yellow or red notes.

The individual phase is essential so that participants do not influence one another and nobody's attention is redirected away from a part of the architecture before they have assessed it themselves. Collaborative identification anchors the entire group on whatever gets said first, and the risks nobody mentions early tend never to get mentioned.

## Phase 2: Consensus

Highly collaborative. The goal is agreement on the risk level of each area.

Most effective with a large printed architecture diagram on the wall, or an electronic version on a large screen. As participants arrive, they place their notes on the relevant areas of the diagram.

Once the notes are up, the pattern is immediately readable. A typical starting state:

- Two participants rated the load balancer medium (3); one rated it high (6).
- One participant rated a component 9; nobody else flagged it at all.
- Three participants rated the database medium (3) — agreement.
- One participant rated the cache 9; nobody else flagged it.
- Three participants rated logging low (2) — agreement.
- Nothing at all on the remaining areas.

The agreements need no further discussion. **The discrepancies are the entire point of the phase.**

### Working a discrepancy

Ask the outlier for their reasoning before arguing with their number. Never average.

**Case 1 — the outlier is talked down.** Two participants rated the load balancer 3; one rated it 6, on the grounds that if it goes down the entire system is inaccessible. That is true and brings impact to high. The other two establish that clustering makes the likelihood low. The group settles at 3.

Note that this could have gone the other way. If the two had missed something real, the one would have convinced them to classify it high. That possibility is why the phase exists.

**Case 2 — the outlier has experience nobody else has.** One participant rated a set of expansion servers 9; nobody else saw any risk. Asked why, they explained they had watched that technology crash repeatedly under loads comparable to this architecture's. Without that participant in the room, the risk would have surfaced in production.

**Case 3 — the outlier does not know the technology.** One participant rated a cache component 9. Asked for their rationale, the answer was *"What's a Redis cache?"*

This is the rule worth internalizing: **whenever a participant identifies a technology as unknown to them, that area automatically gets the highest rating.** The impact × likelihood matrix cannot be applied to a component nobody understands, so there is nothing to score.

And the answer is valuable information rather than an embarrassment. It tells the architect that either the technology should change, or training costs need to be budgeted. Neither is visible if nobody asks. This is also the clearest argument for having developers in the room.

The phase continues until all participants agree on the risk areas identified, and ends when the notes are consolidated.

## Phase 3: Mitigation

Collaborative, and this is where the architecture actually changes.

Mitigating risk usually involves changing areas that had been considered finished. Depending on what was found, the original architecture may need substantial redesign, or the changes may be a targeted refactoring — adding a queue for backpressure to relieve a throughput bottleneck, for instance.

**Involve business stakeholders with decision authority.** Mitigation costs money, and the question of whether a given mitigation is worth its cost is not the architect's to answer alone.

**Bring more than one option.** The pattern:

> The team identifies a central database as medium risk (4) for availability. Clustering it and breaking it into separate physical databases would mitigate that — at $50,000. The facilitating architect takes the trade-off to the business owner, who decides the price is too high and the cost does not outweigh the availability risk. The architect then offers a different approach: instead of expensive clustering, split the database into two domain-based databases. $16,000, still reduces the risk. The stakeholders accept.

Presenting only the expensive option would have left the risk standing and the architecture unchanged. This is also why risk storming shapes negotiations with stakeholders as much as it shapes the architecture.

**Check that the mitigation removes the failure.** A good practice applied is not the same as a risk removed. Worked chain, from a system whose third-party diagnostics engine could handle only 500 requests per second while seasonal outbreaks drove demand far higher:

1. Asynchronous queues between the gateway and the engine — provides a backpressure point. Good practice. Users still wait too long and requests still time out.
2. Two prioritized message channels, so professional users' requests outrank self-service requests. Helps. Still leaves wait times.
3. Cache the outbreak-related questions in a dedicated service so those requests never reach the engine at all. **This one removes the risk**, and frees capacity for everything else.

Each step was defensible; only the third was sufficient. Keep asking whether the specific failure can still occur, and prefer eliminating demand over buffering it.

**Prefer structural separation to a check on a shared path.** Where regulation says only one class of user may reach a resource, per-call authorization on a shared gateway leaves real risk — everyone's traffic still flows through the same component. Separate gateways per user class mean unauthorized calls can never reach the protected interface at all. In one worked case, participants unanimously rated a shared gateway 6 on security grounds (high impact if the wrong users reached medical records, medium likelihood), and convinced the facilitator, who had initially rated it 2.

## Cadence

Not a one-time process. It continues throughout the lifecycle, identifying and mitigating risks before they reach production.

Frequency depends on the rate of change, any architecture-refactoring effort, and the pace of incremental development. Typical practice is to storm one particular dimension after adding a major feature, or at the end of every iteration.

## The same technique on user stories

During story grooming, rate the impact if a story is not completed within the iteration, and the likelihood that it will not be. Multiply. The high-risk stories can then be tracked carefully and prioritized accordingly, and the totals give an overall risk assessment for the iteration.
