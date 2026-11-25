"""Write verdicts into an art ledger: python3 verdicts.py <ledger.yaml> <verdicts.json> (a {key: verdict} map).

A subject that already has a verdict right after its key is left alone; edit those by hand.
"""

import json
import re
import sys
from pathlib import Path

import yaml

p = Path(sys.argv[1])
t = p.read_text()
for key, verdict in json.loads(Path(sys.argv[2]).read_text()).items():
    if re.search(rf"^- key: {re.escape(key)}\n  verdict:", t, flags=re.MULTILINE):
        continue
    block = "".join(
        "  " + line + "\n"
        for line in yaml.safe_dump({"verdict": verdict}, width=118).splitlines()
    )
    t, n = re.subn(
        rf"(^- key: {re.escape(key)}\n)",
        lambda m, block=block: m.group(1) + block,
        t,
        flags=re.MULTILINE,
    )
    assert n == 1, key
p.write_text(t)
yaml.safe_load(t)
print("ok")
