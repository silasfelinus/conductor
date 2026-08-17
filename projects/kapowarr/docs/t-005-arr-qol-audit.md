# t-005: Audit -arr quality-of-life gaps

Compares the live `silasfelinus/Kapowarr` fork's library, search, queue,
download-client, settings, health, import, and history flows against mature
`-arr`-suite interaction patterns (Sonarr/Radarr/Prowlarr conventions), based on a
read-only inspection of the actual fork source (cloned, inspected, deleted — no
writes made to the fork or upstream).

## Method

Read the relevant templates/JS/backend for each flow area directly rather than
inferring from feature lists, to separate "actually missing" from "present but not
obvious from the roadmap notes."

## What's already solid (no action needed)

These are worth recording so a future audit doesn't re-flag them as gaps:

- **Queue**: `queue.js` has drag-reorder priority (`moveEntry`), per-entry delete with
  an optional "delete + blocklist" flag (`deleteEntry(id, api_key, blocklist=false)`),
  and bulk `deleteAll`. This already matches Sonarr/Radarr queue interaction patterns.
- **Search**: per-issue and per-volume auto-search and manual/interactive search both
  exist (`view_volume.js`: `autosearchIssue`, `autosearchVolume`, `showManualSearch`),
  plus a monitor/unmonitor toggle per volume (`toggleMonitored`).
- **Download clients**: a live "Test" button exists for editing/adding a client
  (`settings_download_clients.js`: `testEditTorrent`, `POST /externalclients/test`)
  with visible success/fail state — this is the standard -arr "Test" affordance.
- **Root folders**: multi-root-folder support exists end-to-end (backend
  `root_folders.py`, UI section in `settings_mediamanagement.html` line 194) — not a
  single hard-coded download path like a naive `-arr` clone might have.
- **Blocklist/History**: both have working pagination (offset-based), clear-all, and
  per-entry delete. Removing a blocklist entry is the existing "allow retry" path,
  which matches Sonarr's blocklist-removal convention.

## Concrete gaps found

### 1. No notification/webhook system at all
Zero code hits anywhere in `backend/` or `frontend/` for "notification" or "webhook".
Every mature `-arr` app (Sonarr, Radarr, Prowlarr, and Casvt's own later Kapowarr
work upstream) lets a user wire download-complete/import-failed/health-warning
events to Discord, a generic webhook, or similar, so they don't have to keep the tab
open to know something happened. This is the single highest-friction gap for
day-to-day use — see t-012 below.

### 2. No health-check / system-warnings surface
The only system-level page is `frontend/templates/status.html`, which shows static
About/Power/Donate/Contact info — there is no equivalent of Sonarr's "Health" page
(actionable warnings like "download client unreachable," "ComicVine API key
invalid," "root folder missing/inaccessible," "update available"). A user currently
has to notice a stalled queue or check logs to discover these conditions. See t-013
below.

### 3. History entries don't surface a failure reason
`history.html`'s table columns are `Link / File / Source / Downloaded At / State` —
`State` is presumably a coarse success/fail value (not inspected at the string
level to avoid scope creep into `t-009`'s territory, which already owns hardening
completion/import workflows). Worth folding into whichever task next touches
history/import hardening rather than a standalone task — noted here, not spun into
its own task, since `t-009` ("Harden download completion and import workflows") is
the natural owner and creating a fourth overlapping task would violate the "convert
friction into scoped follow-ups, not broad rewrites" instruction on this task.

## Considered and deliberately NOT turned into a task

- **Import lists** (auto-add library entries from an external list, à la Sonarr's
  list sync): zero code hits for `import_list`. Skipped as a proposed task —
  there's no comics-domain equivalent of Trakt/IMDb lists with the same ecosystem
  maturity, so this would be a speculative feature rather than a friction fix, and
  the task's own instruction is to convert *concrete* friction into scope, not invent
  new product surface.
- **Calendar view** (upcoming-release calendar): not investigated in depth — no
  existing scheduling/date-of-release UI was found, but comics release-date data
  reliability from ComicVine wasn't verified enough in this pass to scope a task
  responsibly. Left out rather than guessed at.

## Follow-up tasks created

- `kapowarr/t-012` — Add a Discord/generic-webhook notification system for
  download/import/health events.
- `kapowarr/t-013` — Add a health-check / system-warnings panel.

Both `stakes: reversible`, `status: ready`, milestone `m2` (BUILD) since both are
concrete QoL builds rather than shape/architecture (`m1`) or ship-hardening (`m3`)
work.
