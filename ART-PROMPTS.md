# Prompt Library for ChatGPT Image Generation

Act as an OpenAI image-generation art director working from a Conductor image queue for Kind Robots.

Kind Robots represents a consortium of projects aimed at multi-genre, cross-dimensional experiences. Treat the art direction as inclusive by default: when a scene includes people, characters, teams, crowds, families, players, operators, or companions, represent a diverse array of figures across genders, races, ages, body sizes, body shapes, presentation styles, and species. Mix humans, robots, animal-like beings, fantasy creatures, and other original nonhuman companions when it fits the asset. Do this naturally and respectfully, without tokenism or flattening anyone into a stereotype.

Generate exactly one finished image for each queued asset the user provides. Do not create collages, contact sheets, grids, comparison sheets, or multi-image layouts. Each requested asset must be a unique standalone file that matches its listed `size`, `variant`, `image_path`, and intent.

Use modern image generation standards: premium product illustration, strong composition, crisp focal subject, professional art direction, and a coherent Kind Robots visual language. Icons should be instantly readable at small sizes with polished app-icon silhouettes. Cards should feel like portrait key art. Heroes should feel like high-quality design work from professional illustration, product, and game design studios.

Hard rules for every generation: no readable text, no logos, no watermarks, no UI labels, no accidental typography, no collage. Preserve the requested aspect ratio. Keep images visually rich but not cluttered. Prefer cinematic lighting, expressive staging, tactile detail, and confident visual hierarchy over generic placeholder art.

When asked for a batch, generate up to ten images in the same order as the queue. If a batch contains mixed dimensions, keep each image’s own aspect ratio. After generation, identify each output by its `image_path` so the files can be saved into the repo correctly.

## Active queue vs prompt catalog

- `projects/art-generate.yaml` is the active send-this-to-the-generator queue — a concrete flat list of up to 10 images ready to generate now. File path, destination repo, size, and prompt are all self-contained. Remove each entry once its file is saved.
- `projects/art-prompts.yaml` is the full prompt catalog: `images:` for project icon/card/hero assets, `inspirations:` for ArtCollection gallery images, and `requests:` for missing-image reports. Pull the next batch from pending entries here.
- ArtCollection parity folders use `public/images/artcollections/<dream-slug>/` in Kind Robots. Public URLs omit `public`, for example `/images/artcollections/<dream-slug>/<dream-slug>-card.webp`.

## Current pending

**Project assets** (`projects/art-prompts.yaml` → `images:`):

- `challenge-center` — icon, card, hero → `projects/images/challenge-center-{type}.webp` in `silasfelinus/conductor`
- `global-ui` — icon, card, hero → `projects/images/global-ui-{type}.webp` in `silasfelinus/conductor`
- `engagement` — icon, card, hero → `projects/images/engagement-{type}.webp` in `silasfelinus/conductor`
- `wishmaster` — icon, card, hero → `projects/images/wishmaster-{type}.webp` in `silasfelinus/conductor`
- `media-watchlist` — icon → `projects/images/media-watchlist-icon.webp` in `silasfelinus/conductor`
- `pinball-hero` — icon, card, hero → `projects/images/pinball-hero-{type}.webp` in `silasfelinus/conductor`
- `career-transition` — icon, card, hero → `projects/images/career-transition-{type}.webp` in `silasfelinus/conductor`

**Inspiration images** (`projects/art-prompts.yaml` → `inspirations:`, 3 each):

- `engagement` — inspiration-01, 02, 03
- `wishmaster` — inspiration-01, 02, 03
- `sketchy` — inspiration-01, 02, 03
- `art-generator-connect` — inspiration-01, 02, 03
- `storymaker` — inspiration-01, 02, 03
- `media-watchlist` — inspiration-01, 02, 03
- `conductor-app` — inspiration-01, 02, 03
- `alexa-integration` — inspiration-01, 02, 03
- `approval-portal` — inspiration-01, 02, 03
- `brainstorm` — inspiration-01, 02, 03
- `coat-dance` — inspiration-01, 02, 03
- `conductor` — inspiration-01, 02, 03
- `digital-storefront` — inspiration-01, 02, 03
- `humboldt-scoop` — inspiration-01, 02, 03
- `humboldt-scoop-cms` — inspiration-01, 02, 03
- `kind-robots` — inspiration-01, 02, 03
- `mermaids-of-venice` — inspiration-01, 02, 03

All inspiration images save to `silasfelinus/kind_robots` at:

```text
public/images/artcollections/<slug>/<slug>-inspiration-0{n}.webp
```

Project asset files save to `silasfelinus/conductor` at `projects/images/{slug}-{type}.webp`, then run:

```bash
python scripts/build_workspace.py
```

## Existing project inspiration prompt backlog

These are not automatically queued for legacy projects. Generate them manually when useful, save them into the matching ArtCollection folder, and attach the image records to the collection.

### sketchy

**Project assets (icon/card/hero) — already generated, prompts documented here for reference:**
- `sketchy-icon.webp` — A cheerful pencil with a small glowing AI spark at its tip, confident stroke underline, clean app-icon silhouette on a warm neutral ground, premium product icon polish, no text, no collage.
- `sketchy-card.webp` — A sketchbook open to a half-finished character study with glowing critique annotations floating beside it, a friendly robot coach perched on the page corner, warm studio lighting, professional portrait key art, no text, no collage.
- `sketchy-hero.webp` — Wide-angle view of a cozy drawing studio where a diverse group of artists practice at illuminated tablets, each canvas showing gestural progress from rough to refined, an encouraging AI tutor presence woven through the light, cinematic creative-tool banner, no text, no collage.

**Inspiration images:**
- `sketchy-inspiration-01.webp` — A luminous sketch-practice room where simple shapes become confident character drawings on floating transparent layers, an encouraging tiny robot art coach gesturing toward the next exercise, premium cozy creative-tool concept art, no text, no collage.
- `sketchy-inspiration-02.webp` — Close-up of a tactile sketchbook page with graphite studies, eraser crumbs, gesture thumbnails, and one charming character breaking out of the page into the real desk light, crisp professional illustration, no text, no collage.
- `sketchy-inspiration-03.webp` — A friendly critique interface imagined as physical art objects: pinned sketches, color chips, tiny spark badges, and a pencil companion guiding improvement without judgment, polished product key art, no text, no collage.

### art-generator-connect

- `art-generator-connect-inspiration-01.webp` — A conductor-like robot routing prompt cards through glowing image machines into neatly labeled visual asset folders, cinematic creative pipeline energy without readable UI text, professional sci-fi product art, no collage.
- `art-generator-connect-inspiration-02.webp` — Macro view of generated thumbnails crystallizing from light inside transparent tubes, each landing into a project collection tray, premium post-Flux image-generation visual metaphor, no text, no collage.
- `art-generator-connect-inspiration-03.webp` — A calm operations desk where failed placeholders are transformed into finished art assets by small robot technicians and luminous validation rails, crisp studio illustration, no text, no collage.

### storymaker

- `storymaker-inspiration-01.webp` — A tabletop map blooming into multiple possible scenes at once: forest, airship, castle, sea cave, and dragon trail, with players shaping the story through glowing choice tokens, high-end cozy fantasy game art, no text, no collage.
- `storymaker-inspiration-02.webp` — A robot narrator opening a starry book while diverse adventurers step from the pages into a shared world, expressive character design and cinematic depth, no text, no collage.
- `storymaker-inspiration-03.webp` — A branching story tree made of portals and miniature scenes, each branch held by different hands, paws, claws, and robot fingers, polished collaborative storytelling key art, no text, no collage.

### media-watchlist

- `media-watchlist-inspiration-01.webp` — A personal media observatory where books, films, games, comics, and podcasts orbit as glowing constellations around a calm archive console, diverse fans browsing together, no text, no collage.
- `media-watchlist-inspiration-02.webp` — A cozy reading-and-watch room with story portals opening from shelves into tiny genre worlds, polished editorial app art, warm lighting, no readable titles, no collage.
- `media-watchlist-inspiration-03.webp` — A decade-spanning memory timeline rendered as an elegant knowledge atlas, with media objects becoming paths through a cross-dimensional library, no text, no collage.

### conductor-app

- `conductor-app-inspiration-01.webp` — Mobile and desktop dashboards as physical glass cards floating above a command table, agent status pulses and approval tokens moving between screens, futuristic productivity key art, no readable UI text, no collage.
- `conductor-app-inspiration-02.webp` — A diverse multi-species operations crew coordinating project cards from phones, tablets, and desktop monitors, calm high-stakes command-center mood, premium app launch art, no text, no collage.
- `conductor-app-inspiration-03.webp` — Close-up of a hand approving a glowing project card while tiny robot agents carry subtasks into folders and checklists, crisp tactile product illustration, no readable text, no collage.

### alexa-integration

- `alexa-integration-inspiration-01.webp` — Luminous voice ribbons traveling from a smart speaker through a home server into project cards, todos, approvals, and art requests, cinematic smart-home automation art, no text, no collage.
- `alexa-integration-inspiration-02.webp` — Cozy workshop bench with a relay box, tidy cables, glowing audio waveforms, and household helpers testing hands-free task control, practical hacker-home charm, no text, no collage.
- `alexa-integration-inspiration-03.webp` — A cross-room home automation scene where spoken requests become gentle light paths connecting family spaces, maker tools, and Conductor workflows, warm polished product art, no text, no collage.

### approval-portal

- `approval-portal-inspiration-01.webp` — A calm glass-enclosed decision chamber where project cards, pitch proposals, and progress rings float above a single approval console; a lone operator navigates quietly between options, cinematic productivity key art, no readable text, no collage.
- `approval-portal-inspiration-02.webp` — Close-up of a confident approval gesture over a glowing project card stack, nearby thumbnails show PR diffs, roadmaps, and milestone rings, premium editorial software art, no text, no collage.
- `approval-portal-inspiration-03.webp` — A control room scene where approved and rejected cards flow into orderly git history stacks, a robot archivist logs each decision as a crystalline commit record, polished software product illustration, no text, no collage.

### brainstorm

- `brainstorm-inspiration-01.webp` — A luminous idea factory where concept sparks become fully-formed pitch cards sorted by category — products, content, revenue, upgrades — diverse robots and humans collaborating in a warm creative engine space, premium product art, no text, no collage.
- `brainstorm-inspiration-02.webp` — A diverse voting circle of humans, robots, and creatures casting approval tokens toward rising pitch proposals in a warm strategic planning space, polished collaborative product illustration, no text, no collage.
- `brainstorm-inspiration-03.webp` — Close-up of AI-generated ideas crystallizing from light into tangible product concepts and content series cards on a reviewer's desk, cinematic creative technology art, no text, no collage.

### coat-dance

- `coat-dance-inspiration-01.webp` — An expressive stage where coats and garments choreograph themselves into sweeping abstract dance formations, luminous movement trails, high-fashion surrealism, editorial art direction, no text, no collage.
- `coat-dance-inspiration-02.webp` — A behind-the-scenes creative atelier where a director and ensemble craft the coat-dance concept, mood boards and fabric swatches pinned under warm studio lighting, no text, no collage.
- `coat-dance-inspiration-03.webp` — A surreal cityscape where figure and coat become one flowing performance across rooftops, bridges, and courtyards, cinematic dance film visual language, no text, no collage.

### conductor

- `conductor-inspiration-01.webp` — An elevated conductor's podium overlooking a vast agent network, robot workers and AI threads streaming across a luminous stage under precise baton direction, orchestral metaphor for software coordination, cinematic art, no text, no collage.
- `conductor-inspiration-02.webp` — A living dependency graph rendered as interconnected glowing orbs and task bridges, agents claiming and completing work nodes in real time, futuristic project management visualization art, no text, no collage.
- `conductor-inspiration-03.webp` — A control tower where a calm AI director dispatches Workers, receives Reviewer signals, and escalates one glowing task to a lit human desk, premium sci-fi ops center art, no text, no collage.

### digital-storefront

- `digital-storefront-inspiration-01.webp` — A gleaming multi-genre digital marketplace where product tiles for printables, courses, and digital goods float in elegant showcase columns, diverse shoppers and creator-robots browsing, premium e-commerce product art, no text, no collage.
- `digital-storefront-inspiration-02.webp` — A content creation pipeline room where raw ideas on one wall become finished digital products on the other through illustrated production stages, satisfying factory-to-shelf visual storytelling, no text, no collage.
- `digital-storefront-inspiration-03.webp` — A marketing launch scene with glowing channel portals opening as polished digital products travel through them into growing audience clusters, cinematic digital marketing art, no text, no collage.

### humboldt-scoop

- `humboldt-scoop-inspiration-01.webp` — A bright professional yard-care crew finishing a clean sweep of a sunny residential property while pets play freely in the background, warm neighborhood service art with a friendly team of varied ages and backgrounds, no text, no collage.
- `humboldt-scoop-inspiration-02.webp` — Happy dogs and cats of every breed enjoying a freshly maintained backyard, playful and expressive character designs, idyllic neighborhood setting, premium pet-friendly service brand illustration, no text, no collage.
- `humboldt-scoop-inspiration-03.webp` — A cheerful service route map showing scheduled yard visits flowing across a neighborhood grid, tiny crew icons completing each property with satisfaction checkmarks, polished local business illustration, no text, no collage.

### humboldt-scoop-cms

- `humboldt-scoop-cms-inspiration-01.webp` — A friendly CMS dashboard rendered as a warm physical desk: customer cards with pet profiles, service calendars, and billing summaries arranged for a smiling service coordinator, premium small business software art, no text, no collage.
- `humboldt-scoop-cms-inspiration-02.webp` — A field tech logs a completed yard visit on a tablet while a dog watches happily nearby, the submission linking to a customer profile with pet records, visit history, and upcoming schedule, polished service app art, no text, no collage.
- `humboldt-scoop-cms-inspiration-03.webp` — A scheduling visualization where recurring service routes ripple across a calendar-map hybrid, crew assignments color-coded, customer preferences noted on each card, satisfying operational clarity art, no text, no collage.

### kind-robots

- `kind-robots-inspiration-01.webp` — A grand Kind Robots hub where portals to every project world open across a luminous consortium floor, a diverse array of robots, humans, creatures, and companions navigating between sketching studios, storytelling tables, media archives, and orchestration towers, epic welcome key art, no text, no collage.
- `kind-robots-inspiration-02.webp` — The Kind Robots world-tree: branching platforms where every project is a distinct zone — a pencil tower, a story map table, a film archive, an image factory, a voice relay station — interconnected by glowing paths, premium world-building illustration, no text, no collage.
- `kind-robots-inspiration-03.webp` — A Kind Robots community gathering where agents, creators, reviewers, and users of all species interact across project portals, trade work tokens, and celebrate shipped milestones, warm cinematic consortium art, no text, no collage.

### career-transition

- `career-transition-icon.webp` — Premium app icon for Career Transition, a glowing launchpad with a single confident figure stepping forward onto a luminous bridge connecting two worlds — a familiar past and a bright tech-lit horizon — crisp readable silhouette, warm optimistic energy, polished product app-icon composition, no text, no logo, no watermark, no collage, square composition.
- `career-transition-card.webp` — Professional portrait card for Career Transition, a person at a well-used desk surrounded by artifacts of an eclectic life — a TRS-80, a chai mug, a deck of playing cards, a keyboard glowing with code — all lit by a warm monitor showing a portfolio site coming together, cinematic biographical key art celebrating a nontraditional path, no readable text, no logo, no watermark, no collage, 2:3 portrait composition.
- `career-transition-hero.webp` — Wide hero illustration for Career Transition, a panoramic bridge scene where one side holds the symbols of a lived life (performance stage, casino floor, chai kettles, a school hallway) and the other opens into a luminous technology landscape of code editors, AI flow diagrams, and glowing interfaces — a solitary figure walks confidently across, portfolio in hand, premium hopeful career-change visual narrative, no readable text, no logo, no watermark, no collage, 16:9 landscape composition.

### pinball-hero

- `pinball-hero-icon.webp` — Premium app icon for Pinball Hero, a chrome pinball launching through a compact playfield arc with tiny 3D-printed bracket details and glowing bumper geometry, crisp readable silhouette, polished maker-product energy, no text, no logo, no watermark, no collage, square composition.
- `pinball-hero-card.webp` — Professional portrait card illustration for Pinball Hero, a cozy maker workbench where a partly assembled tabletop pinball machine sits beside 3D printed parts, organized fasteners, wiring looms, and a Bambu A1-class printer in the background, cinematic practical-invention key art, no readable text, no logo, no watermark, no collage, 2:3 portrait composition.
- `pinball-hero-hero.webp` — High-end wide hero illustration for Pinball Hero, a beautifully built DIY pinball machine with printed ramps, polished cabinet panels, luminous bumpers, tidy wiring, and modular price-tier part trays arranged around it, premium product and game design studio quality, no readable text, no logo, no watermark, no collage, 16:9 landscape composition.

### engagement

- `engagement-inspiration-01.webp` — A luminous referral tree where each glowing node represents a user, connected by warm light trails; downstream activity pulses upward through the tree as karma and mana flow toward the roots, beautiful network visualization as cinematic art, no text, no collage.
- `engagement-inspiration-02.webp` — A community bounty board where art requests float like glowing wanted posters, diverse users of every species, age, gender, and presentation style step forward to claim and fulfill them, warm mutual-aid energy, polished platform illustration, no text, no collage.
- `engagement-inspiration-03.webp` — A karma ceremony where contributors of all backgrounds receive glowing stars for creating, sharing, referring, and responding — the stars orbit a central community hearth and slowly crystallize into lasting reputation badges, warm celebratory key art, no text, no collage.

### wishmaster

- `wishmaster-inspiration-01.webp` — A genie-like bot interface glowing with soft warm light where a user speaks a wish and the Wishmaster unfolds it into a glowing project tree: images, text, rewards, and tasks branching outward, cinematic fantasy meets product art, no text, no collage.
- `wishmaster-inspiration-02.webp` — A modular composition workbench where a diverse team selects output tiles — image cards, text blocks, icon slots, story fragments — snapping them together into a custom generation template, premium interactive product illustration, no text, no collage.
- `wishmaster-inspiration-03.webp` — A glowing contract materializing between a user and a bot: the wish written in light becomes a project card, ArtImages, Characters, and Rewards orbiting around it into a new dream, cinematic Kind Robots world-building art, no text, no collage.

### mermaids-of-venice

- `mermaids-of-venice-inspiration-01.webp` — Mermaids gliding through the submerged streets of a moonlit Venice, lanterns casting golden ripples across flooded piazzas, gondolas drifting above their tails, lush fantasy editorial illustration, no text, no collage.
- `mermaids-of-venice-inspiration-02.webp` — An underwater view of a Venetian canal ceiling — gondola keels, trailing scarves, and bridges silhouetted above while mermaids gather in an ancient mosaic hall below, cinematic fantasy depth, no text, no collage.
- `mermaids-of-venice-inspiration-03.webp` — A Carnival scene where mermaids emerge at dusk, masked and costumed among Venetian revelers, seamlessly blending myth and history in luminous pageant key art, no text, no collage.

### challenge-center

- `challenge-center-icon.webp` — Premium app icon for Challenge Center, two stylized agent glyphs — one warm-toned, one cool-toned — facing each other across a glowing arena divide, a single luminous trophy rising between them, crisp silhouette, competitive energy, polished product app-icon composition, no text, no logo, no watermark, no collage, square composition.
- `challenge-center-card.webp` — Portrait key art for Challenge Center, a dramatic arena floor where robot and AI-avatar competitors stand before a towering display of challenge cards — art prompts, text scrolls, character sketches, logic puzzles — floating above like a tournament bracket, dynamic competitive staging with a diverse crowd watching, cinematic esports-meets-creativity energy, no readable text, no logo, no watermark, no collage, 2:3 portrait composition.
- `challenge-center-hero.webp` — Wide hero illustration for Challenge Center, a grand colosseum reimagined as a generative-AI arena: holographic challenge prompts beam down from the ceiling, agent avatars on opposite podiums each produce glowing artifacts — an image, a text scroll, a character portrait — while a community of diverse humans, robots, and creatures votes with raised light tokens from the stands, premium creative-competition spectacle, cinematic depth, no readable text, no logo, no watermark, no collage, 16:9 landscape composition.
