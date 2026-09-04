# Operating through the mixed-version window

Read at step 7, whenever a vendor version change or your own rollout means two versions are live
at once — which is always.

Contents: [the window is unavoidable](#the-window-is-unavoidable) · [the version discriminator](#the-version-discriminator) ·
[the mixed-version test](#the-mixed-version-test) · [expand then contract](#expand-then-contract) ·
[trickle then batch](#trickle-then-batch) · [old data](#old-data-that-todays-code-could-not-create) ·
[deployment as a span](#deployment-is-a-span-not-an-instant)

## The window is unavoidable

A clean cutover is impossible **in principle**, not merely difficult to organise:

- Some components convert before others.
- Some rarely-used consumers never convert at all.
- Even if everything could switch at one instant, every channel would first have to be drained of
  in-flight messages in the old format.

So plan the window rather than enduring it. Decide its duration deliberately, state it, and know
what is true while it is open.

## The version discriminator

The prerequisite for any breaking change is a **version of the format** — not of the application —
carried in the request and reply messages themselves. Its purpose is primarily **debuggability**:
when something behaves strangely you can tell which format it was speaking. It is not usually a
bridging mechanism, since a given consumer typically supports one version at a time.

Where the discriminator lives is a real choice with real trade-offs:

| Location | For | Against |
|---|---|---|
| URL path prefix | trivially routable; visible in every log and trace | the identifier for a thing changes with version, so "the same" record has two addresses |
| Query parameter | routable; keeps the resource identity stable | easy to omit accidentally, and defaults then decide |
| Header | keeps identity and path clean | invisible in most logs; easy to lose through proxies |
| Content type | technically the most correct place | poor tooling support; frequently mangled |

Pick one and **apply it to every route at once**. A mixed scheme means nobody can tell what version
a given call is on without reading code.

Convert old requests up and new responses down **in the controller**, not by forking the business
logic. Forked business logic is how a mixed-version window becomes permanent.

## The mixed-version test

**Create entities through the new path, then read them back through the old one.**

This is the test almost nobody runs, and it is where the failures actually are. It is skipped for a
structural reason: each path passes its own tests. The new code is tested against new data; the old
code was tested against old data. Nothing tests new data against old code, which is precisely the
combination the window produces.

The characteristic failure is that entities created via the new interface return errors through the
old one — a required field the old path does not know how to populate, an enum value it cannot map,
a nested structure it cannot flatten. In production this appears as errors confined to recently
created records, which is a confusing signal because the code that reads them did not change.

Run both versions side by side for a stated period, and run this test before the rollout rather
than after.

## Expand then contract

For schema change with no downtime, split the work around the code rollout.

**Expansion, applied before the code rollout.** Only changes the *current* application will not
use: add a table, add a view, add a nullable column, add aliases or synonyms, add stored procedures
or triggers, and copy existing data into the new structures. The criterion is the whole rule:
**nothing added in this phase may be used by the running version.** That is what makes the phase
safe to apply while the old code is live.

Write **shims in both directions** — for insert, update and delete — for any structure being split
or merged, so writes through either shape land correctly in both.

**Contraction, after the rollout.** Remove the old structures and the shims, only once no old
instances remain.

Put a migrations framework under programmatic version control of the schema, forward *and*
backward, before any of this. A migration you cannot reverse is a deployment you cannot abort.

## Trickle then batch

For a data migration too slow to run inside a deployment window:

1. **Deploy code that reads both shapes**, before touching any data.
2. **Convert each record as it is touched**, writing back the current shape. This amortises the
   migration across many requests as a little extra latency each, rather than one long outage.
3. **Let it run** until the active working set has converted — weeks, typically.
4. **Batch-migrate the cold remainder** later. This is now safe to run concurrently with production
   precisely because no old instances remain.
5. **A final deployment removes the conditional** version-handling code.

The ordering is the point: code before data, always. Data migrated ahead of code is data the
running application cannot read.

## Old data that today's code could not create

Any store in production for years holds records that survived a succession of schema changes,
administrative interventions and application versions. Some of it **cannot be produced by the
application as it exists today**: users predating a required field and having none, accounts
untouched for a decade holding nulls where current code marks the field mandatory.

The consequence for a migration is direct: a migration written against the current model's
assumptions will fail on the oldest records, which are often the most sensitive and the least
replaceable.

**Test every migration against the oldest records you have**, not against a fresh sample. Where the
oldest records cannot satisfy current invariants, decide explicitly — quarantine, backfill with a
recorded sentinel, or relax the invariant — rather than letting the migration decide by crashing.

## Deployment is a span, not an instant

Most designs describe the system *after* a release, quietly assuming the whole system changes in an
instantaneous jump. It does not. Users experience *during*.

Four measurable phases, per instance, worth measuring separately in production-like conditions:

- **Prepare** — copying files and warming anything that can be warmed while the old version still
  serves.
- **Drain** — letting in-flight work finish. Choose an explicit **time limit** rather than waiting
  for all sessions to end; at scale, predictability beats completeness.
- **Apply** — the switch itself.
- **Ready** — until the instance can actually serve. Gate the load balancer on a **real readiness
  signal**, not on the process having started.

For a vendor integration specifically, the question to answer is what happens to **your** in-flight
calls during **their** window, and whether their readiness signal is one you can observe at all.
Usually it is not, which makes their upgrade window a period during which your retry and
circuit-breaking behaviour is the only thing protecting you.
