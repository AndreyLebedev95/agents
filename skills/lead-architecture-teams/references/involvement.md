# Setting your level of involvement

Read when deciding how involved to be with a team, how many teams you can cover, or when re-checking as a project changes.

## The three personalities as a spectrum

They are not personality types so much as positions on one axis: how tightly you constrain the team.

```
armchair  ←———————————— effective ————————————→  control freak
(too few constraints)                        (too many constraints)
```

**Control freak.** Decisions too fine-grained and too low-level. Restricting useful or necessary open source libraries. Dictating naming conventions, class designs, method lengths. In the extreme, writing pseudocode for developers to implement, which takes the art of programming away from them and loses their respect.

Easy to fall into when transitioning from developer to architect, because the internal design work is exactly what you used to do and were good at.

**Armchair.** Has not coded in a long time or ever. Does not account for implementation details. Disconnected from the team, rarely around, moves on to the next project after the initial diagrams.

Nobody intends this. It happens when an architect is spread too thin across projects or teams and loses touch with the technology or the business domain. The fix is to get more involved in the project's technologies and build a stronger understanding of the domain.

**Effective.** Appropriate constraints, team members working well together, the right level of guidance, the tools and technologies the team needs, and roadblocks removed.

## The boundary that defines control-freak territory

| Architect's job | Developer's job |
|---|---|
| Identify the logical component | Determine how best to implement it |
| Determine its core set of operations | Class diagrams |
| Identify which other components interact with it | Design pattern selection |
| | Internal data structures |

Worked: for a component managing reference data — static name-value pairs, product codes, warehouse codes — the architect identifies the component, names its operations (`GetData`, `SetData`, `ReloadCache`, `NotifyOnUpdate`), and identifies its collaborators.

Deciding the component should be implemented with a parallel loader pattern using an internal cache with a particular data structure crosses the line. That might be an effective design. It might even be the best one. It is not the architect's to make.

## The five factors

Assume a fixed scale of ±20 points per factor. Negative values indicate less involvement, ending at the armchair extreme; positive values indicate more, ending at the control-freak extreme. The scale is not exact — it is a way of making a subjective judgment discussable.

**Team familiarity.** How well do the members know each other? Have they worked together before? The better they know each other, the more they self-organize and the less they need the architect. The newer they are to each other, the more the architect is needed to facilitate collaboration and reduce cliques.

**Team size.** More than 12 developers is a big team; 5 or fewer is small. The larger the team, the more the architect is needed. (Check the three team-size warning signs separately — a team may need splitting rather than more architect attention.)

**Overall experience.** What is the mix of senior and junior developers? How well do members know the technology and the business domain? Teams with many junior developers require more involvement and mentoring. With mostly senior developers, the architect becomes a facilitator rather than a mentor.

Where the business domain is particularly complex, assess technological experience and business-domain experience **separately** — they diverge more often than people expect, and a team senior in technology and new to the domain needs a different kind of attention than the reverse.

**Project complexity.** Highly complex projects require the architect to be available to assist with issues. Relatively simple, straightforward projects require less.

**Project duration.** Short (~2 months), average (~6 months), or long (~2 years). **Involvement grows with length**, which surprises people.

The reasoning: two months is not a lot of time to qualify requirements, experiment, develop code, test every scenario and release to production. The team already has a keen sense of urgency, and a heavily involved architect would get in the way and delay the project — so behave more like an armchair architect. On a two-year project, developers are more relaxed and feel no sense of urgency; they are planning holidays and taking long lunches. The architect is needed to keep the project on schedule and to ensure the most complex tasks are accomplished first.

## Two worked scenarios

**Scenario 1**

| Factor | Value | Rating | Tends toward |
|---|---|---|---|
| Team familiarity | New team members | +20 | Control freak |
| Team size | Small (4 members) | −20 | Armchair |
| Overall experience | All experienced | −20 | Armchair |
| Project complexity | Relatively simple | −20 | Armchair |
| Project duration | 2 months | −20 | Armchair |
| **Accumulated** | | **−60** | **Armchair** |

Limit involvement in daily interactions. Facilitate, but stay out of the team's way. You will be needed to answer questions and make sure the team is on track; otherwise be largely hands-off and let an experienced team do what it does best — develop software quickly.

**Scenario 2**

| Factor | Value | Rating | Tends toward |
|---|---|---|---|
| Team familiarity | Know each other well | −20 | Armchair |
| Team size | Large (12 members) | +20 | Control freak |
| Overall experience | Mostly junior | +20 | Control freak |
| Project complexity | High complexity | +20 | Control freak |
| Project duration | 6 months | −20 | Armchair |
| **Accumulated** | | **+20** | **Control freak** |

Take on a mentoring and coaching role and be fairly involved in day-to-day activities — but not so much as to disrupt the team.

## Using the scale honestly

**Re-run it.** Architects use these factors at the start to plan involvement, and the level usually changes as the project progresses. Analyze them continually through the lifecycle.

**Weight where appropriate.** It is difficult to make these factors fully objective, and some — overall experience, typically — carry more significance than others. Weight or modify the metrics to suit the situation.

**The output is a direction, not a number.** The point is that the appropriate amount of involvement varies according to these five factors, and scoring them makes that variation discussable with a team lead or a project manager instead of being a matter of personal style.
