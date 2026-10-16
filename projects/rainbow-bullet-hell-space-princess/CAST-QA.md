# Cast Identity QA Contract
**Rainbow Bullet Hell Space Princess** · Conductor `t-016` · 2026-10-16 PT

This contract applies [CAST-BIBLE.md](CAST-BIBLE.md) to real ArtJobs. The per-pilot manifest is
[art/CAST-MANIFEST.yaml](art/CAST-MANIFEST.yaml): every shipped pilot asset, with its ArtImage, ledger entry, ArtJob,
engine, checkpoint, seed and source image, plus coverage of the bible's base deliverables. It was generated from the
`art/ART-ROUND-*.yaml` ledgers and the Kind Robots commits that shipped each file. It is docs only: no approved art
is overwritten by it.

## The contract: before a pilot asset or atlas is marked ready

An asset is **ready** only when every line below holds and is recorded in the manifest. Anything else stays
`proposed`.

1. **Manifest row.** It has a shipped path, ArtImage ID, ledger round and key, ArtJob ID, engine and checkpoint,
   seed, and source ArtImage for Kontext edits. The image must have been inspected after the job completed. A
   queued job, a `DONE` status or a URL is not inspection.
2. **Identity lock.** Each pilot's menu character ID portrait is the identity lock (`identity_lock` in the manifest).
   New pilot art is either a Kontext edit of the lock or of an asset already approved against it, or it is
   compared side by side with the lock before approval. Hair, skin tone, build, face shape and signature accessories
   must match the lock and the character sheet.
3. **Fixed links.** P1 Maribel is pink and flies Petal Wing (four-petal diamond). P2 Azure is cyan and flies Prism
   Lance (needle). P3 Solenne is yellow/gold and flies Halo Fin (double ring). P4 Vivi is lilac and flies Comet Crown
   (three-point star). An asset that swaps colour, ship or glyph between pilots is a reconciliation candidate, not
   a canon change.
4. **Silhouette.** Full-body art passes a monochrome silhouette test at 96 px and 256 px. The four bodies must read as
   short and compact, tall and long-limbed, broad and muscular, and rounded and curvy. To check honest size
   differences, the test must place all four against a shared height reference. Scaling each image to the same
   height does not test size.
5. **Build is kept through edits.** Kontext edits and rerolls must not slim Solenne's muscle or Vivi's curves, lighten
   skin, or flatten the four into one body type. This holds at sprite and cut-in scale as well as in portraits.
6. **No baked text.** No painted words, logos or gibberish lettering on clothing, screens or backgrounds, unless a
   deliverable asks for a specific legible word. Prompts must not ask for space for a title, since that makes
   Kontext paint gibberish (round 15).
7. **Group art.** Group art shows exactly the four pilots (plus Lilt-7 when asked for), each recognisable against
   their lock. Each must be in their own colour, with honest size differences. No one is relegated to the background.
8. **In-game previews.** Assets used in the cabinet are rendered in the engine at 390, 768 and 1440 px before they ship.
9. **Rights and provenance.** Record the model each asset came from. Pilot art so far is generated in-house through
   Kind Robots ArtJobs, using the Arthemy Western Art v3.0 Illustrious checkpoint and Flux Kontext dev (fp8). Before
   any public release, a human must confirm the licences of those models for commercial use. This QA pass did not
   verify them.
10. **Canon conflicts.** A departure from the bible goes into the reconciliation table below, with its reason, asset
    ID and approval status, before it replaces older frames. Superseded art is kept, never deleted.

## Shipped pilot assets (inspected 2026-10-16)

These are all derived from the lock, so identity holds across menu, comms and cut-in (contract line 2).

| Pilot | Menu ID (lock) | Comms portrait | Super cut-in | Ship sprite |
| --- | --- | --- | --- | --- |
| P1 Maribel | 246030 (r1, Arthemy) | 247448 (r9 Kontext from 246030) | 247644 (r14 Kontext from 246030) | 247486 Petal Wing (r9) |
| P2 Azure | 246031 | 247454 (from 246031) | 247649 (from 246031) | 247488 Prism Lance (r9) |
| P3 Solenne | 246032 | 247460 (from 246032) | 247803 (r22 Kontext from 246032; replaced 247652) | 247566 Halo Fin (r11) |
| P4 Vivi | 246033 | 247799 (r22 Kontext from 246033, clean tee; replaced 247466) | 247844 (r23 Kontext from 247799; replaced 247655) | 247492 Comet Crown (r9) |

### Identity findings

- **Maribel:** passes. The cropped copper hair, freckles, rose-pink jacket and rose badge hold across all three
  portraits and the round-8 turnaround (246426).
- **Azure:** the portraits pass, with the braid and undercut, cyan suit and gold coat. The round-8 turnaround
  (246432) reads correctly as tall and long-limbed, but its coat is olive green, not powder cyan. This fails
  line 3; see the reconciliation table.
- **Solenne:** the lock and comms portrait pass, with deep-brown skin, muscular arms, twists in an updo and gold
  armour. The cut-in (247652) keeps her face and colours but visibly slims her build, which is a line 5 flag. The
  round-2 turnaround (246157) passes.
- **Vivi:** the lock and cut-in keep the shaved side, lilac hair and holographic jacket. Her T-shirt carries gibberish
  pseudo-lettering in the lock (246033) and comms portrait (247466), which is a line 6 flag. The comms portrait and
  cut-in under-express her curvy build (line 5). The round-8 turnaround (246442) shows the curvy build and shaved
  side, but brown hair without the lilac streaks.
- **Ships:** all four links pass line 3. Prism Lance is a dark hull with cyan trim, which reads cyan at sprite
  scale; Halo Fin reads as a ring.

### Silhouette test (line 4)

The front poses of the turnarounds (246426, 246432, 246157, 246442) were reduced to black silhouettes at 96 px and
256 px. The four builds are distinct at both sizes: compact, long-coated and tall, broad with a hair bun, and curvy
through the hips. **Caveat:** each turnaround was scaled to the same height, so this pass does not test honest
height differences. A shared-reference lineup is still owed (see open work).

### Group art

All four existing group plates fail lines 2, 5 and 7: 246078 (r1b) and 246128, 246129 and 246130 (r2). They flatten
the body types, lighten or swap skin and hair, and two show five figures. None is canon. CAST-GROUP should be composed
by Kontext from the approved locks instead (the t-022 pass), and then checked against this contract.

## Reconciliation table

| Asset | Conflict | Reason | Proposed fix | Status |
| --- | --- | --- | --- | --- |
| 246432 Azure turnaround (r8) | Olive-green coat | Breaks the cyan fixed link | Kontext recolour to powder cyan, the same method as 247504 | approved: 247795 (r22) |
| 246442 Vivi turnaround (r8) | No lilac streaks | Bible: lilac/coral streaks | Kontext recolour, the same method as 247505 and 247506 | partial: 247798 (r22) fixes the front views; Kontext left the back view unchanged in r23 and r24, so r25 draws a fresh turnaround from 247799 |
| 246033 / 247466 Vivi lock and comms | Gibberish shirt lettering | Line 6 | Kontext edit to a plain or patterned tee; keep the shipped files until a clean take is approved | approved: 247799 (r22), shipped as the comms portrait in kind_robots#3772; the menu lock 246033 stays the identity reference |
| 247466 / 247655 Vivi comms and cut-in | Curvy build under-read | Line 5 | Reroll with explicit full hips and soft belly | approved: comms 247799 (r22) and cut-in 247844 (r23, from 247799), both shipped (kind_robots#3772, #3775) |
| 247652 Solenne cut-in | Slimmed build | Line 5 | Reroll from 246032 with explicitly broad, muscular shoulders and arms | approved: 247803 (r22), shipped in kind_robots#3772 and previewed in the engine at 390/768/1440 px |
| 246078, 246128–246130 group plates | Wrong cast, flattened bodies | Lines 2, 5 and 7 | Not canon; compose CAST-GROUP from the locks | rejected |
| 247744 (r19 C03 take 2) | Gibberish screen text | Line 6 | Use 247742 provisionally; reroll | rejected; replaced by 247809 (r22, no painted text) |
| 247801 / 247802 / 247808 (r22 Vivi cut-in and frustrated) | Shirt lettering again | Line 6 | Reroll from the clean-tee 247799 (r23) | rejected; replaced by 247844 and 247847 (r23) |
| 247857 (r23 Vivi helmet) | Shirt lettering (made from the old lock) | Line 6 | Reroll from 247799 (r24) | rejected; replaced by 247862 (r24) |

Approving a proposed fix needs the fixed asset to pass this contract and a reviewer sign-off in the manifest.
Shipped files stay in place until their replacement is approved.

## Open work (not ready)

- **Missing for all four pilots:** a six-frame action key animation and a colour/material callout. Helmet-on
  portraits passed for Maribel 247854, Azure 247855 and Solenne 247856 (round 23) and Vivi 247862 (round 24).
- The frustrated expression: round 22 passed Maribel 247805, Azure 247806 and Solenne 247807, and round 23 passed
  Vivi 247847. The cabinet draws one portrait per speaker today, so these are
  inventory until it shows expressions.
- A shared-height silhouette lineup of the four full-body turnarounds.
- Model licences for public release (line 9).
