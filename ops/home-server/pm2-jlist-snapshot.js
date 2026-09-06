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

    // `proc`, not `process` -- the callback parameter used to shadow Node's
    // global `process`, which is merely confusing until you add a field like
    // `pid` that BOTH objects define. `process.pid` inside the old callback
    // would have read the pm2 entry's pid, but only by accident of shadowing,
    // and it reads like the snapshot helper's own pid to everyone else.
    const snapshot = processes.map((proc) => ({
      name: proc && typeof proc.name === 'string' ? proc.name : null,
      // The OS pid pm2 is actually supervising. The watchdog compares it
      // against whoever holds port 8188: when a crash-looping app cannot bind
      // because some OTHER process owns the port, that mismatch is the whole
      // diagnosis (2026-09-06 -- see healthcheck.ps1's Get-PortOwner). pm2
      // reports 0 for an app that is not currently running.
      pid: asNumber(proc ? proc.pid : null),
      pm2_env: {
        status:
          proc && proc.pm2_env && typeof proc.pm2_env.status === 'string'
            ? proc.pm2_env.status
            : null,
        restart_time: proc && proc.pm2_env ? asNumber(proc.pm2_env.restart_time) : null,
        unstable_restarts:
          proc && proc.pm2_env ? asNumber(proc.pm2_env.unstable_restarts) : null,
        // When the CURRENT process started, epoch ms. restart_time counts only
        // the restarts pm2 itself performed, so it cannot see a process that
        // was replaced some other way -- a pm2 daemon restart, a resurrect, a
        // reboot. kr-relay on 2026-09-06 read `restarts 0` with 44 minutes of
        // uptime and a fresh startup line in its log: nothing had crashed, and
        // pm2's own counter was the wrong instrument to notice. pm_uptime
        // moving forward while restart_time stands still is that event.
        pm_uptime: proc && proc.pm2_env ? asNumber(proc.pm2_env.pm_uptime) : null,
      },
    }));

    process.stdout.write(JSON.stringify(snapshot));
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`pm2 jlist snapshot parse failed: ${message}\n`);
    process.exitCode = 2;
  }
});
