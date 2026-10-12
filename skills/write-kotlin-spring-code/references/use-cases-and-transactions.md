# Use cases, ports and transactions

## Use cases

- One class per operation or job, with one public method. It opens the transaction, loads through
  outbound ports, calls the domain, saves, and writes any outbox row.
- Authorisation is decided before the use case runs, unless the project places it inside.
- The use case returns a domain result type. It never returns an HTTP status or a wire DTO.
- The controller reaches the use case through an interface (the use-case port), so a slice test can
  replace it with a fake.

## Ports

- A port is a Kotlin `interface` in the project's types: domain types and plain values, never a jOOQ
  record, a generated client type or a Spring type.
- Name a port after what the caller needs (`findOpenOrders`), not after the storage.
- When the project marks port kinds — read-only query ports and state-changing command ports — mark
  every new port. A query port changes nothing and takes no row lock.
- When two modules would depend on each other, the caller declares the port in its own API and the
  callee implements it.

## Transactions

- `@Transactional` sits on the public method of the use case, not on the controller and not on the
  repository. Read-only work uses `readOnly = true`.
- Set `propagation` only by the project's rule for that kind of port. Never use `REQUIRES_NEW` unless
  the project allows it: it suspends the outer transaction and holds a second connection.
- Use one transaction mechanism. With Spring's `@Transactional` in place, do not open jOOQ's
  `dsl.transaction { }` as well.
- Keep a transaction short. No call to another system, file upload or sleep inside it. Work another
  system must do travels as an outbox row written in the same transaction.
- Remember the traps from the main skill file: self-invocation skips the proxy, and a checked exception
  commits.

## Locks

- Take row locks through jOOQ (`forUpdate()`, `forNoKeyUpdate()`, `skipLocked()`), never in plain SQL.
- When one transaction locks several rows of a table, lock them in ascending key order:
  `orderBy(T.ID).forUpdate()`.
- When it locks rows in several tables or schemas, follow the project's stated lock order. If the
  project states none and you need two, report it; do not invent one.
- A deadlock victim is retried by the project's mechanism, not by a loop of your own.

## Outbox and asynchronous work

- An outbox row is written in the same transaction as the change it announces.
- A consumer of an outbox row is idempotent: delivering the row twice changes state once. Key the
  effect on the row's identifier or a deterministic key.
- Order and retry belong to the relay. A consumer does not sleep, poll or re-enqueue by hand.
