# Mandarin Tutor Art Direction v2

## Decision

v2 is a full visual reset for Mandarin Tutor, not a selective cleanup of v1.

Every core card whose manifest policy is `illustrate` should receive a new v2 render even if a v1 image already exists. Grammar/function/component entries may remain `glyph-only` when a decorative picture would teach the wrong thing. v1 assets remain historical and do not satisfy v2 coverage.

Canonical implementation lives in Kind Robots (`docs/mandarin-tutor-art-direction.md` and `server/utils/mandarinIllustrationManifest.ts`). This Conductor document records the coordination and rollout contract so autonomous art work does not drift back to the older generic style.

## House style

Art direction id: `modern-chinese-picturebook-v2`

Target character:

- modern Chinese educational picture-book illustration;
- hand-painted gouache with gentle watercolor and restrained ink-wash influence;
- matte pigments and subtle paper grain;
- clean silhouettes, deliberate simplification, limited detail, and generous negative space;
- natural asymmetry and quiet, believable lighting;
- one strong memory anchor or one compact scene.

The purpose is pedagogical clarity plus a distinctive authored visual identity. Avoid the highly polished, globally generic rendering habits that make generated images immediately read as interchangeable AI art.

## Chinese cultural grounding

Chinese flavor comes from believable lived detail when relevant: ceramics, foodways, kitchens, homes, markets, neighborhood streets, transit, textiles, bamboo and wood objects, furnishings, games, working environments, gardens, farms, and landscape.

Do not use cultural symbols as wallpaper. Pagodas, lantern walls, dragons, Great Wall imagery, calligraphy, red-and-gold festival dressing, or historical costume belong only when they are genuinely part of the vocabulary concept. Contemporary people should look like ordinary people in ordinary situations rather than costume-like ethnic shorthand.

Casino vocabulary should resemble a working table-game environment: plausible felt, chips, cards or tiles, payouts, cash handling, dealer gestures, and player interaction. It should not default to fantasy luxury or invented branded table text.

## Anti-synthetic-image rules

Prefer deliberate illustration decisions over maximal rendering. Avoid:

- photorealism and glossy CGI surfaces;
- plastic-looking skin;
- indiscriminate micro-detail;
- mechanically perfect symmetry;
- cinematic rim light, lens flare, bokeh, or neon glow used as filler;
- decorative clutter and impossible background objects;
- elaborate hand poses when a simpler pose teaches better;
- uncanny facial close-ups;
- impossible anatomy or object relationships.

A successful card should look as though an illustrator chose what not to paint.

## Text policy

Generated art contains no Hanzi, pinyin, English, Latin letters, numerals, pseudo-writing, labels, captions, readable signage, speech bubbles, logos, or watermarks. The tutor UI owns all written language.

## Durable identities

- recipe version: `v2`
- request prefix: `mandarin-tutor-v2-`
- canonical media root: `/images/mandarin-tutor/cards/v2/`
- engine: `krea2`
- size: `768x768`

Conductor validates the live manifest recipe and art-direction id before staging. v1 request ids and v1 media paths never suppress v2 requests.

## Submission policy

Once the self-hosted Kind Robots runtime exposes the v2 manifest, Conductor should stage every missing `illustrate` entry and submit the complete v2 corpus as durable ArtJobs up front. The home relay may render those jobs at its own safe pace. Submission should not require a human to return every forty cards and restart the queue.

Daily Dream remains higher scheduling priority. Mandarin curriculum art has priority 80 and should stay ahead of ordinary priority-0 repair/backfill traffic without starving truly time-sensitive work.

## Tutor behavior

The tutor loads only a manifest that reports recipe `v2` and art direction `modern-chinese-picturebook-v2`. For sourced cards it probes only the currently viewed deterministic v2 media path, displays the image when present, and otherwise keeps the Hanzi fallback. Manual core-card retries use the exact canonical v2 prompt from the server manifest; there is no generic browser-side prompt fallback.

Requested cards use the same v2 prompt builder. Existing requested cards with old art hide stale v1 image/job linkage; the next art action upgrades their stored prompt/version and submits a fresh v2 job.

## Quality rubric

A rendered card is acceptable only if:

1. the intended vocabulary meaning is obvious quickly;
2. it belongs visibly to the Mandarin Tutor house style;
3. its Chinese cultural grounding feels lived-in rather than decorative or stereotyped;
4. it avoids conspicuous synthetic-image tells;
5. it belongs comfortably beside hundreds of other cards in the same deck.

A failure is a regeneration candidate. It does not create another vocabulary edition.

## Per-card style variation — added 2026-08-28

The house style is fixed. The illustrator's decisions are not.

The original v2 recipe emitted identical style language for every card: any two prompts
were ~82% identical and 38 pairs were byte-for-byte identical. A corpus built from that
converges on one camera distance, one lighting setup, and one palette — which is the
interchangeable read this document exists to prevent, arriving through the recipe rather
than through the model.

Each card now also draws one option per axis — framing (6), light (5), palette (6), paint
handling (5), ground (4), 3600 combinations — from its own stable card token, the same
token that names its media file. Deterministic in both directions: a card's look is tied
to its identity, and the tutor's per-card retry rebuilds the prompt the batch was
submitted with. The draw ships in the manifest as `styleVariant` and on each staged
request as `style_variant`, so a weak render can be traced to a weak concept or a weak
style draw.

Canonical implementation: kind_robots `server/utils/mandarinIllustrationStyle.ts`, guarded
by `utils/scripts/verifyMandarinArtRecipe.test.ts`.

## The prompt contract is part of the art direction

Kind Robots enforces `server/utils/artPromptContract.ts` at the enqueue boundary, and it
rejected all 577 v2 prompts with HTTP 422. The recipe hedged the way a person writes —
"ground it in Chinese detail **only when** it naturally belongs to the concept" — and the
contract rejects conditionals because Krea 2 cannot evaluate one; it paints the densest
noun phrase it is handed. The corpus was unsubmittable from the day the recipe was
written, which is the actual reason nothing rendered, upstream of any container update.

Three rules the recipe now respects, all of which read as pedantic and are not:

- **No conditionals.** The recipe knows each card's categories and meaning, so it decides
  at build time and states one outcome. The cultural-shorthand exclusion is dropped
  entirely for a card whose concept *is* a dragon or a lantern.
- **No format nouns.** Not "flashcard illustration" — asking for a card renders a card,
  title bar and invented text included. The tutor owns the card.
- **No piled-up exclusions.** At cfg 1 the ComfyUI negative prompt is inert, so naming
  text fourteen ways and listing "lens flare, bokeh, neon glow" put all of it into
  *positive* conditioning. Same art direction, stated as the wanted result.

Any future edit to the house style has to keep passing that contract. The recipe test
asserts it card by card, per category, including the dragon case.

## Submission evidence — 2026-08-28

Recorded against the bar this document sets:

1. **Live manifest** returns recipe `v2` and `modern-chinese-picturebook-v2`. ✅
2. **Committed snapshot** (`art-manifest.json`) records 621 total, 577 `illustrate`,
   44 `glyph-only`. ✅ The snapshot is the manifest the submission was built from, produced
   by a local run of kind_robots#2174 via `queue_mandarin_tutor_art.py --manifest-file`,
   because Alexandria still serves the pre-fix recipe.
3. **Bulk submission**: 577/577 durable ArtJobs, ids 10291–10867, each recorded on its
   request as `last_art_job_id`. ✅ All 577 prompts unique; 537 distinct style draws.
   By 09:20Z the queue had drained and **all 577 were FAILED at attempts=3** on the render
   host, not on anything about the prompts. The requests and job ids survive in
   `art-prompts.yaml`, so requeueing after the mount is fixed is a required step, not an
   optional one — the corpus will not render on its own.
4. **Media under `/images/mandarin-tutor/cards/v2/`**: none yet. ❌ Blocked on the render
   host, not on the queue — see below.
5. **Tutor displays rendered v2 media**: not yet verifiable. ❌
6. **Visual QA sample against the rubric**: not yet possible. ❌

Coverage measured immediately before submission was **0 of 577**: every sampled v2 media
path answers 200 `text/html`, which is Nuxt's catch-all page rather than an image. The
tutor's probe used to treat that as a hit — fixed in kind_robots#2174.

**Remaining gate is the render host.** Alexandria's ComfyUI cannot see its model directory
(`VAELoader.vae_name='qwen_image_vae.safetensors'` absent from the live model list) and has
rendered nothing since 2026-08-27T09:04Z. The submitted jobs drain into that failure. This
predates the Mandarin submission and affects every project's art. Filed as
mandarin-tutor/t-020; recover with `scripts/drain_failed_art_backlog.py`, which canaries
before draining.

## Current rollout state — 2026-08-25

- Kind Robots PR #2095 merged: canonical v2 prompt recipe and house-style documentation.
- Conductor PR #2848 merged: full-corpus v2 staging and durable bulk ArtJob submission.
- Kind Robots PR #2096 merged: canonical v2 media appears automatically in the tutor; requested-card art upgrades to v2.
- The code-only production image containing the v2 manifest recipe has been successfully published to `ghcr.io/silasfelinus/kind_robots:latest`.
- Production is self-hosted on Alexandria/Unraid. The live `KindRobots` container must be updated to the code-only v2 image before Conductor can fetch `/api/mandarin/art-manifest` and submit the corpus.
- Keep schema-bearing Mandarin admin PR #2092 separate from this rollout. Its `MandarinCatalogOverride` / `MandarinCatalogChange` migrations should be deployed later as an explicit migration-bearing release, not accidentally bundled into the art-only update.

## Evidence required before calling v2 art launched

Do not infer success from a green fail-open workflow step. Record all of the following:

1. the live self-hosted manifest returns recipe `v2` and the expected art-direction id;
2. the committed Conductor snapshot records total, `illustrate`, and `glyph-only` counts;
3. bulk-submission logs report the actual number of v2 ArtJobs submitted and their job ids;
4. self-hosted media begins appearing under `/images/mandarin-tutor/cards/v2/`;
5. the tutor displays rendered v2 media without manual refresh;
6. a representative visual QA sample across several categories passes the rubric above.
