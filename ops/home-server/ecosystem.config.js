// pm2 process definitions for the home art backends.
// Fill in the three *_DIR paths for this machine, then: pm2 start ecosystem.config.js
//
// Each app points pm2 at the SAME Python command the launcher .bat runs, so pm2
// supervises the real process (crash detection + clean restarts) instead of a
// cmd.exe wrapper. See README.md in this folder.

// ---- EDIT THESE THREE PATHS ------------------------------------------------
const COMFY_DIR = 'C:/AI/ComfyUI_windows_portable' // folder containing python_embeded/ and ComfyUI/
const SD_DIR = 'C:/AI/stable-diffusion-webui' // A1111 checkout (contains launch.py and venv/)
const LOG_DIR = `${__dirname}/logs`
// ----------------------------------------------------------------------------

module.exports = {
  apps: [
    {
      // ComfyUI — portable/standalone install.
      // Mirrors run_nvidia_gpu.bat:
      //   .\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build
      // If ComfyUI lives in a plain git checkout + venv instead, set script to
      // <checkout>/venv/Scripts/python.exe and args to 'main.py --listen 0.0.0.0 --port 8188'.
      name: 'comfyui',
      cwd: COMFY_DIR,
      script: `${COMFY_DIR}/python_embeded/python.exe`,
      args: '-s ComfyUI/main.py --windows-standalone-build --listen 0.0.0.0 --port 8188',
      interpreter: 'none',
      windowsHide: true,
      autorestart: true,
      restart_delay: 5000, // give CUDA a beat before relaunch
      max_restarts: 50, // per crash-window; stops true crash-loops
      min_uptime: 30000, // <30s alive counts as a failed start
      kill_timeout: 15000,
      out_file: `${LOG_DIR}/comfyui.out.log`,
      error_file: `${LOG_DIR}/comfyui.err.log`,
      merge_logs: true,
    },
    {
      // Stable Diffusion WebUI (A1111).
      // Mirrors webui-user.bat -> webui.bat -> launch.py, using the venv python.
      // --api is REQUIRED for the kind_robots /sdapi/v1/txt2img handshake.
      // Add --medvram here if sharing the GPU with ComfyUI.
      name: 'sd-webui',
      cwd: SD_DIR,
      script: `${SD_DIR}/venv/Scripts/python.exe`,
      args: 'launch.py --api --listen --port 7860',
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
    },
    // kr-relay — pull-based bridge between the kind_robots ArtJob queue and the
    // local engines (see relay_agent.py). UNCOMMENT after the queue endpoints
    // (art-generator-connect/t-010) are merged and deployed, and fill in the
    // two env values. Harmless if enabled early — it just logs "not deployed
    // yet" and waits — but there's nothing for it to do until then.
    // {
    //   name: 'kr-relay',
    //   cwd: __dirname,
    //   script: 'C:/Python311/python.exe', // any Python 3.9+; stdlib only
    //   args: 'relay_agent.py',
    //   interpreter: 'none',
    //   windowsHide: true,
    //   autorestart: true,
    //   restart_delay: 10000,
    //   env: {
    //     KR_RELAY_TOKEN: 'YOUR-ADMIN-USER-APIKEY',
    //     KR_RELAY_USER_ID: '1',
    //     // KR_BASE_URL: 'https://kindrobots.org',
    //   },
    //   out_file: `${LOG_DIR}/kr-relay.out.log`,
    //   error_file: `${LOG_DIR}/kr-relay.err.log`,
    //   merge_logs: true,
    // },
  ],
}
