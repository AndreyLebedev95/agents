# Classifying and modelling failure

Read when deciding how failures travel through a pipeline. Contents: [three kinds](#three-kinds-of-error) · [triage](#the-triage-question) · [modelling domain errors](#modelling-domain-errors) · [growing the set](#growing-the-set-deliberately) · [ignoring failures](#deliberately-ignoring-a-failure) · [where each is handled](#where-each-kind-is-handled)

## Three kinds of error

Not every failure belongs in the domain model, and trying to type all of them produces signatures nobody can read.

**Domain errors** are expected parts of the business process. An order rejected by billing. A product code that does not exist. A device failing its pre-flight check. A rollout halted because the canary failure rate exceeded its threshold.

The defining property: **the business already has a procedure for this.** Somebody knows what happens next, because it happens regularly. These must be modelled, discussed with domain experts, and put in the type system, because the code has to reflect a process that already exists.

**Panics** leave the system in an unknown state. Out of memory. Null reference. Divide by zero. Programmer oversight generally.

Nothing sensible can be done locally, and there is no business procedure — nobody has a policy for "the process ran out of memory". Abandon the workflow, raise an exception, catch it at the highest appropriate level.

**Infrastructure errors** are expected by the architecture but are not part of any business process. A network timeout. An authentication failure. A message broker being briefly unavailable.

These are real and must be handled, but they are handled *in the architecture* — retries, circuit breakers, backoff — not in the domain model. The business has no opinion about them.

## The triage question

When you cannot tell whether something is a domain error, **ask a domain expert**. Their reaction is the test:

> "If we get a connection abort accessing the load balancer, is that something you care about?"
> — blank incomprehension —
> "Fine. That's an infrastructure error; we'll retry and tell the user to try again later."

That reaction is a successful triage, not a failed conversation. A failure that means nothing to the people who run the business is not part of the business process, whatever it costs you operationally.

The question generalises usefully: *does your team have a procedure for this today?* If they do, it is a domain error and the procedure is the specification. If the answer is "we'd call someone", it is infrastructure.

## Modelling domain errors

Errors get the same treatment as everything else in the domain — domain vocabulary, not strings, and each case carrying its own data:

```
PlaceOrderError =
  | ValidationError    of string
  | ProductOutOfStock  of ProductCode
  | RemoteServiceError of RemoteServiceError
```

```
StartRolloutError =
  | ArtifactNotSigned    of ArtifactRef
  | FleetNotFound        of FleetRef
  | NoEligibleDevices    of FleetId
  | RolloutAlreadyActive of RolloutId
  | PhaseThresholdInvalid of { phase : PhaseName; given : Percentage }
```

What this buys:

- The set is **visible documentation** of everything that can go wrong, in one place, reviewable by someone who knows the domain.
- The **data attached to each error** is explicit, so a caller has what it needs to react — `NoEligibleDevices` carries the fleet, so the message can name it.
- The set is **safe to expand or contract**, because exhaustiveness checking will point at every place that now needs to handle a new case.

Note that an infrastructure error can appear as a case where the *business* has a view on it — a remote service being down might warrant retrying a set number of times before giving up, and that policy is a business decision even though the failure is not.

## Growing the set deliberately

**Do not try to enumerate every error up front.** During design you know failures are possible without knowing exactly what they are, and inventing an exhaustive list at that stage produces cases nobody needs and misses ones that matter.

Cases surface as the work proceeds. When one does, decide whether it is a domain error; if it is, add it.

Adding a case will produce warnings everywhere the set is handled. **That is the mechanism working.** Each warning is a place someone must now decide what happens in that case — which forces the conversation with the domain expert or product owner rather than letting the case be handled by accident or overlooked entirely.

This only pays off where exhaustiveness is genuinely checked. Without it, adding a case is silent and none of the above happens — so if the language or linter does not check, wire that up first or the discipline is decorative.

## Deliberately ignoring a failure

Sometimes the business does not care. A device notification that fails should not abort a rollout that has already started.

Say so explicitly. The step keeps the effect for I/O but not for failure:

```
NotifyDevices = NotifyDevice -> StartedRollout -> Async<StartedRollout>
```

The signature now records the decision, where a reviewer can see it and challenge it. That is much better than a swallowed exception, which records the same decision invisibly — and which nobody can distinguish from a bug.

## Where each kind is handled

| Kind | Modelled in the domain | Handled where | Caller sees |
|---|---|---|---|
| Domain error | yes, as a case in a named error type | in the workflow, per the business procedure | a specific case it can act on |
| Panic | no | abandoned; caught at the top level | a failure, with no expectation of recovery |
| Infrastructure error | usually not, unless the business has a policy | in the architecture — retries, backoff, circuit breakers | often nothing, until retries are exhausted |

The practical consequence: a workflow's public error type should contain domain errors and the infrastructure failures the business has an opinion about — and nothing else. If it has thirty cases, most of them are infrastructure that leaked in.
