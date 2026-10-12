# Domain code in Kotlin

The domain is pure Kotlin. Its imports hold no Spring, no jOOQ, no Jackson, no `jakarta.*`. It reads no
clock and does no I/O. Time and anything else from outside arrive as arguments.

For deciding which states a type must exclude, use the `make-illegal-states-unrepresentable` skill. This
file covers how to spell those decisions in Kotlin.

## Contents

- Closed sets of cases
- Checked constructors
- Value types
- Expected refusals are values, not exceptions
- Producible only by one step
- Where the guarantees stop

## Closed sets of cases

```kotlin
sealed interface Delivery {
    data class Scheduled(val at: Instant) : Delivery
    data class Sent(val at: Instant, val receipt: Receipt) : Delivery
    data object Cancelled : Delivery
}
```

- A field that exists in one case only lives in that case, non-null. No status enum beside nullable
  fields.
- Match with `when` as an expression and no `else`.
- A case with no data is a `data object`.

## Checked constructors

A constrained value is built only through a factory that can refuse it.

```kotlin
@ConsistentCopyVisibility
data class Quota private constructor(val limit: Int, val used: Int) {
    companion object {
        fun of(limit: Int, used: Int): QuotaResult = when {
            limit <= 0 -> QuotaResult.Invalid("limit must be positive")
            used !in 0..limit -> QuotaResult.Invalid("used must be within 0..limit")
            else -> QuotaResult.Valid(Quota(limit, used))
        }
    }
}
```

- A `data class` with a private constructor still exposes `copy()`, which skips the check. Annotate it
  `@ConsistentCopyVisibility`, or use a plain `class`. The compiler warns about the exposed `copy()`, and
  `allWarningsAsErrors` turns that warning into a failed build.
- `init { require(...) }` is enough for a rule whose breach is a programming error. A factory returning
  a result type is for input that can legitimately be wrong.

## Value types

```kotlin
@JvmInline
value class OrderId(val value: UUID)
```

- Wrap identifiers and constrained primitives, so two `UUID`s of different meaning cannot swap.
- Keep value classes inside the domain and the use-case layer. Adapters take and return plain types
  and map at the edge: frameworks that reach code by reflection (MVC binding, Jackson, jOOQ record
  mapping, MockK matchers) handle the mangled names of value-class functions unevenly.

## Expected refusals are values, not exceptions

A business refusal — not allowed now, limit reached, wrong state — is a case of a sealed result type
the caller must match. An exception is for a bug or an infrastructure failure.

```kotlin
sealed interface CancelResult {
    data class Cancelled(val order: Order) : CancelResult
    data class AlreadyShipped(val shippedAt: Instant) : CancelResult
    data object NotFound : CancelResult
}
```

Kotlin's own `Result<T>` carries a `Throwable` and loses the case; do not use it for business outcomes.

## Producible only by one step

When a type may exist only as the output of one step, such as an approval, give it an `internal`
constructor and keep its producer in the same Gradle subproject. `internal` is the unit Kotlin
enforces; there is no "only this function" visibility.

## Where the guarantees stop

Type guarantees hold for objects the domain builds. They do not hold where an object is built from
bytes:

- **Database rows.** Build the domain object through the same factory application code uses. A row
  that fails the factory is a loud error, never a default.
- **External payloads.** Parse into an adapter DTO whose fields are nullable, then translate. An enum
  value you do not recognise is an explicit error case, not an `else` branch.
- **Bulk scripts and migrations.** They bypass factories; the project's rules for them apply.

These boundaries are where tests are mandatory: one hydration test per aggregate, one parse test per
external payload.
