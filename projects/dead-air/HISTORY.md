# dead-air — task history archive

Full `note:` prose for completed dead-air tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Bootstrap Dead Air editorial archive, pilot, reusable producer and daily attempt

<!-- note:begin t-001 -->
Silas-directed new continuous project bootstrap. Original authored pilot The Closed Caption Department, substantial pop-culture reference study, versioned transmission archive, 15s/5-shot/two-motion-clip validation, MusicVideo/ArtJob adapter, and daily attempt workflow. This is a private production scaffold and pilot script, not a claim that an MP4 rendered.

Bootstrap landed in conductor PR #7313, squash d8d5a39ecc2ade7bd811e611b01e93ce563aaa02. The exact PR head 0fdf6107c6852c54eb9080ca5c96dc9a8dbd4f5b had 28 completed successful, neutral or skipped checks, including 4600+ passing Python tests. The first pilot is a privately staged production, not a verified MP4.
<!-- note:end t-001 -->

## t-002 — Render and verify the first complete private fifteen-second pilot

<!-- note:begin t-002 -->
Resume the pilot's MusicVideo/ArtJobs; verify final mp4 exists, 15 sec duration, sound, text, coherent style and purposefully animated cinematic shots. Only one optional genuine GPU clip may queue under the 2-hour new-request budget. Record exact video, ArtJob and final ArtImage IDs.

First private production created MusicVideo 18 but all still-enqueue results were rejected by the Krea caption/lettering contract. Scoped implementation repair is ready for review; do not call the film finished until still and motion ArtJobs render and a probed private MP4 exists.

Merged scoped Krea2 scene-prompt repair in Conductor PR #7315 at 75d30d44f7d68cfd6ca4c99de3b9be27f596dfcb after 24 final-head CI checks passed, skipped or neutral. GitHub Actions run 43209359458 verified five durable still ArtJobs for MusicVideo 18: s1 68688, s2 68689, s3 68690, s4 68691, s5 68692. They are rendering; no clip ArtJobs or final MP4 yet, so do not mark film delivery done. Resume this same MusicVideo 18 after stills render, request two actual motion clips, and verify 15-second final media.

Producer budget recovery and morning delivery patch under review. One optional clip maximum, 7200-second cutoff for new GPU requests, authored camera presets, overnight retries, private film digest linking, original episodic run and inclusive anime/metal/jaguar series bible. No claim of completed MP4.

2026-11-12 PT review: merged conductor#7322 (squash 24f09f4b, 27 checks green/skipped on
head c8025a0b; 18 dead-air tests re-run green on a merge with main). Landed the 7200s
per-PT-day cutoff on new GPU requests, one optional hero clip, authored camera presets,
four overnight passes (1:00-3:15am PST) and the private digest link gated on a probed
15s final. Back to ready, not done: MusicVideo 18 stills 68688-68692 still need to
render and a probed private MP4 must exist. Next: let the overnight passes resume
MusicVideo 18, then record the final ArtImage id here.

First private film delivered and independently verified in durable production ledger and Actions output: The Closed Caption Department (MusicVideo 18, final ArtImage 271245), completed 2026-11-13 PT. 15.0 seconds, 1280x720 H.264/AAC, one generated motion clip and four kinetic shots; recorded still ArtJobs 68688-68692 and clip ArtJob 68794. Second private film Plot Assist also completed 2026-11-14 PT (MusicVideo 19, final ArtImage 272338). No public release authorization is inferred.

Pilot actually completed, not merely queued: MusicVideo 18 and final ArtImage 271245, 15-second H.264/AAC privately archived on 2026-11-13 PT. Rendered ArtJobs and independent probe are in the production ledger; a second verified MP4 (MusicVideo 19, final ArtImage 272338) confirms repeatability. Prior pilot implementation PRs conductor#7315 and conductor#7322 are merged. Release approval is separate dead-air/t-007. This resolves the dependency of dead-air/t-004 daily recurring production.
<!-- note:end t-002 -->

## t-008 — Record per-shot render times and skip the optional GPU clip when the queue is congested

<!-- note:begin t-008 -->
Kaizen from conductor#7322 review (2026-11-12 PT). Keep a small per-shot render-time history in production-state.json and have dead_air_produce.py request zero generated clips when recent still renders ran long, so the compositor cut is never waiting on a clip that cannot finish inside the two-hour window. Also add one late-morning catch-up pass, since removing the 10am PT cron left no retry after 3:15am PST. Cover both with tests.

Added observed per-shot still queue waits, congestion-aware optional clip fallback, a late film catch-up pass, and digest/retry/recovery scheduling after the film. Verifying CI on the implementation PR before closing this task.

Merged conductor PR #7405 at 03ba15116e5286deeede3a4d62c4706e4bb6fe64. On final head f84c4054b275ebc330dbba5c88cd3144db1b0e9f, complete Worker PR CI (including full Python test suite), Security Audit, Daily Dream Contract, Process task events and latest Handoff check all passed. The superseded initial template check failed but its corrected rerun passed. Private producer now records observed per-shot ArtJob waits and omits optional hero clips when congested; morning 17:00 UTC catch-up precedes 17:30 UTC digest, with retry and sentinel timing updated. Digest discloses shared PR entries and absence of new Comfy ArtJob evidence. No public release.
<!-- note:end t-008 -->

## t-009 — Enforce daily fresh-asset evidence and replenish the private episode slate

<!-- note:begin t-009 -->
Kaizen from the green dead-air/t-008 review of conductor#7405, 2026-11-14 PT. The morning digest should distinguish five independent substantive project improvements from five link-preview cards bundled in one PR, and expose the actual count of new Comfy ArtJobs or other genuinely new finished creative assets. Do not silently classify recycled images or code-drawn preview frames as freshly generated artwork. Keep a rolling seven-day reserve of original Dead Air storyboards so a functioning producer never runs out of work after the three initial episodes. Verify each Pacific day's film against the private MP4 ArtImage and show a no-film alert when it is absent, with exact IDs, status and remediation; never publish automatically.

Authored six additional private 15-second original storyboards for 2026-11-15..2026-11-20 PT, making seven dated unrendered episodes including the existing 2026-11-14 Clap Credit. Each includes five original scene prompts, distinct visual design, three formal cultural references, original voiceover and a bounded optional hero clip. Regression tests validate the full initial seven-day slate and uniqueness. This increment replenishes the content runway; the generalized asset-freshness guard remains separate scope for a subsequent increment. Production is private.

Shipped a major partial increment via merged conductor PR #7406 at edf0d6a2951508d7640e4f45f9617819c584b500, with all four latest final-head workflows green including full Python tests. Six original private 15-second storyboards dated November 15-20 have validated painter prompts, five authored shots each, one optional clip maximum and three documented cultural studies. Together with the existing Clap Credit brief this supplies seven dated upcoming films. Storyboards are production input, not completed ArtImages or delivered videos. Return this nonrecurring task to ready for remaining fresh-asset guard and automatic rolling slate replenishment. Public release remains human gated.

Restored the canonical single-writer 14-asset daily cycle alongside Dead Air (six linked Dream and eight Zuzu/Emperor extras). Added verified ArtJob ID accounting for digest image cards, no-film-today warnings, and a seven-day private storyboard shortage guard. Existing paid-model proposal authoring remains opt-in; autonomous agent docket authoring is reactivated. PR and CI verification follow.

Merged conductor PR #7408 at c5fbb54318a35677ab1b213498593a800d81fe72. All six final-head workflow groups, including the full Python test suite, Security Audit, Daily Dream Contract and Roadmap Audit, completed green. The canonical single-writer v3 Daily Dream is re-enabled alongside Dead Air: six linked Dream rows and eight independent Zuzu/Emperor rows with registered model lanes and fourteen durable ArtJob targets. Morning digest now records submitted ArtJob IDs separately from verified media and distinguishes a same-day finished film from yesterday's premiere. A seven-day original screenplay-runway guard runs in each private producer attempt and agent top-up instructions are restored. No claim that a fresh live fourteen-row bundle or video was created solely by merging this code; confirm on the next scheduled production run. Paid proposal authoring and public release remain gated.
<!-- note:end t-009 -->
