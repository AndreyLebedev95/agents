# Specification document skeleton

## Area 1 — The Problem
1. Goals (Purpose / Advantage / Measurement per goal)
2. Stakeholders (with priority tier: key / secondary / unimportant)
3. Glossary — one definition per essential term, referenced everywhere that term is used
4. Scope of the problem space
5. Business data dictionary

## Area 2 — The Solution
6. Scope of automation — the product boundary through the business use cases

## Area 3 — The Business Events
7. Event list (each event: name in "[actor/system] + [action]" form, kind — external / time-triggered / conditional)
8. Per business event:
   - Functional requirements
   - Non-functional requirements (own + inherited from the event level)
   - Additional material (supporting data, references)

## Open Issues Register
(See the gap-flagging skill's register format — filed here as its own section, cross-referenced from any affected requirement.)

---

## Atomic requirement record schema

Use this same shape for every requirement, regardless of type — only the Type value and filing section change:

| Field | Notes |
|---|---|
| Number | Unique, assigned at write time |
| Description | "The product shall `<verb>`..." — one sentence, one verb |
| Rationale | Why this exists — drives priority, exposes smuggled solutions |
| Type | functional / non-functional / constraint / technological / project driver / project issue |
| Fit Criterion | The testable measure (see the fit-criteria skill) |
| Source | Who/what raised this requirement |
| Customer Satisfaction | Rating if delivered |
| Customer Dissatisfaction | Rating if omitted — the more diagnostic of the two for spotting gold-plating |
| Conflicting Requirements | Cross-references |
| Dependent Requirements | Cross-references |
| Supporting Material | Evidence behind the fit criterion, background |
| Version Number | For change tracking |
