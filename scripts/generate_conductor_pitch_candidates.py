#!/usr/bin/env python3
"""
generate_conductor_pitch_candidates.py — brainstorm/t-020: reconnect Conductor
proposal ideation as an explicit downstream consumer of Kind Robots' own
Brainstorm engine, instead of Conductor generating pitches internally.

Per projects/brainstorm/DESIGN-BRIEF.md's "Relationship to Conductor's
proposal generator" section:
    - Brainstorm generates candidate ideas in Kind Robots application state.
    - Conductor decides whether something becomes a coordination pitch/task.
    - No user brainstorm silently mutates a roadmap or project lifecycle.

This script is the "request candidate ideas" half only. It calls the live
POST /api/brainstorm/generate endpoint (the same one the public /brainstorm
product uses), asking for small-to-medium Kind-Robots-ecosystem project
pitches, then runs a cheap local novelty heuristic against every existing
pitch title and every known project slug/goal so an obvious duplicate is
flagged before a human/agent spends time on it.

It deliberately does NOT write pitches/*.md itself -- promoting a candidate
into a canonical pitch is a Conductor policy decision (existing-work check,
vetting, the pitch template's fuller narrative sections), not something this
script should do unattended. Run it, review the JSON it prints, and hand-author
the surviving candidate(s) as a normal pitches/*.md file per AGENTS.md's pitch
template if one clears the bar.

Requires: KR_API_TOKEN env var (a valid kind_robots JWT for Silas's account --
see scripts/kr_token_set.sh to check presence safely). Spends a small amount
of that account's mana per run, same as any other automated text-generation
call already made routinely by daily-dream tooling in this repo.

API:  GET  https://kindrobots.org/api/server           (pick a usable text server)
      POST https://kindrobots.org/api/brainstorm/generate

Usage:
    python scripts/generate_conductor_pitch_candidates.py [--count N] [--server-id ID]

Exit codes: 0 = success (even if all candidates flagged as likely duplicates),
            1 = auth/network/API failure, 2 = no usable text server found
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://kindrobots.org"
SERVER_LIST_URL = f"{BASE_URL}/api/server"
GENERATE_URL = f"{BASE_URL}/api/brainstorm/generate"

# Providers whose credentials live server-side (not tied to network location),
# so the brainstorm backend's public/official/default visibility gate doesn't
# apply to them -- see kind_robots server/api/brainstorm/generate.post.ts's
# assertBackendProviderAccess(): `if (provider === 'openai' || provider ===
# 'anthropic') return`. A COMFY server is art-only and never text-compatible.
TEXT_CAPABLE_SERVER_TYPES = {"OPENAI", "ANTHROPIC", "OLLAMA", "CUSTOM"}
BACKEND_KEYED_SERVER_TYPES = {"OPENAI", "ANTHROPIC"}

PREMISE = (
    "Pitch one small-to-medium-scope project or product idea that could become "
    "a first-class project in the Kind Robots / Conductor ecosystem: a family of "
    "small, personally-meaningful creative-AI tools, games, and content pipelines "
    "built by one person with AI agents doing the implementation work. Good ideas "
    "are buildable in weeks not months, fit the platform's existing playful, "
    "handmade, non-corporate tone, and either extend something already shipped "
    "(a new surface for existing assets/pipelines) or fill a clear, currently-"
    "empty gap in the product family. Do not pitch generic SaaS boilerplate, "
    "ad-driven content mills, or anything requiring licensing/legal review to "
    "even prototype."
)

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "with",
    "is", "are", "be", "this", "that", "it", "as", "at", "by", "from", "into",
    "project", "kind", "robots", "conductor", "new", "using", "use", "via",
}


def tokenize(text: str) -> set:
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def load_existing_novelty_corpus():
    """Returns list of (label, token_set) for every existing pitch title and
    every known project's slug + goal, so a fresh candidate can be checked
    for overlap against both."""
    corpus = []

    pitches_dir = REPO_ROOT / "pitches"
    for path in sorted(pitches_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^#\s*Pitch:\s*(.+)$", text, re.MULTILINE)
        title = m.group(1).strip() if m else path.stem
        corpus.append((f"pitch:{path.name}", tokenize(title)))

    overrides_path = REPO_ROOT / "project-overrides.yaml"
    known_slugs = set()
    if overrides_path.exists():
        overrides = yaml.safe_load(overrides_path.read_text(encoding="utf-8")) or {}
        for entry in overrides.get("overrides", []):
            slug = entry.get("slug")
            if slug:
                known_slugs.add(slug)
                corpus.append((f"project-slug:{slug}", tokenize(slug.replace("-", " "))))

    projects_dir = REPO_ROOT / "projects"
    for roadmap_path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = roadmap_path.parent.name
        if slug == "_template":
            continue
        try:
            data = yaml.safe_load(roadmap_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        goal = data.get("goal", "")
        if goal:
            corpus.append((f"project-goal:{slug}", tokenize(goal)))

    return corpus


def score_novelty(candidate_text: str, corpus) -> dict:
    tokens = tokenize(candidate_text)
    best_label, best_score = None, 0.0
    for label, other_tokens in corpus:
        score = jaccard(tokens, other_tokens)
        if score > best_score:
            best_label, best_score = label, score
    return {"closest_match": best_label, "similarity": round(best_score, 3)}


def http_get(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def http_post(url: str, token: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read())


def pick_text_server(servers: list, explicit_id: int = None):
    if explicit_id is not None:
        for s in servers:
            if s.get("id") == explicit_id:
                return s
        return None

    def is_text_capable(s):
        category = (s.get("category") or "").lower()
        if category:
            return category in ("text", "chat")
        return (s.get("serverType") or "").upper() in TEXT_CAPABLE_SERVER_TYPES

    candidates = [s for s in servers if is_text_capable(s)]
    if not candidates:
        return None

    # Prefer a backend-keyed provider (OpenAI/Anthropic) since those bypass
    # the public/official/default visibility gate entirely on the backend
    # (see module docstring); fall back to isDefault/isOfficial/isPublic,
    # then just the first text-capable server.
    def rank(s):
        server_type = (s.get("serverType") or "").upper()
        return (
            0 if server_type in BACKEND_KEYED_SERVER_TYPES else 1,
            0 if s.get("isDefault") else 1,
            0 if s.get("isOfficial") else 1,
            0 if s.get("isPublic") else 1,
        )

    candidates.sort(key=rank)
    return candidates[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=6, help="number of candidates to request (1-24)")
    parser.add_argument("--server-id", type=int, default=None, help="override text server id")
    parser.add_argument("--dry-run", action="store_true", help="skip the API calls; just print the request that would be sent")
    args = parser.parse_args()

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("KR_API_TOKEN not set -- see scripts/kr_token_set.sh", file=sys.stderr)
        return 1

    corpus = load_existing_novelty_corpus()
    print(f"Novelty corpus: {len(corpus)} existing pitch/project entries.", file=sys.stderr)

    payload = {
        "premise": PREMISE,
        "count": args.count,
        "outputDomain": "ideas",
        "batchShape": "assortment",
        "returnTypes": [
            {"id": "practical"},
            {"id": "left-field"},
            {"id": "inversion"},
        ],
        "mode": "freeform",
    }

    if args.dry_run:
        print(json.dumps({"would_post_to": GENERATE_URL, "payload": payload}, indent=2))
        return 0

    try:
        servers = http_get(SERVER_LIST_URL, token)
    except urllib.error.HTTPError as e:
        print(f"GET {SERVER_LIST_URL} failed: HTTP {e.code}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"GET {SERVER_LIST_URL} failed: {e}", file=sys.stderr)
        return 1

    if isinstance(servers, dict):
        servers = servers.get("data", servers.get("servers", []))
    if not isinstance(servers, list):
        print("Unexpected /api/server response shape.", file=sys.stderr)
        return 1

    server = pick_text_server(servers, args.server_id)
    if not server:
        print("No usable text-capable server found on this account.", file=sys.stderr)
        return 2

    payload["server"] = {"id": server["id"]}
    print(
        f"Using server id={server['id']} label={server.get('label') or server.get('title')} "
        f"type={server.get('serverType')}",
        file=sys.stderr,
    )

    try:
        response = http_post(GENERATE_URL, token, payload)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(f"POST {GENERATE_URL} failed: HTTP {e.code} -- {detail}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"POST {GENERATE_URL} failed: {e}", file=sys.stderr)
        return 1

    if not response.get("success"):
        print(f"Brainstorm generation failed: {response.get('message')}", file=sys.stderr)
        return 1

    candidates = response.get("data", {}).get("candidates", [])
    mana = response.get("mana", {})
    print(
        f"Generated {len(candidates)} candidate(s). mana charged={mana.get('charged')} "
        f"balance={mana.get('balance')}",
        file=sys.stderr,
    )

    results = []
    for c in candidates:
        novelty = score_novelty(f"{c.get('title', '')} {c.get('text', '')}", corpus)
        likely_duplicate = novelty["similarity"] >= 0.35
        results.append(
            {
                "id": c.get("id"),
                "title": c.get("title"),
                "text": c.get("text"),
                "novelty": novelty,
                "likely_duplicate": likely_duplicate,
            }
        )

    print(json.dumps({"server_id": server["id"], "candidates": results}, indent=2))

    novel_count = sum(1 for r in results if not r["likely_duplicate"])
    print(
        f"{novel_count}/{len(results)} candidate(s) below the duplicate-similarity "
        f"threshold and worth a human/agent look.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
