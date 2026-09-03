# Fitness function cookbook

Read when writing an actual check. Organized by what you are protecting.

## Contents
- [Tooling by platform](#tooling-by-platform)
- [Dependency cycles](#dependency-cycles)
- [Structural distance](#structural-distance)
- [Layer access rules](#layer-access-rules)
- [Module compliance](#module-compliance)
- [Dependency caps](#dependency-caps)
- [Pairwise restrictions](#pairwise-restrictions)
- [Version-control churn](#version-control-churn)
- [Integration boundaries from logs](#integration-boundaries-from-logs)
- [Runtime coupling discovery](#runtime-coupling-discovery)
- [Memory and synchronization](#memory-and-synchronization)
- [Role tagging](#role-tagging)

## Tooling by platform

| Platform | Tool |
|---|---|
| Java | ArchUnit, JDepend |
| .NET | ArchUnitNet, NetArchTest |
| Python | PyTestArch |
| TypeScript / JavaScript | TSArch |

All of these express architecture rules as ordinary unit tests, so they run in the continuous build alongside functional tests.

## Dependency cycles

Cycles destroy modularity: no component can be reused without dragging the others along, and coupled components pull each other in until the code base is a big ball of mud.

```java
public class CycleTest {
    private JDepend jdepend;

    @BeforeEach
    void init() {
      jdepend = new JDepend();
      jdepend.addDirectory("/path/to/project/persistence/classes");
      jdepend.addDirectory("/path/to/project/web/classes");
      jdepend.addDirectory("/path/to/project/thirdpartyjars");
    }

    @Test
    void testAllPackages() {
      Collection packages = jdepend.analyze();
      assertEquals("Cycles exist", false, jdepend.containsCycles());
    }
}
```

Wire this into the continuous build and stop worrying about trigger-happy auto-imports.

## Structural distance

Assert each package sits within tolerance of the ideal abstractness/instability balance.

```java
@Test
void AllPackages() {
    double ideal = 0.0;
    double tolerance = 0.5; // project-dependent
    Collection packages = jdepend.analyze();
    Iterator iter = packages.iterator();
    while (iter.hasNext()) {
      JavaPackage p = (JavaPackage)iter.next();
      assertEquals("Distance exceeded: " + p.getName(),
        ideal, p.distance(), tolerance);
    }
}
```

Set the tolerance from your own baseline rather than copying this number.

## Layer access rules

Define each layer by package, then declare who may reach whom.

```java
layeredArchitecture()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")

    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

Two periods either side of a package name indicate ownership of that package and everything under it.

The .NET equivalent asserts the same relationship as a namespace dependency:

```csharp
// Classes in the presentation should not directly reference repositories
var result = Types.InCurrentDomain()
    .That()
    .ResideInNamespace("NetArchTest.SampleLibrary.Presentation")
    .ShouldNot()
    .HaveDependencyOn("NetArchTest.SampleLibrary.Data")
    .GetResult()
    .IsSuccessful;
```

## Module compliance

Assert that every namespace in the repository falls under one of the declared modules, so a developer creating a new top-level directory gets an alert rather than silently establishing a new structure.

```
# The following namespaces represent the modules in the system
LIST module_list = {
   com.orderentry.orderplacement,
   com.orderentry.inventorymanagement,
   com.orderentry.paymentprocessing,
   com.orderentry.notification,
   com.orderentry.fulfillment,
   com.orderentry.shipping
   }

LIST namespace_list = get_all_namespaces(root_directory)

FOREACH namespace IN namespace_list {
   IF NOT namespace.starts_with(module_list) {
      send_alert(namespace)
   }
}
```

This works when all modules share one repository. Where modules live in separate repositories, validate each one against its own expected namespace instead.

## Dependency caps

Cap each module's total dependency count — incoming plus outgoing references — to keep intermodule coupling bounded.

```
LIST module_list = { ...as above... }

MAP module_source_file_map
FOREACH module IN module_list {
  LIST source_file_list = get_source_files(module)
  ADD module, source_file_list TO module_source_file_map
}

FOREACH module, source_file_list IN module_source_file_map {
  FOREACH source_file IN source_file_list {
    incoming_count = used_by_other_module(source_file, module_source_file_map)
    outgoing_count = uses_other_module(source_file)
    total_count = incoming_count + outgoing_count
  }
  IF total_count > 5 {
    send_alert(module, total_count)
  }
}
```

Five is a starting point. Set the limit from your baseline; what matters is that it does not creep.

## Pairwise restrictions

Where two modules must stay independent, assert it directly.

```java
public void order_placement_cannot_access_shipping() {
   noClasses().that()
   .resideInAPackage("..com.orderentry.orderplacement..")
   .should().accessClassesThat()
   .resideInAPackage("..com.orderentry.shipping..")
   .check(myClasses);
}
```

## Version-control churn

Some properties are about how something *changes*, and are therefore invisible to code analysis. Stability of a component meant to be stable is the archetype.

Source the check from repository history: measure churn per area over a rolling window, and alarm on a rise rather than on an absolute value. Pair it with a rate-of-change measure for the areas that are supposed to absorb variation instead.

This generalizes to any stability, ownership or volatility rule.

## Integration boundaries from logs

Where an integration layer connects systems that must only communicate in specified directions, govern it from logs. First make every integration point log consistently, then assert conformance.

```
READ logs for ERP into ERP-logs for past 24 hours
READ logs for Sales into Sales-logs for past 24 hours

FOREACH entry IN ERP-logs
    IF 'operation' is 'update' and 'target' != 'accounting' THEN
       raise fitness function violation
             "Invalid communication between integration points"
    END IF

FOREACH entry IN Sales-logs
    IF 'operation' is 'update' and 'target' != 'accounting' THEN
       raise fitness function violation
             "Invalid communication between integration points"
    END IF
```

This is what lets a powerful integration tool be used strategically while guarding the places teams typically misuse it.

## Runtime coupling discovery

Static coupling is easy to see: shared libraries show up in a software bill of materials, in deployment scripts, and in dependency-management tooling. Note that contracts are static coupling too — an asynchronous protocol decouples two services dynamically while leaving them coupled through the contract.

Dynamic coupling needs one of two techniques.

**Log analysis.** Each service logs every call it makes to another internal or third-party service, recording target and protocol. Fitness functions analyze those logs into a coupling map. This depends entirely on consistent logging, which a shared library exposing one logging API can enforce at compile time.

**Startup registration.** When the first instance of a service starts, it registers its interservice calls as a contract — JSON or similar — with a configuration service. Querying that service then yields a map of every interservice call across the ecosystem.

Either way, the output is a coupling map you can govern against.

## Memory and synchronization

For architectures whose viability depends on memory footprint or replication lag:

**Memory.** Have every instance periodically publish its current memory usage. Where all instances of a unit share the same replicated cache, the report needs only the unit's name. Run a second function recording the instance count per unit, so total consumption per unit is continuously computable.

**Synchronization time.** Have the writing component stream the request ID of an update with a timestamp, and the persisting component stream the same request ID with a timestamp after commit. A fitness function pairs them and subtracts. Report per unit and averaged. Trend analysis then shows whether architecture changes are improving or degrading synchronization, and whether the business's timing goals are being met.

**Queue depth.** Where an asynchronous channel is the pressure-relief point, track its depth. A growing backlog lengthens synchronization time, degrades consistency, and raises the chance of both data loss and update collisions.

## Role tagging

Where no automated check is possible, provide context instead. Tags perform no function; they tell the next developer what kind of thing they are modifying.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Filter {
   public FilterType[] value();

    public enum FilterType {
       PRODUCER,
       TESTER,
       TRANSFORMER,
       CONSUMER
    }
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface FilterEntrypoint {}
```

```csharp
[System.AttributeUsage(System.AttributeTargets.Class)]
class Filter : System.Attribute {
    public FilterType[] filterType;
    public enum FilterType { PRODUCER, TESTER, TRANSFORMER, CONSUMER };
}

[System.AttributeUsage(System.AttributeTargets.Class)]
class FilterEntrypoint : System.Attribute {}
```

Applied to the entry-point class:

```java
@FilterEntrypoint
@Filter(FilterType.TRANSFORMER)
public class TrendAnalyzerFilter { ... }
```

The second marker exists because a component spans several classes and the role tag needs one place to live. This will not stop every misuse — but it supplies the context that prevents most of it.
