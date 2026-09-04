# What the test harness must be able to inflict

Read at step 2, and when specifying a gateway stub. This is the concrete work item behind "test the
failure path".

Contents: [why a harness and not a mock](#why-a-harness-and-not-a-mock) · [the thirteen](#the-thirteen-misbehaviours) ·
[above the socket layer](#above-the-socket-layer) · [implementation notes](#implementation-notes) ·
[the pass rubric](#the-pass-rubric)

## Why a harness and not a mock

A mock object can only be trained to produce behaviour that **conforms to the defined interface**.
A test harness runs as a separate server and is **not obliged to conform to anything** — it can
provoke network errors, protocol errors and application errors that the interface does not admit.

The failures that take integrations down are, definitionally, the ones no interface admits. So if
all your low-level tests pass against something that is trying to be correct, you have tested
nothing about the boundary.

A conventional integration environment has the same ceiling. The system at the other end is trying
to behave, so only the last category below — application logic — is reachable from it at all.

## The thirteen misbehaviours

Four categories. Only the last is reachable from a normal integration environment.

**Network transport**

1. Refuse the connection.
2. Leave the connection sitting in the listen queue until the caller times out.
3. Reply with a connection acknowledgement and then never send data.
4. Send nothing but resets.
5. Report a full receive window and never drain the data.

**Network protocol**

6. Establish the connection and never send a byte.
7. Establish the connection but lose packets, causing retransmit delays.
8. Never acknowledge a packet, causing endless retransmission.

**Application protocol**

9. Send a response header naming a content length that disagrees with the body actually sent.
10. Send a response far larger than expected — including large enough to exhaust memory.
11. Send a content type that is not what the payload actually is.

**Application logic**

12. Send a well-formed response containing an application-level error.
13. Send a stale or duplicate response — one belonging to an earlier request, or a second copy of
    one already delivered.

**The three most commonly untested are 6, 3 and 13.** Number 13 deserves particular attention
because it is the only one that produces *wrong answers* rather than errors: a stale reply arriving
on a shared reply path is consumed as though it answered the current request, and nothing anywhere
reports a problem.

## Above the socket layer

An HTTP-style integration inherits every socket failure and adds its own, and these arrive as
protocol violations rather than as well-formed error responses:

- The provider accepts the connection but never responds to the request.
- **The provider accepts the connection but never reads the request.** This one is non-obvious and
  worth understanding: a large request body fills the provider's receive window, which fills your
  send buffer, which blocks your socket write — so with a slow provider even *sending* can never
  finish, long before any response is involved. Code that carefully bounds the response wait and
  ignores the send is still exposed.
- A status code outside the documented set, which the caller has no handling for.
- An unexpected content type — very often an infrastructure error page in HTML where the contract
  promises structured data, delivered with a success status.
- A response that is a redirect, possibly looping.
- Declared compression that is not applied, or vice versa.
- Authentication succeeding but the response scoped to a different identity than expected.

The last two matter most for a purchased core behind someone else's infrastructure, because neither
produces an obvious error and both yield plausible, wrong data.

## Implementation notes

Two things keep this cheap:

**You do not need a full protocol implementation.** Most of the transport-level behaviours are
produced by a small socket server that accepts connections and then does something unhelpful —
sleeping, closing, or writing a fixed byte string. A few dozen lines covers items 1-6.

**Drive it from the harness, not from the test.** Give the harness a mode switch so a single test
can walk it through several misbehaviours in sequence, rather than standing up a separate fixture
per case. That is what makes it cheap enough to run in continuous integration rather than once
during a hardening sprint.

Where the vendor's client library sits between you and the socket, remember that the library is
part of what you are testing. Its internal pooling and timeout behaviour is exactly what these
tests are meant to expose, and it is frequently the least-hardened code in your process.

## The pass rubric

Decide this before running, so the outcome is a verdict rather than a discussion.

**Pass:** the caller slows down, then fails fast, then recovers once the far side returns to normal.
Errors are attributed to the right dependency. No work is silently lost.

**Fail:** any of —
- the caller crashes or hangs,
- work is lost with no record,
- the failure propagates to unrelated functionality,
- the caller does not recover after the far side returns,
- the failure is attributed to the wrong component (which costs hours during a real incident),
- the caller retries an operation whose outcome it cannot know to be safe to retry.

The last one is easy to miss and expensive: a harness that returns an ambiguous failure on a
state-changing call is testing whether your retry policy understands the difference between
"definitely did not happen" and "unknown".
