# Pagination mechanisms and what each guarantees

Read at steps 1-5 and 9. Contents: [the mechanisms](#the-mechanisms) ·
[what each guarantees](#what-each-guarantees) · [the termination rule](#the-termination-rule) ·
[token lifetime and restart](#token-lifetime-and-restart) · [page size](#page-size) ·
[reconciliation without vendor counts](#reconciliation-without-vendor-counts) ·
[the walk checklist](#the-walk-checklist)

## The mechanisms

**Offset / limit.** The request names a starting row number. Simple, and the only one that supports
jumping to an arbitrary page — which is why vendors keep it and why user interfaces like it.

**Last-seen cursor.** The request names the last record seen; the server continues after it,
usually by an indexed sort key. Avoids the shifting-window problem for inserts before the cursor.

**Opaque token.** The server returns a token encoding its own continuation state. Correctly built,
it is *encrypted* rather than encoded, so consumers cannot depend on its contents and the vendor
stays free to change the implementation.

**Keyset / range partitioning.** Not a vendor mechanism so much as one you impose: split the
collection by a stable attribute (date range, identifier range) and walk each partition
independently. This is the only one that parallelises.

## What each guarantees

| Mechanism | Stable under concurrent insert | Stable under concurrent delete | Parallelisable | Resumable | Random access |
|---|---|---|---|---|---|
| Offset / limit | **no** — re-reads records | **no** — skips records | yes | yes | yes |
| Last-seen cursor | mostly | mostly | no | yes, if the cursor is stored | no |
| Opaque token | unspecified | unspecified | no | only until expiry | no |
| Keyset partitioning | within partition | within partition | **yes** | yes | yes |

The critical column is the first two. Offset pagination over a mutating collection is *wrong* in a
specific, quantifiable way: insert two records at the head while you walk two at a time, and your
next offset points back inside a page you already read. Deletions do the mirror. Neither raises an
error, and the damage is proportional to how long the walk takes and how active the collection is.

"Unspecified" for opaque tokens is not pedantry. The token hides the mechanism, which means it also
hides which of these behaviours you have. Run the token diagnostic (`scripts/inspect_page_token.py`)
rather than assuming the wrapper implies the guarantee.

## The termination rule

**Stop when the vendor stops returning a next-page token. Never on row count.**

The requested page size is a maximum, not a target. A server working to a latency budget scans
until its cutoff and returns what it has — which can be fewer rows than requested, or none, with
matching records still ahead.

The shape that breaks count-based termination: a handful of matches, then an enormous run of
non-matching rows, then more matches. A page-size-10 request over that returns the first few rows
plus a token. A loop that stops on `len(page) < page_size` stops there and reports success.

This is invisible on dense test data and appears on sparse or heavily filtered production data,
which is the worst possible distribution of when-you-find-out.

## Token lifetime and restart

Token lifetime is the most commonly undocumented field in this whole area. Where it is documented
it is short — minutes; an hour counts as generous.

Vendors are relaxed about this because they treat paging as idempotent, so an expired token "just
needs a retry". From your side, **retry means re-running the entire walk from the beginning.**
There is no resume, and for a large extract that can mean it never completes.

Design order:

1. **Chunk by a stable filter** so each chunk completes well inside the token lifetime.
2. **Checkpoint by business key**, not by token, so a restart skips completed chunks.
3. Only then consider one long walk, and only with a measured lifetime.

Token pagination is also strictly sequential: no page numbers, no paging backward, and no
parallelism, because a second worker cannot obtain a starting token without walking to it. If the
extract must be parallel, partition by filter — that is a decision made at design time, not a
tuning knob later.

## Page size

Common defaults are small: often 10, sometimes 100 for very small items, and 10–25 where items are
kilobytes, because sensible vendors size by response *bytes* rather than row count.

Omitting the page-size field gets you the default. At 10 rows per call, a million-record extract is
100,000 sequential round trips — the difference between minutes and days.

Set it explicitly, then verify the vendor honours it. The maximum belongs to them.

## Reconciliation without vendor counts

A total-results count is a display value. Past a certain collection size, counting is either slow or
approximate, and vendors choose approximate. Where one is exposed, assume it is an estimate,
produced by a different code path than your pages, at a different instant. Reconciling against it
generates mismatches that mean nothing.

Reconcile against things you can defend:

**Continuity.** This run's count against last run's count plus the changes you were told about.
Divergence is a signal even when you cannot say which side is wrong.

**Sampling.** Re-read a random subset by identifier and compare field by field. Cheap, and it
catches translation bugs that a count never will.

**Vendor-computed aggregates.** A checksum, digest, or per-window count endpoint is computed on
their side over their data — that is exactly the property a total-results estimate lacks. Prefer
these where they exist.

**A second path.** Where the vendor offers both an export and a list API, periodically compare them.
Two wrong answers rarely agree.

Set an alerting threshold on the reconciliation, and make sure someone owns the alert. An unowned
reconciliation is a job that turns red and gets muted.

## The walk checklist

- [ ] Pagination mechanism identified, and the token diagnostic run
- [ ] Termination is on the token, not the row count
- [ ] Page size set explicitly, and the vendor verified to honour it
- [ ] Token lifetime measured, not assumed
- [ ] Walk chunked so each chunk fits inside the token lifetime
- [ ] Checkpointing by business key, so a restart resumes
- [ ] Consistency model written down in one sentence
- [ ] Canary filter in place alongside the real filter
- [ ] Credential recorded, and its visibility scope understood
- [ ] Arrays treated as unordered unless a position field exists
- [ ] Soft-delete behaviour established for both get and list
- [ ] Reconciliation defined against something other than the vendor's total
- [ ] Alerting threshold set, and an owner named
- [ ] Every query bounded
- [ ] Destructive operations guarded against an empty filter
