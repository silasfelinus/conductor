# Project front-end tab integration

Every active **user-facing** project should be discoverable inside Kind Robots as a tab in an existing channel. A standalone route or external app can still exist, but it does not replace the tab: the tab is the shared discovery surface, and the PROJECT Dream's `liveUrl` is the canonical launch pointer.

This document decides **where a project belongs and how to prove it is stitched in**. It does not fork the implementation recipe. For exact file paths, templates, and image conventions, follow:

- `kind_robots/sample/new-section.md` — canonical implementation recipe.
- `conductor/projects/kind-robots/SECTIONS.md` — conductor policy and condensed checklist.

## Placement rule

Use this order every time:

1. **Reuse an existing stitched surface.** If the project already has a working tab and route, keep them. Record the channel key, tab key, route, and PROJECT Dream `liveUrl`; do not build a duplicate page.
2. **Choose the best existing channel.** Put the project beside the tools and experiences users would naturally associate with it.
3. **Use WonderLab as the fallback.** When no existing channel is an honest semantic fit, add the project as a tab under the `wonder` dashboard and route it through `/wonderlab` or a dedicated page belonging to that dashboard.
4. **Do not invent a new channel casually.** A new top-level channel is a hard human gate and requires Silas's explicit approval. A project needing a tab is not, by itself, justification for a new channel.
5. **Classify infrastructure explicitly.** Internal orchestration, scripts, shared libraries, and deployment plumbing may be marked `internal-only`; do not create a fake public page merely to satisfy a checkbox.

## Channel placement guide

Prefer the channel whose existing users and tools overlap with the project:

| Channel | Good fit |
| --- | --- |
| `art` | Image generation, styling, coloring, visual production, galleries, and creative image tools. |
| `academy` | Courses, guided learning, curriculum, references, and educational studios. |
| `builder` | Tools whose primary purpose is creating or editing reusable objects. |
| `dream`, `character`, `bot`, `composition` | Deep tools focused on one existing Kind Robots model or workflow. |
| `conductor` | Project steering, agent orchestration, roadmaps, approvals, and admin operations. |
| `giftshop` / community surfaces | Storefront, supporter, entitlement, and community experiences. |
| `wonder` | Cross-domain experiments, unusual tools, prototypes, and the required fallback when no better channel exists. |

Do not choose WonderLab merely because a project is new. Choose it because the project genuinely crosses domains or lacks a more natural home.

## Working reference surfaces

Use these as patterns rather than rebuilding navigation from scratch:

- **Superkate / Hair Studio** — a project-owned suite presented as the `stylist` tab in the existing Art channel, with its own `/stylist` route.
- **Conductor** — an admin project presented through the dedicated existing Conductor dashboard and `/conductor` route.
- **Challenge Center** — a working project front end that demonstrates a project becoming an actual usable surface rather than remaining roadmap metadata.
- **Mural** — a standalone `/mural` page registered as a canonical WonderLab tab.
- **Coloring Book** — a project front end registered as the `coloring` tab in the Art channel.
- **AI Art Academy** — an already-approved Academy surface with multiple tabs under one coherent channel.

Before adding anything, search `dashboardConfigs` and the relevant manager component; a surface may already be stitched even when the conductor roadmap does not mention it clearly.

## Required integration steps

For project `{project}` using tab `{tab}` in channel `{channel}`:

1. **Choose and record the placement.** Add `{channel}`, `{tab}`, intended route, and whether the route is internal or external to the project's ecosystem map row.
2. **Add the canonical dashboard tab.** Register the tab in `dashboardConfigs.{channel}.tabs[]` in `kind_robots/stores/helpers/dashboardHelper.ts` using a unique lowercase key, label, icon, title, summary, image, narrative, and route.
3. **Add the tutorial entry.** Add the matching key to `tutorialChannels.{channel}.sections[]` in `kind_robots/stores/helpers/tutorialCards.ts`.
4. **Add the two tab images.** Supply or queue:
   - `public/images/dashboard-tabs/{channel}/{tab}.webp`
   - `public/images/tutorials/{channel}/{tab}.webp`
   Placeholder art may ship temporarily; missing final art must be tracked rather than blocking the functional tab.
5. **Wire actual rendering.** Update the existing channel manager so selecting `{tab}` renders the project's real manager component. A tab card that only changes stored state, routes to the wrong default component, or displays an empty placeholder is not complete.
6. **Create a dedicated page only when useful.** When the project deserves a direct route, follow the page recipe in `kind_robots/sample/new-section.md`: `content/{title}.md`, valid `dashboardKey` / `dashboardTab`, and one `:{title}-manager` directive. The tab's `route` should point there.
7. **Set the PROJECT Dream launch pointer.** Set `Dream.liveUrl` to the internal route or external app URL. The Conductor project detail's **Open Project** control must launch the same surface.
8. **Keep ownership clean.** The project's roadmap owns its feature work. `ecosystem-map` owns placement audits and gap routing. Shared tab/navigation changes belong in `kind_robots` or `global-ui`, not duplicated in every project.

## Completion checklist

A front end is considered stitched only when all applicable checks pass:

- [ ] The project appears as a tab in the selected existing channel.
- [ ] Selecting the tab renders the intended project component, not the channel's default component.
- [ ] Refreshing or directly loading its route preserves the correct channel and active tab.
- [ ] A matching tutorial section exists.
- [ ] Dashboard and tutorial images exist or have explicit tracked replacements.
- [ ] The PROJECT Dream `liveUrl` points to the same route or external app.
- [ ] The Conductor project detail's **Open Project** action reaches it.
- [ ] TypeScript/typecheck and repository contract checks pass.
- [ ] Mobile tab density and basic responsive layout have been checked.
- [ ] No duplicate tab, route, manager, or source of project truth was introduced.

## Audit output

`FRONTEND-SURFACE-MAP.md` should include one row per active project with:

- project slug
- user-facing or internal-only
- existing surface status
- chosen channel key
- tab key
- route
- PROJECT Dream `liveUrl`
- manager/component owner
- tutorial/image coverage
- verification status
- follow-up roadmap task, when incomplete

Missing user-facing surfaces become small tasks in the owning project roadmap. Unless explicitly approved otherwise, those tasks should add a tab to an existing channel, with WonderLab as the fallback.