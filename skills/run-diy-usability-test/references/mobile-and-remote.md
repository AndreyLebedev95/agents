# Mobile and remote testing

Read when testing on a phone or tablet, or with remote participants.

> **Dated material warning.** Written this when robust mobile screen recording and screen sharing didn't
> exist, because mobile operating systems prohibited background processes and the devices lacked the
> horsepower. He expected that to change, and it has. **Check what current tooling offers before building a
> physical rig.** The reasoning below — why a camera beats mirroring, why not to use a face camera — still
> holds regardless of tooling.

## The process doesn't change

Testing on mobile devices is, for the most part, exactly the same as testing anything else. You're still
making up tasks and watching people try to do them. You still prompt them to say what they're thinking. You
still keep quiet most of the time and save probing questions for the end. You still get as many stakeholders
as possible to come and observe in person.

**Almost everything that differs is logistics.** Don't let rig complexity turn a mobile round into a
different, heavier kind of exercise — that's how testing stops happening.

## The four logistics questions

Settle these before the session, not during it:

1. Do participants need to use **their own devices**?
2. Do they need to **hold the device naturally**, or can it sit on a table or a stand?
3. What do **observers** need to see — just the screen, or the screen *and* the participant's fingers so
   they can see the gestures? And how will you display it in the observation room?
4. How will you create a **recording**?

## recommendations

### Point a camera at the screen rather than mirroring

Mirroring (via AirPlay-style software, or a video-out cable) shows what's on the screen — and nothing else.
That's the problem: **you can't see the gestures and taps the participant is making.** Watching a test
without seeing the fingers is like watching a player piano — it moves fast and is hard to follow. Seeing the
hand and the screen together is far more legible and far more engaging for observers.

Some mirroring software draws dots and streaks where taps land. It isn't the same thing.

So if you want fingers, there's a camera involved.

### Attach the camera to the device

In many setups the device sits fixed on a desk, or the participant may hold it but is told to keep it inside
an area marked with tape. The **only** reason for restricting movement is to keep the device in a fixed
camera's view.

Attach the camera to the device instead and the participant can move it freely while the screen stays in
view and in focus — which also gives observers a stable image even when the participant is waving the phone
around.

built one from a webcam and a book-light clamp with a gooseneck: about $30 in parts, an hour to make,
weighing almost nothing, capturing audio through its built-in microphone. It answers the standard objections
to mounted-camera rigs — it's not heavy or awkward, it's small enough and positioned out of the
participant's line of sight so it isn't distracting, and it clamps with a padded grip rather than the Velcro
or double-sided tape that sleds use, so nobody has to attach anything sticky to their phone. Its one
limitation: it's tethered by a USB extension cable to a laptop.

### Don't bother with a camera pointed at the participant

Some observers like seeing faces. Treat it as it a distraction: he'd much rather observers focus on
what's happening on the screen, and they can almost always tell what someone is feeling from tone of voice
anyway. A second camera makes the configuration substantially more complicated for little return.

His caveat, worth keeping: if your boss insists on seeing faces, show faces. This is not a hill to lose the
round over.

## Remote testing

Instead of coming to your office, participants do the session from home or their own office over screen
sharing. All they need is high-speed Internet and a microphone.

Two gains, the second larger than the first:

- Eliminating travel makes it much easier to recruit busy people.
- It expands the recruiting pool from *people who live near your office* to *almost anyone* — which matters
  a great deal if your users aren't distributed like your office is.

Everything else about the session is unchanged.

## Unmoderated remote testing

Services exist that provide people who record themselves doing a usability test. You send in your tasks and
a link to your site, prototype, or app, and within about an hour on average you can watch a video of someone
doing your tasks while thinking aloud.

The trade: you don't get to interact with the participant in real time — no probing, no follow-up on
something surprising. What you get is very low cost and almost no effort, especially on recruiting. All you
have to do is watch the video.

Good for: a quick read on a specific flow, testing when you have no recruiting capacity at all, and getting
a first round to happen when the alternative is no round.

Note that discloses being compensated by the service he names in the book — worth knowing when reading
his endorsement of it, though his description of the method's tradeoffs is straightforward.
