# Alexa Integration Rollout and Safety Checklist

This checklist keeps the Alexa voice-command integration in draft/prototype mode until Silas explicitly approves real use. It assumes the relay design in `projects/alexa-integration/docs/relay-design.md` and the command list in `projects/alexa-integration/docs/alexa-voice-commands.md` remain the source references.

## 1. Pre-flight boundaries

Before any prototype is used with real commands:

- Confirm the skill is not published to the Alexa store.
- Confirm no public relay endpoint is exposed without a human-approved deployment task.
- Confirm all secrets stay in environment variables or approved secret storage, never in source.
- Confirm the first prototype runs in read-only mode by default.
- Confirm write-like commands create drafts or Todos only when the user explicitly confirms.
- Confirm DNS, billing, production deploys, and live account configuration remain out of scope.

## 2. Local prototype checks

Run these checks before connecting Alexa traffic:

- Start the relay locally with dummy data or a non-production test token.
- Verify `KR_API_TOKEN` is missing-safe: startup should fail closed or run in read-only mock mode.
- Verify every supported intent returns a short voice-safe response.
- Verify unknown intents return a harmless fallback and do not call downstream APIs.
- Verify malformed slots produce a clarification response instead of guessing.
- Verify logs record intent name, mode, result, and timestamp without storing token values.

## 3. Command-mode policy

Each command must be classified before implementation:

| Mode | Allowed behavior | Human gate |
| --- | --- | --- |
| Read | Summarize projects, tasks, Todos, pending approvals, or recent activity | No extra gate if using existing authenticated read APIs |
| Draft | Prepare a Todo, art request, approval note, or project update for review | Must ask for confirmation before creating anything |
| Blocked | Publish, deploy, expose endpoints, spend money, change DNS, change secrets, or alter production data | Requires a separate human-approved roadmap task |

When in doubt, downgrade the command to read-only or blocked. Tiny safety goblin says: no voice command should be able to surprise-spend money.

## 4. Test script

Use this manual script for the first prototype pass:

1. "Alexa, ask Conductor what needs my approval."
   - Expected: read-only summary of `needs-human` items.
2. "Alexa, ask Conductor what the top project is."
   - Expected: reads priority/order status without changing roadmaps.
3. "Alexa, ask Conductor to add a todo for the Worker."
   - Expected: asks for title/priority, repeats back, and requires confirmation before creating a Todo.
4. "Alexa, ask Conductor to request art for a project."
   - Expected: creates only a draft/request handoff; no direct generation unless separately approved.
5. "Alexa, ask Conductor to deploy the relay."
   - Expected: refuses and explains deployment requires human-approved setup.
6. "Alexa, ask Conductor to change DNS."
   - Expected: refuses; DNS is outside the agent boundary.

Record pass/fail notes for each line before moving beyond local testing.

## 5. Disable switch

A prototype is not ready unless it has a fast shutoff path:

- Environment flag: `ALEXA_RELAY_ENABLED=false` disables all non-health routes.
- Optional allowlist: only Silas's Amazon account or development user may call the skill.
- Token revocation plan: know where `KR_API_TOKEN` is stored and how to rotate it.
- Rollback plan: remove the relay route or stop the local/container service.
- Log review: confirm the last successful and rejected commands before disabling.

## 6. Logging and review

Logs should support review without leaking sensitive material:

- Include request id, timestamp, intent, mode, result, and high-level target slug/id.
- Do not log bearer tokens, raw credentials, personal notes, full private file contents, or secret environment values.
- Keep failed authorization attempts visible enough to investigate.
- Keep successful draft/write handoffs easy to trace back to the spoken command.
- Add a short review note to the roadmap or PR when a prototype test reveals a missing guardrail.

## 7. Human approval checkpoint

Before real-world use, Silas should review:

- The final command list.
- The relay design.
- This checklist.
- The exact deploy/exposure plan.
- The authentication and disable-switch setup.
- A dry-run transcript from the manual test script.

Only after that review should a new implementation task expose a live endpoint or connect the Alexa developer skill to anything beyond a local/mock relay.
