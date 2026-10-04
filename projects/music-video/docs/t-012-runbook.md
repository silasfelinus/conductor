# t-012 runbook: first song on the render box

**Who:** Silas, at Ferngrotto. This is a production deploy to the render box, so no session does it.
**Why:** this is the first real render of the audio lane. Every agent-side piece is already on `main`:

- the ACE-Step song workflow and the `acestep` enqueue engine (kind_robots t-010, #3193);
- relay audio support (conductor t-011, #5506);
- the `audio` tier in `sync-comfy-models` (kind_robots t-012, #3198).

**Time:**
- About 10 minutes of hands-on work.
- The ~9.5 GiB model download on top of that.
- The first song takes a cold model load (30-90 s) plus generation.

The model choice, node names and file list come from [`ace-step-spike.md`](ace-step-spike.md). Anything that file marks **UNVERIFIED** gets confirmed in step 5 below.

## 1. Stage the four ACE-Step files on the share

The sync script only copies from the share to local disk, so the files have to land on Alexandria first. They come from `Comfy-Org/ace_step_1.5_ComfyUI_files` on Hugging Face (MIT licence) and go into the same category folders the other models use:

```powershell
cd Z:\ai\models
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

## 2. Copy them to local disk

```powershell
cd D:\code\kind_robots
git pull --ff-only
.\scripts\sync-comfy-models.ps1 -Local D:\comfy\comfy-fast\models -Tier audio -DryRun   # expect 4 COPY rows, ~9.5 GiB
.\scripts\sync-comfy-models.ps1 -Local D:\comfy\comfy-fast\models -Tier audio -Yes
```

## 3. Make sure ComfyUI has the ACE-Step 1.5 nodes

The nodes are `TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio` and `SaveAudioAdvanced`. They live in current ComfyUI master; older stable builds lag behind.

ComfyUI lives at `D:\comfy\comfy-fast` (a venv install; `COMFY_DIR` in
`ops/home-server/ecosystem.config.js`), not `D:\ComfyUI`. Update it while the queue is quiet, and
write down the current commit first so a broken custom node can be rolled back with
`git checkout <sha>`:

```powershell
cd D:\comfy\comfy-fast
git rev-parse --short HEAD
git pull --ff-only
.\venv\Scripts\python.exe -m pip install -r requirements.txt
cd D:\code\conductor
git pull --ff-only
cd ops\home-server
pm2 restart ecosystem.config.js --only comfyui --update-env
Start-Sleep -Seconds 90
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

From any shell with an admin `KR_API_TOKEN` set:

```powershell
cd D:\code\conductor
python scripts\build_music_video.py --title "t-012 smoke test" --pitch "A small brass robot hums to the tomatoes on a rooftop garden at dusk" --duration 30 --bpm 110 --genre "lofi synth pop" --mood "warm" --vocal female
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
