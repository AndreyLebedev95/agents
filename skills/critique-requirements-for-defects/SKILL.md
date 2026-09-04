---
name: critique-requirements-for-defects
description: Attacks a requirements artifact — a requirement, user story, spec section, or acceptance-criteria list — for defects before it moves to design or implementation, and returns a findings list of ambiguous wording, contradictions, untestable statements, and requirements with no acceptance criteria. Runs mechanical techniques against the text itself (word-stress readings, dictionary-sense substitution, comparative-word checks, solution-vs-outcome checks, root-assumption checks) instead of relying on a read-through to "feel" vague. Use whenever a requirements document, user story, spec, PRD, or acceptance-criteria list needs review, sign-off, or a defect/ambiguity/testability check before implementation starts — even if the request is just "does this look right," "can we build this yet," "review this spec," or "is this ready for design." Also use proactively before approving or signing off on any requirements artifact, even without the words "ambiguity," "defect," or "review." Not for writing or eliciting requirements, not for generating design ideas, and not for checking finished implementation against a spec.
---

# Critique Requirements for Defects

A finished-looking requirement is not the same thing as a correct one. Most requirements defects don't look like gaps — they look like ordinary, confidently-stated sentences that different readers will silently interpret differently, or specific-sounding demands nobody could ever fail to meet, or solutions dressed up as needs. Catching these before design starts is cheap; catching them after is not; catching them after ship is worse by an order of magnitude or more per stage. That asymmetry is the entire justification for this review — see `references/evidence.md` if you need to make that case to someone skeptical of spending review time on "words on a page."

This skill is a critic, not an author. Its job is to find and report defects in an existing artifact, not to rewrite the requirement, design a fix, or decide whether a requirement is a good business idea. Findings only.

## Operating stance

Don't read a requirements document straight through hoping ambiguity will jump out. It won't — that's exactly why it survived to this point. Instead, run specific techniques against specific statements. A finding that isn't traceable to a technique ("this feels vague") is not a finding; it's a hunch. Every finding below should be able to answer "what did I do to find this, specifically?"

Work one discrete statement at a time — one requirement, one acceptance criterion, one sentence. Ambiguity hides at sentence grain and disappears when you skim a whole page at once.

Expect some of the techniques below to produce silly or absurd alternate readings. That's not a sign the technique failed — a sentence that supports a ridiculous reading is a sentence proven not to be as precise as it looked. Don't discard odd results; they're often the tell that leads to the real ambiguity.

The strongest findings usually come from stacking two or three techniques on the same statement, not from picking the one that seems most relevant and stopping. A comparative word (technique 2) is often also the word worth running dictionary substitution on (technique 3); a statement that fails the testability check (technique 5) is often also a solution in disguise (technique 4). Don't treat the numbered steps below as a menu to choose one from — run a suspicious statement through all of them.

Not every technique will produce something on every statement, and that's normal, not a sign you're doing it wrong. If the stress-test comes up empty, move on to the next technique rather than forcing a finding.

## Defect categories

Every finding belongs to exactly one of these six categories. Decide the category *before* writing the finding up — it's what keeps a finding a finding instead of a vague complaint:

- **Ambiguity** — the wording, taken as written, genuinely supports more than one *complete, internally coherent* reading, and different readers could land on different ones. Covers stress-test and dictionary-substitution results (a word with several senses, each of which gives a different but fully-formed meaning) and terms the artifact uses without ever defining (see technique 6). The test: can you name two or more specific, different things this could mean, each of which would look "done" to whoever assumed it?
- **Contradiction** — two statements conflict, either directly or because they rest on incompatible unstated assumptions about the same foundational question.
- **Untestable** — the statement doesn't describe anything checkable, *even taken at face value, under any reading*. Covers solutions standing in for outcomes (technique 4) and comparative or relative words with no stated reference point (technique 2) — "fast," "small," "reasonable effort" fail as a check no matter which specific reading you assume, because no reading was ever offered a baseline to check against. This is the dividing line from ambiguity: ambiguity is "which of these several specific meanings did they intend," untestable is "even the most generous specific meaning still can't be checked."
- **Missing acceptance criteria** — the requirement names a real, checkable-in-principle outcome, but no metric, threshold, or example was ever attached to it. The difference from "untestable": here, something *could* make this checkable, it's just absent; there, what's present couldn't function as a check even if you filled in the blanks.
- **Missing requirement** — the artifact is completely silent on an entire attribute, scope boundary, environment, or condition — not a weak statement, no statement at all. This is a gap in the requirement *set*, not a defect in one requirement's wording.
- **Unstated assumption** — a foundational premise (direction, scope, audience, environment) that nothing in the document states or challenges, and that would send the whole artifact in a different direction if it turned out to be wrong.

If a defect doesn't cleanly fit one category, pick the nearest one and say in the finding why it's a borderline case — don't silently force-fit it.

## The procedure

Work through each statement in the artifact:

### 1. Stress-test the wording

Read the sentence once per word, mentally (or literally) stressing only that word each time, and ask what that emphasis implies was being singled out or contrasted with something else. Do this for every word in the sentence, then, if the sentence is short, for pairs of words together.

*Example:* "Mary had a little lamb." Stress "Mary" and you're implicitly contrasting her with someone else who didn't have one. Stress "had" and you're implying she no longer has it. Stress "little" and you're distinguishing it from a larger lamb. Stress "lamb" and you're ruling out a dog, a cat, a goat. Five words, six distinct readings from single-word stress alone, more from combinations — and that's a five-word children's rhyme. A real requirement sentence will yield just as many, and they won't be silly.

Flag any statement where two or more stresses produce genuinely different, plausible readings. That divergence is the defect — write it down before moving on to the next technique.

Full worked mechanics and a second example (a single ambiguous noun traced through a dozen dictionary senses) are in `references/ambiguity-techniques.md` — read it before applying this technique for the first time, or whenever a statement resists a quick pass.

### 2. Check comparative and relative words

Any word that only means something *relative to* a reference class — "small," "fast," "cheap," "sufficient," "reasonable," "as needed," "user-friendly" — is unusable as a check by construction unless the requirement also states the reference point. "Small" for a football stadium and "small" for a coffee shop differ by orders of magnitude, and nothing about the word itself narrows it down.

For every comparative or relative word in the statement, ask "compared to what?" If the answer isn't in the document, that's a finding — not a style nitpick, a real defect, because different builders will supply different reference points and produce genuinely different products, each internally consistent with the stated requirement. File this as **untestable**, not ambiguity: the issue isn't that "fast" has several distinct candidate meanings to choose between, it's that no reference point exists under *any* reading, so nothing built could ever be checked against the word as written.

### 3. Substitute dictionary senses of the load-bearing word

Once the stress-test points at a specific word as the likely source of trouble, look up its full range of dictionary senses — not just the obvious one — and re-read the sentence under each sense in turn. Common nouns and short verbs often carry ten or more senses that have nothing to do with each other (a "point" can be a tip, a location, a moment in time, a unit of scoring, a purpose, a small mark, a rhetorical claim...). Whichever sense the reader defaults to is doing unstated interpretive work.

This also works across an entire phrase: pick each operative word, list its senses, then mix and match combinations across words to construct alternate full-sentence readings, including deliberately absurd ones. Proving a sentence supports an absurd alternate meaning under its own dictionary is proof the "obvious" reading was never actually forced by the words — it was supplied by the reader. See `references/ambiguity-techniques.md` for the worked nursery-rhyme example that demonstrates just how far two ordinary words can be pushed.

Especially apply this when a requirement may have been authored in, or will be read in, a different context than yours — context is exactly what silently selects one sense over the others, and a different reader in a different context will select differently.

### 4. Check for a solution wearing a requirement's clothes

Ask of every statement: "what problem does this solve, and how would we know it was solved?" If the statement names an implementation, a feature, or a specific fix rather than an observable, checkable outcome, and the author can't restate it in outcome terms, it's a solution in disguise — not a requirement.

This matters because a solution-shaped requirement hides the actual need, and different readers silently attach different real needs to the same surface request. "We need sharper carbon copies" sounds specific and buildable — it took direct questioning to discover the real need was one legible digital copy per recipient, with no carbons and no paper at all. Two engineers could both "satisfy" the literal words and build completely different, both wrong, things. File this as **untestable**, not ambiguity — the problem isn't that the statement is unclear, it's that a feature described this way can never be checked against the need it's supposed to serve.

### 5. Check testability directly

Ask two separate questions, because they produce two different categories of finding:

- Does the statement describe anything checkable *at all*, even in principle — or is it a comparative word, a subjective quality, or another form nothing could ever satisfy or fail regardless of how you fill in the blanks? That's **untestable**.
- Does it describe something checkable in principle, but never actually attach the metric, threshold, or example that would let anyone run the check? That's **missing acceptance criteria** — the shape of a real requirement is there, the specific number or condition isn't.

A statement that nobody could ever fail to meet is not a requirement — it's a wish. If every plausible implementation would satisfy the wording, the wording isn't doing any work.

### 6. Watch for introduced elements

While reading (or discussing) the artifact, track every noun and term the artifact actually defines versus every term that creeps into the conversation around it without ever being defined. A word that "feels like" a natural paraphrase of something in the document, but never actually appears in it, silently narrows the solution space the moment people start treating it as settled — and different readers will each silently narrow it in their own direction. File this as **ambiguity**: an undefined term genuinely supports several distinct, complete readings — each reader silently supplies their own specific definition, and each of those definitions is coherent on its own. This is also exactly where contradictions between people (not yet between documents) are born, and it shows up later as a full-blown contradiction once each side has built on their own unstated version of the term.

### 7. Cross-check for contradiction — including the quiet kind

Check requirements against each other for direct, obvious contradiction first. Then check for the quieter form: two requirements that are each individually consistent with everything explicitly stated, but that rest on incompatible unstated assumptions about the same foundational question — direction, scope, audience, environment, or similar.

This quiet form is more dangerous precisely because it passes every consistency check. A solution can satisfy every single stated answer and still solve the wrong problem, because the framing assumption that would have exposed the conflict was never asked about at all. Treat "internally consistent" and "correct" as two separate questions, and check both — consistency only proves nobody asked the question that would have surfaced the real disagreement.

### 8. Check for missing requirements, not just wrong ones

Ask what the artifact never mentions: what attributes, environments, constraints, or edge conditions does it leave completely silent on? Silence is not neutral — it's exactly where each implementer will independently guess, and each guess will differ. A requirement set that is internally airtight can still be riddled with holes nobody has looked for, because looking for an absence takes a deliberate pass, not just a read-through. File this as **missing requirement**, distinct from missing acceptance criteria: this category is for a gap in the whole *set* (nothing addresses data retention, or access control, or what happens on failure), while missing acceptance criteria is for a single existing requirement that names an outcome but never says how to check it.

### 9. Weight and prioritize the findings

Not all findings are equal. A false or missing assumption at the *foundation* of a requirement — the kind of assumption that would send the whole solution in a different direction if corrected — is far more costly than a wording nit in a downstream detail, even when the wording nit is more obviously "wrong" on the page. Order findings so the foundational ones are addressed first: a single foundational fix can make a dozen smaller findings moot, while fixing a dozen wording nits first and then hitting a foundational problem wastes all of that work.

When two findings both look foundational, rank the one that would invalidate more of the rest of the document higher — ask "if this turned out wrong, how much of everything else becomes moot?" and order by that answer, not by how early the finding appears in the document or how confident-sounding the wording is.

If reviewers or stakeholders are actually available to poll (not just yourself reading solo), the real version of this whole procedure is even stronger: give each reviewer the identical statement, have them independently and privately commit to a concrete answer or interpretation with no chance to discuss first, then tabulate the results. Genuine disagreement across people — not just variation in wording between people who agree — is direct, empirical proof of ambiguity, and is worth more than any solo technique above. Where this is available, run it in addition to (not instead of) the solo techniques, since it will surface disagreements that no single reader, however careful, will find by working alone.

## Reporting findings

Report every finding with:

- **Quote** — the exact text being flagged. A contradiction or a cross-item unstated assumption legitimately needs two or more quotes, one from each conflicting statement — don't force a relational finding into a single-quote shape.
- **Category** — one of the six defect categories above.
- **How it was found** — which technique(s) surfaced it and what the divergent readings, missing reference point, or gap actually are.
- **Fix or open question** — either a concrete rewording, or the specific question that needs answering to close the gap.

Never report a category without the technique that produced it. "This seems ambiguous" is not a finding; "stressing 'small' produces no answer to 'compared to what' — 25,000 people is small for a stadium and enormous for a coffee shop" is.

If the artifact has no numbered items or stable identifiers, quote enough of the exact text (the first several words, or the whole statement if short) that the finding can be located without ambiguity about which sentence you mean.

Label each finding **candidate** or **confirmed**. Everything found by reading solo — stress-test, dictionary substitution, the comparative-word and testability checks — is a candidate: a plausible-reading analysis, not proof anyone will actually misread it that way. Only a finding backed by an actual poll of independent readers (the last paragraph of step 9) earns **confirmed**. Don't blur this distinction — a candidate finding can still be worth fixing, but it shouldn't be reported with the same certainty as a confirmed one.

Order the findings list foundational-first, per step 9 above — don't just list them in document order.

## Common failure modes to avoid

| Symptom | What's actually happening | Fix |
|---|---|---|
| Sign-off happens because every stated answer is internally consistent | Consistency mistaken for correctness — nobody separately checked the foundational framing | Explicitly test the root-level assumption (direction, scope, audience) as its own step, not just cross-check the details |
| A requirement reads as complete, but implementation still has to guess at something basic | The "obvious" next step or default was never actually written down, just assumed shared | Ask "what happens right after this is satisfied — is *that* specified too?" |
| Two reviewers approve the same document but have different mental models of what it asks for | Interpretation ambiguity was mistaken for clarity because nobody checked independently | Where possible, poll reviewers independently before sign-off rather than relying on a shared read-through |
| A finding gets flagged "vague" with nothing actionable attached | The review was feeling-based rather than technique-based | Always name the technique used and the specific divergent readings it produced |
| A "requirement" turns out to be a proposed fix, and the real need was something else entirely | Nobody challenged it with "what problem does this solve" before accepting it | Run the solution-vs-outcome check (step 4) on every requirement, not just the ones that sound like technology |

## When you need more

- `references/ambiguity-techniques.md` — full worked mechanics of the stress-test and dictionary-substitution techniques, with a complete example tracing one ambiguous word through a dozen distinct dictionary senses. Read this before applying either technique for the first time, or whenever a quick pass isn't turning anything up on a statement you suspect is hiding something.
- `references/evidence.md` — the cost-of-defect data and real-world consequences of unclarified requirements, for justifying review time to a stakeholder who thinks this is pedantry.
