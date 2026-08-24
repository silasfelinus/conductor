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

## The shared bestiary

Fish are **`Character` records in the kind_robots database**, not a
Cthulhuquarium-private table. This is the single most important architectural call in
the brief and it is deliberate:

- `Character` already carries `species`, `class`, `backstory`, `quirks`, `alignment`,
  `slug`, `packId`, and six `Rarity` stats (`charm`, `empathy`, `grace`, `luck`,
  `might`, `wits` — `COMMON` → `MYTHIC`). That is a bestiary schema already.
- It already has `artImageId` / `cardArtImageId` / `heroArtImageId` / `artPrompt`, so
  fish plug straight into the existing Comfy art pipeline with zero new plumbing.
- **Ruler is Hooked already uses `Character`.** Its brief commits to the same model and
  its "evil" ecosystem branch produces dark, twisted, catchable fish. Same model means
  the twisted lake fish and the aquarium monsters are literally the same records —
  catch it in one game, find it in the other, no sync layer, no duplicate art.
- A `Pack` (`abyssal-bestiary`) groups them, so either game can query its own subset
  without either game owning the others' fish.

The canonical source of truth is `fish/` in the **cthulhuquarium repo** — plain YAML,
one file per fish, human-editable, diffable, portable. A seed script reads that YAML
into `Character` rows. The repo stays authoritative so the bestiary survives a database
migration, an offline build, or a future Steam port that has no Kind Robots behind it.

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

## Open questions for Silas

1. **Do fish die?** Insaniquarium's tension came from starvation. A darkly funny game
   arguably *needs* loss — but an idle game that punishes you for closing the tab is a
   game people close permanently. Current assumption: fish get hungry, sad, and stop
   producing, but do not die while you're away. Worth overriding if you want teeth.
2. **Is there an end state**, or does the tank just deepen forever? Sunless Sea has an
   ending. Cookie Clicker doesn't.
3. **How weird is too weird?** The bestiary can go from "unsettling anglerfish" to
   "clearly not a fish." Where's your line?
4. **Does the aquarium talk back?** A narrator voice (a previous owner's notes, the
   shop keeper) is very on-tone but is new scope.
