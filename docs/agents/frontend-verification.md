# Verifying front-end changes (kind_robots)

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

**Visually verifying a front-end change: kind_robots production is self-hosted at
`kindrobots.org`, not Vercel.** As of 2026-08-12 kind_robots migrated off Vercel
entirely — Vercel Git deployments are disabled repo-wide (there is no `vercel.json` in
the repo anymore) and production is served from a self-hosted container on Unraid at
`https://kindrobots.org` (kind-robots/t-064, closed 2026-08-12; see the
`kindrobots-unraid` project). **A `*.vercel.app` URL returning `402 Payment Required` /
`DEPLOYMENT_PAUSED` / `DEPLOYMENT_DISABLED`, or `mcp__Vercel__get_project` showing
`live: false`, is the expected state of retired infrastructure — it is NOT a production
incident and does not need a new gate or notification.** (Re-confirmed 2026-08-15: every
`*.vercel.app` URL for the project 402s/503s while `kindrobots.org` itself serves fine —
200, real SSR markup, real image assets.)

This changes what verification is actually possible and when:

- **No PR preview exists anymore.** Vercel previews are gone for every branch prefix,
  not just the `agent/*`/`worker/*`/`conductor/*` ones that were already disabled for
  cost before the migration. A session cannot visually verify an *unmerged* branch's UI
  — verification pre-merge is limited to `vue-tsc`/`eslint`/unit tests/
  `test:layout-contract`.
- **No auto-deploy-on-merge either.** The Unraid container only picks up a merged commit
  when Silas runs a manual "Force Update" in the Unraid UI (see the `kindrobots-unraid`
  roadmap and `docs/runbooks/migration-credential-boundary.md`). A merged, CI-green PR
  can sit un-deployed for a while — check `https://kindrobots.org/api/health/database`,
  and whether the specific code path you changed actually answers as expected, before
  concluding a change "isn't showing up" means it's wrong (davinci/t-018 hit exactly
  this deploy-timing gap on 2026-08-08: a new endpoint returned the SPA shell, not JSON,
  until the next Force Update).
- **Post-deploy, direct HTTPS is the verification path.** Plain `curl` or `WebFetch`
  against `https://kindrobots.org/<route>` (or an asset path such as
  `/images/dashboard-tabs/art/<slug>.webp`) works directly in this sandbox — no MCP
  connector is required for this host, egress to it is unrestricted like any ordinary
  HTTPS host. This returns real SSR markup with the same caveats as before: it proves a
  route loads, isn't a 500, and contains the markup you expect from SSR; it does NOT
  prove anything that only appears after hydration, nor layout, spacing, or anything
  pixel-level. Say which of those you actually checked.
- **Real cross-width geometry**: `responsive-layout-audit.yml`'s `audit` check now runs
  on a schedule and via manual `workflow_dispatch` against production
  (`https://kindrobots.org` by default, overridable via its `base_url` input) — Vercel
  preview support was removed from the workflow along with the rest of the Vercel infra,
  so it no longer fires per-PR against a branch preview. It measures rendered geometry at
  phone/tablet/desktop widths, fails on elements that spill past the viewport or get
  crushed to a sliver, and uploads screenshots as artifacts every run. Trigger it
  manually after a merge + confirmed Force Update if you need fresh geometry/screenshots
  for a specific change; it will not run automatically per-PR the way the retired
  Vercel-preview flow did.
- **Chromium-through-the-sandbox-proxy still fails on every HTTPS host, not just
  Vercel's** (interface-vision/t-091, measured 2026-08-04): a headless-Chromium fallback
  in this sandbox gets `net::ERR_CONNECTION_RESET`/`ERR_TUNNEL_CONNECTION_FAILED`
  regardless of target host (confirmed byte-identical against `example.com`),
  independent of proxy flags (`proxy:`, `--proxy-server`, `--disable-http2`,
  `--disable-quic`, `--ignore-certificate-errors`, `ignoreHTTPSErrors` all changed
  nothing). This is a Chromium-through-the-proxy limitation, not anything about the
  target being Vercel or kindrobots.org — don't reach for a local headless-browser
  fallback in a non-interactive session; use `curl`/`WebFetch` for markup and let CI's
  `audit` check carry real pixels.
  **UPDATE (rainbow-butterflies/t-053 cycle, measured 2026-09-16): this failure does
  NOT reproduce in a Claude Code web/cloud remote-execution environment** (the kind
  with a pre-installed `/opt/pw-browsers/chromium` and `PLAYWRIGHT_BROWSERS_PATH` set
  for it, distinct from whatever sandbox interface-vision/t-091 ran in). There, the
  earlier failure mode was a cert error (`net::ERR_CERT_AUTHORITY_INVALID`), not a
  connection reset — a different symptom than what t-091 saw, and one `ignoreHTTPSErrors`
  alone did not fix (it changed the error to a timeout instead). The combination that
  worked, verified against `https://example.com`, `https://kindrobots.org`, and
  `https://kindrobots.org/model-builder` (200, real hydrated title, zero horizontal
  overflow at a 390px viewport): launch with explicit
  `proxy: { server: 'http://127.0.0.1:38425' }` (read the actual port from `$HTTPS_PROXY`
  rather than hardcoding it) plus `args: ['--ignore-certificate-errors', '--disable-http2']`,
  and a browser context with `ignoreHTTPSErrors: true`. Use Node's global Playwright at
  `/opt/node22/lib/node_modules/playwright` via `require()`/CJS (a bare `import
  'playwright'` fails with `ERR_MODULE_NOT_FOUND` unless the project's own
  `node_modules` has it). Do not assume this generalizes to every session type — verify
  with the `example.com` + target-host pair above before relying on it for a specific
  task, since t-091's environment and this one clearly differ in ways not fully
  understood. If it works, this reopens live UI-driven verification (clicking through
  an authenticated flow, screenshotting hydrated state, running a task like
  model-builder/t-031's live smoke test) for sessions that previously treated it as
  categorically impossible.

  **UPDATE (model-builder/t-031 cycle, 2026-09-17): the authenticated-flow gap above is
  closed** — a working test-login path already exists, it just hadn't been wired to
  browser-based verification before. kind_robots' own CI (`cleanup-test-users.yml`,
  Cypress's `createFreshLoggedInTestUser`) already registers and logs in disposable
  `cypress-*` users against production `kindrobots.org` as its normal test methodology.
  The same pattern works from a plain script, no Cypress required: `POST
  /api/users/register` with `x-api-key: $KR_API_TOKEN` (this is the beta-admin token,
  read via `x-api-key`/`x-admin-token`/`Authorization`, per
  `server/utils/validateKey.ts`) creates a `cypress-`-prefixed user; `POST
  /api/auth/login` with that user's username/password returns a real session JWT;
  `page.evaluate(() => localStorage.setItem('token', <jwt>))` before navigating logs the
  Playwright browser context in exactly the way the SPA's own `userStore.ts` expects
  (`getFromLocalStorage('token')`, validated via `/api/auth/validate/token`) — confirmed
  live, including a full `/model-builder` source-pick → recipe → run flow rendering
  correctly with a real username in the header. `KR_API_TOKEN` itself is NOT a valid
  session token and must not be dropped into `localStorage` directly — it authenticates
  server-to-server admin calls (`x-api-key` etc.), not a browser session; the app's own
  client-side validation silently strips it back out if you try. Clean up afterward via
  `POST /api/users/cypress-cleanup` with `{"username": "cypress-..."}` and the same
  admin header — restricted server-side to `cypress-*` usernames, so it can't be used to
  delete real accounts. This whole round trip is the established, sanctioned pattern
  already running in kind_robots CI, not a new bypass. One live gap remains, not an
  auth one: a fresh test user owns nothing, so exercising a source-owned flow (model
  builder, or anything gated by `assertSourceOwnership`-style checks) needs a same-session
  API call to create an owned record first (e.g. `POST /api/characters` with
  `Authorization: Bearer <jwt>`) — the UI's source picker itself does not filter to
  owned-only records and will happily let you pick something you can't actually build on,
  which surfaces as a 403 from the write endpoint rather than a clear UI-level warning
  (worth a small UX task on its own).

So a UI change on a `claude/*` branch is NOT merging on structural CI alone. The honest
summary of what a non-interactive session can claim: SSR markup via `curl`/`WebFetch`
against `kindrobots.org` post-deploy (itself), real cross-width geometry plus
screenshots via the `audit` check (CI, scheduled/manual against production), structural
invariants via the layout contract (CI), and nothing about aesthetics pre-deploy or
pre-Force-Update. The old Vercel MCP connector flow
(`list_teams`/`list_projects`/`list_deployments`/`web_fetch_vercel_url` against the
kind-robots Vercel project) is retired for kind_robots verification purposes — its data
now describes decommissioned infrastructure, not anything a merge or preview affects.

