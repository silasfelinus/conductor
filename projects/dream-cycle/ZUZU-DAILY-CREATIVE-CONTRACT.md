# Daily Dream plus private Zuzu / Emperor catalog candidates

**Current direction, 2026-11-14 PT:** Continue the original complete six
linked Daily Dream records (PITCH world, LOCATION, Character, ITEM, SKILL,
Scenario), all sharing an independent daily world's visual style.

The Zuzu Gamebook and Emperor of Dust supplement is **four proposed objects**:
one setting/location and one character model per project. Store settings as
Kind Robots Dream LOCATION rows and character models as real Character rows.
Give each candidate explicit project attribution and its own registered
Arthemy/Illustrious ArtJob. Save candidates privately and without links to
the random daily Dream or either playable game's content. Do not make them
canonical or public until reviewed.

No new game concepts, branches, quests, moral decisions, scenes, follower
mechanics, reward records, scenario records, or playtest roster additions may
be authored or created through this sidecar. The two games are nearing finite
human testing; a perpetual game-content generator would move the finish line.

The **v4 contract** is original six assets plus
`zuzu_assets: { locations: [2], characters: [2] }`: ten Kind Robots records,
ten Facet target slots and ten durable ArtJobs, one existing transactional
writer with the original rollback and retry semantics. Version-3 14-asset
bundles remain readable as historical output but unbuilt v3 proposals do
not auto-execute. Do not mechanically link old candidate rewards/scenarios.

## Historical (superseded) contract

The former v3 sidecar required two locations, two characters, two rewards
and two moral-choice scenarios. That is historic background, **not** a
future instruction.

## Daily pitch direction (effective for newly authored dockets starting 2026-10-13 PT)

Five daily pitches, all **expansions of existing active projects**: new stages/fighters for Zuzu Showdown, acts/ships/characters for Rainbow Princess Bullet Hell, book sections or card sets for Zuzu Gamebook, Shifting Lands encounter/deck packs, new follower sets and dilemmas for Emperor of Dust, or levels/power-ups for Arcade games. Each carries a real `target` project slug, an `expansion_kind`, a content hook, art plan and actionable first slice.

An approval is **not intake** and **not authorization to publish**. It is a durable request for the next agent to prepare a **polished scope and actionable roadmap additions in that existing project's roadmap.yaml**, with milestones, dependency ordering, tests/acceptance, art, and `source_pitch: pitches/<date>-<slug>.md` for deduplication. Notes from Silas must be folded in. Never create a new conductor or Kind Robots Project for a post-cutover daily pitch. Preserve pre-cutover pitch decisions and intake history.


## Superseding five-daily-upgrades direction (2026-10-12 PT)

Effective for 2026-10-13 PT dockets, the five daily project entries are now
a **build-first delivery report**, NOT five concepts or five approvals to make
roadmaps later. The older daily pitch rules above remain historical.

Autonomous workers should implement five independent improvements to already
approved, active projects before review, preferring playable, tested, merged
features and producing art where possible. Real in-progress PRs can fill slots
that could not safely finish today, but a design spec or roadmap is not an
implemented feature. Never pad a docket with proposals.

Record five source-backed entries at
projects/dream-cycle/daily-deliveries/YYYY-MM-DD.yaml, including title, target,
kind, summary, status (shipped or in-progress), implementation PR, actual
GitHub Actions run, verification, and artwork status. Shipped requires a
full merge SHA and passing completed CI; in-progress requires a concrete
next step. Link playables, delivered image URLs and durable ArtJob IDs where
available. Run scripts/daily_project_deliveries.py --materialize and --check
to prepare review records and digest entries. An absent or invalid docket is
reported as missing, not fabricated.

The existing signed Kind Robots pitch inbox is reused for *after-the-fact*
Keep (approve), Modify (approve with changes), Reject (pass). Agent workers
read --feedback to action modifications or propose carefully verified,
reversible rollback PRs after rejection. Never directly destroy data.
This does not authorize outward-facing publishing, secrets, billing or
irreversible production changes. Preserve prior pitch votes and their
historical interpretation.

The unrelated daily creative pipeline still produces its original six linked
mini-world assets and eight separate Zuzu-world assets, not counted among
the five software upgrades.
