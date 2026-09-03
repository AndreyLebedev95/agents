# Stating blind spots

Read before publishing a result to anyone outside the team.

## Why this section is not optional

A clean result is read as evidence that things are clean. It is not — it is evidence that the checks that ran found nothing in the area they cover. Those are very different claims, and the gap between them is where a stakeholder builds false confidence.

Publishing the limits alongside the findings costs a paragraph and is the difference between a report that is trusted appropriately and one that is trusted wrongly. The second kind eventually gets discovered, and takes the whole mechanism down with it.

## The three that always apply

### Uncovered mechanisms

**What:** Links created by a route the extraction does not walk are absent from the result, not clean.

**Wording that does not overclaim:**

> This scan covers requirement markers in source annotations, test tags and commit messages. Links established by any other means — configuration, generated code, runtime registration, external tooling — are not visible to it and their absence here is not evidence of their absence in the system.

**Keep it specific.** List the mechanisms you *do* cover. A vague admission that "some things may be missed" tells the reader nothing they can act on; a list of what is covered lets them judge whether their concern is inside it.

### Shared-state coupling

**What:** A relationship neither side declares — another system reading or writing your database directly, a shared file, an agreed message format nobody owns — is effectively undetectable from the artifacts.

**Wording:**

> Integration through shared state cannot be detected from the artifacts. If another system reads or writes this data directly, nothing here will show it. These surface only in conversation, and finding them is a matter of asking rather than scanning.

**Do not try to soften this.** You may reasonably believe the database is a private detail of your system; if another team queries it directly, you will not find that out from a scan. It is worth naming precisely because it is the failure people are most surprised by.

### Declared versus exercised

**What:** The check verifies links present in the artifacts. It does not verify that those links are exercised in production, or that the marked component actually does what the requirement says.

**Wording:**

> This reports links declared in the artifacts, not links exercised in production. A component marked as implementing a requirement is asserted to implement it, not shown to. Where the codebase serves several deployments or product variants, this shows every potential link, not the subset active in any one of them.

The last clause matters more than it looks. A codebase serving a product line will show links that are inert in most instances.

## A fourth, when it applies

### Marker presence is not correctness

Where the check is being read as quality assurance rather than as bookkeeping, say this explicitly:

> This verifies that the chain connects. It does not verify that what it connects is right. A test marked as covering a requirement is asserted to cover it; whether it actually does is a question for review, not for this check.

## Where to put it

At the end of the findings, always present, whether or not anything was found. Especially when nothing was found — that is the moment the section is doing the most work.

Never move it to an appendix, a footnote, or a separate document. A limitation the reader does not encounter is a limitation you did not state.
