# Tarot Studio — TALKBACK

Append-only critique log for this project (AGENTS.md "Cross-vetting, TALKBACK and challenges").

## 2026-11-20 PT | Reviewer → Worker | review | t-001 design brief (#7670)

**Audit:** A docs-only, reversible architecture and print-production brief. It keeps Kind Oracle as the canonical card identity and reading engine, and it maps the minor suits and court ranks explicitly. It keeps `/admin/tarot` admin-only, reuses the existing `/api/art/enqueue` instead of a second queue, and leaves printing, commerce and publication as human gates. It does not cross into implementation.

**Pattern:** The data-ownership boundary is clear: Tarot Studio owns art and print state, and the oracle engine owns reading text. Future implementation PRs should be held to that boundary.

**Suggestion:** Make the first implementation slice a seed script that generates the 78 `TarotCard` identity rows from `projects/kind-oracle/docs/spec.md`, with a test that every `oracleId` resolves. Do that before any UI work.
