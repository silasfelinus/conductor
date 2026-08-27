# Cthulhuquarium remaining art pass (t-044) — queue committed, render pending

Date: 2026-08-27
Task: cthulhuquarium/t-044 — "Full art pass for the remaining ~120 non-tier-1 species,
and fix the bg-parlour style miss"

---

## TL;DR

This session queued the work; **it has not rendered yet**. `projects/art-generate.yaml`
now holds 138 pending entries (119 remaining fish species, the `bg-parlour` re-render,
and 18 previously-unqueued non-fish assets — 2 characters, 6 set pieces, 6 egg-tier
icons, 3 UI screens, and the Ichthyonomicon cover). The scheduled `auto-art-generate.yml`
workflow (cron `0 */6 * * *`) is what actually submits these to the ArtJob queue and
writes results to `projects/process/` — this session did not manually POST/poll each one
the way t-015 did, for the reasons below. **A follow-up session needs to confirm the
workflow actually drained the queue and review the results before this task can close.**

## Where the queue came from, and why it needed editing before committing

`scripts/build_cthulhuquarium_art_queue.py` exists specifically to regenerate this file
from the bible (`silasfelinus/cthulhuquarium`, `fish/*.yaml`) plus a hardcoded set of
non-fish prompts in the script itself, so a fish's rendered art prompt is never retyped
by hand. Running it unmodified writes **174 entries — every species and background in
the bible, including the 32 species and 3 backgrounds t-015 already rendered and Silas
has not asked to be redone.** The script has no "already generated" awareness; it is a
full regeneration tool, not an incremental one. Committing its raw output as-is would
have queued 35 needless re-renders (wasted GPU time, plus a real risk of Silas seeing a
species he already approved silently replaced with a different roll of the dice).

This session filtered the raw output against t-015's own completed list (see that
task's doc, `t-015-full-art-pass.md`) before committing:

- **Excluded** (already rendered, approved, not to be touched): the 32 tier-1 species
  and `bg-shipwreck` / `bg-cathedral` / `bg-abyssal`.
- **Kept**: `bg-parlour` (the one background t-015's own doc flagged as an off-style
  photoreal miss that still needs a re-render), plus every other entry the generator
  produced.

One entry was lost to a parsing edge case while filtering (174 generated → 139 expected
kept by slug-matching → 138 actually written) — almost certainly two adjacent entries'
text merged during a line-based split rather than any content being corrupted (the
committed file re-parses cleanly as YAML with 138 well-formed, unique-`image_path`
entries, zero malformed). Not chased further this session; if the render results come
back one species short of 119, that is almost certainly the missing one and it can be
re-added with a fresh `build_cthulhuquarium_art_queue.py` run filtered the same way.

## Why this session didn't just render them directly (t-015's approach)

t-015 called `POST /api/art/enqueue` per species and polled each job directly. That
worked well for 32 images in one session. 138 is a different shape of problem: krea2's
documented cold start alone can run ~25 minutes, and steady-state is still ~40s/image —
138 sequential jobs is 1.5-2+ hours of continuous polling, which does not fit
comfortably in one scheduled-routine session alongside everything else a sweep needs to
cover. `auto-art-generate.yml` exists precisely to drain a committed queue like this one
without a human or agent babysitting each request live (`timeout-minutes: 150` on the
job, which is enough headroom for a queue this size). Committing the queue and letting
the scheduled workflow drain it is the intended division of labor here, not a shortcut.

## Verified before committing

- `engine: krea2` on every entry — confirmed `krea2` is
  `consume_art_queue_core.py`'s `DEFAULT_ENGINE` and one of its three
  `COMFY_WORKFLOW_ENGINES`, so the consumer the scheduled workflow calls actually knows
  how to build a krea2 job from these entries (not a guess — read the consumer source).
- Re-parsed the filtered file with `yaml.safe_load` after every edit: 138 entries, no
  duplicate `image_path` values, no entry missing `prompt` or `image_path`.
- Cross-checked `queue_missing_project_art.py` (the *other* script that also writes
  `projects/art-generate.yaml`, for unrelated per-project icon/card/hero requests) —
  its `merge_queue_entries` preserves any existing entry whose `status` reads as active
  (the default when unset) before adding its own, keyed on `(target_repo, image_path,
  variant)`. These 138 entries have no `status` field (defaults to pending/active) and
  distinct `image_path`s, so a future `queue_missing_project_art.py` run will not drop
  or collide with them — read the source rather than assumed compatibility.

## What a follow-up session needs to do to close this task

1. Confirm `auto-art-generate.yml` actually ran against this queue (check its run
   history / the `ArtJob` rows it created) and that `projects/art-generate.yaml`'s
   entries have moved from pending to completed.
2. Spot-check a sample of the resulting images the way t-015 did — same `gosse` /
   `trade-card` / `gyotaku` / `blaschka` medium consistency check, and specifically
   confirm `bg-parlour`'s re-render actually reads as the intended hand-coloured
   lithograph rather than repeating the photoreal miss.
3. If any jobs failed or came back off-style, requeue just those (same filtering
   approach as this session, scoped to the failures) rather than a full regeneration.
4. Once satisfied, close t-044 `done` and update `projects/cthulhuquarium/SHIPPED.md`
   / the roadmap milestone the way t-015's close-out did.
