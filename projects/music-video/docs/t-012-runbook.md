# t-012 runbook: first song on the render box

**Who:** Silas, at Ferngrotto. This is a production deploy to the render box, so no session does it.
**Why:** this is the first real render of the audio lane. Every agent-side piece is already on `main`:

- the ACE-Step song workflow and the `acestep` enqueue engine (kind_robots t-010, #3193);
- relay audio support (conductor t-011, #5506);
- the `audio` tier in `sync-comfy-models` (kind_robots t-012, #3198). This is only for restocking a box from the share; see step 2.

**Time:**
- About 10 minutes of hands-on work.
- The ~9.5 GiB model download, straight to Ferngrotto's local disk, on top of that.
- The first song takes a cold model load (30-90 s) plus generation.

The model choice, node names and file list come from [`ace-step-spike.md`](ace-step-spike.md). Anything that file marks **UNVERIFIED** gets confirmed in step 5 below.

## 1. Download the four ACE-Step files onto Ferngrotto's local disk

ComfyUI loads models from local disk, so download them straight to where it reads them. Don't go through the Alexandria share first. The files come from `Comfy-Org/ace_step_1.5_ComfyUI_files` on Hugging Face (MIT licence). They go into `unet`, `clip` and `vae`. Those are the folders that the workflow's `UNETLoader`, `DualCLIPLoader` and `VAELoader` nodes read from, and the same layout `sync-comfy-models` uses:

```powershell
cd D:\comfy\comfy-fast\models
New-Item -ItemType Directory -Force unet, clip, vae | Out-Null
$base = "https://huggingface.co/Comfy-Org/ace_step_1.5_ComfyUI_files/resolve/main/split_files"
curl.exe -L -o unet\acestep_v1.5_turbo.safetensors "$base/diffusion_models/acestep_v1.5_turbo.safetensors"
curl.exe -L -o clip\qwen_0.6b_ace15.safetensors  "$base/text_encoders/qwen_0.6b_ace15.safetensors"
curl.exe -L -o clip\qwen_1.7b_ace15.safetensors  "$base/text_encoders/qwen_1.7b_ace15.safetensors"
curl.exe -L -o vae\ace_1.5_vae.safetensors       "$base/vae/ace_1.5_vae.safetensors"
dir unet\acestep_v1.5_turbo.safetensors, clip\qwen_*_ace15.safetensors, vae\ace_1.5_vae.safetensors
```

Expected sizes:

| File | Bytes |
|---|---|
| `acestep_v1.5_turbo.safetensors` | 4,787,825,604 |
| `qwen_0.6b_ace15.safetensors` | 1,191,588,248 |
| `qwen_1.7b_ace15.safetensors` | 3,708,523,360 |
| `ace_1.5_vae.safetensors` | 337,431,732 |

A file that is much smaller than its expected size is usually a saved Hugging Face error page. Delete it and run that `curl.exe` line again.

## 2. (Optional) Archive a copy on Alexandria

You can skip this step for t-012. Do it only if you want the share to keep its full set of models, so that a rebuilt or second render box can restock with `sync-comfy-models -Tier audio`. That script only copies share to local, so the upload has to be done by hand:

```powershell
robocopy D:\comfy\comfy-fast\models\unet Z:\ai\models\unet acestep_v1.5_turbo.safetensors
robocopy D:\comfy\comfy-fast\models\clip Z:\ai\models\clip qwen_0.6b_ace15.safetensors qwen_1.7b_ace15.safetensors
robocopy D:\comfy\comfy-fast\models\vae  Z:\ai\models\vae  ace_1.5_vae.safetensors
```

## 3. Make sure ComfyUI has the ACE-Step 1.5 nodes

The nodes are `TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio` and `SaveAudioAdvanced`. They live in current ComfyUI master; older stable builds lag behind.

ComfyUI lives at `D:\comfy\comfy-fast` (a venv install; `COMFY_DIR` in
`ops/home-server/ecosystem.config.js`), not `D:\ComfyUI`. Update it while the queue is quiet, and
write down the current commit first so a broken custom node can be rolled back with
`git checkout <sha>`.

This checkout follows release **tags**, not a branch. `git pull` therefore fails with
"You are not currently on a branch". Fetch the tags and check out the newest release
instead (ComfyUI v0.39.0 has the ACE-Step 1.5 nodes; 2026-10-06 run):

```powershell
cd D:\comfy\comfy-fast
git rev-parse --short HEAD          # rollback point
git describe --tags                 # the release you are on
git fetch --tags
git checkout v0.39.0                # or a newer release tag
.\venv\Scripts\python.exe -m pip install -r requirements.txt
cd D:\code\conductor
git pull --ff-only
cd ops\home-server
```

Then restart ComfyUI with **stop, clear the port, start**, not `pm2 restart`. On 2026-10-06
a plain restart left the old ComfyUI process holding port 8188 outside pm2's tracking.
`pm2 pid comfyui` read `0`, and the new copy crash-looped on "Port 8188 is already in use":

```powershell
pm2 stop comfyui
Get-NetTCPConnection -LocalPort 8188 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
Start-Sleep -Seconds 3
pm2 start ecosystem.config.js --only comfyui --update-env
Start-Sleep -Seconds 90
pm2 pid comfyui                                                                    # a real PID, not 0
Get-NetTCPConnection -LocalPort 8188 -State Listen | Select-Object OwningProcess   # the same PID
(curl.exe -s http://127.0.0.1:8188/system_stats | ConvertFrom-Json).system.comfyui_version
foreach ($n in 'TextEncodeAceStepAudio1.5','EmptyAceStep1.5LatentAudio','SaveAudioAdvanced') { curl.exe -s -o NUL -w "$n %{http_code}`n" "http://127.0.0.1:8188/object_info/$n" }   # expect 200 three times
```

A 404 means ComfyUI is still too old. Update ComfyUI again (or switch to nightly) before going on.

## 4. Update the relay so it claims song jobs

The relay code changed (`supportsAudio`); its pm2 config did not. A pull plus a restart is enough, and no `pm2 delete` is needed:

```powershell
cd D:\code\conductor
git pull --ff-only
pm2 restart kr-relay
pm2 logs kr-relay --lines 20
```

Until this restart, song jobs sit in PENDING. The kind_robots claim gate holds them back from any relay that does not advertise audio support.

## 5. Run one 30-second song

From any shell with an admin `KR_API_TOKEN` set. On Ferngrotto, `python` on the PATH is the
Microsoft Store stub ("not a valid application for this OS platform"), so call the real
interpreter, the same one the relay uses. The script needs only the standard library:

```powershell
cd D:\code\conductor
C:\Python312\python.exe scripts\build_music_video.py --title "t-012 smoke test" --pitch "A small brass robot hums to the tomatoes on a rooftop garden at dusk" --duration 30 --bpm 110 --genre "lofi synth pop" --mood "warm" --vocal female
```

- It creates the video, writes lyrics, queues the song, and plans and queues the scene stills. It then exits with code 3 while the renders run. Note the `--video-id` it prints.
- Re-run with `--video-id <id> --wait` to follow it to the end. That step also assembles an MP4 locally, which proves the whole pipeline. It is not needed for t-012 itself.
- **Song check:** open `https://kindrobots.org/api/art/images/<song artImageId>/file` while signed in as an admin, and confirm the mp3 plays.
  - `GET /api/music-video/<id>/song` shows the `artImageId` once the job is DONE.

**Record these back on t-012 to close the spike's UNVERIFIED items:**

- peak VRAM during the song;
- cold and warm wall-clock time;
- mp3 size;
- whether `SaveAudioAdvanced` accepted the `format` / `format.quality` encoding as sent.

If ComfyUI rejects that encoding, `SaveAudioMP3` is the documented fallback (inputs: `audio`, `filename_prefix`, `quality`). Paste the node error onto the task, and an agent will swap the output node in `server/api/comfy/acestep/utils/workflow.ts`.

## Done means

- `pm2 logs kr-relay` shows the song job claimed and completed.
- The audio ArtImage plays.
- t-012 is set to `done` with `approved_by_human: true`. That unblocks the first-run trailer (t-015).
