# Diagramming and presenting a decision

Read when the decision must be drawn or presented. Effective communication is not a soft addition to the work — however good the technical idea, if you cannot convince managers to fund it and developers to build it, it never manifests.

## Representational consistency

Showing part of an architecture without indicating its place in the whole confuses viewers. **Always show the relationships between parts before changing views.**

Start with a diagram of the entire topology. Then show the relationship between it and the substructure you are about to detail — the region highlighted in place. Then show that substructure. Repeat at each level of descent.

This applies equally to diagrams and to live presentations, and it eliminates a common source of confusion for almost no effort.

## Keep early artifacts disposable

A person's attachment to an artifact is proportional to how long it took to produce. Four hours in a polished diagramming tool produces more attachment than two — and that attachment costs objectivity at exactly the moment the design most needs to change.

So keep early design artifacts cheap and ephemeral, so people throw them away freely and the real shape emerges through revision, collaboration and discussion. Move to the high-fidelity tool only once the team has iterated enough. Noticing that you are unwilling to change a diagram is a signal you over-invested too early.

The classic ephemeral artifact is a phone photo of a whiteboard, with the inevitable "Do Not Erase". A tablet driving a projector beats it on four counts: an unlimited canvas; the ability to copy and paste "what if" variants without destroying the original; images that are already digitized and free of glare; and much better remote collaboration.

## Tool features worth having

**Layers** — group items logically and show or hide them as needed. **Stencils and templates** — a library of common visual components, so diagrams stay consistent across an organization and are faster to build. **Magnets** — control the points on a shape where connector lines snap, giving alignment and other visual niceties.

Plus the basics: lines, colours, shapes, and export to a wide variety of formats.

## Use layers semantically, not decoratively

Layers should contribute meaning to the image, not just tidy it.

- **Base layer: the topology.** Containers, databases, dependencies, brokers, and other core elements — described architecturally rather than by implementation. Write "synchronous communication", not a named protocol.
- **Second layer: implementation detail.** Which database, which protocol.
- **Further layers: one meta-concern each.** Domain boundaries, transactional scope, quantum boundaries — anything you want to read *against* the topology.

Layering this way makes diagrams extensible, and lets you hide detail that would overwhelm a particular discussion without maintaining a second diagram.

## The three standards

**UML.** Created in the 1980s to unify competing design philosophies. Like many things designed by committee, it failed to create much impact outside organizations that mandated it. Its class and sequence diagrams remain in genuine use for communicating structure and workflow; most other diagram types have fallen into disuse.

**C4.** Developed between 2006 and 2011 to address UML's deficiencies and modernize the approach. Four levels:

- **Context** — the entire context of the system, including user roles and external dependencies.
- **Container** — the physical and often logical deployment boundaries. A good meeting point for operations teams and architects.
- **Component** — the component view, aligning most neatly with an architect's view of the system.
- **Class** — reuses UML class diagrams, which work and need no replacement.

It defines standards for components, lines, containers, databases and other common artifacts, is supported by templates in many tools, has an active ecosystem, and has kept pace with ecosystem change. A good default for an organization wanting to standardize.

**ArchiMate.** An open enterprise-architecture modeling language for describing, analyzing and visualizing architectures within and across business domains. Deliberately designed to be as small as possible rather than to cover every edge case, which is why it stays usable at enterprise scale.

Establish a standard for consistency, and allow reasonable exceptions. Architects frequently and legitimately break the rules when the standard offers no good way to represent a design — the older generation of heavyweight modeling tools forced elaborate models of simple things, full of details that were noise in context, and that is worth not recreating.

## Diagram guidelines

**Titles.** Title every element unless it is very well known to the audience. Use rotation and other effects so a title sticks to the right thing and uses space efficiently.

**Lines.** Thick enough to be clearly visible. Use arrows for directional or two-way flow. Different arrowheads may carry different meaning as long as it is consistent. One of the few genuinely general standards in architecture diagrams: **a solid line means synchronous communication and a dotted line means asynchronous.**

**Shapes.** No pervasive standard set exists outside the formal languages, so build your own and consider adopting it organization-wide. A workable convention: three-dimensional boxes for deployable artifacts, rectangles for containers, cylinders for databases.

**Labels.** Label every item, especially where ambiguity is possible.

**Colour.** Architects underuse it — a habit inherited from decades of black-and-white printing. Use it to distinguish artifacts. But never let colour alone carry a critical distinction: people who are colourblind or have other visual disabilities will not see it. Add unique iconography as well, the way crossing lights pair green and red with distinct figures.

**Keys.** Include one whenever shapes could be ambiguous. An easily misinterpreted diagram is worse than no diagram at all.
