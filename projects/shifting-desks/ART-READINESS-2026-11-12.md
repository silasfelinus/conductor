# Shifting Desks art acceptance audit — November 12, 2026

**Status: NOT ready for verified Playtest transition.** Evidence inventory, not a
creative sign-off. The result is independent of whether an existing runtime
asset happens to return HTTP 200: the latest forced rerender needs its own
media provenance and a separate human/agent editorial *keep* decision.
Existing published art must not be deleted or replaced on speculation.

## Latest effective art ledger entry per destination

Compared all available `art/ROUND-*.yaml` files; later round number wins
when a destination is repainted. This prevents a previous KEEP from silently
approving a newer requested or rendered image.

| Accepted KEEP + delivered evidence | Delivered, no verdict yet | Visually rejected, needs redo | New/latest delivery not verified | Distinct destinations |
|---:|---:|---:|---:|---:|
| 201 | 0 | 170 | 20 | 391 |

All **196 round-18 subject-first Western Cartoon renders** have now
received individual, image-to-prompt visual verdicts. The earlier eleven
incorrect ending paintings remain rejected, and reviewing the other 185
produced **26 usable KEEP** and **159 REDO** verdicts. Thus 170/196
Western Cartoon paintings fail key authored visual requirements; all
verdicts are documented beside their source ArtJob and image IDs in
`art/ROUND-18.yaml`. Contact sheets and the prompt manifest came from
GitHub Actions artifacts 13930814494 and 13932222834.

This is a systemic subject-fidelity failure of the current Western Cartoon
rerender pipeline, **not 170 missing files**. Do not blindly resubmit 170
identical prompts to the same checkpoint. The optional Western style is
temporarily suspended in Kind Robots while a better scene-faithful pipeline is
designed and reviewed. Existing Classic and Noir styles remain available,
and no artwork was deleted. This does not certify Classic art complete:
20 later Classic/recovery repaint requests still lack verified newer delivery.

The **20 not-delivered-latest** entries are:

- Round 13 (1): `ending-the-kind-rewrite`.
- Round 14 (9): `wellness`, `nutrition-studies`,
  `cognitive-testing-chamber`, `mutation-suite`, `sub-level-zero`,
  `boardroom-antechamber`, `founders-office`, `server-room-zero`,
  `the-board`.
- Round 15 (9): `the-curious-robot`, `kevin-from-tank-nine`,
  `dale-in-the-mustache`, `the-taste-panel`,
  `the-suppression-drill`, `the-jam-in-tube-14`,
  `mutation-four-second-precognition`, `mutation-empathic-static`,
  `mutation-eyes-in-the-back-of-your-head`.
- Round 17 (1): `ending-permanent-adjournment`.

**Verified remote-media finding (2026-11-12):** Every one of these 20
paths returns HTTP 200 `image/webp`, but the `Last-Modified` timestamps
precede its respective later round request. Rounds 13-15 were requested on
2026-10-20 at 18:45, 19:30 and 20:10 UTC, whereas those existing images
were last modified around 12:37-13:49 UTC on that date. The round-17
Permanent Adjournment image was last modified 2026-10-23, before its
2026-11-01 recovery request. This is **positive evidence of older images**,
not newer delivery. Full per-image timestamps are in the GitHub Actions
artifact manifest. The current Classic ending plates must be preserved.
Before queuing any duplicate, check production ArtJobs by exact request ID,
destination and creation time via `art/reconcile_delivery.py --live --write`.
Only an independently proven newer completed render can be called delivered.

## Verification workflow

The script `scripts/shifting_desks_art_readiness.py` is the one-command
inventory. The Auto Art Generate workflow attaches a human-readable report on
each run, and the script can emit every individual blocker in JSON:

```bash
python scripts/shifting_desks_art_readiness.py --markdown
python scripts/shifting_desks_art_readiness.py --json
python scripts/shifting_desks_art_readiness.py --strict
```

The strict command must fail while any ledger destination remains missing,
unreviewed, rejected or unsupported by delivery evidence. It is an **art gate
only**, not a replacement for independent gameplay, editorial, 390/768/1440
layout, screen-reader and user-facing verification.

Next agent-owned actions:
1. Reconcile the 20 requested rerenders against actual DONE ArtJobs and newer
   media. If an old painting is good enough, explicitly withdraw the *new*
   request with documented evidence, rather than inventing a delivery.
2. Design and test a small scene-faithful Western repaint pilot before
   enqueueing any replacement batch; do not revive the optional skin merely
   because images exist. Retain all 196 render records for comparison.
3. Link accepted Classic imagery with
   `projects/shifting-desks/encounters/link_art.py --write --probe`.
4. Re-run the readiness audit and the actual game/art/device tests, then hand
   the **final fun verdict** to Conductor `shifting-desks/t-020` with
   `status: needs-human`. Never grant this approval on the agent's behalf.

**References:** `projects/shifting-desks/art/ROUND-13.yaml` through
`ROUND-18.yaml` (round 16 was not present); `projects/shifting-desks/roadmap.yaml`,
`ART-DIRECTION.md`, and
`projects/shifting-desks/STANDARD-AUDIT-2026-11-12.md`.
