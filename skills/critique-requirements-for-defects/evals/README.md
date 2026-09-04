# Evaluating this skill

This skill is judgment-shaped, not mechanically checkable: whether a phrase is genuinely ambiguous, whether a fix is concrete enough, and how findings should be prioritized all require reading comprehension and domain judgment that a fixed pass/fail assertion can't substitute for. Don't manufacture quantitative assertions for it — iterate qualitatively instead.

## How to iterate

1. Build (or reuse) a fixture: a short requirements-style document with a handful of *known, planted* defects — at minimum one comparative/relative word with no reference point, one solution stated in place of an outcome, one requirement with no acceptance criteria at all, one direct contradiction between two items, and one whole-dimension gap (nothing addresses access control, retention, error handling, etc.).
2. Run the skill against it fresh (a subagent with no other context works well, so it can't lean on anything but the skill's own instructions).
3. Check **recall**: did it find the planted defects, and file each under the category that actually fits (not force-fit into the nearest one)?
4. Check **precision**: did it avoid flagging clean statements, and avoid duplicate findings for the same underlying defect?
5. Read the output for whether every finding names the specific technique that produced it — a finding with no technique behind it is exactly the failure mode the skill exists to prevent in the reviewer, and it's worth catching in the skill's own output too.

## Fixtures

- `fixtures/order-export-requirements.md` — a 7-item requirements list with a comparative word ("fast"), a solution-in-disguise ("the export button shall be added..."), an untestable "reasonable effort" clause, an undefined-term reference ("the accounting system"), an ambiguous scope term ("all orders placed by users"), a missing acceptance criterion (an undated "monthly close" deadline), a direct contradiction between two items about how refunds affect the exported total, and a whole-dimension gap (nothing addresses access control, export failure handling, or file retention). Used during the skill's initial build to validate the defect-category taxonomy across two rounds of testing — see the pipeline's `report.md` for what each round found and how the skill was revised in response.
