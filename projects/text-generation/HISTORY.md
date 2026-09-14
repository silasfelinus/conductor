# text-generation — task history archive

Full `note:` prose for completed text-generation tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Map the existing text stack and write the private-server design brief

<!-- note:begin t-001 -->
Start from the code that already exists, not a greenfield provider rewrite. Inventory server/api/chats/openai/stream.post.ts, server/api/chats/anthropic/stream.post.ts, server/api/chats/ollama/stream.post.ts, server/utils/serverResolver.ts, the Prisma Server model, preferredTextServerId, server CRUD/health APIs, and the current chat/text consumers. The current runtime already accepts stored server profiles in the OpenAI and Anthropic routes and has a native Ollama stream route, but the capability routing and product surface are incomplete. Produce projects/text-generation/BRIEF.md defining: one-shot generation vs chat vs streaming contracts; provider/profile capabilities; model selection; server ownership/visibility; error and cancellation semantics; mana accounting; a compatibility/migration plan for the three existing endpoints; and what is explicitly out of scope. Treat briefs as direction, not permanent contracts.

Closed 2026-08-17: projects/text-generation/BRIEF.md merged via PR #2351, covering all six required sections (capability map, target contract, migration strategy, security boundaries, success criteria, implementation sequence) plus the required Ollama/stored-server current-vs-missing explanation. t-002/t-003 are now unblocked by resolve_deps.py.
<!-- note:end t-001 -->

## t-002 — Build a shared server-side text generation provider layer

<!-- note:begin t-002 -->
Closed 2026-08-17: shared server-side text provider service merged via kind_robots PR #1919 (squash 21bcde9). server/utils/textProviderService.ts extracts the mechanics duplicated across all three chat streaming routes (optional server resolution, provider-key precedence, per-authType auth headers, SSE/ndjson header setup, byte-relay-then-mana pump, error status extraction, refId shaping); all three routes now call the single shared estimateTextCostUsd instead of three drifted local estimators. Net -367 lines. t-003 (Ollama capability-routing fix + private-server profile UX) is the next task per BRIEF.md sequence; t-004 stays waiting on both t-002 and t-003.
<!-- note:end t-002 -->

## t-003 — Add first-class trusted private text-server profiles

<!-- note:begin t-003 -->
Reuse the existing Server model and admin server surfaces where they fit. Make text-capable private/self-hosted servers explicit and selectable, including native Ollama and OpenAI-compatible endpoints. Fix capability resolution so supported server types are actually discoverable for text generation. Include an authenticated health/test operation and user preferredTextServerId selection. Private-network access is allowed only through stored trusted profiles created by an authorized user/admin, never through arbitrary client-supplied URLs.
<!-- note:end t-003 -->

## t-005 — Harden private-server networking, secrets, and failure behavior

<!-- note:begin t-005 -->
Treat private LLM connectivity as a deliberate SSRF boundary. Trusted stored profiles may target approved LAN/private addresses, but untrusted request data may not choose destinations. Block cloud metadata/link-local destinations and unsafe redirects, constrain protocols, set connection/read timeouts and response limits, cancel upstream streams when clients disconnect, avoid secret-bearing logs, and verify ownership/visibility before every server selection. Preserve the ability to use a home/private server without weakening the rest of the app into an open proxy. This task changes a security boundary and therefore stays human-gated before merge even though the code itself is reversible.

FOR SILAS: kind_robots PR #1926 (open, not merged) implements this. Two new files -- server/utils/networkSafety.ts (destination validation: blocks cloud metadata IPs/hostnames and link-local ranges; blocks loopback UNLESS the caller explicitly opts in) and server/utils/safeFetch.ts (validates before dialing and on every redirect hop, one connect-timeout budget, correct 301/302/303 method-downgrade). Wired into generate/text.post.ts and the three legacy chat routes in place of plain fetch(). sendMeteredStream (textProviderService.ts) now caps response size, enforces a per-chunk idle timeout, and aborts the upstream request when the client disconnects.

Deliberately does NOT block RFC1918 (10/8, 172.16/12, 192.168/16) or the 100.64.0.0/10 Tailscale CGNAT range -- home-LAN and Tailscale servers are this project's actual intended use case (ServerAccessMode.TAILSCALE already exists in the schema), so blocking them would break the feature. Loopback (127.0.0.1, ::1, "localhost") IS blocked by default, since any authenticated user (not just admins) can set a Server.baseUrl -- except for ollama/stream.post.ts's config.ollamaBaseUrl fallback (nuxt.config.ts default: http://localhost:11434, an operator env var, not user input), which explicitly opts back in via a new allowLoopback flag threaded only to that one call site.

TO APPROVE: read the PR diff (10 files, ~1080 lines, mostly the two new utility modules) and confirm the blocked/allowed scope above matches your intent -- in particular whether loopback should default-block for DB-stored servers, and whether RFC1918/Tailscale staying unblocked is correct. If yes, merge kind_robots#1926, then set approved_by_human: true and status: done here (or say so and a session will do the close-out). If you want a narrower or wider blocked range, say what to change and it'll be revised on the same PR.

What unblocks when approved: t-006 (product-surface wiring + self-hosted setup docs) is already status: waiting on this task via depends_on; nothing else is gated behind it.

Closed under Silas's 2026-09-07 human-gate simplification instruction. The recommended boundary is accepted: DB-stored server profiles block loopback/cloud-metadata/link-local destinations, while explicitly trusted RFC1918 LAN and Tailscale CGNAT remain usable because private/self-hosted text servers are the feature's purpose; only the operator-configured Ollama localhost fallback opts into loopback. Kind Robots PR #1926 already merged with focused security coverage, so leaving the roadmap at needs-human was stale bookkeeping.
<!-- note:end t-005 -->

## t-007 — Extend the admin server-uptime dashboard to cover text-capable servers

<!-- note:begin t-007 -->
Kaizen from t-001's research: server/api/server/uptime.get.ts currently restricts its serverType where-clause to A1111/COMFY by default (overridable via ?serverType= but not surfaced anywhere for text). Once t-003/t-004 land real text-server profiles, extend the admin uptime dashboard's default scope (or its UI) to include OPENAI/ANTHROPIC/OLLAMA/CUSTOM text servers so their health/uptime is as visible as the art/GPU servers already are.
<!-- note:end t-007 -->

## t-008 — Unify OpenAI/Anthropic header construction into one shared code path

<!-- note:begin t-008 -->
Kaizen from t-004: server/api/generate/text.post.ts's buildUpstreamAuth hand-builds OpenAI/Anthropic auth headers inline, duplicating the shape of textProviderService.ts's existing buildTextServerAuthHeaders (used for Ollama and any generic stored-server case). Fold both into one shared header-building function in textProviderService.ts so the legacy chat routes and the new unified generation endpoint share exactly one code path instead of two independently-maintained ones.
<!-- note:end t-008 -->
