# <System name> API reference

**Version documented:** <vendor version / date>
**Sources:** <docs URL and version, sandbox, observed traffic, vendor correspondence>
**Marking key:** `C` contracted in writing · `O` observed but not promised · `U` unknown

---

## 1. Shape and scope

Surface shape: <factors into method x resource | flat list of special-purpose operations>
Covered here: <...>
Deliberately excluded: <...> (see related documents)

## 2. Identifier contract

| Id type | Format | Uniqueness scope | Mutable parts | Reused after delete? | Bad vs deleted distinguishable? | Mark |
|---|---|---|---|---|---|---|
| | | | | | | |

Second natural key (where a mutable part forces one): <...>

## 3. Resources and operations

| Operation | Purpose | Preconditions | Must follow | Idempotent | Atomic | Side effects | Mark |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Operations outside the standard verb set (feeds the capability report):
- <operation> — <what the model could not express>

## 4. Field semantics

| Field | Type | Unit | Four-state behaviour | Zero = value or sentinel | Output-only | Omitted by default | Format is a parse contract | Mark |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## 5. Required call ordering

| Sequence | Preconditions | Documented or discovered | Mark |
|---|---|---|---|
| | | | |

## 6. Auth model

- Credential type and what it represents:
- What it proves (origin / integrity / non-repudiation):
- Signature covers (components, order, canonicalisation):
- Scope:
- Lifetime and expiry behaviour:
- Rotation shape (overlap window or hard cutover):

## 7. Error semantics and retry

| Error | Meaning | Bucket (retriable / never / unknown outcome) | Distinguishable from caller error | Mark |
|---|---|---|---|---|
| | | | | |

Rate limits: dimensions, windows, behaviour on breach, retry hint format.

## 8. Open questions

| # | Question | Blocks | Who can answer | Asked on | Answer |
|---|---|---|---|---|---|
| | | | | | |
