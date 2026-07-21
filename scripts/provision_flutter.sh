#!/usr/bin/env bash
# provision_flutter.sh — get a Flutter SDK toolchain into PATH inside an ephemeral
# web-session sandbox, so apps/* Flutter tasks (superkate-services-calculator,
# alexa-integration, appmaker scaffolds, etc.) can run `flutter analyze` /
# `flutter test` locally instead of being inspected-not-verified.
#
# Background: conductor/t-028 (kaizen from superkate/t-022, PR #343, merged
# 2026-07-10), a recurring TALKBACK theme — web sessions historically had no
# Flutter toolchain, so apps/* changes were reviewed by reading, never by
# actually running the SDK's own checks. A 2026-07-20 cycle confirmed a plain
# SDK download works fine in this sandbox: storage.googleapis.com is reachable
# through the egress allowlist, no apt/root/version-manager needed.
#
# Mirrors scripts/provision_node24.sh: idempotent, no root, no version manager,
# no persistent host state (each session is a fresh container, so this reruns
# cheaply whenever it's actually needed — it is NOT auto-run at session start,
# since most sessions never touch a Flutter app and the download is ~1.4GB /
# ~60-90s the first time a session needs it).
#
# Usage:
#   source scripts/provision_flutter.sh   # adds $FLUTTER_HOME/bin to PATH in this shell
#   scripts/provision_flutter.sh          # just provisions; prints the PATH export to run yourself
#
# Override the exact version with FLUTTER_VERSION (default: latest known-good stable
# confirmed working in this sandbox).

set -euo pipefail

FLUTTER_VERSION="${FLUTTER_VERSION:-3.32.5}"
FLUTTER_HOME="${FLUTTER_HOME:-$HOME/.flutter}"
ARCHIVE="flutter_linux_${FLUTTER_VERSION}-stable.tar.xz"
URL="https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/${ARCHIVE}"

if [ -x "${FLUTTER_HOME}/bin/flutter" ] \
   && "${FLUTTER_HOME}/bin/flutter" --version 2>/dev/null | grep -q "Flutter ${FLUTTER_VERSION}"; then
  echo "flutter: already provisioned at ${FLUTTER_HOME} (${FLUTTER_VERSION})" >&2
else
  echo "flutter: downloading ${URL} (~1.4GB, this takes a minute or two)" >&2
  TMP_TAR="$(mktemp -t flutter-XXXXXX.tar.xz)"
  trap 'rm -f "${TMP_TAR}"' EXIT
  curl -fsSL -o "${TMP_TAR}" "${URL}"
  rm -rf "${FLUTTER_HOME}"
  mkdir -p "${FLUTTER_HOME}"
  tar -xJf "${TMP_TAR}" -C "${FLUTTER_HOME}" --strip-components=1
  echo "flutter: provisioned at ${FLUTTER_HOME}" >&2
fi

# The sandbox runs as root; flutter shells out to git against its own SDK
# checkout and against `$FLUTTER_HOME` being owned by the invoking user, and
# git's dubious-ownership check can otherwise abort that. Mark it safe once,
# idempotently (git de-dupes repeated --add values for the same path).
git config --global --add safe.directory "${FLUTTER_HOME}"

export PATH="${FLUTTER_HOME}/bin:${PATH}"
echo "export PATH=\"${FLUTTER_HOME}/bin:\$PATH\""
flutter --version >&2
