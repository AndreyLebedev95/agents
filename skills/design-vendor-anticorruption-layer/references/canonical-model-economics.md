# Should there be a shared canonical model?

Read at step 5, and **only** when someone actually proposes a common or canonical data model.
Reading it otherwise wastes the decision on a question nobody asked.

Contents: [the arithmetic](#the-arithmetic) · [the break-even](#the-break-even) ·
[the permanent cost](#the-permanent-cost) · [the documented failure mode](#the-documented-failure-mode) ·
[the scoping rule](#the-scoping-rule) · [how to decide](#how-to-decide)

## The arithmetic

Direct translation between every pair of systems needs **N(N−1)** translators. Routing everything
through a common model needs **2N** — one in and one out per system.

| Systems | Direct N(N−1) | Canonical 2N | Verdict |
|---|---|---|---|
| 2 | 2 | 4 | direct wins clearly |
| 3 | 6 | 6 | a wash |
| 4 | 12 | 8 | canonical ahead |
| 6 | 30 | 12 | canonical well ahead |
| 10 | 90 | 20 | no contest |

Multiply both columns by the number of message types each system publishes — the counts multiply,
so a small estate exchanging many document types reaches the crossover on message types rather than
on system count.

A precision worth keeping: this growth is **quadratic**, not exponential. The distinction matters
because a large upfront modelling effort is often justified by invoking runaway growth that is not
actually there. Quadratic is bad enough to justify a canonical model at ten systems and nowhere
near bad enough to justify one at three.

## The break-even

**Three.** Below three, a canonical model is strictly more work than writing the direct mappings.
At three it is a wash and the decision should be made on other grounds. Only above three does the
arithmetic favour it.

Count the systems that **actually exchange messages with each other**, not every system in the
estate. This is where the count is usually inflated: an estate of twelve systems where only four
participate in this exchange is an N of four.

## The permanent cost

Every message pays **two translations instead of one**, on every path, forever. This is not a
migration cost that amortises; it is a per-message latency and CPU tax for the life of the system.

Before agreeing, check whether every path's latency budget survives two transformations. Where one
does not, carve out direct translation for that path specifically and document the exception — a
canonical model with two deliberate bypasses is a normal, healthy design, and pretending otherwise
is how latency-critical paths get quietly broken.

## The documented failure mode

Most enterprises already have a failed enterprise data model behind them, and the reason is
specific rather than incidental.

The stated goal — a unified model that works equally well for every application being integrated —
**is not achievable in practice.** Every participant's shape pulls the model a different way. It
either bloats to satisfy everyone, or quietly favours whichever system was loudest in the room, and
in both cases the participants slowly stop believing in it.

When someone proposes "one model for the enterprise", this is the specific prediction to make. It
is not pessimism; it is the observed outcome, and the next section is the one change that avoids it.

## The scoping rule

**Model only the data that crosses the wire. Never the data inside the applications.**

This single constraint is what makes a canonical model tractable. It shrinks the model by an order
of magnitude, removes most of the disagreements (because internal representations are where the
irreconcilable differences live), and gives an objective test for every proposed addition: is this
field genuinely exchanged, or was it added because it exists somewhere?

Check after each addition. Models fail by accretion, one reasonable-looking field at a time.

## How to decide

1. Count the systems that genuinely exchange messages. Multiply by message types per system.
2. Run N(N−1) against 2N on that number.
3. If two or three, **do not build one.** Write the direct mappings and revisit if the count grows.
4. Above three, check each path's latency budget against two transformations, and carve out the
   paths that cannot afford it.
5. Scope the model to exchanged data only, and put the test in writing.
6. When a term is contested, **record the disagreement as the finding** rather than silently
   picking a winner. A contested term is telling you two parts of the business mean different
   things, which is information worth more than the model.
7. Sell it on replaceability and shared vocabulary, not on elegance. Its real payoff is forcing one
   agreed name onto "account", "payer", "contact" — it is a semantics negotiation that happens to
   produce a technical artifact, and pitching it as a technical artifact is how it loses the support
   it needs from the people who must agree to it.
