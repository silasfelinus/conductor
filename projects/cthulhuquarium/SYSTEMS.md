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

**Resolution: rivalry is a rate effect, never a loss.** Silas's own framing, and it is
cleaner than the abstract version: *"fish fighting with each other would not be eating,
thus not generating resources."* A squabbling fish is a fish that stopped eating. The
mechanic is already in the game — it is hunger, arrived at socially instead of by neglect.

Refinements from Silas, 2026-08-24:

- **Fish can fight their own species.** Territory pressure, not just cross-species dislike.
  Two of the same fish in a cramped tank is a real consideration, which makes the size and
  slot systems below matter more.
- **A squabble can briefly incapacitate one fish.** Short, recoverable, self-clearing. This
  stays inside the rule: an incapacitated fish produces nothing for a moment, and then it
  does again. Nothing is lost, only paused.

Nothing dies, nothing leaves, nothing you own stops being owned.

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

**Resolution, and Silas gave it a testable form:**

> *"an active player should always be able to evolve faster than someone idling with
> equivalent upgrades."*

Treat that as **the invariant the whole economy is balanced against.** It is the single
most useful sentence in the systems layer, because it is falsifiable: take two identical
save states, idle one and play the other, and measure. Any set, upgrade, or background
that breaks it is mis-tuned by definition, and t-019's balance pass should assert it
directly rather than eyeballing it.

Within that, idle collection is free to be generous — Silas: *"idle collection can still
pick up slower than an active user. A set item can have an effect that it just affects the
rate."* So idle sets scale the rate rather than being capped arbitrarily, which is a better
mechanism than a hard ceiling: it stays meaningful at every tier instead of hitting a wall.

The auto-collector that *moves around* (Silas's note that it should) earns its keep partly
as a thing to watch, not only as a multiplier.

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

1. ~~Do set pieces and fish share one slot pool, or two? → One pool.~~
   **SUPERSEDED BY SILAS, 2026-08-24: two distinct pools, measured differently.** This
   session recommended one shared pool and reasoned it well from this document's own
   "a set occupies a slot a fish could have used" line — but Silas had the opposite
   instinct first and kept it: *"I definitely thought originally that they would be
   different pools, as it would be easier to fit locations when accommodating for
   sizes... For now, let's say that the pools are distinct, but I like the idea and will
   consider it in playtesting."* The shared-pool idea is parked, not rejected.
   The shipped model, and the asymmetry is deliberate: **set slots are counted** (start
   with three, buy up to about five), **fish capacity is weighed** by total `size` rather
   than by count. Counted set slots stay easy to hold in your head; weighed fish capacity
   turns stocking into a packing problem. See "Capacity: two pools, two units" below.
   **Schema implication for t-007, replacing the one above:** `Aquarium` carries TWO
   caps — a counted `setSlotsCap` and a weighed `sizeCap` — and a tank upgrade raises
   both. Do NOT build the single-`slotsCap`-plus-`kind`-discriminator shape recommended
   above; it models the wrong thing now. Keep both capacity checks in ONE place, though,
   because Silas may swap to a shared pool after playtesting and that should be a rule
   change rather than a refactor.

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
   **Extended by Silas, 2026-08-24**, in ways the emergent table above does not yet
   cover: fish can fight **their own species** over territory, so the rules table needs a
   same-species crowding term rather than only cross-species pairs; and a squabble may
   **briefly incapacitate** one fish. Incapacitation is short, self-clearing, and stays
   inside the rule — it is a live rate effect like the rest, and must not be persisted as
   damage. Silas's framing is also the cleanest statement of the whole mechanic: a
   fighting fish *is not eating*, so rivalry is hunger arrived at socially.
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

## Capacity: two pools, two units

Decided 2026-08-24. The pools are distinct and they are **measured differently**, which is
the part worth getting right:

- **Set slots are counted.** Start with three; buy more; cap somewhere around five. A
  small, legible number the player holds in their head.
- **Fish capacity is measured by size.** Fish have a `size`, and a tank holds a total, not
  a count. Silas: *"fish could be say different sizes and an aquarium can accommodate more
  or less."*

That asymmetry is doing real work. Counted set slots make builds easy to reason about;
size-weighted fish capacity makes stocking a **packing problem** — six small fish or one
enormous one — which is a far better decision than "pick six." It also gives the tier-5
monsters a cost beyond price: The Long Patience should eat most of a tank.

`size` is therefore a new required field on every species in the bible.

**Tank upgrades raise both**, which keeps the milestone reward legible: a bigger tank means
more room *and* more sets, so an interstitial that hands you a new tank always visibly
changes what you can do.

## Genetics: hidden stats, breeding, and secret evolutions

Silas, 2026-08-24, and this is the largest single addition to the design so far:

> *"whether fish can mate. if we allow fish to have secret random stats, then that could
> include the ability to create new fish, which would be how the user can discover the
> secret evolution fish. Then we have an entire hidden pokemon like stat system."*

### The species/individual split this forces

This is the architectural consequence and it needs stating plainly, because it changes
t-007's schema: **the bible describes species; your tank contains individuals.**

- A `Character` row is the **species template** — the six public `Rarity` stats, the field
  note, the art. Shared by everyone, identical for all copies.
- An `AquariumStock` row is **one actual fish** — its own hidden rolled stats, its
  nickname, its hunger, its parents. Yours alone.

Two goldfish are the same species and different animals. Every hidden stat lives on the
individual, never on the species, and the bible stays a catalogue rather than becoming a
save file.

### Rules that keep it from becoming a grind

- **Breeding never consumes the parents.** Progress never degrades; a pairing produces a
  new individual and leaves both parents exactly as they were.
- **Hidden stats are discovered, not rolled-for-forever.** If the only path to a good fish
  is re-buying a hundred of them, the game becomes a slot machine. Breeding should
  *converge* — offspring should inherit toward the better parent — so effort compounds
  instead of resetting.
- **Secret evolutions are the payoff**, and they are a second, separate evolution axis from
  the goldfish line: one evolves by growth, the other only appears through breeding. Both
  use the same `evolves_to` plumbing; the difference is how you get there.
- **Nothing hidden may be strictly required.** A player who never touches breeding should
  still finish the bestiary. Genetics is depth for the people who want it, not a wall for
  the people who do not.

## The shop rotates; the book is forever

Silas: *"set pieces are static bonuses, and can be bought whenever. But fish will rotate
through."* Plus selling fish back — *"usually at a loss, but if they end up breeding fish
with good stats, or a new evolve, it could be worth more."*

**These two ideas create a problem and then solve it, which is worth spelling out.**

The problem: rotating stock plus selling means a player can sell a fish and then be unable
to buy another. That is exactly the kind of quiet, permanent loss the no-degradation rule
exists to prevent — and it is worse than an obvious one, because the player will not notice
until they want it back.

The solution is already in Silas's own message: **the Ichthyonomicon records every species
you have ever bought or raised, including ones you no longer own.** Make that record the
**re-purchase mechanism**, not just a trophy case. Then:

- **Rotation governs discovery, not access.** Today's stock is what is *new, cheap, or
  well-rolled* — a reason to check in, not a gate. Anything you have ever owned is orderable
  from the book at any time.
- **Selling becomes genuinely safe**, so the sell button can be an ordinary part of play
  rather than a decision the player has to be protected from.
- **It matches the gating philosophy exactly.** Gate capacity, never access. The shop is a
  rotating window onto a catalogue that never closes.

**Selling at a loss is fine** — that is spending, which Silas's rule already permits — but a
well-bred individual selling for *more* is the good version, because it makes breeding an
economy rather than a collection sidebar.

## The Ichthyonomicon

Silas asked for a name closer to a grimoire than an encyclopedia, and asked for the spelling
checked. The Greek for fish is *ikhthús*, and the standard combining form is **ichthyo-**
(as in ichthyology, ichthyosaur). The parallel formation to *Necronomicon* is therefore:

> **The Ichthyonomicon**

Its formal name. In dialogue, Charlotte and Wilbur should call it something flatly mundane —
"the book", "the register" — because the gap between what it is called on the cover and what
the staff call it is free characterisation.

What it holds: every species ever bought or raised, whether or not it is currently owned;
the field note, revealed on first acquisition; the best individual stats seen of each; and
the re-order button that makes rotation safe.

## Scope note, offered honestly

Breeding, hidden stats, rotating stock, selling, and the Ichthyonomicon are a substantial
systems layer — plausibly larger than the entire MVP Silas defined ("a fully working webpage
where users can load and interact with their aquariums").

They are **designed now and built later**: captured here in full, tracked as m3 tasks, and
deliberately not folded into the m2 tasks that get the game playable. The MVP still ships on
its original eight points. Nothing above is descoped — it is sequenced, and the design work
is done while it is fresh rather than reconstructed later.

## Open questions

The original four are answered above in **"Open questions — resolved"** — three by a
concurrent session's t-025 pass, and the slot-pool one by Silas directly, overriding that
session's recommendation. This list is kept empty deliberately rather than deleted: it is
where the next round goes.

Currently open, raised by the genetics and shop sections above:

1. **Does breeding need a dedicated space, or do fish pair in the tank?** A breeding tank
   is a second capacity sink and another thing to buy; pairing in place is simpler but
   makes crowding do double duty as both rivalry pressure and breeding pressure.
2. **Do hidden stats show once discovered, or stay hidden forever?** Revealing them after
   the fact makes breeding legible and plannable. Keeping them hidden preserves mystique
   but risks the player never understanding why one fish outperforms another — and a
   system nobody can perceive is a system nobody enjoys.
3. **How many secret evolutions exist?** One would confirm the mechanic. A dozen would be
   the spine of the late game. This is a content-budget question as much as a design one.
