# Monster Recast color-art queue

## What is queued

Run:

```bash
python scripts/queue_monster_recast_art.py
```

The script expands the current Monster Recast source package into independent full-color jobs:

- one job for each entry in `sets/monster-recast/characters.yaml`
- one job for the cover in `sets/monster-recast/pages.yaml`
- one job for each page composition in `sets/monster-recast/pages.yaml`

With the current v1 files this is **53 separate images**: 24 character concepts, 28 page-source scenes, and 1 cover. Every entry explicitly says one scene, one image, no collage, no contact sheet, and no comic panels.

The generated files are targeted to:

```text
projects/coloring-book/sets/monster-recast/generated/color/characters/
projects/coloring-book/sets/monster-recast/generated/color/pages/
projects/coloring-book/sets/monster-recast/generated/color/cover/
```

The queue is safe to regenerate: the script replaces only existing entries whose `project` is `coloring-book` and whose `set` is `monster-recast`; unrelated jobs remain in place.

## Which path is canonical?

The two project-level art YAML files are related, but they are not two competing sources of truth.

### `projects/art-prompts.yaml`

This is the **durable prompt catalog**. It stores reusable project icon/card/hero prompts, inspiration requests, and site-wide missing-image requests. Humans and tooling may edit this file. It is the long-lived source for project-asset requests.

### `projects/art-generate.yaml`

This is the **executable batch queue** consumed by `scripts/consume_art_queue.py`. It should be treated as generated/ephemeral: each entry is one concrete render job with a destination path, size, engine settings, and prompt. It is not the place to maintain the master copy of dozens of Monster Recast pitches.

### Monster Recast source files

For this set, the durable pitch sources are already more specific than `art-prompts.yaml`:

- `sets/monster-recast/characters.yaml` owns character designs and `artPrompt` values.
- `sets/monster-recast/pages.yaml` owns the cover and page compositions.
- `scripts/queue_monster_recast_art.py` converts those sources into individual `art-generate.yaml` jobs.

This avoids duplicating 53 evolving prompts into a second catalog while still giving the generator one independent job per image.

## Redundancy verdict

Neither YAML file should be deleted:

- deleting `art-prompts.yaml` would remove the durable project-asset request catalog;
- deleting `art-generate.yaml` would remove the concrete queue contract used by the autonomous generator and image distributor.

The redundant part was the old manual instruction that treated `art-generate.yaml` as something a person maintained or copied into ChatGPT. The clean pathway is now:

```text
canonical prompt source
  -> queue script
  -> projects/art-generate.yaml
  -> scripts/consume_art_queue.py
  -> projects/process/
  -> scripts/distribute_images.py
  -> final destination
```

For ordinary project icon/card/hero work, the canonical source is `art-prompts.yaml` and the builder is `queue_missing_project_art.py`. For Monster Recast, the canonical sources are the set YAML files and the builder is `queue_monster_recast_art.py`.
