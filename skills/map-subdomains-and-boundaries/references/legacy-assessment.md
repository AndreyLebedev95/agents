# Assessing and modernising an estate that already exists

Read when the system is not greenfield. Contents: [why brownfield](#why-brownfield-is-the-good-case) · [find the subdomains](#find-the-subdomains-in-a-running-system) · [chart the current design](#chart-the-current-design) · [five strategic smells](#five-strategic-smells) · [recover lost knowledge](#recover-lost-knowledge) · [modernise](#modernise-think-big-start-small) · [strangler](#the-strangler-migration) · [growth checks](#three-growth-checks)

## Why brownfield is the good case

A common belief is that this approach only works on greenfield projects with an expert team. The opposite is closer to true: the systems that gain most are the ones that have already proved their business viability and are now carrying accumulated debt and design entropy. Those are also where most engineering time is actually spent.

It is also not all-or-nothing. Applying every tool on a brownfield estate is not possible in any reasonable timeframe, and it is not what makes the approach work. What makes it work is analysing the business domain, seeking effective models for specific problems, and letting the domain's needs drive design decisions.

## Find the subdomains in a running system

Start with the questions that establish the shape: what does this organisation do, who are its customers, what value does it provide, who does it compete with. Then use the org chart as the first coarse cut and open each unit up.

**Core.** Look for the secret sauce: in-house algorithms, patents, know-how competitors lack. Remember the advantage may not be technical at all.

Then use the unfortunate but reliable heuristic: **look for the worst-designed component that everyone hates and the business refuses to rewrite.** Two qualifying conditions — no off-the-shelf product could replace it (that would make it generic), and any change to it carries business risk. Software that is simultaneously awful and untouchable is almost always core.

**Generic.** Look for what is already bought, subscribed to, or pulled from open source. Competitors have access to the same solutions and their using them costs you nothing.

**Supporting.** What remains: cannot be bought, confers no advantage. If this code is in rough shape it provokes less feeling, because it changes rarely, and the consequences of its poor design are correspondingly milder.

**Do not try to map everything.** For anything beyond a small company it is impractical. Get the overall structure, and go deep only where it touches the systems you are actually working on.

## Chart the current design

Identify the high-level components. These are not necessarily proper model boundaries — they are whatever the system was decomposed into.

**The test that matters is decoupled lifecycles:** which parts can be evolved, tested and deployed independently of the rest? That holds even inside one repository or one deployable, and it is what tells you where the real seams are, as opposed to the ones in the architecture diagram.

For each component, record which subdomains it holds and what patterns implement its logic. Then ask whether the solution fits the complexity of the problem: where is more machinery needed, and where could corners be cut or a product bought instead. Chart the components as though they were boundaries and label the relationships between them.

## Five strategic smells

Read the resulting map for these:

1. **Multiple teams working on the same high-level component.**
2. **Duplicate implementations of a core subdomain.**
3. **A core subdomain implemented by an outsourced company.**
4. **Friction from integration that fails frequently.**
5. **Awkward models spreading out of external services and legacy systems.**

Each maps to a known move: split by team; integrate and give it one owner; bring it in-house; change the relationship pattern; put a translation layer in front of it.

## Recover lost knowledge

Domain knowledge decays for mechanical reasons: documentation goes stale, the people who made the original design leave, functionality accretes ad hoc. At some point the codebase earns the label "legacy" — which mostly means nobody left understands why it does what it does.

This is most acute and most damaging in core subdomains, where the logic is both complex and business-critical.

Recovering it needs a structured pass over the process with everyone who touches it, not an archaeology project by one person reading code. See `derive-model-from-business-process`, and use the result as the foundation for the shared language.

## Modernise: think big, start small

Big rewrites rarely succeed and management rarely backs them. Accept that not all of a large system will be well designed, and decide deliberately where to invest.

**First move: align the logical boundaries.** Reorganise namespaces, modules and packages so they reflect subdomains rather than technical layers. This repositions types without touching business logic, which makes it a comparatively safe refactor — check that reflection, dynamic loading and full-type-name references do not break.

Then find the business logic living outside the main codebase: stored procedures, serverless functions, scheduled jobs. Introduce the same boundaries there, by renaming or by relocating into a dedicated schema. Logic you cannot see is logic that will contradict the model later.

**Second move: turn logical boundaries physical, where it pays.** Two questions decide where:

- Are multiple teams working on the same codebase? Split so each has its own boundary and its own lifecycle.
- Are conflicting models colocated? Separate them.

Then examine the relationships between the boundaries you now have, and fix the ones where the pattern no longer matches how the teams actually work.

**Third move: tactical.** Look for the most painful mismatches between business value and implementation — core subdomains implemented with patterns that cannot carry their complexity. Those components change most often and are most painful to change, which is the worst possible combination.

## The strangler migration

Stand up a new boundary. Implement all new requirements there. Migrate the legacy functionality across piece by piece while the legacy side is frozen except for hotfixes. When everything has moved, the legacy codebase dies.

Pair it with a thin facade that routes each request to whichever side currently owns that functionality, and delete the facade once migration completes.

**The one relaxed rule.** During migration the two sides may share one database, deliberately breaking one-database-per-boundary. Integrating them properly while both work on the same data would otherwise force distributed transactions, which is a worse problem than the temporary coupling. The relaxation is conditional: the legacy side must actually be retired, and sooner rather than later. A "temporary" shared database that outlives the migration is just a shared database.

**Refactoring in place instead.** Take small steps. Never go from procedural or record-based logic straight to an event-sourced model — land on state-based aggregates first and spend the effort getting those boundaries right. Discovering a wrong transaction boundary is orders of magnitude cheaper there. See `design-aggregates-and-invariants` and `choose-business-logic-pattern`.

As you go, protect the new code from old models with a translation layer, and shield consumers from legacy churn by publishing a separate integration contract.

## Three growth checks

Growth is a sign of a healthy system, but unregulated growth — extending functionality without re-evaluating design decisions — is what produces a ball of mud. Check three boundaries repeatedly, distinguishing accidental complexity from the domain's essential complexity:

- **Subdomain.** As it expands, re-apply the coherent-use-cases test. It may now contain several finer-grained subdomains whose different business value you are currently blind to.
- **Boundary.** Watch for one accumulating logic for unrelated problems, and for boundaries becoming chatty — unable to complete an operation without calling another. Chattiness signals an ineffective model and a boundary that needs redrawing for autonomy.
- **Aggregate.** Watch for new functionality quietly distributed into existing aggregates until they hold data that not all of their logic needs strongly consistent. Extracting it often reveals a hidden model that belongs in its own boundary.

Aim for useful boundaries rather than perfect ones. The test is whether they let you identify components of different business value and apply appropriate tools to each.
