#!/usr/bin/env bash
# provision_node24.sh — get a Node 24.x toolchain into PATH inside an ephemeral
# hourly-cycle sandbox, for local reproduction of kind_robots' CI (engines: "node": "24.x").
#
# Background: challenge-center/t-021 (kaizen from kind-robots/t-014, t-015, t-019).
# The sandbox's default Node is 22.x; nvm/fnm are not preinstalled, and package-manager
# installs (nodesource apt repo) are blocked by the sandbox's egress allowlist. This
# script downloads the official prebuilt tarball straight from nodejs.org, which IS
# reachable through the proxy, and unpacks it locally — no root, no version manager,
# no persistent host state (each session is a fresh container, so this reruns cheaply
# every time it's needed; ~30MB download, a few seconds).
#
# Usage:
#   source scripts/provision_node24.sh   # adds $NODE24_HOME/bin to PATH in this shell
#   scripts/provision_node24.sh          # just provisions; prints the PATH export to run yourself
#
# Override the exact version with NODE24_VERSION (default: latest known-good 24.x LTS).

set -euo pipefail

NODE24_VERSION="${NODE24_VERSION:-v24.18.0}"
NODE24_HOME="${NODE24_HOME:-$HOME/.nodejs24}"
ARCHIVE="node-${NODE24_VERSION}-linux-x64.tar.xz"
URL="https://nodejs.org/dist/${NODE24_VERSION}/${ARCHIVE}"

if [ -x "${NODE24_HOME}/bin/node" ] && "${NODE24_HOME}/bin/node" --version | grep -q "^${NODE24_VERSION}$"; then
  echo "node24: already provisioned at ${NODE24_HOME} ($("${NODE24_HOME}/bin/node" --version))" >&2
else
  echo "node24: downloading ${URL}" >&2
  TMP_TAR="$(mktemp -t node24-XXXXXX.tar.xz)"
  trap 'rm -f "${TMP_TAR}"' EXIT
  curl -fsSL -o "${TMP_TAR}" "${URL}"
  mkdir -p "${NODE24_HOME}"
  tar -xJf "${TMP_TAR}" -C "${NODE24_HOME}" --strip-components=1
  echo "node24: provisioned $("${NODE24_HOME}/bin/node" --version) at ${NODE24_HOME}" >&2
fi

export PATH="${NODE24_HOME}/bin:${PATH}"
echo "export PATH=\"${NODE24_HOME}/bin:\$PATH\""
node --version >&2
npm --version >&2
