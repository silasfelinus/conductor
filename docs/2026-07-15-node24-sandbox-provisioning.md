# Node 24.x provisioning in the hourly-cycle sandbox

**Task:** challenge-center/t-021 (kaizen from kind-robots/t-014's TALKBACK entry,
which hit the same Node 22-sandbox vs Node 24-CI gap kind-robots/t-015 and t-019
had already run into).

## The problem

kind_robots pins `"engines": { "node": "24.x", "npm": "11.x" }`, and its CI runners
build on Node 24. The hourly-cycle sandbox's default Node is 22.x. Reproducing a red
kind_robots TypeScript/CI check locally (to tell a pre-existing break from a real
regression) needs the exact same major version — Node's type-checking and module
resolution behavior has shifted enough across majors that a 22-vs-24 mismatch is not
a reliable stand-in.

Two paths were ruled out:
- **nvm/fnm** — neither is preinstalled in the sandbox, and t-014's session found no
  reliable way to install one durably (each session is a fresh, ephemeral container —
  nothing persists between hourly runs, so "install nvm once" isn't actually once).
- **nodesource apt repo** (`deb.nodesource.com`) — blocked by the sandbox's proxy
  egress allowlist (`403` on CONNECT).
- **CI artifact download** (e.g. a `typescript-diagnostics` upload) — also ruled out;
  GitHub Actions artifacts redirect to signed Azure Blob Storage URLs, and that host
  isn't on the proxy allowlist either.

## The fix

`nodejs.org` itself **is** reachable through the sandbox's proxy. `scripts/provision_node24.sh`
downloads the official prebuilt `linux-x64` tarball for a pinned Node 24.x release
straight from `https://nodejs.org/dist/` and unpacks it to `$HOME/.nodejs24` — no root,
no package manager, no version manager, no persistent host state to maintain. It's
idempotent (skips the download if the exact pinned version is already unpacked) and
fast (~30MB, a few seconds), so re-running it once per session that needs CI-accurate
Node is cheap.

```bash
source scripts/provision_node24.sh   # exports $NODE24_HOME/bin onto PATH in this shell
node --version                       # v24.18.0 — matches kind_robots' engines pin
```

Or without sourcing, to just provision and print the export line to run yourself:

```bash
scripts/provision_node24.sh
```

Bump the pinned version by setting `NODE24_VERSION` (e.g. `NODE24_VERSION=v24.19.0`)
if kind_robots' CI runner moves to a newer 24.x patch and the exact patch match starts
to matter; the default tracks whatever was current as of this task.

## When to use this

Any time a task needs to reproduce kind_robots CI locally — most commonly, deciding
whether a red TypeScript/lint check on a PR is a pre-existing break on `main` or a
real regression from the diff (see kind-robots/t-014's TALKBACK entry for the pattern:
clean `git worktree` of `origin/main`, Node pinned to match CI, re-run `npm run test`,
compare error sets). Source this script first so the Node version isn't the variable
under test.
