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
| `memory-dungeon-house-atlas-original-6x6` | `public/images/memory-dungeon/house/maps/house-atlas.webp` | Pending submission | Unverified |
| `memory-dungeon-house-atlas-mirrored-6x6` | `public/images/memory-dungeon/dark-briar/house/maps/house-atlas.webp` | Pending submission | Unverified |

Both requests live in `projects/art-prompts.yaml`. The Auto Art Generate workflow owns enqueueing and durable `last_art_job_id` receipts; the render relay owns image delivery. Never interpret this request ledger as evidence that the images exist. Before closing the task, verify each ArtJob ID, completed render, final unauthenticated media HEAD response and **visually inspect** the actual floorplans for six-by-six alignment. If Krea2 distorts the topology, re-render with a stronger geometry guide rather than treating the HTML overlay as a substitute for coherent art. Run 390px, 768px and 1440px rendered gameplay checks, keyboard and save/resume tests. Keep the issue open until those gates pass.
