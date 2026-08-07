# AI Art Academy — t-044 (Kontext LoRA loading fix) verification run log

Historical live-verification history for `ai-art-academy/t-044` ("kind_robots: fix Kontext
LoRA loading -- every lora_name naming convention rejected by ComfyUI as not-in-list"),
moved out of `roadmap.yaml`'s task note by `ai-art-academy/t-010` lane 2 (roadmap accuracy,
2026-08-07) so the roadmap note stays short enough to select from quickly — the same
note-bloat fix already applied once to `t-010`'s own note (see
`continuous-improvement-run-log.md`). The roadmap task itself now carries only the current
status plus a pointer to this file; this is the append-only, most-recent-first provenance
record for every live-verification attempt.

Entries below the 2026-08-07 recheck are unedited except for de-indentation; nothing was
reworded or summarized in the move.

---

LIVE VERIFICATION RECHECK 2026-08-07 (~02:35 UTC, conductor scheduled agent run, session
claude-conductor-scheduled-20260807T022853Z-t010, lane 2 roadmap accuracy): Re-checked the
two ArtJobs left in the queue by the 2026-08-05 live-verification attempt rather than
re-submitting (per that entry's own instruction — re-check first, don't spend mana again).
`python scripts/recheck_render_queue.py` now reports the relay as **draining**, not stuck:
queueDepth PENDING=3046/RUNNING=1/DONE=3198/CANCELLED=816 (all-time), 24h window
PENDING=69 added vs **DONE=103 completed** (real throughput, a sharp change from the
2026-08-05 reading of DONE=2 in the same window), zero recent failures. This looks like
the `connection-refused`-to-ComfyUI incident from 2026-08-05 has resolved and the relay is
processing its backlog. However, `GET /api/art/queue/7622` and `/7623` (the two specific
jobs from the 2026-08-05 attempt) show **both still frozen at `PENDING`, `createdAt` ==
`updatedAt`** (2026-08-05T02:33:18.922Z / T02:33:25.203Z) — completely unchanged since
creation, not yet reached by the drain. The overall queue's oldest-pending job is a
different, older job (id 4658, ~124.1h) — plausible the relay is processing roughly
oldest-first and simply hasn't reached 7622/7623's position yet, or they are individually
stuck for an unrelated reason; not enough evidence to tell which from this vantage point.
Left `t-044` at `status: ready` / `gate_human: true` / `soft_gate: true` unchanged — no
new information to act on yet, and re-submitting now would duplicate in-flight jobs and
spend mana for no reason while the relay may still reach 7622/7623 on its own. Next cycle:
re-check `GET /api/art/queue/7622` and `/7623` again before doing anything else with this
task; if they complete cleanly (no `value_not_in_list` error) that confirms the fix and
unblocks `t-045` without spending mana. If they're still frozen once the relay is
confirmed fully drained (`recheck_render_queue.py` PENDING near baseline / oldest-pending
age not still climbing from today's 124.1h), that's a signal the fix should be re-verified
with a *fresh* submission instead, since those two specific jobs may be individually stuck
rather than merely queued.

---

LIVE VERIFICATION ATTEMPT 2026-08-05 (~02:33 UTC, conductor scheduled agent run, session
claude-scheduled-20260805T023207Z-aa-t044-liveverify): Silas sent back "I think this is
fixed, please let me know if otherwise" (via Kind Robots For You) and a prior cycle
returned this task to `ready` per its own instruction. Ran the same live test again: `GET
/api/resources` confirmed Resource 1284's `localPath` is still the exact same string that
failed before (`Kontext/SFW/acrylic.safetensors`), likewise Resource 1055
(`Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors`) -- so the DB rows themselves were not
edited. Queued two real jobs anyway (`POST /api/art/enqueue`, `engine: kontext`, same
source image, `loraResourceIds: [1284]` and `[1055]`): ArtJob 7622 and 7623, both HTTP
201. Inspected the resulting job payloads directly: `resolveEnqueueLoraResource()`
correctly resolved `lora_name` to each Resource's own `localPath` in both workflows
(`61.inputs.lora_name: "Kontext/SFW/acrylic.safetensors"` for 7622) -- so the routing side
(PR #1090) is confirmed still working as designed.

COULD NOT COMPLETE VERIFICATION: both jobs sat `PENDING` for the full observation window
(2+ minutes, no `error`, never reached ComfyUI) rather than failing fast with the expected
`value_not_in_list` 400 the way every prior live attempt did within seconds. `python
scripts/recheck_render_queue.py` explains why -- this is a separate, severe infrastructure
incident, not this task's bug: queue depth PENDING=3140 (oldest job age ~76.3h), 24h
window shows PENDING=2749 added vs DONE=2 completed, and 16 of the last 25 failures are
`connection-refused` to ComfyUI (the relay's own local ComfyUI process appears down or
unreachable, not merely slow). This is a much larger and more severe backlog than the
same-day 2026-08-04 mural-design entries in root `TALKBACK.md` (which were single stuck
jobs on an otherwise-answering relay) -- filed as its own incident there rather than
duplicated here. Jobs 7622/7623 are left in the queue; once the relay recovers, re-check
them directly (`GET /api/art/queue/7622` and `/7623`) instead of re-submitting -- if they
complete without the `value_not_in_list` error, that confirms t-044's fix without spending
mana again. `soft_gate: true` added (this is a tooling/infra failure blocking
verification, not a new gate on the content itself -- `gate_human: true` and `status:
ready` are left unchanged so the original Silas-only diagnostic path this task also
depends on is unaffected). Released the claim uncompleted rather than guessing at an
outcome.

---

LIVE VERIFICATION 2026-07-28 (~14:22 UTC, conductor Reviewer scheduled run, session
2026-07-28T140745-conductor-scheduled-aa-t044-liveverify): Ran the exact test the prior
note called for -- POST /api/art/enqueue against https://kind-robots.vercel.app (the live
production API, reachable with KR_API_TOKEN), engine: kontext, source image = the
project's own rights-clean projects/images/ai-art-academy-card.webp. TWO real ArtJobs,
both FAILED with the identical pre-PR-#1090 error: ArtJob 2773 (Kontext-native LoRA,
Resource 1284, localPath "Kontext/SFW/acrylic.safetensors") -- ComfyUI /prompt HTTP 400
`lora_name: 'Kontext/SFW/acrylic.safetensors' not in (list of length 2096)`; ArtJob 2774
(FLUX-dev LoRA, Resource 1055, localPath "Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors")
-- same error, `lora_name: 'Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors' not in (list
of length 2096)`. This DISPROVES the prior note's optimistic reading of PR #1090: that PR
fixed the *routing* (`server/utils/artLoraResource.ts`'s `resolveEnqueueLoraResource()`
now reliably forwards the Resource's own `localPath` as `lora_name` instead of a stale
caller-provided string) but did NOT touch the underlying data -- the Resource `localPath`
values in the DB still do not match whatever ComfyUI's local `models/loras` folder scan
actually returns for the `LoraLoaderModelOnly` dropdown. Confirmed with two independent
Resources under two different localPath prefix conventions (`Kontext/SFW/` and
`Flux/SFW/`), both rejected identically, so this is not a one-off bad row -- the whole
convention is off.

FOR SILAS: this task cannot progress further from a conductor sandbox -- there is no code
fix left to guess at (five naming conventions have now failed identically across two
sessions). What's needed is exactly what docs/t-044-comfy-lora-path-diagnostics.md has
asked for since 2026-07-27 and still hasn't been run: from your own Tailscale-connected
machine, save ComfyUI's `/object_info` response and Kind Robots `/api/resources` response
as local JSON files, then run `python scripts/compare_comfy_lora_paths.py --object-info
object-info.json --resources resources.json --output lora-path-report.json` (the
comparator, merged via PR #1212). That report will show which Resource `localPath` values
need correcting in the DB, or reveal a stable prefix-rewrite rule agents can implement in
`resolveEnqueueLoraResource`. Do not commit the captures -- they may expose private model
inventory and local folder paths. TO APPROVE: once the DB rows are corrected (or a rewrite
rule is implemented and deployed), set `status: ready` so the next cycle re-runs this same
live test -- the exact repro is saved (POST /api/art/enqueue, engine: kontext,
loraResourceIds: [1284] or [1055], sourceImageBase64 from
projects/images/ai-art-academy-card.webp) and will confirm before marking t-044 done. This
unblocks t-045.

---

ROADMAP-ACCURACY UPDATE 2026-07-28 (~09:30 UTC, conductor Reviewer sweep,
claude-conductor-agentrun-20260728-aa-t010-lane2): Silas merged kind_robots PR #1090
("Resolve Resource LoRAs and add WAN/LTX video support", squash-equivalent, merged
directly by silasfelinus) at 09:19:23Z -- this is the shared resolver this task's own note
called for. `server/utils/artLoraResource.ts`'s `resolveEnqueueLoraResource()` now
resolves every Kontext/Krea2/Flux2/LTX/WAN enqueue request's `loraName`/`loraResourceIds`
through the Resource table before building the Comfy workflow (exact `localPath` match
first, then name/label/source-URL match, then unique basename/stem match), rejecting
inaccessible, ambiguous, or pathless selections up front instead of letting a stale
caller-provided string reach Comfy. `server/api/art/enqueue.post.ts` now calls this
resolver before `buildJobPayload`, so the workflow's `lora_name` node input is always the
Resource's own authoritative `localPath`, not whatever the caller happened to send. This
is architecturally exactly the fix this task's note called for ("implement one shared
resolver ... that maps a Resource's localPath to whatever ComfyUI expects"), and its
timing (right after the FOR SILAS diagnostics handoff referencing PR #1212's comparator)
strongly suggests Silas ran the private relay capture and used it to correct the
underlying data/path mismatch, not just the routing bug. NOT independently live-verified
this cycle (no live relay/DATABASE_URL access from this sandbox, same limitation as every
prior note on this task) -- per this task's own instruction, returning to `ready` rather
than `done`: the next cycle with live access should run one Kontext-native and one
FLUX-dev LoRA through the real queue (POST /api/art/enqueue) and confirm ComfyUI accepts
the workflow and saves an image before marking this `done`, which will unblock t-045 via
resolve_deps.py.

---

Filed 2026-07-27 from t-004's live-render A/B pass (docs/style-remix-configs.yaml). t-037
(merged 2026-07-26) wired a LoraLoaderModelOnly node into buildKontextWorkflow but
explicitly flagged it as not yet verified against a real render. This session ran that
verification for real via POST /api/art/enqueue {engine:"kontext", loraName,
loraStrength} and it fails 100% of the time: ComfyUI rejects every lora_name value with
`{'61': {'errors': [{'type': 'value_not_in_list', ... 'details': "lora_name: '<value>' not
in (list of length 2096)" ...}]}}`. FOUR independent naming conventions were tried and all
four failed the same way (see style-remix-configs.yaml's header comment for full detail
and ArtJob ids):
  1. the style-lora-registry.md HF repo name (e.g.
     "UmeAiRT/FLUX.1-dev-LoRA-Impressionism") -- ArtJob 2603
  2. the Resource table's `localPath` under Kontext/ (e.g.
     "Kontext/SFW/impressionist.safetensors") -- ArtJob 2609
  3. the Resource table's `localPath` under FLUX/ -- the EXACT string
     art-styler.vue's own production BUILTIN_STYLES sends today for
     these same styles (e.g. "FLUX/impressionist.safetensors"), tried
     both with forward slash (ArtJob 2611) and backslash (matching the
     relay's Windows client id "Silas-PC-prompt-...")
  4. the bare filename with no folder prefix ("impressionist.safetensors")
     -- ArtJob 2620
Since attempt #3 is the literal string production's Remix Studio already sends for
impressionism/watercolor/oil-painting/illuminated-manuscript, this strongly suggests
LoRA-mode remixes are ALREADY silently broken in production for every BUILTIN_STYLES entry
today, not just this task's registry-derived candidates -- worth checking independent of
the Academy curriculum scope. GET /api/resources confirms 47 Kontext-native LoRA files ARE
cataloged in the DB, so the files plausibly exist on the relay's disk; the mismatch is
between whatever string the KR database stores as `localPath` and whatever string
ComfyUI's local `models/loras` folder scan actually returns for the LoraLoaderModelOnly
node's dropdown. This needs someone with direct access to the relay (or its ComfyUI
/object_info, reachable only from Silas's own Tailscale-connected browser per
stores/serverStore.ts's fetchComfyObjectInfo -- not reachable from a conductor sandbox) to
read the actual valid `lora_name` list and compare it against the DB's localPath values,
then either fix the DB records to match reality or add a normalization step in
buildKontextWorkflow / simpleCheckpointWorkflow.ts (also affected, same lora_name
pass-through pattern) that maps a Resource's localPath to whatever ComfyUI expects.
Unblocks re-running t-004's A/B for impressionism, illuminated-manuscript, watercolor,
oil-painting, and pop-art (loraPath/loraTrigger/loraWeight already recorded in
style-remix-configs.yaml, ready to re-test the moment this is fixed) plus the other 5
styles whose LoRA candidates need downloading to the relay first (see the same file's
per-style `deployment_gap` notes).

Connector Worker claim for the highest-priority eligible ready task after the concurrent
t-010 cycle completed.

Added an offline, default-deny comparator and focused tests so the relay's authoritative
ComfyUI LoRA dropdown can be reconciled with Kind Robots Resource localPath values without
further path guessing. The final runtime fix still requires one private relay capture.

FOR SILAS: PR #1212 merged the offline ComfyUI LoRA path comparator and tests. The tool is
`scripts/compare_comfy_lora_paths.py`; the exact private capture/run instructions are in
`projects/ai-art-academy/docs/t-044-comfy-lora-path-diagnostics.md`. It compares Kind
Robots Resource `localPath` values against ComfyUI's authoritative `LoraLoaderModelOnly`
dropdown, accepts normalized exact or unique-basename matches, and refuses ambiguous
guesses. TO RESUME: from a Tailscale-connected machine, save ComfyUI `/object_info` and
Kind Robots `/api/resources` as private local JSON files, run the documented comparator
command, and use the report to correct exact Resource paths or implement one shared
resolver. Do not commit the captures because they may expose private model inventory and
local paths. Before marking this task done, run one Kontext-native and one FLUX-dev LoRA
through the real queue and confirm ComfyUI accepts the workflow and saves an image. Then
return t-044 to ready for the implementation/live-verification pass; this unblocks t-045.

SENT BACK by silasfelinus via Kind Robots For You. I think this is fixed, please let me
know if otherwise.
