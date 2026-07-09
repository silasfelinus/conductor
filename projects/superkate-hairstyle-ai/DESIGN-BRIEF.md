# Design Brief — Superkate Hairstyle AI ("Hair Studio")

Status: draft, development underway (scope confirmation runs in parallel as a soft gate)
Slug: `superkate-hairstyle-ai`
Kind: software
Sibling project: [`superkate-services-calculator`](../superkate-services-calculator/) (Hair by Superkate)
Backend: existing Kind Robots Flux **Kontext** Comfy endpoint

## What it is

A new **Hair Studio** tab for Hair by Superkate. Superkate uploads or snaps a photo of a
client, chooses what she wants changed — **color**, **style**, and/or an overall **image
enhance** (any one, any two, or all three) — and the app sends the photo plus a generated
style prompt to the Kind Robots Kontext Comfy backend. It returns the *same client photo*
with the requested new hair, which is saved into that client's gallery as a before/after
pair.

The point is a fast, playful "try it before the scissors" surface Superkate can use chairside:
show a client the color or cut on their *own face* in under a couple of minutes.

## Who it serves

- **Right now:** Superkate only. Single trusted operator, so we do **not** gate hard on
  per-client auth, quotas, or abuse handling yet. (That work is real but deferred to the
  paid/public-launch milestone.)
- **Later (separate gate):** a paid feature behind a free trial + service charge — possibly
  spun into its own app. That decision is Silas's and is human-gated; nothing here commits to it.

**It's a surprise for Superkate.** Keep it out of anything she can see in her current app
build until Silas is ready to reveal it. Don't wire the new tab into a shipped Superkate
release; stage it behind a flag / preview surface until Silas says go.

## Recommended surface (the main scope question for Silas)

The Superkate services app is a **Flutter** app, but building/verifying Flutter is human-gated
in this environment (calculator `t-014`), which repeatedly stalls that roadmap. Meanwhile the
Kontext backend **and** the gallery infrastructure both already live in the **Kind Robots web
app** (Nuxt), which agents *can* build and verify today.

**Recommendation:** ship Hair Studio **first as a web tab in Kind Robots**, calling the
existing `/api/comfy/kontext/generate` endpoint, then bridge it into the Flutter Superkate app
once that toolchain is unblocked. This lets the surprise get fully built and demoable now
instead of waiting behind the Flutter gate. `t-002` asks Silas to confirm or redirect — it is a
**soft** gate; development proceeds on the web-first assumption meanwhile.

## Backend contract (already exists — no backend build required for MVP)

`POST /api/comfy/kontext/generate` (Kind Robots)
- **in:** `imageData` (data URL / base64 of the client photo, **required**), `prompt` (the
  style request), optional `serverId`/`serverName`, sizing, seed, detail params.
- **out:** `data.imageData` (data URL of the transformed image), `promptId`, `filename`,
  and `mana.balance`/`mana.charged`.
- **gated by** `authAndGate({ engine: 'kontext' })` — it charges mana and requires a
  logged-in Kind Robots user. For the Superkate-only phase we run it under Superkate's / the
  studio's account; real per-client billing is the paid-launch milestone.
- Kontext preserves the input image and edits by prompt (`FluxKontextImageScale` +
  `ReferenceLatent`), which is exactly the "same photo, new hair" behavior we want.

There is also `POST /api/comfy/kontext/kombine` (two-image stitch) — out of MVP scope, a
possible later "reference photo" feature (bring a target hairstyle image).

### The transformation controls → prompt builder

Three independent toggles, combined into one Kontext prompt:

- **Change color** → e.g. *"change the hair color to {color}, keep the same cut and length"*
- **Change style** → e.g. *"restyle the hair as {style}, keep the same hair color"*
- **Enhance image** → e.g. *"improve overall photo quality, lighting, and sharpness; keep the
  person's identity, face, and features unchanged"*

Toggling more than one merges the clauses. Every prompt carries an identity-preservation
suffix ("same person, same face, photorealistic") so the client still recognizes themselves.
Free-text refinement is allowed on top of the toggles. The exact prompt templates are `t-003`.

## Async + navigable loading (hard UX requirement)

Kontext runs up to ~180s. The UI must:
- fire the job, show a **loading indicator on the pending result tile**, and
- **stay fully navigable** — Superkate can leave the tab, look at another client, come back,
  and the result lands when ready (poll/await in the background, don't block the app).
Treat each generation as a background job keyed to the client + a pending gallery slot.

## Gallery — yes, we already expect it, and we reuse it

Per-client galleries are already an expectation on the Hair by Superkate side: the calculator
ships **customer profiles** (`customer_profiles.dart`, calculator `t-019`) as the identity
anchor, and Kind Robots already has a mature gallery pattern (`ArtCollection`,
`dream-gallery.vue`, `user-galleries.vue`, per-slug `gallery.json` manifests).

**Decision:** don't invent a new gallery model. Give each Superkate client a
**transformation gallery** that reuses the Kind Robots ArtCollection/gallery pattern, anchored
to the calculator's customer profile as the client identity. Each entry stores the original
photo, the result, the toggles/prompt used, and the mana/prompt metadata (so any result is
traceable and reproducible per AGENTS.md art rules). Whether the gallery record lives in the
KR web data model or bridges back to the Flutter customer profile is a coordination point with
the calculator project (`t-008` + the calculator team) — the identity key is the shared
customer.

## The ChatGPT × Claude collaboration (responsibilities)

Per `AGENTS.md`, this is a standard two-agent software project:

- **ChatGPT (Worker) — builds.** Owns implementation: the Hair Studio tab shell + nav entry,
  image intake (upload + camera capture) with client association, the transform-controls →
  prompt builder, the async background job + navigable loading state, the KR Kontext API client
  (error/timeout/mana handling), and the per-client transformation gallery. One task at a time,
  one PR per task, fills the handoff template, verifies, merges safe reversible PRs.
- **Claude (Reviewer) — reviews & guards the gates.** Reviews each PR against this brief and the
  SPEC, verifies behavior, merges reversible/scoped/software PRs, and **hard-gates** the
  outward-facing / irreversible / monetized steps to `needs-human`: anything touching real
  client billing, the paid/free-trial gating, a public launch, the surprise reveal, deploys,
  secrets, or DNS. Keeps `TALKBACK.md`, files one kaizen task per merge.
- **Silas — steers & unlocks.** Sets direction via `notes_from_silas`, answers the web-vs-Flutter
  scope question (`t-002`), and is the only one who can approve the paid launch, the public
  reveal, or any real-customer/data/billing step.

**Boundary the whole project respects:** the Superkate-only MVP is internal and reversible and
moves fast. Every step toward *charging money*, *going public*, or *touching real client PII at
scale* stops at a human gate — it never auto-fires.

## MVP definition of done (Superkate-only, web-first)

1. A Hair Studio tab exists (staged/flagged, not in a shipped Superkate release).
2. Upload or camera-capture a client photo, tied to a client.
3. Pick any combination of color / style / enhance, with optional free text.
4. Submit → background job → transformed photo returns, app stays navigable, loading shown.
5. Result saved to that client's before/after transformation gallery with prompt metadata.
6. Graceful empty / loading / error / timeout / retry states.

Explicitly **out** of MVP: paid gating, free-trial logic, public signup, multi-operator auth,
the two-image `kombine` reference-photo mode, and any production deploy.
