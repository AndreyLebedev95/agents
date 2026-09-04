# The four translation levels

Read at step 2, when decomposing the layer into stages. The discipline is one translator per
level, chained — not one translator per integration.

Contents: [why levels](#why-levels) · [level 1 transport](#level-1-transport) ·
[level 2 data representation](#level-2-data-representation) · [level 3 data types](#level-3-data-types) ·
[level 4 data structure and semantics](#level-4-data-structure-and-semantics) ·
[promotion](#promotion-making-fields-visible-to-the-infrastructure) · [wrapping and unwrapping](#wrapping-and-unwrapping) ·
[what this gives you](#what-this-gives-you)

## Why levels

Two payoffs, one obvious and one not.

The obvious one: chaining lets any single level be swapped without touching the others, and the
lower levels can be reused for every document arriving from the same source.

The one that earns its keep: **a mismatch can be located at a level instead of being called "the
mapping is wrong."** "Their date has no timezone" is a level-3 problem with a level-3 fix. "Their
'account' means something different from ours" is level 4 and cannot be fixed in code at all. Teams
without this vocabulary argue about mapping bugs that are actually modelling disagreements.

The level list is also the outline of what must be documented for any vendor interface.

## Level 1: Transport

Protocol and delivery mechanism — file drop, HTTP, a queue, a database connection, SFTP.

Mismatches here are bridged by an **adapter**, not by mapping code. Keep this distinction sharp: an
adapter changes how bytes arrive, and nothing about what they mean. If you find business rules in
your transport stage, they migrated from level 4 and will be invisible to everyone reviewing the
mapping.

Record: the mechanism, its failure modes, its ordering and delivery properties, and whether it is
push or pull.

## Level 2: Data representation

Wire format and syntax — the serialization format, character set, encryption, compression, check
digits, line endings, escaping.

This stage parses and renders. It should have no opinion about fields.

**Note the character set explicitly.** It is the single most commonly unstated part of a vendor
interface and produces corruption that appears months later in the small percentage of records
containing non-ASCII characters. "It works" is not evidence; a name with a diacritic is.

## Level 3: Data types

Field names, types, value domains, constraints, code values. The concrete work:

- Dates versus datetimes, and **timezone** — whether one is carried at all, and what a bare date
  means at a boundary.
- Numeric precision, scale, and rounding behaviour.
- **Units** on every numeric field.
- Whether the vendor's empty string means null.
- Code and enumeration values, where a value exists on both sides.
- String length limits and what happens on overflow — silently truncated or rejected.

This is where most *fixable* mismatch lives. Anything that survives this stage and still does not
map is a level-4 problem, and level-4 problems are not code problems.

## Level 4: Data structure and semantics

The shape of the entities and what they *mean*: cardinality, nesting, which entity owns which
attribute, and whether a concept on one side corresponds to a concept on the other at all.

Two things belong here and nowhere else:

**Semantic dissonance.** Same word, different meaning. It passes every schema check. See the main
skill's step 4 for how to hunt it.

**Enumerations that partition differently.** If a value in their set spans two of yours, or a value
in yours has no counterpart, there is no total mapping and the residue is a capability gap.

This is the only level whose resolution requires **agreement between people** rather than a
technical mechanism. The first three can be solved by tooling; this one cannot, and treating it as
if it can is why integration projects stall in a way nobody can debug.

## Promotion: making fields visible to the infrastructure

Messaging infrastructure, routers, subscription filters and monitoring can generally only see
fields declared in a message's header. The moment one message is nested inside another, everything
in the inner payload becomes opaque.

So any field you need to route, correlate, filter, deduplicate or trace on must be explicitly
lifted from the body into the header. That lift is **promotion**, and it is a design decision with
a security consequence: a promoted field is visible to every intermediary along the path.

Procedure:

1. List the fields anything downstream needs in order to route, correlate, filter, deduplicate or
   trace.
2. Confirm each is in the header rather than the body; promote the ones that are not.
3. Note which promoted fields are now visible to intermediaries, and whether any of them should not
   be.

The inverse is also a tool: deliberately *not* promoting a field — or wrapping a message so
intermediaries cannot read it — is how you stop intermediaries depending on data they have no
business seeing. Fields nobody can see are fields nobody can build a hidden dependency on.

## Wrapping and unwrapping

Each stage that wraps a message must have a matching unwrap step, and the order must be exactly
reversed. Keep each wrap/unwrap pair independent, so a layer can be removed when its reason
disappears — encryption at this level, for instance, once the traffic moves onto a link that
already provides it.

Where a large payload passes through hops that do not need it, consider parking the payload in a
store and passing a reference. Be honest about what that buys: it does **not** reduce the bytes
that ultimately travel, only the marshalling, unmarshalling, encryption and decryption performed by
intermediate hops that have no use for the data. The benefit scales with the number of such hops
and is zero for a single hop — count them before adopting it.

Its under-advertised benefit is architectural: **intermediaries that never see a field cannot start
depending on it.**

The same mechanism bounds a third party. When work must leave your trust boundary, strip the
sensitive fields into a local store and hand the outside party an opaque reference in their place,
merging the data back when their response returns. Mint the reference per message rather than
exposing a business identifier, and make it single-use or expiring: a message the third party
fabricates or replays then carries a key that is invalid, expired or already used, and the merge
step rejects it before any business logic runs.

Decide the deletion policy explicitly — delete-on-read (single retrieval, right for sensitive
data), or expiry plus collection. A store with no deletion policy becomes a second, unmanaged copy
of your data.

## What this gives you

When something breaks, the level tells you who fixes it:

| Level | Broken by | Fixed by |
|---|---|---|
| Transport | infrastructure change, protocol deprecation | operations, adapter change |
| Representation | charset, format version, encoding change | parser change |
| Data types | field added, type widened, precision changed | mapping change |
| Structure and semantics | the vendor changed what something *means* | a conversation, then a model change |

A change that crosses from level 3 into level 4 is the one to escalate. It is not a bug; it is the
vendor altering the meaning of the contract, and it belongs in a change impact assessment rather
than a defect queue.
