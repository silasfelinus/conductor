# Zuzu: Koala Assassin — World Registry

**Start here for every Zuzu production.** This is the shared directory for the comic,
trailer, animated film, Lair, Showdown, arcade and gamebook, as well as concept art,
character-LoRA datasets, and Kind Robots model resources.

Machine-readable index: [catalog.json](catalog.json) · Contribution rules: [CONTRIBUTING.md](CONTRIBUTING.md).
This world index is **not** a new Conductor project or a second Kind Robots database.
Every production keeps its own roadmap, code, runtime assets and ownership.

## Read the canon before creating anything

The current sources live in the comic's existing issue folder; **do not move or copy them**.
Read the following in order of relevance:

1. [BOOK-ONE.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/BOOK-ONE.md) — **current story of record** for Book One.
2. [CAST-PICKS.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/CAST-PICKS.md) — selected designs, latest angle decisions, and ArtImage IDs.
3. [VIDEO-GUARDRAILS.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/VIDEO-GUARDRAILS.md) — art style, safety and prompting rules; consult the actual document for its restricted terms.
4. [BRAINSTORM-ROUND-3.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/BRAINSTORM-ROUND-3.md) — revisions that supersede early drafts.
5. [SERIES-BIBLE.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/SERIES-BIBLE.md) — earlier world sketch, **not authoritative** where revised.
6. [ISSUE-01-SCRIPT.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/ISSUE-01-SCRIPT.md) — archived draft, replaced by Book One.

**Important:** Early Kind Robots Dream/Scenario lore is a *springboard*, not confirmed comic canon.
In particular, do not quietly reinstate superseded locations, supporting characters or story
devices from the draft series bible. Keep the concealed plot reveal out of public titles,
metadata, prompts, descriptions and this index. Read the restricted list from the original
guardrails at generation time rather than replicating it into catalogues.

The original graphic-novel continuity remains fixed. Branching-game outcomes, match victories,
QTE deaths and arcade mechanics are alternate-play interpretations, **not retcons**. The comic
may be mature; the fighting game's lighter tone and the gamebook's alternate route follow
their own [project briefs](#productions).

## Productions

| Production | Canon relationship | Project source |
| --- | --- | --- |
| Comic / Book One | Canonical story | [Comic issue folder](../../projects/comic-creator/issues/zuzu-koala-assassin-01/) |
| Title music video / trailer | Adaptation | [Music Video](../../projects/music-video/DESIGN-BRIEF.md), [video guardrails](../../projects/comic-creator/issues/zuzu-koala-assassin-01/VIDEO-GUARDRAILS.md) |
| Animated episode / film | Selective adaptation | [Comic Film](../../projects/comic-film/DESIGN-BRIEF.md) |
| Zuzu's Lair | Separate QTE adventure | [Lair](../../projects/zuzu-lair/DESIGN-BRIEF.md) |
| Zuzu Showdown | Noncanonical versus matchups | [Showdown](../../projects/zuzu-showdown/DESIGN-BRIEF.md), [fighters](../../projects/zuzu-showdown/fighters.yaml) |
| The Bell That Never Rang | Alternate-trail RPG | [Gamebook](../../projects/zuzu-gamebook/DESIGN-BRIEF.md) |
| Zuzu: Ghost Trail | Arcade spinoff | [Arcade game queue](../../projects/kr-arcade/games.yaml) (slug `zuzu-ghost-trail`) |

Projects share *world references*, not tasks or implementation ownership. Each project
still owns its own code, assets, decisions and human publication gate.

## Shared characters, art and model assets

- **Character sheets & chosen images:** [CAST-PICKS.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/CAST-PICKS.md);
  the [catalog](catalog.json) provides a few verified `ArtImage` IDs as searchable pointers,
  not duplicates of the images or a claim that every old pick is still the latest.
- **Character LoRA specifications:** [LORA-SETS.yaml](../../projects/comic-creator/issues/zuzu-koala-assassin-01/LORA-SETS.yaml)
  and [expressions](../../projects/comic-creator/issues/zuzu-koala-assassin-01/LORA-EXPRESSIONS.yaml). These are *dataset specifications*.
  A completed training run and an imported Kind Robots `Resource` must be verified independently.
- **Canonical house art lane and prompt rules:** [VIDEO-GUARDRAILS.md](../../projects/comic-creator/issues/zuzu-koala-assassin-01/VIDEO-GUARDRAILS.md).
  Production-specific frame formats and sprite rigs remain project-owned.
- **Kind Robots runtime models:** `Character`, `Scenario`, `Reward`, `Resource`,
  `ArtImage`, `Dream` and `Project` are the live source records. The catalog's
  `runtime_model_discovery` entries are **lookup instructions**, not assertions that
  matching rows have been verified. Prefer stable row IDs after verification and
  existing `Project.conductorSlug` for project joins. Never create a duplicate row
  simply to fill an empty catalogue slot.

## Cross-project production contract

1. **Read** this index, Book One, Cast Picks, the Guardrails, then the owning project brief.
2. **Resolve** needed Character, Reward, Scenario, Resource and ArtImage records from
   Kind Robots. Confirm identity, provenance, permission and latest accepted visual pick.
3. **Reuse** the existing asset/model by ID or canonical source path. Record source `ArtImage`,
   `ArtJob`, Resource ID, checkpoint, LoRA trigger and image rights in the production's
   normal provenance fields. Avoid mirrored binary files and parallel truth tables.
4. **Produce** in the owning project's pipeline and ledger. Do not centralize gameplay
   logic, creative branches, project milestones or GPU job queues here.
5. **Propose** new canon, a cast change or a newly approved asset via a scoped PR updating
   the *true owner first* (usually Book One, Cast Picks or the Kind Robots record), then
   update this catalogue and affected consumers. Unreviewed production invention is
   not automatically promoted into the shared world.
6. **Keep visibility honest:** a source-defined LoRA is not a trained `Resource`;
   an ArtJob queued is not an image delivered; a concept is not a locked design.
   Follow project-level human gates before publishing externally.

This registry can be consumed from GitHub immediately by Conductor agents. A Kind Robots
admin resource browser with live database joins is an **additional integration**, not
implemented by this index; do not advertise this static catalogue as a live DB view.
