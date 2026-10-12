# Persistence with jOOQ and Flyway

## Contents

- Generated classes only
- Queries
- Hydration into the domain
- Writing
- Migrations

## Generated classes only

- Name every table, column, view and function through the generated classes. No plain-SQL API:
  `DSL.table(String)`, `DSL.field(String)`, `DSL.sql(String)`, `DSLContext.execute(String)`,
  `DSLContext.fetch(String)`.
- A repository reads its own schema's generated classes only, unless the project names an exception.
- After a migration changes the schema, regenerate the classes with the project's task before writing
  code against them. Do not hand-edit generated code.
- Inject `DSLContext`; the Spring Boot jOOQ starter binds it to the Spring transaction.

## Queries

- Single row: `fetchOne()` returns `R?` and throws on more than one row; `fetchSingle()` throws on zero
  rows too. Pick by what zero rows means.
- Lists: page with a keyset (`seek(...)` or `where(key > last)`), not `offset`, on any table that grows.
  Order by a unique key so pages are stable.
- Avoid one query per element of a list; fetch the set in one query (``where(T.ID.`in`(ids))``), then
  `associateBy`.
- Select the columns you map, not `selectFrom` of a wide table, when the read is hot.
- Use `Records.mapping` or explicit lambdas for mapping, not `into(Domain::class.java)`: reflection
  bypasses the domain's factory.

## Hydration into the domain

- Generated fields are nullable (Kotlin generator) or platform types (Java generator), even for a
  `not null` column. A platform type left to inference carries a `null` onward and fails far from the
  row. Read each field into an explicit Kotlin type and check it; a missing required value is a loud
  error naming the row's key.
- Build the domain object through its factory. A row the factory refuses is a data error: throw with
  the row's key. Never fall back to a default.
- `timestamptz` arrives as `OffsetDateTime` unless the generator is configured otherwise; convert to
  `Instant` in the adapter.
- A database enum or text code maps to a domain case with an exhaustive `when`; an unknown code is an
  error.

## Writing

- Many rows: one multi-row `insertInto(...).valuesOfRows(...)` or a batch, not a loop of single inserts.
- Upserts with `onConflict(...).doUpdate()` or `doNothing()`, when the effect must be idempotent.
- An update that must find its row checks the affected count and treats `0` as the case it means:
  not found, or a lost optimistic race.

## Migrations

- Flyway migrations are plain SQL, one versioned file per change, named by the project's pattern.
- Never edit a migration that has run anywhere; add a new one.
- A migration on a large table avoids long locks: add a nullable column, backfill in batches, then add
  the constraint. Create indexes the way the project allows on live tables.
- Every instant column is `timestamptz`.
- Every new table and column has a test path: the container tests run the migrations.
