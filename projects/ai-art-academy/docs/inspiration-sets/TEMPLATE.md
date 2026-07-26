# Inspiration Set Template

Copy this file to `docs/inspiration-sets/<slug>-teaching-sequence.md`, fill in every
section, then delete this instructional preamble. Keep the same section headings and
order so sets stay comparable and future tooling (e.g. a style-preview generator) can
parse them consistently. See `everyday-modernity-teaching-sequence.md` for a filled
example.

A set is a small comparison sequence — typically 3-5 images — that reinterprets one
shared source scene through several distinct movements/styles, so learners compare
style decisions rather than subject changes.

---

# <Title> — <N>-Image Teaching Sequence

One or two sentences: what this set is for and what comparison it's designed to teach.

## Shared source scene

Describe one scene in enough detail that every entry can reinterpret it consistently.
State explicitly which elements (figures, objects, camera angle) must stay fixed across
the set so viewers compare style, not subject.

> Scene description as a single prompt-ready paragraph.

## 1. <Movement/Style name> — <short descriptor>

**Teaching goal:** What visual-language lesson this entry demonstrates.

**Prompt:**

> Full generation prompt, referencing the shared scene and movement-level visual cues
> only (no living artists, no copying a specific named work — see
> `PUBLIC-DOMAIN-POLICY.md`).

**Look for:**
- Bullet list of the specific visual signals a learner should notice

**Ethics/agency question:** One question about how the treatment regards its subject —
e.g. does it grant a depicted figure agency, or reduce them to atmosphere/symbol/spectacle?

**Common failure:** The generic or lazy result this prompt tends to produce if the model
defaults to cliché instead of the actual movement-level language.

*(Repeat this numbered section once per entry in the set.)*

## Comparison exercise

A short list of questions asking learners to compare decisions across entries —
depth/space, attention/focal point, treatment of the subject, ethics, and remix fidelity
(which cues survived without reproducing a famous artwork) are good defaults; adapt to
the set's actual teaching goals.

## Generation notes

- Generate all entries with the same source image/crop/seed family where the backend permits.
- Generation metadata checklist — record for each result: prompt, model, seed,
  source-image ID, and any LoRA path/weight.
- Use only movement-level prompts or dead/public-domain artist references allowed by
  `PUBLIC-DOMAIN-POLICY.md`.
- Reject outputs with readable signage, malformed figures, famous-landmark drift, or
  composition changes large enough to undermine comparison.
- This set is educational/internal by default; commercial generation must follow the
  repository's license-clean backend rule.
