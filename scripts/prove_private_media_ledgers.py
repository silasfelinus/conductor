#!/usr/bin/env python3
"""Prove authenticated source bytes, game-media bytes and private access per ledger.

Reusable by both Prom canon and Tactics workflows. Each source ledger is
checkpointed immediately, even when its download fails; this preserves real
ArtJob/media evidence instead of losing it to a later failing batch. No media
bytes, bearer tokens, signed URLs or metadata response bodies enter logs.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

if __package__:
    from .verify_prom_tactics_media import candidates
else:
    from verify_prom_tactics_media import candidates


def parse_ledger(value: str) -> tuple[Path, int]:
    try:
        name, count_text = value.rsplit(":", 1)
        count = int(count_text)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("expected ledger-path.yaml:count") from exc
    path = Path(name)
    if not path.is_file() or path.suffix != ".yaml" or count <= 0:
        raise argparse.ArgumentTypeError("ledger must exist and count be positive")
    return path, count


def verify_private_metadata(path: Path, expected: int, request=None) -> int:
    """Confirm every accepted receipt remains private, without leaking API details."""
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if document.get("is_public") is not False:
        raise ValueError("private candidate ledger has incorrect visibility")
    rows = candidates([path])
    if len(rows) != expected:
        raise ValueError("private receipt count changed after verification")
    if request is None:
        if __package__:
            from . import consume_art_queue_core as core
        else:
            import consume_art_queue_core as core

        def request(image_id):
            return core.http_json(
                "GET", f"{core.KR_BASE_URL}/api/art/image/{image_id}"
            )

    for row in rows:
        status, payload = request(row["image_id"])
        flag = ((payload or {}).get("data") or {}).get("isPublic")
        if status != 200 or flag is not False:
            raise PermissionError("ArtImage visibility is not private")
    return len(rows)


def prove_ledger(
    path: Path,
    count: int,
    *,
    write_evidence: bool,
    require_private: bool,
    checkpoint_message: str,
    runner=subprocess.run,
    request=None,
) -> bool:
    path_text = str(path)
    src = [
        sys.executable,
        "scripts/verify_prom_tactics_media.py",
        path_text,
        "--require-count",
        str(count),
    ]
    if write_evidence:
        src.append("--write-evidence")
    source_ok = runner(src, check=False).returncode == 0

    runtime_ok = False
    if source_ok:
        runtime_ok = (
            runner(
                [
                    sys.executable,
                    "scripts/verify_tactics_runtime_media.py",
                    path_text,
                    "--require-count",
                    str(count),
                ],
                check=False,
            ).returncode
            == 0
        )

    # Always persist authentic partial receipts before touching another ledger.
    checkpoint_ok = True
    if write_evidence:
        checkpoint_ok = (
            runner(
                ["bash", "scripts/checkpoint_art_state.sh", checkpoint_message],
                check=False,
            ).returncode
            == 0
        )

    private_ok = False
    if source_ok and runtime_ok and checkpoint_ok and require_private:
        try:
            private_count = verify_private_metadata(path, count, request=request)
            print(f"PRIVATE_POLICY_VERIFIED={private_count} ledger={path.name}")
            private_ok = True
        except Exception as exc:
            # Never print str(exc): HTTP failures may include tokens or signed URLs.
            print(f"PRIVATE_POLICY_FAILED={path.name} type={type(exc).__name__}")
    elif not require_private:
        private_ok = True

    passed = source_ok and runtime_ok and checkpoint_ok and private_ok
    print(
        f"LEDGER_MEDIA_PROOF ledger={path.name} expected={count} "
        f"source={int(source_ok)} runtime={int(runtime_ok)} "
        f"checkpoint={int(checkpoint_ok)} private={int(private_ok)}"
    )
    return passed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger",
        action="append",
        required=True,
        type=parse_ledger,
        help="private ledger path and exact expected ArtImage count, path.yaml:count",
    )
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--require-private", action="store_true")
    parser.add_argument(
        "--checkpoint-message",
        default="chore: checkpoint verified private media receipts [skip ci]",
    )
    args = parser.parse_args(argv)
    all_good = True
    for path, count in args.ledger:
        good = prove_ledger(
            path,
            count,
            write_evidence=args.write_evidence,
            require_private=args.require_private,
            checkpoint_message=args.checkpoint_message,
        )
        all_good = good and all_good
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
