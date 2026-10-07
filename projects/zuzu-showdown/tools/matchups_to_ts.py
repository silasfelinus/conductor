"""zuzu-showdown t-019: port matchups.yaml to kind_robots as JSON data.

    python projects/zuzu-showdown/tools/matchups_to_ts.py KIND_ROBOTS_DIR [--check]

matchups.yaml stays the source of truth (t-018 writes and checks it). This writes it as
utils/zuzuShowdown/matchups.json, which kind_robots' matchups.ts imports for the VS and win screens.
--check exits 1 when the JSON there holds different lines than the YAML (compared as data, so
formatting the JSON never makes it stale).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
TARGET = Path("utils/zuzuShowdown/matchups.json")


def port(data: dict) -> dict:
    return {
        "source": "conductor projects/zuzu-showdown/matchups.yaml (tools/matchups_to_ts.py); edit there, not here",
        "matchups": [
            {
                "pair": entry["pair"],
                "intro": [{"speaker": t["speaker"], "line": t["line"]} for t in entry["intro"]],
                "win": entry["win"],
            }
            for entry in data["matchups"]
        ],
        "boss": data["boss"]["intro"],
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    out = Path(argv[0]) / TARGET
    data = port(yaml.safe_load((HERE / "matchups.yaml").read_text()))
    if "--check" in argv:
        if not out.exists() or json.loads(out.read_text()) != data:
            print(f"{out} is stale: re-run tools/matchups_to_ts.py")
            return 1
        print(f"{out} matches matchups.yaml")
        return 0
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
