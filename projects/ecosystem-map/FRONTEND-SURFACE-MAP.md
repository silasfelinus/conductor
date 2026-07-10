# Front-end surface map

Static repository audit completed 2026-07-10 for every project marked `active` in
`project-overrides.yaml`. This map answers where each project is discoverable in Kind
Robots, or where it should be stitched next.

## Audit rules

- A project is **complete** only when a useful surface is reachable and renders its
  intended component. A project card, API, image collection, or route-shaped file alone
  does not count.
- Existing channels are reused. WonderLab (`wonder`) is the fallback when no semantic
  channel fits.
- New top-level channels are not proposed here.
- `Dream.liveUrl` is the canonical Open Project target. Database values were not
  available to this static repo audit; every row therefore records the value that should
  be verified or set during implementation.
- Shared infrastructure is explicitly internal rather than receiving a fake page.

## Current roster

| Project | Class | Existing / proposed surface | Component / implementation evidence | Tutorial + images | `liveUrl` target | Audit result |
| --- | --- | --- | --- | --- | --- | --- |
| `superkate-services-calculator` | A | `art / stylist` → `/stylist` | Existing Hair Studio tab and stylist manager; shared suite surface | Existing tab contract; verify both images | `/stylist` | **Complete** — intentionally shares the Superkate suite tab. |
| `superkate-hairstyle-ai` | A | `art / stylist` → `/stylist` | Existing Hair Studio tab and stylist manager | Existing tab contract; verify both images | `/stylist` | **Complete** — intentionally shares the Superkate suite tab. |
| `conductor` | A | `conductor / conductor` → `/conductor` | Registered admin tab and Conductor manager/workspace | Registered image; tutorial should remain in parity | `/conductor` | **Complete**. |
| `kind-robots` | C | Whole application / home → `/` | Platform shell; adding a project-specific tab would duplicate the product itself | Site-wide | `/` | **Internal platform with a real product surface**; no extra tab. |
| `global-ui` | C | Shared across all managers and navigation | Cross-project UI layer, not an independent user product | N/A | `/conductor` | **Internal shared layer**; no fake tab. |
| `ecosystem-map` | C | Conductor project workspace | Planning/audit layer | N/A | `/conductor` | **Internal planning project**; no public tab. |
| `humboldt-scoop` | B/D | Proposed `wonder / humboldt-scoop` bridge to external site | Conductor card exists; no Kind Robots manager/tab found | Missing pair | External site URL when verified | **Missing bridge tab**. WonderLab fallback is appropriate unless a future business/community channel is approved. |
| `humboldt-scoop-cms` | D | Proposed admin-only `conductor / scoop-cms` | Conductor card exists; no dedicated rendered component found | Missing pair | `/conductor?workspace=scoop-cms` or dedicated route | **Missing admin tool surface**. |
| `digital-storefront` | A | `giftshop / giftshop` → `/sanctuary` | Existing giftshop/community channel surface | Existing registry; verify current art parity | `/sanctuary` | **Complete surface, product still in development**. Do not add a duplicate storefront tab. |
| `ai-art-academy` | A | `academy / timeline|styles|remix|stylelab` → `/academy` | Dedicated Academy channel and registered tabs | Registered tab images/tutorial contract | `/academy` | **Complete**. |
| `coloring-book` | A | `art / coloring` → `/art` | Registered Coloring Book tab and shared coloring engine | Registered tab image; verify tutorial image | `/art` | **Complete**. |
| `brainstorm` | A | `brainstorm / brainstorm` → `/dreams` | Registered Brainstorm dashboard tab | Registered image/tutorial contract | `/dreams` | **Complete**. |
| `sketchy` | D | Proposed `academy / sketchy` → `/sketchy` | Project images/collection references exist, but no manager/page/tab found | Missing pair | `/sketchy` | **Missing front end**. Academy is the best fit because this teaches drawing practice and critique. |
| `art-generator-connect` | C | Existing Art/Wonder generation tools are the user surface | Worker-to-art API relay/integration project | N/A | `/art` | **Internal integration**; do not add a duplicate relay tab. |
| `mural-design` | A | WonderLab Mural surface → `/mural` | Existing Mural page/manager and shared coloring engine | Existing route; verify canonical Wonder tab/tutorial pair | `/mural` | **Complete**. |
| `storymaker` | D | Proposed `scenario / storymaker` → `/stories` | Story channel exists, but no project-specific Storymaker tab/manager found | Missing pair | `/stories` (after tab wiring) | **Missing project tab**. Reuse the Stories channel. |
| `davinci` | D | Proposed `games / davinci` → `/davinci` | Life-sim game project; no dedicated manager/tab found | Missing pair | `/davinci` | **Missing game surface**. Reuse Games. |
| `media-watchlist` | D | Proposed `wonder / watchlist` → `/watchlist` | Conductor card exists; no app manager/tab found | Missing pair | `/watchlist` | **Missing front end**. WonderLab is the honest fallback until a media channel exists. |
| `conductor-app` | B/D | Proposed admin bridge `conductor / app` | External Flutter client project; Conductor card exists but no launch/bridge tab found | Missing pair | Deployed Flutter web/app landing URL, or `/conductor` until deployed | **Missing bridge surface**. |
| `alexa-integration` | B/D | Proposed `wonder / voice-lab` bridge/status tab | Voice skill + local relay; no web surface found | Missing pair | `/wonderlab` or a later relay-status route | **Missing bridge/status surface**. WonderLab fallback fits experimental voice integration. |
| `mermaids-of-venice` | D | Proposed `giftshop / mermaids` → `/mermaids` | Steering explicitly requires a simple Kind Robots landing page; none found | Missing pair plus landing hero | `/mermaids` | **Missing required landing page/tab**. This is also the first digital-storefront product. |
| `packmaker` | D | Proposed `builder / packs` → `/packs` | Builder-adjacent product; no registered tab/manager found | Missing pair | `/packs` | **Missing front end**. Reuse Builder and shared ACL/content primitives. |
| `coat-dance` | D | Proposed `art / coat-dance` → `/coat-dance` | Creative video-remix project; no project manager/tab found | Missing pair | `/coat-dance` | **Missing creative-project surface**. Art is the best fit. |
| `engagement` | C | Shared engagement primitives across existing surfaces | No evidence this is a standalone destination; treat as cross-cutting system | N/A | `/` or `/conductor` | **Internal shared feature** pending contrary product direction. |
| `wishmaster` | A/D | Existing nested Conductor workspace; proposed canonical `conductor / wishmaster` tab | `WishmasterPage` is rendered by `conductor-manager.vue` when the workspace card key is selected | Project card exists; canonical tab/tutorial pair absent | `/conductor` with Wishmaster selected, or dedicated `/wishmaster` | **Working nested surface, incomplete tab integration**. Reuse the component; do not rebuild it. |
| `challenge-center` | D | Proposed `conductor / challenges` or existing intended Challenge Center workspace | Challenge APIs, schema, project card, and image collection exist; no dedicated Challenge component/render branch was found in the current Conductor manager | Collection art exists; canonical tab/tutorial pair missing | `/conductor` with Challenge Center selected, or `/challenges` | **Partial, not statically verified as a working front end**. Finish the existing intended surface rather than creating a second one. |
| `serendipity` | D | Proposed `scenario / serendipity` → `/serendipity` | Story/chat/task-weaving product; no dedicated registered tab found | Missing pair | `/serendipity` | **Missing front end**. Reuse Stories/Scenario infrastructure. |
| `appmaker` | A/D | Existing nested Conductor workspace; proposed canonical `conductor / appmaker` tab | `AppmakerPage` exists and is rendered from `conductor-manager.vue`; APIs also exist | Project card exists; canonical tab/tutorial pair absent | `/conductor` with AppMaker selected, or dedicated `/appmaker` | **Working nested surface, incomplete tab integration**. Reuse the existing component. |
| `dream-cycle` | C | No public project surface; its creations appear in their owning product surfaces | Autonomous scheduler/automation layer | N/A | `/conductor` | **Internal automation**; no fake tab. |

## Totals

- **8 complete user-facing surfaces:** both Superkate projects, Conductor,
  Digital Storefront, AI Art Academy, Coloring Book, Brainstorm, and Mural Design.
- **5 internal/shared projects with no separate product tab required:** Kind Robots,
  Global UI, Ecosystem Map, Art Generator Connect, Engagement, and Dream Cycle.
  (Kind Robots itself remains reachable at `/`; the count is six when including it as
  both platform and product.)
- **15 missing or incomplete surfaces:** Humboldt Scoop, Humboldt Scoop CMS, Sketchy,
  Storymaker, Da Vinci, Media Watchlist, Conductor App, Alexa Integration, Mermaids of
  Venice, Packmaker, Coat Dance, Wishmaster canonical tab integration, Challenge Center,
  Serendipity, and AppMaker canonical tab integration.

The arithmetic is 29 active projects: 8 complete, 6 internal/platform, 15 incomplete.

## Highest-value implementation order

1. **Finish already-built or partly-built surfaces:** Challenge Center, AppMaker,
   Wishmaster. Their data/components/cards already exist; the work is mostly canonical
   tab registration and correct manager rendering.
2. **Finish explicit product promises:** Mermaids of Venice, Sketchy, Packmaker,
   Storymaker, Serendipity, Da Vinci.
3. **Add external/admin bridges:** Humboldt Scoop, Humboldt Scoop CMS, Conductor App,
   Alexa Integration.
4. **Add creative/support surfaces:** Coat Dance and Media Watchlist.

## Follow-up routing

`ecosystem-map/t-006` owns converting these confirmed gaps into small implementation
work items. Shared tab-framework or manager-switching work belongs in `kind-robots` or
`global-ui`; each project-specific component and copy belongs in the matching project
roadmap. No implementation should land in `ecosystem-map` itself.

Each follow-up must include:

- existing channel and tab key;
- reused component or new manager component;
- tutorial section and image pair;
- route and intended `Dream.liveUrl`;
- a browser verification that selecting the tab renders the intended component rather
  than the channel default.

## Evidence and limits

This was a static GitHub audit of the active roster, Kind Robots dashboard registry,
Conductor manager/card wiring, project steering, and searchable repository paths. It did
not query the production database or run the deployed UI. Rows labeled complete should
still have their `Dream.liveUrl` values verified when t-006 dispatches work; rows marked
partial deliberately avoid claiming that APIs/assets/cards equal a functional page.
