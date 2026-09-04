# A plain notation for models people can review

Read when producing the model as a reviewable document rather than as code. Contents: [why not diagrams](#why-not-diagrams) · [data notation](#data-notation) · [workflow notation](#workflow-notation) · [the unknown marker](#the-unknown-marker) · [worked example](#worked-example) · [translating to types](#translating-to-types)

## Why not diagrams

Boxes-and-lines diagrams are hard to work with and not detailed enough to hold the subtleties that matter — which combinations are legal, what a field means, what must be true. A small text notation is more precise and, importantly, is not frightening to non-programmers, so the people who know the domain can work on it with you rather than being shown it afterwards.

It also translates directly into types, because the AND/OR structure it records is exactly what a type system encodes. The document and the eventual model are the same shape.

## Data notation

```
data Order =
    CustomerInfo
    AND ShippingAddress
    AND BillingAddress
    AND list of OrderLine
    AND AmountToBill

data ProductCode = WidgetCode OR GizmoCode

data WidgetCode = string starting with "W" then 4 digits

data OrderQuantity = UnitQuantity OR KilogramQuantity
data UnitQuantity = int between 1 and 1000
```

Four constructs, and no more:

- **AND** — both parts required. A record.
- **OR** — exactly one of these. A choice.
- **list of** — zero or more; write `non-empty list of` when the rule requires at least one, because that is a different type.
- **constraint in words** — `string starting with "W" then 4 digits`, `int between 1 and 1000`. These become checked constructors later.

Deliberately absent: no class hierarchies, no tables, no foreign keys, no nullability syntax, no inheritance. Introducing any of them at this stage imports a technical bias the domain does not have.

## Workflow notation

```
bounded context: Device-Delivery

workflow "Start rollout"
  triggered by:
    "Rollout approved" event
  primary input:
    An approved rollout plan
  other input:
    Fleet membership, current firmware inventory
  output events:
    "Rollout started"
    AND "Canary phase entered"
  side-effects:
    Devices in the canary cohort are notified
```

Then the substeps, each with its own inputs, outputs and dependencies:

```
substep "ValidateRolloutPlan" =
  input: UnvalidatedRolloutPlan
  output: ValidatedRolloutPlan OR ValidationError
  dependencies: CheckArtifactSigned, CheckFleetExists
```

For the logic inside a step, plain pseudocode is enough. The point is the shape of the data crossing each boundary, not the algorithm.

Turning these substeps into signatures with their effects is `model-workflow-as-type-pipeline`.

## The unknown marker

```
data CustomerInfo = ??? // don't know yet
```

Write this rather than guessing. It is the single most useful convention in the notation, for two reasons: it is honest about the state of knowledge, and it is visible — an unknown marker in a reviewed document gets asked about, whereas a plausible invention gets adopted and nobody afterwards remembers it was a guess.

Keep the markers in the document until someone answers them. A model with four honest unknowns is more useful than one with four confident fabrications.

## Worked example

Recording a device model in this notation before writing any types:

```
bounded context: Fleet-Management

data Device =
    UnprovisionedDevice
    OR ProvisionedDevice
    OR EnrolledDevice
    OR RetiredDevice

data UnprovisionedDevice =
    DeviceId AND ManufacturedAt

data ProvisionedDevice =
    DeviceId AND FirmwareVersion AND ProvisionedAt

data EnrolledDevice =
    DeviceId AND FirmwareVersion AND FleetId AND EnrolledAt

data RetiredDevice =
    DeviceId AND RetiredAt AND RetiredReason

data FirmwareVersion = ??? // format not yet confirmed with the platform team
data RetiredReason = ??? // is this free text or a fixed set? ask ops
```

Two things a reviewer can now check without reading code: that a device is exactly one of four things, and that a firmware version exists only where the device has actually been provisioned. Both are questions a domain expert can answer.

## Translating to types

The mapping is mechanical, which is the point:

| Notation | Becomes |
|---|---|
| `A AND B` | a record with both fields required |
| `A OR B` | a closed choice with a case each |
| `list of A` | a collection |
| `non-empty list of A` | a type whose shape guarantees one element |
| `int between 1 and 1000` | a wrapper with a checked constructor |
| `string starting with...` | a wrapper with a checked constructor |
| `??? // don't know yet` | stays a finding; do not invent a type for it |

Because the mapping is mechanical, the document does not become stale in the usual way: if the types stop matching it, one of them is wrong and the difference is visible. Once the types exist, they are the better artifact to maintain — they are checked — and the notation's job is done.
