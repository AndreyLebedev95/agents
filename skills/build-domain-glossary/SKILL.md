---
name: build-domain-glossary
description: Builds the authoritative glossary for a domain — one term, one meaning, stated in the language of the business — plus the scenarios that carry the rules a definition cannot hold. Covers splitting a term that carries two meanings, separating apparent synonyms that turn out to be different concepts, driving out technical jargon, capturing behaviour, causality and invariants rather than nouns alone, pairing the term list with Given/When/Then scenarios, and recording conflicts and undefined concepts as findings. Use whenever someone asks for a glossary, canonical terminology, a domain dictionary, a data dictionary or naming conventions for a model; when the same concept goes by several names across services, documents, teams or parallel work streams; when a term turns out to mean two different things; when a spec's nouns need fixing before work starts; or when the code's names and the business's names have drifted apart — even if the request is only "what should we call this". For deciding which boundary a term is valid inside use map-subdomains-and-boundaries; for deriving terms from a business process use derive-model-from-business-process; for lifecycle states and event names use model-lifecycle-and-events; for stopping an existing glossary from going stale use sustain-living-documentation.
---

# Building a domain glossary

A glossary is not a courtesy for newcomers. It is the mechanism that stops parallel work — several people, several teams, several concurrent agents — from inventing three names for one concept and then building three incompatible things.

The value is concentrated in one rule: **each term carries exactly one meaning**. Everything else here serves that rule or works around its limits.

## The output

A glossary document with three parts.

**1. Term entries.** One per concept:

```markdown
### <Term>
**Context:** <which boundary this definition is valid in>
**Means:** <one sentence, business language, no alternatives>
**Behaviours:** <what it does or what happens to it>
**Invariants:** <what must be true of it at every moment>
**Relates to:** <cause-and-effect links to other terms>
**Not to be confused with:** <the near-neighbour term and the difference>
```

**2. Banned synonyms.** A flat table, because this is the part people actually consult mid-argument:

| Do not use | Use instead | Why they are different |
|---|---|---|

**3. Scenarios.** Every rule that will not fit inside a definition, written as Given/When/Then in business language.

Plus a **Findings** section: concepts nobody could define, and conflicts where two people gave incompatible answers. These are results, not blockers — record them and keep going.

## Where the terms come from

Get definitions from the people who originated the requirements or who will use the system. Not from analysts relaying them, not from engineers who inherited them. Each hand-off between a knowledge holder and you loses information, and the loss is invisible: what arrives is a coherent-sounding account that is subtly wrong. When engineers can only describe the system in terms of tables and endpoints, that chain is why.

Expertise has scope. Someone may know one area deeply and guess about the next. Note which person owns which area, so a definition can be traced back and challenged.

If no such person is reachable, the glossary you write is a set of hypotheses. Say so in the document rather than letting it read as settled.

## The procedure

### 1. Collect every term and every place it appears

Sweep the specs, tickets, code, database, interface labels and conversations. You want the raw vocabulary before any tidying, including terms you suspect are duplicates — those are the interesting ones.

### 2. Write the single definition each term must carry

One sentence. If you find yourself writing "usually means X, but in some cases Y", stop: you have found an ambiguous term, which is step 3.

### 3. Split terms that carry two meanings

A term with two meanings cannot be modelled. People resolve the ambiguity from conversational context without noticing they are doing it; software and parallel agents cannot.

The move is to coin two explicit terms and retire the ambiguous one. If "policy" means both a regulatory rule and an insurance contract, the glossary gets **regulatory rule** and **insurance contract**, and "policy" goes into the banned-synonyms table pointing at both with the disambiguating question.

### 4. Separate apparent synonyms

When two words are used interchangeably, the default assumption should be that they are *not* synonyms — they usually denote different concepts that happen to overlap in casual speech.

A system with "user", "visitor" and "account" floating around rarely has three words for one thing. It usually has: visitors, whose data feeds analysis and who cannot act; and accounts, which exercise functionality and have permissions. Those are different concepts with different behaviour, and collapsing them into "user" throws away a distinction the model needs.

So for each pair, look for the behavioural difference that justifies keeping both. Found one? Keep both, define both, and state the difference in each entry. Found none? Retire one and record it as a banned synonym.

### 5. Drive out technical jargon

Test each definition by asking whether the person who runs this part of the business would recognise it as a description of their work.

- "A rollout can be started only if at least one of its phases is active" — belongs in the glossary.
- "A rollout can be started only if it has at least one row in the active_phases table" — does not.

Strike any definition mentioning tables, records, files, endpoints, services or classes, and rephrase using only nouns and verbs the business uses. A rule you cannot rephrase is a rule you do not yet understand — that is a finding, not a formatting problem.

This matters beyond tidiness. Someone who knows only the solution-shaped phrasing cannot tell *why* a rule exists, which caps how good a model they can build and makes every edge case a surprise.

### 6. Add behaviour, causality and invariants

A list of nouns with attributes is a data schema, not a model of the domain. For each term record what it does, what happens as a consequence of what, and what must be true of it at every moment.

The invariants are the highest-value part and the part most often missing, because nobody states them out loud — they are the rules so obvious to the business that they never come up until something violates one.

### 7. Write scenarios for the rules that will not fit

Glossaries are structurally good at nouns and structurally bad at behaviour. A rule is not a verb hung off a noun; it is a conditional with assumptions and edge cases. Trying to compress one into a definition either mangles it or silently drops half of it.

So let the term list be the noun reference, and put every remaining rule in a Given/When/Then scenario in business language. Domain experts can read these and confirm or correct them, which is the point — do not expect them to write the scenarios themselves.

```gherkin
Scenario: Escalating a rollout that has stalled
  Given a rollout in the Canary phase
  And the failure rate has exceeded the phase's threshold
  When the rollout is evaluated
  Then the rollout is halted
  And the operator on call is notified
```

### 8. Record what you could not settle

Concepts nobody can define, and questions where two people answered differently, go in Findings with who said what. Asking these questions is usually not retrieval — it forces people to resolve ambiguities and gaps in their *own* understanding, which is why this section tends to be the most useful output of the whole exercise.

Also chase what nobody volunteered: definitions arrive describing the path where everything works. Ask what happens on each path not mentioned.

## One term, one meaning — inside one boundary

The rule is scoped. The same word may legitimately mean different things in different parts of a business, and that is not an error to correct.

"Lead" can be a notification event to a marketing team and an entire multi-week process to a sales team. Both are right. Forcing one definition on both gives marketing a model far heavier than they need, or sales one too thin to work with.

So when definitions genuinely differ in structure or behaviour, do not merge them. Name the context each belongs to and record the term separately under each, stating explicitly that these are different concepts sharing a spelling.

**Do not solve this by prefixing.** "Marketing lead" and "sales lead" fails twice: it forces a decision about which model applies every time anyone touches either, with the mistake getting easier the closer the two sit; and nobody says the prefix out loud, so the written model drifts away from the language people actually speak. If the codebase is full of qualified names that appear in no conversation, this is what happened.

Deciding where those boundaries fall is a separate job — see `map-subdomains-and-boundaries`.

## Naming conventions worth fixing early

- **Events are past tense.** `device-registered`, `rollout-halted`. They name something that already happened and cannot be refused.
- **Commands are imperative.** `halt rollout`, `register device`. They name a request that can be rejected.
- **Names in the model follow the glossary, not the reverse.** Entity names, field names, command names and event names come from the agreed term. When the code needs a name the glossary does not have, that is a missing term, not a licence to invent one.
- **Mark which terms are public.** Terms internal to one boundary and terms appearing in a contract other components consume are different populations with different change costs. Flag them, so nobody renames a public term casually.

## Failure modes

| Tell | What happened | Fix |
|---|---|---|
| Definitions mention tables, endpoints, classes | Solution view substituted for the business view | Rephrase in business terms; if you cannot, you do not understand the rule yet |
| Codebase full of qualified names nobody says aloud | Prefixing used instead of naming the boundary | Name the contexts; keep the bare term inside each |
| Glossary exists, nobody speaks from it | It was documented instead of used | Reinforce it in specs, tests, docs and code; make maintenance everyone's, not a lead's private duty |
| Every term defined only for the happy path | Elicitation stopped at the first answer | Ask what happens on every path not mentioned |
| A list of nouns with attributes | Data schema mistaken for a domain model | Add behaviours, causality and invariants |
| Two teams "agree" but build incompatible things | A shared word hid two meanings | Look for the term both use and neither defined |

## Keeping it honest

Cultivating the language is continuous, not a one-time deliverable. Everyday use surfaces deeper distinctions, and when one appears the glossary has to change to match — a glossary frozen at the moment of writing quietly becomes wrong.

Tools help and do not substitute. A wiki, a linter that checks term usage, a search across the codebase: all useful for *managing* the language, none of them a replacement for people actually speaking it in specs, tests, code and conversation. Expect changing entrenched terminology to take time.

For diagnosing an artifact that has already gone stale and making the practice survive, use `sustain-living-documentation`.

## Bundled references

- `references/glossary-format.md` — the full entry template, the banned-synonym record, and worked before/after splits of an ambiguous term and a false synonym pair. Read this when you are about to produce the artifact.
- `references/eliciting-definitions.md` — question sets for drawing out tacit knowledge, unstated edge cases and the invariants nobody says out loud. Read this when the source is people rather than documents.

## Worth reading

- Eric Evans, *Domain-Driven Design* (2003) — the origin of the shared-language practice.
- Cyrille Martraire, *Living Documentation* (2019) — on knowledge sharing that survives contact with a real codebase.
