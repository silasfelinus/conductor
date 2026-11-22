# dream-cycle/t-035 — full note history archive

This file is the archaeology index for dream-cycle/t-035 ("Daily improvements: ship five changes and close out their canonical roadmap tasks"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-035 -->
HISTORICAL DAILY CONTRACT (Silas, 2026-10-02): every day's digest carries FIVE new project
pitches, biased to free-to-play ideas that need no LLM at runtime (Kind Robots has a lot
locked behind LLM API access; authoring tokens and image generation are plentiful). Silas
decides each by clicking Approve or Pass in the email (signed confirm links), or on the
Kind Robots project page; sessions only AUTHOR the pitches and never decide them.
Recipe: `python scripts/daily_pitches.py --brief` (what to avoid and the rules), write
pitches/daily/<pacific-date>.yaml, `--check`, `--materialize`, PR, merge when green.
Then check `--approved`: any approved pitch with no project yet is scaffolded with
scripts/intake.py (brief, roadmap, ready build tasks) in the same session.
Every completed daily attempt updates daily_last_checked to that Pacific date; update
daily_last_completed only after the day's docket is merged. Undecided pitches stay in the
digest ("still waiting") until decided; never re-pitch a rejected one.

UPDATED DIRECTION (Silas, 2026-10-12 PT): starting with new 2026-10-13 PT dockets,
ALL five pitches are expansions of existing projects, never fresh projects.
A pitch has target and expansion_kind; approvals request the NEXT agent to
write a polished roadmap extension with milestones, tasks, dependency order,
art direction, tests, and source_pitch: pitches/<date>-<slug>.md.
They do not create a project via intake.py or a Kind Robots Project row.
See ZUZU-DAILY-CREATIVE-CONTRACT.md and scripts/daily_pitches.py --brief.

RAN 2026-10-09: docket pitches/daily/2026-10-09.yaml already authored and materialized
by an earlier session today (5 pitches, 5 undecided). Bumper Bubbles approval already
shipped (kind_robots#3384).

Daily delivery contract implementation in worker/dream-cycle-t035-deliveries-c7e4 is ready for PR and CI review. Recurring daily entry generation remains open; this slice makes future digests evidence-backed, with Keep/Modify/Reject feedback and no fake builds.

Merged the five-evidenced-daily-upgrades foundation as conductor#6077 (full CI green). The Kind Robots review UI companion is PR #3616 pending its full 488-step contract suite. This was workflow implementation, NOT five already-built game additions; keep daily_last_completed unchanged. Re-arm t-035 for the next five tangible project upgrades, with PR evidence and post-build Keep/Modify/Reject feedback.

Materialize October13PT build-first ledger from five independently verified already-implemented Shifting Desks upgrades: kind_robots#3627/#3628/#3629/#3632/#3633. All five merged after PT midnight; all33 actual checks per exact head completed success/intentional skip. Independent final-main gameplay suite passes2475/3000 completed525 eliminated. Preserve independent original Daily Dream and8Zuzu assets, existing worker ownership and artwork delivery truth; no new duplicate implementation.

Five October13PT real Shifting Desks upgrades already implemented and merged by assigned project worker, exact33 passing checks each and independent final-main gameplay suite2475/3000 verified. Ledger and5 Keep/Modify/Reject records on worker/dream-cycle-t035-daily-deliveries-j3p8; daily_project_deliveries --materialize and --check pass. All five software additions are shipped, separate art remains honestly blocked where final delivery not verified. Daily completion marker must stay unchanged until this evidence ledger merges; original Daily Dream and8Zuzu assets excluded. Await focused PR/full-head CI.

October13PT five-entry delivery ledger and after-build Keep/Modify/Reject records merged as conductor#6117 at978d2bb5e753256c9f61b4c6d8672802f9e5601b after all24 exact-head checks completed success/intentional skip, including full Python suite. Five distinct kind_robots#3627/#3628/#3629/#3632/#3633 gameplay additions all merged after PT midnight with33 completed green checks each; independent final-main gameplay2475/3000 verified. Narrow CAS updated only t035 dailychecked/completed metadata after evidence merge and appended kaizen t039; lifecycle rearm remains task-event controlled. Three packs' art still truthfully blocked awaiting render verification; independent6Dream+8Zuzu assets excluded. Fixture isolation corrected without weakening policy. Re-arm for future days and --feedback; no email/publication/deployment.

2026-10-14 agent cycle: five kind_robots deliveries (PRs 3680/3681/3683/3684/3685)
already materialized and --check valid (#6175); no feedback queue. Dream docket shows
4/5 only because --brief reproduces seed 8856167133454325615, already authored twice for
2026-10-14; authoring again would duplicate, deferred to next dated seed.

2026-10-15 agent cycle: five shipped kind_robots deliveries merged via #6199, --check
valid, no feedback queue. Dream seed 2090383560336650705 already authored and built
(spare-sun-annex); no duplicate authored.

2026-10-17 agent cycle: five shipped deliveries (Shifting Lands wagon kind_robots#3808,
Emperor Day 3 #3809 etc.) merged via #6283, --check valid, no feedback queue. Dream seed
9574574129836055354 already authored (backlog/2026-10-17-bloomrig-jubilee.md); no
duplicate authored.

2026-10-18 agent cycle: five shipped kind_robots deliveries (seed-burst gnats
kind_robots#3834 etc.) merged via #6296, --check valid, no feedback queue; reconciled
daily dates the prior cycle left at 10-17.

2026-11-04 PT: no 2026-11-03/04 delivery docket authored. kind_robots deps install, but
the dev server needs DATABASE_URL so UI changes cannot be screenshot-verified in this
sandbox; shipping unverified front-end work was declined. Audience-first candidates
left: interface-vision t-150/t-151.

2026-11-07 PT: no delivery docket authored. Sandbox has no kind_robots DB, so front-end
changes cannot be screenshot-verified; t-151 still lacks a week of site-stats events.
Shipped instead: ruler-hooked/t-053 audit false positive closed. daily_last_completed
unchanged.

2026-11-10 PT daily-creative cycle: five audience-first link-preview/share upgrades
shipped in kind_robots#4976 (merge 08afc11, 13/13 checks completed green/skip): Shifting
Desks poster preview, Slime City card, Monstrique's missing preview, aquarium
leaderboard preview, owner-aware public tank share card. Ledger projects/dream-
cycle/daily-deliveries/2026-11-10.yaml, --check valid. Next: remaining
FALLBACK_PREVIEW_IMAGE pages (Mandarin, Brainstorm, Sliding Tile Gallery...).

2026-11-11 PT daily cycle: five audience-first link-preview cards shipped in
kind_robots#5004 (squash e8c0867, 11/11 checks green): Sliding Tile Gallery, Brainstorm,
Mandarin Tutor, Music Mentor, Coloring Page Maker. Ledger daily-
deliveries/2026-11-11.yaml, --check valid. Next: remaining FALLBACK_PREVIEW_IMAGE pages
(video-generator, daily-pitches, hybridizer, comic-studio, tzaddik-gallery, art-archive,
challenge-leaderboard).

2026-11-12 PT daily cycle: five audience-first link-preview cards shipped in
kind_robots#5074 (squash f78eb29, 11/11 checks green): Video Studio, Daily Pitches,
Hybridizer, Comic Studio, Art Archive. Ledger daily-deliveries/2026-11-12.yaml, --check
valid. Next: remaining FALLBACK_PREVIEW_IMAGE pages (tzaddik-gallery, challenge-
leaderboard), then pick a new audience-first lane.

2026-11-13 PT cycle: five deliveries in kind_robots#5135 (squash 52df00c, 11/11 checks
green): designed link-preview cards for Tzaddik Gallery, Hall of Contenders, Arcade and
Cthulhuquarium leaderboard (no FALLBACK_PREVIEW_IMAGE pages remain), plus the
windmill-polder-dusk screensaver. Ledger daily-deliveries/2026-11-13.yaml, --check valid.
Next: link-preview coverage is complete; pick a new audience-first lane.

2026-11-14 PT reconciliation: today's five audience-first link-preview cards (Crystal
Street, Zuzu Ghost Trail, Rainbow Bullet Hell, Save the Plumber, Emperor of Dust)
shipped in kind_robots#5150 (merge ff3c764, 12/12 checks green) and were recorded via
#7381 (daily-deliveries/2026-11-14.yaml, --check valid), but that PR left t-035's daily
dates at 11-13; this close-out records them. Next: pick a new audience-first lane (link-
preview coverage is complete).

Nov 14 PT user-directed refinement: retain five real daily PR-backed project increments, not five newly created roadmaps. From Nov 15 each one must cite a distinct existing canonical project roadmap task with a dated, PR-specific implementation and verification note. Enforce in daily delivery validator, show roadmap evidence in each review card, and preserve historical deliveries. Reversible PR and final checks pending.

2026-11-14 PT: merged conductor PR #7414 (5a5a57f245fe67db88474950886fa5d1545c6909) after all six workflow groups including the full Python test suite completed green. Starting 2026-11-15 PT each of five daily project improvements records its own distinct existing canonical project roadmap task, a dated delivery marker and the actual implementation PR and test evidence. Original game roadmaps are not closed on one increment; historical deliveries remain unchanged and visible after archival. Re-arm recurring daily improvement commitment; Nov 15 new deliveries have NOT been performed.

2026-11-15 PT daily cycle: five audience-first upgrades shipped in kind_robots#5209
(merged c24cef2, CI green): designed link-preview cards for Space Couch, Prom of Doom,
Zuzu gamebook + Shifting Lands, Slime City duel invites (page had no meta), plus slime-
city/t-067 LOCAL PLAY instead of STORY SYNC ERROR. Ledger projects/dream-cycle/daily-
deliveries/2026-11-15.yaml (--check valid). Next: remaining raw-art previews (ecotone,
zuzu-showdown, zuzu-pinball) or a non-preview audience lane.

2026-11-16 PT cycle: five shipped in silasfelinus/kind_robots#5248 (merged 88b21a1, CI green):
interface-vision/t-151 login names destination, t-104 route-scoped tab titles, t-143 phone
mission line, slime-city/t-063 honest gated share cards, kr-arcade/t-169 showcase cold-open
probe (22/22 live). Ledger projects/dream-cycle/daily-deliveries/2026-11-16.yaml (--check
valid).

2026-11-18 PT: five shipped (docket projects/dream-cycle/daily-
deliveries/2026-11-18.yaml, --check valid): interface-vision t-104 site-name tab titles,
t-151 honest app description, kr-arcade t-171 strict unfurl schedule (task done), t-169
daily cold-open probe (kind_robots#5309), dead-air t-004 VO peak headroom
(conductor#7574). Three audience-first (titles, description, share-link guards).

2026-11-20 PT: five shipped via kind_robots#5416 (one PR, five distinct interface-vision
tasks): t-144 guessable URL aliases, t-151 Chessweeper/Ruler share previews, t-104 stale
share-description guard, t-105 plain /register copy, t-137 prettier ratchet 1047->930. Four
audience-first.

2026-11-21 PT: five shipped in silasfelinus/kind_robots#5513 (merged d142dd9, 13/13
checks green): interface-vision/t-151 three games added to sitemap with an arcade-tab
completeness guard, memory-dungeon/t-068 and chessweeper/t-003 light share cards
(643/582 KB -> 205/175 KB), interface-vision/t-144 light Art gallery card, t-105 plain
/navigation copy. All five audience-first. Ledger projects/dream-cycle/daily-
deliveries/2026-11-21.yaml.

2026-11-22 PT: five shipped in silasfelinus/kind_robots#5580 (merged de1be6c, 15/15
checks green) from a live audit of all 29 sitemap URLs: memory-dungeon/t-068 plain one-
line description, interface-vision/t-144 /art leads with browse-free, t-151
Cthulhuquarium says a tank needs a free sign-in, t-105 real Zuzu Showdown preview, t-137
Prettier ratchet 930->913. Four audience-first. Ledger projects/dream-cycle/daily-
deliveries/2026-11-22.yaml (--check valid).
<!-- note:end t-035 -->
