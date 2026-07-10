# Home Server Supervision — ComfyUI + Stable Diffusion (A1111) auto-restart

Keeps the two art backends on Silas's Windows box alive without hand-launching
`.bat` files: crash → auto-restart, reboot → auto-start, plus an optional
health watchdog. Uses **pm2**, which runs fine on Windows.

Files in this folder:

| File | What it is |
|---|---|
| `ecosystem.config.js` | pm2 process definitions for `comfyui` and `sd-webui` (plus an opt-in `kr-relay`) |
| `healthcheck.ps1` | optional watchdog — probes the HTTP health endpoints and `pm2 restart`s a hung process |
| `relay_agent.py` | pull-based bridge: claims ArtJobs from kind_robots and drives local ComfyUI/A1111 (enable after art-generator-connect/t-010 deploys) |
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
input folder before posting the workflow. **A stale agent will claim these
jobs and fail them** (Comfy errors on the missing LoadImage file, and after
3 attempts the job lands FAILED) — so restart the relay before anyone tries
the deployed Hair Studio. Verify end-to-end by running a styling in
`/stylist` and watching `pm2 logs kr-relay` for
`uploaded input image kr_kontext_queue_...` followed by the save-generated
upload line.

**Future option — local fast path:** the engines, kind_robots, and conductor
checkouts all live on the same physical drive, so the relay could someday
write finished images straight into the local kind_robots
`public/images/{...}` folder (and just POST the DB record) instead of
round-tripping base64 through the API. Skipped for now — the API path is
simpler and works from anywhere — but the option is recorded in
art-generator-connect/t-012's note if generation volume ever makes it worth it.

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
