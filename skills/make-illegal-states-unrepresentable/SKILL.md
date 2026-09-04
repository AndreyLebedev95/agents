---
name: make-illegal-states-unrepresentable
description: Redesigns a type or entity so contradictory states cannot be constructed at all, rather than being validated against at runtime. Covers the boolean-flag-beside-the-data anti-pattern and its three failure modes, replacing flags with a closed set of cases each carrying only its own data, enumerating the legal combinations instead of using several optional fields, giving a privileged case its own type with a constructor only the authorising process can call, checked constructors for constrained values, invariants a type's shape enforces for free, and the difference between integrity and consistency. Use whenever an entity has status or boolean flags governing whether other fields are populated; when a record has optional fields whose combinations include nonsense; when a rule says "must have at least one of"; when validation is duplicated across call sites; when a defect came from a field being set that should not have been; when designing a schema or type where some field combinations are invalid; or when asking how to stop a caller or an agent producing a contradictory entity. For the runtime consistency boundary and transactions use design-aggregates-and-invariants; for lifecycle transitions and their events over time use model-lifecycle-and-events; for typing the steps of a process use model-workflow-as-type-pipeline.
---

# Making illegal states unrepresentable

There are two ways to stop bad data existing. You can check for it — validation, assertions, tests, code review — or you can arrange for it to be unconstructible, so the bad combination has no representation and the question never arises.

The second is strictly better where it is available, and it is available far more often than people use it. The reason it gets missed is structural rather than careless: most languages make it trivial to say *this AND that AND that*, and awkward to say *this OR that OR that*. So a concept that is genuinely a choice gets flattened into a record with flags and optional fields, and every nonsense combination of those fields becomes constructible.

That is where contradictory entities come from. Not from carelessness — from a modelling default.

## The output

A revised type model:

1. **The cases** — the closed set of situations the thing can actually be in, each carrying exactly the data that situation has.
2. **The gated types** — where a case is privileged, the distinct type that only an authorising process can produce.
3. **The checked values** — constrained values with a constructor that can refuse.
4. **The structural invariants** — rules the shape carries for free.
5. **What is now unconstructible** — the list of states that have ceased to exist, and the tests that can be deleted.

Item 5 is worth writing down explicitly. It is the argument for the work, and it is what someone reviewing the change needs in order to agree the tests are safe to remove.

## Step 1 — Find the tells

Scan the type for these. Each one is a contradictory state waiting to be built:

- **A boolean or status flag beside the data it qualifies.** `isVerified` next to an address. `isProvisioned` next to a device. `isPriced` next to an amount.
- **An optional field that is only meaningful when some other field holds a particular value.** If `amountToBill` is only populated when `status == Priced`, the type permits an unpriced thing with an amount, and a priced thing without one.
- **Several optional fields where some combinations are nonsense.** Two optionals where the rule requires at least one means the both-absent state is constructible.
- **A comment explaining when a field applies.** The comment is there because the type does not say it. Comments are the residue of rules that failed to get encoded.
- **The same validation repeated at multiple call sites.** Each site is a place someone can forget.

### Why the flag is worse than it looks

A record holding a value plus a flag describing that value fails in three separate ways, and it is worth being able to name all three, because people tend to see only the first:

1. **Nothing says when the flag should be set or unset.** If the address changes, the verified flag must go back to false. That rule lives in a comment or in someone's head. A developer can miss it, or never learn it.
2. **The state is implicit, so handling it needs conditional code everywhere.** Every reader must reconstruct which state it is in before it can do anything.
3. **Nothing prevents the flag being set for data that never went through the process it claims.** In a security context that is a breach — password resets sent to unverified addresses. In a device context it is a fleet entity claiming a firmware version it never received.

The third is the one that matters most and gets noticed least, because it needs no bug to occur: the type *permits* it, so eventually something constructs it.

## Step 2 — Listen for how the business says it

The move is almost always signalled in the domain language. When a domain expert says a thing is "either verified or unverified", or "a device is either unprovisioned, provisioned, or retired", they are describing a choice, and modelling it as a flag is a translation error.

Ask the question directly: *what situations can this thing be in?* The answer is your case list.

## Step 3 — Enumerate the legal combinations and count them

This is the step that does the work, and it is mechanical.

Take the rule as stated. Write down every combination it actually permits. Count them. That count is the number of cases.

**Worked example.** The rule: *a customer must have an email or a postal address.*

The reflex is a record with both fields. That is wrong — it demands both. So make them optional:

```
Contact = { name; email: Email option; address: Address option }
```

Also wrong, and now silently so: this permits a customer with neither, which breaks the rule.

Read the rule closely and enumerate:

- email only
- postal address only
- both

Three situations. So:

```
ContactInfo =
  | EmailOnly of Email
  | AddressOnly of PostalAddress
  | Both of { email: Email; address: PostalAddress }

Contact = { name; contactInfo: ContactInfo }
```

The contactless customer no longer has a representation. There is no test to write for it, because there is no way to express it. And the design now states, visibly, that exactly three situations exist — which is documentation that cannot go stale.

## Step 4 — One case per state, carrying only that state's data

Where the flags describe a lifecycle, give each state its own type holding exactly its own data, then define the thing as a closed choice across them.

**Before** — one record, three problems:

```
Device = {
  deviceId
  isProvisioned : bool          // implicit state
  isEnrolled    : bool          // implicit state
  firmwareVersion : Version option   // only when provisioned
  fleetId         : FleetId option   // only when enrolled
  retiredReason   : string option    // only when retired
}
```

Nothing stops a device that is unprovisioned with a firmware version, enrolled with no fleet, or retired while still reporting as provisioned.

**After:**

```
UnprovisionedDevice = { deviceId; manufacturedAt }
ProvisionedDevice   = { deviceId; firmwareVersion; provisionedAt }
EnrolledDevice      = { deviceId; firmwareVersion; fleetId; enrolledAt }
RetiredDevice       = { deviceId; retiredAt; retiredReason }

Device =
  | Unprovisioned of UnprovisionedDevice
  | Provisioned   of ProvisionedDevice
  | Enrolled      of EnrolledDevice
  | Retired       of RetiredDevice
```

Every field is now required, because each lives only where it applies. There is no unprovisioned device with a firmware version, and no enrolled device without a fleet — those states have no representation.

Two further benefits worth knowing:

- **A state with no data of its own needs no type**, just a case. Do not invent an empty record for it.
- **New states cost nothing to existing code.** Adding a quarantined device means adding a type and a case. Because the other states are defined independently, code working with them is unaffected. Compare the flag-bearing record, where a new state means new fields every existing reader must now handle.

**Include only states the thing can actually reach.** Something that looks similar but belongs to a different process is not a state of this one. A quote is not a state an order gets into; a decommissioned *fleet* is not a state a *device* gets into.

## Step 5 — Gate the privileged case

A choice alone still permits constructing the privileged case with unprivileged data. Nothing stops someone writing `Verified(someRandomAddress)`.

The fix has two more moves, and this is where most attempts stop short:

**Give the privileged case its own type.** Not `Verified of EmailAddress` but `Verified of VerifiedEmailAddress`, where the verified type is distinct from the ordinary one.

**Make that type's constructor private**, so only the module containing the verification service can produce a value of it.

Now the only way to hold a verified address is to have obtained one from the verification service. Holding a new address, you *must* construct the unverified case, because you have nothing else to construct the other with.

Then type the downstream steps to demand it:

```
verifyEmail        : EmailAddress -> Result<VerifiedEmailAddress, VerificationError>
sendPasswordReset  : VerifiedEmailAddress -> ...
sendVerification   : EmailAddress -> ...
```

The rule "only send password resets to verified addresses" is now enforced at every call site by the compiler. Nobody has to have read the documentation.

The same shape carries any must-happen-before rule:

```
provisionDevice : UnprovisionedDevice -> Result<ProvisionedDevice, ProvisioningError>
enrolDevice     : ProvisionedDevice -> FleetId -> Result<EnrolledDevice, EnrolmentError>
```

A device cannot be enrolled without having been provisioned, because enrolment demands a type only provisioning produces. That guarantee needs no test.

## Step 6 — Checked constructors for constrained values

Real domain values are almost never unbounded. A quantity is not negative or four billion. A name does not contain tab characters. A firmware version matches a format.

Rather than documenting the constraint in a comment and hoping callers read it:

- Make the constructor private.
- Expose a `create` function taking the raw value and returning success, or a named failure explaining what was wrong.
- Add an extractor, since a private constructor also blocks destructuring.

Because the value is then immutable, the constraint holds forever after. **Nothing downstream ever re-checks it, and no defensive coding is needed anywhere inside.** That is the actual payoff — an interior you can trust, distinct from the untrusted outside world, where the implementation stays clean because there is nothing to guard against.

The value of this is proportional to how many places would otherwise re-check. Weak for a value used once; very strong for one threaded through a system.

### Prefer structural encoding where the shape can carry the rule

Some invariants need no check at all. "An order always has at least one line" is structural: define the collection as *one element plus a list of the rest*, and it cannot be empty. The definition enforces the rule, at no runtime cost, with no way to bypass it and no test to write.

"Between 1 and 1000" is not structural and needs a checking constructor.

Reach for the structural form first — it is free and unbypassable — and fall back to the checked constructor only where the shape cannot carry the rule.

### Units are a cheap structural win

Tagging a number with its unit stops quantities that share a representation but not a meaning being interchanged. Beyond physical units this applies to timeouts (seconds against milliseconds), spatial dimensions (x against y), and currency. Where the mechanism is compile-time only it costs nothing at runtime.

Likewise, two identifiers both represented as integers are not interchangeable. Give each its own wrapper type and confusing them becomes a compile error rather than a silent defect — both in comparisons and in argument passing.

## Integrity is not consistency

Keep these separate, because only one of them is solvable this way.

**Integrity** is whether one piece of data obeys its own rules: a quantity in range, an order with at least one line, an address that was actually validated. This is largely solvable in the type system, and everything above is about it.

**Consistency** is whether separate parts of the model agree about a fact: an order's total matching its lines, an order having its invoice, a used voucher marked used. This is a business term whose meaning is context-dependent, it places a large and costly burden on the design, and product owners routinely ask for more of it than is desirable or practical. Much of it can be avoided or delayed.

Whether a price change should propagate to unshipped orders has no correct answer — it depends on what the business needs. Treat each consistency demand as a question to put back to the business with its cost attached, not as a requirement to engineer around silently.

For consistency boundaries and what must be transactionally consistent together, use `design-aggregates-and-invariants`.

## What this buys, stated plainly

- Invalid situations cannot exist, so there is nothing to test for. The compiler performs the check that a unit test would otherwise perform, on every build, at every call site.
- The model becomes the documentation, and it cannot drift from the implementation, because it *is* the implementation.
- The design states how many situations exist and exactly what they are, visibly, without anyone consulting a document.
- Finer-grained types tend to find immediate uses elsewhere once they exist.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Boolean flag beside the data it qualifies | A choice was flattened into a record | Replace with cases |
| Optional field only meaningful when a status holds | State-specific data in a shared record | One type per state |
| Two optionals where at least one is required | Combinations were not enumerated | Count the legal cases |
| Same validation at every call site | No checked constructor | Private constructor plus create |
| A comment explaining when a field applies | The rule failed to get encoded | Encode it, delete the comment |
| Privileged case constructible from ordinary data | Stopped at the choice, skipped the gate | Distinct type, private constructor |
| Tables or class hierarchies sketched before the model | Storage or inheritance driving the design | Model without either in mind |
| A case for a state the thing cannot reach | A different process's states mixed in | Remove it |

## A caution on where the model comes from

Two reflexes distort a model before it is written.

Sketching tables and foreign keys first bends the domain to fit storage, and it silently erases distinctions — one foreign key can do dual duty for two relationships the business considers different, hiding that one kind of thing requires a field the other does not. Model without regard to storage: in a paper version of the process there is no database, and the word is not in the business's vocabulary.

Sketching class hierarchies first introduces artifacts that exist nowhere in the domain. The test is simple — ask a domain expert what your abstract base class is.

## Bundled references

- `references/refactoring-recipes.md` — worked before-and-after transformations for each tell, plus encodings for languages without native choice types. Read when applying this to a concrete type, especially outside a language with built-in sum types.
- `references/notation.md` — the plain AND/OR notation for expressing a model that non-programmers can review, and the honest-unknown marker. Read when producing the model as a document rather than as code.
