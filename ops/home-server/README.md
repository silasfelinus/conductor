# Home Server Supervision — ComfyUI + Stable Diffusion (A1111) auto-restart

Keeps the two art backends on Silas's Windows box alive without hand-launching
`.bat` files: crash → auto-restart, reboot → auto-start, plus an optional
health watchdog. Uses **pm2**, which runs fine on Windows.

Files in this folder:

| File | What it is |
|---|---|
| `ecosystem.config.js` | pm2 process definitions for `comfyui` and `sd-webui` (plus opt-in `kr-relay` and `kr-download`) |
| `healthcheck.ps1` | optional watchdog — probes the HTTP health endpoints and `pm2 restart`s a hung process |
| `relay_agent.py` | pull-based bridge: claims ArtJobs from kind_robots and drives local ComfyUI/A1111 (enable after art-generator-connect/t-010 deploys) |
| `relay_download_agent.py` | pull-based model downloader: claims queued LoRA/checkpoint downloads, fetches them onto the engine dirs, and catalogs them as Resources (the `kr-download` app) |
| `start-engines.bat` | double-click launcher: starts both engines (no-op if running) and attaches the live log stream — the old bats' echo, without owning the processes |

---

## Why not just keep using the .bat files?

You can — pm2 *can* supervise a `.bat` — but it's the worse option:

- pm2 monitors the `cmd.exe` wrapper, not Python. If Python crashes and the
  bat lingers (or has a `pause`), pm2 thinks everything is fine and never restarts.
- A bat that ends in `pause` blocks unattended restarts entirely.

The fix is to point pm2 at **the same Python command the bat runs**, so pm2
watches the real process. The ecosystem file does exactly that; you only need
to fill in your install paths. (A bat-wrapper fallback is documented at the
bottom if you'd rather not unpack a bat.)

## One-time setup (PowerShell, as your normal user)

```powershell
# 1. Install pm2 (needs Node.js; you already have it for kind_robots)
npm install -g pm2

# 2. Verify the two *_DIR paths at the top of ecosystem.config.js
#    (pre-filled from startcomfyfast.bat / webui-user.bat, 2026-07-05:
#     D:\comfy\comfy-fast and D:\code\sd-webui-forge-neo)

# 3. Stop any copies still running from the old bats, then start under pm2
cd <this folder>   # wherever you checked out conductor/ops/home-server
pm2 start ecosystem.config.js

# 4. Verify
pm2 status          # both should say "online"
pm2 logs comfyui    # watch ComfyUI boot; Ctrl+C to detach
curl http://127.0.0.1:8188/system_stats       # ComfyUI health
curl http://127.0.0.1:7860/sdapi/v1/progress  # A1111 health (needs --api)

# 5. Freeze the process list so pm2 can restore it
pm2 save
```

### Start on boot

Two options, pick one:

**Option A — pm2 as a real Windows service (recommended for a server):**
survives reboot with no login. Uses [`pm2-installer`](https://github.com/jessety/pm2-installer):

```powershell
# In an *admin* PowerShell:
git clone https://github.com/jessety/pm2-installer
cd pm2-installer
npm run configure
npm run setup
# then, back as your user: pm2 save  (the service resurrects the saved list)
```

**Option B — start at logon (RECOMMENDED — simplest, fine if the box gets logged into):**

```powershell
npm install -g pm2-windows-startup
pm2-startup install
pm2 save
```

> Field note (2026-07-05): Option A's `npm run setup` looped "Stopped…" on
> Silas-PC — pm2-installer's service fails to start unless `npm run configure`
> ran first (it unifies `PM2_HOME` at `C:\ProgramData\pm2\home` for the service
> AND your shell; otherwise the service resurrects from an empty home while
> your `pm2 save` wrote to your user profile → reboot brings up nothing).
> To back out a half-installed service: `cd pm2-installer; npm run deconfigure;
> npm run remove`, then use Option B. Tradeoff: Option B starts apps at
> *logon*, not boot — a machine idling at the login screen runs nothing.

### Gotcha: WSL pm2 ≠ Windows pm2

There are two pm2 worlds on this box and they don't see each other. A shell
prompt like `silasfelinus@Silas-PC:/mnt/d/...$` means WSL — its pm2 daemon
(`/home/<user>/.pm2`) has its own empty process list, and `pm2 status` there
will happily show a blank table while the Windows engines are running fine.
The engines are Windows apps: **always run pm2 commands for them from
PowerShell/cmd**, and if a fresh Windows daemon comes up empty after a
reboot, `pm2 resurrect` restores the last `pm2 save`d list. (`pm2 kill` in
WSL cleans up an accidentally spawned Linux daemon; harmless either way.)

### Optional: health watchdog

pm2 restarts a process that *exits*, but not one that hangs (e.g. CUDA wedge
where the process is alive but the API stops answering). `healthcheck.ps1`
covers that gap. Register it in Task Scheduler to run every 5 minutes:

```powershell
schtasks /Create /SC MINUTE /MO 5 /TN "AI-Backends-Healthcheck" `
  /TR "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\path\to\conductor\ops\home-server\healthcheck.ps1\""
```

### Email alerts on restart

The watchdog can email you when it has to restart a hung backend (and, more
importantly, when a restart *doesn't* bring it back). It reuses the same Brevo
transactional-email account as the daily digest — no new provider. Set these
once on the box, then open a **new** shell so `schtasks` picks them up:

```powershell
setx BREVO_API_KEY "your-brevo-key"
setx DIGEST_TO     "silasfelinus@gmail.com"     # or ALERT_TO to override
setx DIGEST_FROM   "ops@your-verified-sender"    # or ALERT_FROM; must be a Brevo-verified sender
# optional: setx ALERT_COOLDOWN_MINUTES "60"     # min gap between repeat emails per backend (default 60)
```

With no `BREVO_API_KEY` set the watchdog still restarts — it just won't email.
A per-backend cooldown (default 60 min, in `logs\alert-state.json`) keeps a
flapping process from emailing every 5-minute tick.

Two layers of coverage:

- **This watchdog** catches a *hung or crashed* ComfyUI/SD backend on a box
  that's still online, restarts it, and emails the outcome.
- **CI** (`auto-art-generate.yml`) catches the box being *entirely
  unreachable* — it probes `media.acrocatranch.com` each run and emails on the
  down↔up transition (a dead box can't email you itself). Those alerts use the
  repo's existing `BREVO_API_KEY` / `DIGEST_*` GitHub Actions secrets.

## Day-to-day commands

```powershell
pm2 status                  # what's running
pm2 restart comfyui         # bounce one backend
pm2 restart sd-webui
pm2 stop all                # free the GPU (e.g. before gaming)
pm2 start all
pm2 logs sd-webui --lines 200
```

## What carried over from the old bats (and what deliberately didn't)

Checklist against `startcomfyfast.bat` / `webui-user.bat` (2026-07-05):

| Old bat behavior | In the pm2 kit? |
|---|---|
| ComfyUI: venv python, `--listen 127.0.0.1 --port 8188 --enable-cors-header` | ✅ verbatim in `ecosystem.config.js` |
| Forge: full `COMMANDLINE_ARGS` — `--api --listen --cuda-malloc`, Z:\ model dirs, `--cors-allow-origins` (kindrobots.org, vercel, localhost:3000/3001), `--xformers --skip-python-version-check --reserve-vram 2` | ✅ verbatim, passed straight to `launch.py` |
| Tailscale Serve (`serve --bg` → 443 for comfy, `--https=8443` for forge) | ⚠️ **not pm2-managed — it doesn't need to be.** `tailscale serve --bg` config persists in tailscaled across reboots. Run the two commands once (below), confirm with `tailscale serve status`, done. |
| pip repair / ensurepip bootstrap (webui-user.bat) | ❌ intentionally left out — that's a one-time repair job, not supervision. Keep the old bat around; if Python ever breaks, run it once by hand. |
| `pause` at the end | ❌ dropped — it's what makes bats un-automatable. |

### Tailscale Serve (one-time)

```powershell
& "C:\Program Files\Tailscale\tailscale.exe" serve --bg http://127.0.0.1:8188
& "C:\Program Files\Tailscale\tailscale.exe" serve --bg --https=8443 http://127.0.0.1:7860
& "C:\Program Files\Tailscale\tailscale.exe" serve status   # verify both mappings
```

If both mappings already show in `serve status` from your old bat runs, there's
nothing to do — the config is already persistent.

## The relay agent (kr-relay) — enable after t-010 deploys

`relay_agent.py` closes the autonomous loop: it polls the kind_robots ArtJob
queue outward (claim → generate on localhost → upload via
`/api/art/save-generated` → complete). Pull model, so nothing dials into your
network and queued jobs simply wait whenever the box is down.

The queue endpoints are **live** (kind_robots PR #90, merged 2026-07-05). To
enable: uncomment the `kr-relay` block in `ecosystem.config.js`, set
`KR_RELAY_TOKEN` (your admin user's apiKey) and `KR_RELAY_USER_ID` (that
user's id), then `pm2 start ecosystem.config.js --only kr-relay && pm2 save`.
Needs any Python 3.9+ — stdlib only, no pip installs. Watch it with
`pm2 logs kr-relay`.

## The download agent (kr-download)

`relay_download_agent.py` is the relay's companion for *models*. When you queue
a LoRA or checkpoint from the Discover browser (`/models` → Discover), the
server writes a `DownloadRequest` (PENDING). This agent polls
`/api/lora/download/claim`, downloads the file, drops it into the right engine
directory (LoRA → `Z:/ai/models/Lora`, checkpoint → `Z:/ai/models/Stable-diffusion`,
picked from the row's `resourceType`), catalogs it as a Resource via
`POST /api/resources`, then reports `.../complete` with the new `resourceId`.

Same pull model and stdlib-only footprint as the relay — it reuses
`relay_agent.py`'s `log`/`http_json`/token, so no new setup beyond the token
you already set for kr-relay. To enable:

```powershell
# KR_RELAY_TOKEN is already set (shared with kr-relay). Optionally, for gated
# Civitai downloads that need an API key:
setx KR_CIVITAI_TOKEN "your-civitai-token"
# open a NEW shell after setx, then:
pm2 start ecosystem.config.js --only kr-download
pm2 save
pm2 logs kr-download --lines 20   # expect: "download agent … polling …" idle loop
```

Override `KR_LORA_DIR` / `KR_CHECKPOINT_DIR` only if your engine loads models
from non-default paths. Like the relay, it runs whatever was on disk when pm2
started it — `git pull && pm2 restart kr-download` to update.

### Updating a running relay (e.g. the 2026-07-10 Hair Studio upgrade)

The agent runs whatever `relay_agent.py` was on disk when pm2 started it —
it does not hot-reload. After pulling a conductor update:

```powershell
cd D:\code\conductor   # or wherever the checkout lives
git pull
pm2 restart kr-relay
pm2 logs kr-relay --lines 20   # expect: "claim got 404/None — waiting" idle loop
```

Why the 2026-07-10 update matters: Hair Studio (kind_robots `/stylist`)
enqueues image-to-image Kontext jobs whose payload carries
`images: [{name, imageData}]`. The updated agent uploads those to ComfyUI's
input folder before posting the workflow AND declares
`supportsInputImages: true` when claiming — kind_robots only hands image
jobs to agents that declare it, so a stale agent leaves them waiting
instead of failing them. Verify end-to-end by running a styling in
`/stylist` and watching `pm2 logs kr-relay` for
`uploaded input image kr_kontext_queue_...` followed by the save-generated
upload line.

### Triage: a Hair Studio job enqueues but never completes (2026-07-10 incident)

Observed on the first live test: the job appeared as an ArtJob and sat
there. The /stylist job tile shows which case you're in:

| Tile says | Meaning | Fix |
| --- | --- | --- |
| `queued` (never flips) | No capable agent is claiming. The relay is offline, OR it's running a pre-handshake script (pulled before conductor PR #326 merged) — capable or not, it isn't *declaring* `supportsInputImages`, so kind_robots skips it. | `git pull` (must include #326), `pm2 restart kr-relay`. The stalled job is still PENDING and completes on its own within ~10s of the new agent starting. |
| `rendering` then `failed` | An agent claimed it and the workflow errored. | `pm2 logs kr-relay` has the ComfyUI error (missing model/custom node, upload failure). The tile's Retry re-enqueues. |
| `failed` with a mana/auth message | Enqueue-side problem, nothing to do with the relay. | Check the signed-in user's mana balance / session. |

Timeline of the incident: kind_robots #141 (claim guard) merged 08:47,
conductor #326 (agent declares the capability) merged 08:53 — a relay
pulled/restarted between the two knows *how* to handle image jobs but never
*receives* them. One more pull + restart resolves it.

**Future option — local fast path:** the engines, kind_robots, and conductor
checkouts all live on the same physical drive, so the relay could someday
write finished images straight into the local kind_robots
`public/images/{...}` folder (and just POST the DB record) instead of
round-tripping base64 through the API. Skipped for now — the API path is
simpler and works from anywhere — but the option is recorded in
art-generator-connect/t-012's note if generation volume ever makes it worth it.

### Triage: every render fails and the errors blame the model files (2026-08-25 incident)

Symptom, in the order it actually appeared over ~15 hours — all three are **one
broken `Z:` mount**, and none of them is a prompt problem:

1. `ComfyUI POST /prompt failed ... [WinError 1117] The request could not be
   performed because of an I/O device error: 'Z:\ai\models\unet'`. Raised from
   `folder_paths.get_filename_list()` inside `INPUT_TYPES()`, which enumerates
   the models the box *has* — it runs before ComfyUI looks at anything in the
   submitted graph. WinError 1117 is `ERROR_IO_DEVICE`: the connection object
   exists and its transport is dead.
2. `ComfyUI has no matching file for: CLIPLoader.clip_name='qwen3vl_4b_fp8_scaled
   .safetensors'` for models that are registered and were rendering an hour
   earlier. `folder_paths` re-enumerated a half-readable share and cached a short
   list. The relay now prints how many files ComfyUI listed for that input —
   a name missing from a healthy list is a misnaming; the same name missing from
   a list that has shrunk is a lost mount.
3. `dir Z:\ai\models\unet` → `The system cannot find the path specified`
   (`ERROR_PATH_NOT_FOUND`), i.e. the mapping is simply gone.

**Diagnose in this order:**

```
net use                      REM what is Z: mapped to, and is it "Disconnected"?
dir Z:\                      REM does the root list at all? is `ai\` under it?
dir \\alexandria\<share>\ai\models\unet   REM does the UNC path work when Z: doesn't?
```

If the UNC path works and `Z:` doesn't, that is the whole bug.

**Why it recurs: a mapped drive letter belongs to one Windows logon session.**
A pm2 service, an elevated shell, and your desktop shell can each see a
different `Z:` — or none. That is exactly the split above: ComfyUI held a dead
handle while an interactive `dir` said the path did not exist. Re-running
`net use Z: ...` in your own shell does not fix what the service sees.

**The durable fix is to stop using the letter.** Every model path in
`ecosystem.config.js` derives from `KR_SHARE_ROOT` (default `Z:`), so:

```
setx KR_SHARE_ROOT "//alexandria/<share>"
```

then open a **new** shell (setx only affects new processes) and
`pm2 restart ecosystem.config.js --update-env`. Override `KR_MODEL_ROOT`
instead if the models and the media share live in different places.

ComfyUI's own model paths are **not** in this repo — they are in
`extra_model_paths.yaml` under `D:\comfy\comfy-fast`. Point that at the UNC
path too, and restart ComfyUI so `folder_paths` rebuilds its cached filename
lists; a restart is required either way, because those caches survive the mount
coming back.

### The 2026-08-26 recurrence, and the guard that now stops it

Same root cause, one day later, with a new consequence. alexandria was rebooted
several times while replacing a failed array disk. Each reboot dropped all four
of Silas-PC's SMB mappings:

```
Unavailable  Z:  \\192.168.7.172\pc
```

kr-relay kept polling, kept claiming, and every job died at
`node 3 (CLIPTextEncode): hostbuf_file_reader_read failed` — a *read* failure,
not a not-found: ComfyUI resolved the path from `folder_paths`' cached filename
list and then could not pull bytes through a dead session. **PENDING drained
straight into FAILED at ~5 jobs/min** (7 → 71 in fifteen minutes) while every
health signal stayed green: relay heartbeat checking in, `/system_stats`
answering, `pm2 status` all `online`.

Two guards now exist, both on by default:

**1. The relay will not claim what the box cannot render.** `KR_SHARE_PROBE_PATH`
(defaulted to `KR_MODEL_ROOT` in `ecosystem.config.js`) is read as a directory
before each claim, cached for `KR_SHARE_PROBE_SECONDS` (30). While it fails, the
relay logs once and idles instead of burning the queue:

```
⚠ model share Z:/ai/models is unreachable (OSError: ...) - NOT claiming jobs
  until it returns. Renders would fail on model load and burn their retry
  budget. Check the mount on this box (net use), not the queue.
```

It is a `scandir`, not an `isdir`: a stale SMB handle can satisfy `isdir()` and
still fail every read, which is precisely the 2026-08-25 split above. Unset
`KR_SHARE_PROBE_PATH` to disable the gate entirely.

**2. The LoRA import watcher survives a dead share.** It used to call
`os.makedirs(LORA_IMPORT_DIR)` *above* its poll loop, outside the `except` that
guards every cycle, so a share that was down at startup killed the thread:

```
FileNotFoundError: [WinError 67] The network name cannot be found: 'Z:/'
```

Python kills only that thread, so kr-relay carried on rendering with no importer
and nothing said so. The `makedirs` moved inside the guarded body, and the
thread now runs under a supervisor (`_supervised_lora_watch`) that logs and
restarts anything that escapes.

**Neither guard removes the need to restart ComfyUI once the mount is back.**
`folder_paths` caches its filename lists and does not re-enumerate just because
the share returned — the recovery log line says so on purpose. Order is: fix
the mount → `pm2 restart comfyui` → `pm2 start kr-relay`.

**The mount fix itself is still the `setx KR_SHARE_ROOT` UNC change above.** The
guards convert a NAS reboot from a silent backlog into a visible pause; they do
not stop the mapping from being lost.

**3. `healthcheck.ps1` closes the loop.** A share watchdog now runs *before* the
other two, because both misread a dead mount: the liveness probe sees ComfyUI
answering `/system_stats` with a 200 and is satisfied, and the render-failure
watchdog sees the failure spike and would restart ComfyUI straight back into the
unreadable share, repeatedly. It:

- probes `KR_SHARE_PROBE_PATH` by **enumerating** it (a stale SMB handle passes
  `Test-Path` and still fails every read)
- remaps the drive from `KR_SHARE_UNC` if configured, with stdin redirected from
  `NUL` so a missing credential fails fast instead of blocking a Task Scheduler
  run on an unanswerable username prompt
- **restarts ComfyUI when the share returns** — the step that matters, and the
  one a human kept forgetting
- suppresses the render watchdog's restart while the share is down, and says so
  in the spike email

Configure with:

```
setx KR_SHARE_PROBE_PATH "Z:\ai\models"
setx KR_SHARE_UNC        "\\192.168.7.172\pc"
cmdkey /add:192.168.7.172 /user:silasfelinus /pass
```

`KR_SHARE_UNC` is optional — leave it unset to detect and alert without touching
the mapping. The remap needs the credential in Credential Manager; without it
`net use` has nothing to authenticate with and the watchdog will alert rather
than silently fail.

Together with the relay's share gate the sequence becomes: NAS reboots → relay
stops claiming → healthcheck remaps and restarts ComfyUI → renders resume. No
human in the loop, and the queue is paused rather than consumed throughout.

**4. The watchdog can now tell you it is blind.** On 2026-08-27 ComfyUI was
dead — nothing listening on 8188 — while `\AI-Backends-Healthcheck` ran every
five minutes and exited 0 throughout. The per-target lookup was:

```powershell
$status = (& pm2 jlist | ConvertFrom-Json) | Where-Object { $_.name -eq $t.Name } ...
if (-not $status -or $status.status -ne 'online') { continue }
```

With `$ErrorActionPreference = 'SilentlyContinue'`, **a `pm2 jlist` that returns
nothing is indistinguishable from "the app is deliberately stopped."** The
`.vbs` launches PowerShell `-NonInteractive` under Task Scheduler, so if `pm2`
is not on that context's PATH — or the task runs as a different user than the
one owning the pm2 daemon, which is per-user — every target is skipped and the
script reports success. Same per-logon-session trap as the mapped drive letters,
one layer up.

Now: `pm2 jlist` is read **once** per tick, an empty result is treated as a
fault (logged, emailed once per cooldown, all checks skipped explicitly), and
every tick writes a heartbeat naming the user it ran as and the apps it could
see. A silent log previously could not answer "did the watchdog run?" — the
question that mattered. The log is trimmed to 4000 lines once it passes 8000.

If you get a `WATCHDOG BLIND` email, fix the task's *Run as* account to match
the pm2 daemon owner, or give the `.vbs` an absolute path to `pm2`.

**`extra_model_paths.yaml` is now tracked** at `ops/home-server/extra_model_paths.yaml`
as a reference copy of what belongs at `D:\comfy\comfy-fast\extra_model_paths.yaml`.
It was audited 2026-08-26 against a full directory listing of the share: dead
paths removed, case-duplicates removed (SMB is case-insensitive, so `models/VAE`
and `models/vae` were the same directory scanned twice and listed twice), and
seven real directories added that had never been declared. Every declared path
is a directory scan across SMB on each `folder_paths` refresh, so the duplicates
were costing exactly the I/O that fails first when the mount degrades.

**Then requeue the backlog** from the conductor checkout:

```
python scripts/drain_failed_art_backlog.py --live
```

It renders a canary batch first and refuses to drain if the host is still
broken, so it is safe to run before you are sure the mount is fixed.

## Notes & gotchas

- **A1111 must run with `--api`** or the kind_robots handshake
  (`/sdapi/v1/txt2img`) fails. It's already in the ecosystem args — keep it.
- **`--listen` / `0.0.0.0`** binds beyond localhost so the tailscale interface
  can reach each backend. Tailscale is the only route in; do not port-forward
  these on the router.
- **VRAM contention:** pm2 keeps *both* backends resident. ComfyUI and A1111
  each grab VRAM at load. If one GPU can't hold both, either add
  `--medvram` (A1111) / `--lowvram` (ComfyUI) to the args, or run only one at
  a time (`pm2 stop sd-webui` when doing Flux work, etc.).
- **Model updates / git pulls:** pm2 only supervises the process. Update the
  apps the way you always have, then `pm2 restart <name>`.
- **Logs** land in `ops/home-server/logs/` next to the config (gitignored —
  they stay on the box).

## Fallback: supervising the existing .bat directly

If you'd rather not extract the Python command, this works with caveats:

```js
{
  name: 'comfyui',
  script: 'C:/AI/ComfyUI/run_nvidia_gpu.bat',
  interpreter: 'none',
  windowsHide: true,
  autorestart: true,
}
```

Caveats: remove any `pause` from the bat first; pm2 restarts only when the
*bat* exits (pm2 does kill the whole tree on Windows via `taskkill /T`, so
stop/restart is safe, but crash *detection* is weaker). The healthcheck
watchdog becomes more important in this mode.
