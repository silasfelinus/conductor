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


## 2026-10-31 PT · Worker · t-004 · PR #4567

**What landed:** Merged [Kind Robots PR #4567](https://github.com/silasfelinus/kind_robots/pull/4567) as `48bc973` after 19/19 completed checks succeeded. Twelve original real night cases now have 60 distinct grade/refusal-specific morning consequences, integrated into the seeded school-day progression; the 24 previously expanded cases remain available.

**What I challenged:** The existing case deck had reached 36 families, but the original 12 lacked morning callbacks. The seeded Academy playthrough caught an ordering flaw in the first integration: an unanswered side mission displaced the player's completed neighborhood-patrol aftermath. The follow-up priority was corrected and verified before merge.

**Remaining:** Task t-004 remains `ready` for delayed faction standing, injured-roster conflicts, more deeply authored moral approaches and callback branches across all 36 families. An authored text callback is not itself a complete persistent consequence system.

**Kaizen:** Preserve the distinction between a player-led patrol, a delegated call, and an unanswered emergency in structured report provenance rather than inferring the choice only from display names.


## 2026-10-31 PT · Worker · t-004 case-history gameplay · PR #4569

**Shipped:** Kind Robots PR #4569 merged as `c412e3a` after 19/19 completed checks passed. Thirty-day campaigns now save a validated history of 36 authored case families and whether a call was left unanswered. Investigating in a district uses outcomes from the previous five nights as a bounded seeded mission modifier. Failed attempts and ignored emergencies are distinct, older saves retain compatibility, and duplicate history is rejected.

**Adversarial finding:** An initial passive modifier changed the three established seeded campaign finales, including the canonical transmitter shutdown. Restored legacy rescue odds by applying the trust modifier only to a personally selected investigative approach. The 30-day seeded playthrough and new case-memory test both passed on the merged head.

**Remaining:** t-004 returns to `ready` for broader roster injury follow-ups, faction relationships, and character-specific delayed callbacks. This was a gameplay effect and save contract, not final art or self-hosted deployment verification.

**Kaizen:** Show local case memory in the investigation dossier, with a player-visible rationale for the trust bonus or cost.
