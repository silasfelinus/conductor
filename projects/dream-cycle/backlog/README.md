# Dream Cycle backlog

This folder is the shared steering surface for daily proposals, legacy dream ideas, and delegated creation scheduler cards. The canonical daily-dream pipeline is documented in `../PIPELINE.md`.

## Three kinds of file

### Dated daily proposals

Files with `proposal: true` and `proposal_date` are the only files eligible to create daily-dream database objects. They contain exactly one vibe, one location, one Character, one ITEM Reward, one SKILL Reward, and one Scenario.

Their lifecycle is:

```text
outline / approved → built
                     ↘ pinned retry until the same builder succeeds
```

They do not use `status: building`. `scripts/build_dream_records.py` owns the complete transaction and is the only daily-dream object writer.

### Legacy dream ideas

Older `type: dream` files without `proposal: true` are idea inventory. They may supply a premise, image, or character seed when an agent authors a future dated six-asset proposal. They are never resumed as stage-by-stage API builds.

The Lantern Post file is parked as the record of the retired staged experiment. Its already-created production rows are retained, but no further stages may run from that card.

### Delegated creation scheduler cards

Types such as `coloring-book` keep their actual content in their home project. Their file here is only the scheduler and steering surface. A delegated playbook may use `status: building` across idle cycles, but it must keep the home roadmap synchronized and never double-claim a home task another Worker holds.

## Frontmatter

| field | values | meaning |
|---|---|---|
| `type` | `dream`, `coloring-book`, or another playbook-backed type | creation family |
| `proposal` | `true` for dated daily-dream proposals | eligible for the sole object builder |
| `proposal_date` | Pacific `YYYY-MM-DD` | steering day and digest date |
| `status` | `outline`, `approved`, `built`, `parked`, `vetoed`; `building` only for delegated types | queue state |
| `priority` | `low`, `normal`, `high` | Silas steering |

Slugs follow `../specs/SLUG-POLICY.md`. The proposal's world slug is the bundle through-line; the builder derives safe element slugs and art paths.

## Daily proposal authoring

Check and author through the validator:

```bash
python scripts/build_dream_proposal.py --check --fetch
python scripts/build_dream_proposal.py --brief
python scripts/build_dream_proposal.py --from-json proposal.json
```

Only one proposal may exist per Pacific date. Commit promptly after writing so concurrent agents see it on `origin/main`.

Queue selection for proposals is handled by the builder: pinned retries first, otherwise one eligible unbuilt proposal past its steering day. `parked`, `vetoed`, `built`, and substantive unincorporated Notes from Silas are skipped.

## Rules for agents

- Read `## Notes from Silas` before authoring or building. Fold notes into agent-owned content and never edit or delete Silas's Notes section.
- Never manually call daily-dream object endpoints from a backlog card. Fix or retry the sole builder.
- Never mark a partial API result as built. Trust the committed `built-data` ledger.
- Keep at least five useful dream ideas or active delegated scheduler cards available.
- New ideas must not intentionally duplicate existing kind_robots content, home-project sets, or backlog concepts.
- Art request definitions come from the builder and use stable unique IDs.

## For Silas

Leave notes in any file's `## Notes from Silas` section, change proposal priority, or set a proposal to `parked` or `vetoed`. You may also drop a bare premise as a legacy idea file. An agent will adapt a selected idea into a future dated proposal rather than creating objects directly from the rough outline.
