# Refactoring recipes: from constructible-bad to unconstructible-bad

Read when applying the discipline to a concrete type, especially in a language without native choice types. Contents: [notation](#notation-used-here) · [flag beside data](#recipe-1-flag-beside-the-data-it-qualifies) · [conditional optional field](#recipe-2-optional-field-governed-by-a-status) · [at least one of](#recipe-3-at-least-one-of-a-or-b) · [gated privileged case](#recipe-4-privileged-case-anyone-can-construct) · [scattered validation](#recipe-5-validation-repeated-at-every-call-site) · [encodings](#encodings-in-languages-without-choice-types) · [when not to](#when-not-to-do-this)

## Notation used here

Language-neutral, matching the notation reference:

```
Thing = A AND B          // a record: both required
Thing = A OR B           // a choice: exactly one
Thing = list of A
Thing = A option         // present or absent, explicitly
```

## Recipe 1: flag beside the data it qualifies

**Before**

```
CustomerEmail = {
  emailAddress : EmailAddress
  isVerified   : bool          // set after the customer clicks the link
}
```

**Diagnosis.** Three distinct failures. Nothing says when the flag resets — change the address and it must go back to false, a rule living only in that comment. Nothing stops it being set for an address that never went through verification. And every reader must branch on it before doing anything.

**After**

```
CustomerEmail =
  | Unverified of EmailAddress
  | Verified   of VerifiedEmailAddress    // distinct type, gated constructor
```

**Check.** Can you still construct the verified case from an ordinary address? If yes you have done half the job — continue to recipe 4.

## Recipe 2: optional field governed by a status

**Before**

```
Order = {
  orderId       : OrderId
  status        : Placed | Validated | Priced
  amountToBill  : Money option      // only when status is Priced
  validatedAt   : Instant option    // only when Validated or later
}
```

**Diagnosis.** The comments are the specification, and nothing enforces them. `{ status = Placed; amountToBill = Some(...) }` is constructible and meaningless. So is `{ status = Priced; amountToBill = None }`, which is worse — it looks valid and will fail somewhere downstream.

**After**

```
PlacedOrder    = { orderId; placedAt; lines }
ValidatedOrder = { orderId; placedAt; lines; validatedAt }
PricedOrder    = { orderId; placedAt; lines; validatedAt; amountToBill }

Order =
  | Placed    of PlacedOrder
  | Validated of ValidatedOrder
  | Priced    of PricedOrder
```

Every field is now required, because each lives only where it applies.

**Note the deliberate duplication.** `orderId` and `lines` repeat across the state types. That is not a defect to factor out into a shared base — a shared base reintroduces the coupling you just removed and makes adding a state expensive again. Repetition across state types is the price of independence, and it is worth paying.

## Recipe 3: "at least one of A or B"

**Before**

```
Contact = {
  name    : Name
  email   : Email option
  address : PostalAddress option
}
```

**Diagnosis.** Permits the both-absent state, which the rule forbids.

**Method.** Enumerate what the rule permits, and count:

| # | email | address | legal? |
|---|---|---|---|
| 1 | yes | no | yes |
| 2 | no | yes | yes |
| 3 | yes | yes | yes |
| 4 | no | no | **no** |

Three legal combinations, so three cases.

**After**

```
ContactInfo =
  | EmailOnly   of Email
  | AddressOnly of PostalAddress
  | Both        of { email : Email AND address : PostalAddress }

Contact = { name : Name AND contactInfo : ContactInfo }
```

Generalises: *n* optional fields give 2ⁿ combinations; enumerate them, strike the illegal ones, and the survivors are your cases. If the survivor count is large, that is a signal the concept is really several concepts.

## Recipe 4: privileged case anyone can construct

**Before**

```
Device =
  | Unprovisioned of DeviceId
  | Provisioned   of DeviceId AND FirmwareVersion    // anyone can build this
```

**Diagnosis.** The choice removed the flag but not the forgery. Any code can assert a device is provisioned.

**After**

```
// only the provisioning service's module can construct this
ProvisionedDevice = private { deviceId; firmwareVersion; provisionedAt }

provisionDevice : UnprovisionedDevice -> Result<ProvisionedDevice, ProvisioningError>

Device =
  | Unprovisioned of UnprovisionedDevice
  | Provisioned   of ProvisionedDevice
```

**Then type the consumers to demand it:**

```
enrolDevice     : ProvisionedDevice -> FleetId -> Result<EnrolledDevice, EnrolmentError>
scheduleRollout : EnrolledDevice list -> ...
```

Enrolment cannot run on an unprovisioned device, and a rollout cannot target an unenrolled one. No test asserts this; it cannot be expressed.

## Recipe 5: validation repeated at every call site

**Before**

```
FirmwareVersion = FirmwareVersion of string   // must match N.N.N
```

...with a format check at each of the eleven places it is parsed, three of which are subtly different and one of which was forgotten.

**After**

```
FirmwareVersion = private FirmwareVersion of string

module FirmwareVersion:
  create : string -> Result<FirmwareVersion, string>
  value  : FirmwareVersion -> string          // extractor, since private blocks destructuring
```

**Payoff.** One check, at the edge. Everywhere downstream holds a value that is valid by construction and immutable, so nothing re-checks and no defensive branch is needed. Delete the other ten checks and their tests.

## Encodings in languages without choice types

The modelling decision is identical everywhere; only the encoding changes. In every case the goal is the same: illegal combinations should fail to compile, or failing that, be impossible to construct through the public surface.

**TypeScript** — discriminated unions, which are genuinely checked:

```typescript
type Device =
  | { kind: "unprovisioned"; deviceId: DeviceId }
  | { kind: "provisioned";   deviceId: DeviceId; firmwareVersion: FirmwareVersion }
  | { kind: "enrolled";      deviceId: DeviceId; firmwareVersion: FirmwareVersion; fleetId: FleetId };
```

Narrowing on `kind` gives access to exactly that case's fields. Add `never`-exhaustiveness in the default branch so a new case breaks the build.

**Kotlin / Scala / Java 17+** — sealed hierarchies:

```kotlin
sealed interface Device {
    data class Unprovisioned(val deviceId: DeviceId) : Device
    data class Provisioned(val deviceId: DeviceId, val firmwareVersion: FirmwareVersion) : Device
}
```

Exhaustive `when` / pattern matching gives the compile-time check. Use `private constructor` plus a companion factory for the gated types.

**Rust** — enums are exactly this; use a module-private inner field for gating.

**Python** — dataclasses per state plus a tag, with a `Union` alias, checked by a type checker:

```python
@dataclass(frozen=True)
class Provisioned:
    device_id: DeviceId
    firmware_version: FirmwareVersion

Device = Unprovisioned | Provisioned | Enrolled
```

Freeze them, keep constructors module-private behind factory functions, and use `assert_never` in the fallthrough.

**Go** — interfaces with an unexported marker method restrict implementations to the package, giving a closed set. There is no exhaustiveness check, so pair it with a linter.

**SQL** — the shape does not transfer; a table is an AND type. Options, in descending order of strength: a table per state; one table with a check constraint enumerating legal combinations; or a single table plus the rule enforced only in the code that writes to it. Where the database is written by more than one system, the check constraint is worth its awkwardness.

## When not to do this

- **The combinations are all legal.** Optional fields whose absence carries no rule are fine as optional fields.
- **The concept has one state.** Do not manufacture cases to look thorough.
- **The value is used once, locally.** A checked constructor for something parsed and consumed in the same function buys nothing.
- **The rule is genuinely dynamic** — driven by configuration, or by data the type system cannot see. Then it is a runtime check, and pretending otherwise produces a type that lies.
- **It is a consistency rule, not an integrity rule.** Two records agreeing about a fact is not something a single type can enforce.
