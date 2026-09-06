# Home Server Supervision — ComfyUI auto-restart

Keeps the art backend on Silas's Windows box alive without hand-launching
`.bat` files: crash → auto-restart, reboot → auto-start, plus an optional
health watchdog. Uses **pm2**, which runs fine on Windows.

> **A1111 / Forge was removed 2026-08-29.** It had not been used in a long
> time, and its pm2 entry meant `pm2 restart ecosystem.config.js` silently
> started it and held VRAM that ComfyUI wanted. ComfyUI is the only engine this
> box runs. If you find an `sd-webui` process still registered from an older
> `pm2 save`, clear it with `pm2 delete sd-webui && pm2 save`.

Files in this folder:

| File | What it is |
|---|---|
| `ecosystem.config.js` | pm2 process definitions for `comfyui` (plus opt-in `kr-relay` and `kr-download`) |
| `healthcheck.ps1` | optional watchdog — probes the HTTP health endpoints and `pm2 restart`s a hung process |
| `restore-shares.ps1` | logon-time repair for **this box's** SMB drive letters after *it* reboots (healthcheck covers the NAS going away while this box stays up) |
| `preflight.ps1` | read-only "if I reboot now, does it all come back?" check — verifies the **saved** state (persistent mappings, `dump.pm2` and its env), not just the running state |
| `relay_agent.py` | pull-based bridge: claims ArtJobs from kind_robots and drives local ComfyUI (enable after art-generator-connect/t-010 deploys) |
| `relay_download_agent.py` | pull-based model downloader: claims queued LoRA/checkpoint downloads, fetches them onto the engine dirs, and catalogs them as Resources (the `kr-download` app) |
| `start-engines.bat` | double-click launcher: starts both engines (no-op if running) and attaches the live log stream — the old bats' echo, without owning the processes |
| `container_log_triage.py` (now in **kind_robots** `scripts/`, deployed to `/mnt/user/appdata/kind_robots/scripts/`) | daily Unraid User Script: reads every container's logs, collapses them to signatures, reports only what is new, spiking, or newly silent, and commits the digest into this repo in the same run — no pm2 entry, this box is not ferngrotto (see `CONTAINER-LOG-TRIAGE.md`) |

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

# 2. Verify COMFY_DIR at the top of ecosystem.config.js
#    (pre-filled from startcomfyfast.bat, 2026-07-05: D:\comfy\comfy-fast)

# 3. Stop any copies still running from the old bats, then start under pm2
cd <this folder>   # wherever you checked out conductor/ops/home-server
pm2 start ecosystem.config.js

# 4. Verify
pm2 status          # comfyui should say "online"
pm2 logs comfyui    # watch ComfyUI boot; Ctrl+C to detach
curl http://127.0.0.1:8188/system_stats       # ComfyUI health

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
pm2 restart comfyui         # bounce the render backend
pm2 stop all                # free the GPU (e.g. before gaming)
pm2 start all
pm2 logs comfyui --lines 200
```

## What carried over from the old bats (and what deliberately didn't)

Checklist against `startcomfyfast.bat` / `webui-user.bat` (2026-07-05):

| Old bat behavior | In the pm2 kit? |
|---|---|
| ComfyUI: venv python, `--listen 127.0.0.1 --port 8188 --enable-cors-header` | ✅ verbatim in `ecosystem.config.js` |
| Forge: full `COMMANDLINE_ARGS` | ❌ **removed 2026-08-29** — the app was unused and its pm2 entry cost VRAM. |
| Tailscale Serve (`serve --bg` → 443 for comfy) | ⚠️ **not pm2-managed — it doesn't need to be.** `tailscale serve --bg` config persists in tailscaled across reboots. Run the two commands once (below), confirm with `tailscale serve status`, done. |
| `pause` at the end | ❌ dropped — it's what makes bats un-automatable. |

### Tailscale Serve (one-time)

```powershell
& "C:\Program Files\Tailscale\tailscale.exe" serve --bg http://127.0.0.1:8188
& "C:\Program Files\Tailscale\tailscale.exe" serve status   # verify the mapping
```

If the mapping already shows in `serve status` from your old bat runs, there's
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

### The 2026-08-29 recurrence: the *client* rebooted, not the NAS

"I rebooted ferngrotto and lost access to my network drives, again." Same
symptom, a different cause from 2026-08-25/26 — and worth separating, because
the fixes are different and the earlier ones don't cover this.

The two failures:

| | 2026-08-25/26 | 2026-08-29 |
|---|---|---|
| What rebooted | alexandria (the NAS) | ferngrotto (this box) |
| What was lost | the *sessions* behind live mappings | every mapping in every logon session, at once |
| Who notices first | ComfyUI, mid-render | you, opening Explorer |
| What covers it | `healthcheck.ps1` share watchdog, 5-min tick | `restore-shares.ps1`, at logon |

Three specific reasons the existing watchdog does not close the client-reboot
case, all of them structural rather than bugs:

1. **It may not be running yet.** A `schtasks /SC MINUTE` task created without
   `/RU` runs only while its creating user is logged on. A box sitting at the
   login screen after a reboot runs no watchdog at all — the same trap as pm2
   Option B starting at *logon* rather than boot.
2. **It repairs one letter.** `KR_SHARE_UNC` remaps whatever letter is in
   `KR_SHARE_PROBE_PATH`. There are four mappings on this box; a reboot takes
   all four, and the watchdog was only ever asked about the models one.
3. **It cannot repair a letter into your session anyway.** See below.

**Why you cannot just have a service fix this for you.** A mapped drive letter
belongs to one Windows logon session. Letters mapped by a task running as
SYSTEM, or as "run whether user is logged on or not", land in a session you are
not sitting in — your desktop still shows nothing, and pm2 running under your
account still sees nothing. This is the same per-session trap that produced the
two misreads already recorded here: a `net use` listing from Terminus showing
everything `Unavailable` while the console session was fine (2026-08-25), and
`pm2 jlist` returning an empty list under a Task Scheduler account that did not
own the daemon (2026-08-27). There is no configuration that makes one process
restore letters for everybody.

So the split is:

**The pipeline is *supposed* to be off drive letters — verify, do not assume.**
`extra_model_paths.yaml` and `ecosystem.config.js` both default to
`//192.168.7.172/pc`, and a UNC path has no logon session to lose. But
2026-08-29 caught the box still running on `Z:` regardless: ArtJob 10258 failed
with `[WinError 3] The system cannot find the path specified: 'Z:\'` at 09:50,
two days after this repo recorded the move as done. Documentation of an intended
state is not evidence of the deployed state. Check the running process, not this
file:

```powershell
pm2 logs kr-relay --lines 40 | findstr /i "share gate"
```

`share gate armed on //192.168.7.172/pc/ai/models` means it took. `armed on Z:`
means it did not. `share gate disabled` means `KR_SHARE_PROBE_PATH` is unset in
that process and the relay will claim jobs it cannot render, converting PENDING
into FAILED at the rate the queue feeds it.

**Why the change can silently not take: `pm2 resurrect` replays the environment
captured at the last `pm2 save`.** A `setx` performed after that save never
reaches the resurrected process, and every reboot faithfully restores the stale
env. That is the mechanism that kept this box on `Z:` for two days while the
config on disk said UNC. Applying it needs both halves:

```powershell
setx KR_SHARE_ROOT "//192.168.7.172/pc"
setx KR_SHARE_UNC  "\\192.168.7.172\pc"
# open a NEW shell -- setx only affects new processes
cd D:\code\Conductor\ops\home-server
pm2 restart ecosystem.config.js --update-env
pm2 save
```

Leave `KR_SHARE_PROBE_PATH` unset on purpose. Unset, the relay inherits the UNC
path from `KR_SHARE_ROOT` while `healthcheck.ps1` falls back to `Z:\ai\models`
and can still auto-remap via `KR_SHARE_UNC`. Setting it machine-wide collapses
both consumers onto one path and disables the remap.

Whichever path the pipeline is on, it needs the **credential**, and that is the
part to check first when the box comes back:

```powershell
cmdkey /list          # is there an entry for 192.168.7.172 at all?
```

A bad credential presents *identically* to a dead NAS — every path unreadable,
the host plainly up, `folder_paths` enumerating nothing. It has been wiped here
before (ai-art-academy/t-033, 2026-08-25: "`cmdkey /list` was empty and all four
alexandria mappings showed Unavailable"). Three traps, all hit on 2026-08-29:

1. **A listed credential is not a working credential.** `cmdkey /list` showed
   entries for both `192.168.7.172` and `alexandria`, and every share still
   answered `The user name or password is incorrect`. The entries were present
   with a stale password. Re-adding replaced it and the share read immediately.
   Treat "an entry exists" as telling you nothing; only a successful `dir` of
   the UNC path counts.
2. **You cannot fix this over SSH.** `cmdkey /add` from a network logon session
   fails with `CMDKEY: Credentials cannot be saved from this logon session` —
   Credential Manager refuses to write from one. A Termius/SSH shell also reads
   its own (empty) drive-letter table, which is how a `net use` listing showing
   everything `Unavailable` got misread as "the array is down" on 2026-08-25.
   Confirm where you are before believing anything: `echo %SESSIONNAME%` should
   say `Console` or `RDP-Tcp#N`. Do this work from the console.
3. **`cmdkey` is per-user**, so the account pm2 runs as needs its own entry. If
   the engines run under a different account than your desktop, adding it in
   your shell fixes Explorer and nothing else.

Errors do not agree with each other across shells, and only one of them is
honest. For the same broken share on the same box: cmd said `The user name or
password is incorrect` (true), PowerShell said `Cannot find path ... because it
does not exist` (misleading — the path exists, the session could not
authenticate to it), and ComfyUI reported `no matching file for` a model that
was registered and present. Believe the cmd error.

**The letters are for you**, and `restore-shares.ps1` restores them at logon:

```powershell
cd <this folder>
.\restore-shares.ps1 -Save     # once, while the mappings are healthy:
                               # snapshots letter -> UNC into shares.json (gitignored)
.\restore-shares.ps1 -Check    # report only: what is mapped, readable, credentialed
.\restore-shares.ps1           # restore anything missing or unreadable
```

Register it — **as your normal user, not elevated, not SYSTEM**, or it will map
letters into a session you are not in:

```powershell
schtasks /Create /SC ONLOGON /TN "Restore-SMB-Shares" /RL LIMITED `
  /TR "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\path\to\conductor\ops\home-server\restore-shares.ps1\""
```

It waits up to 90s for TCP 445 on each file server before touching anything (a
logon trigger fires while the NIC may still be negotiating), reports any host
missing a stored credential, remaps only what is actually unreadable — it
*enumerates* rather than trusting `Test-Path`, for the stale-handle reason
above — and restarts ComfyUI if it restored anything and can see the daemon,
because `folder_paths` caches its filename lists and will not re-enumerate just
because a share came back. Logs to `logs\restore-shares.log`.

`-Save` deliberately refuses to record a mapping it cannot read, so running it
during an outage cannot bake today's breakage into the config as if it were the
intent. Which means: run `-Save` once now, while things are working, or it has
nothing to restore from next time.

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

### Triage: the ComfyUI console keeps reappearing, and art jobs fail (2026-09-02 incident)

**Symptom.** A `comfy-fast` console window recycles on the desktop every ~30
seconds, and the art queue drains into FAILED while the model share is
perfectly healthy. `pm2 logs comfyui` shows a full, normal-looking startup —
GPU detected, custom nodes loading, model paths added — that simply *ends*, and
then begins again.

**Cause.** A Python `UnicodeEncodeError` on a log line, taking the whole
interpreter with it:

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u26a1'
  File "D:\comfy\comfy-fast\custom_nodes\comfyui-mnemic-nodes\__init__.py", line 102
  File "D:\comfy\comfy-fast\main.py", line 571, in <module>
```

Windows takes stdout's encoding from the locale codepage (cp1252) whenever
stdout is a pipe, and under pm2 it always is. A custom node printed a `⚡` from
its `__init__` and that raised. `load_custom_node()` *does* catch a failing
import — but it reports it with `logging.warning(traceback.format_exc())`, and
the traceback it formats contains the same un-encodable character, so the
handler raised too. That second raise escaped `init_extra_nodes()` and killed
`main.py` **before the Prompt Server ever bound 8188**. pm2 restarted it, and
around it went.

Two things make this nastier than it looks:

- The engine never binds its port, so the relay's claims have nowhere to land.
  Each one waits out `COMFY_RECOVERY_SECONDS` at `POST /prompt` and burns an
  attempt. Nothing is wrong with the queue or the share.
- Each crash comes ~26s in, which is under the comfyui app's `min_uptime`
  (30s), so pm2 scores every restart as unstable. At `max_restarts` (50) it
  stops trying and parks the app in `errored` — the recycling console you were
  using to notice the problem disappears, and the box goes quiet rather than
  green.

**Fix (already in `ecosystem.config.js`).** The comfyui app now sets
`PYTHONIOENCODING: 'utf-8'`, which kr-relay and kr-download have carried since
2026-08-13. ComfyUI needed it most and had it least: it is the process that
loads ~60 third-party custom nodes whose banner text nobody here controls.
Pull the checkout and reload:

```powershell
cd D:\code\Conductor
git pull
cd ops\home-server
pm2 restart ecosystem.config.js --only comfyui --update-env
pm2 save
```

Note the second `cd`: `ecosystem.config.js` lives in `ops\home-server`, not at
the repo root, and pm2 resolves that argument relative to the current directory.
Running it from the repo root fails to find the file (and a bare `pm2 restart
comfyui` "works" while silently keeping the old environment, which looks like
the fix not taking).

`pm2 restart comfyui` alone does **not** pick up a changed `env` block — a
bare app name reuses the environment the process was started with. Pass the
ecosystem file *and* `--update-env`. If you want to be certain (and a few
seconds of downtime is fine, which it is here):

```powershell
pm2 delete comfyui
pm2 start ecosystem.config.js --only comfyui
pm2 save
```

Confirm it took:

```powershell
pm2 env 3                          # the app id from `pm2 status`; dumps its real environment
pm2 status                         # comfyui's restart count should stop climbing
curl http://127.0.0.1:8188/system_stats
```

Use `pm2 env <id>`, **not** `pm2 describe`. `describe` prints a summary table
and does not include environment variables at all, so grepping it for
`PYTHONIOENCODING` returns nothing whether the variable is set or not — an
answer that looks like a diagnosis and is really just silence.

If a custom node later dies on a *file* read rather than a print, add
`PYTHONUTF8: '1'` to the same block — that also switches `open()`'s default
encoding, so it is the bigger hammer; `PYTHONIOENCODING` alone only covers
stdout/stderr.

**Guard.** kr-relay now runs an **engine gate** alongside the share gate: it
probes `/system_stats` (cached `KR_ENGINE_PROBE_SECONDS`, default 15s) and will
not claim a job while ComfyUI is not answering. Jobs stay PENDING through an
engine outage instead of burning their attempts against a port nothing is
listening on, and the block is logged once per transition rather than once per
poll. The relay had in fact been posting `COMFY ok:false` on every heartbeat
throughout this outage — it simply never consulted its own signal before
claiming. Set `KR_ENGINE_GATE=0` to restore the old always-claim behaviour.

**Then requeue the backlog**, exactly as for a share outage:

```
python scripts/drain_failed_art_backlog.py --live
```

### Triage: `Port 8188 is already in use` (2026-09-06 incident)

**Symptom.** `pm2 logs comfyui` shows a complete, healthy-looking startup —
custom nodes load, `Adding extra search path ...` scrolls past — and then, in
the `.err` stream:

```
[ERROR] Port 8188 is already in use on address 127.0.0.1. Please close the
        other application or use a different port with --port.
```

…followed a few seconds later by another full startup, and another. Every
signal *except* the pm2 restart counter says the box is fine, because it almost
is: something is listening on 8188 and answering `/system_stats` perfectly well.

**Cause.** Two ComfyUI processes, one port. ComfyUI logs that line and calls
`sys.exit` — there is no traceback, so the usual "read the FIRST exception"
advice finds nothing. Usual sources of the second copy:

- a stray engine from the old `startcomfyfast.bat`, double-clicked out of habit;
- a previous ComfyUI that outlived the pm2 daemon that started it (`pm2 kill`,
  a daemon restart, or the WSL/Windows pm2 split — see the gotcha above);
- a `pm2 restart` whose old process had not released the port yet, when the new
  one is already trying to bind.

Three things make it nastier than a plain crash:

- **The liveness probe stays green.** The squatter answers `/system_stats`, so
  the watchdog's HTTP check — and the relay's engine gate — see a healthy
  engine. Renders may keep working the whole time.
- **The engine that works is unsupervised.** pm2 is not watching the process
  that owns the port, so when it dies nothing restarts it.
- **It ends in `errored`.** Each attempt dies well inside `min_uptime` (30s), so
  pm2 counts every restart as unstable and gives up at `max_restarts` (50).

**What in that log is *not* the problem.** The same startup is full of louder
red herrings, all of them ComfyUI-Manager reaching for the network at boot:
`Cannot connect to comfyregistry`, `FETCH DATA from: ...custom-node-list.json`,
`[ComfyUI-Manager] Due to a network error, switching to local mode`, and the
tqdm bar crawling at ~6s/it (that is eight HTTP fetches each waiting out a
timeout). None of it stops ComfyUI. `cannot schedule new futures after shutdown`
is the *consequence* of the exit above — an in-flight Manager fetch landing on
an interpreter that is already on its way out — not a second fault.

**Diagnose.** Find out who actually owns the port, and whether it is the process
pm2 thinks it is running:

```powershell
netstat -ano | findstr :8188          # last column is the owning PID
tasklist /FI "PID eq <pid>"           # what it is
pm2 status                            # comfyui's own pid + restart count
```

`pm2 status`'s pid matching the netstat pid means the port is not your problem.
A *different* pid is the whole diagnosis.

**Fix.** Stop the squatter, then let pm2 own the port:

```powershell
taskkill /PID <pid> /F
pm2 restart ecosystem.config.js --only comfyui --update-env
pm2 save
```

Run this from `ops\home-server` (pm2 resolves the ecosystem path relative to the
current directory), and confirm with `curl http://127.0.0.1:8188/system_stats`
plus a `pm2 status` whose restart count has stopped climbing. If pm2 had already
parked the app in `errored`, `pm2 restart` still revives it — the counter resets
on a successful start.

**Guard.** `healthcheck.ps1` now names the port owner in both the crash-loop and
`errored` alerts (and in `logs\healthcheck.log`): the pid, process name, start
time, and command line of whatever holds 8188, plus whether that pid is the one
pm2 is supervising. `pm2-jlist-snapshot.js` carries `pid` through for that
comparison. The watchdog deliberately does **not** kill the squatter itself — it
can be a working engine mid-render, and choosing to end that render is a human's
call, not a 5-minute timer's.

### Triage: "something keeps resetting" — heartbeats arriving minutes apart (2026-09-06, open)

**Symptom.** ComfyUI, the relay, or "something" appears to restart on its own.
Renders stall and resume for no visible reason. `pm2 status` shows no crash to
explain it, `healthcheck.log` simply skips stretches of time, and ComfyUI's own
log has no error at the moment the gap starts — every log just *jumps*.

**The signal that does show it** is the COMFY heartbeat series on
kindrobots.org, because it is recorded off the box:

| Window (local) | What arrived |
|---|---|
| 09-05 11:46 – 15:06 | no heartbeat at all — 200 minutes |
| 09-05 18:22 – 18:43 | no heartbeat — 21 minutes |
| 09-05 18:51 – 21:10 | **one beat every ~7 minutes**, for 2h20m |
| 09-06 00:15 – 02:39 | no heartbeat at all — 143 minutes |

The middle row is the diagnostic one. `relay_agent.py`'s heartbeat runs on its
own daemon thread: `time.sleep(60)`, with a 10-second engine probe and a
15-second post. **85 seconds is the widest gap a running relay can produce.**
Seven minutes, metronomically, for two hours, is not the relay pacing itself.

Check the resolution before reading any such table: `GET /api/server/uptime`
caps at 500 samples and downsamples to fit (confirmed by asking for 5000 and
getting 500), which invents ~6-minute gaps in a 24-hour window. The rows above
were re-confirmed against uncapped 9-hour and 12-hour windows.

**Ruled out: the box is not sleeping.** This was the first hypothesis and it is
wrong. On Silas-PC, `powercfg /q SCHEME_CURRENT SUB_SLEEP` reports **Sleep after
AC = 0** and **Hibernate after AC = 0** (both disabled), `powercfg /lastwake`
reports **Wake History Count - 0**, and the newest Kernel-Power 42/107 pair in
the System log is **7/6/2026** — two months before these gaps. The box was awake
the entire time.

**Also ruled out: Kind Robots was not down.** `render-box-watchdog.yml` read
`/api/server/uptime` successfully from GitHub Actions at 08:48Z — inside the
143-minute blackout — and wrote `state: silent` from the result. The API was up
and reachable from the public internet throughout.

**What is left**, and the one command that separates them. `post_heartbeat`
swallows a failed POST and logs it, so the relay's own log distinguishes a relay
that was not running from one whose posts were not landing:

```powershell
pm2 describe kr-relay     # uptime shorter than the gap = it restarted

Select-String -Path D:\code\Conductor\ops\home-server\logs\kr-relay.out.log `
  -Pattern 'failed to post|polling' | Select-Object -Last 40
```

- `heartbeat(COMFY) failed to post: ...` lines across the gap → the beats were
  attempted and lost. The relay was up; its path to kindrobots.org was not.
  Read the error: DNS, TLS, timeout and connection-refused all look different.
- repeated `agent ... polling https://kindrobots.org every 2s` lines → the relay
  restarted that many times. Then `pm2 logs kr-relay --err` has the reason.
- **neither** → the process was alive and never even attempted a beat, which
  means its thread was not scheduled. That is a frozen process on an awake box:
  look at what else was running (a long render pinning the machine, a driver
  reset, disk stalls in Event Viewer under Disk/Ntfs).

**Guard.** Two additions, one on each side of the box, because neither works
alone:

- `healthcheck.ps1` records the time of every tick and, when the next tick is
  more than 12 minutes later, reads Kernel-Power 42/107 across the gap. The log
  now says either `the BOX SLEPT` or `NO Kernel-Power sleep/resume event - the
  box was awake and this task did not run`. That distinction was previously
  unavailable — an empty stretch of `healthcheck.log` meant both things at once
  — and it is what would have refuted the sleep theory in one line instead of a
  round trip.
- `check_engine_heartbeat.py` gains a **DOZING** state next to SILENT and DOWN.
  It scores the *spacing* of the beats rather than their content, so a box that
  contributes nothing for most of an hour no longer reads as healthy just
  because each beat it manages to send is fresh and `ok:true`. It refuses to
  score a downsampled series, so a wide `--window-hours` cannot manufacture an
  alarm. It deliberately names no cause — that is what this section is for.

## Why a 24-hour outage produced no alerts (2026-09-02), and what watches now

The ComfyUI crash loop above ran for about a day before a human noticed. Four
things could have caught it. Each was quiet for a different reason, and the
first one is the one that matters:

**1. The on-box watchdog was not running.** From `logs/healthcheck.log`:

```
2026-08-31   288 ticks
2026-09-01    30 ticks, last at 02:26:07
2026-09-02    (nothing)
```

It stopped ~37 hours before the outage was noticed, while the box was still
healthy — so it was already gone when ComfyUI started failing. Its email path
was fine (23 alerts delivered, 0 skipped for missing Brevo config); it simply
was not running. **A watchdog cannot report its own absence**, and this one was
the only thing watching. If the watchdog log's newest line is not within the
last ~10 minutes, nothing on this box is being monitored, whatever else looks
green. Check the Task Scheduler entry first:

```powershell
Get-ScheduledTask -TaskName *health* | Get-ScheduledTaskInfo
Get-ScheduledTask -TaskName *health* | Select-Object -ExpandProperty Actions
(Get-ScheduledTask -TaskName *health*).Settings |
    Select-Object ExecutionTimeLimit, MultipleInstances
```

`LastTaskResult` is the field that matters, and **a non-zero one alongside a
healthy `NextRunTime` is the trap**: the task is firing on schedule and failing
every time, which from the outside looks identical to a task that works.

`1073807364` (`0x40010004`) means the run was **terminated** rather than
finishing.

The settings on this box (verified 2026-09-02) are `ExecutionTimeLimit PT72H`
and `MultipleInstances IgnoreNew`, and that pair is what turned one bad minute
into 37 hours of silence. Under `IgnoreNew`, a run that hangs is **not** killed
by the next trigger — the next trigger is simply *skipped*, and so is every one
after it, for up to the full 72 hours before the stuck run is force-ended. So a
single hang stops the watchdog completely, for days, while Task Scheduler goes
on reporting a healthy `NextRunTime` and the log stays empty because the tick
line is never reached.

`pm2 jlist` against an unresponsive per-user pm2 daemon is the likeliest place
to hang, which is why that call is now bounded by `$pm2TimeoutSeconds` (60s).
Restarting pm2 clears the wedge and the watchdog resumes on the next trigger,
as it did at 16:46 on 2026-09-02.

Two log lines tell these apart. `run starting` is written before anything that
can block; `tick` is written after the pm2 block. **`run starting` with no
`tick` after it means the pm2 block hung.** Neither line at all means the task
never really ran — check its run-as account and the "run only when user is
logged on" setting, the usual casualties of a reboot or a profile change.

**2. The render-failure watchdog needs work to fail.** It alerts on per-tick
deltas of new FAILED jobs. Once the PENDING backlog drained there was nothing
left to claim, the delta went to zero, and it went quiet. A dead box with an
empty queue is indistinguishable from a healthy box with an empty queue.

**3. `check_render_box.py` actively reported UP.** With a drained queue its
throughput verdict was `None, "queue idle"`, which `main()` treated as fine.
`RENDER-BOX-STATUS` read `up` throughout, so the state-change email in
`auto-art-generate.yml` never had a change to fire on.

**4. The heartbeat was arriving the whole time and nothing alarmed on it.**
kr-relay posted `COMFY ok:false` to `/api/server/heartbeat` every 60 seconds —
roughly 1,440 explicit "the engine is down" messages — into a
`ServerHealthCheck` table whose stated purpose is charting uptime. The daily
digest, the one message guaranteed to reach Silas, said nothing about render
health at all.

The shape they share: every check was **edge-triggered** (a delta, a state
transition) or **work-conditional** (it needed queued jobs to have an opinion).
None asked *"when did a render last succeed?"*, so silence meant health
everywhere.

### What watches now

| Layer | Where it runs | Catches |
| --- | --- | --- |
| `check_engine_heartbeat.py` via the **Render Box Watchdog** workflow (every 30 min) | GitHub Actions | Engine down OR silent, on an idle queue, **even if this box is off or its watchdog is dead** |
| Render-engine banner at the top of the daily digest | GitHub Actions | A daily positive assertion of health, so absence of an alert means something |
| `check_render_box.py` engine-heartbeat gate | GitHub Actions | "Queue idle" no longer reads as UP |
| `healthcheck.ps1` crash-loop + `errored` detection | this box | A climbing pm2 restart counter, and pm2 giving up entirely |

The first row is the important one: it runs **off the box**, so it survives the
exact failure that made this outage invisible. It alerts on transition and then
re-alerts every 6 hours while the problem persists, rather than emailing once
and going quiet. State lives in `ENGINE-HEARTBEAT-STATE.json` beside this file.

Run it by hand any time:

```
KR_API_TOKEN=... python scripts/check_engine_heartbeat.py
```

Exit 0 healthy, 1 a real problem, 2 unresolved (no token / API unreachable).
2 is deliberately not 1: a broken credential must never look like a broken
render box.

## Reboot-readiness check (`preflight.ps1`)

```powershell
cd D:\code\Conductor\ops\home-server
.\preflight.ps1
```

Read-only; changes nothing. Exit 0 clean, 1 if something would break on reboot.

It exists because **working now and surviving a reboot are different
questions**, and every failure in the 2026-08-25 → 08-29 run looked fine right
up until the box came back. What survives is the *saved* state, so that is what
it checks:

| Running state | What a reboot actually restores |
|---|---|
| `net use` shows `Z:` working | `HKCU:\Network\Z` — absent means the mapping was made without `/persistent:yes` and is gone |
| `pm2 status` lists the right apps | `~\.pm2\dump.pm2` — the list *and the environment* frozen at the last `pm2 save` |
| `setx KR_SHARE_ROOT` succeeded | the env inside `dump.pm2`, which a `setx` after the last save never reached |
| a credential is listed by `cmdkey` | nothing — presence is not validity; only a UNC read proves it |

It reports the logon session as INFO rather than a warning: `SESSIONNAME` is
empty in plenty of good shells (Windows Terminal among them), and warning on
that alone cried wolf on a session whose drives, credential and pm2 all worked.
It only matters as an explanation for a failure, so the summary raises it there
instead — a network logon session (SSH, Termius) reads its own empty drive
table and cannot save credentials at all, so a FAIL from the wrong shell may be
an artifact rather than a fault.

**Reading fields off `DeserializeObject` output: index, never `.Contains()`.**
It returns `Dictionary[string,object]`, which implements the non-generic
`IDictionary` *explicitly* — so `-is [IDictionary]` is true while `.Contains()`
is not publicly bound and, under `SilentlyContinue`, resolves to nothing rather
than erroring. That returned `$null` for every field and printed a wall of
`[FAIL]  is , not online` on a completely healthy box. The indexer is public on
both shapes; use `$obj[$key]`. The pm2 checks now also refuse to report
failures at all when no app name could be read — "cannot tell" is the honest
answer there, and it is indistinguishable from "everything is down" otherwise.

**On PowerShell 5.1, do not parse pm2's output with `ConvertFrom-Json`.** There
it is `JavaScriptSerializer` with a `MaxJsonLength` cap it will not tell you
about, and `pm2 jlist` — every app with its full environment — goes straight
past it. The first version of this script reported "pm2 returned no usable
process list" on a box where pm2 was working perfectly, silently losing exactly
the two checks that read the reboot-restored state. `ConvertFrom-JsonBig` raises
the cap and parses directly; capture `pm2 jlist` with `2>$null` rather than
`2>&1`, since merging its stderr chatter corrupts the JSON before parsing.

## Notes & gotchas

- **`--listen` / `0.0.0.0`** binds beyond localhost so the tailscale interface
  can reach the backend. Tailscale is the only route in; do not port-forward
  this on the router.
- **VRAM:** ComfyUI is now the only resident backend, which is the point of
  removing Forge — nothing else on this box competes for VRAM at load. Add
  `--lowvram` if a single large model still will not fit.
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
