# The goodwill audit

Read when the complaint is about trust or tone rather than confusion, or when the screen asks the user for
data, money, or a signup.

## The reservoir

Most usability work is about **clarity** — can they understand what they're looking at and how to use it?
There's a second question underneath it: **does this behave like a mensch?** Doing the right thing by the
person using it.

Imagine every visitor arriving with a reservoir of goodwill. Each problem lowers the level. Exhausting it
risks more than departure — reduced willingness to come back, a worse opinion of the organization, public
complaint.

Four properties govern it, and they change how you weight findings:

- **It's idiosyncratic.** Some people arrive with a large reserve, some small; some are naturally suspicious
  or ornery, others patient and trusting. You cannot count on much.
- **It's situational.** Hurry, or a bad experience on the previous site, arrives with them. A generous
  person can walk in nearly empty.
- **You can refill it.** Acts that show you're looking out for them replenish it, even after mistakes.
- **A single mistake can empty it.** Opening a registration form with dozens of fields can take some people
  to zero on the spot. So don't average findings — look for the one cliff.

The diagnostic uses is a session trace: walk the task and mark each moment the level drops or rises.
A worked example: an airline site on the morning of a possible strike, with nothing about the strike
anywhere on the site and the Home page still promoting ticket sales. Whatever the internal reason — no
process for updating the Home page, legal caution, or nobody thinking of it — the effect on him was the
same.

## What depletes it

Users conclude you don't have their interests at heart when you:

**Hide information they want.** Most commonly support phone numbers, shipping rates, and prices.
- Hiding the support number to suppress calls backfires twice: it depletes goodwill, and they're angrier
  when they finally find it. Counter-intuitively, a number in plain sight — even on every page — keeps
  people looking for the answer on the site *longer*, because knowing they *can* call is enough. That
  raises the chance they solve it themselves.
- Hiding price to get people invested before the sticker shock reads as a phone-sales tactic. example
  is airport Wi-Fi sign-up: three pages of "Wireless Access" and "Click here to connect" before anything
  hints at cost.

**Punish them for not doing things your way.** Nobody should have to think about data formatting — dashes in
an ID number, spaces in a credit card number, parentheses in a phone number. Rejecting spaces in card
numbers is perverse, since the spaces are what make the number easy to type correctly. Parse it yourself.
Don't make people jump through hoops because you'd rather not write a little code.

**Ask for information you don't need.** People are skeptical of requests for personal data and find it
annoying when a form asks for more than the task requires.

**Shuck and jive them.** Faux sincerity is detected instantly. Think about what goes through your head at
"your call is important to us".

**Put sizzle in the way.** Wading through feel-good marketing photography on a task path makes it clear you
don't understand — or care — that they're in a hurry.

**Look amateurish.** Sloppy, disorganized, or unprofessional loses goodwill.

One important calibration on that last point: people *love* commenting on appearance, especially colour, but
almost nobody leaves because a site doesn't look great. The rule for tests is to ignore colour comments
entirely unless three of four participants reach for a word like "puke" — at which point it's worth
rethinking.

## What rebuilds it

Mostly the flip side. Any of these can refill a reservoir you've already drained:

**Know the top three things people come to do, and make them obvious and easy.** Identifying them is rarely
the problem — even people who agree on nothing else about their organization's site give the same answer.
The problem is that making them easy never becomes the priority it should be. If most people come to apply
for a mortgage, nothing should get in the way of applying for a mortgage.

**Tell them what you'd rather not.** Shipping costs, hotel parking fees, service outages. You lose a few
points on the bad news and usually gain more for candor and for making it easy to compensate.

**Save steps.** Don't hand over a tracking number — put a link in the receipt that opens the carrier's site
with the number already submitted.

**Put visible effort in.** For example, a printer maker's support site where obvious work went into
generating the right information, keeping it accurate, presenting it clearly, and organizing it findably —
and it kept him buying their printers.

**Answer the questions they actually have.** FAQs are enormously valuable when they're genuine — this week's
top five from Customer Service and Support, kept current, at the top of the Support page, and candid.
Beware the counterfeit: Questions We Wish People Would Ask. A marketing pitch shaped like an FAQ depletes
goodwill instead of building it.

**Provide creature comforts.** Printer-friendly pages cost little in CSS. Drop the ads — a banner is even
more useless on paper — but keep the illustrations, photos, and figures.

**Make error recovery graceful and obvious.** Enough testing spares people many errors; where the potential
is unavoidable, always provide an obvious way back.

**When in doubt, apologize.** Sometimes you genuinely can't do what they want. At minimum, let them know
that you know you're inconveniencing them.

## A note on deliberate depletion

Some of the depleting behaviours can be legitimate business decisions. Uninvited pop-ups annoy people; if
the numbers show they raise revenue ten percent and the organization judges that worth the annoyance, that's
a decision it's entitled to make. The requirement is that it be made **knowingly rather than inadvertently**.
A review's job in that case is to name the cost accurately, not to forbid the choice.
