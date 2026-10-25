# Ecotone companion first encounters and re-encounters (text draft v1)

**2026-10-25 PT · t-009 · text only.** No art, ArtJobs, deployment or publishing. Authored from
[COMPANIONS-AND-PROLOGUE.md](COMPANIONS-AND-PROLOGUE.md) and [COMPANION-OPTIMAL-PATHS.md](COMPANION-OPTIMAL-PATHS.md),
inside the [2026-10-22 exclusion decision](EXCLUDED-CONTENT-2026-10-22.md) (no Wiyot/Tuluwat material, no tribal-grant or
reservation backstory for Mara, no culturally coded designs). Cedar and Mara are working names; this is draft prose for
the t-004 creative review, not final card copy.

## Contract every intro obeys

- **One canonical event.** The same impossible sign (a six-winged form / repeating shape / CB tone) is real in all four intros. The opening
  perception changes who you meet first and how it is *perceived*, never whether it is true.
- **2-4 consequential choices each.** At least one no-roll "do something useful" option, at least one sober-verifiable evidence option,
  and a failure on any roll leaves a recoverable, still-informative scene (no dead end, no reroll on reload).
- **Optional companionship.** Each intro ends with Stay-with-current / Follow / Decline-and-meet-later. Declining never locks that companion's
  optimal arc (see Re-encounters).
- **Sober evidence parity.** Each intro stores one `evidence:*` item that a sober player can reach by an ordinary route, and that unlocks the same
  later clue regardless of opening perception.
- **No identity levers.** Heritage, sobriety and body are never stats, keys or moral scores. Competence comes from the person's work and life.
- **Flags** reuse the names in COMPANION-OPTIMAL-PATHS.md; new ones are marked *(new)*.

## 1. Mara: "Lines Where I Left Them" (Sober opening)

**Motivation:** protect a client's privacy and her own authorship. She wants to know who is copying a design before she has drawn it, without
exposing whoever asked for it.

> A table of handwritten price tags and bold flash sheets. The artist behind it, ink winding down both forearms, is drawing a bird with six
> wings. You are fairly sure it had four a moment ago.
> "There's a reason I don't smoke when I'm working," she says. "I like my lines where I left them."
> She lays the new sketch beside an older page. The extra wings are on both. The older page is dated next week.

| # | Choice | Check | Success | Failure (recoverable) |
|---|--------|-------|---------|----------------------|
| 1 | Compare the dates against her appointment book | Wits 7 | `evidence:dated_flash_pair`; she realises the book itself has an entry she did not write | You only confirm the one date mismatch; she still trusts you with the book later |
| 2 | Ask why she came to this festival | Rizz 7 | Her stakes: rent, a regular client who must stay unnamed, a rival shop's flyers | Awkward answer, but she names the client's *situation*, not the client |
| 3 | Mind the table while she checks the original | none, costs time | `mara_trust_table` *(new)*; a stranger asks for the six-wing design and you can refuse on her behalf | She may decline help; you learn where her studio is instead |

**Sober parity item:** the dated pair is a physical object any opening can inspect at the re-encounter.
**Close:** Follow sets `follow_history += mara`; Decline sets `mara_met_later = true` and she leaves a card with the studio address.

## 2. Kit: "The Stage That Won't Fold" (Tipsy opening)

**Motivation:** keep a giant kinetic puppet, and the people who built it, out of a sponsor's brand deck before a lease expires.

> A maker co-op loading dock, a puppet the size of a bus half-folded onto a pedal cart. Kit hangs from a gantry, grinning, mid-argument with
> three builders about whose name goes on the drawings. She tells you her cousin Pa Nhia, who wires half the machine, is the only one being
> sensible. Then the puppet folds a hinge that does not exist, and for a second the loading dock opens onto a street you have never seen.

| # | Choice | Check | Success | Failure |
|---|--------|-------|---------|---------|
| 1 | Repair the folding gear with the builders | Wits 9 | `kit_collaborator_credit_kept` (partial): the drawings get a visible credit list | Slower salvage: the puppet ships in pieces, the credit fight is still open |
| 2 | Negotiate the lease and credit | Rizz 8 | A written, enforceable month-to-month, not a sponsor's promise | Kit gets a short extension and a lesson in reading a clause |
| 3 | Clear a passage and help the neighbours | none, costs time | Kit chooses where the show goes; `kit_workshop_kept_public` (partial) | Neighbours get a stoop concert; Kit loses an hour but no one |
| 4 | Photograph the folded street | Psyche 7 | `evidence:folded_street_photo`, readable sober | Blurred; Pa Nhia's service log still records the glitch |

**Notes:** Kit's family and Hmong identity are texture and loyalty, not a power; cousin Pa Nhia is a working technician with his own opinions
about the sponsor. The 1885 Chinese expulsion is *not* part of this intro; it lives in its own sourced encounter.
**Close:** Stay / Follow / Decline; declining leaves Kit's number on the loading-dock whiteboard.

## 3. Juniper: "Honey and the Wrong Shape" (Stoned opening)

**Motivation:** protect one living place without lying to her human friends about why. She is unsure how much she can ask of them.

> A potluck under second-growth redwoods, string lights, a pot of something too fragrant to be soup. Juniper leans on a trunk with thrift-store
> flannel and a teasing smile, sorting who is hungry and who is lost without being asked. The ferns behind her have grown, in the last hour, into
> a spiral that no fern makes. "Huh," she says. "It's never done that for company."

| # | Choice | Check | Success | Failure |
|---|--------|-------|---------|---------|
| 1 | Measure the spiral and note the ferns | Local Lore 7 | `evidence:fern_spiral_measure`: repeatable, sober-reproducible | Partial notes; a potluck gardener supplies the missing numbers |
| 2 | Ask what the grove needs, not what it means | Rizz 7 | `juniper_habitat_verified` (first step): she names the real threat, a culvert and a cut line | She deflects with a joke and offers a smaller truth |
| 3 | Help carry the potluck leftovers to the neighbours' porch | none, costs time | She sees you do small work; trust, no secret yet | She says thanks and goes back to her grove alone |

**Notes:** Juniper may refuse to guide, argue, or proceed without you. Her nature is revealed only when she chooses, never by a drug effect
or a lucky roll alone; sober players see the same spiral and hear the same honest answer when she decides to give it.

## 4. Cedar: "A Line From Somewhere Else" (Tripping Balls opening)

**Motivation:** prove his CB tone is a real signal before anyone mocks it, and keep his parents' old argument from becoming his own.
He is a younger working rural local: boots, oil-stained jacket, tools in the truck, jokes about cosmic forces, an excellent memory for backroads.

> Behind the festival's rented stage, Cedar is on his back under a generator, swearing at a wire. His CB on the truck seat clicks twice and
> says, in a voice like his own, the name of a road that is not yet built. "That's not me," he says, "and I would like that noted."
> The player may be tripping. Cedar is not. He hands you a flashlight anyway.

| # | Choice | Check | Success | Failure |
|---|--------|-------|---------|---------|
| 1 | Log the broadcast with a tape recorder | Wits 7 | `evidence:cb_tone_tape`: same tone, same hour, sober-verifiable | A garbled tape, but his handwritten log still timestamps it |
| 2 | Ask what the tone reminds him of | Rizz 7 | He tells the one-line version of his parents: logger father, support-volunteer mother, one family, two ribbons | He jokes it off; the green ribbon is visible in the truck |
| 3 | Fix the generator with him | none, costs time | `cedar_modern_signal_checked` (first step); he stays practical, not mystical | He fixes it alone and respects that you tried |

**Fixed history, fixed boundaries:** Julia Butterfly Hill's tree-sit in Luna ran 738 days, Dec 10 1997 to Dec 18 1999, and ended with a protection
agreement. Cedar's mother is an *imagined* ground-support volunteer; no invented dialogue with Hill, no spiking accusations. His parents stay together
in every route. The future the CB hints at is a fictional modern signal, not a claim about real history.

## Re-encounters (anchor slots)

Each companion has one guaranteed re-encounter at chapter anchors, so no optimal arc depends on drawing a specific random card.

| Companion | If you followed first | If you declined first | Late-follow catch-up |
|-----------|----------------------|-----------------------|----------------------|
| Mara | She shows the client's *situation* and a second dated flash, then asks for your help with a copied-design complaint | She finds you through the table card; the dated pair is waiting | One short scene recaps her stakes and hands over the dated pair (sober parity) |
| Kit | The puppet street reappears; a sponsor's offer arrives and you help her reject the brand deal | Her loading-dock whiteboard note brings you to a co-op open house | A rehearsal montage and a fair-pay meeting replace the missed intro |
| Juniper | The grove's cut line is real; she asks for a human forum | The ferns have grown a second spiral by the culvert | She tells you the grove's problem in one dinner conversation |
| Cedar | The CB names a place that exists; he asks you to check a real worker-safety risk | His truck's log lists the places the tone has named | His mother and father both explain the ribbons at one table |

**Failure recovery:** a failed first-meeting roll yields an authored repair scene at the re-encounter, not a missing optimum.
**Persistent flags:** `evidence:*` item, `meeting_order`, `follow_history`, the *(new)* trust flags above, never reset by a mid-run perception change.

## Four optimism arcs: status

The four arcs live in COMPANION-OPTIMAL-PATHS.md; this task confirmed them consistent with the current cast and corrected Mara's section
(see the correction block there). Cedar's `parents_together` invariant is unchanged. No new endings or badge definitions are added.

## Open items for t-004 human creative review

- Kit's family surname/clan/dialect remain unassigned by design.
- Pa Nhia is a proposed fictional cousin; rename or cut freely.
- Cedar's father's specific heritage and his occupation details remain open.
