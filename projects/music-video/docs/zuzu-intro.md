# Zuzu: Koala Assassin intro: creative brief and settings (music-video t-024)

Requested by Silas, 2026-10-04. Written 2026-10-06. This is the input to t-028 (run the builder) and t-029
(render and verdict). Canon comes from `projects/comic-creator/issues/zuzu-koala-assassin-01/`:
`BRAINSTORM-ROUND-3.md` (source of truth), `VIDEO-GUARDRAILS.md`, `BOOK-ONE.md`, `CAST-PICKS.md`.
Where this brief and those disagree, they win.

## Pitch

A 55-second title-sequence for *Zuzu: Koala Assassin*, a mature weird-western about a koala ronin
crossing a dying wasteland with two starving fennec-fox orphans. A samurai in a western: dust, a poncho,
a wide kasa shading the eyes, a katana across the back. The intro makes a promise of mood, not plot: lone
figure, long road, a world that has been beaten down, a hard stillness, then the title.

## Format

| Field | Value |
|---|---|
| Length | 55 s (inside the 45 to 60 s ask), about 22 beats at 100 BPM |
| Aspect | 16:9, 1280x720 export |
| Voice | Instrumental, with at most a sparse low group chant (no lyrics a viewer could read as dialogue) |
| Words on screen | A title card only: `ZUZU` / `KOALA ASSASSIN`. Diegetic signs and posters are allowed; no captions, no narration |
| Rating | Mature. Menace and violence may be implied or shown; see Children below |

## Genre and mood

A samurai-western title theme: slow, dusty and ominous, building to a hard final hit. Think lone
whistle-less spaghetti-western tension crossed with shakuhachi and taiko, never comedic, never cute.
Zuzu is always serious (Clint Eastwood stillness).

Arc by time:

| Time | Beat | Music |
|---|---|---|
| 0:00-0:10 | Cold open: wind over dunes, a hat brim, a dusty poncho | Drone, sparse shakuhachi, no drums |
| 0:10-0:25 | The road: Zuzu walking, the small fennec shapes behind him | Slow twangy guitar enters, taiko heartbeat |
| 0:25-0:42 | Menace: a one-eyed coyote at a waterhole, the shadow of the crocodile, sand shifting | Taiko builds, low chant on the beats |
| 0:42-0:50 | The draw: hilt over the right shoulder, a single beat of stillness | Everything drops, one held note |
| 0:50-0:55 | Title card on black with dust | One hard taiko and guitar hit, ring out |

## ACE-Step settings

Model and graph per `ace-step-spike.md` (ACE-Step 1.5 turbo, split files). Pitch row:

- **durationSeconds:** 55
- **bpm:** 100 (a 4/4 grid gives 22 bars of beat targets for the timeline)
- **key:** D minor
- **seed:** 31 (the spike default; change only for a re-roll, and log the new seed)
- **lyrics:** `[Instrumental]` (the spike marks which of `[Instrumental]` or an empty string behaves
  better as UNVERIFIED; t-012 decides. If a chant is wanted, use `[Verse 1]` with three or four vowel
  syllables only, for example `ha, ho, ha, ho`, never a word.)
- **tags** (prose, genre first, as the template wants):

```
cinematic samurai western title theme, instrumental, slow and ominous, dusty desert atmosphere,
shakuhachi flute, twangy baritone electric guitar with spring reverb, deep taiko drums, low
throat-chant drone, sparse arrangement, building tension, 100 bpm, D minor, dramatic final hit,
no vocals, no lyrics
```

Negative: leave the template's `ConditioningZeroOut` negative as is.

## Style bible (visuals)

Use as `settings.styleBible`:

```
A mature graphic-novel weird western. Dark, gritty and desaturated, more Tarantino than Disney: dust-
brown and rust palette, hard sidelight, long shadows, a pale smoky sky, a few orange accents (the
sash, the sun). Painted western-comic linework in the Arthemy Western Art house style. Slow, heavy
camera: low angles, wide landscapes with a small figure, tight shots of eyes under a hat brim, hands
and boots. Action over exposition, no dialogue, no narration. Every character is an animal.
```

Canon in every character shot (from `VIDEO-GUARDRAILS.md`):

- **Zuzu:** koala-sized and stocky (Danny DeVito proportions: short, barrel-chested, short legs, a slight
  paunch), always serious. Rust-brown poncho with orange zigzag trim, conical straw kasa shading his eyes,
  dark tunic, orange sash, dark brown cloth trousers. Katana sheathed diagonally across his back, hilt over
  the RIGHT shoulder, scabbard tip at the LEFT hip; from behind the whole scabbard shows. Negate
  `straw boater, cowboy hat, cloak, cape, tall, lanky`.
- **Siblings:** fennec foxes, a gaunt sister of about ten and a toddler brother. Starving, beaten,
  frightened; claw-torn rags.
- **Coyote:** destitute, sick and poor but never skeletal; eyepatch on the RIGHT eye, revolver on the
  RIGHT hip, empty hands in the shot unless the keyframe says otherwise.
- **Crocodile:** erupting from the oasis (only as a shadow, a swell of water and teeth, never lingering).
- **Otter abbess and nuns:** short otter snout, a convent wall; optional single cutaway only.

## Children (absolute)

The siblings may be shown scared, starving and hunted. Never sexualised, never undressed, injuries
implied rather than detailed. The intro keeps them small, distant or turned away; the road shot is the
only one where they are the subject.

## Comic lane routing

| Setting | Value |
|---|---|
| `comicSeriesId` | the Kind Robots ComicSeries with slug `zuzu-koala-assassin` (look up the id by slug at run time) |
| `comicLaneKey` | the series' house lane, Arthemy Western Art v3.0 (`arthemy-western` in `projects/comic-creator/docs/checkpoints.md`); confirm the exact key in `utils/comicLanes.ts` before the run |
| Engine | The comic house lane wins over Krea 2 for this video (t-025): Illustrious Arthemy, the lane's prefix and suffix plus the series negatives, **tag-style prompts**, not prose |
| Clip motion prompts | Prose: one camera move plus one action. No art-direction jargon |

Words the image models draw literally (keep out of positive AND negative prompts): "duster" (say "long
riding coat"), "mother" (say "abbess"), "muzzle" (describe the snout), "squat" (say "chubby, standing
upright"), "ribs showing" (say "thin, sickly, underfed", negate `ribs, ribcage, skeleton`), "sea otter".

## settings.bannedTerms

Copy exactly (from `VIDEO-GUARDRAILS.md`, which is the single source for this list). The server refuses
any scene, LLM or clip prompt containing one, on every engine. This list covers the comic's secret
(comic-creator t-019); the secret itself is not written here or in any prompt.

```
human, humans, humanity, mankind, people, pharmacy, great wall, skyscraper, highway,
billboard, road sign, english lettering
```

Also keep out of every positive prompt, title and chant syllable: "people" (say "townsfolk" or name the
species), and the v0 Kind Robots world (Gallowsun Junction, the Stationmaster, Tomoe, Old Shelba,
contract-language). Statues and ruins are allowed as ordinary western sets, never with a giant figure
or lettering.

## Keyframes: vetted comic attempts

Character shots start from vetted attempts (verdict selected, then liked) via
`POST /api/music-video/[id]/scenes/keyframes`, not fresh renders. From `CAST-PICKS.md` and the
comic-creator t-015 ledgers (ArtImage ids; check each is still selected in the studio before assigning,
and prefer a newer selected attempt if one exists):

| Use | Character | ArtImage | Note |
|---|---|---|---|
| Hero, title and draw shots | Zuzu final (R6) | 241913 | rust poncho, kasa, katana on the back |
| Front half angles | Zuzu | 241919 (front), 241920 (3/4 left), 241921 (profile left), 241925 (profile right), 241926 (3/4 right) | Kontext keepers; check against the sword rig |
| Road shot | The sister (S2) | 241879 | long torn pale dress |
| Road shot | The toddler (T2) | 241883 | checked tunic |
| Waterhole | The one-eyed coyote | 242435 (stump bandaged pick), else C1 241888 | prefer the newest selected coyote |
| Waterhole | The crocodile (K2) | 241893 | erupting from the oasis; shadow only |
| Optional cutaway | Otter nuns (N2) | 241895 | |
| Wide road | Scene X4 | 241899 | chapter 11, the road |

Back views are the known weak spot (the katana must be plainly across the back); use a back keyframe only
if one has a selected verdict, otherwise stay frontal or in profile.

## Shot list (22 beats at 100 BPM, scene changes on bars)

Scenes use Ken Burns by default. **At most 6 beats get a real ltx or wan clip** (each takes 30 to 90
minutes on the single 12 GB card, so t-029 queues them overnight). Clip beats are marked C.

| # | Time | Shot | Source | Motion |
|---|---|---|---|---|
| 1 | 0:00-0:05 | Wind-blown dunes at dawn, empty frame | fresh still | slow push in |
| 2 | 0:05-0:10 | Close on a hat brim, eyes in shadow | keyframe Zuzu R6 crop | tilt up |
| 3 | 0:10-0:15 | Wide: tiny Zuzu walking a ridge | X4 or fresh still | Ken Burns pan |
| 4 | 0:15-0:20 | Boots and poncho hem in dust | fresh still | Ken Burns |
| 5 | 0:20-0:25 | Two small fox silhouettes follow behind (distant, turned away) | S2 and T2 keyframes | pan across |
| 6 C | 0:25-0:29 | Waterhole at dusk, the coyote's one eye in the dark | coyote keyframe | clip: slow dolly in |
| 7 | 0:29-0:33 | A revolver on a right hip, a hand hovering | fresh still | Ken Burns |
| 8 | 0:33-0:37 | Water bulging; a long shadow beneath | K2 keyframe | Ken Burns |
| 9 C | 0:37-0:42 | Sand erupts, teeth and spray | fresh still | clip: sudden burst, camera shakes |
| 10 C | 0:42-0:46 | Zuzu stops, wind in the poncho | Zuzu R6 front | clip: slow push-in on the brim |
| 11 C | 0:46-0:50 | Hand rises to the hilt above the right shoulder | Zuzu 3/4 left keyframe | clip: hand closing on the hilt |
| 12 C | 0:50-0:53 | Blade flash cut to black | fresh still | clip: single light streak |
| 13 | 0:53-0:55 | Title card `ZUZU` / `KOALA ASSASSIN` over dust | text over still | fade in |

Beats 1 to 13 are the editable list; the timeline needs only to land cuts on the bar lines of the 100
BPM grid (one bar is 2.4 s). The title card is rendered by the exporter's text overlay; if there is no
overlay by t-029, use a flat generated title still made through the house lane with the words as the
image's only text (keep the word `human` and every other banned term out of it).

## Acceptance (t-029 FOR SILAS note)

Character fidelity to the comic (poncho, kasa, sword side, koala proportions); cuts on beats; the title
card; no banned term anywhere in prompts, lyrics, titles or captions; the mood reads as serious, never
cute; the siblings are never sexualised or detailed in injury.

## Open items for t-028 / t-029

1. Confirm the exact `comicLaneKey` for Arthemy in `utils/comicLanes.ts`.
2. t-012 decides `[Instrumental]` versus an empty lyrics string.
3. If t-012 is not done when t-029 runs, ask Silas for an MP3 and use the t-013 upload route, keeping
   the 55 s length and the 100 BPM grid for the timeline.
