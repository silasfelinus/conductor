# Marketing Deck

## Purpose

Marketing Deck is a reusable internal production tool that turns a selected Kind Robots record into a coherent, reviewable marketing set. V1 is Project-first: choose a Project, optionally attach related Projects, choose the deliverables to generate, review the source brief, and create only those assets.

The first complete reference project is Humboldt Scoop Solutions:

- `humboldt-scoop` is the parent business and existing website/brand project.
- `humboldt-scoop-cms` is the related customer-management, scheduling, and route-planning product.
- The existing HSS logo, website, approved copy, and real product screens are inputs to preserve, not invitations for an unsolicited rebrand.

## Product principles

1. **Selectable, not monolithic.** A user may request one flyer, a full launch kit, or any combination in between.
2. **Existing assets are authoritative.** Reuse supplied logos, colors, copy, screenshots, and approved layouts. Missing inputs become explicit requests.
3. **One normalized source contract.** Renderers consume a `MarketingSource` snapshot rather than reaching directly into every Prisma model.
4. **Separate fact from invention.** Supplied business facts remain facts; generated positioning, copy, and concepts are labeled suggestions until approved.
5. **Human-gated outward action.** Generation may be automated. Publishing, printing, outreach, account creation, deployment, media buying, and spend are not.
6. **Traceable generation.** Store source slugs, asset references, prompt/version metadata, provider/model information, and output manifests.
7. **Commercially safe generation.** Commercial assets follow the licensing rules in `CONTROL.md`; dev-licensed models do not produce commercial output.

## V1 source flow

1. Select a primary Project by slug.
2. Optionally select one or more related Projects.
3. Load identity, goal, waypoints, descriptions, repo/live URLs, art collections, logos, screenshots, audience notes, geography, offers, and constraints.
4. Display a normalized creative brief for correction before generation.
5. Select deliverables individually or start from an editable preset.
6. Generate drafts and an export manifest.
7. Review, revise, approve, and export without publishing.

For HSS, the primary source is `humboldt-scoop`; `humboldt-scoop-cms` contributes app screens, operational proof points, scheduling, and the customer route-maker story.

## Selectable deliverable catalog

### Brand and print

- Business card
- Existing-logo application or lockup sheet
- Lawn sign
- Banner
- Flyer
- Static ad poster variants

### Digital presentation

- Desktop and mobile website mockup board
- Android-first app mockup board
- Linux/iOS future-platform presentation board
- Social and display-ad crops derived from approved masters

### Content production

- Photo-shoot concepts
- Print-content shot list
- Short-form and commercial video shot list
- Location, subject, prop, release, b-roll, orientation, and reuse guidance

### Campaign and advertising

- Static ad concepts and copy variants
- Video commercial treatment
- Storyboard and edit plan
- Optional ComfyUI execution package: prompts, workflow references, source assets, generation manifest, captions, and export sizes
- Week-by-week launch schedule with asset deadlines, suggested channels/communities, posting cadence, outreach ideas, measurement checkpoints, and optional budget scenarios

## Proposed normalized records

The implementation may refine names, but it should preserve these boundaries:

### MarketingSource

- `sourceType`
- `sourceId`
- `sourceSlug`
- `relatedSources`
- `identity`
- `audience`
- `geography`
- `offers`
- `proofPoints`
- `copy`
- `assets`
- `screenshots`
- `constraints`
- `userNotes`
- `provenance`

### MarketingSet

- primary and related source references
- selected deliverable keys
- normalized creative brief snapshot
- generation status and human-review status
- provider/model and token/compute usage metadata
- prompts and workflow versions
- generated output references
- export manifest
- revision history

### MarketingDeliverable

- stable deliverable key
- dimensions and aspect ratio
- required inputs
- dependency keys
- copy and asset slots
- print/export rules
- generation method: deterministic template, LLM-assisted, image generation, video generation, or mixed
- human-gate requirements

## HSS reference acceptance criteria

The first approved reference set should include:

- one business-card system
- one lawn-sign design
- one banner design
- one flyer design
- website presentation mockups based on the existing HSS site
- app presentation mockups based on the CMS and mapped route-maker
- one practical photo/video shoot plan
- at least two static ad poster directions
- one video commercial treatment and storyboard
- an optional ComfyUI execution package
- a week-by-week launch calendar
- one export manifest listing sources, dimensions, versions, and approval state

No customer address, access code, billing data, or private route detail may appear in the marketing set.

## AI and computation policy

This is initially a single internal tool for Silas and the team. It may use Silas-owned LLM, image, and video generation tokens where helpful. Credentials stay server-side, usage should be visible, and generation must not imply authorization to spend on ads, print products, publish content, create accounts, or deploy software.

Deterministic work should remain deterministic. Template layout, dimensions, export rules, geospatial route calculation, and file assembly do not become better merely because an LLM was invited to the meeting.

## Evolution beyond Projects

After the Project-first workflow is stable, introduce a `MarketingSource` adapter interface for other Kind Robots models. Each adapter maps a model into the normalized source contract. Deliverable renderers remain model-agnostic.

The second-model proof should be deliberately small and low-risk. The goal is to prove reuse, not unleash a switch statement hydra.