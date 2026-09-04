# <System> integration capability report

**Prepared:** <date> · **Status:** <draft / issued before spec sign-off>
**Read this before finalising requirements.**

---

## 1. Summary for specification

The limits that most constrain what can be built, one line each:

1.
2.
3.

## 2. Constraint register

| # | Gap | Kind | Evidence | Confidence | Workaround | Cost | Forbids specifying |
|---|---|---|---|---|---|---|---|
| | | not exposed / not answerable / not representable / not guaranteed | | high / medium / low | | | |

## 3. Semantic gaps

| Our term | Their term | Where the meaning diverges | Consequence |
|---|---|---|---|

Enumerations with no total mapping:

| Our set | Their set | Values with no counterpart | Decision |
|---|---|---|---|

## 4. Failure modes at this boundary

| Mode | Mechanism | Tell | What it does to us | Required protection on our side |
|---|---|---|---|---|

Composite-operation latency check: <the arithmetic, where a business operation spans several calls>

## 5. Costs not on anyone's budget

| Cost | Driver | Estimate |
|---|---|---|
| Asynchronous handling | per interaction, not per call | |
| Middleware bridging | per channel | |
| Absent bulk path | cold start / backfill route | |
| Existing manual workarounds | people-hours currently invisible | |

## 6. Open questions blocking specification

| # | Question | Blocks | Owner | Asked | Answer |
|---|---|---|---|---|---|
