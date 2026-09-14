# scene-animator — task history archive

Full `note:` prose for completed scene-animator tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Build the resumable Scene Animator MVP in Kind Robots

<!-- note:begin t-001 -->
Merged silasfelinus/kind_robots#2072 (squash 0e823d3). Reviewer fixed 6 TypeScript errors the PR CI caught before merging: server/api/scene-animator/index.get.ts included a non-existent ArtJob->ArtImage Prisma relation (ArtJob only has a plain artImageId int column, no declared relation) -- replaced with a batch findMany by id; server/api/scene-animator/source.get.ts passed Content-Length as a string where h9s typed header expects number; stores/sceneAnimatorStore.ts durationSeconds ref was inferred as the literal union from the readonly VIDEO_PRESETS array instead of number, and the first-folder lookup was not guarded against an empty array. All 39 CI checks green after the fix, mergeable_state clean, merged via squash.
<!-- note:end t-001 -->

## t-002 — Confirm the Scene Animator scope with Silas

<!-- note:begin t-002 -->
FOR SILAS: soft checkpoint only; development is not blocked. Review DESIGN-BRIEF.md after the MVP lands and redirect naming, defaults, or workflow if desired. The project is intentionally scoped to internal/admin batch animation, not public publishing.


Closed under Silas's 2026-09-07 human-gate simplification instruction. Accept the implemented internal/admin batch-animation scope and current naming/defaults as the baseline. Future reversible workflow polish is agent-owned; public publishing or outward distribution remains a separate genuine gate if ever added.
<!-- note:end t-002 -->

## t-003 — Harden media-root deployment and source-folder operations

<!-- note:begin t-003 -->
After the MVP establishes the code contract, verify the self-hosted app and media container expose the dedicated kindrobots/animate source tree safely. Prefer a single ANIMATE_PATH/ANIMATE_MEDIA_ORIGIN contract with traversal protection and clear health diagnostics. Any physical mount/container-template change remains an operator step; code and docs should make the required mapping explicit.
RESOLVED: Merged silasfelinus/kind_robots#2108 (squash 6e02168). Admin-only GET /api/scene-animator/health reports which source (ANIMATE_PATH / IMAGES_PATH-derived sibling / local /animate fallback) is in effect plus folder/image counts, or a specific unavailable reason; GET /api/scene-animator no longer hardcodes rootAvailable: true; sceneAnimatorStore surfaces the specific reason through its error banner. Traversal protection was already solid and untouched. 41/41 CI checks green, mergeable_state clean, merged via squash.
<!-- note:end t-003 -->

## t-006 — Make Scene Animator's source root reachable in production, or fail legibly

<!-- note:begin t-006 -->
FOR SILAS: found by you on 2026-09-11 attempting the t-005 confirmation pass. /admin/scene-animator loads but reports "Scene Animator source root is unavailable: /app/animate", so the surface cannot be confirmed and the project cannot close.
This is environment/deployment, not code. server/utils/sceneAnimator.ts resolves its source root from ANIMATE_PATH, falling back to an IMAGES_PATH-derived path, and returns a 503 the moment that path is missing or unreadable inside the container. The value it is resolving to, /app/animate, does not exist in the running Kind Robots container -- so either ANIMATE_PATH is unset and the derived fallback is wrong, or it is set to a directory that was never mounted.
TO UNBLOCK, one of: (a) mount the real scene-source directory into the Kind Robots container and point ANIMATE_PATH at it -- this is the Unraid/compose side, so kindrobots-unraid may be the right home for the actual change; or (b) tell us the path you want it to use and we will wire and document it. Either way the env var belongs in the deployment's documented configuration, since nothing in the repo currently records that Scene Animator needs a mounted volume at all -- which is why this shipped "done" without anyone noticing it could never work in production.
AGENT-ACTIONABLE HALF, do not wait on Silas for it: the failure is currently a bare red string on an otherwise-empty admin page. Make it legible -- name the variable (ANIMATE_PATH), say that it must point at a directory mounted into the container, and distinguish "unset" from "set but missing" from "present but unreadable", which sceneAnimator.ts already tracks internally and then flattens into one message. An admin who sees this should know what to fix.
RESOLVED BY SILAS, 2026-09-11, in session. He recreated the Kind Robots container on Alexandria with the two settings this task was asking for, and the health endpoint now confirms it live:

  GET /api/scene-animator/health ->
  "Scene Animator source root is reachable (0 folders, 0 images)"
  root: /app/animate   source: ANIMATE_PATH   latencyMs: 0

ROOT CAUSE, for the record. This was never a code defect and never a missing feature. docker-compose.yml already had the right shape -- ANIMATE_PATH=/app/animate plus a read-only bind of the host animate tree, with verifySceneAnimatorDeploymentContract.ts asserting both and explicitly forbidding an :rw mount. The running container simply predated that: Silas's Unraid DockerMan template carried neither the animate bind nor the variable, so getSceneAnimatorRoot() fell through both configured tiers to its last-resort fallback, path.resolve(process.cwd(), 'animate') = /app/animate, which did not exist. The 503 was accurate; the deployment had drifted from the compose file that documents it.
The same template was also missing IMAGES_PATH as a VARIABLE (it had only the volume bind). That was provable from the error text rather than guessed: with IMAGES_PATH set, the second tier would have resolved to /app/.output/public/animate, not /app/animate. Silas set both variables in the same pass.
WHAT HE RAN (kept here because the Unraid template is not version-controlled -- it lives in DockerMan on the host, which is exactly how it drifted from compose in the first place):
  -e 'ANIMATE_PATH'='/app/animate'
  -e 'IMAGES_PATH'='/app/.output/public/images'
  -v '/mnt/user/pc/kindrobots/animate/':'/app/animate':'ro'

SILAS'S ARCHITECTURAL REQUIREMENT IS SATISFIED, and was already the design. He raised it directly: "due to the sensitive mature nature of some animation production, it shouldn't be a part of the kind robots directory, but rather part of comfy, or the media folders." /app/animate is only a mount point inside the container; the files live on the media share at /mnt/user/pc/kindrobots/animate, mounted READ-ONLY, so nothing mature is ever in the repo, the image, or writable by the app. Pointing it at a Comfy tree instead is a one-field change to the host path with no code involvement.
CURRENT STATE: reachable, 0 folders / 0 images -- the mount works and the tree is simply empty. Scene Animator expects one subfolder per scene containing stills (.png .jpg .jpeg .webp .gif); loose images at the root register as a single unnamed folder. Dropping content in makes folders appear in the picker with no further configuration.
The agent-actionable half of this task -- making the failure legible by naming ANIMATE_PATH and distinguishing unset / set-but-missing / present-but-unreadable -- is now LOWER VALUE than when it was filed, because `source` already reports which tier answered and that is the distinction that mattered here. Worth keeping as a small improvement, not as a gate. One genuine latent trap remains and is deliberately NOT fixed in this close-out: the third-tier fallback silently resolves inside the application working directory, which for mature content is the worst possible default -- if anyone ever created /app/animate in the image it would work and quietly store that content there. Unreachable under this compose, but it should fail loudly naming ANIMATE_PATH instead. Filed as its own concern rather than reopening this task.
<!-- note:end t-006 -->

## t-008 — Scene Animator clips were flattened to a still by the ArtImage offload

<!-- note:begin t-008 -->
Silas, 2026-09-11: "looks like we have the first animation back from scene animator, and it
didn't make any actual animation, just returned a static image. perhaps a failure of the loop
request?"

NOT the loop request, and not ComfyUI. The render was correct end to end; the frames were
destroyed afterwards, inside Kind Robots, by the ArtImage offload.

Chain: engine 'wan' defaults to the wan-startup-webp preset, so every Scene Animator job has
outputFormat 'webp'. buildVideoOutputNodes() saves that through ComfyUI's SaveAnimatedWEBP,
which emits a real multi-frame WebP (the 2026-09-11 15:31-15:33 comfyui.err.log lines show
WanVAE + WAN22 TI2V-5B loading and a 20-step sample, which is the animation being made). The
relay downloads it and stamps the ArtImage fileType 'webp'. Then offloadArtImageBytes()
classified clips by extension against VIDEO_TYPES = {mp4, webm, mov, mkv}. 'webp' is not in
that set -- it is also the project's default STILL format -- so an animated clip took the
transcode branch, and `sharp(buffer)` defaults to `pages: 1`: it decodes frame 0, silently
discards the rest, writes that single frame to the share, and nulls imageData, which was the
only animated copy left. Measured on a synthetic 8-frame clip: 7390 bytes/8 pages in,
652 bytes/1 page out, no error raised.

FIX: resolveOffloadEncoding() (extracted from offloadArtImageBytes so it can be tested
directly) now asks sharp for the frame count instead of guessing from the extension. A
webp/gif with pages > 1 is written verbatim under its own extension and keeps its stored
fileType; a genuine still, including a one-frame webp, still transcodes exactly as before, so
the storage growth the offload exists to stop is unaffected. Video containers are untouched.

The UI needed no change -- pages/admin/scene-animator.vue already branches <video> vs <img>
and animated WebP plays in an <img>. It was faithfully showing a flattened file.

Regression coverage: utils/scripts/verifyAnimatedArtOffload.test.ts builds a real animated
WebP and asserts frames survive (verified to FAIL against the pre-fix classification), wired
into contract-tests.yml; plus a source-contract check in verifyArtImageOffload.ts that the
helper reads metadata().pages BEFORE re-encoding.

NOT FIXED, deliberately, and worth a look if it ever bites: relay_agent.py's encode_webp()
has the same shape (PIL save without save_all=True), but it is only reached for
media.is_video == False, so no clip passes through it today.
<!-- note:end t-008 -->

## t-009 — Re-render a finished scene from the admin surface

<!-- note:begin t-009 -->
Silas, 2026-09-11, looking at four Done cards holding flattened stills: "We should be
able to resubmit from the scene-animator window."

He was right, and there was no way to. The enqueue dedupe treats PENDING, RUNNING and
DONE alike as reusable, and that check runs BEFORE `retryFailed` is consulted -- so
`retryFailed` only ever rescued FAILED/CANCELLED, and a finished scene was unreachable
from any request the admin UI could send. The per-card "Retry this scene" button only
renders for failed/cancelled cards for exactly that reason.

That is correct behaviour while a finished render IS the render you wanted. t-008 made
it wrong: every completed clip was a flattened still, all DONE, all visibly wrong, none
re-queueable. Worth noting the earlier advice in that session -- "just re-queue with
retryFailed" -- was itself wrong for the same reason, and the screenshot is what caught
it.

FIX: a `force` flag, kept narrow because it is a hole in a guard that exists for good
reasons. It re-queues DONE (and FAILED, so one control serves both); it NEVER duplicates
PENDING/RUNNING -- isActiveStatus is split out of isReusableStatus and checked first,
since the relay renders one clip at a time and a duplicate does not arrive sooner, it
only jumps the queue; it applies to one named sourceFile only, because a folder-wide
force would re-render every finished scene in a batch off a single click; and it
re-reads the live job first, being the one path that enqueues over a job it already saw.
The listing already resolves the newest job per dedupeKey, so a re-submitted job slots
into its card with no listing change. UI: "Re-render this scene" on DONE cards, plus
store.rerenderSource(); a forced request that queues nothing now reports why rather than
leaving the card on its old Done badge looking inert.

Coverage: utils/scripts/verifySceneAnimatorResubmit.test.ts, wired into
contract-tests.yml, pinning both the gate and the wiring. Verified against four
mutations run individually (guard order reversed, force unscoped, live recheck dropped,
UI control unwired). One contract check initially passed mutation 2 -- a multiline regex
matched an unrelated later `requestedSourceFile` -- and was tightened to the statement
before all four were re-confirmed failing. Without that mutation pass the suite would
have shipped a check that did not check.
<!-- note:end t-009 -->

## t-010 — Motion prompt asked for restraint and got it; previews cropped the frame

<!-- note:begin t-010 -->
Silas, 2026-09-11, on the first batch that actually animated: "the animations are pretty
lackluster ... the others have minimal movement, or something completely left field, like
a miniature figure on a segway riding in front of the dog logo for hss". Plus: "I can't
see the entire image on the display."

THREE THINGS.

1. The prompt was five hedges in one sentence -- "subtle coherent motion ... only
plausible ambient movement, gentle secondary motion, and stable cinematic camera
behavior". Every one a vote against movement, and WAN obliged. Rewritten to ask for
deliberate motion and, per Silas ("if there is a figure, they should be animated, wink,
smile, laugh"), to NAME the performance: blink, smile, wink, laugh, head turn, hands with
intent. Subject integrity deliberately untouched -- the Segway rider is what that clause
prevents, and it is the obvious casualty of a "make it more dynamic" retune, so the test
pins both halves together and fails if either goes.

2. negativePrompt shipped as ''. Now carries terms for both observed failure modes:
stillness, and invented subjects.

3. Cards paired a square source against a square clip inside an aspect-video box using
object-cover, so both lost their top and bottom. object-contain letterboxes instead.

TRAP FOUND EN ROUTE: pages/admin/scene-animator.vue had the entire prompt re-typed as
literal HTML in its "Automatic motion direction" panel. Nothing connected the copies, so
tuning the prompt would have left the operator reading the old direction while a different
one was sent -- both halves working, quietly disagreeing. Constants moved to
utils/sceneAnimatorPrompt.ts; the page interpolates them and the test refuses any inlined
copy, including a re-paste of the current text.

Coverage: utils/scripts/verifySceneAnimatorPrompt.test.ts, verified against four
regressions run individually. One initially reported a false pass because the mutation's
anchor did not match the file -- re-run with the right anchor before trusting a mutation
result.
<!-- note:end t-010 -->

## t-011 — Per-image motion direction, editable before re-render

<!-- note:begin t-011 -->
Silas, 2026-09-12: "I should also be able to edit the individual prompts for each image,
and edit them before resubmitting."

A collapsed Motion direction panel per card, badged custom/default: edit, Save prompt,
then Re-render (t-009's button). Use default clears it. Saving deliberately does NOT
enqueue -- an edit is free, a render is minutes of GPU on a box that does one at a time.

THE DELICATE PART WAS THE DEDUPE KEY, not the editor. Every job ever rendered stores a
configKey and dedupeKey from sceneAnimatorConfigKey(). A custom prompt must produce a
DIFFERENT key or an edited prompt collides with the result it was written to replace; a
source without one must produce the EXACT key it always had, or every finished render is
orphaned at once, every card flips to missing, and the next batch redoes the folder. So
the fingerprint is appended and only when custom. The default key is pinned to a literal
in the test and was verified byte-identical to what the pre-change implementation on main
produces -- by extracting and running the old function, not by checking the new code
agrees with itself.

Overrides live in a new SceneAnimatorPrompt table keyed by source SHA-256, so one follows
its image through a rename. prompt.put.ts derives that hash by READING THE FILE and never
accepts one from the body: the hash is the primary key, so a supplied one would retarget
another operator's prompt and skip path containment.

TWO CI FAILURES, both mine, both worth remembering:

(a) The new test imported sceneAnimatorPromptStore.ts -> prisma, which throws at module
scope without DATABASE_URL, so it died on import in the DB-free Contract Tests job. This
was the SECOND occurrence -- verifyAnimatedArtOffload.test.ts did the same thing the day
before (t-008). Both passed locally because the provisioned sandbox exports a dummy
DATABASE_URL, so the local run was never the CI run. Fixed by splitting
sceneAnimatorPromptResolve.ts, and by adding `npm run test:contracts-db-free`, which runs
all 323 contract scripts with the variable stripped. That is the pre-push command; use it.
(A first attempt at a static import-graph guard was deleted after two false positives in
one minute -- a deliberate lazy await import(), and an `import prisma` inside a
template-literal fixture.)

(b) @@index([sourceFolder, sourceFile]) over two utf8mb4 VARCHAR(512) columns is 4096
bytes of key against InnoDB's 3072 limit, so the table could not be created at all -- this
would have failed the PRODUCTION migration, not just the nightly job. Caught by Da Vinci
Seed Verify, which runs on prisma/schema.prisma changes. The index also indexed nothing
anybody queries. Removed, with the byte math recorded at both sites. Could not be
reproduced locally (docker client, no daemon), so CI was the confirmation.

DEPLOY NOTE: this carries a Prisma migration. Unlike the rest of this cycle it needs
`prisma migrate deploy`, or saving a prompt 500s on a missing table.
<!-- note:end t-011 -->
