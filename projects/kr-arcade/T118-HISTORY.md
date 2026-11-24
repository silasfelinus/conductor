# kr-arcade/t-118 — full note history archive

This file is the archaeology index for kr-arcade/t-118 ("Petal Post depth slice 1: Street engine and Primrose Lane"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-118 -->
CABINETS.md section 20, Petal Post (Paperboy riff), slice 1 of 4: Street engine and Primrose Lane. The upgrade is "A Season in Blossom Valley". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug petal-post). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Implemented persistent house bloom, two-gift neighbour signups, wilting before cancellation, and visible garden growth in Petal Post. Further Primrose Lane route work remains.

PR silasfelinus/kind_robots#5676 merged at 28514e531cdcdd2f4e0099e7e63b917a95d2848d; nine CI workflows passed. Bloom persistence, wilting and flower-gift subscription recruitment shipped. Remaining authored Primrose Lane encounters, two-sided street layout, day/week structure and gameplay tests remain.

Added daily mailbox/porch request signs and double-bloom delivery rewards on worker/kr-arcade-t-118-requests-p9x3. Remaining route, encounter and deterministic QA work stays open.

kind_robots#5678 merged as 19d3584994b8b14a1462f6f32c333a0fe9a26b25 after all nine workflows passed on 4eff361b. Six authored weekdays, three hazards, weather, Valley Gazette and regression suite delivered. Remaining: two-sided street and throws, authored geometry, Park Loop and device QA.

Two-sided street and persistent alternate-side houses, mirrored art, A/B directional velocity, speed-sensitive toss distance, right/left mailbox and porch collision, updated attract pilot and controls, and input-level regressions implemented on worker/kr-arcade-t118-two-sided-c83f. Remaining authored street landmarks and Park Loop course; requeue after green merge.

PR kind_robots#5686 merged as c0b3ae58381f42ab78c464ae48e04f1bc0930660; all nine latest-head workflows passed on 7d4b99e, including Contract Tests, browser contracts and viewport matrix. Two-sided street and directional throws shipped. Remaining authored landmarks, Park Loop and device QA.

Added stable authored crossings, side roads, shops and park landmarks with weekday unlocks and guaranteed shop refills. Park Loop has two ramps, eight timed targets including two airborne rings, supply reset, jump-dependent parcel range, gold course stamp and Gazette recap. Input-level regression coverage added. Branch worker/kr-arcade-t118-park-93ac; pending CI and rendered playtest. No release or deploy initiated.

PR kind_robots#5690 squash-merged at e62e1e464824e03b35c35bd05bb2b599cc58420c. All eight workflows returned for exact head 8c2655954593bb47164e0e58880c47b6c81a5b75 completed successfully; job results include TypeScript, four contract shards and aggregate, Chromium arcade and Rainbow browser contracts, formatting, layout, architecture and migration parity. Park Loop, ramp throws, seven authored landmarks and shop refills shipped. Keep ready for remaining authored segment/slope audit, deterministic week and pilot evidence, and rendered device QA. No deployment or human playtest claimed.
<!-- note:end t-118 -->
