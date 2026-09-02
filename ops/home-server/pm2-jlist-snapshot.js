'use strict';

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  input += chunk;
});
process.stdin.on('end', () => {
  try {
    const processes = JSON.parse(input);
    if (!Array.isArray(processes)) {
      throw new Error('pm2 jlist did not return a JSON array');
    }

    // restart_time / unstable_restarts are the only reliable crash-loop
    // signature available to the watchdog. Status alone cannot express it: a
    // process restarting every ~30s reads 'online' most of the time and
    // 'waiting restart' the rest, and both are indistinguishable from a
    // healthy app or a deliberate stop at any single 5-minute tick.
    // See healthcheck.ps1's crash-loop block (2026-09-02).
    const asNumber = (value) => (typeof value === 'number' && isFinite(value) ? value : null);

    const snapshot = processes.map((process) => ({
      name: process && typeof process.name === 'string' ? process.name : null,
      pm2_env: {
        status:
          process && process.pm2_env && typeof process.pm2_env.status === 'string'
            ? process.pm2_env.status
            : null,
        restart_time: process && process.pm2_env ? asNumber(process.pm2_env.restart_time) : null,
        unstable_restarts:
          process && process.pm2_env ? asNumber(process.pm2_env.unstable_restarts) : null,
      },
    }));

    process.stdout.write(JSON.stringify(snapshot));
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`pm2 jlist snapshot parse failed: ${message}\n`);
    process.exitCode = 2;
  }
});
