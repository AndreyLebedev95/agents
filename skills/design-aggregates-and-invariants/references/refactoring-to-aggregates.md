# Refactoring an existing model into aggregates

Read when the entity model already exists — typically objects with public setters, persistence methods, and the business rules living outside in procedures. Contents: [when to do this](#when-this-refactor-is-warranted) · [the compiler-first sequence](#the-compiler-first-sequence) · [finding transaction boundaries](#finding-the-transaction-boundaries) · [logic in other codebases](#logic-that-lives-in-other-codebases) · [going further](#going-further)

## When this refactor is warranted

The trigger is not aesthetic. Objects that separate data from behaviour are perfectly correct where the logic is simple, and replacing them there adds accidental complexity for nothing.

Refactor when the logic manipulating them has become complex **and** you are seeing inconsistencies and duplication — the same rule implemented in several callers, drifting apart. That combination is the signal that the rules need a home that can enforce them.

If you are unsure whether the area warrants this at all, settle that first with `choose-business-logic-pattern`.

## The compiler-first sequence

Work in this order. Each step is small and independently safe.

### 1. Extract value types

Ask which data structures can be immutable, and move the logic related to each into it. This step alone reduces complexity meaningfully even if you go no further, and it is entirely reversible.

### 2. Make the setters private, and let compilation fail

This is the useful trick. Change every setter to private and build.

Every compilation error marks a place where code outside the object is controlling its state. That list is the thing you could not otherwise see — it is the real inventory of where the business logic lives, and it is generated for you rather than assembled by reading.

```
// before
public class Player {
    public Guid Id { get; set; }
    public int Points { get; set; }
}

public class ApplyBonus {
    public void Execute(Guid playerId, byte percentage) {
        var player = _repository.Load(playerId);
        player.Points *= 1 + percentage/100.0;   // <- outside code, mutating state
        _repository.Save(player);
    }
}
```

### 3. Move each state change inside the object that owns the data

One error at a time, relocate the mutation into a named method on the object:

```
public class Player {
    public Guid Id { get; private set; }
    public int Points { get; private set; }

    public void ApplyBonus(int percentage) {
        Points *= 1 + percentage/100.0;
    }
}
```

Name these methods for what the business calls the operation, not for the field they touch. `ApplyBonus`, not `SetPoints`.

### 4. Find the hierarchies that need to check rules together

With the logic gathered, look for groups of objects where a rule needs to see several of them at once with strong consistency. Those groups are the aggregate candidates.

### 5. Decompose along the smallest transaction boundaries

For each candidate, find the least data that must stay strongly consistent for its rules to hold, and draw the boundary there. Apply the strong-consistency test from the main skill per piece of data.

### 6. Reference external aggregates by id only

Replace object references that cross a boundary with the id. This is what makes the boundary real rather than notional.

### 7. Designate a root per aggregate

Pick the entry point and make every other internal object's methods private, reachable only from within the aggregate.

## Finding the transaction boundaries

When analysing the existing code, two questions cut in opposite directions and both matter:

- **Are there decisions that require strong consistency but currently operate on eventually consistent data?** These are live defects — the system is already capable of reaching invalid states, and probably does so rarely enough that nobody has traced it.
- **Does the solution enforce strong consistency where eventual consistency would suffice?** This is where contention and slow writes come from, and it is the more common finding in code that grew by accretion.

Both are business questions, not technology questions. The answer to "does this need to be consistent" comes from what the business considers broken, not from what the database makes easy.

## Logic that lives in other codebases

Before declaring the model reshaped, find the business logic that is not in the application: stored procedures, database triggers, scheduled jobs, serverless functions, report queries with rules embedded in them.

Logic in those places will contradict the aggregate's rules eventually, because nothing forces the two to agree. Either move it inside the boundary, or — where that is genuinely impractical — record explicitly that this rule is enforced elsewhere, so the next person does not assume the aggregate is authoritative.

## Going further

**Do not jump to an event-sourced model from here.** Land on state-based aggregates first and spend the effort getting the boundaries right. Discovering that a transaction boundary was wrong is orders of magnitude cheaper to fix in a state-based aggregate than in one where the events are already the source of truth and cannot be rewritten.

Once the boundaries are stable and the invariants live inside them, moving to events becomes a mechanical change of how state is persisted rather than a redesign. See `model-lifecycle-and-events`.

**None of this has to happen at once.** Value types first is a complete, useful increment on its own. Gathering scattered logic is another. The full aggregate design can wait until the first two have made the current shape visible.
