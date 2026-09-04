# Writing step signatures

Read when writing the step list for a concrete process. Contents: [template](#the-template) · [two questions](#the-two-questions-per-dependency) · [worked pipeline](#worked-a-device-rollout-pipeline) · [public vs internal](#public-versus-internal-contracts) · [reading a signature](#reading-a-signature-as-a-reviewer) · [smells](#signature-smells)

## The template

```
StepName =
    Dependency1                  // what it needs to collaborate with
    -> Dependency2
    -> InputType                 // the state the data must be in
    -> OutputType                // the state it produces, including effects
```

Dependencies first, then the input, then the output. The ordering matters in practice: it means the dependencies can be supplied once at assembly and the remaining shape is the input-to-output transformation you actually care about.

## The two questions per dependency

For every dependency, ask exactly these, and encode both answers:

**1. Can it fail in a way the caller must handle?**
→ wrap the output in a success-or-failure type with a named error.

**2. Does it do I/O?**
→ wrap the output in an asynchronous type.

| Can fail | Does I/O | Output shape |
|---|---|---|
| no | no | `T` |
| yes | no | `Result<T, Error>` |
| no | yes | `Async<T>` |
| yes | yes | `AsyncResult<T, Error>` |

Then propagate: **an effect anywhere in a step appears on the step**, and on everything calling it.

There is a third question worth asking at design time, because the answer changes the shape of everything above: **could this dependency be made local?** A remote catalogue lookup and a cached one differ by two effects and a great deal of downstream plumbing. Deciding to cache is a design decision, and it is cheaper to take it here than after the pipeline is built.

A fourth, less obvious: **do we care if it fails?** Sometimes the answer is no — a notification that fails should not abort the process. Then the step carries the asynchronous effect but not the failure one, and that decision is visible in the signature where a reviewer can challenge it.

## Worked: a device rollout pipeline

Plain-language shape first:

```
workflow "Start rollout"
  triggered by:  "Rollout approved" event
  primary input: An approved rollout plan
  other input:   Fleet membership, firmware inventory
  output events: "Rollout started" AND "Canary phase entered"
  side-effects:  Devices in the canary cohort are notified

  step 1: ValidateRolloutPlan
  step 2: SelectCanaryCohort
  step 3: StartRollout
  step 4: NotifyDevices
  step 5: create and return the events
```

Stage types — each carrying only its own stage's data:

```
UnvalidatedRolloutPlan = { planId : string; artifactRef : string; fleetRef : string; phases : UnvalidatedPhase list }
ValidatedRolloutPlan   = { planId : RolloutId; artifact : SignedArtifact; fleet : FleetId; phases : NonEmptyList<Phase> }
CohortedRolloutPlan    = { planId : RolloutId; artifact : SignedArtifact; fleet : FleetId; phases : NonEmptyList<Phase>; canary : NonEmptyList<EnrolledDevice> }
StartedRollout         = { planId : RolloutId; artifact : SignedArtifact; canary : NonEmptyList<EnrolledDevice>; startedAt : Instant }
```

Note the transformation across the first boundary: loose strings become parsed domain types, and `phases` goes from a plain list to one that cannot be empty. That is what validation *is* here — a change of type, not a flag being set.

Dependencies, with their effects decided:

```
CheckArtifactSigned = ArtifactRef -> AsyncResult<SignedArtifact, SignatureError>   // remote, can fail
LookupFleet         = FleetRef -> Result<FleetId, FleetNotFound>                   // cached, can fail
ListEnrolledDevices = FleetId -> EnrolledDevice list                               // cached, cannot fail
NotifyDevice        = EnrolledDevice -> Async<NotifyResult>                        // remote; failure ignored
```

Steps:

```
ValidateRolloutPlan =
    CheckArtifactSigned
    -> LookupFleet
    -> UnvalidatedRolloutPlan
    -> AsyncResult<ValidatedRolloutPlan, ValidationError list>

SelectCanaryCohort =
    ListEnrolledDevices
    -> ValidatedRolloutPlan
    -> Result<CohortedRolloutPlan, CohortError>

StartRollout =
    CohortedRolloutPlan
    -> Result<StartedRollout, RolloutError>

NotifyDevices =
    NotifyDevice
    -> StartedRollout
    -> Async<StartedRollout>          // failures deliberately ignored

CreateEvents =
    StartedRollout
    -> RolloutEvent list
```

Three things a reviewer can now check without reading any implementation:

- A rollout cannot start on an unvalidated plan, because `StartRollout` demands a cohorted plan and only `SelectCanaryCohort` produces one.
- A rollout cannot start with an empty canary cohort, because the type cannot hold one.
- Only the first step and the notification step touch the network, so those are the only places a timeout can arise.

## Public versus internal contracts

**Public** — inputs and outputs only:

```
StartRolloutWorkflow = StartRolloutCommand -> AsyncResult<RolloutEvent list, StartRolloutError>
```

The caller does not need to know about signature checking or fleet lookup, and telling them makes the contract brittle: a change of internal collaborator becomes a breaking change for everyone.

**Internal** — dependencies explicit, as above. This documents what each step needs, and means changing what a step depends on forces a visible change to its definition and then to its implementation. That forcing is the point.

The dividing line is the boundary of the thing you own. Guideline, not law.

## Reading a signature as a reviewer

Given `ValidateRolloutPlan` above, you can establish, without any implementation:

- **What state the input must be in** — unvalidated, so this is the entry point.
- **What it guarantees** — a validated plan with a signed artifact and a non-empty phase list.
- **What it talks to** — a signature service and a fleet lookup, and nothing else.
- **Whether it touches the network** — yes, so it can be slow and can time out.
- **How it fails** — a list of validation errors, so it reports all problems rather than the first.

Any of those being wrong is a design conversation, and it can happen before anything is built. That is the return on writing signatures first.

## Signature smells

| Smell | What it means |
|---|---|
| Every step takes and returns the same type | Stages are not modelled; the pipeline's ordering is unenforced |
| A step returns the type it was given | It is mutating, or it is not really a step |
| Every step is asynchronous | Effects were assumed rather than examined per dependency |
| No step can fail | Failure paths have not been thought about, not that they do not exist |
| A step takes six dependencies | It is doing several things; split it |
| The public contract lists dependencies | The boundary has leaked |
| A step takes a flag parameter | Two steps wearing one name |
| Input and output differ only by a boolean field | Validation modelled as a check rather than a transformation |
