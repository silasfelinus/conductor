#!/usr/bin/env python3
"""One-shot Kapowarr aggregation roadmap expansion.

This file is deleted by the companion one-shot workflow after it updates and
validates the authoritative roadmap on main.
"""
from pathlib import Path

import yaml


PATH = Path("projects/kapowarr/roadmap.yaml")
roadmap = yaml.safe_load(PATH.read_text(encoding="utf-8"))

roadmap["notes_from_silas"] = (
    "Higher-than-average priority. Aggregation is the primary product goal; "
    "multi-user support and deep reader polish are intentionally secondary for "
    "now. After live hardening the existing SABnzbd/Newznab path, expand the "
    "-arr acquisition fabric (Torznab/Prowlarr/Jackett and torrent lifecycle), "
    "then prioritize weekly release lists, story arcs/read lists, GetComics "
    "discovery/recommendations, metadata-provider resilience, and additional "
    "sources. Do not run recurring upstream-fork monitoring; inspect upstream "
    "deliberately when a concrete integration or sync task calls for it.\n\n"
    "Keep Conductor and Kind Robots project state synchronized; treat missing "
    "Project/conductorSlug or milestone projection as a bug to investigate "
    "rather than silently continuing."
)

milestones = roadmap.setdefault("milestones", [])
by_milestone = {m["id"]: m for m in milestones}
by_milestone["m4"].update(
    title="MAINTAIN — respond to real usage without recurring upstream monitoring"
)
new_milestones = [
    ("m5", "ACQUIRE — complete the -arr-style source/indexer/client fabric", 40, "in-progress"),
    ("m6", "DISCOVER & CURATE — weekly lists, story arcs, wanted, and recommendations", 30, "not-started"),
    ("m7", "METADATA — reduce ComicVine dependence and preserve portable identity", 20, "not-started"),
    ("m8", "SOURCES — broaden lawful discovery and acquisition options", 15, "not-started"),
    ("m9", "READER FOLLOW-UPS — format completeness after aggregation priorities", 5, "not-started"),
]
for milestone_id, title, weight, status in new_milestones:
    if milestone_id not in by_milestone:
        item = {"id": milestone_id, "title": title, "weight": weight, "status": status}
        milestones.append(item)
        by_milestone[milestone_id] = item


tasks = roadmap.setdefault("tasks", [])
by_task = {t["id"]: t for t in tasks}
t023 = by_task["t-023"]
t023.update(
    status="done",
    owner=None,
    recurring=False,
    note=(
        "Recurring upstream monitoring retired by explicit user direction on "
        "2026-08-17. Keep FORK_MAINTENANCE.md as the deliberate one-time sync "
        "procedure, but only inspect/import upstream when a concrete task needs "
        "it. The prior no-op cycle confirmed stable upstream/main remained at "
        "V1.3.1."
    ),
    updated="2026-08-18T00:51:00Z",
)


def add_task(task_id, milestone, title, note, status="not-started"):
    if task_id in by_task:
        return
    item = {
        "id": task_id,
        "milestone": milestone,
        "title": title,
        "status": status,
        "owner": None,
        "passes": 0,
        "stakes": "reversible",
        "note": note,
    }
    tasks.append(item)
    by_task[task_id] = item


add_task(
    "t-024", "m5", "Live-verify and harden Newznab to SABnzbd end-to-end",
    "The SABnzbd client and Newznab search/NZB handoff are merged and heavily "
    "unit-tested, but neither was live-verified against the user's real services "
    "during implementation. Exercise caps/search/download/queue/history/storage, "
    "remote mappings, restart persistence, failures, and post-processing on the "
    "real stack before treating Usenet support as complete.",
    "ready",
)
add_task(
    "t-025", "m5", "Reconcile relevant upstream development acquisition architecture",
    "Perform a one-time selective reconciliation against Casvt/development's newer "
    "indexer/download-client/download-prepper/query-builder/search-planner architecture. "
    "Preserve fork-only SABnzbd/Newznab, importer, notifications, health, reader, and "
    "branding behavior. This is foundation work, not recurring monitoring.",
    "ready",
)
add_task(
    "t-026", "m5", "Add Torznab with first-class Prowlarr and Jackett support",
    "Implement torrent indexers as protocol peers to Newznab so Prowlarr and Jackett "
    "feed the normal search/ranking/queue pipeline. Support multiple indexers, test/caps "
    "behavior, categories, source provenance, and clean handoff to torrent clients.",
    "ready",
)
add_task(
    "t-027", "m6", "Add weekly release and pull-list workflows",
    "Build a comic-native weekly releases and pull-list workflow after the current NZB "
    "path is live-hardened. Cross-reference new releases with monitored library volumes, "
    "surface wanted additions, and keep the release data source replaceable.",
    "ready",
)
add_task(
    "t-028", "m6", "Add story arcs and portable CBL/read-list workflows",
    "Model ordered story arcs/read lists across volumes and issues, support CBL import/export "
    "where practical, and let arcs identify missing issues acquisition can fill. Keep this "
    "aggregation oriented; per-user reading-state sophistication is out of scope for now.",
    "ready",
)
add_task(
    "t-029", "m6", "Build a GetComics Discover browser",
    "Implement the spirit of upstream issue #6: browse recent GetComics releases inside "
    "Kapowarr, open/search/add matching series, and optionally monitor discovered series. "
    "Reuse source parsing/search infrastructure instead of a second scraping path.",
)
add_task(
    "t-030", "m6", "Add library-informed Discover and Similar recommendations",
    "Extend Discover with explainable recommendations from the current library: related "
    "series/franchise/title stems, publisher, creators and characters when metadata supports "
    "them, plus recent source releases not already owned. Start deterministic, not opaque ML.",
)
add_task(
    "t-031", "m5", "Harden torrent lifecycle, hardlinks, and oversized pack handling",
    "Close acquisition gaps reflected in upstream issues #208 and #212: allow packs with extra "
    "issues to satisfy monitored gaps when permitted, add seed-safe hardlink imports, and verify "
    "rename/conversion/post-processing does not break active seeding.",
)
add_task(
    "t-032", "m5", "Add source quality preferences and upgrade policy",
    "Bring more Sonarr/Radarr-style acquisition control to comics: source/client priority, "
    "GetComics SD/HD preference (upstream issue #222), pack preference, and optional later "
    "upgrade searches without replacing a known-good file with a worse candidate.",
)
add_task(
    "t-033", "m6", "Add Wanted/Missing workbench and manual import",
    "Add an -arr-style global Wanted view for monitored missing issues/volumes, searchable and "
    "bulk-actionable, with manual import for files acquired elsewhere. Incorporate the useful "
    "intent of upstream issue #344 without duplicating continuous library import.",
)
add_task(
    "t-034", "m5", "Add watched-folder auto import for external downloads",
    "Implement upstream issue #122's workflow: watch inbound folders, match completed external "
    "files to known volumes/issues, then move, rename, convert and register through the hardened "
    "post-processing pipeline. Do not compete with root-library continuous import.",
)
add_task(
    "t-035", "m5", "Add NZBGet as a second Usenet download client",
    "Generalize the Usenet client seam beyond SABnzbd with NZBGet-compatible submission, status, "
    "history and cancel handling so the acquisition matrix is not tied to one downloader.",
)
add_task(
    "t-036", "m6", "Add calendar and upcoming monitored release view",
    "Complement weekly pull lists with an -arr-style calendar of upcoming and recently released "
    "monitored issues, direct search actions, and clear source/metadata provenance.",
)
add_task(
    "t-037", "m7", "Introduce a metadata-provider abstraction",
    "Stop treating ComicVine as an irreplaceable global singleton. Define stable provider IDs, "
    "cross-provider external IDs, search/fetch capabilities, cover provenance and conflict rules "
    "so alternate metadata providers can coexist without destabilizing existing libraries.",
)
add_task(
    "t-038", "m7", "Add Metron as an alternate metadata provider",
    "Implement upstream issue #182 after the provider boundary exists. Support Metron search and "
    "volume/issue metadata with durable IDs and graceful fallback when ComicVine is unavailable "
    "or rate-limited rather than silently mixing identities.",
)
add_task(
    "t-039", "m7", "Use and export portable comic metadata",
    "Expand local-metadata awareness into deliberate ComicInfo.xml and compatible series metadata "
    "import/export. Incorporate upstream issues #139 and #50 so imported files can identify "
    "themselves and managed archives retain useful metadata outside Kapowarr.",
)
add_task(
    "t-040", "m8", "Add an Anna's Archive source adapter",
    "Track upstream issue #171 and the maintainer's preference for Anna's Archive over separate "
    "Z-Library/Libgen integrations. Fit discovery into the generic source/indexer boundary and "
    "only automate downloads lawfully accessible to the user; do not bypass access controls.",
)
add_task(
    "t-041", "m8", "Add Internet Archive public-download source support",
    "Integrate Internet Archive search/metadata and official downloadable assets where an item "
    "permits direct public access. Treat controlled-lending or restricted items as browse/link-out "
    "only; do not build page ripping or access-control bypasses.",
)
add_task(
    "t-042", "m8", "Evaluate debrid acquisition support",
    "Assess upstream issue #276 and common -arr-adjacent workflows for a clean debrid client "
    "boundary. Implement only if it adds meaningful coverage without contaminating generic "
    "search/download architecture with a provider-specific shortcut.",
)
add_task(
    "t-043", "m8", "Evaluate eMule/aMule for non-US comic catalogs",
    "Preserve upstream issue #178 as lower-priority acquisition research, especially for European "
    "and non-US catalogs poorly represented in the current source mix. Require a maintainable "
    "client API and matching strategy before implementation.",
)
add_task(
    "t-044", "m5", "Verify downloaded comic/archive integrity",
    "Incorporate upstream issue #154: verify CBZ/ZIP/CBR/RAR and other supported containers can "
    "open and contain plausible pages, surface CRC/corruption problems, and integrate failures "
    "with history/blocklist/retry rather than discovering damage only in a reader.",
)
add_task(
    "t-045", "m9", "Add CBR/RAR and remaining archive formats to the built-in reader",
    "Reader-only follow-up after aggregation priorities. Library/file-processing already recognizes "
    "CBR/RAR plus CB7/7z, CBT/tar and other containers; the reader currently opens CBZ/ZIP, loose "
    "images and PDF. Add safe extraction for CBR/RAR first, then other practical formats.",
)

PATH.write_text(
    yaml.safe_dump(roadmap, sort_keys=False, allow_unicode=True, width=100),
    encoding="utf-8",
)
