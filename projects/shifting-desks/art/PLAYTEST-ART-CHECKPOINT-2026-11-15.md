# Shifting Desks: base-game artwork acceptance checkpoint (2026-11-15 PT)

The render queue is empty, **not** the acceptance backlog. Conductor [Auto Art Generate run 43710225215](https://github.com/silasfelinus/conductor/actions/runs/43710225215) reported no pending requests and no latest-delivery gaps. Its audited ledgers show **181/195 accepted Classic** paintings and **14/195 delivered but visually rejected** paintings. Zero Classic slots await delivery. The optional Western Cartoon skin is already suspended in Kind Robots (`utils/shiftingDesks/artStyles.ts`); its **26/196 accepted** and **170/196 REDO** paintings are a separate quality backlog, not a reason to delay the Classic playtest experience.

The `scripts/shifting_desks_art_readiness.py --strict` check is now scoped to the **required Classic edition** and will remain red while any of the 14 rejected Classic paintings remain. `--all-styles-strict` still checks the entire experimental art catalog. This is a **gate-definition correction**, never an implied visual KEEP or gameplay approval.

## Rejected Classic images: source of truth

All 14 images have a recorded DONE ArtJob, ArtImage ID, image probe and explicit REDO in `art/ROUND-19.yaml`. Art review reference: Round 19 contact-sheet artifact `14085491858` (recorded in `art/ROUND-19.yaml`).

| Subject | ArtJob | ArtImage | Specific reason for REDO |
| --- | ---: | ---: | --- |
| `wellness` | 68769 | 271146 | ordinary clinical hallway with rigid rectangular doors; no organic ribbed doorframes |
| `cognitive-testing-chamber` | 68770 | 271147 | ordinary mechanical examination chair; no enormous breathing lung-like upholstery folds |
| `mutation-suite` | 68771 | 271148 | worker has three arms but floats outside the tank instead of inside it; composition contradicts the foreground-tank brief |
| `sub-level-zero` | 68772 | 271149 | ordinary red executive hallway; no huge branching raised vein-shaped ridges in upholstered walls |
| `boardroom-antechamber` | 68773 | 271150 | ordinary leather chair beside wood paneling; no chair upholstery merging into wall via tendrils |
| `server-room-zero` | 68774 | 271151 | red cables are multiple thin straight wires, not one enormous glossy tendon connecting two cabinets |
| `the-board` | 68775 | 271152 | many separate executive heads and bodies; no eleven necks growing from one continuous suit-covered torso |
| `dale-in-the-mustache` | 68797 | 271444 | large white moustache appears, but required obvious black elastic strap, separate prop edges and raised forefinger are absent |
| `the-taste-panel` | 68776 | 271153 | all four employees smile at pudding; teal-shirted woman's extreme sour recoil and tongue-out contrast absent |
| `the-suppression-drill` | 68777 | 271154 | floor fog is present but crouching employee lacks balloon-inflated cheeks and supposed headphone-wearing janitor is not calmly dusting |
| `the-jam-in-tube-14` | 68778 | 271155 | worker presses a pipe valve; required huge spherical brass bulge containing a trapped ball is absent |
| `mutation-four-second-precognition` | 68779 | 271156 | only one worker steps over a cable; required identical future echo already tripping is absent |
| `mutation-empathic-static` | 68780 | 271157 | two coworkers face each other but the visible electric spark between their foreheads is absent |
| `mutation-eyes-in-the-back-of-your-head` | 68781 | 271158 | rear hairstyle has no additional open eyes; stapler holder appears but supernatural focal gag is absent |

## Exit steps

1. Preserve already accepted Classic art; do not change the 14 REDO verdicts to KEEP without visually comparing a *different* scene-faithful candidate. The Round 19 full-scene generator repeatedly missed focal gags, so blindly repeating the same requests is not justified.
2. Review private single-subject fidelity ArtJobs **69090–69092**, ArtImages **271721–271723**, using `art/SUBJECT-FIDELITY-PILOT-V2.yaml`. These are experimental, not linked game art. If one passes, create a separately verified composite/full-scene replacement for its corresponding rejected Classic slot; otherwise choose a better reference/compositing method rather than resubmitting an unchanged prompt.
3. Reconcile accepted imagery to the five authored encounter packs with `encounters/link_art.py --write --probe`, then rerun `scripts/shifting_desks_art_readiness.py --strict`. Validate final images at phone/tablet/desktop alongside the gameplay and rewards checks (`t-041`, `t-046`, `t-049`).
4. Only after the finite build and QA gates genuinely pass, set Conductor `playtest/normal` and close Kind Robots master issue [#4150](https://github.com/silasfelinus/kind_robots/issues/4150) using the verified handoff. Human playtesting is post-roadmap and publication stays separately gated.

No fresh ArtJob was queued, no asset was silently approved, and no production deployment or lifecycle promotion is represented by this checkpoint.
