# Pitch: Add Resource.commercialSafe (licensing gate for gallery-to-swag)
date: 2026-07-15
project-target: kind-robots
status: awaiting-silas

## The idea
Add an additive Prisma field to the `Resource` model (kind_robots' LoRA/checkpoint
registry) recording whether the checkpoint/LoRA it represents is licensed for
commercial output: a `commercialSafe Boolean @default(false)` column (or a
`licenseClass` enum — `open` | `restricted` | `unknown` — if a tri-state reads
better against `resourceType`/`supportedServer`'s existing enum style). Seed the
known license-clean backends (FLUX.1 schnell, OpenAI/ChatGPT image gen, approved
licensed APIs like BFL Kontext pro/max) as safe at migration time; every other
existing row defaults to unsafe/unknown. `ArtImage.checkpointResourceId` already
joins to `Resource`, so this is the one join point the self-service "print my
gallery art" flow needs to enforce CONTROL.md's commercial-generation licensing
rule (FLUX.1 dev / Kontext dev / dev-trained LoRAs never touch commercial output).

## Why it's worth doing
Without this field there is no way to answer "was this ArtImage generated on a
commercially-licensed backend?" at the database level — the digital-storefront
project's gallery-to-swag pipeline (docs/gallery-to-swag-pipeline.md §4/§6) has to
fall back to a conservative default-deny (only print images with no checkpoint
override, i.e. `checkpointResourceId IS NULL`), which blocks a real majority of
gallery art from ever being print-eligible even when it was actually generated on
a safe backend. A defaulted-conservative additive column unblocks that without
touching billing, generation routing, or any existing read path — it's pure
metadata that other systems can start gating on immediately once seeded.

## Rough effort
small

## Suggested first task
Additive migration: `ALTER TABLE "Resource" ADD COLUMN "commercialSafe" BOOLEAN
NOT NULL DEFAULT false;` (or the enum variant), update `schema.prisma` and the
generated client, then a one-off seed script that flips `commercialSafe: true`
for rows whose `civitaiUrl`/`huggingUrl`/`localPath`/`generation` fields identify
them as FLUX.1 schnell, OpenAI, or an approved licensed API. No UI work needed
yet — digital-storefront's print-eligibility check is the first consumer and can
land as its own follow-up task once the field exists.
