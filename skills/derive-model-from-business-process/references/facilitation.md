# Facilitating a derivation session

Read when a group session is being planned rather than a solo analysis pass. Contents: [who](#who-should-be-there) · [materials](#materials-and-the-colour-code) · [opening](#opening-the-session) · [dynamics](#managing-the-dynamics) · [questions](#questions-that-move-a-stuck-session) · [remote](#remote-sessions) · [afterwards](#what-to-do-afterwards)

## Who should be there

**Diverse.** Anyone connected to the process in question: engineers, domain experts, product owners, testers, designers, support staff. More varied backgrounds surface more knowledge, and the gaps tend to appear precisely where two roles' understanding meets.

**Capped at around ten.** Above that, not everyone can contribute, and a session where half the room is spectating loses the thing that made it worth doing. If more people need to be involved, run more sessions rather than a bigger one.

The goal is to learn as much as possible in the shortest time. These are usually busy people whose time is expensive — that is a reason to prepare properly, not a reason to shorten the session.

## Materials and the colour code

A large modelling surface — a wall covered in paper is ideal, a very large whiteboard acceptable. It will not be big enough; that is normal. Plenty of sticky notes in each colour, and enough markers that supplies never become the bottleneck on someone's idea.

The conventional colour code, worth keeping so the model is legible to anyone who has done this before:

| Element | Colour | Written as |
|---|---|---|
| Domain event | orange | past tense — `order shipped` |
| Command | blue | imperative — `submit order` |
| Actor / role | small yellow | the role, attached to a command |
| Policy (automation) | purple | the rule, with its conditions |
| Read model | green | the view the decision needed |
| External system | pink | the system's name |
| Aggregate | large yellow | commands left, events right |
| Pain point | pink, rotated to a diamond | the concern |

Sessions run about two to four hours. Bring food.

## Opening the session

With a group new to this, spend the first few minutes on the process itself: what you are about to do, which process you are exploring, and the elements you will use.

**Build the legend as you introduce each element** — write each element type on a note of its colour and post it. Leave it visible for the whole session. People will refer to it far more than they expect to, and it removes a recurring low-grade interruption.

## Managing the dynamics

**Track the energy.** When the pace slows, the cause is either a stuck point or a finished step. Ask a question to reignite it, or move to the next stage. Sitting in a slow patch is how sessions lose the room.

**Everyone participates.** If people are drifting to the edges, draw them back with direct questions about the current state of the model — not "any thoughts?", which invites silence, but "does this match how you'd describe it?"

The point is not politeness. The person who has gone quiet is often the one who knows the exception nobody else does.

**Take breaks, and resume properly.** This is intense work. When you break, do not resume until everyone is back, and restart by walking the current state of the model out loud. That returns the group to a shared position rather than to whatever each person was thinking about when they left.

**Capture concerns whenever they arise.** Do not wait for the pain-points step. When someone raises a doubt at any point, mark it on the surface immediately.

## Questions that move a stuck session

**Finding events nobody has mentioned:**
- "What happens if that never arrives?"
- "What if two of these happen at once?"
- "Can this ever go backwards?"
- "Who finds out when this goes wrong?"

**Finding the conditions on a policy:**
- "Does that always happen, or only sometimes?"
- "Has there ever been a case where you didn't want that to fire?"

**Finding invariants:**
- "What would be obviously broken if you saw it on screen?"
- "Has anyone got one into a state that shouldn't exist? What happened?"
- "What do you have to fix by hand when it goes wrong?"

Incident stories are dense with rules nothing was enforcing. Every "we had to correct it manually" is an invariant the model is missing.

**Finding time-based rules:**
- "Is there a deadline on this? What happens when it passes?"
- "Who can undo this, and until when?"

Expiry windows, grace periods and timeouts are business rules that are almost never volunteered and are frequently where two people disagree.

**When two people disagree:** do not mediate toward a middle definition. Record both, attributed, and establish whether they differ in structure and behaviour or only in wording. Structural differences mean two concepts, which usually means a boundary. Wording differences mean a terminology decision someone has to own.

## Remote sessions

This was designed as a colocated, low-technology activity, and it does not transfer cleanly. Remote groups do not reach the same levels of participation, and since participation is the mechanism by which knowledge gets shared, the output is genuinely weaker — not merely less pleasant.

Remote sessions happen anyway. If you must:

- Be more patient. Everything takes longer.
- Accept less effective collaboration and plan around it — smaller groups, more sessions, more explicit turn-taking.
- Use a shared infinite canvas tool that supports simultaneous editing.
- Be more deliberate about drawing people in, since the ambient cues that show someone wants to speak are absent.

## What to do afterwards

The wall is not the deliverable and it will not survive. Before the room clears:

- **Photograph it in sections**, legibly, with enough overlap to reconstruct.
- **Transcribe the findings first** — the pain points, the unattributed commands, the conflicts — because those are the parts with owners and deadlines attached, and they are what decays fastest in memory.
- **Write up the terminology while the session is fresh.** See `build-domain-glossary`.
- **Note what was inferred versus stated.** Six months later nobody can tell the difference, and the inferences are where the wrong assumptions live.
