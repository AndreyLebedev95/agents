---
name: flag-requirement-gaps-as-open-questions
description: Runs a fixed set of quality-gate tests (scope, relevancy, completeness, viability, terminology consistency) against a requirement or requirement set, and converts every unresolved gap into an explicit, tracked open question instead of a silent assumption. Use whenever checking a requirement set for gaps, asking whether something is in scope, hunting for missed requirements, resolving conflicting stakeholder demands, or when asked to log an open question or state an assumption explicitly. Also use proactively before treating any requirement set as "done" or ready to hand off. Not for producing the requirement's decomposition, description, or fit criterion (see decompose-requirement-into-scenario, write-atomic-requirement-statement, derive-fit-criteria-and-acceptance-criteria) — this skill gates and tracks what those produce, it doesn't generate requirement content itself. Not for the physical structure of the specification document (see assemble-requirements-specification), which owns where the resulting register lives.
---

# Flag Requirement Gaps as Open Questions

The most dangerous requirements aren't the ones that are wrong — they're the ones where a real question got silently resolved by whoever happened to be building or testing later. This skill's whole job is to make sure that never happens invisibly: every gap this skill finds gets converted into either an assumption on a clear path to resolution, or an explicit open issue that stays visible until someone actually decides it.

## Two different registers — don't conflate them

- **Assumption**: a belief the team is *currently taking as true* so work can proceed. Transient by design — before the spec is released, every assumption must have become a requirement, become a constraint, or been proven irrelevant and dropped. An assumption still sitting as "just an assumption" at release time is an unresolved gap, not a valid closing state.
- **Open issue**: something the team explicitly knows it does *not yet know*, tracked for risk analysis and allowed to remain open at a given checkpoint. Record: an issue number, a cross-reference to every requirement/event/use-case/term it affects, a one-line summary, the stakeholders involved, and the action to be taken (even if that action is just "none yet, awaiting input from X").

Treating an open issue as though it were a resolved assumption (or vice versa) hides which gaps are actually blocking versus tracked-but-tolerable — pick the right one before logging anything. See `references/open-issues-register.md` for the register format and a worked example.

## The quality-gate tests

Run these against a requirement (or the requirement set as a whole) before treating it as settled. Each one below names what it catches and what a failing example looks like — the point is that each test targets a different kind of gap, so running only one of them will pass requirements that fail the others.

**Within-scope test.**
Does all the data this requirement needs already appear as a flow on the context/scope model, or does its rationale explain itself using only data already inside the boundary? If accepting it would require inventing new inbound/outbound flows just to justify it, that's a sign it's out of scope — or that the scope model itself is incomplete. Check both possibilities before concluding either way.

**Relevancy test.**
Trace the *rationale*, not the description, back to a stated project goal. A requirement can look relevant from its description and still fail this test once you check its rationale doesn't actually connect to anything the project is trying to achieve. The reverse also happens: something that looks irrelevant on its surface can pass once a deeper rationale is surfaced. Always compare rationale against goals, never description against goals.

**Completeness test (per requirement).**
Every relevant attribute of a requirement record (ID, description, rationale, fit criterion, source, etc.) must be either filled in or have its absence explicitly stated as deliberate ("not applicable because X" or "pending — waiting on Y"). A blank field that's blank because it was overlooked or judged too hard fails this test even if the requirement otherwise reads fine — that distinction (deliberate vs. overlooked) is the whole mechanism for catching silent assumptions at the level of a single requirement.

**Consistency-of-terminology test.**
Every essential domain term used in the requirement set has exactly one agreed definition, kept centrally, and every place that term is used matches that definition. A term used with drifted or inconsistent meaning across a spec is an ambiguity defect, not a style note — it's worth grepping every use of a load-bearing term and checking it against its one definition, not just trusting that everyone means the same thing.

**Viability test.**
A requirement is not viable if any of these fail, even when it's technically buildable: can the people or systems that will actually operate it do so (not just "is it technically possible")? Can the team afford the time, money, and skill to build it? Will the stakeholders who must use or tolerate it actually accept it? A requirement can be perfectly correct on paper and still fail this test if it assumes information or capability that the actual operators don't have.

**CRUD completeness check** (requires a data model and an event/requirement list to already exist).
Cross-reference every data class against every discovered business event or requirement, marking which perform Create/Read/Update/Delete on it. A class that's created but never read (or read but never created, with no external-system explanation) points at a missing business event or a missing requirement — not at bad data.

**Non-event check.**
For every discovered business event, ask what the work does if it does *not* happen. Most answers are "nothing" — but a real answer (an unfulfilled-order reminder, an escalation after a missed deadline) reveals a second, easily-missed business event that needs its own requirements.

## Other things to catch

- **A requirement written as a named technology** ("runs on Chrome, Safari, Edge") locks in one solution and hides which need it's actually serving. Restate it as the outcome the technology was meant to achieve ("runs on browsers used by 90% of the target population") before evaluating it for scope or completeness — you can't judge relevance or completeness against a mechanism, only against a need.
- **A candidate stored-data class** should satisfy: it represents a real-world thing the business recognizes, has a business-recognizable name, carries a unique identifier per instance, is a collection of attributes (not itself a scalar value), and needs to be stored and later read. A candidate that fails one of these is itself an open question about what's actually being tracked, not a data-modeling detail to wave through.
- **Gold-plating tell**: check the *dissatisfaction-if-omitted* rating, not the satisfaction-if-delivered rating. A requirement can score high on "people would like this" and still be a gold-plating candidate if almost nobody would actually mind losing it. Flag these rather than silently building them.
- **Late "new" requirements near delivery** are usually evidence that the original discovery process missed something, not scope creep to reflexively reject. Investigate what was missed rather than just pushing back.
- **A missing stakeholder category predicts a missing requirement category.** If the stakeholder register is incomplete, treat that as a leading indicator that a whole category of requirements hasn't been discovered yet, not as a separate, unrelated gap.
- **A constraint with no rationale and no fit criterion** is a candidate false constraint — a preference dressed up as a mandate. Challenge it before accepting it as non-negotiable.
- **Permission pairing**: for every requirement granting a capability, check that its restrictive complement ("...and no more") also exists. An unpaired grant is a common place for scope to quietly expand later.

## Resolving conflicts instead of leaving them open forever

When two stakeholders demand contradictory behavior, and there's a declared user-priority register (key users vs. secondary users vs. unimportant/infrequent/unauthorized users), resolve by that tier — key users take precedence. If no priority register exists yet, that absence is itself an open question: don't invent a tiebreaker on the spot, log the missing register as the gap.

## Failure modes

| Tell | Cause | Fix |
|---|---|---|
| A requirement's data has no flow on the context/scope model | Scope creep, or a missing scope-model entry | Flag out-of-scope, or fix the scope model — check both |
| The same term is used differently in two places in the spec | No central definition, or a drifted one | Add or enforce one definition; flag every mismatched use |
| A requirement's description reads fine but an attribute is just blank | Overlooked field mistaken for "not applicable" | Require an explicit "not applicable, because X" instead of a blank |
| A data class is created but never read anywhere | A business event is missing | Trace forward to find the missing event or requirement |
| A "new" requirement appears right before delivery | The original discovery pass was incomplete | Investigate the original gap — don't just label it scope creep |
| An assumption is still listed as "assumption" at spec sign-off | It was never actually resolved | Force it into a requirement, a constraint, or drop it, before release |

## Reference

`references/open-issues-register.md` — the exact fields for an open-issue entry, plus a worked example, and a short side-by-side of assumption vs. open-issue closing rules. Read it whenever creating or updating the register itself.
