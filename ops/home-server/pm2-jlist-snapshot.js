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

    const snapshot = processes.map((process) => ({
      name: process && typeof process.name === 'string' ? process.name : null,
      pm2_env: {
        status:
          process && process.pm2_env && typeof process.pm2_env.status === 'string'
            ? process.pm2_env.status
            : null,
      },
    }));

    process.stdout.write(JSON.stringify(snapshot));
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`pm2 jlist snapshot parse failed: ${message}\n`);
    process.exitCode = 2;
  }
});
