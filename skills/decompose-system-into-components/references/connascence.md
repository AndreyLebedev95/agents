# Connascence

A vocabulary for coupling that is precise enough to argue with and gives a direction to refactor in. Read when assessing coupling, or in code review where "this is too coupled" is not landing.

Two components are connascent if a change in one would require the other to be modified to maintain the overall correctness of the system.

It is not a metric. It is a language that names kinds of coupling and their consequences, and it overlays rather than replaces incoming/outgoing coupling counts, adding the object-oriented and runtime distinctions those predate.

## The taxonomy, weakest to strongest

### Static — visible in source code

**Connascence of Name.** Multiple components must agree on the name of an entity.

Method names and parameters are the most common coupling in any code base and the most desirable, because modern refactoring tools make a system-wide rename trivial. Nobody hand-edits a method name any more; they refactor it and the change propagates.

**Connascence of Type.** Multiple components must agree on the type of an entity.

The common tendency in statically typed languages to limit variables and parameters to specific types. Not exclusive to them — some dynamically typed languages offer selective typing.

**Connascence of Meaning** (also Connascence of Convention). Multiple components must agree on the meaning of particular values.

The obvious case is hardcoded numbers rather than constants. Consider a codebase defining `int TRUE = 1; int FALSE = 0` and imagine someone flipping them.

**Connascence of Position.** Multiple components must agree on the order of values.

An issue with positional parameters even in statically typed languages. Given `void updateSeat(String name, String seatLocation)`, the call `updateSeat("14D", "Ford, N")` type-checks perfectly and is semantically wrong.

**Connascence of Algorithm.** Multiple components must agree on a particular algorithm.

The common case is a security hash that must produce identical results on both server and client to authenticate. A high degree of coupling: if any detail of either implementation changes, the handshake stops working.

### Dynamic — exists only at execution time, and stronger

**Connascence of Execution.** The order of execution matters.

```
email = new Email();
email.setRecipient("foo@example.com");
email.setSender("me@me.com");
email.send();
email.setSubject("whoops");
```

**Connascence of Timing.** The timing of execution matters. The common case is a race condition between two threads affecting the outcome of a joint operation.

**Connascence of Values.** Several values depend on one another and must change together.

A rectangle defined by four corner points cannot have one point changed without considering the others. The more problematic case is transactions in distributed systems: a single value updated across separate databases must either change everywhere or nowhere.

**Connascence of Identity.** Multiple components must reference the same entity. Two independent components sharing and updating a common data structure, such as a distributed queue.

## The three properties

Strength alone will mislead you. Read all three together.

**Strength** is how easily a developer can refactor the coupling away — not how bad it is in absolute terms. Prefer static to dynamic: static forms are determinable by simple source-code analysis and modern tools make them trivial to improve. Connascence of Meaning improves to Connascence of Name by extracting a named constant.

**Locality** is how proximal the coupled modules are in the code base. Proximal code — code in the same module — typically has more and higher forms of connascence than separated code, and that is fine. Forms indicating poor coupling when components are far apart are acceptable when they are close together. Two classes in the same module sharing Connascence of Meaning is far less damaging than the same two classes in different modules.

This is the same advice bounded contexts give, arrived at independently: limit the scope of implementation details as narrowly as practical.

**Degree** is the size of the impact — does changing a class affect a few classes or many? Lesser degrees require fewer changes and damage code bases less. High dynamic connascence is not terrible across a few modules. But code bases grow, which makes a small problem correspondingly bigger.

Consider strength and locality together: stronger forms within the same module represent much less of a smell than the same forms spread apart.

## The five rules

Three for structuring:

1. Minimize overall connascence by breaking the system into encapsulated elements.
2. Minimize any remaining connascence that crosses encapsulation boundaries.
3. **Maximize connascence within encapsulation boundaries.**

The third is the counterintuitive one. High coupling inside a boundary is desirable, not merely tolerated.

Two for refactoring:

4. **Rule of Degree** — convert strong forms of connascence into weaker forms.
5. **Rule of Locality** — as the distance between software elements increases, use weaker forms of connascence.

## Why it is worth learning the vocabulary

For the same reason design patterns are worth learning: compression. An architect can say "we need a service and there can only be one instance", or say "we need a singleton service" and have the context and the solution travel with the name.

In code review, "don't add a magic string constant in the middle of a method declaration, extract it as a constant instead" is an instruction. "You have Connascence of Meaning; refactor it to Connascence of Name" carries the instruction, the classification and the direction of improvement.

This only works with an audience that shares the vocabulary. Otherwise say both.

## One kind of coupling this does not cover

**Temporal coupling** — a nonstatic dependency based on timing or transactional ordering, where one operation must be invoked before another. It is real coupling and current tooling cannot detect it, so it surfaces only through design documentation or through error conditions in production. Do not expect static analysis to find it. Record known ordering constraints deliberately, and treat unexplained runtime errors as candidate temporal coupling.
