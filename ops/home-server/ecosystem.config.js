// pm2 process definitions for the home art backends.
// Paths and args below are taken from the real launcher bats (startcomfyfast.bat,
// webui-user.bat, 2026-07-05) — verify they still match, then: pm2 start ecosystem.config.js
//
// Each app points pm2 at the SAME Python command the launcher .bat runs, so pm2
// supervises the real process (crash detection + clean restarts) instead of a
// cmd.exe wrapper. Tailscale Serve is NOT managed here — `tailscale serve --bg`
// config persists across reboots; see README "Tailscale Serve" for the one-time
// setup. The pip-repair bootstrap from webui-user.bat is also intentionally not
// here (one-time repair job — keep the old bat around for that).

// ---- VERIFY THESE PATHS ----------------------------------------------------
const COMFY_DIR = 'D:/comfy/comfy-fast'
const SD_DIR = 'D:/code/sd-webui-forge-neo'
const LOG_DIR = `${__dirname}/logs`
const KR_MEDIA_IMAGES_DIR = 'Z:/kindrobots/images'
// ----------------------------------------------------------------------------

module.exports = {
  apps: [
    {
      // ComfyUI — venv install at D:\comfy\comfy-fast.
      // Mirrors startcomfyfast.bat:
      //   call venv\Scripts\activate
      //   python main.py --listen 127.0.0.1 --port 8188 --enable-cors-header
      // Binds 127.0.0.1 on purpose: Tailscale Serve (443) fronts it for remote
      // access, and the relay agent talks to localhost directly.
      name: 'comfyui',
      cwd: COMFY_DIR,
      script: `${COMFY_DIR}/venv/Scripts/python.exe`,
      args: 'main.py --listen 127.0.0.1 --port 8188 --enable-cors-header',
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 50,
      min_uptime: 30000,
      kill_timeout: 15000,
      out_file: `${LOG_DIR}/comfyui.out.log`,
      error_file: `${LOG_DIR}/comfyui.err.log`,
      merge_logs: true,
      // ComfyUI and sd-webui do not timestamp their own output, and theirs is
      // where the real generation errors surface -- without this a red line
      // cannot be told apart from a week-old one. Our own agents DO timestamp
      // themselves, so they set time:false rather than carry two stamps per
      // line (see kr-relay below).
      time: true,
      log_date_format: 'YYYY-MM-DDTHH:mm:ssZ'
    },
    {
      // Stable Diffusion WebUI (forge-neo) at D:\code\sd-webui-forge-neo.
      // Mirrors webui-user.bat's COMMANDLINE_ARGS, passed straight to launch.py
      // via the venv python (webui.bat's only supervision-relevant job).
      // --api is REQUIRED for the kind_robots /sdapi/v1/txt2img handshake.
      // If venv/ doesn't exist yet, run the old webui-user.bat once to bootstrap.
      name: 'sd-webui',
      cwd: SD_DIR,
      script: `${SD_DIR}/venv/Scripts/python.exe`,
      args: [
        'launch.py',
        '--api',
        '--listen',
        '--cuda-malloc',
        '--ckpt-dir',
        'Z:/ai/models/Stable-diffusion',
        '--cors-allow-origins',
        'https://kindrobots.org,http://localhost:3000,http://localhost:3001',
        '--lora-dir',
        'Z:/ai/models/Lora',
        '--vae-dir',
        'Z:/ai/models/vae',
        '--controlnet-dir',
        'Z:/ai/models/controlnet',
        '--xformers',
        '--skip-python-version-check',
        '--reserve-vram',
        '2',
        '--enable-insecure-extension-access'
      ].join(' '),
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 50,
      min_uptime: 30000,
      kill_timeout: 15000,
      out_file: `${LOG_DIR}/sd-webui.out.log`,
      error_file: `${LOG_DIR}/sd-webui.err.log`,
      merge_logs: true,
      // ComfyUI and sd-webui do not timestamp their own output, and theirs is
      // where the real generation errors surface -- without this a red line
      // cannot be told apart from a week-old one. Our own agents DO timestamp
      // themselves, so they set time:false rather than carry two stamps per
      // line (see kr-relay below).
      time: true,
      log_date_format: 'YYYY-MM-DDTHH:mm:ssZ'
    },
    // kr-relay — pull-based bridge between the kind_robots ArtJob queue and the
    // local engines. relay_media_agent.py wraps the proven relay_agent.py and
    // writes Kind Robots-targeted jobs to their exact self-hosted media path
    // before reporting the job successful.
    //
    // It ALSO runs the LoRA auto-import watcher on a daemon thread in the same
    // process (relay_media_agent.start_lora_watcher). Files dropped in
    // <LORA_ROOT>/import are auto-detected (base model, SFW/NSFW, triggers,
    // preview image), sorted into <Base>/<SFW|NSFW>/, and upserted as
    // kind_robots Resources with the localPath the enqueue path
    // (server/utils/artLoraResource.ts) needs — reusing scan_loras.py +
    // import_catalog.py. One process, one token, one log; the watcher thread
    // can't stall the render loop and vice versa. The array host (alexandria)
    // is a locked-down NAS that doesn't run ad-hoc daemons, so this render box
    // is the permanent home. The tree is reached over SMB (Z:), which is
    // case-insensitive — with the folders already merged to single casing
    // (case_merge.py), Windows moves are safe and prevent fresh case-dupes.
    // If the LoRA env vars are unset the watcher just logs "disabled" and
    // kr-relay runs as a pure render relay.
    //
    // One-time, in PowerShell (keeps secrets out of git):
    //   setx KR_RELAY_TOKEN "your-admin-apikey"
    //   setx KR_RELAY_USER_ID "1"
    //   setx CIVITAI_TOKEN "your-civitai-token"      # for LoRA detection
    //   py -3.12 -m pip install Pillow
    //
    // The canonical media destination is Z:/kindrobots/image. Override
    // KR_MEDIA_IMAGES_DIR only when intentionally moving the mounted image root.
    // The scan/import tools run from LOCAL disk — vendored copies in
    // ops/home-server/lora-catalog/ (the agent defaults to them). Only the LoRA
    // files are remote (LORA_ROOT=Z:). Re-sync those two scripts from kind_robots
    // when its lora-catalog tools change (see lora-catalog/PROVENANCE.md).
    // Open a NEW shell after setx, then:
    //   pm2 start ecosystem.config.js --only kr-relay
    //   pm2 save
    // NEVER paste the real token into this file — it is committed to git.
    {
      name: 'kr-relay',
      cwd: __dirname,
      script: 'C:/Python312/python.exe',
      args: 'relay_media_agent.py',
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 10000,
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
        COMFY_PROMPT_TIMEOUT: process.env.COMFY_PROMPT_TIMEOUT || '180',
        COMFY_RECOVERY_SECONDS: process.env.COMFY_RECOVERY_SECONDS || '45',
        GEN_TIMEOUT: process.env.GEN_TIMEOUT || '1800',
        // LoRA auto-import watcher (embedded thread). Unset LORA_ROOT to disable.
        LORA_ROOT: process.env.LORA_ROOT || 'Z:/ai/models/Lora',
        LORA_IMPORT_DIR:
          process.env.LORA_IMPORT_DIR || 'Z:/ai/models/Lora/import',
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
      env: {
        KR_RELAY_TOKEN: process.env.KR_RELAY_TOKEN || '',
        KR_BASE_URL: 'https://kindrobots.org',
        KR_LORA_DIR: process.env.KR_LORA_DIR || 'Z:/ai/models/Lora',
        KR_CHECKPOINT_DIR:
          process.env.KR_CHECKPOINT_DIR || 'Z:/ai/models/Stable-diffusion',
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
