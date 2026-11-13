# Shifting Desks visual art acceptance / 2026-11-12 PT

The editor inspected the **20 actual replacement Classic images and six isolated
Western-fidelity pilot images**, using the authenticated media capture from
[GitHub Actions #43356430754](https://github.com/silasfelinus/conductor/actions/runs/43356430754),
[artifact 14005599553](https://github.com/silasfelinus/conductor/actions/runs/43356430754/artifacts/14005599553).
The original audit confirmed the 20 final media objects are newer than their
DONE ArtJobs. The first artifact capture included 15 older Round 13 KEEP rows
as empty thumbnails because they lack the newest batch's provenance; those
are *not* failures in this review. The scoped evidence collector now chooses
only this 20-ArtJob recovery wave.

## Classic replacement verdicts

| Round | Image | ArtImage | Verdict | Visual reason |
|---|---|---:|---|---|
| 13 | Kind Rewrite ending | 270615 | KEEP | Gold speaker-grille wall, cable-knit thumbs-up intern, happy typewriter staff |
| 14 | Wellness arrival | 270624 | REDO | No living doors or windpipe ducts |
| 14 | Nutrition Studies | 270620 | KEEP | Green paste trays on fleshy pink conveyor under observation glass |
| 14 | Cognitive Testing Chamber | 270617 | REDO | Near-photographic sterile room, no breathing chair or ciliated speaker |
| 14 | Mutation Suite | 270619 | REDO | All tank occupants look unmutated |
| 14 | Sub-Level Zero arrival | 270622 | REDO | Ordinary wood corridor, no organic veins/tongue carpet/iris door |
| 14 | Boardroom Antechamber | 270616 | REDO | Ordinary chairs and typewriters, no organic fusion or beetle shells |
| 14 | Founder's Office | 270618 | KEEP | Mustached jar-head, living wires, caterpillar-like mustaches and radio |
| 14 | Server Room Zero | 270621 | REDO | Conventional racks, no breathing mouths or tendon cabling |
| 14 | The Board | 270623 | REDO | Executives sit separately instead of being fused into one suit |
| 15 | The Curious Robot | 270630 | KEEP | Tiny robot looks up at bespectacled human clerk |
| 15 | Kevin from Tank Nine | 270626 | KEEP | Frost-cleared face and palm print |
| 15 | Dale in the Mustache | 270625 | REDO | Natural dark mustache instead of giant crooked white fake with elastic |
| 15 | The Taste Panel | 270633 | REDO | Every diner smiles, missing disgust contrast |
| 15 | The Suppression Drill | 270632 | REDO | No calm janitor and no puffed-cheek gag |
| 15 | The Jam in Tube 14 | 270631 | REDO | No enormous swelling in the central brass pipe |
| 15 | Four-Second Precognition | 270629 | REDO | No same-person phantom/time-echo stepping over tripwire |
| 15 | Empathic Static | 270627 | REDO | Bolt from ceiling, not between foreheads; hair stays flat |
| 15 | Eyes in Back of Head | 270628 | REDO | No extra eyes on hair or stapler thief |
| 17 | Permanent Adjournment ending | 270634 | KEEP | Isolated worker, waiting rows, huge clock, frosted silhouettes |

**Totals: 6 KEEP, 14 REDO.** Individual evidence and verdicts are in the
authoritative ROUND-13/14/15/17 YAML rows, with original prompts, seeds,
request IDs, ArtJob IDs, ArtImage IDs and confirmed newer media. Four accepted
encounter/location images now have corresponding `verified-repository-art`
links in the packs. The two accepted ending destinations are handled by the
game's ending-art convention and are not encounter-pack slots.

## Western Cartoon fidelity comparison (private, not in game)

Six DONE ArtJobs were individually assessed at the same three scene intents,
with two checkpoints (Krea 2 prose / Nova Comic XL subject-first tags).

| Subject | Krea 2 | Nova Comic XL |
|---|---|---|
| Gus visibly files a grievance as a giant real roach | **KEEP pilot**: giant roach, cardigan, paperwork, human clerk | REDO: insect in office, no filing scene or clerk |
| Wind-up robot looks up at clerk | **KEEP pilot**: tiny robot, clerk and upward gaze | REDO: robot under red giant eye, no clerk |
| Huge stopped clock in endless waiting room | REDO: chairs and clock, but stage reads auditorium and isolated employee is missing | REDO: corridor with lockers and multiple clocks; no waiting room |

Krea 2 preserves the original scene in **2 of 3** test images, compared with
**0 of 3** for Nova. These are only six samples, not a reliable overall quality
benchmark; they do show that Nova is not a promising drop-in replacement for
these relational gags. **Do not re-enable the optional Western edition or blindly
repeat the 170 rejected Western renders.** The 196-image prior review stays
authoritative. Pilot verdicts are attached to `SUBJECT-FIDELITY-PILOT-V1.yaml`;
none of the private candidates was linked or published.

## Next art delivery work

The 14 REDO subjects require individually revised scene-first prompts and a
controlled replacement wave. Preserve their current ArtJobs and full failure
notes as evidence. Important visual requirements are relational (eyes on the
*back* of a head, multiple people physically fused into *one* body, lightning
*between foreheads*, etc.), not generic style adjectives.

After new ArtJobs complete, independently check delivery timestamps, review
every image again, and run `encounters/link_art.py --write --probe` plus
`scripts/shifting_desks_art_readiness.py --strict`. Do not promote to
`playtest` or bypass the human fun gate while 14 Classic and 170 optional
Western renders remain rejected.
