# Kapowarr Fork — Design Brief

date: 2026-08-15
source: Silas (project registered 2026-08-15, `d4a5a4e`), grounded against upstream
  Casvt/Kapowarr and silasfelinus/Kapowarr's public state
kind: software
slug: kapowarr

## The one-liner

Evolve Silas's personal fork of [Kapowarr](https://github.com/Casvt/Kapowarr) — a
comic-book library manager in the *arr family (Sonarr/Radarr, but for comics) — into
a more comfortable, more personal tool, while keeping it a clean, rebasable fork that
gives clear, ongoing credit to the upstream project.

## What Kapowarr is today (upstream, for context)

- **Purpose:** builds and manages a digital comic library — search, download, import,
  rename, and organize comic issues/volumes/TPBs/one-shots/hardcovers.
- **Stack:** Python backend (`Kapowarr.py`, `backend/{base,features,implementations,
  internals,lib}`), a web frontend, Docker-first deployment. GPL-3.0 licensed.
- **Metadata:** ComicVine is the primary metadata source.
- **Downloads today:** two distinct client families, already separated in the
  settings model —
  1. **Built-in direct-download clients** (GetComics-sourced DDL, Mega, Pixeldrain),
     which can optionally take user credentials for higher speeds/limits.
  2. **External torrent clients**, added by the user (URL + credentials); Kapowarr
     talks to them over their own APIs.
- **No Usenet/NZB support exists yet.** Upstream tracks this as
  [issue #71](https://github.com/Casvt/Kapowarr/issues/71) (opened 2023-07-15,
  labeled "Handled Soon" in the project's own plan) — this fork's m2 Usenet/NZB work
  (t-006–t-009) is picking up a gap upstream has acknowledged wanting but hasn't
  shipped, not inventing a competing feature.
- **`silasfelinus/Kapowarr`** is currently a plain fork with no divergence yet
  (same history as upstream) — this brief is the first fork-specific artifact.

## Fork goals

1. **Personality and comfort first (m1).** Small, low-risk QoL/personality touches
   that make the fork feel like *Silas's* tool without changing its behavior for
   anyone who doesn't opt in — rotating loading lines, a configurable display title,
   database-driven launch flair.
2. **Real capability growth (m2).** The QoL gap audit (t-005) plus deliberate
   Usenet/NZB support (t-006–t-009) — the single largest capability upstream itself
   doesn't have yet.
3. **Stay a good fork citizen (m3 + ongoing).** Preserve attribution, keep
   customizations isolated enough to rebase cleanly, keep Conductor/Kind Robots
   project state in sync with reality, and document the maintenance workflow so this
   doesn't silently rot into an unmergeable divergence.

## Upstream-credit and licensing policy

- Kapowarr ships GPL-3.0. The fork **keeps the GPL-3.0 `LICENSE` file verbatim** and
  keeps the existing upstream copyright/attribution notices in place — GPL-3.0
  requires this and it also happens to be the right thing to do.
- The fork's README (or a dedicated `FORK.md`) must say, near the top, that this is a
  personal fork of Casvt/Kapowarr, link to the upstream repo, and briefly state how
  it diverges (personality/QoL layer + Usenet/NZB support). Do not imply upstream
  endorses or maintains the fork's changes.
- **Upstream is reference-only.** Agents read upstream code/issues/docs for context
  (e.g. issue #71 above) but do not open upstream PRs or issues unless Silas
  explicitly asks for that in a session. All implementation work lands in
  `silasfelinus`-owned repositories only.
- No renaming that erases the Kapowarr identity. A configurable *display* title
  (t-003) is fine; forking the product identity away from "Kapowarr, personalized"
  is not part of this brief's scope.

## Architecture boundaries

- **Where things live:** the actual fork code lives in `silasfelinus/Kapowarr`, a
  separate repository from both `conductor` and `kind_robots`. **This conductor
  session's GitHub access is scoped to `silasfelinus/conductor` and
  `silasfelinus/kind_robots` only** — it cannot open branches/PRs against
  `silasfelinus/Kapowarr` directly. Every task after this one (t-002 onward) that
  touches actual fork code needs either a session with `Kapowarr` in its GitHub
  scope, or should follow AGENTS.md's cross-repo target-repo handoff pattern
  (`projects/kapowarr/docs/<task-id>-<slug>.md` with the intended branch, files, and
  patch/steps) if no such session is available when the task is picked up. This
  brief itself is a conductor-repo document, not a Kapowarr-repo change, so it
  doesn't hit that boundary.
- **Personality/QoL layer stays additive, not invasive.** Loading-line copy (t-002),
  the display title (t-003), and launch flair (t-004) should each be a small,
  centralized module (e.g. a `personality`/`branding` layer) that the existing UI
  calls into — not scattered edits across core templates/routes. This is what keeps
  m1 easy to both review and rebase.
  - Loading copy: one data source (list or table) + one lookup function, with the
    existing default/neutral loading state as the guaranteed fallback if the
    personality lookup fails or JS is unavailable — never let a joke line become a
    single point of failure for "is Kapowarr loading."
  - Display title: read from configuration (env var or a settings-DB row, matching
    Kapowarr's existing settings patterns) with the literal string `"Kapowarr"` as
    the hard-coded default — never bake a custom title into a template in a way that
    would conflict on every upstream merge.
  - Launch flair: derive from data already in the local database (a random
    comic/volume title), sanitize anything comic-derived before it reaches a
    template (user-imported metadata is not trusted input), and fall back to a
    fixed, deterministic generic message when the library is empty — this must
    degrade gracefully on a brand-new install, which is the single most common state
    a first-time fork user will actually see.
- **Usenet/NZB sits beside the existing client abstraction, not inside it (t-006).**
  Kapowarr already separates "built-in DDL clients" from "external clients the user
  registers." SABnzbd should join as a new *external client type* in that same
  family — not a special case bolted onto the torrent-client code path, and not
  merged into the GetComics DDL scraper. Concretely, the boundary to design:
  - **Search/indexing** (finding NZBs) is a distinct concern from **submission**
    (handing a chosen NZB to SABnzbd) and from **status/import** (polling completion,
    handing off to the existing post-processing/renaming pipeline). Upstream's
    GetComics scraper is a direct-download source, not an indexer — an NZB indexer
    is a new, parallel search source, not a modification of the scraper.
  - Normalize NZB search results into whatever shape the existing "pick a release"
    UI/queue already expects, so the download-queue and history UI don't need a
    Usenet-specific code path once a release is selected.
  - SABnzbd itself (t-007) only needs: connection test, submission, status polling,
    cancellation (where SABnzbd's API allows it), and config validation — the same
    shape as any other external client, which is exactly why it belongs in that
    family rather than a bespoke subsystem.
  - This keeps the door open for additional indexers/clients later (t-008) without
    a second architecture rewrite.
- **Rebase discipline is a first-class constraint, not an afterthought.** Every m1/m2
  change should ask "if upstream touches this file next release, how bad is the
  merge?" Prefer: new files over edited core files, config/data over hard-coded
  behavior, and feature flags that default to "behave like upstream" so a fresh
  `git fetch upstream && git merge` mostly just works. t-011 turns this into a
  written maintenance workflow once there's enough real experience to document it
  honestly — this brief sets the constraint, t-011 writes the runbook.

## First-release scope (m1 exit criteria)

A first release is "shippable" for Silas's own use once:

1. The fork has visible, documented identity (README/`FORK.md` crediting upstream,
   configurable display title working, GPL-3.0 license intact).
2. Rotating loading lines and launch flair are live and degrade safely (no JS, no
   data, or a corrupted lookup never breaks the underlying loading/launch behavior).
3. `kapowarr` shows up correctly in Kind Robots (t-010) with `conductorSlug:
   kapowarr` and current lifecycle/priority/milestone projection — the fork isn't
   just code, it's also a tracked project, and t-010 exists specifically because
   this kind of sync has silently drifted before on other projects.
4. Nothing in (1)–(3) has modified core matching, scraping, download-client, or
   import logic — m1 is purely additive personality/config work. Usenet/NZB (m2) is
   deliberately sequenced after m1, not bundled into the first release.

## What should remain easy to rebase from upstream

- Core comic matching, metadata handling, the existing DDL scraper, and the existing
  torrent-client integration: **do not modify these for personality/QoL work.** m2's
  Usenet/NZB work adds beside them per the boundary above; it doesn't rewrite them.
- Settings/config schema: extend (new keys/tables) rather than repurpose existing
  fields, so an upstream settings-page change doesn't collide with a repurposed field
  that now means something else in the fork.
- Frontend templates/static assets Kapowarr already owns: prefer new
  components/partials the personality layer calls into, over line-edits inside
  upstream's existing template files.
- Docker/install docs: keep the upstream install path working unmodified; document
  fork-specific setup (if any config knobs are fork-only) as an addendum, not a
  replacement.

## Boundaries (hard gates, unchanged from AGENTS.md defaults)

- No upstream PRs/issues without Silas's explicit ask.
- No publishing, app-store/package distribution, payments, or production deploys of
  the fork without `needs-human` sign-off — this is a personal tool project, but the
  same outward-facing/irreversible gates apply as anywhere else.
- No modification to upstream-owned files' *licensing* content, ever.
- Generated art for the fork's own branding goes through the normal conductor art
  pipeline like any other project asset.

## Status

Registered by Silas 2026-08-15 (`d4a5a4e`, `project-overrides.yaml` status: active,
priority: high). This brief (t-001) is the first task; t-002–t-004 (m1 personality/
QoL) and t-005–t-006 (m2 audit + Usenet/NZB boundary design) are `ready` and can be
picked up independently once a session with the appropriate repo access claims them.
t-007–t-009 are `not-started`, gated behind t-006's boundary design landing first so
implementation doesn't guess at an interface that hasn't been specified yet.
