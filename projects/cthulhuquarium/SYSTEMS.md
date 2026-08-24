# Cthulhuquarium — Systems Design

date: 2026-08-24
status: draft, from Silas's design download in session
companion to: DESIGN-BRIEF.md (tone, characters, decided scope)

---

## The shape of the game, in Silas's own framing

> *"Set pieces should be what provides variation to the aquarium. Fish are what provide
> colour and eat to create currency, which is used to buy more food, fish, backgrounds,
> and upgrades."*

That is the whole economy in one sentence, and everything below serves it.

- **Fish** produce. They are the income engine and the collection.
- **Set pieces** modify. They are the build, and the source of synergy.
- **Backgrounds / tanks** frame. They are the milestone reward and the capacity.
- **Currency** flows from fish, and buys food, fish, backgrounds, and upgrades.

---

## Three ideas that collide with "progress never degrades"

Silas's rule — *"progress should never degrade, other than spending currency for
upgrades"* — is load-bearing, and three of the new mechanics violate it as stated. Each
has a resolution that keeps the idea and the rule. **These are the most important
paragraphs in this document**, because each one is cheap to settle now and expensive to
discover during implementation.

### 1. Fish that fight

> *"maybe some fish don't get along, or fight for resources"*

If a fight can kill, injure, or remove a fish, that is degradation and it is out.

**Resolution: rivalry is a rate effect, never a loss.** Two rival species in the same
tank both produce less while co-located. Nothing dies, nothing leaves, nothing you own
stops being owned. The moment you separate them, both recover fully.

This is strictly better than the punishing version, because it turns rivalry into a
**puzzle the player solves by arranging their tank** rather than a tax they pay for not
knowing. It also gives the "fish don't fight" set real value: it buys you out of a
constraint you can feel, which is the most satisfying kind of upgrade.

### 2. Debris and tank cleaning

> *"cleaning a fish tank is a reasonable task for users for a clicking game"*

Debris accumulating is degradation-shaped, and needs the same treatment as hunger.

**Resolution: debris throttles the production rate, never holdings.** A filthy tank earns
slowly. A cleaned tank earns fully. No coin total ever decreases and nothing is lost.

But debris is better than merely permissible — **it is the strongest active-play channel
in the game.** Silas's rule is that idling earns, and playing earns faster. Debris is
generated over time and cleared by clicking, so the longer you are away the more there is
to click when you return. That inverts it from a chore into an opportunity, and it means
the reward for coming back is *something to do*, not just a number that went up.

### 3. The idle-collection set

> *"set that picks up currency when the game is idle"*

This one points directly at the rule that idling must be **strictly worse** than playing.
A set that fully automates collection erases the active channel's advantage, and the game
quietly becomes a spreadsheet.

**Resolution: idle-collection sets collect a fraction, or up to a cap, never everything.**
Something like "collects 40% of what drops while you are away" removes the tedium of
missing an entire night without removing the reason to be present. The auto-collector set
that *moves around* (Silas's own note that it should) can be the better one precisely
because you can watch it work — it earns its keep as a thing to look at, not only as a
multiplier.

---

## The gating problem

Silas, verbatim, and this is the hardest question in the project:

> *"The hardest thing I have as a game creator is gating options. I just want to let the
> user fill a tank with every fish and option they want. but a good game gates those
> options through experience and play, with flavor text and character moments interspersed
> to mark as landmarks."*

The instinct to give everything away and the instinct to pace are both right. They only
conflict if gating means *withholding access*. It does not have to.

### Gate capacity, not access

**Make tank size the master gate.** Nearly every fish and set piece becomes purchasable
reasonably early. What stays scarce is **slots**.

Then "you can have every fish" is literally true — just not all at once. The question
stops being *"may I have this?"* and becomes *"what comes out to make room?"* That is a
**choosing** problem rather than an **access** problem, and choosing is the fun part.
Nobody resents a tank that is full; everybody resents a lock icon.

This is also the only gate that never has to say no, which matters for a game whose
central promise is that it never takes anything away.

It makes set pieces matter for free: **a set occupies a slot a fish could have used.**
Every build is a real trade — more modifiers or more producers — and that tension is
where synergy hunting actually lives.

### The unlock is the character moment, not the number

Silas already found this one:

> *"characters are who are seen at the beginning, during select screens... and then during
> the interstitials when a notable milestone has been reached (which to me feels like what
> unlocks backgrounds..eg. new tanks"*

Formalise it, because the ordering is the whole trick. **A milestone does not unlock a
background. A milestone causes Charlotte to appear, and she gives you the background.**
The reward for progress is a scene; the mechanical unlock rides along inside it.

This is Little Inferno's letters exactly, and it does three things at once: pacing becomes
authored rather than computed, the gate has a *face* so it reads as story rather than a
lock, and Charlotte and Wilbur get a structural reason to exist instead of being decoration.
It also means every gate is an opportunity to be funny, which is the best possible reason
to have one.

### Two economies, pacing each other

The two gates should draw on different currencies, so neither can be rushed by grinding
the other:

| | Buys | Earned by |
|---|---|---|
| **Coins** | fish, sets, food, upgrades — *breadth* | producing and clicking |
| **Milestones** | tanks, backgrounds, capacity — *room* | play landmarks, delivered by Charlotte |

Coins accumulate faster than milestones arrive. So you always own more than you have room
for, permanently — which sustains the choosing tension indefinitely without the game ever
once saying "you cannot have that." The catalogue is open; the tank is finite.

---

## Set pieces

Silas's seed list, with what each one is *for*:

| Set | Effect | Why it earns a slot |
|---|---|---|
| — | allows an extra species | buys capacity with coins instead of milestones — the pressure valve |
| — | more currency when food is eaten | rewards active feeding over idling |
| — | fish swim faster | visible, and speed likely feeds collection rate |
| — | fish don't fight | buys you out of the rivalry constraint |
| — | auto-collects coins, **and moves around** | Silas's own note that it should move — it is a thing to watch |
| — | picks up debris | competes with the snail and with clicking; see below |
| — | collects currency while idle | capped or fractional, per the collision above |

**For synergy to be real, set bonuses must key off fish properties, not be flat buffs.**
A set that boosts `school` fish rewards building a shoal tank. One that boosts `anchor`
species rewards a still tank of things that do not move. That is what produces archetypes,
and archetypes are what produce the surprise combos Silas is after — a flat +10% produces
arithmetic, not discovery.

**Three routes to debris, deliberately.** Manual clicking, the debris set, and the snail
all clear it. Keeping all three viable is what stops any of them becoming mandatory — the
moment one is strictly best, the choice dies and it stops being a build.

---

## Backgrounds

Silas: *"either completely aesthetic or having a singular bonus (the latter is better)."*

Agreed, with one constraint: **make the bonus qualitative, not quantitative.** A background
that *enables something* (a species can live here that cannot live elsewhere; debris
accumulates differently; a set behaves differently) stays interesting forever. A background
that gives +15% is obsolete the moment a +20% one exists, and since backgrounds arrive by
milestone rather than purchase, obsoleting the early ones means the early *story beats*
stop mattering too.

One bonus each, and they should be sideways from one another rather than ascending.

---

## The snail

> *"fish that is a snail that sits on the actual glass of the tank wall and clean debris"*

Authored as **The Sexton** — a sexton is a church caretaker who also digs the graves. It
needs a ninth movement mode, `cling`, because it is on the glass rather than in the water,
and per SCHEMA.md a new behavior needs its renderer motion landed in the same change.

It is the first species with a **functional** role rather than a purely economic one, which
is a precedent worth being deliberate about: functional fish risk becoming mandatory, and a
mandatory fish is one less real choice. The three-routes-to-debris rule above is what keeps
it optional.

---

## Open questions — resolved (agent recommendation, t-025, 2026-08-24)

Per t-025's own instruction, these are decided on paper rather than left to stall the
build. Each is a recommendation with reasoning, flagged here for Silas to confirm or
override — none of the four blocks t-026/t-027 from proceeding on this basis.

1. **Do set pieces and fish share one slot pool, or two? → One pool.** This document
   already assumed the answer two sections up, in "Gate capacity, not access": *"a set
   occupies a slot a fish could have used. Every build is a real trade."* A second,
   separate set-piece pool would quietly delete that sentence's tension and make sets a
   pure add-on instead of a real trade against fish — a strictly weaker design by this
   doc's own stated standard. **Schema implication for t-007:** `Aquarium` carries a
   single `slotsCap`; whatever occupies a slot (fish placement or equipped set piece)
   is accounted against that one total, not two separate caps. `AquariumStock` (or a
   sibling join row for set pieces) needs a `kind` discriminator so both draw from the
   same ledger.
2. **Is rivalry authored or emergent? → Both**, exactly as this doc's own draft
   guessed. A small emergent rules table (`predator` vs `small`, `anchor` vs `school`)
   scales for free as the bestiary grows past 20 species; a short authored override list
   is where the actual jokes live ("these two specifically loathe each other," no rule
   required). **Schema implication for t-003:** the fish bible needs (a) a couple of
   ecological tags per species — a diet role and a schooling role are enough to drive
   the emergent table — and (b) an optional authored `rivals: [slug, ...]` list that
   layers on top. Rivalry does **not** need its own Prisma model or table for t-007 —
   it is computed live, server-side, from whichever species are currently placed in an
   `AquariumStock`, against tag/override data already seeded onto the `Character` rows
   by t-008. This keeps rule 1 ("progress never degrades") trivially true for rivalry
   too: it is a live rate effect with no persisted loss state to accidentally leak into
   holdings.
3. **Does tank size grow, or do you own several tanks? → One growing tank per aquarium
   for v1.** DESIGN-BRIEF's MVP scope is written in the singular throughout ("load and
   interact with **their** aquarium," "see **their** tank") and multiple tanks is the
   costlier option on both axes this doc already flagged (persistence and UI). Ship the
   simpler version now. **Schema implication for t-007:** key `Aquarium` by
   `(userId, slug)` rather than a hard one-row-per-user unique constraint. That costs
   nothing today and leaves a second tank as a purely additive future feature (a new
   row, not a migration) if Silas wants tier-2 multi-tank play later — do not build
   multi-tank UI or persistence now, just don't foreclose it in the schema.
4. **What is a milestone? → A landmark event, not a coin threshold**, delivered through
   a Charlotte (occasionally Wilbur) interstitial per "The unlock is the character
   moment, not the number" above, and consistent with DESIGN-BRIEF's own call that the
   leaderboard metric is species collected, not coins. Concrete v1 landmark set: first
   full tank (every slot filled), first evolution, first spotless tank (debris fully
   cleared after being high), first rivalry resolved (a placed pair separated), and
   bestiary breakpoints (e.g. 5 / 10 / 15 / 20 species collected). **Schema implication
   for t-007:** none beyond what is already planned — each landmark is one
   `AquariumEvent` row with `kind: 'milestone'` and a `payload` naming which landmark
   fired; that event is what a Charlotte interstitial reads to decide what to say and
   which background to hand over. No new model needed.

FOR SILAS: the four decisions above are this session's recommendation, not a unilateral
final call — reopen any of them with a note here or on cthulhuquarium/t-025 if a
different answer fits your vision better. t-026/t-027 (and t-007's schema) will proceed
on this basis unless you say otherwise.
