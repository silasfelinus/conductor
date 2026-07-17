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
      restart_delay: 5000, // give CUDA a beat before relaunch
      max_restarts: 50, // per crash-window; stops true crash-loops
      min_uptime: 30000, // <30s alive counts as a failed start
      kill_timeout: 15000,
      out_file: `${LOG_DIR}/comfyui.out.log`,
      error_file: `${LOG_DIR}/comfyui.err.log`,
      merge_logs: true
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
        'https://kindrobots.org,https://kind-robots.vercel.app,http://localhost:3000,http://localhost:3001',
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
        // --listen makes forge lock the Extensions tab (AssertionError:
        // "extension access disabled because of command line flags").
        // The box is only reachable via LAN/tailscale, so re-enabling
        // extension management is fine here.
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
      merge_logs: true
    },
    // kr-relay — pull-based bridge between the kind_robots ArtJob queue and the
    // local engines. relay_media_agent.py wraps the proven relay_agent.py and
    // writes Kind Robots-targeted jobs to their exact self-hosted media path
    // before reporting the job successful.
    //
    // One-time, in PowerShell (keeps secrets and machine paths out of git):
    //   setx KR_RELAY_TOKEN "your-admin-apikey"
    //   setx KR_RELAY_USER_ID "1"
    //   setx KR_MEDIA_IMAGES_DIR "Z:/kindrobots/images"
    //   py -3.12 -m pip install Pillow
    //
    // Open a NEW shell after setx, then:
    //   pm2 start ecosystem.config.js --only kr-relay
    //   pm2 save
    // NEVER paste the real token into this file — it is committed to git.
    {
      name: 'kr-relay',
      cwd: __dirname,
      script: 'C:/Python312/python.exe', // any Python 3.9+; Pillow required for webp targets
      args: 'relay_media_agent.py',
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 10000,
      env: {
        KR_RELAY_TOKEN: process.env.KR_RELAY_TOKEN || '',
        KR_RELAY_USER_ID: process.env.KR_RELAY_USER_ID || '',
        // Prod currently lives on the vercel.app host; switch to
        // kindrobots.org when that domain points at prod.
        KR_BASE_URL: 'https://kind-robots.vercel.app',
        // Exact backing directory for https://media.acrocatranch.com/images/.
        KR_MEDIA_IMAGES_DIR: process.env.KR_MEDIA_IMAGES_DIR || '',
        // Optional generic ArtImage-id copies for jobs without an exact target.
        KR_LOCAL_IMAGES_DIR: process.env.KR_LOCAL_IMAGES_DIR || ''
      },
      out_file: `${LOG_DIR}/kr-relay.out.log`,
      error_file: `${LOG_DIR}/kr-relay.err.log`,
      merge_logs: true
    }
  ]
}
