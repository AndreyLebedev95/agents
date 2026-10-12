---
name: write-kotlin-spring-code
description: Writes and changes production and test Kotlin code in a blocking Spring Boot (Spring MVC) backend built as hexagonal modules over jOOQ and Flyway, tested with JUnit 5, Kotest assertions and MockK. Covers reading the build's decisions before writing, Kotlin idioms, a pure domain with checked constructors and closed result types, use cases and transactions, jOOQ repositories and migrations, thin controllers for a code-first contract, test forms with in-memory fakes, and the Kotlin-on-Spring traps that compile but misbehave. Use when implementing or fixing backend code in Kotlin on Spring Boot — a controller, use case, domain type, port, repository, migration or test. Not for choosing the stack or the architecture, and not for ticket process.
---

# Writing Kotlin on Spring

This skill holds Kotlin and Spring know-how only. It states no fact about any one project.

**The project's decisions win.** Its build files, architecture documents, conventions and existing code
override every rule below. Where a rule here conflicts with them, follow the project and report the
conflict in one line. Where the project states nothing, follow this skill.

## 1 · Read the decisions before writing

Do this once per task, before the first line of code.

1. **Build.** Read the version catalog, the convention plugins and each touched subproject's build file.
   Note:
   - the Kotlin, Spring Boot and JDK versions;
   - compiler plugins: `kotlin("plugin.spring")` (all-open), any `noarg` or `allOpen` setup;
   - `compilerOptions`: `allWarningsAsErrors`, `-Xjsr305=strict`, `-Xannotation-default-target`;
   - test libraries, and which libraries the build excludes from the classpath;
   - which test tasks exist and which tag separates slow tests.
2. **Architecture.** Find where the project states its layers, its port kinds, its transaction rules and
   its error format. Read the section that governs the layer you change.
3. **Neighbours.** Open the nearest existing class of the same kind — controller, use case, repository,
   test — and copy its shape: package, naming, imports, mapping, test form. On Spring Boot 4 the test and
   auto-configuration packages moved; copy imports from a neighbour, not from memory.
4. **Dependencies.** Add no library, plugin or subproject dependency the task does not demand. When one
   is unavoidable, name it and why in the report.

## 2 · Kotlin idioms

- `val` over `var`; read-only `List`, `Set`, `Map` in every signature; never hand out a mutable collection.
- No `!!` in production code. Use `?.`, `?:`, or `requireNotNull(x) { "why" }` and `checkNotNull`.
  A type is nullable only when absence means something.
- `require` for arguments, `check` for state, `error("…")` for the impossible branch.
- `when` over a sealed type or enum is an expression with no `else`, so a new case breaks the build.
- Named arguments when two parameters share a type; default parameters instead of overloads.
- Mapping as `private` or `internal` extension functions (`fun Row.toDomain()`), next to the adapter that
  uses them. Do not nest scope functions (`let` inside `also` inside `apply`).
- Narrowest visibility the build allows: `private`, then `internal` (one Gradle subproject is one Kotlin
  module), then public for what another subproject must see.
- `BigDecimal` compares with `compareTo`; `==` also compares scale.
- No `runCatching` around business flow: it catches every `Throwable`. Catch the one exception you
  handle, at the boundary that can handle it.
- Instants are `java.time.Instant`. Code reads time from an injected `Clock`, never from `Instant.now()`
  or `Clock.system*()`.
- With `allWarningsAsErrors`, every warning fails the build: an unused parameter, a deprecated call, an
  unchecked cast. Fix the cause; `@Suppress` only with a comment that names the reason.
- Blocking stack: no `suspend`, `Flow`, `Mono` or `runBlocking` unless the project already uses them.

## 3 · Kotlin-on-Spring traps

These compile and then misbehave at runtime.

- **Final classes.** Kotlin classes are final. Without the all-open `spring` plugin, `@Transactional`,
  `@Cacheable`, `@Async` and `@Configuration` proxies silently do nothing. Confirm the plugin is applied
  to the subproject before relying on a proxy.
- **Self-invocation.** A call from one method of a bean to another method of the same bean skips the
  proxy, so the callee's `@Transactional` does not apply. `private` methods are never proxied.
- **Rollback.** Spring rolls back on `RuntimeException` and `Error` only. A checked Java exception
  (`IOException`, `SQLException`) thrown through Kotlin code commits the transaction. Wrap it in an
  unchecked exception or declare `rollbackFor`.
- **Annotation targets.** On a constructor property, a Java annotation lands on the parameter only
  unless `-Xannotation-default-target=param-property` is set. Without that flag, write `@field:NotBlank`
  and `@field:Valid`. With it, the plain form works. `@get:` is still needed where a framework reads
  getters.
- **Injection.** Primary-constructor injection with `private val`. No `@Autowired lateinit var` in
  production code. In tests, constructor parameters marked `@Autowired` work.
- **Configuration values.** In `@Value`, escape the dollar: `@Value("\${app.limit}")`. Prefer an
  immutable `@ConfigurationProperties` class with constructor binding.
- **Request parameters.** A nullable `@RequestParam` type means optional; a non-null one means
  required. Give a default only when the contract states one.
- **Nullability of Spring APIs.** With `-Xjsr305=strict`, and JSpecify in Spring Framework 7, Spring
  return types carry their nullability. Handle the `null`; do not `!!` it away.

## 4 · Where each rule lives

Read the reference for the layer you change. Each file is self-contained.

| Writing | Read |
| --- | --- |
| Domain types, value types, closed result types, invariants | [references/domain.md](references/domain.md) |
| Use cases, ports, transactions, locks, outbox | [references/use-cases-and-transactions.md](references/use-cases-and-transactions.md) |
| jOOQ repositories, Flyway migrations, hydration | [references/persistence-jooq.md](references/persistence-jooq.md) |
| Controllers, request and response types, errors on the wire | [references/http-adapter.md](references/http-adapter.md) |
| Any test | [references/testing.md](references/testing.md) |

## 5 · Before reporting done

1. Find the build, test and check commands in the build's README, the root build file or the CI
   configuration. Do not guess them.
2. Compile every touched subproject with warnings as errors.
3. Run the fast tests of every touched subproject. Run the slow (container) tests when the change touches
   persistence, transactions or anything else only they exercise, and say which ran.
4. Run the project's architecture and boundary checks when the change adds a dependency, a package or a
   port.
5. Re-read the diff against sections 2 and 3 and the reference you used.
6. Report what ran, with its result. A step not run is reported as not run.
