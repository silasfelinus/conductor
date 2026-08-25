# Cthulhuquarium — Design Brief

date: 2026-08-24
status: draft (scaffolded in-session with Silas; scope confirmation is t-002, non-blocking)
author: Reviewer (Claude), from Silas's pitch on kind_robots Project 2112

---

## What it is

A darkly funny idle aquarium game. You come in out of whatever is happening
outside, and they are so pleased to see you. There is a tank. Things live in it.
You feed them. They grow. Some of them are grateful.

Mechanically it is Insaniquarium's loop — click for coins, buy food, feed fish,
fish drop more coins, buy upgrades, unlock stranger fish — with a cookie-clicker
idle layer so it keeps earning while you are gone, and a Pokémon-style collection
layer so the reason to keep playing is *seeing what else is down there*.

Tonally it is not cute. It is Little Inferno's cheerful complicity, Limbo and
Inside's silhouette dread, Sunless Sea's dry gallows humor about a hostile ocean,
and Tim Burton's spindly-but-endearing character design. The fish are monsters. The
game is fond of them. So are you, eventually.

**The one-line pitch:** *It sits there, in the back of the curiosity shop. Why can't
I find any of these fish on Wikipedia? But this is my aquarium, and it is mine.*
(Lifted from Silas's own 2020 index.html copy — the tone was right six years ago.)

## The setting — you came in out of it

Silas, 2026-08-25, and this is the frame the whole game hangs off:

> *"You are welcomed after stumbling into the aquarium store. Things are* oof *outside,
> but they are welcoming you, and maybe it will be better if you distract yourself.
> After all, everything out is in, or so they tell you..."*

**The opening.** You stumble in. The door closes behind you. It is warm, and green-lit,
and someone is genuinely delighted you came. Nobody asks what it is like out there.
Charlotte offers you something to feed.

**Outside is never shown, named, dated, or explained.** This is a hard rule, not a
tease. There is no establishing shot, no broadcast, no survivor with news, no flashback,
no dropped hint that a clever player assembles into a timeline. *Oof* is the entire
specification and it is enough. The dread is not in what happened; it is in the fact
that a cheerful woman in a clean apron will not mention it, and neither will you.

Anything that explains outside destroys this. If a future task proposes lore, a prologue,
or a "what happened" reveal, the answer is no, and this paragraph is why.

**"Everything out is in, or so they tell you."** Three readings, all true at once, and
none of them ever confirmed:

- *Reassurance.* Everything out there is also in here — catalogued, fed, behind glass.
  Nothing new can arrive. You are safe because the world is already inventoried.
- *Inventory.* The aquarium is what's left. The tanks are not a collection of the world,
  they are the collection *of the world*.
- *Threat.* The things outside are the things inside. You have been feeding them.

**This makes the bestiary the win state for a real reason.** Completing the
Ichthyonomicon was already the goal; now it is an inventory of everything that exists.
The last empty page is not a completionist's itch. It is the question of whether the
list ends.

**Distraction is the mechanic, diegetically.** Charlotte does not ask you to save
anything. She asks whether you would like to feed something. The idle loop *is* the
coping — and that is why FISH DO NOT DIE and progress never degrades. A refuge that took
things away from you would not be a refuge. The no-degradation rule stops being a genre
convention and becomes the promise the building is making.

**It also explains the staff.** Charlotte's dreadful cheerfulness is not a quirk, it is
the coping mechanism wearing an apron. Wilbur's missing fingers and fresh bandages are
what keeping the place running actually costs, and he will not say so, and she will not
either. Neither of them is lying to you. They are doing the same thing you came in to do.

**The door.** There is a door. It stays closed, and it is never opened, because the
door is not the way out and by the end you will understand why.

## The finale — you are also in an aquarium

Silas, 2026-08-25: *"finale moment is the realization that you are also in an
aquarium."*

That is the whole ending, and it closes "everything out is in" on itself. The shop is a
tank. The warm green light is tank light. The one lit place in the world is lit the way
an exhibit is lit. Somebody is on the other side of the glass, and has been the whole
time, and is fond of you.

**IT IS ALREADY FORESHADOWED BY A SHIPPING MECHANIC, which is why it will land.**
Browsable public aquariums (t-014) were in the MVP from day one, described in this very
document as *"you visit someone's aquarium the way you'd look in someone's window."*
Every player has spent the entire game looking into other people's tanks. The finale is
the realisation that the view goes both ways. Do not add hints; the hint has been the
core loop.

Everything else already points at it too, and none of it was designed to:

- **Fish do not die and progress never degrades.** You are being kept, and kept well.
- **The food is alive.** So is yours.
- **The leaderboard** ranks specimens.
- **The Ichthyonomicon** is an append-only record of every species ever held. Somewhere
  there is one with you in it.
- **The idle loop** means the tank is observed while you are away.

**HOW IT LANDS, Silas 2026-08-25:** *"discovered after buying the last and largest
aquarium, when you get to see a giant eye moving around and watching you from a window."*

**The trigger is the tank, not the bestiary.** Every upgrade you have ever bought made
your enclosure bigger. The last and largest one is big enough to see out of. You spend
the whole game paying for a better tank and the reward is finding out it is a tank.
(An earlier draft of this section gated the ending on completing the Ichthyonomicon.
That was wrong and is superseded: the collection is what makes the world feel
inventoried, but the *upgrade path* is what has been quietly building the enclosure, and
the payoff belongs to the thing that set it up.)

**The eye is moving around, and that is the entire craft of it.** It is not staring. It
is not a jump scare. It drifts past the window, pauses the way you pause at a tank you
have already seen today, and goes on with whatever it was doing. It looks at you the way
you have been looking at your fish for hours: fondly, distractedly, in passing. Being
*stared at* is frightening. Being **unremarkable** is worse, and it is the note this
whole game has been playing.

Render it in the same vibrant cartoon register as everything else — glossy, saturated,
almost friendly. A horror-styled eye would let the player file it under "spooky bit". A
cheerful one does not give them anywhere to put it.

**The window, not the door.** The door has stayed closed all game and is never opened;
it was never the way out. The window is not an exit either. It is the viewing pane, and
it has always been on the other side.

**Words are optional and probably unnecessary.** If anything is written, it is one more
field note in the same dry placard register the player has been reading for hours
without once asking whose voice it is — two sentences, faintly concerned, explaining
nothing. But the eye does the work alone. If the text is doing the lifting, cut it.

### The last tank

Silas, 2026-08-25: *"I like there being a final tank and what you get is functionally the
same or minorly larger, but cosmetically it re-evaluates everything."*

**It grants nothing, or nearly nothing.** `slots_cap` +0 or +1. It is the most expensive
thing in the game and it is not an upgrade. Everything it gives you is cosmetic.

This dissolves the design conflict rather than making an exception for it. ECONOMY.md's
rule — coins buy breadth, milestones buy room — **survives completely intact**, because
the final purchase does not buy room. An earlier draft of this section recommended
breaking that rule once at the end; this is better, and it is superseded.

**Three things fall out of it, all good:**

- *It is safe to gate the ending on.* No power spike, so no balance implications, no
  must-buy pressure during play, nothing for t-019 to tune around. Buying it is purely a
  want.
- *"Buying" still implicates you.* Nobody makes you. You buy the biggest tank because you
  wanted the biggest tank, and that is the entire moral position the game has been
  quietly putting you in since the first fish.
- *It is the only cosmetic you purchase.* Backgrounds are milestone rewards; everything
  else coins buy is capability. The one thing you spend a fortune on for looks is the one
  that shows you the window.

**"Cosmetically re-evaluates everything" means re-render what is already there, not add
new content.** Same fish, same set pieces, same room — re-lit, re-framed, seen from a
step further back. That is far cheaper to build than new assets and far stronger, because
the player is not being shown something new; they are being shown *their own tank*, the
one they spent hours arranging, and understanding it differently. Nothing has changed
except what it means. That is the ending in one sentence.

**The risk, stated plainly:** a player can feel cheated by an enormous purchase that does
nothing. The mitigation is entirely in how big the cosmetic payoff is. If the last tank
looks like "a slightly nicer tank", this fails and reads as a bad shop item. It has to be
the moment everything they have been looking at gets re-lit. Charlotte still sells it
without comment — see rule 6 — so the copy cannot do this work. The art has to.

**Rules, and they matter more than the idea:**

1. **Earned, never announced.** The player should get there a beat before the game says
   it. If the text has to spell it out, the foreshadowing failed and the fix is upstream,
   not a longer paragraph.
2. **Once.** No callbacks, no winking afterward, no achievement named after it. A joke
   repeated is a joke explained.
3. **The game continues.** This is the hard one. Afterwards you go back to feeding, and
   nothing has changed, and nothing is taken away — because progress never degrades and
   that rule does not get suspended for a mood. The horror is that it is still nice here.
4. **Still never explained.** This is not a reveal of what happened outside. It is a
   reveal of *where you are*. The "outside is never explained" rule survives the ending
   completely intact; if anything the ending is why it had to.
5. **Gate it on the last and largest aquarium, not the clock and not the bestiary.**
   It belongs to whoever finished paying for the enclosure. That also means the terminal
   tank upgrade must actually exist as a purchasable end of the line rather than an
   open-ended capacity curve — an idle game that never stops selling you a bigger tank
   has no final purchase to hang this on. See t-032's capacity work and ECONOMY.md's
   slots_cap progression.
6. **Do not let it be spoiled by the shop.** Whatever the last tank is called, its name
   and its store copy must not gesture at the ending. Charlotte sells it the way she
   sells everything: cheerfully, and without comment.

**Tasks this touches.** None need to change now; they need to know this is coming.

- **t-039 — the last tank, SETTLED by Silas 2026-08-25.** There was no purchasable tank
  in the design at all, and "buying the last and largest aquarium" looked like it
  contradicted ECONOMY.md's decided rule that *"coins buy breadth, milestones buy room"*.
  Silas dissolved it rather than making an exception: *"I like there being a final tank
  and what you get is functionally the same or minorly larger, but cosmetically it
  re-evaluates everything."* See **The last tank** below.
- **t-014 (public tanks)** — the foreshadowing, already shipped. Nobody optimises the
  window framing out for being flavourless.
- **t-028 (milestones and interstitials)** — the delivery surface for the eye.
- **t-017 (tank decoration and layout)** — whatever renders the tank has to be able to
  render a window in it, once.
- **t-031 (Ichthyonomicon)** — where the optional final placard would live.
- **t-018 (leaderboard)** — ranks specimens. Leave it alone; it is funnier untouched.

## Who it serves

Primarily Silas, as a bucket-list project he has restarted twice and never shipped.
Beyond that: Kind Robots visitors who want a low-commitment thing to leave open in a
tab, and the collection-hunter audience that plays idle games for the bestiary rather
than the numbers. Browsable public tanks make it social without making it competitive —
you visit someone's aquarium the way you'd look in someone's window.

Secondary and real: this project is the **proving ground for autonomous project
scaffolding**. Silas said so explicitly in the pitch — if agents can't generate their
own game assets through Comfy, fixing that is part of this project's scope, not an
excuse to descope. Every asset pipeline gap this surfaces is a finding, not a blocker.

## Creative direction

**Visual — corrected 2026-08-25.** Vibrant saturated cartoon creature illustration.
Thick confident outlines, exaggerated asymmetric anatomy, glossy wet highlights, bold
colour, playful macabre storybook monsters against dark water.

This replaces the silhouette-forward direction this section carried until 2026-08-25.
Silhouettes were chosen on the theory that they would survive Comfy's inconsistency
better than detailed creature art. The first real batch disproved it — Silas, on ten
returned renders: *"they almost all look like real animals, not misshapen horrors from
the deep with a cartoonish playfulness... I want creative, colorful, and vibrant monster
fish and backgrounds."* A dark, low-detail, rim-lit prompt reads to the model as
*underwater photograph*, so restraint in the prompt bought realism, which is the one
thing this bestiary cannot be. Every prompt now carries an explicit negative against
photorealism. Full rules in the bible's `fish/SCHEMA.md`.

The warmth matters more than it looks. The interior is the only lit place in the world
the game will show you, and it should feel like somewhere you would want to stay.

**Written.** Every fish has a one-line field note written like a museum placard by
someone who is not telling you everything. Dry, short, faintly concerned. No jokes with
punchlines; the humor is in the understatement.

**Anti-goals.** Not gross-out horror. Not grimdark. Not a bullet-sponge numbers game
with reskinned assets. If a fish is not fun to look at, it does not ship.

## The bestiary is its own model — corrected 2026-08-25

**This section previously said fish were `Character` records. That was wrong, and it did
real damage — see the postmortem at the end.**

Silas: *"why do our characters have size? These monsters are not meant to be added as
characters. characters are our website's chattable personalities and npcs for story based
games. the monsters are something new."*

`Character` is for **people you can talk to** — chattable personalities and story-game
NPCs. Charlotte Fishmonger and Wilbur Stint are Characters, correctly, because they speak.
The things in the tank are not. They have no dialogue, no personality, no chat surface;
they have a field note, a size, a payout rate and a swim behavior. Putting them in
`Character` meant every aquarium concern leaked into a model the rest of the site relies
on for something else entirely.

**Monsters get their own model.** Proposed name `Creature` — broad enough that not
everything in it has to be monstrous (the Parlour Rustfish isn't) and reusable by Ruler is
Hooked, which is the point. `Monster` is the obvious alternative; Silas overrides in a
word. It carries what the bible actually needs: slug, name, species, class, field note,
quirks, rarity, the six rarity stats, tier, size, yield, interval, unlock cost, behavior,
hue, games, art prompt, evolution links.

**Sharing with Ruler is Hooked survives intact.** That was the real argument for reusing
`Character`, and it does not depend on `Character` at all — it depends on there being ONE
shared table with a `games` list. A `Creature` row tagged `[cthulhuquarium, ruler-hooked]`
is read by both games exactly as planned. Ruler is Hooked keeps using `Character` for its
actual characters — the ruler, the warlock, the druids — which is what its brief meant.

**The canon stays in this repo either way.** `fish/*.yaml` remains the source of truth and
the seed script targets `Creature` instead of `Character`. Nothing about the YAML shape
changes except that its fields no longer have to contort to fit someone else's columns —
which was always a constraint on the bible rather than a feature of it.

### Postmortem: what the wrong call cost

The original reasoning was that `Character` already had `species`, `class`, `backstory`,
`quirks`, `slug`, `packId` and six `Rarity` stats, so a bestiary was "a schema already".
That is true and it is not a good enough reason. Reusing a model because its *columns* fit
ignores what the model *means*, and meaning is what every other consumer of it depends on.

The concrete cost: fish needed a capacity weight, so `Character.size` was added. That
column shipped in kind_robots#2075, its migration was never applied to production, and
every `prisma.character.findUnique()` on the live site began returning HTTP 500 —
including the ArtJob completion path, which broke character-linked art generation
entirely. A field that should never have existed took down an unrelated feature.

The rule worth keeping: **shared models are shared because of what they mean, not because
their columns happen to line up.** If the new thing does not belong to the same concept,
it gets its own table, and the sharing you actually wanted is arranged deliberately rather
than inherited by accident.

## MVP scope — "the first completed version"

Silas's bar, verbatim: *"a fully working webpage where users can load and interact with
their aquariums."* Concretely, v1 ships when a logged-in user can:

1. Open `/play/aquarium` and see their tank, with their fish swimming in it.
2. Click drifting collectibles for coins.
3. Spend coins on food; drop food; fish eat it and stay alive.
4. Spend coins on upgrades (better food, faster drops, more tank slots).
5. Buy or unlock a new fish species and watch it appear.
6. Close the tab, come back later, and have earned offline income — capped, so idling
   is rewarded but active play is still faster.
7. Browse other users' public tanks read-only.
8. Have all of it persist server-side across devices.

Plus **20 distinct fish** with real art, real field notes, and rarity tiers — that
number is from Silas's stated goal and it is the difference between a demo and a game.

## Explicitly out of MVP (planned, not now)

- **Decoration/tank editing** — in the pitch, deferred to POLISH. Placing objects needs
  a UI that the core loop doesn't, and the loop has to be fun first.
- **Leaderboard** — in the pitch, deferred. It needs a scoring metric worth ranking, and
  we won't know what that is until the economy is tuned.
- **Rare random events** — designed in SHAPE, built in POLISH. They're the retention
  hook, but they're only interesting once the baseline is boring.
- **iOS / Android** — Silas's tier 2, and a real human gate (developer accounts,
  signing certs, store submission). Agents can prepare a Capacitor/PWA wrapper and
  document the steps; agents do not create accounts or submit builds.
- **Steam** — Silas's "final final", explicitly human-gated. Nothing in this roadmap
  touches it.

## Guardrails

- No store submissions, no developer-account creation, no payments, no external
  publishing. Those are hard gates regardless of what a task note says.
- Generated art follows the standing 2026-07-06 rule: agents may generate and commit
  fish/background art without per-image approval, preserving prompt/seed/model metadata.
  That permission covers generation, not publishing.
- Fish are `isMature: false` and `isPublic: true` by default. Monstrous, not explicit.
  Anything that would need a maturity flag doesn't belong in the bestiary.
- Public tank browsing shows a display name and a tank, never an email or a user id.
- The economy must be tunable from data, not code, so balance passes don't need a deploy.
- **Outside is never shown, named, dated, or explained.** No prologue, no broadcast, no
  survivor with news, no flashback, no assemblable timeline. This is a hard creative
  gate in the same class as the ones above: a task that proposes lore gets refused, not
  negotiated. It is the single easiest thing to erode, because every individual addition
  will look like harmless texture and each one costs a little of the ending.
- **Nobody says the finale out loud before the finale.** Charlotte and Wilbur do not
  hint, do not wink, and are not in on it. Neither is the UI. The foreshadowing is the
  core loop — you have been looking into other people's tanks all game — and that is
  enough. A line of dialogue that gestures at the glass is worth less than the mechanic
  and costs the whole payoff.
- **`t-014`'s window framing is load-bearing, not flavour.** "You visit someone's
  aquarium the way you'd look in someone's window" is the finale's entire setup. If a
  later pass wants to make public tanks feel more like a leaderboard and less like
  looking in a window, that trade is a creative decision about the ending, not a UX
  tweak, and it comes back here first.

## Decided (Silas, 2026-08-24, in session)

All four open questions are answered. These are decisions, not assumptions — build to
them, and reopen only with Silas.

**1. Fish do not die. Progress never degrades.** Verbatim: *"fish do not die. it's an
incremental clicker game, progress should never degrade, other than spending currency
for upgrades."* Nothing you have earned is ever taken away — coins, unlocks, upgrades,
and collected species all persist unconditionally. There is no starvation loss, no
decay of holdings, and no punishment for closing the tab.

Hunger survives as a **rate gate only**: a hungry occupant stops paying out and resumes
the instant it is fed. That is the one sanctioned exception and it is not a loss —
income pauses, holdings don't shrink. Anything that would reduce an accumulated total
is out of bounds, which specifically rules out a prestige reset, decay timers, and
losing a species you have already unlocked.

**2. The food is alive.** Silas, same session: *"fish food should be alive. i guess in
that sense, something will die, but that's just because our fish food should be
wriggling."* Feeding means buying something that squirms and dropping it in. This is the
tonal keystone of the whole economy — the game never takes anything from *you*, and the
cost it does have is one you pay to something else, cheerfully, by the handful. Pellets
are wrong; it wriggles on the way down and stops when eaten. Do not soften this into
generic flakes, and do not escalate it into gore.

**3. Endless, but the bestiary completes.** No ending screen and no prestige reset. The
"win" is filling the collection — the last species is the credits roll. This makes the
bestiary the actual progression spine rather than a side board, so the leaderboard
metric is species collected, not coins (coins only rank whoever left a tab open longest).

**4. The ceiling is clearly-not-a-fish.** The bestiary may escalate past "recognizably a
fish, but wrong" into things that only resemble fish — too many joints, mostly eye,
something wearing a fish. Two constraints hold: it stays unsettling rather than
gross-out, and it still has to read as a legible silhouette, so escalation belongs in the
rare and higher tiers where a strange shape is the reward. The common tiers stay
recognizable; the restraint downstairs is what makes the escalation upstairs land.

**5. The voices: Charlotte, and Wilbur.** Two characters, decided by Silas
2026-08-24. Each is a **pair of existing records** — a kind_robots `Character` carrying
identity (personality, voice, sampleResponse, art) and a `Bot` carrying the narrator
behavior that speaks as it. Same reuse move the bestiary makes, and for the same reason:
those columns already exist, and going through both models means these two are available
to any other Kind Robots surface that wants them.

**Charlotte Fishmonger**, of the Portsmouth Fishmongers. The dreadfully cheerful head of
the aquarium. Silas's words, and "dreadfully" is doing the work — she is not cheerful
*despite* what the aquarium is, she is cheerful *about* it, warmly and without reservation,
in a register that never breaks. She is in charge, she is delighted you are here, and she
is entirely unharmed.

**Wilbur Stint**, her assistant. Male. Bespectacled. Young, but with thinning hair —
shoulder length and unevenly cut. A stutterer. Multiple missing fingers, scarred and
scratched. He really tries, and he is always injured.

**The names are the thesis.** *Charlotte's Web* is Silas's favourite book, and in it
Charlotte spends her whole life — literally, fatally — keeping Wilbur alive. Here she is
his cheerful superior, presiding over the operation that is taking him apart a finger at a
time, and she has never looked happier. That inversion is the most economical statement of
this game's tone available, and it is why these two are named what they are. It is also
never to be pointed at: no character references the book, no line winks at it, and nothing
in the UI explains the joke. It works entirely on whoever brings it with them.

("Stint" carries its own: a small wading bird, and a bounded period of labour — for someone
whose time here is being measured out in fingers.)

**The joke is the pairing, and it is not kind.** Charlotte runs the operation and is
immaculate. The assistant is the one actually reaching into the tanks, and he is visibly
coming apart doing it. She never mentions his hands. He never mentions his hands. Nobody
explains, apologises, or connects the two facts, and the game must never do it for them —
the moment anything acknowledges it out loud, the joke dies and takes the tone with it.
This is the Little Inferno move: cheerful complicity, and the cost paid somewhere off to
the side by someone not complaining.

**He has dignity, and this is a hard rule.** He really tries — that is the load-bearing
half of the character. He is the most sympathetic figure in the game and the only one who
seems to understand what is in the tanks. Write him earnest, competent, and unlucky, never
pathetic and never a fool. His stutter is characterisation, not a punchline: it is never
the reason a line is funny, it never appears in a moment played for laughs at his expense,
and the humour around him always lands on the situation or on Charlotte's obliviousness —
never on him. A build that gets this wrong is meaner than the game is, and it will read
that way immediately.

**Field notes remain a third register**, unattributed and separate from both. Authored text
only: nothing in this game makes a live model call at runtime, same offline constraint
Ruler is Hooked holds. Tracked as t-023.
