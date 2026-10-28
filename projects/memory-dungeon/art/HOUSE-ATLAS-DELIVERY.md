# House dungeon floorplan delivery contract

Task: `memory-dungeon/t-040` · issue: `silasfelinus/kind_robots#4380` · 2026-10-28 PT.

The original and mirrored Houses share the immutable `HD-01` through `HD-36` identifiers and the same ordered 6×6 atlas grid. The map is **not** a 36-image montage: each Krea2 request asks for a single overhead, painterly floorplan. The app's 36 interactive cells, labels, disabled boundaries, focus indicators and action beacons remain DOM controls above the painting.

| Row | West → east (six columns) |
| --- | --- |
| 1 | HD-01, HD-02, HD-03, HD-04, HD-05, HD-06 |
| 2 | HD-07, HD-08, HD-09, HD-10, HD-11, HD-12 |
| 3 | HD-13, HD-14, HD-15, HD-16, HD-17, HD-18 |
| 4 | HD-19, HD-20, HD-21, HD-22, HD-23, HD-24 |
| 5 | HD-25, HD-26, HD-27, HD-28, HD-29, HD-30 |
| 6 | HD-31, HD-32, HD-33, HD-34, HD-35, HD-36 |

The authored room graph contains nonlocal passages (for example HD-06 → HD-01 and HD-24 → HD-31). Depict these as magical stair/portal connections, **not** misleading straight doors across nonadjacent rooms. Preserve the gameplay graph from `utils/memoryDungeon/house.ts` and `darkHouse.ts`; do not edit save IDs to fit a render.

## Durable production requests

| Request ID | Krea2 destination | ArtJob ID | Delivery |
| --- | --- | --- | --- |
| `memory-dungeon-saturate-house-atlas-original-6x6` | `public/images/memory-dungeon/house/maps/house-atlas.webp` | **50365** | Unverified |
| `memory-dungeon-saturate-house-atlas-mirrored-6x6` | `public/images/memory-dungeon/dark-briar/house/maps/house-atlas.webp` | **50366** | Unverified |

Both requests live in the separate `projects/memory-dungeon/art/HOUSE-ATLAS-REQUESTS.yaml` ledger, preserving the historical 752-receipt audit. The Auto Art Generate workflow bulk-submits these two requests before its slower general art queue, reconciles interrupted submissions by immutable request ID and destination, and owns enqueueing and durable `last_art_job_id` receipts; the render relay owns image delivery. Never interpret this request ledger as evidence that the images exist. Before closing the task, verify each ArtJob ID, completed render, final unauthenticated media HEAD response and **visually inspect** the actual floorplans for six-by-six alignment. If Krea2 distorts the topology, re-render with a stronger geometry guide rather than treating the HTML overlay as a substitute for coherent art. Run 390px, 768px and 1440px rendered gameplay checks, keyboard and save/resume tests. Keep the issue open until those gates pass.

## Automated delivery evidence (not visual approval)

Auto Art Generate now runs `scripts/audit_memory_dungeon_house_atlases.py --live --report projects/memory-dungeon/art/HOUSE-ATLAS-STATUS.json` after the receipt checkpoint. The audit fetches the existing Memory Dungeon ArtJobs, verifies each job's immutable request ID, destination and target repository, requires a completed ArtImage, and HEAD-checks the exact unauthenticated media URL for the expected image MIME, nonempty content and a Last-Modified timestamp no older than its job. It writes a separate two-row machine-readable status report; the 752 historical receipts remain unchanged. A missing render or media host is recorded as **not delivered**, never silently counted as success.

Use `python scripts/audit_memory_dungeon_house_atlases.py --live --require-delivered` as the strict **automated media gate** once both jobs finish. The routine status audit is intentionally non-blocking while the renderer works. A delivered media result is still **not** proof that the painted image has coherent 6×6 topology or passed 390/768/1440 rendered, keyboard, reduced-motion and save/resume QA. Those remain explicit requirements before closing issue #4380.
