# HTTP adapter

## Controllers

- A controller maps and delegates, nothing else: request type to use-case input, use-case port call,
  result to response type. No business rule, no repository call, no transaction.
- Follow the project's granularity (for example one controller per operation) and carry every
  per-operation annotation the project requires.
- Build domain values from request members through the domain's factories. A refusal there is a
  validation error in the project's error format, not an exception that escapes as `500`.
- Map a sealed use-case result to a status with an exhaustive `when`, so a new case breaks the build:

```kotlin
return when (val result = cancelOrder.cancel(OrderId(id), by = caller)) {
    is CancelResult.Cancelled -> ResponseEntity.ok(result.order.toResponse())
    is CancelResult.AlreadyShipped -> problems.conflict("already-shipped")
    CancelResult.NotFound -> problems.notFound()
}
```

  `problems` stands for whatever helper the project uses to build its error responses.

## Request and response types

- Request and response types are their own `data class`es in the adapter. Never expose a domain type,
  a jOOQ record or a generated client type on the wire.
- In a code-first contract, the Kotlin types are the published schema. A property's name, type,
  nullability, default and enum values are contract. Renaming, retyping, making a member required or
  adding an enum value is a contract change; regenerate and check the published document as the
  project requires.
- Nullable means optional in the schema; non-null means required. Do not make a member nullable to
  dodge a binding error.
- Bean Validation annotations on constructor properties need the right target; see the main skill file.
  Mark nested objects and list elements `@Valid` (with `@field:` when the target flag is absent).
- A `Boolean` property whose name starts with `is` may serialize under a name you did not expect. Check
  the generated schema; pin the name with `@JsonProperty` when the contract fixes it.
- Instants, identifiers and paging tokens use the project's shared wire helpers, not ad hoc formatting.

## Errors on the wire

- Errors use the project's problem format (often RFC 9457 `ProblemDetail`) through its shared helper
  and its global handler. Do not build an error body by hand in a controller, and do not add another
  `@ControllerAdvice`.
- Binding and deserialization failures (a missing required member, a wrong type) must reach the same
  handler and format. Check that a new request type's failures do.
- A problem's text never echoes a secret, a password, key material or a personal identifier from the
  request.

## Jackson

- On Spring Boot 4, Jackson 3 is the default: its classes live under `tools.jackson.*`, while its
  annotations stay under `com.fasterxml.jackson.annotation`. Copy imports from a neighbour.
- Kotlin classes without a no-argument constructor need the Kotlin module on the classpath; the project
  provides it.

## Logs and metrics in adapters

- No secret, password, key material or personal identifier in a log line, an exception message or a
  metric label.
- No metric label whose values grow with the data (an entity identifier, a user name). Use the
  project's telemetry helpers.
