# Per-scenario analysis record

One record per scenario examined. This is the unit of evidence behind every finding — a risk with no
record behind it is an opinion.

## Template

```
Scenario #: <id>            Scenario: <one-line statement>
Attribute(s):               <the quality attribute(s) this exercises>
Environment:                <the scenario's environment part>
Stimulus:                   <the scenario's stimulus part>
Response:                   <the required response and its measure>

Architectural decisions     Sensitivity   Tradeoff   Risk   Nonrisk
  <decision>                    S<n>                 R<n>
  <decision>                    S<n>        T<n>     R<n>
  <decision>                    S<n>                        N<n>

Reasoning:
  - <why this decision serves or fails the response, referencing the finding ids>
  - <quantitative claim where one exists, with the figure>
  - <the assumption that, if wrong, changes the verdict>

Architecture diagram:
  <the fragment of the architecture this scenario traverses>
```

## Worked example

```
Scenario #: A12             Scenario: Detect and recover from HW failure of main switch.
Attribute(s):               Availability
Environment:                Normal operations
Stimulus:                   One of the CPUs fails
Response:                   0.999999 availability of switch

Architectural decisions     Sensitivity   Tradeoff   Risk   Nonrisk
  Backup CPU(s)                 S2                    R8
  No backup data channel        S3           T3       R9
  Watchdog                      S4                           N12
  Heartbeat                     S5                           N13
  Failover routing              S6                           N14

Reasoning:
  - Ensures no common mode failure by using different hardware and operating system (see Risk 8)
  - Worst-case rollover is accomplished in 4 seconds, as computing state takes that long at worst
  - Guaranteed to detect failure within 2 seconds based on rates of heartbeat and watchdog
  - Watchdog is simple and has proved reliable
  - Availability requirement might be at risk due to lack of backup data channel (see Risk 9)

Architecture diagram:
  Primary CPU (OS1) ──┐
        │ heartbeat   ├──▶ Switch CPU (OS1) ──▶
        │ (1 sec)     │
  Backup CPU w/ Watchdog (OS2) ──┘
```

## Numbering convention

Number findings **across the whole evaluation**, not per scenario, so the reasoning text of any
record can cite a finding raised elsewhere:

- `S1, S2, …` sensitivity points — decisions with a marked effect on a response
- `T1, T2, …` tradeoff points — one decision where two responses move in opposite directions
- `R1, R2, …` risks — decisions that may lead to undesirable consequences
- `N1, N2, …` non-risks — decisions analysed and deemed safe

## What makes a record usable

**A decision appears on a row, not a component.** "Backup CPU(s)" is a decision. "The CPU" is not.

**One decision can carry several finding types.** In the example, "no backup data channel" is
simultaneously a sensitivity, a tradeoff and a risk. That is the normal case for the interesting
decisions, and the reason the columns are separate rather than a single label.

**Non-risks are recorded with the same weight as risks.** Three of the five decisions above are
non-risks. Writing them down is what tells a later reader those decisions were examined rather than
overlooked — silence and safety are different claims.

**The reasoning carries the numbers.** "Worst-case rollover in 4 seconds", "detect failure within 2
seconds" — the figures are what let someone else check the verdict. Reasoning without figures is
an assertion that the scenario was considered.

**Name the assumption that would change the verdict.** A record whose reasoning holds under every
possible world is not analysis. If the verdict depends on the failure rate, the client count or the
network being in one data centre, say so — that line is what makes the finding re-checkable when the
assumption moves.
