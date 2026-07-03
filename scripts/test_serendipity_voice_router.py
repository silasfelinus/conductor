#!/usr/bin/env python3
"""Deterministic tests for scripts/serendipity_voice_router.py."""

from serendipity_voice_router import parse_serendipity_voice_request


def check(raw, **expected):
    parsed = parse_serendipity_voice_request(raw)
    for key, value in expected.items():
        actual = getattr(parsed, key)
        assert actual == value, f"{raw!r}: expected {key}={value!r}, got {actual!r}"
    return parsed


def main():
    check(
        "Serendipity: what is the goal of Alexa Integration",
        domain="project",
        projectSlug="alexa-integration",
        requiresConfirmation=False,
    )
    check(
        "Alexa, ask Serendipity to what is next for kind robots",
        domain="project",
        projectSlug="kind-robots",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: ask AMI why my relay is cranky",
        domain="character",
        characterSlug="ami",
        userIntent="why my relay is cranky",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: have Professor Sparklebiscuit explain this as a dungeon quest",
        domain="character",
        characterSlug="professor-sparklebiscuit",
        userIntent="explain this as a dungeon quest",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: start a cozy mystery story in the redwood library",
        domain="dream",
        dreamSlug="cozy-mystery-redwood-library",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: draft a task for Alexa Integration to add account linking notes",
        domain="project",
        projectSlug="alexa-integration",
        userIntent="add account linking notes",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: play rainy day coding playlist",
        domain="music",
        musicTarget="rainy day coding playlist",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: generate art of a robot fox painting a portal",
        domain="art",
        artPrompt="a robot fox painting a portal",
        requiresConfirmation=False,
    )
    check(
        "Serendipity: waffles",
        domain="unknown",
        requiresConfirmation=True,
    )
    print("serendipity_voice_router: 9 checks passed")


if __name__ == "__main__":
    main()
