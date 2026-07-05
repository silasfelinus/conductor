# Da Vinci Ending Seed and Art Flow

## Decision

Da Vinci should not generate 1024 ending images through the normal `artPrompt` / live app generation path.

The app should store deterministic ending records, milestone links, achievement metadata, and prompt text. Actual icon and hero rendering belongs to the local art generator pipeline once that project is stitched together.

This keeps the database ready without burning local GPU time, cloud credits, or user-facing generation flows on a giant asset batch too early.

## What gets seeded now

Each of the 1024 endings should have stable database fields:

- `title`
- `slug`
- `outcomeKey`
- `summary`
- `victoryType`
- `icon`
- `heroImage`
- `artPrompt`
- `metadata`

Each ending should also map cleanly to:

- a `Milestone` record using existing milestone fields
- a `LifeAchievement` record of type `ENDING`
- later generated `ArtImage` records for icon and hero assets

The existing Milestone fields are enough for the first pass:

- `icon` for the achievement badge path
- `imagePath` for the larger ending image path
- `artImageId` once a generated image exists
- `artPrompt` for the generator prompt
- `triggerCode` for deterministic unlocks such as `davinci-ending-1011010110`

## Stable outcome key

Outcome keys use the 10-dimension order from `projects/davinci/data/ending-dimensions.yaml`:

1. legacy
2. wealth
3. love
4. wisdom
5. health
6. freedom
7. fame
8. creation
9. community
10. mystery

Each ending key is a 10-bit string. Example:

```txt
1011010110
```

That means:

- legacy passes
- wealth fails
- love passes
- wisdom passes
- health fails
- freedom passes
- fame fails
- creation passes
- community passes
- mystery fails

Do not reorder these dimensions after seeding without a migration plan. Reordering changes the meaning of every ending.

## Seed generator

The script lives at:

```txt
scripts/generate_davinci_endings.py
```

Generate all ending seed data as JSON:

```bash
python scripts/generate_davinci_endings.py --format json --output tmp/davinci-endings.json
```

Generate JSONL for easier importer streaming:

```bash
python scripts/generate_davinci_endings.py --format jsonl --output tmp/davinci-endings.jsonl
```

Generate a small local-generator image queue batch for a specific slice:

```bash
python scripts/generate_davinci_endings.py --format art-queue --offset 0 --limit 5 --output tmp/davinci-art-queue-0000.json
```

`--format art-queue` outputs two entries per ending: one icon and one hero. It does not save into `projects/art-generate.yaml` automatically. That is intentional. The generator operator should decide when to queue a batch.

## Local generator contract

The local generator should consume queue entries shaped like `projects/art-generate.yaml`:

```yaml
batch:
  entries:
    - id: davinci-ending-1011010110-icon
      source: davinci-ending-seed
      status: pending
      target_repo: silasfelinus/kind_robots
      image_path: public/images/davinci/endings/1011010110-icon.webp
      source_url: /images/davinci/endings/1011010110-icon.webp
      variant: icon
      size: "512x512"
      label: The Example Ending icon
      prompt: >
        Square achievement badge composition...
```

The generator should write files to `silasfelinus/kind_robots`:

```txt
public/images/davinci/endings/{outcomeKey}-icon.webp
public/images/davinci/endings/{outcomeKey}-hero.webp
```

Public app paths should omit `public`:

```txt
/images/davinci/endings/{outcomeKey}-icon.webp
/images/davinci/endings/{outcomeKey}-hero.webp
```

## Importer expectations

A future importer should be idempotent:

1. Upsert `LifeEnding` by `outcomeKey`.
2. Upsert `Milestone` by `triggerCode`.
3. Upsert `LifeAchievement` by `slug` or `conditionKey`.
4. Link `LifeEnding.milestoneId` to the milestone.
5. Link `LifeAchievement.endingId` and `LifeAchievement.milestoneId`.
6. Leave `iconArtImageId` and `heroArtImageId` null until real images exist.
7. Keep path strings populated immediately so the UI can use placeholders or missing-image flow.

Do not create 1024 `ArtImage` rows until the actual files exist. Empty image records make the gallery look more complete than it is, which is how databases learn to lie. Rude.

## First app-facing implementation after seeding

After the database entries exist, the next app slice should be:

- list locked/unlocked Da Vinci endings
- resolve an outcome key from a fake/test LifeRun
- unlock the matching Milestone and LifeAchievement
- show icon/hero paths even when the files are placeholders or missing
- add a missing-image request only for visible/current endings, not all 1024

That gives the game a playable spine without requiring the full art pipeline first.
