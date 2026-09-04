---
name: model-workflow-as-type-pipeline
description: Specifies a business process as a pipeline of typed transformations, where each step's signature states what it consumes, what it produces, what it depends on and how it can fail. Covers naming a distinct type for each state the data passes through so a step cannot run on data that skipped a prior step, writing actions as signatures rather than methods, putting errors and I/O into the signature and tracking how those effects propagate upward, classifying failures into domain errors, panics and infrastructure errors, letting the error set grow rather than enumerating it up front, and hiding dependencies at the public boundary while making them explicit inside. Use whenever designing or documenting a workflow, process or pipeline; deciding what each step takes and returns; deciding where validation happens and what "validated" means as a type; specifying a process before implementing it; deciding how errors travel through it; reviewing a workflow spec for missing failure paths; or deciding what a service's public contract should expose. For an entity's states and the events recording its transitions use model-lifecycle-and-events; for making one entity's contradictory states unconstructible use make-illegal-states-unrepresentable; for consistency boundaries and transactions use design-aggregates-and-invariants.
---

# Modelling a workflow as a pipeline of type transformations

Most business processes are a series of document transformations: something arrives in one shape, and each step turns it into a different shape until the output falls out the end. Modelling them that way — one pipeline built from small pipes, each doing one transformation — gives you a specification you can review before anything is built.

The leverage comes from a single decision: **give each stage of the data its own type.** Once "validated order" is a different type from "unvalidated order", a step that requires validated input cannot be handed unvalidated data, and the ordering of the pipeline stops being a convention people have to respect and becomes something that is checked.

## The output

A workflow specification:

1. **The command** that initiates it — payload plus who, when, and whatever auditing needs.
2. **The state types** the data passes through, each carrying only its own stage's data.
3. **The steps**, each a signature: dependencies, input type, output type including its effects.
4. **The error type** — a closed set of cases, each carrying its own data.
5. **The public contract** — inputs and outputs only, dependencies hidden.

## Step 1 — Write the process as substeps first

Before any types, record the shape in plain language: the trigger, the primary input, other inputs, the output events, the side effects. Then the ordered substeps.

```
workflow "Place order"
  triggered by:  "Order form received" event
  primary input: An order form
  other input:   Product catalog
  output events: "Order placed"
  side-effects:  An acknowledgment is sent to the customer

  step 1: ValidateOrder — if invalid, return with ValidationError
  step 2: PriceOrder
  step 3: AcknowledgeOrder
  step 4: create and return the events
```

This is reviewable by people who will never read the types, and it is the thing to get agreement on before investing in the rest.

## Step 2 — Name the command that starts it

The input to a workflow is a domain object, not a serialised message — deserialisation happens at the edge, outside the domain.

But the real input is the **command**: the payload plus the metadata the business needs for logging and auditing.

```
PlaceOrder = { orderForm : UnvalidatedOrder; timestamp; userId }
```

Two conventions worth adopting early:

- **Commands share a shape.** Every command carries the same metadata around different payloads, so define that shape once, parameterised by its payload, rather than repeating the fields.
- **Where all commands for a context arrive on one channel**, unify them as a choice type and dispatch at the boundary:

```
OrderTakingCommand = Place of PlaceOrder | Change of ChangeOrder | Cancel of CancelOrder
```

The dispatching stage lives at the edge, not in the domain.

## Step 3 — One type per stage of the data

This is the decision the rest depends on.

The naive alternative is a single record carrying the whole journey with flags — `isValidated`, `isPriced`, and an optional `amountToBill`. That fails in three ways: the states are implicit so every reader needs conditional code; data belonging to one stage must be optional because other stages lack it; and nothing ties a field to the flag governing it, so the contradictory combination is constructible.

Instead:

```
UnvalidatedOrder = { orderId : string;  customerInfo : UnvalidatedCustomerInfo; ... }
ValidatedOrder   = { orderId : OrderId; customerInfo : CustomerInfo; shippingAddress : Address; ... }
PricedOrder      = { orderId : OrderId; ...; orderLines : PricedOrderLine list; amountToBill : BillingAmount }
```

Note what changes between them beyond the added field: the unvalidated form holds raw strings, the validated form holds parsed domain types. That is the actual content of "validation" — it is a transformation from loose types to strict ones, not a boolean that gets set.

Then, where the thing must be stored or passed between contexts as one value:

```
Order = Unvalidated of UnvalidatedOrder | Validated of ValidatedOrder | Priced of PricedOrder
```

**Include only stages the data actually reaches.** Something that looks similar but belongs to a different process is not a stage of this one — a quote is not a state an order gets into.

**Adding a stage is cheap.** Because each stage's type is defined independently, adding a refunded or quarantined stage means adding a type and a case; existing code is untouched. This is the concrete benefit over the flag-bearing record, where a new stage means new fields every reader must now handle.

For the full treatment of making the contradictory combinations unconstructible, see `make-illegal-states-unrepresentable`.

## Step 4 — Write each step as a signature

An action is documented as a named signature, not as a method hanging off a type. The signature *is* the specification: it names the inputs, the output, and by their types the states each must be in.

```
ValidateOrder =
    CheckProductCodeExists          // dependency
    -> CheckAddressExists           // dependency
    -> UnvalidatedOrder             // input
    -> ValidatedOrder               // output
```

Read that and you know what the step needs, what it consumes, what it produces, and that it cannot be run on anything but an unvalidated order — without reading a line of implementation.

Design each step **stateless and free of side effects**, so it can be understood and tested alone. The design work is choosing the steps and their types; implementation is filling them in and assembling.

## Step 5 — Put the effects in the signature, and follow them upward

For each dependency, ask two questions: **can it fail?** and **does it do I/O?** Encode both answers.

- A check against a locally cached catalogue: neither. It returns a plain value.
- A call to a remote address service: both. It returns an asynchronous result that may be an error.

```
CheckProductCodeExists = ProductCode -> bool
CheckAddressExists     = UnvalidatedAddress -> AsyncResult<CheckedAddress, AddressValidationError>
```

**Effects are contagious, and this is the part people underestimate.** Making one dependency asynchronous forces the step containing it to become asynchronous, and that propagates up through every caller:

```
ValidateOrder =
    CheckProductCodeExists
    -> CheckAddressExists
    -> UnvalidatedOrder
    -> AsyncResult<ValidatedOrder, ValidationError list>
```

So deciding whether a dependency is local or remote is a design decision with system-wide reach, not an implementation detail to settle later. It is worth asking, at design time, whether a remote dependency could be made local — a cached copy of a catalogue — because that decision changes the shape of everything above it.

You may also **deliberately ignore a failure**. If a delivery acknowledgement fails and the business wants to carry on regardless, say so: the step keeps the asynchronous effect but not the failure one. That choice then appears in the signature, where a reviewer can challenge it.

## Step 6 — Classify the failures before modelling them

Three kinds, and only one belongs in the domain model:

- **Domain errors** are expected parts of the business process — an order rejected by billing, an invalid product code, a device failing its pre-flight check. The business already has procedures for these. Model them, discuss them with domain experts, put them in the type system.
- **Panics** leave the system in an unknown state — out of memory, null reference, divide by zero. Abandon the workflow, raise an exception, catch it at the top level.
- **Infrastructure errors** are expected by the architecture but are not part of any business process — a network timeout, an authentication failure. Handle them in the architecture, perhaps with retries.

**The triage question when you are unsure: ask a domain expert.** If a connection abort accessing the load balancer means nothing to them, it is not a domain error. That reaction is the test, not a failure of the conversation.

## Step 7 — Model domain errors as a closed set that is allowed to grow

Errors deserve the same treatment as everything else: domain vocabulary, not strings.

```
PlaceOrderError =
  | ValidationError of string
  | ProductOutOfStock of ProductCode
  | RemoteServiceError of RemoteServiceError
```

Each case carries its own data. The set acts as visible documentation of everything that can go wrong.

**Do not try to enumerate every error during design.** Cases surface as the work proceeds, and each one is then a decision about whether it is a domain error. Adding a case will produce warnings wherever the set is handled — and that is the mechanism working, because each warning forces a conversation with a domain expert about what should happen in that case, rather than letting it be quietly overlooked.

This only pays off where exhaustiveness is actually checked. Without that, adding a case is silent and the mechanism does nothing.

## Step 8 — Hide dependencies outside, expose them inside

- **Public contract**: inputs and outputs only. Callers do not need to know what the workflow collaborates with, and exposing it makes the contract brittle.
- **Internal steps**: dependencies explicit as parameters. This documents what each step actually needs, and means a change in what a step depends on forces a visible change to its definition and then to its implementation.

```
// public
PlaceOrderWorkflow = PlaceOrder -> AsyncResult<PlaceOrderEvent list, PlaceOrderError>

// internal
ValidateOrder = CheckProductCodeExists -> CheckAddressExists -> UnvalidatedOrder -> ...
```

This is a guideline, not a law — the trade-off is transparency inside against a stable contract outside.

## Step 9 — Expect the shapes not to line up

Once each step carries its own effects, the chain no longer composes directly:

```
ValidateOrder    : UnvalidatedOrder -> AsyncResult<ValidatedOrder, ValidationError list>
PriceOrder       : ValidatedOrder   -> Result<PricedOrder, PricingError>
AcknowledgeOrder : PricedOrder      -> Async<OrderAcknowledgmentSent option>
```

The output of the first does not fit the input of the second. **This is normal and expected**, and it is resolved by adapting the shapes at assembly time.

The trap is to fix it by simplifying the signatures — dropping the error type, making everything asynchronous, or returning a bare value and throwing on failure. Do not. The effects are information: they are the record of which steps touch the network and which can fail. Removing them to make the plumbing easier destroys the thing the specification was for.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Every step takes and returns the same type | Stages not modelled as types | One type per stage |
| A step can be called on data that skipped a prior step | Prior step's output is not a distinct type | Give it a distinct type and gate its construction |
| Errors thrown rather than in signatures | Failure paths invisible to callers | Wrap the output |
| One catch-all error string | Failure cases never enumerated | Closed error type, one case per kind |
| Public contract lists internal collaborators | Dependencies leaked across the boundary | Inputs and outputs only |
| Effects dropped so the steps compose | Plumbing prioritised over information | Adapt at assembly instead |
| Every dependency is asynchronous | Effects not examined per dependency | Ask the two questions for each |
| Validation is a boolean flag set by a step | Validation modelled as a check, not a transformation | Make it produce a stricter type |

## Long-running workflows

Where a process spans hours, days or human approvals, the pipeline does not run in one go — each step ends by persisting state and the next is triggered later. The specification is unchanged: the same state types, the same step signatures. What changes is that the state types must be storable and the transitions must be durable.

At that point the process is also a lifecycle with recorded transitions, and `model-lifecycle-and-events` covers the states, the guards and the events; this skill covers what each step consumes and produces. Use both.

## Bundled references

- `references/step-signatures.md` — the signature template, worked examples with and without effects, the two questions per dependency, and the public-versus-internal rule. Read when writing the step list for a concrete process.
- `references/error-taxonomy.md` — the three-way classification with its triage question, how to model domain errors, and how the set is grown over time. Read when deciding how failures travel through the pipeline.
