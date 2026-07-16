# Dream-Cycle API Surface Audit

**Task:** dream-cycle/t-003 · **Kind:** software (read-only doc) · **Date:** 2026-07-16

Per-model verdict for every kind_robots model a dream build touches: is there a
create/update endpoint the headless loop can call, what auth it needs, and the
required fields. **This is a read-only audit** — verified by inspecting the
kind_robots repository source (`server/api/**`, `prisma/schema.prisma`), **not**
by hitting the live DB (it is down, and the loop never edits the backend
directly). The kind_robots backend stays read-only/external to conductor: each
gap becomes a proposed kind_robots roadmap task or pitch, never a direct edit.

## Auth model

All write endpoints authenticate via `validateApiKey` / `requireApiUser`
(`server/utils/validateKey.ts`, `server/utils/authGuard.ts`). Present the token as:

```
Authorization: Bearer <KR_API_TOKEN>
```

`KR_API_TOKEN` is the **beta-admin token**. `validateBetaAdminString` resolves it
to the configured beta-admin user and returns `kind: 'beta-admin-token'` **only if
that user is an admin** (`userIsAdmin(user)`), so it satisfies the stricter
`isAdmin` gate that a few endpoints add (expressions/transitions require
`isAdmin || kind === 'server'`). Rows created by the loop carry
`designer: "dream-cycle"` for traceability/removability (the reversibility
contract). Alternate accepted headers: `x-beta-admin-token`, `x-admin-token`.

## Verdict summary

| Model | Create/update endpoint | Verb | Auth | Verdict |
|---|---|---|---|---|
| Dream | `/api/dreams`, `/api/dreams/{id}` | POST / PATCH | Bearer | **api-ready** |
| DreamRelation | `/api/dream-relations`, `/api/dream-relations/{id}` | POST (upsert) / DELETE | Bearer (`requireApiUser`) | **api-ready** ✅ (t-017 gap now closed) |
| Character | `/api/characters` | POST | Bearer | **api-ready** |
| Reward | `/api/rewards` | POST | Bearer | **api-ready** |
| Bot | `/api/bots` | POST | Bearer | **api-ready** |
| Scenario | `/api/scenarios` | POST | Bearer | **api-ready** |
| PitchSheet | `/api/sheets/by-dream/{dreamId}`, `/api/sheets/{id}` | POST / PATCH | Bearer (`requireApiUser`) | **api-ready** (use `by-dream`; see t-016) |
| ExpressionMedia | `/api/bots/expressions` | POST (batch upsert) | Bearer, admin/server | **api-ready** |
| ExpressionTransition | `/api/bots/transitions` | POST (batch upsert) | Bearer, admin/server | **api-ready** (needs a transition video) |
| NarratorTopic | `/api/bots/topics` | POST (batch upsert) | Bearer | **api-ready** |
| NarratorThread | `/api/bots/threads` | POST (batch upsert) | Bearer | **api-ready** |

**Bottom line: every dream-build model is api-ready.** No blocking gaps remain
for the dream playbook (specs/dream.md, t-004). The two historical gaps
(t-016, t-017) are resolved or have a documented workaround; details below.

---

## Newly audited this task (the narrator/expression stage models)

These four back the dream playbook's **stage 6 (Narrator)**: a Bot's expression
set plus its topics/threads. The head-start in `scripts/build_dream_records.py`
already verified Dream/Character/Reward/Bot/Scenario/PitchSheet; this task adds
the remaining four and consolidates.

### ExpressionMedia — `POST /api/bots/expressions`
- **Source:** `server/api/bots/expressions.post.ts`; schema `prisma/schema.prisma:640`.
- **Auth:** `validateApiKey`, then `isAdmin || kind === 'server'` (KR_API_TOKEN
  qualifies — beta-admin user is admin). 401 invalid token, 403 non-admin.
- **Body:** an array of rows, or `{ expressions: [...], dryRun?: true }`.
- **Per-row required:** exactly one of `botId` / `characterId`; `expressionKey`
  (lowercase enum or custom slug); `expression` (enum: NEUTRAL, JOYFUL,
  SORROWFUL, AFRAID, DISGUSTED, ENRAGED, SURPRISED, ANXIOUS, PROUD, LOVING,
  LAUGHING, CRYING, SLEEPING, THINKING, SHRUGGING, WINKING, FACEPALMING,
  CHEERING, WHISPERING, SHOUTING, CUSTOM); `kind` (EMOTION | ACTION).
- **Optional:** label, emoticon, imagePath, videoPath, message, designer,
  artPrompt, isActive, additionalPhrases (stringified if not a string), artImageId.
- **Idempotency:** upsert on the unique `(owner, expressionKey)`; batched (chunks
  of 25). `dryRun: true` validates without writing.
- **Playbook fit:** the stage-6 expression set (NEUTRAL + ≥5 emotions + ≥2
  actions) is one batch call. imagePath/videoPath fill in later via the art
  pipeline; rows can be created art-less first and PATCHed/re-upserted.

### ExpressionTransition — `POST /api/bots/transitions`
- **Source:** `server/api/bots/transitions.post.ts`; schema `prisma/schema.prisma:682`.
- **Auth:** same as expressions (`isAdmin || server`).
- **Per-row required:** exactly one of `botId` / `characterId`; `fromKey` +
  `toKey` (must differ, no self-transition); **`videoPath` (required on create)** —
  the FLF2V-generated animated webp for the transition.
- **Idempotency:** upsert on `(owner, fromKey, toKey)`; chunked; resumable
  (re-send same payload). `dryRun` supported.
- **Playbook fit:** **optional / deferred.** A transition needs a rendered
  transition clip, so it can't be created in the same headless pass that seeds
  expressions. Treat it as a post-art enrichment step, not a core dream stage.

### NarratorTopic — `POST /api/bots/topics`
- **Source:** `server/api/bots/topics.post.ts`; schema `prisma/schema.prisma:779`.
- **Auth:** `validateApiKey` (any valid key; no extra admin gate in-handler).
- **Body:** batch of topic rows.
- **Per-row required:** `slug`, `title`, `prompt`. Optional: subtitle,
  description, icon, sampleUserPrompt, sortOrder, isPublic, isActive.
- **Idempotency:** upsert on unique `slug`.
- **Playbook fit:** the brief says "reuse fitting NarratorTopics; create new
  topics only when none fit." Since `slug` is the upsert key, the loop should
  first GET existing topics (see below) and only POST a topic whose slug is new.

### NarratorThread — `POST /api/bots/threads`
- **Source:** `server/api/bots/threads.post.ts`; schema `prisma/schema.prisma:799`.
- **Auth:** `validateApiKey`.
- **Per-row required:** a resolvable bot (`botId` **or** `botName`) + a resolvable
  topic (`topicId` **or** `topicSlug`); `openingText`. Optional: title, guidance,
  starterPrompts, sortOrder, isActive.
- **Idempotency:** upsert on unique `(botId, topicId)`; chunked; resumable.
- **Playbook fit:** wires the dream's narrator Bot to its topics. `botName` /
  `topicSlug` resolution means the loop can reference by human-readable keys it
  already holds, without a prior id lookup.

**Read side (verification):** narrator content is fetched via
`GET /api/narrators/{type}/{slug}` (`server/api/narrators/[type]/[slug].get.ts`) —
use it to confirm topics/threads landed and to check for an existing topic slug
before creating a new one.

---

## Previously verified (from t-012 / build_dream_records.py)

Documented in `scripts/build_dream_records.py`; summarized here for one complete
reference. These are the core dream-object stages (2–5).

- **Dream** — `POST /api/dreams` (+ PATCH `/api/dreams/{id}`). The universal
  "card hub"; the loop creates PITCH / GENRE / LOCATION / CHARACTER / NARRATOR /
  REWARD dream cards. `designer: "dream-cycle"`.
- **DreamRelation** — `POST /api/dream-relations`
  (`server/api/dream-relations/index.post.ts`, auth `requireApiUser`). Body:
  `{ fromDreamId, toDreamId, relationType, note? }` — all of fromDreamId/
  toDreamId/relationType **required**; `relationType` must be one of
  `dreamRelationTypes` (e.g. RELATED, CONTAINS). Upsert on
  `(fromDreamId, toDreamId, relationType)`; `DELETE /api/dream-relations/{id}`;
  `GET /api/dream-relations`. **This closes the historical t-017 gap** — when
  build_dream_records.py was written the endpoint didn't exist and world-graph
  edges were skipped; they can now be created.
- **Character** — `POST /api/characters`; real Character rows linked to their
  CHARACTER Dreams via `dreamIds`.
- **Reward** — `POST /api/rewards`; two rows per dream, one `rewardType: SKILL`
  and one `ITEM`.
- **Bot** — `POST /api/bots`; the narrator Bot row for the NARRATOR Dream.
- **Scenario** — `POST /api/scenarios`; 1–2 rows linking world + locations + cast.
- **PitchSheet** — canonical create is **`POST /api/sheets/by-dream/{dreamId}`**
  (`server/api/sheets/by-dream/[dreamId].post.ts`), which derives defaults from
  the Dream; `PATCH /api/sheets/{id}` to attach `imagePath` when art lands. Each
  sheet carries `extraData: {dreamCycle, proposalDate, elementType, element}`.

---

## Gaps & follow-ups

| Ref | Was | Status now | Action |
|---|---|---|---|
| kind-robots **t-016** | `POST /api/sheets` reported as a broken/mis-copied handler | The index handler exists (`server/api/sheets/index.post.ts`, `requireApiUser` → `buildPitchSheetFromDream`), but the daily builder **deliberately uses `by-dream/{id}`** as the correct create path. | No blocker for the loop — keep using `by-dream/{id}`. Leave t-016 for kind_robots to reconcile whether the bare `POST /api/sheets` path should be removed or documented. |
| kind-robots **t-017** | "no DreamRelation endpoint" | **Resolved** — `POST /api/dream-relations` exists and upserts. | Recommend closing t-017 in the kind-robots roadmap; the dream playbook can create world-graph edges. |

No **new** gaps discovered: all ten dream-build models have a working
create/update path reachable with `KR_API_TOKEN`. specs/dream.md (t-004) can
reference this document for the exact endpoints, auth, and required fields per
stage.

## Source references (kind_robots repo, audited 2026-07-16)

- `server/api/bots/expressions.post.ts`, `transitions.post.ts`, `topics.post.ts`,
  `threads.post.ts`
- `server/api/dream-relations/index.post.ts`, `server/api/sheets/index.post.ts`,
  `server/api/sheets/by-dream/[dreamId].post.ts`
- `server/api/narrators/[type]/[slug].get.ts`
- `server/utils/validateKey.ts`, `server/utils/authGuard.ts`
- `prisma/schema.prisma` (Bot:113, Character:167, Dream:376, DreamRelation:433,
  ExpressionMedia:640, ExpressionTransition:682, NarratorTopic:779,
  NarratorThread:799, Reward:1018, Scenario:1053)
- conductor: `scripts/build_dream_records.py` (prior-verified contracts)
