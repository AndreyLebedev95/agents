# Checklists

Read when introducing, pruning, or trying to get compliance with checklists.

## Why they work

Airline pilots use checklists on every flight — takeoff, landing, and thousands of other situations, common and edge-case. Even the most experienced veterans use them, because one missed setting can be the difference between a safe flight and a disaster.

The medical evidence is starker. Surgical checklists introduced to address high staph infection rates drove infection rates in the hospitals using them to near zero, while rates in control hospitals not using them continued to rise.

Neither profession uses them because practitioners are forgetful or do not know their jobs. They use them because **when professionals do a highly detailed job over and over, it becomes easy for details to slip by them**, and a succinct list is an effective reminder.

Software developers are mostly not handling life-and-death matters, which means the point is not to checklist everything. The skill is knowing when to leverage them and when not to.

## The qualifying test

**Not a checklist candidate** if:

- The process has a **procedural flow of dependent tasks**, where one step cannot happen until another completes. A sequence for creating a new database table — where the table cannot be verified before the form has been submitted — is a *procedure*, and should be written as one.
- The process is **simple, familiar, and executed frequently without error.**

**Good checklist candidate** if:

- The process has **no set procedural order** and no dependent tasks.
- People **frequently skip steps or make errors** in it.

## Three that earn their place

### Developer code-completion

Useful particularly when a developer states they are "done", and it is how a team arrives at a shared definition of done: if everything in the checklist is complete, the developer can say the code is actually finished.

Contents:

- Coding and formatting standards not included in automated tools
- Frequently overlooked items — absorbed exceptions being the classic
- Project-specific standards
- Special team instructions or procedures

Include the obvious. *"Run code cleanup and code formatting"* looks too trivial to list, and developers in a hurry forget it constantly. The same phenomenon appears in surgical checklists: the obvious tasks are the ones most often missed.

Review it regularly for items that can be automated or written as plug-ins for a code validator. Some project-specific items — *"verify that only public methods are calling setFailure()"* — are straightforward to automate with a code-crawling tool. Others — *"include the service-entry-point annotation on the service API class"* — may not be. Automating what can be automated shortens the list and improves its signal-to-noise ratio.

### Unit and functional testing

Usually the longest of the three, because it encompasses all the types of test that can be run. Its purpose is to make testing complete enough that when the developer finishes the checklist, the code is essentially production-ready.

Contents cover the unusual and edge cases developers tend to forget:

- Special characters in text and numeric fields
- Minimum and maximum value ranges
- Unusual and extreme test cases
- Missing fields

As with the code-completion list, anything that can be written as an automated test, or already exists in the automated suite, should be removed from the checklist and automated.

Two extra benefits. Developers frequently do not know where to start writing unit tests or how many to write, and this gives them the general and specific scenarios to cover. And where testing and development are performed by separate teams, it bridges the gap: the more complete the development team's testing, the more the testing team is freed to focus on business scenarios the checklist does not cover.

### Software release

Releasing to production is one of the most error-prone points in the lifecycle, which makes it an excellent checklist candidate. It helps avoid failed builds and deployments and significantly reduces release risk.

The most volatile of the three, because it changes every time a deployment fails or has problems.

Contents:

- Configuration changes in servers or external configuration servers
- Third-party libraries added to the project
- Database updates and corresponding migration scripts

## The feedback loop

This is what makes checklists improve rather than ossify, and it is the part most teams skip.

- Whenever someone in testing finds a code issue based on a particular test case, **add that test case to the testing checklist.**
- Whenever a build or deployment fails, **analyze the root cause and add a corresponding entry to the release checklist.** The item is then verified during the next build or deployment, preventing the problem from happening again.

A checklist maintained this way encodes the team's actual failure history rather than someone's idea of good practice.

## Keeping them usable

**Do not go overboard.** Architects often start making everything a checklist once they discover checklists work. This invokes diminishing returns: the more checklists that exist, the less likely developers are to use any of them.

**Keep each one as small as possible** while still capturing the necessary steps. Developers will not follow overly long checklists.

**Automate and delete.** If any listed task can be automated, automate it and remove it from the list.

**State the obvious anyway.** The obvious stuff is what usually gets missed.

## Getting them actually used

The hardest part of introducing checklists is getting developers to use them. It is common for some to run out of time and simply check off all the items without performing the tasks.

**First, ownership.** Talk with the team about the difference checklists make and make sure each member understands the reasoning behind each one. Consider having them decide collaboratively what should and should not be on a checklist — creating a sense of ownership does most of the work.

**Then, visible verification.** People who know they are being observed or monitored change their behavior, generally toward doing the right thing. The effect does not require actual monitoring so much as the perception of it — which is why employers mount non-functioning cameras in visible areas and install website monitoring software whose reports are rarely read.

Applied here: let the team know that because checklists are critical to the team's productivity, all checklists will be verified to make sure the task was actually performed. In reality, **occasional spot-checks are all that is needed.** Developers will be much less likely to skip items or falsely mark them completed.

Use this second lever only after the first. Verification without understanding produces compliance theatre; understanding plus light verification produces the behavior you actually want.
