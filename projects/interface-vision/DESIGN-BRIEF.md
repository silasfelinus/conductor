# DESIGN-BRIEF.md — interface-vision

Version: 1.0
Date: 2026-08-01
Status: Draft — aesthetic direction pending Silas's pick (t-002)

---

## What this is

The Kind Robots front end, made coherent. Not a reskin: a **layout contract** that every
page obeys, a **single gallery**, a **single art-request path**, a **single navigation
manifest**, and a **narrator that has somewhere to stand**.

## Who it serves

Two audiences with one interface:

1. **Silas**, daily. His most-used surfaces are the artjob queue, video-gen, newsfeeds,
   and the galleries — especially the Project gallery, which he likes and which is the
   template the rest should follow.
2. **A first-time visitor** who has never heard of karma, mana, dreams, or facets, and
   who needs to understand within one screen that this is a playground of creative tools
   they can use, contribute to, and be credited for.

## The creative direction

Silas's own words: *"a clean, focused interface. Large images, friendly buttons, clean
design. Preferably single screen interfaces that scroll within containers that know where
they need to stay rather than fighting each other, and a straightforward interface that is
modular and open, but has a clear vision."*

He was trained as a theater director with a focus on physical theater. That matters
literally, not decoratively: he thinks in **staging** — who holds focus, what recedes,
where the eye goes, how a body occupies space. The interface should be composed the way a
stage is composed. One thing holds the light at a time.

**The narrator is a performer, not a sidebar.** It currently mounts as
`pointer-events-none absolute inset-y-0 right-0 z-40` — a drawer floating over the page.
It should be a region of the layout with room for a portrait, generated art, and narration
text that reads as narration.

## The three rules

Everything else follows from these.

1. **One header.** The shell already renders the page's icon, hero image, room label and
   title from content frontmatter. A page component never renders a title. If it needs
   controls, it gets one toolbar line. (57 components render their own `<h1>` today;
   Taskmaster shows its own name three times.)
2. **One scroll owner.** A page is handed a correctly-sized box and owns exactly one
   scrolling region inside it. Chrome pins with `shrink-0`; content scrolls with
   `min-h-0 flex-1 overflow-y-auto`. (94 components declare their own `overflow-y-auto`
   today, nested inside a shell that also scrolls.)
3. **Art is never absent.** Every object resolves to an image through a fallback chain.
   Where the data can't supply one, the schema gets the field (t-007) — the galleries are
   data-starved, not merely badly styled.

## MVP shape

Beta-ready means:

- Every page obeys the three rules, verified by `npm run test:layout-contract`.
- Storymaker and Taskmaster have a narrator on a stage, with art.
- All seven core objects (bots, dreams, rewards, facets, projects, characters, scenarios)
  share one gallery with four view modes and one review affordance.
- One art-request path for every object.
- Karma and mana both visible, both correct, with a working `/wallet`.
- A first-launch intro that explains the site and hides afterward.
- A user dashboard where a person can see and change what matters to them.

## Aesthetic direction — PENDING (t-002)

Three mockups of the same Storymaker screen are built in t-001. Silas picks one, or names
the parts he wants from each. **Record the decision here** with the tokens it implies
(surface palette, type pairing, radius, motion), because everything after inherits it.

| | Direction | Character |
|---|---|---|
| A | Theater / lit stage | Dark receding surround, bright lit panel holding narrator + art, chrome dims while a story runs, cinematic contrast |
| B | Storybook | Warm paper tones, generous margins, large rounded image plates, display serif for narration vs clean sans for UI |
| C | Bright playground | Saturated daisyUI brights, chunky friendly buttons, bold cards, playful motion |

> Decision: _pending_
> Tokens implied: _pending_

## What this project is NOT

- Not a rewrite. The tools work; Silas uses them daily. This is about the frame around them.
- Not a `.kr-panel` crusade. Several surfaces are intentionally bespoke (workspace header,
  login page, dashed empty states) and forcing them onto shared classes regresses crafted
  UI — a lesson already paid for in global-ui t-012/t-023.
- Not admin work. Admin routes are explicitly last; several will become user-facing pages
  eventually and shouldn't be polished before they're decided.

## How we know it worked

Progress on this project is reported as **numbers**, not adjectives. Baseline as of
2026-08-01:

| Metric | Baseline | Target |
|---|---|---|
| Files rendering their own `<h1>` | 57 | 0 |
| Files with their own `overflow-y-auto` | 94 | 0 nested |
| Wrappers before page content | 9–10 | ≤5 |
| Content files with >1 MDC block | 4 | 0 |
| Viewport-height hacks outside screenfx | ~45 | 0 |
| Files using any `kr-*` class | 29 / ~421 | contract-compliant, measured by CI |
| Gallery implementations | 7+ | 1 |
| Art-request pipelines | 3 | 1 |
| Navigation taxonomies | 4 | 1 |
| Objects with card+hero art | 3 / 7 | 7 / 7 |
| Karma UI | none | balance, history, ledger-correct |

The last project to own this work (`global-ui`) was closed at 25/25 tasks with the design
system at ~7% adoption, because nobody counted. The counters above exist so that cannot
happen twice.
