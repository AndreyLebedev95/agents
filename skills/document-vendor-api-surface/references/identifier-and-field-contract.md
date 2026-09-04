# Identifier and field contract

Read while working steps 2 and 3. Contents: [why identifiers come first](#why-identifiers-come-first) ·
[the five-part identifier contract](#the-five-part-identifier-contract) · [hierarchy effects](#hierarchy-effects) ·
[the four states of a field](#the-four-states-of-a-field) · [write semantics](#write-semantics) ·
[relationship and shape traps](#relationship-and-shape-traps) · [the interrogation list](#the-interrogation-list)

## Why identifiers come first

Every later artifact depends on being able to name a record and have the name keep meaning the
same thing. The mapping table between the vendor's world and yours is keyed on identifiers.
Reconciliation compares sets of identifiers. Deduplication and idempotence key on them. If the
identifier contract is unstable and nobody noticed, all three fail at once and they fail quietly:
records get duplicated or orphaned rather than raising an error.

## The five-part identifier contract

**1. Format.** Character set, length, case sensitivity, and — critically — whether a
numeric-looking identifier is actually a token. An id that looks like a number will eventually be
parsed as one: leading zeros disappear, large values lose precision, and comparison switches from
string equality to numeric equality with different results. Record the intended type, and store
it as text unless the vendor contracts it as an integer.

**2. Scope of uniqueness.** An identifier is unique within some scope — a tenant, an environment,
a parent record, a region — and the scope is rarely stated. Two consequences: an id from one
environment may silently collide with a different record in another, and an id may be ambiguous
without its scope. Find the scope and store it alongside the id.

**3. Mutability of encoded parts.** Decompose the identifier into its parts and mark each mutable
or immutable. Any part encoding a mutable fact — a branch code, a product line, a status, a year
— is scheduled renumbering. When the fact changes, the vendor renumbers, your foreign keys point
at nothing, and no event announces it. When you find a mutable part, the mapping table needs a
second natural key built from attributes that do not change.

**4. Reuse after deletion.** Ask directly, and do not accept "they're unique" as an answer to a
question about reuse. Reused identifiers mean a stale reference silently resolves to the wrong
record — the worst available failure, because it produces plausible output.

**5. Error distinguishability.** If a malformed identifier and a validly-formed-but-absent one
return the same error, you cannot triage: every "not found" needs a human to decide whether it is
a bug in your code or a genuinely deleted record. Establish this early; it changes how much
diagnostic work every future incident costs.

## Hierarchy effects

A vendor hierarchy is not just a naming convention. It usually carries two cascades you did not
ask for: a **delete cascade** (removing a parent removes children) and a **permission cascade**
(access to a parent implies access to children, or denies it). Both are policy decisions the
vendor made, inherited by you.

Expect the hierarchy to be immutable. Most systems that nest records do not support moving a
record to a different parent, so a mis-filing is not a correction — it is an identity change,
priced as delete-and-recreate with a new identifier and every reference rewritten.

A deep hierarchy makes a leaf identifier unusable on its own. If addressing a record requires the
full ancestor path, your storage must carry the path rather than the leaf, and every place you
pass "the id" around must pass the path instead.

A sub-object the vendor did not promote to a resource has no identifier at all, and therefore
cannot be referenced, tracked, or changed independently of its parent.

## The four states of a field

A field is not present-or-absent. It is in one of four states, and they mean different things:

| State | Wire form | Usually means |
|---|---|---|
| Value | `"x": 5` | set to 5 |
| Empty | `"x": ""` or `[]` | set, to an empty value |
| Null | `"x": null` | explicitly cleared |
| Absent | key not present | not mentioned / not returned |

The collapse between these happens inside **your** deserializer, not on the wire. A structure that
maps missing and null to the same default erases the distinction before any of your code sees it,
and the vendor's traffic looks perfectly correct in a capture. This is the mechanism behind most
silent loss on read and most unintended overwrites on write.

Two follow-ons:

**The zero value is overloaded.** If a numeric field uses zero to mean "unset", a legitimate zero
cannot be represented. Find out whether zero is a value or a sentinel before writing any logic
that treats it as an amount.

**A field absent from a response may be excluded by default, not empty.** Some systems omit
expensive or large fields unless asked. Absence is then a fact about your request, not about the
record — and code that treats absence as "no value" writes emptiness back over real data.

## Write semantics

**Whole-resource writes erase what you do not know about.** A full replace sends your
understanding of the record and overwrites everything else, including fields the vendor added
after your data structures were generated. This gets worse over time and produces no error.

**A replace cannot distinguish create from update.** Success tells you the record now exists in
the state you sent. It does not tell you whether you created it or overwrote someone else's work.

**Inferred field masks cannot express clearing.** If the vendor derives which fields to update
from which keys are present in the payload, then clearing a field and not touching it are the
same request. Explicit masks fix this; inferred masks make "set this to null" unexpressible.

**Nulling a map key is not removing it.** Most systems cannot express removal of a key from a map
or dictionary field, only setting its value to null — which leaves the key present. If your domain
needs removal, that is a capability gap, not a coding problem.

**Anything you cannot address individually must be rewritten whole**, and whole rewrites are where
concurrent writers lose each other's changes.

## Relationship and shape traps

**Every relationship exists in both directions in the data and usually in only one in the API.**
You can navigate parent-to-child but not child-to-parent, or vice versa. Establish the traversable
direction before designing anything that needs the other one.

**Inlined data is a copy of unknown age, not a join.** When a response embeds a related record,
that embedded copy was assembled at some point the vendor does not state. Treat it as cached, not
current, unless the vendor contracts freshness.

**Arrays are unordered until proven otherwise.** Ordering that holds in testing is often incidental
and changes with storage layout, sharding or version.

## The interrogation list

Put these to the vendor, in writing, and record the answers with dates:

1. Are identifiers stable across updates, merges, re-imports and environment refreshes?
2. What is the scope of uniqueness?
3. Which parts of the identifier encode facts that can change?
4. Are identifiers ever reused after deletion?
5. Do a malformed id and a deleted id return distinguishable errors?
6. Which fields are output-only?
7. For each numeric field, what is the unit, and is zero a value or a sentinel?
8. Which fields are omitted by default rather than being empty?
9. Is the field mask explicit or inferred? How is clearing expressed?
10. Which relationships are traversable in which direction?
11. Are embedded related records live or cached, and with what staleness bound?
12. Which arrays have a contracted order?
