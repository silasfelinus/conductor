# Marketing Deck

Marketing Deck turns an existing Kind Robots model into a selectable, reviewable marketing set. The first pilot is **Humboldt Scoop Solutions**, the parent business project. `humboldt-scoop-cms` remains the customer-management and route-planning application; it is an input and product surface for the pilot, not the parent marketing subject.

## Product goal

A user selects a source model, chooses which marketing deliverables to generate, reviews the proposed plan, and produces only the approved items. The system should reuse existing brand assets and product designs before proposing replacements.

Version 1 accepts a `Project`. Later versions should support other schema models such as Dreams, Pitches, Products, Bots, Characters, Events, and reusable Facets without duplicating the generation pipeline.

## Source contract

Each marketing set should record:

- source model type and source model ID
- project or model title, description, audience, location, goals, and constraints
- existing logo, colors, typography, photography, website, app, and approved copy
- selected deliverable modules
- generation status, approvals, revisions, provenance, and export paths
- LLM, image, and video generation runs with provider/model metadata and estimated token or compute cost

Recommended application models:

- `MarketingSet`
- `MarketingDeliverable`
- `MarketingAsset`
- `MarketingCampaign`
- `MarketingScheduleItem`
- `MarketingGenerationRun`

A module registry should define requirements, prompt templates, output formats, dependencies, and approval gates for each deliverable. This keeps the system expandable instead of turning it into one enormous Humboldt-specific form wearing a fake mustache.

## Selectable deliverables

The first module catalog includes:

1. business card design
2. logo usage sheet and optional logo concepts or variants
3. lawn signage
4. large banner
5. flyer or door hanger
6. website mockup images
7. app mockup images
8. photo-shoot brief for print, social, and video content
9. static ad poster concepts and production files
10. video commercial concepts, scripts, shot lists, storyboards, and optional Comfy execution
11. week-by-week launch schedule
12. channel and community recommendations
13. posting frequency, content mix, and reuse schedule
14. complete export bundle and manifest

The selector must allow one, several, or all modules. Existing website and app designs should be imported as references and marked `existing`, `refresh`, or `replace`; regeneration is never the default.

## Humboldt Scoop Solutions pilot

The pilot should use the **Humboldt Scoop Solutions** parent project and consume relevant material from both repositories:

- `humboldt-scoop`: public business identity, existing logo, current site, service positioning, copy, and approved imagery
- `humboldt-scoop-cms`: app design, customer workflow, service scheduling, route cards, and future mapped route planner

Pilot outputs should include:

- a brand inventory using the existing logo
- business card, lawn sign, banner, flyer, and static ad layouts
- website and app presentation mockups based on the designs already present
- a practical local photo and video shoot plan
- commercial concepts ranging from low-cost phone footage to generated or composited Comfy sequences
- a launch calendar with weekly goals, local/community participation, posting cadence, and reusable content themes

No live publishing, advertising spend, printing order, DNS change, customer contact, or public launch may happen unattended.

## Platform architecture

Recommended shape:

- **client:** Flutter, Android first
- **compatibility goal:** Linux desktop and iOS from the same codebase
- **backend:** existing Kind Robots TypeScript/Nuxt/Nitro/Prisma APIs
- **state and records:** Kind Robots project/model IDs remain authoritative
- **image and video generation:** existing ComfyUI pipelines through approved Kind Robots generation routes
- **project orchestration:** Conductor roadmaps and approval gates

The Android-first client should focus on source selection, module selection, approvals, progress, previews, and exports. Generation and long-running work should stay server-side so Linux, iOS, and web clients can consume the same results.

## AI and computation policy

This is an internal tool for Silas and the team.

- Team-owned LLM credentials may be used for approved copy, ideation, campaign planning, scripts, shot lists, prompt expansion, and model-to-marketing transformations.
- Provider keys remain server-side and must never be bundled into Android, iOS, Linux, or web clients.
- Each generation is explicit, attributable, and cost-recorded.
- Route optimization, sizing, file conversion, scheduling arithmetic, and other deterministic work should not use an LLM.
- Comfy generation uses the existing self-hosted infrastructure where possible.
- GitHub Actions do not receive model-provider keys for routine work.

## Review and export rules

Every outward-facing deliverable starts as a draft. Approval is per deliverable, not all-or-nothing.

Exports should preserve:

- editable source or structured layout data
- print-ready PDF or SVG where appropriate
- PNG or WebP previews
- video script, shot list, storyboard, prompt/workflow metadata, and final render when requested
- dimensions, bleed, safe area, color profile, font notes, and asset licensing/provenance
- a manifest connecting every output to its source model and generation run

## Version 1 acceptance criteria

Version 1 is complete when a team member can:

1. choose Humboldt Scoop Solutions as the source project
2. see imported existing brand, website, and app references
3. select any subset of the deliverable catalog
4. generate structured drafts using team-owned LLM credentials and Comfy where selected
5. review, revise, approve, or reject each deliverable independently
6. export approved items with a manifest
7. use the Android client for the full review flow
8. run the same core workflow later from Linux and iOS clients without changing the backend contract
