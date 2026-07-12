# Ecosystem Map Design Brief

## Purpose

Ecosystem Map exists to keep Kind Robots from accidentally building the same thing twice under different project names. It is the cross-project architecture lens for Dreams, Bots, ArtCollections, narrator topics, threads, project menus, image prompts, generated assets, and Conductor roadmaps.

The project should not become a second source of truth. Its job is to document ownership, expose gaps, and create small implementation tasks in the project that already owns the right layer.

## Problem

Kind Robots is becoming an ecosystem, not a pile of apps. Projects now share repeated primitives:

- Project identity through matching Conductor project slugs and PROJECT Dreams.
- Visual identity through icon/card/hero images and inspiration galleries.
- Bot identity through Manager or Assistant bots tied to project Dreams.
- Navigation through narrator topics, threads, and project-specific menus.
- User-facing progress through project goals and roadmap milestones.
- Agent-facing execution through Conductor roadmaps.
- Generated content through ArtCollections, packs, galleries, and media paths.

That is powerful, but it also creates clone-risk. If one project builds a custom menu, another builds a custom narrator thread, and a third builds a different project assistant pattern, the ecosystem turns into a junk drawer with better lighting. We want shared primitives with project-specific flavor layered on top.

## Working model

### Canonical ownership

| Primitive | Canonical owner | Notes |
| --- | --- | --- |
| Agent task queue | Conductor `projects/<slug>/roadmap.yaml` | Authoritative for Worker/Reviewer execution. |
| Project identity/display | Kind Robots Dream with `dreamType: PROJECT` | Slug matches Conductor project directory. |
| Friendly project progress | Project `goal` and roadmap `milestones` | UI/voice layer only, not a replacement for roadmap tasks. |
| Project visual assets | Conductor `projects/images/` for icon/card/hero | Distributed into the workspace by existing scripts only after approval. |
| Inspiration gallery | Kind Robots `public/images/artcollections/<slug>/` | ArtCollection-style folder and manifest layer; generated candidates require approval before becoming canonical. |
| Project bot | Existing Bot framework | One Manager or Assistant bot per project Dream unless explicitly skipped. |
| Bot avatar/emotions/actions | Existing bot image framework | Avatar plus twenty thin portrait images. Avoid a new asset model; generated portraits require approval. |
| Project-specific navigation | Narrator topics and threads | Menus should be generated/configured through the existing narrator structure. |
| Shared content packs | Packmaker + Kind Robots sharing/ACL layer | Do not invent parallel permissions. |

### Project bot parity

Every active project should be able to declare one primary project companion:

- `botType: Manager` when the bot helps coordinate project tasks, menus, approvals, queues, and status.
- `botType: Assistant` when the bot mainly helps the user create, browse, or use the project output.

Each bot should have:

- One avatar image.
- Twenty thin portrait emotion/action images using the existing bot image pattern.
- A Dream link through the shared project slug.
- Narrator topics and threads that define its project-specific navigation menu.
- A short personality/role contract that tells it what it owns and what it must route elsewhere.

### Visual asset parity

Every active project should eventually have:

- `icon`: square app-style identity image.
- `card`: portrait project card key art.
- `hero`: wide project banner/title image.
- Inspiration images: at least three to establish visual vocabulary.
- Mock screenshot concepts where the project includes an interface or product surface.
- Bot avatar and emotion/action portraits when the project has a companion bot.

Agents should write prompts and routing metadata, not commit generated binaries from agent runs.

### Image approval gate

Until the art generator consistently produces high-quality, on-brief assets, all generated images are candidates, not canonical assets. The system may be aggressively populated with requests and prompts, but any generated output that would become a project icon/card/hero, inspiration image, mock screenshot, bot avatar, or bot emotion/action portrait must stop for human approval before replacing placeholders, updating gallery manifests, attaching to Dreams/Bots, or becoming the displayed default.

The intended flow is:

1. Queue many requests with clear `image_path`, size, variant, project slug, and prompt quality criteria.
2. Generate candidate images into a review/staging location.
3. Present candidates for approval, rejection, or regeneration.
4. Promote only approved images into the canonical destination paths and manifests.
5. Preserve rejected or alternate generations only when they are useful as references; otherwise keep them out of the main project surfaces.

Quality criteria should be explicit enough to reject mush without debate:

- correct aspect ratio and destination variant;
- no readable text, accidental UI labels, logos, watermarks, contact sheets, or collages;
- clear focal subject and professional composition;
- matches the project’s visual intent rather than generic “AI art” vibes;
- consistent enough with the Kind Robots ecosystem to share visual language;
- technically clean at display size, especially for icons and thin portrait bot images.

## Duplication risks to audit first

1. **Project navigation** — custom menus should flow through narrator topics/threads, not bespoke per-project menu tables.
2. **Project status** — Conductor owns task status; Dreams own friendly display. Do not sync in both directions without a clear rule.
3. **Image storage** — project hero/icon/card, ArtCollection inspirations, and bot portraits need a documented destination split plus a review/staging path.
4. **Pack permissions** — Packmaker, digital-storefront, and Kind Robots sharing/ACL work should reuse one permission model.
5. **Project assistant logic** — Manager/Assistant bot behavior should be configured data-first, not copied into one-off components.
6. **Mock screenshots** — useful as inspiration assets, but should not become fake UI source files or compete with actual components.

## First deliverables

1. Asset coverage matrix for every active project.
2. Manager/Assistant bot parity spec.
3. Shared-layer reuse map showing where duplicate work is likely.
4. Follow-up tasks routed to the owning project: `kind-robots`, `global-ui`, `packmaker`, `art-generator-connect`, or project-specific roadmaps.
5. Image approval workflow spec covering request population, candidate staging, review, and promotion.

## Non-goals

- Do not create a second project registry.
- Do not add redundant foreign keys where slug parity already joins systems.
- Do not generate or commit binary images.
- Do not publish, deploy, spend, create live products, or touch DNS/secrets.
- Do not replace Conductor roadmaps with a separate friendly-progress layer; milestones surface roadmap state, they do not fork it.
- Do not auto-promote generated images to canonical paths before approval.

## Tone

This project is the map room: tidy, opinionated, and allergic to duplicate wheels. We can have many portals, but one floor plan. Image generation can be prolific, but the velvet rope stays up until the art earns it.
