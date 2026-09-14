# coat-dance — task history archive

Full `note:` prose for completed coat-dance tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Draft production brief and asset checklist

<!-- note:begin t-001 -->
FOR SILAS: Production brief written to projects/coat-dance/BRIEF.md. It covers the core premise, target runtime assumptions, a required-assets checklist, and a suggested (not-yet-created) working-folder layout.

Correction worth flagging: the brief's source note assumed the original video still needed to be provided — it doesn't. `coat dance_x264.mp4` is already in projects/coat-dance/ (has been since 2026-07-17). Read directly from the file (no ffmpeg in this sandbox, so parsed the MP4 box headers by hand): 720x480 H.264, ~5:32 runtime, and it already has a synced audio track (44.1kHz) — not silent, contrary to what "provide the original video" implied.

ANSWERED 2026-07-25: Silas confirmed Q1 (music direction) — "there is very specific audio used in the video, currently no interest in changing it at this point." Original audio only, preserved as-is; no new/replacement track, no blend. Recorded in BRIEF.md's Open Questions section (also resolves Q2 by implication: the audio is intentional, not disposable). Q3-Q5 (tool inventory, surviving stills/notes, target runtime length) remain open but are not blockers for t-002. Unblocking t-002 (video beat-transcription tool research). moves from blocked to ready.
<!-- note:end t-001 -->

## t-002 — Research video beat transcription and shot-slicing tools

<!-- note:begin t-002 -->
Identify practical tools or scripts for segmenting the source dance video by movement beats, shot changes, audio events, and pose/action changes. Compare options such as ffmpeg scene detection, optical-flow/pose analysis, transcript notes, manual beat sheets, and any Comfy/LAX/Wan-friendly preprocessing.
FOR SILAS: Tool-survey draft at projects/coat-dance/RESEARCH-t002-beat-transcription-tools.md (2026-07-29). Contains: (1) a shot/scene-detection pick (ffmpeg scdet as a cheap first pass; PySceneDetect kept in reserve only if the edit later adds cutaways, since the source is one continuous take), (2) an audio beat/onset pick (librosa by default, madmom as a fallback if the 2006 live-performance room audio proves too irregular for librosa's beat tracker), and (3) a movement-detection recommendation to layer MediaPipe Pose (performer) with dense optical flow (the coat itself, which has no skeleton to track) since no single tool covers both duet partners -- plus a suggested t-003 pipeline order for turning these into one merged beat-map table. TO APPROVE: read the doc; if the tool picks look right, set status: ready on t-003 (Create source-video beat map template) yourself, or leave a note here if you want a different tool swapped in first. Also note the doc's caveat: this sandbox has neither ffmpeg nor a Python audio/video stack, so nothing ran against the real file -- it's a selection, not a produced beat map. It re-confirms BRIEF.md's open Q3 (tool inventory in the real render environment) as the actual blocker before t-003's template can be exercised for real, so that's worth resolving alongside/before unblocking t-003. What unblocks: t-003 (currently `blocked` on this task) once you flip it to `ready` -- see BRIEF.md's suggested-folder plan for where its output (source/beatmap.md) should land.


SENT BACK by silasfelinus via Kind Robots For You. I approve the default suggestions, and just need info on how to proceed. if I need to download tools, tell me where to put them.

RESOLVED 2026-08-11: added a "5. Installation -- where to put these tools" section to
RESEARCH-t002-beat-transcription-tools.md answering the direct question -- ffmpeg is a
system package (brew/apt, install wherever the pipeline shell runs), the Python packages
(librosa, madmom, mediapipe, opencv-python, scenedetect) go in a dedicated virtualenv kept
separate from any ComfyUI env (mediapipe/madmom pin numpy/protobuf versions that can
conflict), and none of it needs a GPU except optionally mediapipe/optical-flow (both run
fine on CPU for one 5:32 clip) -- simplest to put it on whatever machine will run t-006's
ComfyUI pipeline so the beat map feeds straight in. Per Silas's own approval above and this
task's own "set status: ready on t-003 yourself" instruction, t-003 is now unblocked to
ready. Closing t-002 done -- deliverable (tool survey + install answer) complete and
approved; nothing further needed from Silas on this task specifically. BRIEF.md's Q3 (tool
inventory actually confirmed present in the real render environment) remains open and is
t-003/t-006's concern, not this task's.
<!-- note:end t-002 -->
