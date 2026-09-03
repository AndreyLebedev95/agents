# Cohesion

Read when judging whether a module's parts belong together, or before splitting one.

## The scale, best to worst

Cohesion is the extent to which a module's parts should be contained within the same module — how related the parts are to one another. An ideal cohesive module is one where breaking the parts apart would require coupling them back together via calls between modules to achieve anything useful.

**Functional.** Every part is related to the others, and the module contains everything essential it needs to function.

**Sequential.** Two modules interact: one outputs data that becomes the input for the other.

**Communicational.** Two modules form a communication chain, each operating on information or contributing to some output — one adds a record to the database, the other generates an email from that information.

**Procedural.** Two modules must execute code in a particular order.

**Temporal.** Modules are related by timing dependencies. The classic case is a list of seemingly unrelated things that must all be initialized at system startup.

**Logical.** The data is related logically but not functionally. A module converting information from text, serialized objects or streams into some other format — the operations are related, the functions are quite different. The `StringUtils`-style grab-bag of static methods that all operate on strings and are otherwise unrelated is in virtually every code base.

**Coincidental.** The elements are unrelated other than being in the same source file. The most negative form.

Treat logical and coincidental as refactoring candidates. Treat temporal and below as smells worth being able to explain.

## Cohesion is less precise than coupling

A module's degree of cohesion is frequently a judgment call. Take this module definition:

```
Customer Maintenance
  add customer
  update customer
  get customer
  notify customer
  get customer orders
  cancel customer orders
```

Should the last two live here, or become a separate Order Maintenance module? It depends, and the three questions that resolve it are:

1. **Are these the only two operations for Order Maintenance?** If so, it may make sense to collapse them back.
2. **Is Customer Maintenance expected to grow much larger?** If so, look for opportunities to extract behavior into a different or new module.
3. **Does Order Maintenance require so much knowledge of Customer information that separating them would demand a high degree of coupling to work?**

That third question is the load-bearing one, and it points at the rule underneath all of this: attempting to divide a cohesive module only results in increased coupling and decreased readability.

## Finding classes that were never one class

Lack of cohesion in methods reads best as: *the sum of sets of methods not shared via shared fields*.

Take a class with private fields `a` and `b`, where many methods only access `a` and many others only access `b`. The sum of the sets of methods not shared via those fields is high, so the class scores high — indicating a significant lack of cohesion.

Picture three classes. In the first, fields and methods interlock and the score is low: good structural cohesion. In the second, every field/method pair could be its own class without affecting system behavior: high score, no real cohesion. In the third, most of the class interlocks but one field/method combination stands apart: mixed, and that one combination could be refactored out.

**Use it** when analyzing a code base to assist with restructuring, migration, or simply understanding it. Shared utility classes are a common headache when moving architectures, and this metric finds the ones that are incidentally coupled and should never have been a single class.

**Limit.** It finds only structural lack of cohesion. It cannot determine whether particular pieces fit together logically. Which is the general shape of the problem with code metrics, and the reason a score is a question rather than an answer.
