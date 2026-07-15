# Pitch: Add ArtImage.storefrontFeatured (curated swag rail)
date: 2026-07-15
project-target: kind-robots
status: awaiting-silas

## The idea
Add a way to mark specific `ArtImage` rows in kind_robots as curated for the
digital-storefront swag rail — pieces Silas specifically wants sold as prints,
independent of the general self-service "print my gallery art" flow. Two shapes
work: the simplest is an additive `ArtImage.storefrontFeatured Boolean
@default(false)` column; the richer option is a small join table
(`StorefrontFeaturedArt { artImageId, sortOrder, addedAt }`) if curation
ordering on the rail matters later. Either way this is additive-only — no
existing `ArtImage` behavior changes.

## Why it's worth doing
The storefront's swag rail (docs/gallery-to-swag-pipeline.md §5) needs to say
"these ArtImage rows are the ones we sell, regardless of the automatic
self-service flow" — separate from the KR-logo item (which is a static asset,
not an ArtImage, and doesn't need this at all). Without this field the
digital-storefront project has no durable, queryable way to curate a featured
set; the doc's fallback (a flat allow-list of `artImageId`s in this project's
own `docs/`) works as a stand-in but drifts from the real gallery data and
can't be managed from any kind_robots admin surface.

## Rough effort
small

## Suggested first task
Additive migration: `ALTER TABLE "ArtImage" ADD COLUMN "storefrontFeatured"
BOOLEAN NOT NULL DEFAULT false;` (boolean variant), update `schema.prisma` and
the generated client. If sort-order curation is wanted from day one, use the
join-table variant instead: `CREATE TABLE "StorefrontFeaturedArt" (artImageId,
sortOrder, addedAt)` with a foreign key to `ArtImage`. No UI needed yet —
digital-storefront's swag-rail query is the first consumer and can land as its
own follow-up task once the field/table exists.
