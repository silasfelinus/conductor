# Rainbow independent review, round 1 (2026-11-23 PT)

Silas decided on 2026-11-23 PT that fresh agent sessions count as independent reviewers: *"Fresh agent sessions
count as independent, go ahead"*. Three read-only reviewer sessions, each with no prior context, reviewed
kind_robots `main` at `4897c0c9`. Each one pushed a defect report to its own kind_robots branch:

| lens | session | report |
| --- | --- | --- |
| gameplay and fairness (#4146 §4, §9) | `session_01L5NKxambWbSZ7WwNsdzrW2` | `claude/rainbow-review-gameplay`: `projects-review/rainbow-gameplay-critic.md` |
| story, routes and endings (§5, §9) | `session_01L5NKxcoC41Nm2tWCsB9Wdk` | `claude/rainbow-review-story`: `projects-review/rainbow-story-critic.md` |
| art, motion, access and devices (§6–§9) | `session_01L5NKxc2Uyg6NvXB3Cv7jdw` | `claude/rainbow-review-presentation`: `projects-review/rainbow-presentation-critic.md` |

**Verdicts:**

- **Gameplay:** playable and fair end to end, with 6 majors and 3 minors.
- **Story:** not story-ready, with 2 blockers, 9 majors and 11 minors.
- **Presentation:** not playtest-ready, with 4 blockers, 11 majors and 8 minors.

#4146 stays open until these are fixed, and the passes will be repeated after the last significant art and
animation change.

Every finding maps to one task below. Status values are **fixed** (with its PR), **open**, or **owner call** (the reviewer named it
Silas's decision; it stays as it is until he decides).

## Gameplay (gameplay critic)

| id | sev | finding | task | status |
| --- | --- | --- | --- | --- |
| D1 | major | B is both focus and super, and a pilot sits at full charge 91% of the time, so focusing spends the super | t-065 | fixed in kind_robots#5713 (hold to focus, tap to fire the super) |
| D2 | major | supers are spam-able screen wipes, 3.5 per pilot-minute (refund of 12 per kill) | t-065 | fixed in #5713 (refund 4, boss damage is a share of the hull; the whole-screen wipe stays because the cut-in covers the comms band) |
| D3 | major | co-op boss HP scales 5.8× at 4p, so 4p fights take as long or longer (finale 4.7 vs 2.7 min) | t-065 | fixed in #5713 (3.4× at 4p) |
| D4 | major | the 2–4p HUD panel hides live pellets (10.8% of 4p combat frames) and clips the boss bar | t-067 | fixed in kind_robots#5716 (every status inside the HUD bar) |
| D5 | major | guardians share one AI and body; a frozen ship takes 0 hits from the Act II guardian; all arrive at frame 6300 | t-065 | partly fixed in #5713 (per-kind motion; aimed fans close the open lane on alternate volleys); arrival timing and per-Act HP open (the HP tier made late guardians escape) |
| D6 | major | the Eclipse Crown's 20° spoke steps leave permanent safe pockets that still deal damage | t-065 | fixed in #5713 (alternate volleys aim a spoke; verifyRainbowBossCamping) |
| D7 | minor | the mortar is reused across 7 Acts and a detour | t-065 | fixed in kind_robots#5737 (one launcher, eight Act shells: own burst pattern and colours, 6-16 pellets each) |
| D8 | minor | infinite continues plus boss-HP carry-over remove the fail state for a parked co-op party | t-065 | **owner call, unchanged**: the phase-reset default was tried and reverted (B01 became unbeatable for the solo test bot), so the kinder carry-over stays until Silas decides |
| D9 | minor | the seed changes nothing | t-065 | open (optional: seeded authored variations, same-seed replay exact) |
| (persona QA) | major | Delphion phase 3: a parked crew is never hit and never hits, so the fight stalls (found by the t-013 personas) | t-013 | fixed in kind_robots#5709 (aimed twin fans) plus `verifyRainbowBossCamping` |

## Story (story critic)

| id | sev | finding | task | status |
| --- | --- | --- | --- | --- |
| S1 | blocker | absent pilots speak in the X1–X4 detours | t-012 | fixed in kind_robots#5709 |
| S2 | blocker | the road epilogues never play, and the party line contradicts loyal endings | t-012 | fixed in kind_robots#5709 |
| S3 | major | the final choice only re-titles the ending (same escape, resolution, epilogue, send-off) | t-066 | fixed in kind_robots#5738 (the escape, Lilt's resolution and the rebel send-off answer the choice) |
| S4 | major | the Crown's plea is a HUD countdown with no dialogue, and a stand-down is never acknowledged | t-066 | fixed in kind_robots#5721 (A09.PLEA scene; stand-down TURN, AFTER and credits) |
| S5 | major | the 15 combination lines are single non-sequiturs with no setup | t-066 | fixed in #5737 (15 three-line exchanges among the pilots flying, built on established pilot hooks; reveal grows to five lines) |
| S6 | major | Vivi speaks for 8 of the 15 crews | t-066 | fixed in #5737 (speakers spread; each pilot has 8+ lines across the combinations) |
| S7 | major | seat renaming hands one pilot's role to another | t-066 | partly fixed in #5709 (four-pilot finale line); the general case is open |
| S8 | major | the princesses are interchangeable in the Acts | t-066 | fixed in kind_robots#5740 (a pilot-keyed arc beat after each of Acts I-VIII, 32 lines carrying each hook) |
| S9 | major | middle seats in 3–4-pilot crews barely speak | t-066 | fixed in #5737 (reveal exchange) and #5740 (the arc beat moves through the seats Act by Act) |
| S10 | major | Lilt-7's agency is a refrain of "I will not choose for you" | t-066 | fixed in #5738 (Lilt states a view and acts: closes Command's channel on the loyal road, spends a memory on the clamps on the rebel road; X3 memory line) |
| S11 | major | ending plates ignore the road and the crew size | t-030 / t-066 | open (with P-03) |
| S12 | minor | the safe trench route knows about the vault's locks | t-012 | fixed in #5709 |
| S13 | minor | the credits contradict the flagship fight | t-012 | fixed in #5709 |
| S14 | minor | plurals at 1 | t-012 | fixed in #5709 |
| S15 | minor | the rescue tally means different things on different screens; the Act I failure line mentions the Eclipse | t-066 | partly fixed in kind_robots#5729 (the Act I-II failure line names the region, not the Eclipse); the rescue-tally wording across screens is open |
| S16 | minor | the continue beat has no writing | t-066 | fixed in kind_robots#5729 (Lilt speaks a continue line per Act; a BACK IN THE FIGHT cue on resume) |
| S17 | minor | internal scene ids appear in the comms header | t-066 | fixed in #5737 (speaker and call sign only; the scene id moves to snapshot.comms) |
| S18 | minor | solo crews are addressed as a group | t-012 | fixed in #5709 |
| S19 | minor | the rebel flight log says the Crown instead of the Motherland | t-012 | fixed in #5709 |
| S20 | minor | developer prose in the ending archive; stand-down is not archived | t-066 | fixed in #5737 (in-world choice pages; a "Turned at the Crown" page for a stood-down crew) |
| S21 | minor | the cadet epilogue ignores whether the cadets came home | t-066 | fixed in #5737 (no combination leans on cadets, academy records or other unplanted beats) |
| S22 | minor | the verdict is road-blind | t-012 | fixed in #5709 (loyal verdict) |

## Presentation (presentation critic)

| id | sev | finding | task | status |
| --- | --- | --- | --- | --- |
| P-01 | blocker | no frame animation for any enemy, boss, ship or pilot | t-030 | partly fixed: picket and urchin (#5717) and anchor and lantern (#5727) idle atlases; hit and victory poses for all four pilots (#5727, #5738); bosses, ships and the other enemies open |
| P-02 | blocker | the living interludes barely move (mean luma difference 0.6–2.6); S03, S04 and S08 have none | t-030 | partly: S08 added in #5717, S03 in #5731, S04 in #5738 (all eight Acts now live); real subject motion open |
| P-03 | blocker | the endings are 3 still plates with no Fever Dream version; sever is in a different style | t-030 | open |
| P-04 | blocker | main Acts have 1–2 painted planes, not 4+; the top half of X3, Act VIII and the finale does not scroll; there is no s09 art | t-022 / t-011 | open |
| P-05 | major | four touch pads cover the play area at 1024×768 | t-067 | open |
| P-06 | major | the P2 pad covers the boss at 844×390 | t-067 | open |
| P-07 | major | the finale reuses Act VIII's card and backdrop | t-022 | open |
| P-08 | major | the 4-pilot HUD covers the boss bar | t-067 | fixed in kind_robots#5716 |
| P-09 | major | phone portrait wastes about 75% of the screen; HUD text is unreadable | t-067 | open |
| P-10 | major | Classic background bubbles look like bullets | t-067 | fixed in kind_robots#5719 (two faint far planes) |
| P-11 | major | pink pellets blend into pink scenes in Fever Dream unless bold shots are on | t-067 | fixed in kind_robots#5716 (firmer default halo and ring) |
| P-12 | major | B02 changes creature between phases | t-030 | open (art regen from the phase-1 reference) |
| P-13 | major | the Act V wreck frames are 1-px outlines | t-067 | fixed in kind_robots#5719 (solid crane silhouettes) |
| P-14 | minor | the detour planes have no Fever Dream twins; the X3 footer has no plate | t-022 | open |
| P-15 | minor | Leviathan's gem-open burst is an illegible clump | t-065 | fixed in #5737 (the two rings spawn 16 px and 28 px out along their spokes) |
| P-16 | major | the stage uses about 27% of a 1920×1080 screen | t-067 | fixed in kind_robots#5720 (stage 1446x813 at 1920x1080, about 57%) |
| P-17 | minor | the settings panel scrolls at 360×640 | t-067 | open |
| P-18 | minor | Seas on phone is text only; the route map is a 40 px strip | t-067 | open |
| P-19 | minor | Solenne has no Fever Dream portrait | t-030 | open |
| P-20 | minor | the Fever Dream Acts blur together (violet plus a rainbow band) | t-067 | fixed in #5740 (a colour key and aurora per Act; the full rainbow opens and closes the flight) |
| P-21 | minor | the HUD control legend stays up for the whole run | t-067 | fixed in kind_robots#5716 (legend in Act I only) |
| P-22 | minor | seat numbers collide with ships | t-067 | fixed in kind_robots#5716 (seat tag behind the tail) |
| P-23 | major | the short-landscape title screen is 190×107 px | t-067 | open |
