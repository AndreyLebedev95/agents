# Eliciting definitions from people

Read when the source of the glossary is conversation rather than documents. Contents: [the stance](#the-stance) · [opening questions](#opening-questions) · [drawing out invariants](#drawing-out-invariants) · [finding the edges](#finding-the-edges) · [detecting a term that needs splitting](#detecting-a-term-that-needs-splitting) · [when two people disagree](#when-two-people-disagree) · [what not to do](#what-not-to-do)

## The stance

Most of what you need is tacit. It is not written anywhere and not because anyone was negligent — it is the part of the job so routine to the person doing it that it never occurs to them to say it.

So this is usually not retrieval. Asking these questions frequently makes people notice, for the first time, that their own understanding has a gap, an unstated assumption, or a conflict with a colleague's. That is the most valuable output, and it means the exercise is co-creating the model rather than extracting one. Expect this most in the areas the business considers its own speciality, where the learning genuinely runs both ways.

Two consequences for how you behave:

- **A concept nobody can define is a finding, not a failure of the interview.** Record it and move on.
- **Do not fill gaps yourself.** The plausible definition you invent will be adopted, and nobody will ever remember it was a guess.

## Opening questions

Establish the concept before arguing about the word:

- "Walk me through what happens to a *<term>* from the moment it appears to the moment you stop caring about it."
- "Who creates one? Who else touches it?"
- "If I showed you two of these, how would you tell them apart?" — separates value-like concepts from identity-bearing ones.
- "What would make you say a *<term>* is in a bad state?" — the fastest route to invariants.
- "Is there anything that looks like a *<term>* but isn't one?" — surfaces near neighbours and the distinction that defines both.

## Drawing out invariants

Invariants almost never arrive when asked for directly, because "what must always be true" sounds like a trick question. Approach sideways:

- "What would be obviously broken if you saw it on a screen?"
- "Has anyone ever managed to get one into a state that shouldn't exist? What happened?"
- "What do you check before you let this go through?"
- "Is there anything you'd have to fix by hand if it went wrong?"

Incident stories are dense with invariants. Every "we had to go in and correct it manually" describes a rule the system did not enforce.

## Finding the edges

Definitions arrive describing the path where everything works. The rest of the model is in what was not mentioned:

- "You said it goes to <state>. What else could happen instead?"
- "What if that arrives late? What if it never arrives?"
- "What if two happen at the same time?"
- "Can this ever go backwards?"
- "Is there a time limit? What happens when it passes?"
- "Who can undo this, and until when?"

The time-limit question is disproportionately productive: deadlines, grace periods and expiry windows are business rules that are almost never volunteered, and they are usually where the disagreements are.

## Detecting a term that needs splitting

Signals that one word is carrying two meanings:

- The definition needs "usually" or "in some cases".
- You cannot write a single invariant that holds for every instance.
- Two people give definitions of different *shape* — one describes an event, the other a process.
- The lifecycle has branches that share no states.
- Counts disagree between teams who both believe they are counting the same thing.

Confirming question: "Is the thing the <other team> calls a *<term>* the same thing you mean?" Ask both sides separately; asking them together tends to produce a polite merge rather than the truth.

## When two people disagree

Do not mediate toward a compromise definition. A merged definition satisfying both is usually true of neither, and it will fail silently.

Instead:

1. Record both, attributed.
2. Establish whether they differ in *structure and behaviour* or only in wording. Wording differences are a synonym problem. Structural differences mean two concepts.
3. If two concepts: name them separately and identify which boundary each belongs to.
4. If genuinely one concept with one meaning: put the decision to whoever owns the area. Your job is to make the choice visible and forced, not to make it.

## What not to do

- **Do not teach the vocabulary of software design.** The shared language is the language of the business. Abstract factories are not part of it.
- **Do not accept a definition you cannot restate.** If you cannot say it back in your own words and have them agree, you have a phrase, not a definition.
- **Do not schedule everything.** Informal conversation — passing questions, coffee breaks — surfaces more than formal review meetings, because people are less invested in defending a previous answer. Domain experts are generally glad to talk to someone genuinely interested in their work.
- **Do not treat the first pass as final.** Everyday use of the language reveals distinctions that no interview would have produced. Expect to revise.
