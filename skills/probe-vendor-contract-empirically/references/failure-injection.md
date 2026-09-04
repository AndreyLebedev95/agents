# Injecting failures deliberately

Read at step 9, and only when an integration's stakes justify it. Most do not.

Contents: [why break what rarely breaks](#why-break-what-rarely-breaks) · [the four prerequisites](#the-four-prerequisites) ·
[designing the experiment](#designing-the-experiment) · [the three injections](#the-three-injections) ·
[combinations not to attempt](#combinations-not-to-attempt) · [what to do with the results](#what-to-do-with-the-results)

## Why break what rarely breaks

Three ideas explain why a system that has not failed recently is not therefore safe.

**Drift.** A system — meaning people, process and technology together — operates inside boundaries.
Constant pressure to increase economic return, combined with people's reasonable disinclination to
work at maximum sustainable effort, produces a gradient pushing the whole system steadily toward
the safety boundary. Nothing announces the approach.

**The regulator paradox.** A control mechanism must be at least as complex as the system it
regulates. Simplifying the controls of a complex system does not make it safer; it makes the
controller unable to represent the states it must handle.

**The rarely-exercised path.** A failure path that has not run in eighteen months has probably
stopped working, and nothing will tell you until the day it is needed. Protective machinery decays
silently precisely because its correct behaviour is indistinguishable from never being invoked.

Against a vendor boundary specifically: your timeout, retry, circuit-breaking and fallback
behaviours are all rarely-exercised paths. Injection is how you find out whether the protection you
wrote two years ago still protects.

## The four prerequisites

All must hold before injecting anything. If any fails, the answer is not to be careful — it is to
not run the experiment.

1. **The experiment cannot cause unrecoverable business loss.** If every single request is
   irreplaceably valuable, this is the wrong technique entirely.
2. **The blast radius is bounded**, in both dimensions: how many customers are affected, and how
   badly. Starting crude — failing every ten-thousandth request — is acceptable, but real
   victim-selection criteria are needed quickly.
3. **End-to-end request tracing exists, with a success verdict per request.** Without it you cannot
   tell whether the injection caused harm, and you will be arguing from aggregate graphs.
4. **The steady-state measurement can actually detect the change you care about.** Verify this
   first, by checking whether the metric moves when you already know something is wrong. A metric
   too coarse to show the effect turns a failed experiment into a false pass.

## Designing the experiment

**State the hypothesis as an externally observable invariant.** Not "the circuit breaker will open"
— that is an internal detail. Rather: "checkout completion rate stays within X% of baseline when
the pricing service returns errors for 5% of calls." Externally observable means you can tell
whether it held without reading logs, and it means the hypothesis is about the property you
actually care about.

**Fix the rejection criterion in advance**, accounting for the normal variation in your baseline.
Deciding afterwards whether a result was acceptable is how an experiment becomes an anecdote.

**Run in production, or accept that you are testing a different system.** A staging environment has
different ratios, different data volumes and different traffic mixes, and those differences are
exactly where the failures live. If production injection is not acceptable, that is a legitimate
decision — but record that the results describe staging.

## The three injections

In ascending order of subtlety. Work through them in this order, because the crude ones clear out
the dense easy defects and stop them masking the subtle ones.

**1. Kill an instance.** The crudest. It will absolutely find weaknesses — but it is the beginning,
not the end, and a system that survives instance kills is not thereby resilient.

**2. Add latency.** Finds two classes the instance kill cannot:
- Services that **time out and report an error where they should have had a useful fallback**. The
  code path exists, was never exercised, and does the wrong thing.
- **Undetected race conditions** that appear only when responses arrive in a different order than
  usual. This is a correctness problem surfaced by a timing change, and it is invisible to every
  other technique.

Latency injection is the highest-value of the three for a vendor boundary, because vendor slowness
is the failure mode that actually occurs.

**3. Inject per-call failures**, propagated from the edge through a common call framework. The most
targeted, and it requires the most infrastructure. Use knowledge of the request's call tree to
target deliberately rather than searching blindly.

## Combinations not to attempt

Some combinations produce a large outage while telling you nothing you could not have reasoned out:

- Failing a dependency that everything requires — you learn the system stops, which was known.
- Simultaneously injecting at several layers of one call path — the result is uninterpretable,
  because you cannot attribute the failure.
- Injecting into a system already degraded for unrelated reasons — you are measuring the incident,
  not the experiment.
- Injecting during a change freeze, a peak period, or while another team is deploying.

The governing principle is attribution: if the result cannot be attributed to the injection, the
experiment produces an outage and no knowledge.

## What to do with the results

**Investigate the faults that did *not* become failures, and record what saved you.** This is the
step everyone skips, and it is where most of the value is. A fault that was absorbed tells you a
protection is working — and naming *which* one converts a lucky outcome into a documented property
you can defend in a future design review.

Where a fault did become a failure, the output is not just a fix. It is a row in the capability
report: this boundary fails this way, and here is what must exist on our side.

Feed confirmed behaviours back into the observed-behaviour register with the date, and into the
gateway stub so the harness can reproduce the failure on demand from then on. An injection
experiment that is not turned into a repeatable test has to be re-run by hand forever.
