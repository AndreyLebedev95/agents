---
name: plan-vendor-data-extraction
description: Plans a correct bulk read, backfill, nightly sync or migration out of a third-party or purchased core, where the characteristic failure is silent wrongness rather than an error. Covers why a short page does not mean the last page, why an opaque page token is not a consistency guarantee and most page walks are a smear rather than a snapshot, why a total-results count is a display value and never a control total, page tokens that expire with no way to resume, offset pagination over a mutating collection skipping and duplicating records, filters that are hermetic and cannot reach related records, a misspelled filter field returning zero rows and success, arrays that are unordered until proven otherwise, soft deletion making get and list disagree, and why the extract cadence is the staleness window and needs a stated conflict rule. Use when designing a full extract or nightly sync or migration from a vendor system, when walking a paginated vendor list, when a report's numbers do not match the vendor's, when deciding how to detect changes, or when reconciliation is failing — even when the ask is only "can we just pull all the records". For the event or webhook path use pin-down-vendor-event-delivery; for the API surface generally use document-vendor-api-surface; for translating the records you extract use design-vendor-anticorruption-layer.
---

# Planning a correct extract from a vendor core

Reading data out of a bought system is the task where **nothing fails**. The job runs green, the
row count looks plausible, and the data is wrong. Every mechanism below produces missing or
duplicated records without raising an error, which is why this needs a plan rather than a loop.

The plan's job is to state, in writing, three things nobody usually writes down: **what
consistency the extract actually has**, **how it terminates**, and **how we would know if it were
wrong**.

## The one-paragraph version

Terminate on the token, never on the row count. Assume your walk is a smear across time, not a
snapshot. Never use the vendor's total as a control total. Assume a filter that matches nothing is
indistinguishable from a filter that is broken. Assume arrays are unordered and identifiers may be
scoped to your credential. Then design reconciliation that does not trust any of the above.

## Procedure

### 1. Identify the pagination mechanism — and run the free diagnostic

Ask the vendor, then verify independently, because the documentation is often aspirational.

**The diagnostic:** base64-decode the vendor's next-page token. A properly built token is
*encrypted*, not merely encoded, precisely so consumers cannot see or depend on its contents. So if
decoding reveals something like `{"offset": 10}` or a readable row key, you are on offset
pagination wearing a costume, and you inherit every offset bug below.

`scripts/inspect_page_token.py` does this and reports what it finds.

`references/pagination-and-consistency.md` has the mechanism-by-guarantee table — read it now, and
again at step 9, because which mechanism you are on decides what reconciliation has to prove.

Offsets are the worse case, and the mechanism matters: insert two records at the head of a
collection while you are walking it, and your next offset points back inside a page you already
read — you see records **twice**. Deletions do the mirror and you **skip** records entirely. A
last-seen-record cursor avoids that specific shape; an opaque token may or may not.

### 2. Terminate on the token, never on the count

**The requested page size is contractually a maximum, not a target.** A server working to a latency
budget scans until its cutoff and returns whatever it found by then. Asking for 10 can legitimately
return 5, or 1, or zero — with plenty of matching records still ahead.

The pathological shape is real and worth picturing: five matches, then five billion non-matching
rows, then six more matches. A page-size-10 request over that collection returns five rows and a
token, and any loop that stops when `len(page) < page_size` stops there, having read five of eleven
records, reporting success.

The bug only appears on sparse or filtered data, which is why it survives testing and detonates in
production.

**Terminate when the vendor stops giving you a next-page token. Nothing else.**

### 3. State the consistency model out loud

Any multi-record read a vendor performs without a point-in-time snapshot produces a **smear**: data
gathered across a stretch of time, in which early records are older than late records, and no
single instant of the source ever looked like your result.

This is the honest description of most vendor exports and full extracts. A smeared extract can
contain a parent without its child, or a child whose parent has since changed — not because
anything failed, but because the two were read minutes apart.

An opaque token does not fix this. It fixes the offset-shifting bug specifically. Consistency is a
separate property that a vendor must promise explicitly, and almost none do.

Write the consistency model into the plan in one sentence: *"This extract is a smear over
approximately N minutes; downstream logic must not assume referential integrity within it."*
Everything downstream is entitled to know that.

### 4. Plan for token expiry, because there is no resume

Token lifetime is the field vendors most often leave undocumented, and where it is documented it is
short — minutes, with an hour described as generous.

Designers are relaxed about this because they consider paging idempotent, so an expired token
"just requires a retry". From the consuming side that is severe: **retry means re-issue the whole
walk from the beginning.** There is no resume.

For a large extract this is the difference between a job that finishes and one that never does.
Mitigations, in order:

1. Chunk the walk by a stable filter (date range, key range) so each chunk is short enough to
   complete inside the token lifetime, and each chunk can be retried independently.
2. Checkpoint by business key rather than by token, so a restart can skip completed chunks.
3. Only then consider a single long walk, and only if you have measured the token lifetime.

Related constraint: **token pagination is strictly sequential.** No page N, no paging backward, no
parallelism — worker two cannot obtain a starting token without walking there itself. If the
extract must be parallel, it must be partitioned by filter, and that is a design decision made
here, not later.

### 5. Set the page size deliberately

Default page sizes are small — commonly 10, sometimes 100 for tiny items, and 10–25 for items
measured in kilobytes, since sensible vendors size by response bytes rather than row count.

A request that omits the page-size field gets that default. **A million-record extract at 10 rows
per call is a hundred thousand sequential round trips**, and at any realistic latency that is the
difference between a job measured in minutes and one measured in days.

Set it explicitly. Then verify the vendor honours it — the maximum is theirs, not yours.

### 6. Establish what filters can and cannot see

**Filters are hermetic.** A well-built filter evaluates against exactly two inputs — the expression
and one resource — and is forbidden from reaching other resources. So a field holding an identifier
of a related record cannot be dereferenced: if the vendor's contact record stores an account id
rather than an embedded account, **filtering contacts by account name is not a supported query and
never will be.** That is a capability gap, not a syntax problem, and it belongs in the capability
report.

**A broken filter and an empty result look identical.** Lenient filter evaluation is the common
behaviour: a misspelled field resolves to undefined, never equals anything, and the call returns
success with zero rows. A type mismatch does the same. So *zero rows is not evidence of zero
matching records.*

Defend with a **canary filter**: alongside the real query, run one whose expected result is known
to be non-empty. If the canary returns nothing, the filter path is broken, not the data. This costs
one extra call per run and is the cheapest insurance in the whole plan.

### 7. Establish visibility and ordering

**A vendor list returns what your credential can see, not what the collection contains.** Different
callers listing the same collection get different views, and partial visibility is normal and
usually unavoidable. So every list-based extract is a statement about a credential rather than
about the vendor's data. Record which credential produced the extract, and expect the counts to
change if it is ever rotated to one with different scope.

**Treat every array as unordered until proven otherwise.** Ordering that holds in testing is
frequently incidental — a consequence of storage layout that changes with version, sharding or
volume. Where order genuinely matters, look for an explicit position or priority field on each
element rather than relying on array position.

### 8. Choose change detection, and set the cadence knowing what it is

**The cadence is the staleness window.** It is not a scheduling detail: it is the maximum age of
every downstream decision made on this data.

It is also the width of the window in which **the same entity can be changed divergently on both
sides with no way to tell afterwards which change is true.** Two systems both accept an address
change the same day, one records it wrong, and now two addresses exist with equal claim to being
current.

So the cadence decision requires a stated **conflict rule** alongside it: which side wins, on what
evidence, and who is told. A cadence chosen without a conflict rule is an unresolved data-integrity
decision that will be made accidentally, later, by whichever code happens to run last.

Also confirm there is a bulk path at all. An event stream carries the delta, not the initial load —
chopping a large one-time transfer into a very large number of small messages loses badly to a bulk
export. If no bulk path exists distinct from the incremental one, cold start and backfill have no
supported route, and that is a hard constraint on the whole design.

### 9. Design reconciliation that does not trust the vendor's counts

**A total-results count is a display value, never a control total.** Past a certain collection size,
counting is either slow or a guess, and vendors choose the guess. Where a total is exposed at all,
assume it is an estimate, computed by a different code path than the one producing your pages, at a
different instant. Reconciling your extract against it will produce mismatches that mean nothing
and consume real time.

Reconcile instead against something you compute:

- Count what you received, and compare to what you received *last* run plus the changes you were
  told about.
- Sample: re-read a random subset by identifier and compare field by field.
- Where the vendor offers a checksum, digest or per-window count endpoint, use that — it is
  computed on their side over their data, which is the property you need.

**Account for soft deletion**, which makes get and list disagree in both directions. A read of a
soft-deleted record typically returns success and the full resource rather than a not-found, so an
existence check cannot distinguish live from deleted unless you read the deleted flag explicitly —
and any "does it still exist" logic in your translation layer is wrong. Meanwhile the list view
usually excludes them. So the same record is simultaneously present and absent depending on how you
ask, and your counts are wrong in whichever direction you did not think about.

### 10. Bound the result set

The standard shape — query, loop, build an object per row — has no upper bound, so the far side
decides how much memory you allocate. Development and test datasets are always small, so this is
invisible until production.

Reframed correctly this is a **handshaking failure**: the caller allowed the other system to
dictate terms. In any protocol the caller should state how much it is prepared to accept. Bound
every query, and treat "there is no limit clause available" as a finding rather than a fact of life.

Batch endpoints deserve their own check: **batch operations do not paginate**, and instead carry an
upper limit chosen by *response size* rather than a round number — so the real cap depends on how
fat each record is. A bulk load that works in test with slim records fails in production with fat
ones. Find the cap before the load, not during it.

Where a batch create has the vendor assigning identifiers, note that **response ordering may be the
only thing linking a created record to your input**. If the vendor does not state that order is
preserved, your fallback is a field-by-field comparison of every submitted record against every
returned one.

### 11. Guard destructive operations

**An unset filter on a destructive operation means all records, not none.** Filter semantics are
deliberately identical between a list and a criteria-based delete — and since an empty filter on a
list returns everything, an empty filter on a purge deletes everything. Vendors generally cannot
reject the empty filter without breaking that consistency, so expect that they do not. The
realistic failure is not a malformed expression; it is a filter variable that ended up empty.

Where a preview-then-confirm option exists, use it, but know its limit: **the set matched at
preview and the set acted on at execution are computed independently, and no vendor can guarantee
they agree.** Making execution fail on any change would render it useless on a live collection.

## Output format

```
# <System> extract / sync plan

## What this extract is
<scope, source, credential used, and the one-sentence consistency statement>

## Pagination
<mechanism, token diagnostic result, page size chosen, termination condition,
 token lifetime, chunking strategy>

## Consistency model
<smear or snapshot; the window; what downstream must not assume>

## Filters
<expressions used, what cannot be filtered on and why, the canary filter>

## Change detection and cadence
<method, cadence, the staleness window it implies, and the conflict rule>

## Reconciliation
<what is compared against what — explicitly not the vendor's total; sampling
 method; alerting threshold>

## Failure and restart
<what happens on token expiry, partial failure, and how a re-run is made safe>

## Known gaps
<anything that cannot be extracted, and anything whose correctness cannot be proven>
```

## Failure modes

| Tell | What is actually happening | Fix |
|---|---|---|
| Extract silently short, only on some runs | Loop terminated on row count | Terminate on the token |
| Records missing or duplicated in a full extract | Offset pagination over a mutating collection | Decode the token; chunk or freeze |
| Counts never reconcile | Vendor total used as a control total | Reconcile against something you compute |
| A long extract dies partway and restarts from zero | Token expired; there is no resume | Chunk by filter; checkpoint by business key |
| A list we already consumed got shorter | Vendor added pagination to a previously unpaginated list | Assert on token presence; alert on shape change |
| A filter returns nothing and nobody notices | Broken filter and empty result are identical | Canary filter with a known non-empty result |
| Deleted records still counted, or missing | Soft delete makes get and list disagree | Read the deleted flag explicitly; state which view each call returns |
| Production query exhausts memory | Unbounded result set; test data was small | Bound the query; caller states how much |
| A bulk load fails only in production | Batch cap is sized by response bytes, not row count | Find the cap with realistic record sizes |
| Two systems hold different truths for one record | Cadence set with no conflict rule | State the conflict rule with the cadence |

## Related work

- The event/webhook path, and replay windows → `pin-down-vendor-event-delivery`
- Identifier stability, which reconciliation depends on → `document-vendor-api-surface`
- Queries the core can never answer → `report-vendor-capability-gaps`
- Translating extracted records → `design-vendor-anticorruption-layer`
- Proving the vendor's pagination behaves as documented → `probe-vendor-contract-empirically`
