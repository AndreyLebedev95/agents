# Hardening the layer against a misbehaving vendor

Read when reviewing an existing anti-corruption layer, or when specifying what the gateway stub
must be able to do. The premise: the layer's job is not only to translate a well-formed vendor
response but to be the place where a badly-formed one stops.

## The thirteen misbehaviours the layer must survive

A stub or harness that only reproduces the happy path proves nothing about the boundary. Each of
these has taken down a real integration, and each should be reproducible on demand:

1. Refuse the connection.
2. Accept the connection but never respond.
3. Accept the connection, send back a single byte, then stall.
4. Respond after a delay far longer than any timeout.
5. Send a response much larger than expected — including one large enough to exhaust memory.
6. Send a well-formed response with the wrong content type.
7. Send content that is not what the declared type says (plain text where JSON is promised; binary
   where text is promised).
8. Send a valid response, then close the connection mid-stream on the next request.
9. Close the connection immediately after accepting it.
10. Reset the connection mid-response.
11. Send a response with a valid envelope and an error inside it.
12. Send a duplicate response to a single request.
13. Send a response to a request that was never made, or a stale response belonging to an earlier one.

The three most commonly untested are 3, 4 and 13 — and 13 is the one that produces wrong answers
rather than errors, because a stale reply on a shared reply path is consumed as though it answered
the current request.

## Additional betrayals above the socket layer

A connection can be perfectly healthy at the transport level while the exchange fails:

- The declared content length disagrees with the body actually sent.
- The response is chunked and a chunk never arrives.
- The character set is not what was declared, or is not declared at all.
- A redirect points somewhere unexpected, or loops.
- Compression is declared and the payload is not compressed, or vice versa.
- The response is an error page from an intermediary — a proxy or gateway — rather than from the
  vendor at all, with a success status attached.
- Authentication succeeds but the response is scoped to a different identity than expected.

The last two matter most for a purchased core sitting behind someone else's infrastructure, because
neither produces an obvious error and both yield plausible, wrong data.

## Review checklist for an existing layer

- [ ] Is there a component that both sides are ignorant of, or only a renamed interface?
- [ ] Does any domain code import from the integration package?
- [ ] Does any vendor exception type or error-code constant appear outside the gateway?
- [ ] Is the mapper keyed by message type rather than by entity?
- [ ] Does any consumer read a pre-translation, vendor-shaped message?
- [ ] Is the gateway interface declared separately from its implementation?
- [ ] Does a stub exist, and does it reproduce error and timeout behaviour rather than only success?
- [ ] Is there a timeout on every call **and** a bound on pool checkout time?
- [ ] Does every enrichment lookup have defined behaviour on failure and timeout?
- [ ] Is the character set stated explicitly at the representation stage?
- [ ] Are units stated for every numeric field?
- [ ] Does any enumeration mapping have a default or "other" bucket that was never escalated?
- [ ] Has the latency floor been calculated from the enrichment lookups on the critical path?
- [ ] Is there a documented list of stages deliberately collapsed for performance, and why?
