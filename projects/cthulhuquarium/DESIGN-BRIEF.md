# Cthulhuquarium — Design Brief

date: 2026-08-24
status: draft (scaffolded in-session with Silas; scope confirmation is t-002, non-blocking)
author: Reviewer (Claude), from Silas's pitch on kind_robots Project 2112

---

## What it is

A darkly funny idle aquarium game. You inherit a tank that was already in the back
of the curiosity shop before you got there. Things live in it. You feed them. They
grow. Some of them are grateful.

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

**Visual.** Silhouette-forward. Dark water, strong backlighting, fish read as shapes
before they read as anatomy. Limited palette per tank — one sickly light source, one
accent. Fish get expressive eyes; everything else can stay murky. This is deliberately
chosen to be *generatable*: silhouettes and rim-light survive Comfy's inconsistency far
better than detailed, consistently-colored creature art would.

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
