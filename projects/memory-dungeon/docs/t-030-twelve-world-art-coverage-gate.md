# Memory Dungeon production-art coverage gate (2026-11-13 PT)

Owner: t-030. Canon: [twelve-world delivery roadmap](../TWELVE-WORLD-DELIVERY-ROADMAP.md); tracking issue [kind_robots#4136](https://github.com/silasfelinus/kind_robots/issues/4136).

## The denominator matters

The active game has **twelve** playable worlds e01–e12. e13–e16 are archival save IDs, not production targets. Every playable world must account for 64 unique authored overworld sites, one linked dungeon, and a **32-face collectible gallery (30 local + 2 cross-world)**. The production target is **768 sites, 12 dungeons and 384 gallery faces**, not 16×64 or 16×32. A single image may serve multiple contextual sites when explicitly art-directed, but a request manifest does not prove a visible image.

## Evidence grades (never collapse these)

| Grade | Proof required | What it does not establish |
| --- | --- | --- |
| Authored | Stable site/room/gallery ID, intended image path and art direction | An ArtJob exists |
| Submitted | Durable request ID and ArtJob ID, with source ledger | Rendering succeeded |
| Rendered | ArtJob DONE plus linked ArtImage ID | Media is accessible |
| Delivered | Final production URL passes HTTP HEAD and attachment resolves for the intended entity | Correct art displays in the game |
| Accepted | Rendered game screen at 390/768/1440, correct subject, no broken image, 30+2 deck unlock/play, saved reload | Publication approval |

Historical t-030 notes record **752 unique request/ArtJob receipts**, and audit run **#40429786760** reportedly verified 752 media deliveries. Those are historical **first-batch** receipts, not 384 world-gallery attachments or proof that all twelve playable worlds are visually complete. Re-run live verification against the current source of truth before promoting any row.

## World-by-world acceptance ledger

Use `?` for **unverified**, never zero or a checkmark. The 64-site and 32-gallery columns are targets, not achieved counts.

| World | Protagonist / geography | Sites target | Dungeon | Gallery target | ArtJob IDs reconciled | Delivered + attached | Rendered viewport QA |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| e01 | Briar original | 64 | House | 30+2 | ? | ? | ? |
| e02 | Dark Briar | 64 | Dark House | 30+2 | ? | ? | ? |
| e03 | Morrow Earth | 64 | linked Earth dungeon | 30+2 | ? | ? | ? |
| e04 | Morrow altered Earth | 64 | linked Earth dungeon | 30+2 | ? | ? | ? |
| e05 | Scylla shore | 64 | linked shore dungeon | 30+2 | ? | ? | ? |
| e06 | Scylla undersea | 64 | Choking Works | 30+2 | ? | ? | ? |
| e07 | Vesper warm Hoshimori | 64 | linked Hoshimori dungeon | 30+2 | ? | ? | ? |
| e08 | Vesper horror Hoshimori | 64 | Furnace of Names | 30+2 | ? | ? | ? |
| e09 | Rowan/Pip collision | 64 | linked collision dungeon | 30+2 | ? | ? | ? |
| e10 | Morrow collision | 64 | linked collision dungeon | 30+2 | ? | ? | ? |
| e11 | Char (Scylla fallback) collision | 64 | linked collision dungeon | 30+2 | ? | ? | ? |
| e12 | Vesper collision | 64 | linked collision dungeon | 30+2 | ? | ? | ? |

## Next executable art increment

1. Export the current request ledger and live ArtJob/ArtImage delivery auditor for e01/e02; join by **request ID**, not filename or index. Report missing IDs, failed jobs, missing attachments, and inaccessible final URLs separately.
2. Reconcile every one of the 64 scene slots, 36 House rooms (where specified), 32 gallery faces, major characters, maps and ending plates against the actual UI image selectors. Count each stable ID once. Record a source commit and audit workflow ID.
3. Resubmit **only missing or failed** requests through the durable ArtJob pipeline. Persist request and ArtJob IDs before waiting on renders; do not duplicate successful jobs.
4. Test the delivered art in actual rendered scenes and deck selection at 390, 768 and 1440px. A generic SVG fallback is not production art; preserve it only for pending/failure states.
5. Repeat the exact reconciliation per world. Add verified counts, ArtJob IDs and screenshots to #4136; leave all unknown cells unresolved until observed.

This ledger is an acceptance contract and reconciliation plan, **not** a claim of new ArtJobs, finished galleries, live HEAD checks or UI screenshots.
