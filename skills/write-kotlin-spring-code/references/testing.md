# Tests in Kotlin on Spring

The runner is JUnit 5. Assertions are Kotest's (`shouldBe`, `shouldThrow`). Mocks, when used at all, are
MockK. When the build excludes AssertJ and Mockito, they are not available; do not reach for them.

## Contents

- Choosing the test form
- Fakes over mocks
- Writing the test
- Spring slice tests
- Container tests
- Traps

## Choosing the test form

| Code under test | Form |
| --- | --- |
| Domain | Plain unit test on Kotlin objects; a fixed `Clock` or `Instant` passed in |
| Use case | Unit test with in-memory fakes of its outbound ports |
| Repository (jOOQ) | One abstract contract test per port, run against the fake and against the jOOQ adapter over a real database in a container |
| Controller | Spring MVC slice test (`@WebMvcTest`) with the use-case port replaced by a fake |
| External client | Mapper tests from recorded payloads; client tests against a stub server |
| Whole application | `@SpringBootTest`, only for wiring, profiles and endpoints that need the full context |

Follow the project's table where it has one.

## Fakes over mocks

- A fake is a small class that implements the port over a `MutableMap` or `MutableList`, kept in the
  module's test fixtures and shared by every test of that module.
- The abstract contract test keeps the fake honest: the same assertions run against the fake and the
  real adapter.

```kotlin
abstract class OrderRepositoryContract {
    abstract fun repository(): OrderRepository

    @Test
    fun `a saved order is found by its id`() {
        val repository = repository()
        repository.save(anOrder(id = ORDER_ID))
        repository.find(ORDER_ID)?.id shouldBe ORDER_ID
    }
}

class InMemoryOrderRepositoryTest : OrderRepositoryContract() {
    override fun repository() = InMemoryOrderRepository()
}
```

- Use MockK only where a fake would be harder to read than the interaction, such as checking a call
  that has no observable state. Prefer `every`/`verify` with exact arguments; avoid `relaxed = true`.

## Writing the test

- Name tests as sentences in backticks: ``fun `a cancelled order cannot be shipped`()``.
- One behaviour per test. Arrange with builders that default every field the test does not care about.
- Fix time: build a `Clock.fixed(...)` and pass it; never sleep, never compare against the wall clock.
- Group related cases with `@Nested inner class`.
- Inject Spring beans into a test class through its constructor with `@Autowired` on the parameter.

## Spring slice tests

- `@WebMvcTest(TheController::class)` and the MockMvc Kotlin DSL:

```kotlin
mockMvc.post("/orders/{id}/cancel", id) {
    contentType = MediaType.APPLICATION_JSON
}.andExpect {
    status { isConflict() }
    jsonPath("$.type") { value("…") }
}
```

- Supply the fake use case as a bean from a nested `@TestConfiguration`, unless the project uses
  `@MockkBean` (springmockk) instead.
- Write the slice test from the contract entry of the operation: every status, member and error code
  the entry states.
- On Spring Boot 4 the slice-test annotations moved to per-technology modules
  (`org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest`); copy imports from a neighbour.

## Container tests

- Tests that need a database or another container carry the project's slow-test tag (for example
  `@Tag("integration")`), so the fast stage stays fast.
- The database comes from the project's Testcontainers setup with the migrations applied. Do not start
  a container per test class by hand when a shared one exists.
- Each test leaves no data another test depends on, or owns data no other test touches.

## Traps

- `@BeforeAll` and `@AfterAll` need a `companion object` member with `@JvmStatic`, or
  `@TestInstance(Lifecycle.PER_CLASS)`.
- A MockK stub of a function that takes or returns a value class can fail to match; prefer a fake there.
- `shouldThrow<T> { }` returns the exception; assert on it instead of catching by hand.
- A test that passes before the production code exists tests nothing. Run it red first.
