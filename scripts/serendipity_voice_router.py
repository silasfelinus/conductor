#!/usr/bin/env python3
"""Local-only Serendipity voice request router for Alexa Integration."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from typing import Optional

DOMAINS = {"chat", "character", "dream", "music", "project", "art", "unknown"}
BLOCKED_ACTIONS = ("approve", "merge", "publish", "release", "spend", "buy", "purchase", "delete", "rename", "force push", "force-push")
SAFE_READS = ("pending approvals", "summarize approvals", "human gates", "approval gates")

PROJECT_PATTERNS = (
    re.compile(r"\bgoal of (?P<project>[a-z0-9][a-z0-9 _-]*)\b", re.I),
    re.compile(r"\bnext for (?P<project>[a-z0-9][a-z0-9 _-]*)\b", re.I),
    re.compile(r"\bwork on (?P<project>[a-z0-9][a-z0-9 _-]*)\b", re.I),
    re.compile(r"\bmove (?P<project>[a-z0-9][a-z0-9 _-]*) forward\b", re.I),
    re.compile(r"\bdraft a task for (?P<project>[a-z0-9][a-z0-9 _-]*) to (?P<intent>.+)$", re.I),
)
CHARACTER_PATTERNS = (
    re.compile(r"\bask (?P<character>[a-z0-9][a-z0-9 _-]*) (?P<intent>.+)$", re.I),
    re.compile(r"\bhave (?P<character>[a-z0-9][a-z0-9 _-]*) (?P<intent>.+)$", re.I),
)
DREAM_PATTERNS = (
    re.compile(r"\bstart (?:a |an )?(?P<genre>[a-z0-9][a-z0-9 _-]*) story in (?P<location>[a-z0-9][a-z0-9 _-]*)\b", re.I),
    re.compile(r"\bcontinue (?:the )?(?P<dream>[a-z0-9][a-z0-9 _-]*) dream\b", re.I),
    re.compile(r"\btell (?:me )?(?:a |an )?(?P<genre>[a-z0-9][a-z0-9 _-]*) story\b", re.I),
)
MUSIC_PATTERNS = (
    re.compile(r"\bplay (?P<music>[a-z0-9][a-z0-9 _'\-.]*)$", re.I),
    re.compile(r"\bput on (?P<music>[a-z0-9][a-z0-9 _'\-.]*)$", re.I),
)
ART_PATTERNS = (
    re.compile(r"\b(?:generate|make|create|draw|render) (?:an? )?(?:image|art|picture|illustration) (?:of |for |showing )?(?P<prompt>.+)$", re.I),
    re.compile(r"\bart prompt (?P<prompt>.+)$", re.I),
)


@dataclass
class SerendipityVoiceRequest:
    rawText: str
    normalizedText: str
    domain: str
    userIntent: str
    requiresConfirmation: bool = False
    clarification: Optional[str] = None
    blockedReason: Optional[str] = None
    projectSlug: Optional[str] = None
    dreamSlug: Optional[str] = None
    characterSlug: Optional[str] = None
    musicTarget: Optional[str] = None
    artPrompt: Optional[str] = None


def slugify(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or None


def strip_serendipity_prefix(raw_text: str) -> str:
    text = " ".join(raw_text.strip().split())
    lowered = text.lower()
    prefixes = (
        "alexa, ask serendipity to ",
        "alexa ask serendipity to ",
        "ask serendipity to ",
        "alexa, open serendipity and ",
        "alexa open serendipity and ",
        "open serendipity and ",
        "serendipity: ",
        "serendipity, ",
        "serendipity ",
    )
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return text[len(prefix):].strip()
    if lowered in {"serendipity", "alexa, open serendipity", "alexa open serendipity", "open serendipity"}:
        return ""
    return text


def blocked_reason(text: str) -> Optional[str]:
    lowered = text.lower()
    if any(safe in lowered for safe in SAFE_READS):
        return None
    if any(action in lowered for action in BLOCKED_ACTIONS):
        return "That needs a safer review path. I can summarize or draft, but I cannot complete that by voice."
    return None


def domain_matches(text: str) -> set[str]:
    lowered = text.lower()
    matches: set[str] = set()
    if any(pattern.search(text) for pattern in ART_PATTERNS) or any(term in lowered for term in ("generate art", "make art", "create art", "image prompt")):
        matches.add("art")
    if any(pattern.search(text) for pattern in MUSIC_PATTERNS):
        matches.add("music")
    if any(pattern.search(text) for pattern in DREAM_PATTERNS) or "story" in lowered or "dream" in lowered:
        matches.add("dream")
    if any(pattern.search(text) for pattern in CHARACTER_PATTERNS) or "character" in lowered:
        matches.add("character")
    if any(pattern.search(text) for pattern in PROJECT_PATTERNS) or any(term in lowered for term in ("project", "waypoint", "roadmap", "task for", "what is next", "what's next", "goal of")):
        matches.add("project")
    if any(term in lowered for term in ("ask ami", "chat", "talk to", "question", "explain", "why", "how do i", "what is")) and not matches:
        matches.add("chat")
    return matches


def extract_project(text: str) -> tuple[Optional[str], str]:
    for pattern in PROJECT_PATTERNS:
        match = pattern.search(text)
        if match:
            return slugify(match.groupdict().get("project")), (match.groupdict().get("intent") or text).strip()
    return None, text


def extract_character(text: str) -> tuple[Optional[str], str]:
    for pattern in CHARACTER_PATTERNS:
        match = pattern.search(text)
        if match:
            return slugify(match.groupdict().get("character")), (match.groupdict().get("intent") or text).strip()
    return None, text


def extract_dream(text: str) -> Optional[str]:
    for pattern in DREAM_PATTERNS:
        match = pattern.search(text)
        if match:
            data = match.groupdict()
            if data.get("dream"):
                return slugify(data["dream"])
            return slugify(" ".join(part for part in (data.get("genre"), data.get("location")) if part))
    return None


def extract_music(text: str) -> Optional[str]:
    for pattern in MUSIC_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group("music").strip()
    return None


def extract_art_prompt(text: str) -> Optional[str]:
    for pattern in ART_PATTERNS:
        match = pattern.search(text)
        if match:
            prompt = match.groupdict().get("prompt")
            return prompt.strip() if prompt else None
    return None


def parse_serendipity_voice_request(raw_text: str) -> SerendipityVoiceRequest:
    normalized = strip_serendipity_prefix(raw_text)
    if not normalized:
        return SerendipityVoiceRequest(raw_text, normalized, "unknown", "", True, "What would you like Serendipity to do?")

    reason = blocked_reason(normalized)
    matches = domain_matches(normalized)
    if reason:
        domain = next(iter(matches)) if len(matches) == 1 else "unknown"
        return SerendipityVoiceRequest(raw_text, normalized, domain, normalized, True, "I can draft or summarize that, but I need a safer review path before doing it.", reason)

    if len(matches) > 1:
        return SerendipityVoiceRequest(raw_text, normalized, "unknown", normalized, True, "Do you want chat, a character, a dream story, music, art, or project work?")

    domain = next(iter(matches)) if matches else "unknown"
    request = SerendipityVoiceRequest(raw_text, normalized, domain, normalized)

    if domain == "project":
        request.projectSlug, request.userIntent = extract_project(normalized)
    elif domain == "character":
        request.characterSlug, request.userIntent = extract_character(normalized)
    elif domain == "dream":
        request.dreamSlug = extract_dream(normalized)
    elif domain == "music":
        request.musicTarget = extract_music(normalized)
    elif domain == "art":
        request.artPrompt = extract_art_prompt(normalized)
    else:
        request.requiresConfirmation = True
        request.clarification = "Do you want chat, a character, a dream story, music, art, or project work?"

    if domain == "project" and not request.projectSlug:
        request.requiresConfirmation = True
        request.clarification = "Which project should I use?"
    if domain == "character" and not request.characterSlug:
        request.requiresConfirmation = True
        request.clarification = "Which character should answer?"
    if domain == "music" and not request.musicTarget:
        request.requiresConfirmation = True
        request.clarification = "What should I play?"
    if domain == "art" and not request.artPrompt:
        request.requiresConfirmation = True
        request.clarification = "What should the art show?"

    return request


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse local Serendipity voice requests.")
    parser.add_argument("request", nargs="*")
    args = parser.parse_args()
    raw = " ".join(args.request).strip() or sys.stdin.read().strip()
    print(json.dumps(asdict(parse_serendipity_voice_request(raw)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
