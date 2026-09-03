# Production governance

Read when a characteristic can only be verified against real conditions, and build-time checks cannot reach it.

## Why governance runs in production at all

The discipline emerged from losing control of operations. When a company moves its systems to someone else's infrastructure, the architects no longer control operations, which raises an unavoidable question: what happens if a defect appears operationally, and how would anyone know before customers do?

The reframing that follows is the useful part: it is not a question of *if* something will break, but *when*. Anticipating those breakages and testing for them deliberately makes systems considerably more robust than waiting to be surprised.

## The pattern set

Six kinds of production fitness function, each addressing a different failure class.

**General chaos injection.** Randomly terminate or degrade running components to verify the system endures it. This is the entry point and the least targeted.

**Specific-failure injection.** Build the failure your environment actually exhibits, not the generic one. High latency turned out to be the characteristic failure mode of one major cloud environment, so a dedicated latency injector was built for it. Your environment has its own signature failure — find it and simulate that.

**Total-zone failure.** Simulate the loss of an entire datacenter or availability zone. Organizations that run this routinely survive real regional outages, because the failure has already been rehearsed.

**Conformity checking.** Enforce architect-defined governance rules continuously in production — for example, that every service responds without errors to all requests. This is the production equivalent of a build-time assertion, for rules that must hold live.

**Security checking.** Scan each service for well-known security defects: ports that should not be active, configuration errors.

**Orphan sweeping.** Find services nothing routes to any more and remove them. In an evolving architecture, teams routinely migrate to newer services and leave the old ones running, and in a cloud environment those consume money indefinitely.

## Choosing what to build

Work from the characteristics the architecture exists to deliver. If a style was chosen specifically for scalability, elasticity and responsiveness, those are what production fitness functions should track — along with the specific bottleneck that style introduces.

Two things worth measuring that are easy to skip:

- **Frequency of fallback reads.** Where an architecture achieves its speed by avoiding a slow path, measure how often the slow path is actually taken. Rising frequency erodes exactly the characteristic the design was for.
- **The pressure-relief point.** Where a queue or buffer absorbs mismatched rates, its depth is the health metric.

## Preconditions

Injecting failure into production presumes enough redundancy to survive it. If the system cannot survive the injected failure, the fitness function has told you something important, but do it in a controlled window and know that is the answer you may get.
