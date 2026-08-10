#!/usr/bin/env bash
# provision_kind_robots_deps.sh — install kind_robots' node_modules + Prisma
# client inside an ephemeral sandbox so burst-mode sessions can run vue-tsc /
# eslint locally instead of guessing at TypeScript CI failures.
#
# Background: conductor/t-046 (kaizen from coloring-book/t-020, kind_robots PR
# #290). Getting a local `npm ci` to complete in the sandbox needs two
# non-obvious workarounds that every session was otherwise re-deriving:
#   1. CYPRESS_INSTALL_BINARY=0 — cypress' postinstall downloads a standalone
#      binary from Cypress' own CDN, which the egress allowlist rejects
#      (ECONNRESET) and which aborts the whole `npm ci`. Skipping just that
#      download lets everything else finish, including the postinstall
#      `nuxi prepare` that generates the `.nuxt` type stubs vue-tsc needs.
#   2. A well-formed dummy DATABASE_URL — Prisma config loading fails without
#      one. No real DB connectivity is required for `prisma generate` or
#      `vue-tsc`; any mysql://-shaped value works locally (CI uses a
#      127.0.0.1:3306 one).
# npmjs.org's registry IS reachable through the proxy, so `npm ci` itself works.
#
# Coloring-book recovery also emits WebP files through Pillow. Fresh sandboxes do
# not reliably include it, which made recovery runs repeatedly fail once before
# installing the same dependency by hand. Provision it here once, idempotently.
#
# Mirrors scripts/provision_node24.sh: idempotent, no root, no version manager,
# no persistent host state (reruns cheaply in each fresh container).
#
# Usage:
#   source scripts/provision_kind_robots_deps.sh   # provisions + exports env in this shell
#   scripts/provision_kind_robots_deps.sh          # provisions; prints the env exports to run yourself
#
# Env overrides:
#   KIND_ROBOTS_ROOT   path to the kind_robots checkout (default: sibling of this repo)
#   DATABASE_URL       Prisma connection string (default: a dummy local mysql URL)
#   PYTHON_BIN         Python executable used to verify/install Pillow (default: python3, then python)
#   FORCE_REINSTALL=1  reinstall node_modules even if it already looks complete

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
CONDUCTOR_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
KIND_ROBOTS_ROOT="${KIND_ROBOTS_ROOT:-$(cd "${CONDUCTOR_ROOT}/.." && pwd)/kind_robots}"

if [ ! -d "${KIND_ROBOTS_ROOT}" ]; then
  echo "kr-deps: kind_robots checkout not found at ${KIND_ROBOTS_ROOT}" >&2
  echo "kr-deps: set KIND_ROBOTS_ROOT to its path and re-run." >&2
  return 1 2>/dev/null || exit 1
fi

# 1. Node 24.x toolchain (kind_robots' engines field). Reuse the sibling script;
#    sourcing it puts node24 on PATH in this shell.
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/provision_node24.sh" >/dev/null

# 2. Prisma needs a well-formed DATABASE_URL (no live DB required).
export DATABASE_URL="${DATABASE_URL:-mysql://user:pass@127.0.0.1:3306/kindrobots}"

# 3. Coloring-book recovery writes WebP output through Pillow. Install only when
#    the active Python cannot import PIL, so repeated provisioning stays cheap.
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "kr-deps: neither python3 nor python is available; cannot provision Pillow" >&2
  return 1 2>/dev/null || exit 1
fi
if ! "${PYTHON_BIN}" -c 'from PIL import Image' >/dev/null 2>&1; then
  echo "kr-deps: installing Pillow for coloring-book WebP recovery" >&2
  "${PYTHON_BIN}" -m pip install --user Pillow
else
  echo "kr-deps: Pillow already available" >&2
fi

# 4. Install dependencies (skipping only the Cypress binary download).
if [ -z "${FORCE_REINSTALL:-}" ] && [ -d "${KIND_ROBOTS_ROOT}/node_modules" ] \
   && [ -d "${KIND_ROBOTS_ROOT}/prisma/generated/prisma" ] \
   && [ -d "${KIND_ROBOTS_ROOT}/.nuxt" ]; then
  echo "kr-deps: node_modules + generated Prisma client + .nuxt already present —" \
    "skipping install (FORCE_REINSTALL=1 to redo)" >&2
else
  echo "kr-deps: installing kind_robots deps (CYPRESS_INSTALL_BINARY=0) — this takes ~30s" >&2
  ( cd "${KIND_ROBOTS_ROOT}" && CYPRESS_INSTALL_BINARY=0 npm ci --no-audit --no-fund )
  # postinstall runs `nuxi prepare` (generates .nuxt type stubs). Generate the
  # Prisma client explicitly too, in case a cached node_modules skipped it.
  ( cd "${KIND_ROBOTS_ROOT}" && npx --no-install prisma generate )
  echo "kr-deps: done — node_modules, .prisma/client, and .nuxt are ready" >&2
fi

# Echo the exports so a plain (non-sourced) invocation is still usable:
echo "export DATABASE_URL=\"${DATABASE_URL}\""
echo "# now: cd \"${KIND_ROBOTS_ROOT}\" && npm run test   # vue-tsc typecheck" >&2
