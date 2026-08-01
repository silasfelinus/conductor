#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "projects" / "dream-cycle" / "roadmap.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "_register-daily-dream-digest-task.yml"
SELF = Path(__file__)

TASK = r'''

  - id: t-022
    milestone: m4
    title: Make the daily dream bundle facet-seeded, date-correct, and art-complete
    status: ready
    owner: null
    passes: 0
    stakes: reversible
    updated: '2026-08-01T02:14:00Z'
    note: >
      Silas-directed 2026-07-31. Fix the daily digest so “yesterday” means the
      prior Pacific calendar day instead of the newest successful historical
      build, and replace the tiny attached-only strip with a readable gallery
      covering every known asset for today and yesterday with honest queue,
      rendered, and attached states. Change future daily output to exactly one
      dream vibe, one dream location, one Character, one ITEM Reward, one SKILL
      Reward, and one Scenario. Seed the umbrella vibe from two weighted random
      GENRE Facets, one random ANIMAL or SPECIES Facet, and one random
      OCCUPATION Facet; give dependent elements one additional GENRE plus
      applicable Facets such as MATERIAL and species; build the Scenario last
      from the completed vibe, location, and Character. Persist the selected
      seed Facets in proposal and built metadata, attach them through the real
      per-model Facet assignment endpoints, expose them in the digest, remix
      eligible unbuilt proposals into the new contract, and verify art requests
      exist for all six created assets.
'''

text = ROADMAP.read_text(encoding="utf-8")
if "  - id: t-022\n" not in text:
    ROADMAP.write_text(text.rstrip() + TASK + "\n", encoding="utf-8")

for path in (WORKFLOW, SELF):
    if path.exists():
        path.unlink()
