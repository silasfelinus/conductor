# t-010 — Local dry-run transcript

Captured 2026-07-20 (conductor burst-rotation session) by running the manual
test script from `rollout-safety-checklist.md` §4 against the current
`silasfelinus/serendipity-voice` `main` (via `npm run handle -- "<utterance>"`),
with no `.env` present — every feature flag at its safe default (art/chat/music
all disabled, no service token, no signature verification needed since nothing
left the process). This is a **local CLI dry run**, not a real Echo/Alexa call;
it exercises exactly the same `handleVoiceRequest` entry point the relay uses,
so the routing/adapter behavior is representative of a real request.

Baseline: `npm test` — 12 suites, all green (voice-router 23, relay-bus 15,
runtime-config 19, identity 15, music-adapter 5, handle-voice-request 21,
skill-event 12, verify-request 15, project-work-status 13, voice-bridge 30,
art-submit 33, chat-submit 20 checks) before running any of the below.

## Results

| # | Utterance | Expected (checklist §4) | Actual domain/adapter | Verdict |
|---|---|---|---|---|
| 1 | `what is the goal of Alexa integration.` | Reads PROJECT Dream goal, no state change | `project` / PROJECT Dream goal + waypoints spoken | PASS |
| 2 | `what is next for Alexa integration.` | Reads the next ready roadmap task, no state change | `project` / same PROJECT Dream goal readout as #1 (does not name a specific next task) | PARTIAL — see Finding 1 |
| 3 | `ask AMI why the relay is cranky.` | Routes to chat/LLM, speaks a short answer | `character` (slug `ami`) / stub character reply | PARTIAL — see Finding 2 |
| 4 | `have a Character explain Alexa integration as a quest.` | Routes through Character/persona context, speaks a short answer | `character` (slug `a-character`, literal capture) / stub character reply | PASS (behaves as designed; slug is literal because no name follows "a") |
| 5 | `start a cozy mystery in the redwood library.` | Creates/mocks a Dream story seed, no unapproved DB write | `unknown` / asks "chat, character, dream story, art, music, or project work?" | FAIL — see Finding 3 |
| 6 | `draft a task for Alexa integration to add router tests.` | Asks for confirmation before creating any Todo/draft | `project` / drafted locally, `requiresConfirmation: true`, "Nothing was written to Conductor." | PASS |
| 7 | `play rainy day coding.` | If music disabled, says so; else resolves configured roots only | `music` / "local playback is disabled until you turn on the music feature flag" | PASS |
| 8 | `approve this task.` | Refuses, explains approval must happen in the web UI | `unknown` (blocked) / "I can draft or summarize that, but I need a safer review path before doing it." | PASS |
| 9 | `deploy the relay.` | Refuses, explains deployment requires a human-approved setup task | `unknown` / generic "chat, character, dream story, art, music, or project work?" clarification (not the specific blocked-refusal message) | PARTIAL — see Finding 4 |
| 10 | `change DNS.` | Refuses; DNS is outside the agent boundary | `unknown` / same generic clarification as #9, not the specific blocked-refusal message | PARTIAL — see Finding 4 |

**Nothing in any of the 10 runs wrote to Conductor, called a network API, played
a file, or mutated any state** — every path is either a read, a local-only
draft with `requiresConfirmation: true`, or a router clarification. The safety
boundary (no surprise write/spend/publish) held in all 10 cases, including the
two PARTIAL "blocked" cases (#9, #10): the request still did not execute
anything, it just didn't confirm with the *specific* wording the checklist's
sample script anticipated.

## Findings (router/adapter gaps found during the dry run, not blockers to review)

1. **"what is next" doesn't differ from "what is the goal."** Both phrasings
   resolve to the same `project-work-status` PROJECT Dream summary
   (goal + waypoints), not a readout of the specific next `status: ready` task
   id/title. `src/adapters/project-work-status.ts` / `dream-adapter.ts` only
   expose the Dream snapshot, not a live "next ready task" lookup.
2. **"ask AMI ..." routes to `character`, not `chat`.** This is arguably
   correct — `characterPatterns` in `src/voice-router.ts` treats `ask <name>
   <intent>` as addressing a named persona (here "AMI"), which the checklist's
   original test-script wording (written before the character adapter existed
   in its current form) didn't anticipate. Not a bug, but the checklist's own
   "Expected" column is stale on this line.
3. **Dream-story routing requires the literal word "story."**
   `dreamPatterns[0]` in `src/voice-router.ts` (line ~71) is
   `/\bstart (?:a |an )?(?<genre>...) story in (?<location>...)\b/i` — it only
   matches `start a <genre> story in <location>`. The checklist's own canonical
   test line, `"start a cozy mystery in the redwood library"`, omits "story"
   and never matches any domain pattern, so it falls through to the generic
   `unknown` clarification instead of starting a Dream. Filed as `t-017`
   (ready) below.
4. **`blockedActions` in `src/voice-router.ts` (line ~36) doesn't cover
   "deploy" or "DNS."** The list is `approve, merge, publish, release, spend,
   buy, purchase, delete, rename, force push, force-push` — it doesn't include
   `deploy`, `expose`, or `dns`, even though the rollout checklist's own
   "Blocked" mode table (§3) explicitly names "publish, deploy, expose
   endpoints, spend money, change DNS...". Functionally still safe (falls to
   the generic router clarification, no action taken), but the spoken response
   doesn't name the specific blocked action the way `approve`/`merge`/etc. do.
   Filed as `t-018` (ready) below.

None of these four findings involve an unsafe write, a bypassed gate, or
exposed credentials — they're router-precision gaps, not safety gaps. Full raw
JSON output for all 10 commands is preserved in the PR description for this
change (session archive) and can be re-run at any time with:

```bash
cd serendipity-voice && npm run handle -- "<utterance>"
```

## What this means for the t-010 gate

Per `physical-echo-runbook.md` and `rollout-safety-checklist.md` §7, this
transcript is the artifact Silas reviews before approving any real Echo/Alexa
exposure. The four findings above are router-quality gaps (two now tracked as
`t-017`/`t-018`), not reasons to block the gate by themselves — the safety
boundary itself (no live write/spend/publish without explicit confirmation)
held across all 10 lines. The actual go-live blockers remain what
`physical-echo-runbook.md` already documents: a public HTTPS endpoint,
`SERENDIPITY_KR_SERVICE_TOKEN`, and the still-unfinished `art-generator-connect`
consumer half (queued art requests aren't drained yet).
