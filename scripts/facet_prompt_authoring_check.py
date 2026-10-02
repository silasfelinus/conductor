#!/usr/bin/env python3
"""
facet_prompt_authoring_check.py -- strict check for hand-authored Facet artPrompts.

Used on the 2026-10-01 card-copy rewrite (projects/kind-robots/repairs/
2026-10-01-facet-card-copy-rewrite.json). Stricter than server/utils/
artPromptContract.ts on purpose: it flags any negation word, "frame",
"silhouette", art-direction jargon, text/format nouns and abstract words, and
any prompt that still contains the Facet's own description. A false positive
(a verb "covers") is cheaper than a render, so reword rather than ignore.
A clean result still never means the prompt is good (ART-PROMPTS.md rule 5).

Usage:
  python scripts/facet_prompt_authoring_check.py repairs.json
where repairs.json is the {"facets": {id: {title, artPrompt, ...}}} shape above.
Exit 1 if any prompt has a problem.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_facet_prompt_subjects as c  # noqa: E402

BAN=[
 (r"\b(?:no|not|without|never|nor|none|free of|devoid of|avoid|don'?t|isn'?t|aren'?t|neither|nothing|nobody|zero)\b","negation"),
 (r"\bframe[sd]?\b|\bframing\b","frame"),
 (r"\bsilhouettes?\b","silhouette"),
 (r"\b(?:concrete|iconic|thumbnail|focal|emblem|unmistakable|subject separation|composition)\b","jargon"),
 (r"\b(?:readable|legible)\b","legibility"),
 (r"\b(?:card|poster|cover|logo|watermark|signature|caption|text|lettering|letters|words?|typography|writing|label|title|banner|sign)s?\b","format/text noun"),
 (r"\b(?:only when|if the|unless|where appropriate|as needed)\b","conditional"),
 (r"\bKind Robots\b|\bFacet\b","app wrapper"),
 (r"\b(?:silly|metaphor|metaphorical|symbolic|symbolizing|represents?|representing|concept|vibe|energy|feeling of|essence)\b","abstract"),
]
def problems(p,title,desc=""):
    out=[]
    for pat,n in BAN:
        m=re.search(pat,p,re.I)
        if m: out.append(f"{n}:{m.group(0)}")
    if c.carries_card_copy(p,desc or ""): out.append("card-copy")
    if len(p)>700: out.append("too-long")
    if len(p)<80: out.append("too-short")
    return out


def main(argv=None) -> int:
    path = (argv or sys.argv[1:] or [None])[0]
    if not path:
        print(__doc__)
        return 2
    facets = json.load(open(path)).get("facets", {})
    bad = 0
    for fid, row in facets.items():
        found = problems(row["artPrompt"], row["title"], row.get("description") or "")
        if found:
            bad += 1
            print(fid, row["title"], found)
    print(f"{len(facets)} prompts, {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
