# Prom of Doom: creative implementation review notes

## 2026-10-29 PT | Worker → Reviewer | comet-city-academy/t-002 | scoped villain henchman bible

**Decision:** scoped content merged, full t-002 task deliberately returned to ready.

**What was good:** Forty-eight stable identity signatures mapped one-to-one to named one-hit henchman types with original tactical behavior, readable counters, visual identity and conflicting allegiances. The runtime JSON and typed lookup share the Prom identity source; all 14 Kind Robots final head checks and all 6 Conductor final head checks passed. The source is cross-linked to both game roadmaps and preserves the distinction between ordinary one-hit species and major independent accomplices.

**What to improve:** Do not treat authored species rows as actual Facet database entities, rendered ArtImages, playable combat units or completed full-game storylines. The current 48 runtime roster does not yet include Granny Mayhem or Dr. Frog, and Zuzu remains a guest: these three proposed henchman concepts must wait for task t-021 reconciliation before acquiring permanent IDs.

**Kaizen:** Follow-up t-024 adds real deployment, Yearbook/Forge cards, ArtJob provenance and adversarial tests without inflating authored coverage. A future Forge progress panel should separately report authored, queued, rendered, attached and playtested counts.

**PR evidence:** Conductor #6791 (38da5c2), Kind Robots #4452 (8e2a21a). No publication, production deploy, irreversible data changes or human acceptance claimed.

## 2026-10-29 PT | Reviewer | comet-city-academy/t-002 | 48 power openings, lairs and lieutenants

**Decision:** approved and merged Conductor #6793 (squash 6bd4a01). Scoped planning/canon content, reversible, all 26 head checks green, no comments outstanding.

**What was good:** Authored-vs-built is stated explicitly (96 scenes and 48 lieutenants are not marked playable); new Prom tasks t-025/t-026 are correctly `waiting` on t-021/t-016; the six-stage Crossfire backbone is preserved and no saves/identities are rewritten.

**What to improve:** Roadmap notes grow with each scoped pass; keep new `notes_from_silas` entries to a pointer plus the bible file name.

**Kaizen:** t-027 added to keep a per-count authored/queued/rendered/playtested tracker so progress claims never conflate stages.

## 2026-10-30 — Reviewer: PR #6825 (Unstable unblock, Prom runtime refill, franchise-safe re-renders)
Merged (squash 9017e41). Art ledgers/prompts only, reversible, CI green. The five held franchise look-alike jobs are marked REJECTED in their own ledgers and replaced by original-costume re-render prompts; a test pins that no DONE status remains on held keys. Pattern worth keeping: reject-in-ledger plus replacement round, rather than deleting art.
