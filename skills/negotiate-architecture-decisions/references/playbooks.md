# Counterparty playbooks

Read when you know who you are negotiating with. Three counterparties, three different approaches.

## Contents
- [Business stakeholders](#business-stakeholders)
- [The availability conversion table](#the-availability-conversion-table)
- [Other architects](#other-architects)
- [Developers](#developers)

## Business stakeholders

### The situation

A senior sponsor insists the new system must support five nines of availability. Based on the time between global markets when no trading occurs — two hours — three nines would meet the requirement comfortably. The sponsor does not like being wrong and does not respond well to being corrected, especially if they perceive it as condescending. They are not technically knowledgeable but think they are, and so tend to get involved in the operational aspects of projects.

Two failure modes to avoid simultaneously: being too egotistical and forceful in your analysis, and missing something that would prove you wrong during the negotiation.

### The sequence

**1. Read the buzzwords before you go in.** Corporate buzzwords are generally meaningless as literal statements and provide valuable information as signals. Ask when a feature is needed and hear *"I needed it yesterday"* — you cannot literally provide that, and you have just learned time to market is what this person cares about. *"Lightning fast"* means performance is a big concern. *"Zero downtime"*, rather than being literal, means availability is critical. Read between the lines of exaggerated statements to find the real concern.

**2. Gather as much information as possible before entering.** In this case: what five nines actually means in downtime, what three nines means, and what the domain's idle windows are. It is likely the sponsor has never converted the figure.

**3. Validate the concern.** *"I understand that availability is very important for this system."* Then steer toward reasonable hours and minutes of unplanned downtime.

**4. Convert to units.** Three nines comes to an average of 86 seconds of unplanned downtime per day — a plainly reasonable number given the context of this system. Stating it that way is frequently enough on its own.

**5. If that does not settle it, divide and conquer.** Does the *entire* system need five nines? Qualify the requirement, narrowing it to the specific areas that genuinely need it. This reduces the scope of the difficult and costly requirement, and the scope of the negotiation with it.

**6. Only when all else fails, state things in terms of qualified cost and time.** Money and time are certainly key factors in any negotiation — and too many negotiations start on the wrong foot with opening statements like *"that's going to cost a lot of money"* or *"we don't have time for that."* Try the other justifications and rationalizations first. Once you reach agreement with the stakeholder, cost and time can be considered.

### Which justification to reach for

Four business justifications carry weight: **cost, time to market, user satisfaction, strategic positioning.** Consider what is important to *these* stakeholders. Justifying a decision on cost savings alone may be the wrong call if the stakeholders are more concerned with time to market — the argument can be entirely correct and still fail.

## The availability conversion table

| Uptime | Downtime per year | Downtime per day |
|---|---|---|
| 90.0% (one nine) | 36 days 12 hrs | 2.4 hrs |
| 99.0% (two nines) | 87 hrs 46 min | 14 min |
| 99.9% (three nines) | 8 hrs 46 min | 86 sec |
| 99.99% (four nines) | 52 min 33 sec | 7 sec |
| 99.999% (five nines) | 5 min 35 sec | 1 sec |
| 99.9999% (six nines) | 31.5 sec | 86 ms |

Five nines is ambitious, costly, and frequently unnecessary. Stating goals in hours and minutes — or seconds — is a much better way to have the conversation than sticking with the nines vernacular, because it brings actual metrics and quantified numbers into the discussion.

Get this table right. A wrong downtime figure loses the negotiation it was meant to win, and hands the other party a reason to distrust everything else you said.

## Other architects

### The situation

You are the senior of two architects. You believe asynchronous messaging is right for communication between a group of services, to increase performance and scalability. The other architect strongly disagrees, insisting a synchronous protocol would be better because it is always faster and scales just as well. They cite their research, which consists of a web search and the output of a prompt to a generative AI tool. This is not the first heated debate, nor will it be the last.

### What not to do

As the senior architect you could tell them their opinion does not matter and ignore it. This intensifies the animosity, and an unhealthy, non-collaborative relationship between a project's two architects almost certainly has a negative impact on the development team.

### Demonstration defeats discussion

Rather than arguing the general question, demonstrate why one option is better **in this specific environment**. Because every environment is different, a search result rarely yields the correct answer — which is precisely the weakness in their evidence and the strength in yours. Compare the two options in a production-like environment and show them the results, and you may avoid the argument entirely.

### De-escalation

Avoid being overly argumentative or letting things get too personal. Once things get heated or personal, the best thing to do is stop the negotiation and re-engage later, when both parties have calmed down.

Architects argue from time to time. Calm leadership, combined with clear and concise reasoning, will almost always win a negotiation — and the other person will usually back down.

## Developers

Effective architects gain a team's respect by working together, and when they then request something it is far less likely to spark an argument or resentment. Where teams feel disconnected from the architecture or the architect, they feel left out of decisions — the ivory-tower pattern, where an architect dictates from on high without regard for the team's opinions or concerns, which leads to lost respect and eventually to team dynamics breaking down entirely.

### Always provide a justification, and put it first

People stop listening as soon as they hear something they disagree with. Stating the reason **before** the demand ensures the justification is heard at all.

Compare:

> **Architect:** "You must go through the Business layer to make that call."
> **Developer:** "I disagree. It's much faster just to call the database directly."

Against:

> **Architect:** "Since change control is most important to us, we have formed a closed-layered architecture. This means all calls to the database need to come from the Business layer."
> **Developer:** "OK, I get it — but in that case, how am I going to deal with these performance issues for simple queries?"

Two changes produced that. The justification came first. And *"this means"* replaced *"you must"*, turning the demand into a statement of fact rather than a command — *"you must"* is not only a poor opening for a negotiation, it is demeaning.

Look at what the developer does in the second version: instead of disagreeing with the layering restriction, they ask a question about improving performance for simple calls. The two can now have a collaborative conversation about making simple queries faster while preserving the closed layers.

### Turn commands into questions

Communicating is not collaborating.

> **Developer:** "So how are we going to solve this performance problem?"
> **Architect:** "What you need to do is use a cache. That would fix the problem."
> **Developer:** "Don't tell me what to do."
> **Architect:** "What I'm telling you is that it would fix the problem."

*"What you need to do is"* shuts down collaboration. Revised:

> **Developer:** "So how are we going to solve this performance problem?"
> **Architect:** "Have you considered using a cache? That might fix the problem."
> **Developer:** "Hmmm, no, we didn't think about that. What are your thoughts?"
> **Architect:** "Well, if we put a cache here…"

*"Have you considered"* turns the command into a question and places control back in the developer's hands. How you use language is vitally important to building a collaborative environment.

The same principle in reverse: in a meeting to solve a production issue, a developer makes a suggestion and the architect responds *"well, that's a dumb idea."* Not only will that developer not make any more suggestions — none of the other developers dare say anything either. One dismissal shuts down collaboration across the entire team.

Leading collaboration is also about facilitating it among the team. Observe team dynamics; where a member uses demanding or condescending language, take them aside and coach them on collaborative language. This creates better dynamics and helps team members respect one another.

### Have them arrive at the solution themselves

You are choosing between two frameworks. Framework Y does not satisfy the security requirements, so you choose Framework X. A developer strongly disagrees and insists Y is better.

Rather than arguing, tell them that if they can show you how Y addresses the security concerns, the team will use Y.

**Option 1:** they try to demonstrate it and fail. In failing they understand firsthand why the team cannot use it. Because they arrived at the conclusion themselves, you automatically get their buy-in for X — you have essentially made it their decision. This is a win.

**Option 2:** they find a way to address the security requirements with Y and demonstrate it. Also a win: you missed something in your assessment, you now have a better solution, and the developer still feels involved in the decision.

### Turn a request into a favor

Human beings dislike being told what to do and want to help others.

> **Architect:** "I'm going to need you to split the payment service into five different services, with each service containing the functionality for each type of payment we accept, such as store credit, credit card, PayPal, gift card, and reward points. That will provide better fault tolerance and scalability in the website. It shouldn't take too long."
> **Developer:** "Sorry, I'm way too busy this iteration for that. I really can't do it."
> **Architect:** "Listen, this is important and it needs to be done this iteration."
> **Developer:** "Sorry, I can't. Maybe one of the other developers can do it. I'm just too busy."

The architect justified the request — better fault tolerance and scalability — and it still failed. They were telling someone to do something they were simply too busy to do, and the demand did not even include the person's name.

> **Architect:** "Hi, Sridhar. Listen, I'm in a real bind. I really need to have the payment service split into separate services for each payment type to get better fault tolerance and scalability, and I waited too long to do it. Is there any way you can squeeze this into this iteration? It would really help me out."
> **Developer** *(pausing)*: "I'm really busy this iteration, but I guess I'll see what I can do."
> **Architect:** "Thanks, Sridhar, I really appreciate the help. I owe you one."
> **Developer:** "No worries. I'll see that it gets done this iteration."

Two things changed. Using the person's name makes the conversation personal and familiar rather than an impersonal professional demand. And the architect admits to being in a real bind and says it would really help them out — playing off the basic human urge to help others, which has a better probability of success than the first conversation.

This does not always work. Try it the next time you face this sort of situation.

### Ask for a business justification rather than refusing

Where a developer pushes a technology you believe is wrong, offering to support it *conditional on a business justification* frequently works better than refusal.

A developer on a complex project became obsessed with introducing a different programming language and wanted to use it on the project. Their desire became so disruptive that two key team members declared their intention to leave for other, less toxic environments. The lead architect convinced them to hold off, then told the enthusiast he would support using the language if the enthusiast provided a business justification for the costs of the training and rewriting involved. The enthusiast was ecstatic and said they would get right on it, leaving the meeting yelling *"Thank you — you're the best!"*

The next day they came in completely transformed and asked to speak with the architect, beginning by immediately and humbly saying *"thank you."* They had come up with all the technical reasons in the world, and none of those technical advantages had any business value in terms of cost, budget and timeline. They had realized two things: the increase in cost, budget and timeline would provide no benefit whatsoever, and they had been disrupting the team. Before long they became one of its best and most helpful members.

Being asked to provide a business justification for something they wanted increased their awareness of the business's needs, making them a better software developer and making the team stronger and healthier. The two key developers who had been planning on leaving stayed.

### Names

Using a person's name and proper pronouns during conversations or negotiations helps build respect and healthy relationships. People like hearing their own names, and it creates a sense of familiarity.

Practise remembering names by using them frequently. If a name is hard for you to pronounce, research the correct pronunciation and practise it until it is right. When someone tells you their name, repeat it back and ask if you are pronouncing it correctly — and if not, repeat the process until you get it right.
