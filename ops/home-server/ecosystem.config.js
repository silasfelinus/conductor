// pm2 process definitions for the home art backends.
// Paths and args below are taken from the real launcher bats (startcomfyfast.bat,
// webui-user.bat, 2026-07-05) — verify they still match, then: pm2 start ecosystem.config.js
//
// Each app points pm2 at the real long-running process so pm2 supervises crash
// detection + clean restarts instead of a cmd.exe wrapper. ComfyUI is a special
// case on Windows: its venv python.exe is a redirector that can create a visible
// child console even when pm2 uses windowsHide. Launch the base interpreter
// directly and set __PYVENV_LAUNCHER__ so Python still adopts the Comfy venv.
// Tailscale Serve is NOT managed here — `tailscale serve --bg` config persists
// across reboots; see README "Tailscale Serve" for the one-time setup. The
// pip-repair bootstrap from webui-user.bat is also intentionally not here
// (one-time repair job — keep the old bat around for that).

// ---- VERIFY THESE PATHS ----------------------------------------------------
const COMFY_DIR = 'D:/comfy/comfy-fast'
const COMFY_BASE_PYTHON =
  process.env.COMFY_BASE_PYTHON ||
  'C:/Users/silasfelinus/AppData/Local/Programs/Python/Python310/python.exe'
const LOG_DIR = `${__dirname}/logs`

// The SMB share on alexandria, reached from this box. Every model path below is
// derived from these two, so moving the share is one edit (or one env var), not
// eight.
//
// PREFER A UNC PATH OVER A DRIVE LETTER. A mapped drive letter belongs to one
// Windows logon session: a service, an elevated shell, and a desktop shell can
// each see a different Z: -- or none. That is not theoretical here. On
// 2026-08-25 renders failed for ~15 hours with
//   [WinError 1117] ... I/O device error: 'Z:\ai\models\unet'
// from ComfyUI (a dead connection object the process still held), degraded into
// ComfyUI reporting registered models as "no matching file" (folder_paths
// re-enumerated a half-readable share into a short list), while an interactive
// `dir Z:\ai\models\unet` in the same hour answered "The system cannot find
// the path specified" -- three different views of one share. A UNC path has no
// per-session mapping to lose:
//   setx KR_SHARE_ROOT "//alexandria/<share>"
// then restart pm2 from a NEW shell so it inherits the variable.
const KR_SHARE_ROOT = process.env.KR_SHARE_ROOT || 'Z:'
const KR_MODEL_ROOT = process.env.KR_MODEL_ROOT || `${KR_SHARE_ROOT}/ai/models`
const KR_MEDIA_IMAGES_DIR =
  process.env.KR_MEDIA_IMAGES_DIR || `${KR_SHARE_ROOT}/kindrobots/images`
// ----------------------------------------------------------------------------

module.exports = {
  apps: [
    {
      // ComfyUI — venv install at D:\comfy\comfy-fast.
      // The original launcher activates the venv and runs:
      //   python main.py --listen 127.0.0.1 --port 8188 --enable-cors-header
      // On Windows, venv\Scripts\python.exe is itself a redirector process. It
      // can spawn the base interpreter with a visible conhost even though pm2
      // started the redirector hidden. Point pm2 at the base interpreter instead,
      // then set __PYVENV_LAUNCHER__ to the venv executable: Python uses the same
      // venv sys.prefix/site-packages while pm2's windowsHide applies to the real
      // interpreter. COMFY_BASE_PYTHON is overrideable if the base Python moves.
      // Binds 127.0.0.1 on purpose: Tailscale Serve (443) fronts it for remote
      // access, and the relay agent talks to localhost directly.
      //
      // 2026-09-06 CONFIRMED, and it is worse than "a visible console": the
      // venv python.exe is a REDIRECTOR. Point pm2 at it and you get two
      // processes - the stub, which pm2 supervises, and the base interpreter it
      // re-execs, which is the actual ComfyUI. `pm2 stop` then kills the stub
      // and the engine keeps running, holding port 8188, the comfyui.db lock
      // and the GPU, supervised by nothing. Every "immortal" ComfyUI in the
      // README's port-8188 section was that child.
      //
      // Changing THIS FILE does not fix a running app: `pm2 restart` reuses the
      // stored script path even when handed the file and --update-env. After
      // editing here you must `pm2 delete comfyui` and `pm2 start
      // ecosystem.config.js`. Verify with the process tree, not with ComfyUI's
      // "** Python executable:" banner - that prints the venv path either way,
      // because __PYVENV_LAUNCHER__ makes the base interpreter report it.
      name: 'comfyui',
      cwd: COMFY_DIR,
      script: COMFY_BASE_PYTHON,
      args: 'main.py --listen 127.0.0.1 --port 8188 --enable-cors-header',
      interpreter: 'none',
      windowsHide: true,
      env: {
        __PYVENV_LAUNCHER__: `${COMFY_DIR}/venv/Scripts/python.exe`,
        // NOT optional, and not cosmetic -- this one keeps ComfyUI alive.
        //
        // Windows picks stdout's encoding from the locale codepage (cp1252)
        // whenever stdout is a pipe, which under pm2 it always is. kr-relay
        // and kr-download below have carried this line since 2026-08-13 for
        // their own log output; ComfyUI was left without it, and ComfyUI is
        // the process that loads ~60 third-party custom nodes whose banners
        // we do not control.
        //
        // 2026-09-02: comfyui-mnemic-nodes printed a "\u26a1" from its
        // __init__ and the UnicodeEncodeError took the whole interpreter
        // down -- not just that node. load_custom_node() does catch a failing
        // import, but it reports it with logging.warning(format_exc()), and
        // the traceback it formats still contains the same un-encodable
        // character, so the handler raised too. That escaped
        // init_extra_nodes() and killed main.py at line 571, BEFORE the
        // Prompt Server ever bound 8188. pm2 restarted it, it died ~26s
        // later, forever: the console that kept reappearing on the desktop.
        // Because it never bound the port, kr-relay's claims had nowhere to
        // go and the art queue drained into FAILED.
        //
        // Note the 26s: it is under this app's min_uptime (30s), so pm2
        // counted every restart as unstable and would have given up at
        // max_restarts (50) and parked the app in `errored` -- silently, with
        // no console left to notice.
        //
        // If a custom node ever raises on a FILE read rather than a print,
        // add PYTHONUTF8: '1' as well (that also switches open()'s default
        // encoding, so it is the bigger hammer -- this line alone fixes
        // stdout/stderr).
        PYTHONIOENCODING: 'utf-8'
      },
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 50,
      min_uptime: 30000,
      kill_timeout: 15000,
      out_file: `${LOG_DIR}/comfyui.out.log`,
      error_file: `${LOG_DIR}/comfyui.err.log`,
      merge_logs: true,
      // ComfyUI does not timestamp its own output, and theirs is
      // where the real generation errors surface -- without this a red line
      // cannot be told apart from a week-old one. Our own agents DO timestamp
      // themselves, so they set time:false rather than carry two stamps per
      // line (see kr-relay below).
      time: true,
      log_date_format: 'YYYY-MM-DDTHH:mm:ssZ'
    },
    {
      name: 'kr-relay',
      cwd: __dirname,
      script: 'C:/Python312/python.exe',
      args: 'relay_media_agent.py',
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 10000,
      // Give the SIGTERM handler room to hand its in-flight job back to the
      // queue before pm2 escalates to SIGKILL. pm2's default is 1600ms, which
      // is tight for one HTTPS round trip; without the release the job stays
      // RUNNING until the queue's 15-minute stale window comes around.
      kill_timeout: 10000,
      env: {
        KR_RELAY_TOKEN: process.env.KR_RELAY_TOKEN || '',
        KR_RELAY_USER_ID: process.env.KR_RELAY_USER_ID || '',
        KR_BASE_URL: 'https://kindrobots.org',
        // Fast enough to feel immediate without changing the relay's pull-only model.
        // Windows picks stdout's encoding from the console codepage (cp1252)
        // whenever stdout is a pipe -- which it always is under pm2. Any
        // non-cp1252 character in a log line then raises UnicodeEncodeError
        // from print(), and a raise inside align_workflow_asset_names fails
        // the render (ArtJobs 8276/8278, 2026-08-13). The agents force UTF-8
        // themselves; this also covers the tools they subprocess out to.
        PYTHONIOENCODING: 'utf-8',
        POLL_SECONDS: process.env.POLL_SECONDS || '2',
        KR_MEDIA_IMAGES_DIR:
          process.env.KR_MEDIA_IMAGES_DIR || KR_MEDIA_IMAGES_DIR,
        KR_LOCAL_IMAGES_DIR: process.env.KR_LOCAL_IMAGES_DIR || '',
        // Refuse to claim jobs while the model mount is down. Without this the
        // relay claims, ComfyUI fails at model load, the queue counts an
        // attempt, and PENDING drains into FAILED at ~5/min -- 71 jobs on
        // 2026-08-26 while every health signal stayed green. Unset to disable.
        KR_SHARE_PROBE_PATH: process.env.KR_SHARE_PROBE_PATH || KR_MODEL_ROOT,
        KR_SHARE_PROBE_SECONDS: process.env.KR_SHARE_PROBE_SECONDS || '30',
        // 2026-08-28: a directory listing alone passed on a share that was
        // only partially readable -- "ComfyUI listed 1 file(s) for that
        // input" on every failure, and the one file every krea2 job needs
        // (qwen_image_vae.safetensors) was not the one listed. The relay
        // claimed and burned ~2700 jobs while the scandir-only gate stayed
        // green. Each entry (relative to KR_SHARE_PROBE_PATH) is opened and
        // read, not just stat()ed. Unset to fall back to the directory-only
        // check.
        KR_SHARE_REQUIRED_FILES:
          process.env.KR_SHARE_REQUIRED_FILES ||
          'vae/qwen_image_vae.safetensors',
        COMFY_PROMPT_TIMEOUT: process.env.COMFY_PROMPT_TIMEOUT || '180',
        COMFY_RECOVERY_SECONDS: process.env.COMFY_RECOVERY_SECONDS || '45',
        // LTX 2.3 22B video renders at 1280x720 can legitimately outlive the
        // previous 30-minute wall-clock deadline. Comfy workflow errors still
        // surface immediately through /history; this only widens the ceiling
        // for accepted jobs that are still producing no final output yet.
        GEN_TIMEOUT: process.env.GEN_TIMEOUT || '7200',
        // LoRA auto-import watcher (embedded thread). Unset LORA_ROOT to disable.
        LORA_ROOT: process.env.LORA_ROOT || `${KR_MODEL_ROOT}/Lora`,
        LORA_IMPORT_DIR:
          process.env.LORA_IMPORT_DIR || `${KR_MODEL_ROOT}/Lora/import`,
        CIVITAI_TOKEN: process.env.CIVITAI_TOKEN || '',
        LORA_POLL_SECONDS: process.env.LORA_POLL_SECONDS || '20',
        // SCAN_SCRIPT/IMPORT_SCRIPT are intentionally NOT set here: the agent
        // defaults to the vendored copies in ops/home-server/lora-catalog/,
        // which run from LOCAL disk in this checkout — never over the Z: mount.
        // Keep the scanner's sqlite cache on LOCAL disk, not the SMB share.
        CACHE_DB: process.env.CACHE_DB || `${LOG_DIR}/.lora-cache.sqlite`
      },
      out_file: `${LOG_DIR}/kr-relay.out.log`,
      error_file: `${LOG_DIR}/kr-relay.err.log`,
      merge_logs: true,
      // relay_agent.log / lora_import_agent.log already emit ISO 8601 with the
      // UTC offset as the first field of every line. pm2's prefix would make it
      // twice per line, and pm2's own stamp carries no offset -- strictly worse
      // than ours. One stamp, ours, leading the line so `cut -d' ' -f1` gets it.
      time: false
    },

    // kr-download — pull-based model download agent. The companion to kr-relay:
    // it claims queued LoRA/checkpoint downloads (from the Discover browser) via
    // /api/lora/download/claim, fetches the file onto the engine's model dir
    // (loras vs Stable-diffusion, chosen by the row's resourceType), catalogs it
    // as a Resource, and reports the outcome. Reuses relay_agent's token + HTTP.
    //
    // Reuses KR_RELAY_TOKEN (already set for kr-relay). Optionally, for gated
    // Civitai downloads, set a Civitai API token:
    //   setx KR_CIVITAI_TOKEN "your-civitai-token"
    // Override the model dirs only if the engine loads from non-default paths.
    // Open a NEW shell after setx, then:
    //   pm2 start ecosystem.config.js --only kr-download
    //   pm2 save
    // NEVER paste the real token into this file — it is committed to git.
    {
      name: 'kr-download',
      cwd: __dirname,
      script: 'C:/Python312/python.exe',
      args: 'relay_download_agent.py',
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 10000,
      // Give the SIGTERM handler room to hand its in-flight job back to the
      // queue before pm2 escalates to SIGKILL. pm2's default is 1600ms, which
      // is tight for one HTTPS round trip; without the release the job stays
      // RUNNING until the queue's 15-minute stale window comes around.
      kill_timeout: 10000,
      env: {
        KR_RELAY_TOKEN: process.env.KR_RELAY_TOKEN || '',
        KR_BASE_URL: 'https://kindrobots.org',
        KR_LORA_DIR: process.env.KR_LORA_DIR || `${KR_MODEL_ROOT}/Lora`,
        KR_CHECKPOINT_DIR:
          process.env.KR_CHECKPOINT_DIR || `${KR_MODEL_ROOT}/Stable-diffusion`,
        // Windows picks stdout's encoding from the console codepage (cp1252)
        // whenever stdout is a pipe -- which it always is under pm2. Any
        // non-cp1252 character in a log line then raises UnicodeEncodeError
        // from print(), and a raise inside align_workflow_asset_names fails
        // the render (ArtJobs 8276/8278, 2026-08-13). The agents force UTF-8
        // themselves; this also covers the tools they subprocess out to.
        PYTHONIOENCODING: 'utf-8',
        KR_DOWNLOAD_POLL_SECONDS: process.env.KR_DOWNLOAD_POLL_SECONDS || '30',
        KR_CIVITAI_TOKEN: process.env.KR_CIVITAI_TOKEN || ''
      },
      out_file: `${LOG_DIR}/kr-download.out.log`,
      error_file: `${LOG_DIR}/kr-download.err.log`,
      merge_logs: true,
      // relay_agent.log / lora_import_agent.log already emit ISO 8601 with the
      // UTC offset as the first field of every line. pm2's prefix would make it
      // twice per line, and pm2's own stamp carries no offset -- strictly worse
      // than ours. One stamp, ours, leading the line so `cut -d' ' -f1` gets it.
      time: false
    }
  ]
}