# Cthulhuquarium — Genre Research

date: 2026-08-24
task: cthulhuquarium/t-006
status: complete

Silas's brief: "Look into both gameplay loops, current features for light aquarium
experiences, and what kind of features people want and appreciated." This surveys
Insaniquarium, Cookie Clicker, Universal Paperclips, Melvor Idle, Abyssrium, and
current web aquarium/idle games, then answers four questions and ends with a concrete
adopt/adapt/reject list — not a survey for its own sake.

Sources checked this session are linked inline and listed at the bottom. Design
patterns below are cross-referenced against `DESIGN-BRIEF.md`, `SYSTEMS.md`, and
`ECONOMY.md`, which already made several of these calls — this document explains
*why* those calls line up with what the genre has already learned, and flags the
one or two places where Cthulhuquarium's committed decisions cut against common
practice on purpose.

---

## 1. The six reference points

### Insaniquarium (2001, PopCap) — the direct namesake and named inspiration
The loop: feed guppies, guppies drop coins, coins buy eggs (bigger fish, pets,
upgrades), bigger fish + carnivores eat the guppies unless you feed everyone in
time, aliens periodically invade and must be shot or the tank gets torn apart.
Progress per level is gated by "earn enough to buy three egg pieces," which is a
soft micro-goal within an otherwise open tank. [Gameplay detail via StrategyWiki
and the Insaniquarium Fandom wiki.]

What actually made it sticky wasn't the clicking — it was the **triage tension**: a
full-screen tank of hungry mouths plus an alien invasion is a juggling act, not a
tap-to-win loop. That tension is exactly what Cthulhuquarium's hunger-as-rate-gate
and debris-as-active-play-channel (t-027) are reaching for, minus the fail state —
Silas's "nothing ever degrades" rule keeps the *feel* of triage without Insaniquarium's
actual loss condition (a starved fish there just dies).

The **pets with unique passive abilities** (Zorf who auto-feeds, Itchy who
auto-fights aliens, Stinky who auto-collects coins) are a direct ancestor of
Cthulhuquarium's set-piece system (t-026): named, personality-bearing objects that
automate one specific chore rather than a generic "+10% income" node. Worth noting
explicitly for t-026's authoring pass — Insaniquarium's pets earned their place by
having a *verb*, not a *modifier*.

### Cookie Clicker (2013, Orteil) — the genre's most-copied skeleton
Click for currency → currency buys generators → generators produce currency
passively → currency buys upgrades that multiply generator output → occasional
prestige (heavenly chips) resets the generator count but permanently multiplies
future production. Its lasting contribution to the genre isn't the mechanics
(clicking a cookie is arbitrary) but the **discovery cadence**: something new to
buy or notice is always close, achievements fire constantly for both meaningful and
joke-sized reasons, and flavor text rewards attention with jokes rather than
information. Cookie Clicker also popularized the *idle-vs-active* framing directly
relevant to Cthulhuquarium's mandate ("leave it running... or play with it and it
will gain resources faster") — active clicking has always out-produced idling in
Cookie Clicker, and the game has never hidden that fact or apologized for it.

### Universal Paperclips (2017, Frank Lantz) — the narrative-through-mechanics case
Starts as a bare clicker (make one paperclip at a time) and *escalates its own
genre* over roughly three acts: manual clicking gives way to automated production,
then to a stock-market/wire-buying minigame, then to a strategic AI-expansion
phase that barely resembles the opening screen. The lesson that transfers directly:
**the interface itself is allowed to change as a reward**. Nothing is explained in
advance; the player learns each new system by being handed its controls at the
moment it becomes relevant, and the escalating absurdity (a clicker about
paperclips slowly reveals it is about instrumental convergence) works because early,
tiny rewards train trust before the game asks for a bigger one.

Cthulhuquarium's "gate capacity, not access" design (t-028, SYSTEMS.md) already
follows this instinct — new tank slots and backgrounds are handed over via a
Charlotte interstitial rather than a menu unlocking silently — but Paperclips
pushes one step further worth flagging for t-028: consider letting the *shop UI
itself* gain a section or a visual tell the first time set pieces (t-026) become
available, rather than a static shop that merely un-grays an item. A UI that
visibly grows alongside the player's aquarium reinforces "this game is escalating,"
which is core to the darkly-funny escalation ladder (CLEARLY-NOT-A-FISH) the fish
bible is already built around.

### Melvor Idle (2020, Games by Malcs) — the RPG-skilling idle hybrid
A RuneScape-inspired skilling/combat idler where every skill trains passively once
started and feeds other skills (woodcutting feeds firemaking feeds cooking, etc.),
with real offline-progress banking and no forced prestige loop at all — you can
play Melvor Idle for hundreds of hours without ever resetting. [Design notes via
missionszanx.com and reviewsbysupersven.com.] Its retention thesis is explicit:
**continuous, legible, never-reversed progression** — "small, consistent efforts
lead to real results" — is enough on its own, without a prestige gimmick, as long
as the interlocking systems keep producing new things to do.

This maps almost exactly onto Silas's decision 1 (progress never degrades, no
prestige resets) and the ENDLESS-BUT-THE-BESTIARY-COMPLETES framing (decision 3).
Melvor Idle is the strongest existing proof that a well-loved idle game does not
need a prestige-reset loop to retain players for the long haul — it needs
interlocking systems (here: fish behavior classes, set-piece synergies, rivalry,
milestones) that keep producing *new legible things to notice*, which is a closer
match to Cthulhuquarium's committed design than Cookie Clicker's reset-based model.

### Tap Tap Fish: AbyssRium (2016, MoonActive/Nekki) — the closest genre sibling
An idle aquarium-building game: tap to feed and collect currency, currency buys
coral and fish species, more species and coral raise passive income, the tank
visibly and continuously expands and levels up as a direct result of collection
progress rather than a separate stat. [Via mwm.ai, Google Play listing, and the
Zelda Zone hidden-fish guide.] The things AbyssRium gets right for a tank game
specifically: the *collection itself visibly redecorates the play space* (an
aquarium with 40 species just looks different from one with 4 — no separate
"trophy room" needed), and species range from mundane to increasingly implausible
(dolphins and whales sharing a tank with player-fantasy creatures), which is a
looser cousin of Cthulhuquarium's own CLEARLY-NOT-A-FISH escalation ceiling.

Where AbyssRium is a cautionary tale rather than a model: its hidden/secret-fish
mechanic (per the Zelda Zone walkthrough, several species require obscure,
undocumented trigger conditions to unlock) trades legible progression for a wiki
dependency — exactly the kind of "figure out random UI element" friction Melvor
Idle and Cookie Clicker both avoid by telegraphing what unlocks what. Flagged as a
reject below.

### Current web aquarium/idle landscape (2026 snapshot)
Beyond AbyssRium's Classic re-release (a stripped, ad-lighter version of the
original — itself a tell that MoonActive judged the original's monetization too
aggressive for a 2026 relaunch), the browser/mobile idle-aquarium space is thin:
most "aquarium" idle games on app stores are AbyssRium clones or reskins with
near-identical mechanics and heavier ad/gacha layers. There is no dominant
*browser-first, no-account, playable-in-one-tab* aquarium idle game occupying the
niche Cthulhuquarium is aimed at — which is a genuine opening, not just a gap:
Insaniquarium itself has no real live successor, and nothing in the current
landscape combines Insaniquarium's active-triage feel with AbyssRium's passive
collection-driven tank growth the way Cthulhuquarium's design already intends to.

---

## 2. What makes an idle loop retain players past day 3

Cross-referencing the design-blog material [GridInc, Mind Studios, apptrove] against
the games above, the pattern is consistent across every source and every game
studied:

1. **The first dopamine loop has to land fast and visibly.** Games that deliver a
   well-paced early loop see meaningfully better Day-7 retention than the ~8%
   category benchmark [per the retention-benchmark search above]. For
   Cthulhuquarium: the current MVP's first few minutes (feed → collect → first
   unlock) needs to produce a visible, legible change in the tank within the first
   session, not just a number going up — which argues for front-loading at least
   one "new species just appeared" beat well before the first real milestone.
2. **Offline progress has to matter without making active play pointless.**
   Melvor Idle, AbyssRium, and Cookie Clicker all bank offline gains; all three also
   make active play strictly better per unit time. Silas's own instruction to
   `t-004` ("idling must be rewarding but strictly worse than playing") is exactly
   this consensus, and `ECONOMY.md`'s simulated 3x-by-minute-120 active/idle gap
   already validates it numerically rather than by assertion.
3. **Interlocking systems beat isolated stat grinding.** Melvor Idle's skills
   feeding each other, and AbyssRium's species-count directly reshaping the tank's
   passive income *and* its appearance, both outperform flat, disconnected upgrade
   trees. Cthulhuquarium's synergy rule for set pieces (t-026 — bonuses must key off
   fish *properties*, not flat percentages) is already the right shape for this;
   this research confirms it rather than discovering it fresh.
4. **Prestige, if present at all, must be optional and clearly explained before the
   reset, or it reads as punishment.** The design-blog material is blunt about this:
   badly timed or unexplained prestige "strongly penalizes long idle periods" and
   is a top complaint category. Cthulhuquarium's decision to have *no* prestige loop
   at all (decision 1) sidesteps this entire failure class rather than trying to
   tune around it — the Melvor Idle precedent shows that's a fully viable choice for
   long-term retention, not a compromise.
5. **The escalating absurd is a legitimate retention hook on its own.** Universal
   Paperclips proves a minimal, honest opening (one paperclip, no lecture) earns
   the trust needed for a much stranger mid-game reveal later. This directly
   supports keeping common-tier fish ordinary and legible while reserving
   CLEARLY-NOT-A-FISH weirdness for rare-and-above tiers — the restraint at the
   bottom is what makes the escalation at the top land, which is already
   `DESIGN-BRIEF.md`'s own stated reasoning; this research corroborates it from the
   outside rather than just from house style.

## 3. Collection systems that reward without grinding

The strongest pattern across AbyssRium and Melvor Idle: **collection has to change
what the player sees, not just what a counter says.** AbyssRium's tank visibly
looks different at 40 species vs. 4; Melvor Idle's skill tree visibly opens new
areas as skills level. A collection system that only updates an off-screen
"12/64 fish collected" counter is the grinding version; one where every new fish
actually swims in the tank, has a revealed field note, and changes the tank's
visual density is the rewarding version. Cthulhuquarium's bestiary-as-win-state
design (t-024) already calls for exactly this ("a bestiary view worth returning
to... its silhouette of what you have not found yet") — the genre precedent says
that silhouette-of-the-unknown affordance (seen in most modern collection games,
and implicitly present in AbyssRium's "??? " placeholder tiles) is worth keeping
as a first-class UI element, not a stretch goal.

The other half of "without grinding": **gate capacity, not access** (already
Cthulhuquarium's stated design in SYSTEMS.md/t-028) is precisely the fix for the
genre's most common grinding complaint — games that force repetitive, low-variance
actions purely to raise a currency total before the *next* interesting thing is
allowed to happen. Species should become ownable through normal, varied play (not
a single repetitive minigame), with tank-slot capacity as the only real limiter.

## 4. What players complain about — and how the current design already avoids it

| Complaint (from design-blog sources + the games' own live reviews) | Cthulhuquarium's current answer |
|---|---|
| **Fake difficulty / walls that exist only to slow spend, not to be interesting** | Gate capacity not access (t-028) — nearly everything is purchasable early; the wall is room, not permission. |
| **Ad gates interrupting the loop** | Not in scope for this project at all — no ad SDK anywhere in the brief; monetization isn't part of MVP. Worth stating explicitly here so a future task doesn't casually introduce one without a design conversation. |
| **Unexplained/undocumented prestige resets that read as punishment** | No prestige system exists (decision 1) — sidesteps the complaint category entirely rather than tuning it. |
| **Hidden/secret unlock conditions requiring a wiki (AbyssRium's specific failure)** | Every unlock Cthulhuquarium ships should be legible from in-game state — a milestone the player can see coming (t-028's "two economies pacing each other": coins accumulate faster than milestones, so the player always sees the next threshold approaching). **Explicit recommendation below: reject undocumented/hidden-trigger unlocks outright.** |
| **Automation that makes active play pointless once purchased** | The idle-collection set piece is explicitly capped ("a FRACTION or up to a cap, never everything" — t-026's hard constraint) for exactly this reason; full auto would flatten the active/idle gap ECONOMY.md worked to establish. |
| **Loss/decay mechanics that punish returning players** | Explicitly ruled out project-wide (decision 1: nothing accumulated ever shrinks). This is the single biggest genre-complaint category the design sidesteps by fiat rather than by careful tuning, and the research above suggests that's the right call, not a missed opportunity for tension. |

## 5. Recommendation list — adopt / adapt / reject

Three features to steal outright, as asked, plus the calls worth recording
explicitly so a later task doesn't relitigate them:

1. **ADOPT — Insaniquarium's named, single-verb automation pets**, generalized into
   Cthulhuquarium's set pieces (t-026). Each set piece should read like Zorf/Itchy/
   Stinky: one clear job, a personality, and a moment where the player *watches it
   work* (Silas's own note on the coin-collector set: "it should be a thing you can
   watch working"). Reason: this is the single most-loved mechanic across the six
   references and it's already partway adopted in the roadmap — this is confirmation
   to keep authoring set pieces with a verb each, not a percentage each.

2. **ADOPT — Melvor Idle's interlocking-systems-without-prestige retention model.**
   No reset loop; instead, keep every system (fish behavior classes, rivalry,
   set-piece synergies, milestones) feeding into and reframing the others so there's
   always a new legible thing to notice. Reason: strongest available evidence that
   long-term retention doesn't require a prestige mechanic, which matches Silas's
   decision 1 exactly and gives the team confidence not to add one "for genre
   compliance" later.

3. **ADOPT — AbyssRium's collection-changes-the-view principle**, but paired with a
   legible unlock condition (never a hidden trigger — see reject below). Every new
   species should visibly alter the tank the moment it's unlocked, and the bestiary
   view (t-024) should keep an unfound-silhouette affordance so the collection goal
   is always visible, not just implied by a counter.

4. **ADAPT — Universal Paperclips' escalating-interface-as-reward.** Don't copy its
   three-act structural rewrite (out of scope for an MVP), but do let the shop/
   bestiary UI visibly grow a new section or visual tell the first time set pieces
   (t-026) or rare-tier fish become available, rather than a static UI that merely
   un-grays a button. Small, cheap, and reinforces the sense of escalation the
   design already leans on.

5. **ADAPT — Cookie Clicker's flavor-text-as-reward-for-attention habit.** Don't
   copy its achievement-spam cadence (it would fight Wilbur's dignity rule and the
   dry museum-placard register already established for field notes), but do keep
   the instinct that *noticing things* should be rewarded with a line of authored
   text, not just a number — which the field-note-on-first-unlock design (t-012)
   already does. No new task needed; this is confirmation of an existing call.

6. **REJECT — hidden/undocumented unlock triggers** (AbyssRium's specific failure
   mode). Every Cthulhuquarium unlock should be legible from visible game state —
   a threshold the player can see approaching, not a wiki-dependent secret. Worth
   recording explicitly here since nothing in the current design docs rules it out
   in writing, and it would be an easy trap to fall into while authoring "random
   rare experiences" (t-016) if not flagged.

7. **REJECT — ad-gated progress and pay-walled speed-ups.** Not currently planned
   anywhere in the design docs, but common enough across the genre (60-70% of idle
   games monetize primarily through ads, per the design-blog survey) that it's
   worth an explicit no here rather than leaving it merely unaddressed, given this
   project has no monetization task on its roadmap at all yet.

8. **REJECT — Insaniquarium's fail-state alien-invasion tension**, specifically the
   "creature can die/be lost" half of it. The *triage feeling* is worth keeping
   (adopted implicitly via debris + hunger-as-rate-gate), but the actual loss
   condition contradicts decision 1 outright and should not be reintroduced even in
   a softened form (e.g. "a neglected fish leaves the tank") — that would still be
   a decrease, which the project has ruled out categorically.

---

## Sources

- [Insaniquarium! Deluxe/Gameplay — StrategyWiki](https://strategywiki.org/wiki/Insaniquarium!_Deluxe/Gameplay)
- [Insaniquarium — PopCap Games Wiki (Fandom)](https://popcapgames.fandom.com/wiki/Insaniquarium)
- [Aliens — Insaniquarium Wiki (Fandom)](https://insaniquarium.fandom.com/wiki/Aliens)
- [Tap Tap Fish: Abyssrium Classic — MWM](https://mwm.ai/apps/tap-tap-fish-abyssrium-classic/6476528044)
- [Tap Tap Fish AbyssRium (+VR) — Google Play](https://play.google.com/store/apps/details?id=com.idleif.abyssrium&hl=en_US)
- [AbyssRium: Tap Tap Fish Hidden Fish & Gameplay Guide — The Zelda Zone](https://zelda.zone/guides/abyssrium/tap-tap-fish-abyssrium-walkthrough-hidden-fish-guide/)
- [Idle Games Best Practices: Design and Strategy — GridInc](https://gridinc.co.za/blog/idle-games-best-practices)
- [How to Make an Idle Game to Thrive Beyond App Store Trends — apptrove](https://apptrove.com/how-to-make-an-idle-game/)
- [Idle Clicker Games: Best Practices for Idle Game Design and Monetization — Mind Studios](https://games.themindstudios.com/post/idle-clicker-game-design-and-monetization/)
- [Melvor Idle review — reviewsbysupersven](https://reviewsbysupersven.com/melvor-idle/)
- [Idle Game Design: Systems, Mechanics, and Progression — Missions Zanx Online](https://missionszanx.com/guides/idle-game-design-systems-mechanics-and-progression)
- [Unlocking the Secrets of Universal Paperclips — Toolify](https://www.toolify.ai/ai-news/unlocking-the-secrets-of-universal-paperclips-14445)
- [Universal Paperclips is the smartest game about a dumb goal — webiano.digital](https://webiano.digital/universal-paperclips-is-the-smartest-game-about-a-dumb-goal/)
- [How Idle Are Idle Games? An analysis of Universal Paperclips — Critical Video Game Studies](https://criticalvideogamestudies.com/how-idle-are-idle-games-an-analysis-of-univeral-paperclips/)

## Cross-references

- `DESIGN-BRIEF.md` — art direction, MVP bar, guardrails this research checks against.
- `SYSTEMS.md` — t-025's four resolved systems questions (slot pool, rivalry, tank
  count, milestone definition); items 1-3 above corroborate the milestone-as-landmark
  and interlocking-systems calls already made there.
- `ECONOMY.md` — the simulated active/idle gap this research's point 2 references.
- Roadmap tasks directly informed: t-012 (field-note-on-unlock, confirmed not
  re-scoped), t-016 (flag hidden-trigger rejection before authoring rare events),
  t-024 (bestiary silhouette affordance), t-026 (set-piece verb-not-percentage
  authoring guidance), t-028 (UI-growth suggestion for the shop/bestiary).
