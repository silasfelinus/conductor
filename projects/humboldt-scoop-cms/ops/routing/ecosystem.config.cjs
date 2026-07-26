// pm2 process definitions for Humboldt Scoop CMS's self-hosted routing
// stack (OSRM road-network matrix/polyline + VROOM stop-order
// optimization), per t-006's approved v1 stack (route-planner/SPEC.md
// section 3a/5) and t-012's "package pm2 startup from the conductor repo"
// note -- same convention as ops/home-server/ecosystem.config.js at the
// conductor repo root and serendipity-voice's ecosystem.config.cjs.
//
// One-time setup BEFORE first start: run ./fetch-extract.sh to download and
// preprocess the OSM extract (see README.md). Then:
//   pm2 start ecosystem.config.cjs
//   pm2 save
//
// Requires Docker. Each app runs `docker run` in the foreground (no -d, and
// --rm so a stopped container doesn't linger) so pm2 supervises the
// container directly -- crash detection + clean restarts, not a detached
// container pm2 has no visibility into.
//
// ---- VERIFY ON THE ACTUAL HOST -- image tags and --network host behavior
// are standard/documented but unverified from a conductor sandbox session
// (no docker there; see projects/humboldt-scoop-cms/TALKBACK.md, t-012
// filing note) ----

const path = require('node:path')

const HERE = __dirname
const DATA_DIR = path.join(HERE, 'data')
const LOG_DIR = path.join(HERE, 'logs')
const OSM_REGION = process.env.OSM_REGION || 'humboldt-county'

module.exports = {
  apps: [
    {
      // osrm-backend -- road-network matrix + turn-by-turn polyline.
      // Serves the exact /table/v1/driving and /route/v1/driving HTTP API
      // that ../../src/routing/matrixProvider.ts's OSRMMatrixProvider
      // expects. Preprocessed .osrm files must exist in data/ first --
      // run ./fetch-extract.sh once (or after a quarterly OSM refresh).
      // `--algorithm mld` matches fetch-extract.sh's partition/customize
      // steps. `--network host` binds directly to the host's port 5000 --
      // set OSRM_BASE_URL=http://localhost:5000 (or the box's Tailscale
      // hostname) in the CMS's env once this is running.
      name: 'osrm-backend',
      cwd: HERE,
      script: 'docker',
      args: [
        'run',
        '--rm',
        '--name',
        'humboldt-scoop-osrm',
        '--network',
        'host',
        '-v',
        `${DATA_DIR}:/data`,
        'osrm/osrm-backend',
        'osrm-routed',
        '--algorithm',
        'mld',
        `/data/${OSM_REGION}.osrm`,
      ].join(' '),
      interpreter: 'none',
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 20,
      min_uptime: 15000,
      kill_timeout: 10000,
      out_file: `${LOG_DIR}/osrm-backend.out.log`,
      error_file: `${LOG_DIR}/osrm-backend.err.log`,
      merge_logs: true,
    },
    {
      // vroom -- stop-order optimization (VROOM HTTP API on :3000), reading
      // OSRM's table output via vroom-config.yml. NOT yet wired into the
      // app (t-007's nearest-neighbor + 2-opt optimizer is the working v1
      // per route-planner/SPEC.md section 3a) -- this stands the service up
      // for a future full-VROOM integration (t-012 item 3) without blocking
      // on it. `--network host` so vroom-config.yml's `host: localhost`
      // reaches osrm-backend above.
      name: 'vroom',
      cwd: HERE,
      script: 'docker',
      args: [
        'run',
        '--rm',
        '--name',
        'humboldt-scoop-vroom',
        '--network',
        'host',
        '-v',
        `${HERE}/vroom-config.yml:/conf/config.yml`,
        'vroomvrp/vroom-docker:v1.13.0',
      ].join(' '),
      interpreter: 'none',
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 20,
      min_uptime: 15000,
      kill_timeout: 10000,
      out_file: `${LOG_DIR}/vroom.out.log`,
      error_file: `${LOG_DIR}/vroom.err.log`,
      merge_logs: true,
    },
  ],
}
