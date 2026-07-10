# Monster Recast

slug: `monster-recast`
status: concept-expanded
book-format: physical + digital coloring book
content-rating: progressive teen horror, approximately PG-13

## The concept

**Monster Recast** combines horror movies, gender bending, and camp. Classic horror and science-fiction lineages are recast through gender, presentation, body, age, scale, and theatrical framing while preserving the ugliness, menace, injury, and monstrosity that make horror work.

This is not a collection of thin models wearing gender-coded versions of monster costumes. Women may remain huge, muscled, burned, scarred, gaunt, old, ugly, ferocious, or barely conventionally feminine. Men may be decorative, vulnerable, beautiful, monstrous, or trans. Nonbinary characters and drag performers belong naturally in the cast. Gender is part of the idea, not a costume preset.

The collection is progressive, queer-positive, sex-positive, and gender-positive. It can be alluring and tastefully titillating, but it is aimed at a progressive teenage horror fan rather than an adults-only audience. Implied nudity, lingerie, swimwear, fishnets, bare legs, muscular bodies, scars, decay, and body horror are allowed; explicit anatomy, sexualized minors, sexual violence, and graphic gore are not.

The name works on three levels: movie casting, gender recasting, and recasting familiar monster ingredients into a new shared universe.

## Current concept pool

The second creative pass expands the project from a fixed 24-character outline into a **34-concept homage pool** plus six group-page seeds.

The pool includes:

- the Amazonian laboratory creation, woman Doctor Frankenstein, and Ivorian
- a dangerously alluring adult female dream killer who remains visibly burned
- the enormous muscular television man
- the disfigured woman lake killer masking up before tastefully obscured skinny dippers
- a genuinely ferocious she-wolf beneath an impossible moon
- Screwhead and her mechanical petaled sphere
- zaftig closet-carnival giant Pound Foolish
- a dapper female game doll
- Draculina and her three beautiful zombified husbands
- the severe hat apparition experiment
- a masculine alien hive king
- the female close-up shushing ventriloquist dummy
- a male haunted porcelain doll
- Ghostface-style bathtub self-care with a knife and comically short leg stubble
- the unraveling red-carpet mummy
- the amphibious creature sincerely doing drag
- a frightening feminine alien hunter
- the mature woman cannibal upright on her gurney
- a bald, ugly, skeletal female Nosferatu
- the conventionally curvy swimsuit model with a fully detailed fly head
- an invisible woman apparently flashing the viewer
- a young trans prom king standing unharmed in the ruined gym
- Babs O'Blob as performer, train, curtains, and engulfing mass
- the commanding female opera phantom
- the malevolent private-school girl with hidden 666s and treacherous pointy shadows
- Satan herself as a woman, not a demoness or succubus
- the teenage boy caught halfway into possession
- the backward bridge-walking adult male ghost
- the older woman murderous barber
- a mature Black woman mirror legend with bees and a hook, requiring strong originalization
- the unnaturally tall older woman mortician with silver spheres
- the middle-aged woman Shape behind suburban laundry
- the eerie hotel hallway boys
- the summoned female harvest vengeance monster

`homage-concepts.yaml` is the authoritative pool for the next concept-art round. It names source lineages internally so the cinematic idea and framing are not lost. Those source names are not the final commercial identities.

## Book shape

Do not lock the first edition at 28 illustrations yet. Rank the expanded pool after rough studies.

Working target:

- **28–32 solo or scene concepts**
- **4–6 duo, trio, or ensemble pages**
- **32–38 illustrated interior pages total**
- one separate full-color cover illustration

One illustration should sit on each right-hand page in print so marker bleed does not ruin another drawing. The page count may split into later volumes if the strongest concepts exceed a coherent first book.

## Canonical art workflow

The book is produced from a paired master system:

1. **Colored graphic master** — a finished high-detail horror illustration with thick black linework, flat bounded color, strong perspective, and many enclosed shapes.
2. **Coloring-page conversion** — the same composition translated faithfully into clean black line art, preserving pose, anatomy, identity, scene detail, and visual hook.

The colored pass is not merely reference art. It is the canonical composition and design master. The coloring page should look like the uncolored ink stage of that same artwork, not a separate simplified redesign.

See `STYLE-GUIDE.md` for the authoritative production standard, including:

- serious camp rather than joke-heavy novelty art
- thick outlines and flat color with no gradients or painterly haze
- dense but organized detail for teen and adult coloring
- anatomy, contact-point, prop-angle, and portal-perspective checks
- no accidental extra limbs
- one independent file per image, never a collage or contact sheet
- specific lessons for the laboratory creation, she-wolf, Broadcast Giant, Pound Foolish, bath ritual, and burned dream killer

## Approved-design preflight

Before generating, selecting, revising, or converting production art, run:

```bash
python scripts/coloring_approved_status.py --check
```

The preflight reads `approved/manifest.yaml`, scans every WebP physically present in `approved/`, and reports confirmed approvals, complete pairs, incomplete pairs, likely filename typos, and unmanifested files. The `Coloring approved preflight` GitHub Actions workflow runs this analysis automatically whenever the coloring-book project changes and publishes the inventory in the workflow summary.

Approval and exploration are intentionally separate:

- **Production:** reuse an approved colored master and its BW partner rather than starting the accepted design over.
- **Exploration:** keep the existing 34-pitch/four-variant queue in its current order, including concepts that already have an approved design.
- A later queued image for an approved concept is inspiration or an optional alternate; it does not replace the approved master unless Silas explicitly promotes it.
- Files in `approved/` that are not yet in the confirmation manifest are surfaced for review rather than silently treated as a new decision.

Current user-confirmed approvals are Freida Krueger, TV Boy, and Masking Up. The current filesystem also contains a complete Perfect Woman pair inside `approved/`; the preflight reports it separately because it was not part of the three approvals named in the 2026-07-10 direction. Masking Up currently has its color file under `inspiration/` and still needs its BW file and final move into `approved/`.

## Production sequence

1. **Creative direction** — use `CREATIVE-DIRECTION.md`, `STYLE-GUIDE.md`, and `homage-concepts.yaml` to lock tone, framing, body diversity, and concept hooks.
2. **Approval preflight** — run the approved-design report and preserve accepted production masters without altering the exploratory queue.
3. **Rough studies** — generate internal composition studies that may stay closer to the named movie lineage so the idea is readable.
4. **Ranking** — score each study for instant recognition, gender recast, horror, camp, originality potential, anatomy/perspective coherence, and coloring-page viability.
5. **Originalization** — replace protected expression with original names, biographies, masks, faces, silhouettes, costume systems, props, settings, and mythology.
6. **Colored masters** — generate and revise the finished thick-line, flat-color graphic illustrations for selected original characters and scenes, reusing approved masters where present.
7. **Selection** — choose the strongest composition and reject images with weak silhouettes, accidental mutation, impossible spatial logic, excessive jokiness, or copyright dependence.
8. **Character creation** — create a private Kind Robots `Character` entry for every original recurring figure who appears in the finished set.
9. **Coloring conversion** — translate the selected colored masters into detailed black line work without changing composition or character design.
10. **Book assembly** — build the digital set manifest, print-ready interiors, cover, credits, and storefront-ready package.
11. **Pause** — hold publishing and POD setup until the coloring app and digital storefront are ready.

Movie-still and traditional painted variants may remain useful staging or mood experiments, but they are secondary references. The production book is built from the colored-master/coloring-page pair.

## Originality guardrails

Every sellable piece should evoke a genre lineage without reproducing a protected character.

- Internal briefs may identify films, poster frames, and trope scenes to preserve the creative idea.
- Final art must not use actor likenesses, studio logos, exact masks, exact makeup, exact costumes, signature weapons, quoted text, or copied poster layouts.
- Change multiple major anchors: silhouette, face, anatomy, clothing era, color language, setting, prop, origin, personality, movement, and mythology.
- Public-domain and folkloric monsters allow closer archetypal treatment than modern franchise-specific masks, dolls, aliens, and slashers.
- Some rough studies may remain useful references but fail commercial originality review. Do not force them into the book.
- Prompts may describe broad periods, media, and public-domain movements. They should not request imitation of living artists or copyrighted studio styles.

## Visual direction

The final set should feel like one curated graphic-horror collection. Individual pages can vary in era, architecture, costume, and palette, but the production treatment remains consistent:

- thick clean black linework
- flat separated color areas
- hard-edged secondary color shapes instead of soft shading
- substantial graphic-novel detail
- bold poses and decisive camera angles
- clear enclosed regions suitable for later coloring
- no text, captions, labels, grids, panels, or collages
- serious menace with theatrical camp rather than slapstick

Historical and genre references may inform palette, costume, and production design, including Gothic portraiture, Expressionist stage design, creature-feature color, occult screen print, practical-effects spectacle, Victorian engraving, botanical and entomology plates, woodblock, linocut, and paper theatre. They should not replace the unified graphic-master treatment.

## Character data

`characters.yaml` remains the first-pass original-character seed bank and is shaped around the current Kind Robots `Character` fields where practical. It is not yet the final cast list.

After rough studies and ranking:

- retain strong existing originals
- add original identities derived from approved homage concepts
- remove or defer weaker concepts
- create private Character records only after copyright-distance review and final art selection

These are seed records, not production database writes. The later Character-import task should verify the current API and enum requirements, attach approved art, and only make Characters public when the book is ready for outward release.

## Files

- `CREATIVE-DIRECTION.md` — authoritative tone, rating, body-diversity, framing, and homage-to-original workflow
- `STYLE-GUIDE.md` — authoritative rendering, detail, anatomy, anti-collage, and colored-master conversion standard
- `homage-concepts.yaml` — 34 movie-lineage concept briefs and six group-page seeds
- `characters.yaml` — first-pass original recurring cast and Character seed bank
- `pages.yaml` — earlier 28-page draft; revise after ranking the expanded pool
- `approved/manifest.yaml` — user-confirmed approvals and explicit no-queue-suppression policy
- `approved/*.webp` — production-master inventory scanned by `scripts/coloring_approved_status.py`
- `art-modeler-request.yaml` — scene prompts
- `art-modeler-four-variant-request.yaml` — exploratory render matrix; production priority is now colored master followed by faithful line conversion
- `README.md` — product shape, workflow, and originality rules
