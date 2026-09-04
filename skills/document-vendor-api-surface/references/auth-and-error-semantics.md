# Auth model and error semantics

Read while working steps 6 and 7. Contents: [credential models](#credential-models) ·
[what a signature proves](#what-a-signature-proves) · [rotation and operations](#rotation-and-operations) ·
[the three retry buckets](#the-three-retry-buckets) · [errors that lie](#errors-that-lie) ·
[rate limits](#rate-limits) · [the interrogation list](#the-interrogation-list)

## Credential models

Distinguish **first-party** authentication — the caller proves identity directly to the system it
is calling — from **third-party**, where the caller presents a proof issued by someone else. A
third-party proof needs two checks that teams routinely conflate: that the proof is genuine, and
that it was issued for *this* audience. A valid token minted for a different service is still
valid; it is just not valid here.

Record for each credential: what identity it represents, what it is scoped to, where it is stored,
who can read it, when it expires, and what happens when it does.

Configured credentials leak from three places worth naming in the reference: the file itself, the
folder it sits in (permissions on the directory, backups, and the deployment mechanism that put it
there), and process memory dumps.

## What a signature proves

A shared secret or HMAC gives you **origin** and **integrity** — the request came from someone
holding the secret and was not altered in flight. It never gives **non-repudiation**, because both
ends hold the same secret and either could have manufactured the request. If a dispute over "did
you send this?" is foreseeable, a shared secret cannot settle it, and the reference should say so
before someone builds an audit story on top of it. The question that decides this is key
provenance — who generated it, who else holds it — not which algorithm is named.

A signature covers **a declared list of components, as bytes**. It does not cover the request's
meaning. Anything outside the declared list is unprotected: a header that is not in the list can
be altered freely, and two requests that differ only outside the covered set produce the same
signature. Record which components are covered, in order, and with what canonicalisation.

## Rotation and operations

If the system permits only one key per identity, rotation is a **hard cutover with no overlap
window**: there is no period during which both old and new credentials are valid, so every client
must switch simultaneously. That is an operational constraint with real cost, and it has to be
designed for well before the rotation date rather than discovered on it.

Where two keys can be live at once, record the maximum overlap period — it bounds how long a
staged rollout can take.

## The three retry buckets

Sort every error the system can return into three buckets:

**Safely retriable.** Transient conditions where the request provably did not take effect —
throttling, temporary unavailability, some connection failures. Retry with backoff.

**Definitely not retriable.** Conditions where the request will fail identically forever —
malformed input, forbidden, method not allowed, unimplemented. Retrying is pure load and delays
the real fix.

**Unknown outcome.** The middle bucket, and the only interesting one: you do not know whether the
work happened. Timeouts, gateway errors and dropped connections after the request was sent all
land here. This bucket is why idempotence matters — with it you can retry safely; without it you
must either reconcile or accept duplicate effects.

Vendor documentation essentially never labels the middle bucket. You have to assign it. Be aware
that the conventional client-error/server-error split is a guideline vendors break routinely, so
classify by observed behaviour rather than by status class.

## Errors that lie

**Indistinguishable classes.** If the system returns one error for conditions you must tell apart,
you cannot build a correct retry policy. Record it as a limitation rather than guessing, because a
wrong guess here produces either duplicate side effects or dropped work.

**Application failure dressed as system failure.** When a caller's malformed input and a genuine
fault return the same response, a user's typo counts toward whatever protective machinery you have
built for vendor outages — and a few bad requests can trip protection meant for a real failure.
Note every place the two are indistinguishable.

**Success responses containing failure.** An asynchronous operation's failure often arrives inside
a transport-level success, and a "done" flag deliberately does not mean "succeeded". Check the
result, not the envelope.

**Prose is not a contract.** Parsing an error message's text manufactures a contract the vendor
never made and will change without notice or version bump.

## Rate limits

Record the **dimensions** (per key, per identity, per endpoint, per tenant, concurrent versus
rate), the **window** and how it slides, and what happens **on breach** — rejection, throttling,
queueing, or silent dropping. Silent dropping is the one to hunt for, since it produces no error
at all.

Where the system returns a retry hint, honour it, but note the trap: a hint expressed as an
absolute date combined with clock skew on your side retries instantly, which is exactly the
behaviour the hint existed to prevent. Prefer a relative interval; if only a date is available,
clamp it to a sane minimum.

For backoff, the parameter that matters is not the base delay but the **jitter**: without
randomisation a fleet of clients that failed together retries together, re-forming into a herd
that keeps the system down after it would otherwise have recovered.

## The interrogation list

1. What identity does each credential represent, and what is it scoped to?
2. Is authentication first-party or third-party? If third-party, what audience check applies?
3. What components does the signature cover, in what order, with what canonicalisation?
4. Can two credentials be live at once? What is the maximum overlap?
5. What is the credential lifetime, and what is the failure mode at expiry?
6. Which errors are safely retriable, which never, and which leave the outcome unknown?
7. Are caller errors and system faults distinguishable?
8. Can an asynchronous failure arrive inside a successful response?
9. What are the rate-limit dimensions and windows?
10. On breach: reject, throttle, queue, or drop silently?
11. Is there a retry hint, and is it relative or absolute?
