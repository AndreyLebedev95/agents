# Ambiguity techniques: full mechanics and worked examples

Read this when a statement resists a quick pass with the summary in SKILL.md, or the first few times you apply either technique, until the pattern is automatic.

## Contents
- [The stress-test, worked in full](#the-stress-test-worked-in-full)
- [Dictionary-sense substitution, worked in full](#dictionary-sense-substitution-worked-in-full)
- [Combining both techniques on one real-world statement](#combining-both-techniques-on-one-real-world-statement)
- [Two supporting checks: recall and independent listing](#two-supporting-checks-recall-and-independent-listing)

## The stress-test, worked in full

Take a short sentence and read it once per word, stressing only that word, then write down what each stress implies was being contrasted or pinned down.

**"Mary had a little lamb."**

| Stress | Implies |
|---|---|
| *Mary* had a little lamb | Someone else did not have one |
| Mary *had* a little lamb | She no longer has it now |
| Mary had *a* little lamb | Exactly one, not several |
| Mary had a *little* lamb | Contrasted with a bigger one |
| Mary had a little *lamb* | Not a dog, cat, goat, or other animal |

That's five readings from single-word stress on a five-word sentence. Stress two words together and the count grows further — "Mary *had a little lamb*" (as opposed to someone else, who still has theirs) is a different claim again. Stress all five at once and you get a reading that implicitly contrasts every single word with an alternative ("as opposed to someone else who has four large turtles"). You can work out the remaining combinations as an exercise; by the time you're done, you may notice the *unstressed* original reading is actually one interpretation among many, not a privileged "plain meaning."

The rhyme is silly on purpose — it's five words everyone already knows, chosen so the mechanism is obvious before you apply it somewhere that matters. A requirement sentence subjected to the same treatment behaves identically: every word was chosen for one reason, but the sentence as written supports several.

**Why this works:** ordinary reading skips past words that don't seem load-bearing. Forcing an emphasis onto each one in turn makes you notice what that word was actually doing — and, just as importantly, what the sentence *doesn't* say once you notice the word could have been emphasized differently.

## Dictionary-sense substitution, worked in full

Once a word is flagged as load-bearing, don't stop at the first meaning that comes to mind — look up its full range of dictionary senses and re-read the sentence under each one.

**Worked example — a single word, many senses.** Take a plain, everyday noun like "point." An unabridged dictionary lists dozens of senses, including at minimum:

- an individual detail or item ("a point in a discussion")
- the essential thing being argued ("the point of a joke")
- purpose or cogency ("what's the point")
- a geometric position (either an abstract location, or a location determined by coordinates)
- a narrowly localized place or locality
- an exact moment in time, or the interval just before something happens ("at the point of death")
- a particular stage of development ("boiling point")
- the sharp or tapering tip of an object
- a projecting piece of land, or a sharp anatomical prominence
- a very small mark, including a punctuation mark or a decimal point
- a unit of measurement — in scoring a game, evaluating a card hand, academic credit, or a typographic unit
- the act of a hunting dog indicating game
- a position in a game (as in lacrosse)

Given a question like "how many points were on the shape shown in the presentation," at least five of these senses produce a *different, defensible answer*: the tips of a star shape (the "obvious" reading), the small marks or dots visible inside it, the geometric vertices including interior intersections (a different count than the tips alone), the number of distinct purposes the shape was shown for, or the number of exact moments during the presentation that it was referenced. None of these were consciously chosen between when the question was first written — the author had one sense in mind and assumed everyone else would land on the same one.

**How to run it:**
1. Identify the load-bearing word (usually whatever the stress-test flagged).
2. List every sense a dictionary gives it, not just the first one.
3. Re-read the full sentence substituting each sense in turn.
4. Note which alternate readings are merely possible versus genuinely plausible given context — both are worth recording, but plausible ones are the real finding.

**Combining across words.** The technique gets stronger when you do it for more than one word in the same sentence and mix the senses together. Take "its fleece was white as snow" — an ordinary description on its face. But "fleece" also has a verb sense meaning to defraud or strip of money, and "snow," besides the weather, is slang for to deceive or charm glibly. Recombined, the sentence supports reading it as a description of a con: someone deceptive tricked a gullible mark out of his possessions. That reading is absurd for a description of an actual lamb — and that's the point. If a five-word description can be forced into a completely different meaning using nothing but its own dictionary, a real requirement sentence, written faster and reviewed less carefully, can be forced just as far, except the alternate reading might not be absurd at all — it might be the one a later implementer actually picks.

## Combining both techniques on one real-world statement

Given a requirement like *"The system must provide a fast response for typical usage,"* run both techniques before accepting it:

- Stress-test: stressing "fast" implies a contrast with slow, but slow relative to what baseline? Stressing "typical" implies some usage is atypical — which is excluded, and who decides? Stressing "must" implies this is a hard requirement rather than a preference — is it, and what happens if it's missed?
- Dictionary substitution on "fast": could mean low latency per request, high throughput under load, quick to learn (as in "fast onboarding"), or even "securely fixed" (a fast knot) — context makes the last one implausible here, but the first three are all live candidates and imply completely different engineering work.

The finding isn't "this sentence is vague" — it's: no reference point for "fast" (compared to what baseline, under what load), no definition of "typical usage" (what's excluded, and by whom), and at least three plausible engineering interpretations of the metric itself (latency vs. throughput vs. perceived speed). That's three distinct, actionable findings from two techniques applied to one sentence.

## Two supporting checks: recall and independent listing

These require other people to be available; use them when a live review session is possible, in addition to the solo techniques above, not instead of them.

**Recall check.** Take the written document out of view and ask each participant to write down, from memory, what a specific passage said. In practice almost nobody re-reads source documents while working — they work from their memory of what a document said — so a passage that gets reconstructed differently by different people is exactly the passage that will get built differently. Compare the reconstructions; divergence marks the ambiguous parts.

**Independent listing.** Before a formal statement even exists, ask each stakeholder to independently list what they consider the critical events or aspects of the problem, without conferring. Compare and discuss. Then have each stakeholder independently redefine the same events and aspects a second time, again without conferring, and compare again. Persistent divergence after a round of discussion is a real, unresolved ambiguity, not a communication hiccup.
