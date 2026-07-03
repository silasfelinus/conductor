# AppMaker GitHub Integration — Design (GitHub App)

Task: appmaker/t-003 · Date: 2026-07-03 · Status: design for Silas review
Decision basis: Silas chose GitHub App over fine-grained PATs (2026-07-02).
Design only — nothing here registers an app, stores a credential, or touches
a live repo. Implementation tasks are proposed at the end, each with its gate.

---

## 1. Why a GitHub App (recap)

| Property | GitHub App | Fine-grained PAT |
|---|---|---|
| Scope | Per-installation, per-repo selection by the user | Per-token, user must configure correctly |
| Revocation | User uninstalls from GitHub settings; instant | User must find and delete the token |
| Expiry | Installation tokens auto-expire in 1 h; app key rotates rarely | Long-lived secrets in our DB |
| Attribution | Actions show as "AppMaker[bot]" | Actions impersonate the user |
| Rate limits | Per-installation (scales with users) | Per-user account |

The app authenticates as itself (private key → app JWT), then mints
short-lived **installation tokens** scoped to exactly the repos the user
granted. Our DB never stores anything that grants standing access on its own.

## 2. The app manifest

One GitHub App, owned by Silas's account (or a future org):

- **Name:** `kind-robots-appmaker`
- **Permissions (least privilege):**
  - `contents: read/write` — clone, branch, commit scaffolds and agent work
  - `pull_requests: read/write` — open/merge PRs (the only path to main)
  - `metadata: read` — mandatory baseline
  - `checks: read` + `actions: read` — surface CI state in AppMaker UI
  - *Explicitly absent:* administration, webhooks-manage, secrets, deployments,
    members. AppMaker never creates repos on the user's behalf in v1 — the
    user creates the repo (or picks an existing one) and installs the app on it.
- **Webhook events:** `push`, `pull_request`, `check_suite`, `installation`
  (created/deleted/repos added/removed). Endpoint:
  `POST /api/appmaker/github/webhook` (HMAC-verified with the webhook secret).
- **Setup URL:** kind_robots AppMaker page, so installs round-trip back to us.

## 3. Credential storage (kind_robots server)

Three secrets exist, all server-side environment/runtime config, never in DB,
never in any client:

| Secret | Where | Used for |
|---|---|---|
| App private key (PEM) | env `APPMAKER_GH_APP_KEY` | Signing 10-min app JWTs |
| Webhook secret | env `APPMAKER_GH_WEBHOOK_SECRET` | Verifying webhook HMAC |
| App ID / client ID | env (non-secret) | JWT issuer, install URLs |

Installation tokens (1 h) are minted on demand and held in an in-memory
LRU cache keyed by installation id; on serverless (Vercel) that degrades to
per-invocation minting, which is acceptable (one extra API call).

**What IS in the DB:** installation ids and repo mappings — useless without
the app private key, safe at rest.

## 4. Data model (Prisma, kind_robots)

```prisma
model GithubInstallation {
  id             Int      @id @default(autoincrement())
  installationId BigInt   @unique          // from GitHub
  userId         Int                       // kind_robots user who connected it
  accountLogin   String                    // github user/org the app is installed on
  createdAt      DateTime @default(now())
  suspendedAt    DateTime?
  User           User     @relation(fields: [userId], references: [id])
  AppRepos       AppRepo[]
}

model AppRepo {
  id              Int      @id @default(autoincrement())
  slug            String                    // the one-slug rule key
  owner           String                    // e.g. "silasfelinus"
  repo            String                    // e.g. "conductor" or "recipe-box"
  subPath         String   @default("")     // "apps/recipe-box" for monorepo apps, "" for whole-repo
  installationId  Int?                      // null = our monorepo via conductor's own token
  dreamId         Int?                      // link to the PROJECT Dream
  userId          Int
  createdAt       DateTime @default(now())
  Installation    GithubInstallation? @relation(fields: [installationId], references: [id])

  @@unique([slug, userId])
}
```

`AppRepo` is the **slug → repo mapping**: every app knows where its code
lives. Monorepo apps (`installationId: null, subPath: "apps/<slug>"`) and
graduated/external apps (installation-backed, `subPath: ""`) are the same
row shape, so the UI and agents treat them uniformly.

## 5. Flows

### 5a. Connect (user installs the app)
1. AppMaker page → "Connect GitHub" → `https://github.com/apps/<app>/installations/new`
   with `state=<signed nonce bound to userId>`.
2. User picks account + repos on GitHub's own UI (this is where permission
   granting lives — GitHub's screen, not ours).
3. GitHub redirects to our setup URL with `installation_id` + `state`;
   server verifies the state signature, fetches installation details with an
   app JWT, and upserts `GithubInstallation`.
4. UI now lists the granted repos for app creation/graduation.

### 5b. Create an external app
1. User (self-serve, per Silas's decision) names the app; picks a granted
   repo (created by them on GitHub beforehand — v1 does not create repos).
2. Server writes `AppRepo` + creates the Dream (slug parity) + files the
   scaffold AGENT todo.
3. Worker cycle: mints an installation token, pushes the `new_app.py`-style
   scaffold as branch `worker/scaffold-<slug>`, opens a PR in *their* repo.
4. User merges (they own the repo; our Reviewer only auto-merges in repos
   that opt into agent-managed mode — see 5d).

### 5c. Graduation (monorepo → own repo)
1. Silas (or the owning user) picks "graduate" on an app.
2. Agent runs `git subtree split --prefix=apps/<slug>` to preserve history,
   pushes to the target repo via installation token, flips the `AppRepo` row
   (sets installationId + clears subPath), and opens a removal PR in the
   monorepo. Both PRs are `needs-human` — graduation is irreversible-ish.

### 5d. Agent roles on external repos
The conductor permission model maps onto any repo:
- **Worker:** may push only `worker/*` branches, may open PRs to the default
  branch, never merges. Enforced by us (the token could do more; the agent
  contract and server-side branch checks keep it honest) — plus optionally
  by the repo owner with branch protection.
- **Reviewer:** merges only in repos where the owner enabled
  `agentManaged: true` (future AppRepo field, default false). Otherwise
  review = comment only; the human merges.
- **Store submission / release:** always `needs-human`, every repo, no flag.

### 5e. Webhooks → app status
`push`/`pull_request`/`check_suite` events update a lightweight status cache
(latest CI state per AppRepo) that the AppMaker page and Flutter app read.
No polling GitHub from clients; clients poll our API as they already do.

## 6. Security invariants (the checklist reviews enforce)

1. No GitHub credential of any kind in any client binary or client storage.
2. DB stores installation ids and mappings only — nothing that grants access
   without the server-held private key.
3. Installation tokens: minted per use, never logged, never returned by any
   API, cache lifetime ≤ 1 h.
4. Webhook handler verifies HMAC before parsing; unverified payloads are
   dropped and counted, not processed.
5. `state` nonce on the install round-trip is signed and single-use
   (prevents installation hijacking onto the wrong kind_robots account).
6. Every write path through an installation token is attributable: branch
   names carry the agent role, commits carry the bot identity.
7. New permission scopes on the app manifest = `needs-human` + TALKBACK note.

## 7. What stays out of v1

- Creating repos for users (they bring a repo; cuts the `administration` scope)
- Org-level features (teams, required reviewers)
- Multiple installations per user (first one wins; add later if needed)
- Marketplace listing / public app directory presence

## 8. Proposed implementation tasks

| id | title | gate |
|---|---|---|
| t-007 | Register the GitHub App (manifest above) and store secrets in Vercel env | **needs-human** (Silas creates it; agents never hold the key outside runtime) |
| t-008 | kind_robots: GithubInstallation/AppRepo models + connect flow + webhook endpoint | normal software cycle, after t-007 |
| t-009 | Worker external-repo support: mint installation token, scaffold PR flow (5b) | after t-008 |
| t-010 | Graduation flow (5c) with its needs-human gates | after t-009 |

TO APPROVE THIS DESIGN: read sections 2 (permissions), 4 (data model), and 6
(invariants) — those are the load-bearing choices. Then set t-003
`approved_by_human: true, status: done`; t-007 becomes actionable (it's yours
anyway — app registration happens under your GitHub account).
