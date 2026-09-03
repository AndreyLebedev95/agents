# Intake template for an unstructured design problem

Read when the problem arrives as a conversation or a wish rather than as something you can analyze.

Four sections. The fourth is the one that gets skipped and the one that changes designs.

```
## Description
The overall domain problem the system is trying to solve.

## Users
Expected number and types of users.

## Requirements
The domain requirements, as domain users and experts would state them.

## Additional context
Facts that would never appear in a requirements document but influence the design —
ownership structure, expansion plans, staffing strategy, regulatory position,
what the company is doing financially.
```

## Why the fourth section earns its place

Requirements documents describe the system. Additional context describes the conditions the system will live in, and it routinely overturns conclusions the requirements support on their own.

Worked example. A national sandwich chain wants online ordering. Requirements: place an order, choose pickup or delivery, give pickup customers a time and directions integrating external mapping services with traffic, dispatch a driver for delivery, provide mobile accessibility, offer national and local daily promotions, accept payment online, at the shop or on delivery. Users: thousands, perhaps one day millions.

Additional context: the shops are franchised with different owners, the parent company plans overseas expansion, and the corporate goal is to hire inexpensive labour to maximize profit.

Each of those three changes the analysis. Franchising imposes cost restrictions and raises the question of whether a simple or sacrificial architecture is warranted. Overseas expansion implies internationalization. Inexpensive labour makes usability important. None of them is a requirement.

## Using it as a practice exercise

The same format works as a training device, which is worth knowing because architects design perhaps half a dozen systems in a career — too few to learn from experience alone.

Run it timeboxed: small teams produce a characteristics analysis and diagrams, not an elaborate design, then share and critique. Have an experienced architect evaluate the trade-off analysis specifically, naming missed trade-offs and alternative designs.

There is no answer key, and that is not an omission. A topology drawing records how a team implemented something; the why — the trade-offs weighed and the alternatives rejected — is the more interesting half and does not survive in a diagram. Keep only the drawings and you have kept half the story.
