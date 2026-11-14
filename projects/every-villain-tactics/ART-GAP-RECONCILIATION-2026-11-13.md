# Every Villain Tactics art-gap reconciliation
**2026-11-13 PT | Source ledgers and game canon, not live preview acceptance**

Silas's correction: use the existing Conductor/ComfyUI art queue, not chat-generated
illustrations. The previous nine chat images were off-pipeline and visually repetitive;
none is represented as a game asset, an ArtJob or a substituted source image.

## Deduplicated baseline

| Type | Canonical slots | Previously rendered/requested | New private Comfy queue requests |
| --- | ---: | --- | ---: |
| Named playable Hero/Villain entrance scenes | 48×2 = 96 | 12 DONE First Bell reveal images (ArtJobs 68782–68793 / ArtImages 270741–270752); Contingency villain direct Prom painting available in `utils/cometAcademy/artManifest.ts` | **83** |
| Named, independent powered lieutenant portraits | 48 | Mags Hardpan already DONE on selected Unstable lane (ArtJob 50524 / ArtImage 257611) | **47** |
| Unique one-hit henchman crew plus captain ensemble introductions | 48 | Warren Wreckers style-check ArtJobs 50516–50518 and 56861–56863; some other model lanes DONE and the preferred Unstable lane had a PENDING receipt at last audit | **47** |
| **All new baseline requests** | | | **177** |

The 48 canonical playable signatures and actor appearances come from Kind Robots
`utils/cometAcademy/identityArcs.json` and Prom's
`art/IDENTITY-PORTRAITS-ROUND-1.yaml`. The 48 powered lieutenants are listed in
`projects/comet-city-academy/POWER-OPENINGS-LAIRS-AND-LIEUTENANTS.md`;
the **current runtime** 48-creature roster is in Kind Robots
`utils/cometAcademy/villainHenchmen.json`.

Three names in the older idea table disagree with the game roster.
The live crew names take precedence for new artwork: **Tadpole Interns**
(not Mabel's Biscuit Bots), **Quilted Doorstep Goblins** (not Gnome Revolt), and
**Clockwork Wombat Ronin** (not Honor Drones). The independently named lieutenants
stay as written in the approved 48-lieutenant slate. Preserve story coherence
without silently swapping a permanent hero identity.

## Source-backed unique composition

The requests deliberately replace the repeated low-angle arms-wide power pose
with character-specific physical tasks and asymmetric cinematic staging:
underwater rescue, kneeling beside victims, clockwork inspections, perched spies,
boardroom negotiations, fly-rail technicians, scientific repair work, seated
regents, and intelligent nonhuman crew behavior. Use continuity from canonical
student portraits and role-specific motivations, not a generic suit or new
random face for each variation. Each role has a different scene, action, camera
and emotional situation. The selected checkpoint remains
`SDXL/sdxlUnstableDiffusers_nihilmania.safetensors` in Comfy (28 steps, CFG 7,
DPM++ 2M), with distinct deterministic seeds.

### Queue entry points

- `art/FIGHTER-REVEALS-REMAINING-2026-11-13.yaml` — 83 genuinely missing
  hero/villain entrances, preserving direct Prom villain art where present.
- `art/POWERED-LIEUTENANTS-REMAINING-2026-11-13.yaml` — 47 distinct
  second-in-command portraits.
- `art/HENCHMAN-CREWS-REMAINING-2026-11-13.yaml` — 47 species/captain
  crew introductions, using their real silhouette, telegraphed trick and counter.

These ledgers specify `auto_submit: true` and `is_public: false`. **Merely merging
YAML is not submission**. Verify numeric `subjects[].jobs.unstable-production`
receipts from Auto Art Generate and record actual `ArtImage` status separately.
Queue requests one time only. Existing unfulfilled Warren Wreckers jobs must be
reconciled, not duplicated.

## Work still missing after these baseline images

The required individual captain story close-ups, unit-scale tactical standees,
telegraph overlays, hit/disarm reactions and other animated combat states are
separate asset categories, not magically satisfied by group introductions.
Likewise rendered `DONE` imagery is not delivery or visual acceptance: compare
each actor against canon, inspect composition diversity and hand/anatomy quality,
then attach the correct ArtImage to the game and test authenticated URLs at
phone/tablet/desktop widths. No game publication, live deployment or human
subjective acceptance is authorized by this queue.
