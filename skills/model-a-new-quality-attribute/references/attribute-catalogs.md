# Attribute catalogs — for coverage checking only

Use everything here as a **checklist**, to confirm no stakeholder concern was overlooked, and as a
seed for your own domain-specific list. Do not adopt the terminology or the hierarchy.

## Contents
- [The main published standard](#the-main-published-standard)
- [Where the standard is internally inconsistent](#where-the-standard-is-internally-inconsistent)
- [Attributes with no catalog entry](#attributes-with-no-catalog-entry)
- [Physical system attributes](#physical-system-attributes)
- [Worth reading](#worth-reading)

---

## The main published standard

The principal software product quality standard divides attributes into those supporting a "quality in
use" model and those supporting a "product quality" model. The division is a stretch in places, but it
begins a divide-and-conquer march through a large array of qualities.

Its eight **product quality** characteristics:

| Characteristic | Definition |
|---|---|
| **Functional suitability** | Degree to which a product or system provides functions that meet stated and implied needs when used under specified conditions |
| **Performance efficiency** | Performance relative to the amount of resources used under stated conditions |
| **Compatibility** | Degree to which a product, system or component can exchange information with others, and/or perform its required functions, while sharing the same hardware or software environment |
| **Usability** | Degree to which a product or system can be used by specified users to achieve specified goals with effectiveness, efficiency and satisfaction in a specified context of use |
| **Reliability** | Degree to which a system, product or component performs specified functions under specified conditions for a specified period of time |
| **Security** | Degree to which a product or system protects information and data so that persons or other products or systems have the degree of data access appropriate to their types and levels of authorization |
| **Maintainability** | Degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers |
| **Portability** | Degree of effectiveness and efficiency with which a system, product or component can be transferred from one hardware, software or other operational or usage environment to another |

Each characteristic is composed of "quality sub-characteristics" — non-repudiation, for instance, is a
sub-characteristic of security. The standard works through almost **five dozen** sub-characteristic
descriptions this way.

---

## Where the standard is internally inconsistent

Worth knowing, because it is the concrete argument for not organizing your work around it:

- It defines the qualities of "pleasure" and "comfort".
- It distinguishes "functional correctness" from "functional completeness", then adds "functional
  appropriateness".
- To exhibit "compatibility", systems must have either "interoperability" or just plain "coexistence".
- "Usability" is filed as a product quality, not a quality-in-use quality — yet it *includes*
  "satisfaction", which is a quality-in-use quality.
- "Modifiability" and "testability" are both parts of "maintainability". So is "modularity", which is a
  *strategy for achieving* a quality rather than a goal in its own right.
- "Availability" is part of "reliability".
- "Interoperability" is part of "compatibility".
- **"Scalability" is not mentioned at all.**

Real time and effort went into deciding that security should be its own characteristic rather than a
sub-characteristic of functionality, where a previous version of the standard had placed it. That is
the shape of the debate this kind of list generates.

For scale: a widely-read public list of system quality attributes ran to more than 80 distinct
entries, including "demonstrability", helpfully defined as the quality of being demonstrable.

---

## Attributes with no catalog entry

Real attributes that matter to real projects and appear in no standard list.

### Measuring the architecture itself

- **Buildability** — how well the architecture lends itself to rapid and efficient development.
  Measured by the cost, in money or time, to turn the architecture into a working product meeting all
  its requirements. Resembles the development-project attributes, but what it measures is a property
  of the architecture.
- **Conceptual integrity** — consistency in the design; the same thing done the same way throughout.
  Contributes to understandability and produces less confusion and more predictability in
  implementation and maintenance. Less is more.
- **Marketability** — the perception of an architecture, which can be at least as important as the
  qualities it actually brings.

### Measuring the development organization

- **Development distributability** — designing the software to support distributed software
  development, measured like modifiability in terms of the activities of a development project.
- **Manageability** — how easy it is for system administrators to manage the application. Commonly
  achieved by inserting useful instrumentation for monitoring operations and for debugging and
  performance tuning.

### Organization-specific attributes

These are legitimate and you should expect them.

One organization designed a system with the conscious goal of retaining key staff and attracting
talented new hires to a quiet region far from the industry's centres. Its architects spoke of imbuing
the system with a quality named after the region, and achieved it by bringing in state-of-the-art
technology and giving development teams wide creative latitude. It appears in no standard list of
quality attributes, and it was as important to that organization as any other attribute.

The lesson to carry: if stakeholders care about it and it shapes the architecture, it is a quality
attribute requirement, whatever it is called and whoever has never heard of it. Build it a scenario
form and a model.

---

## Physical system attributes

For embedded software, the whole system is designed to meet a litany of attributes the software
affects and is constrained by:

weight · size · electric consumption · power output · pollution output · weather resistance ·
battery life

The scenario technique works unchanged on these. If the systems engineers and architects are not
already using it, introduce it.

---

## Worth reading

The product quality standard summarized above is ISO/IEC 25010 — worth looking up if you want the
full sub-characteristic list as a coverage checklist. Treat it as a lookup aid, not as an authority to
organize your work around; the body of this file explains why.

For the qualities of a deployment pipeline specifically — traceability, testability of the pipeline
itself, tooling, and cycle time — see the deployment-pipeline literature; these are a useful worked
example of a non-catalog attribute set built for one narrow purpose.
