# Mona Lisa / Salaì Investigation

## Working question

Does the surviving evidence support the claim that Leonardo's **Mona Lisa** incorporates the facial structure of Gian Giacomo Caprotti, known as **Salaì**—whether as the principal model, a secondary reference, or part of an idealized composite?

The project is allowed to strengthen, weaken, or leave the theory unresolved. It is not a hunt for a predetermined match.

## Historical baseline

The project begins from the mainstream identification of the sitter as Lisa Gherardini, wife of Francesco del Giocondo. That case rests on historical documentation and scholarship, including the Heidelberg marginal note and Frank Zöllner's documentary analysis. A visual resemblance experiment cannot erase documentary evidence; it can only investigate whether Leonardo may also have reused or blended features associated with Salaì.

## Candidate hypotheses

1. **Conventional sitter hypothesis** — Lisa del Giocondo was the sitter, with no meaningful Salaì contribution.
2. **Reusable-feature hypothesis** — Leonardo reused favored facial forms across works, including features associated with Salaì, without depicting him as Mona Lisa.
3. **Composite hypothesis** — the painting began from Lisa del Giocondo but evolved into an idealized or composite face that incorporated Salaì-like features.
4. **Principal Salaì-model hypothesis** — Salaì was the principal physical model for the face.
5. **Style-artifact hypothesis** — apparent similarity is mostly Leonardo's recurring construction of eyes, mouth, jaw, sfumato, pose, and expression.

## Why modern face recognition is not enough

Contemporary face-recognition systems are trained mainly on photographs. Paintings introduce artist style, restoration, glazing, pose, non-photographic anatomy, uncertain attribution, and centuries of surface change. A high cosine similarity between two embeddings would therefore be evidence about the model's response to two images—not proof that they portray the same person.

The experiment must first demonstrate that each method can distinguish known same-sitter and different-sitter painted portraits under comparable conditions. It must also test for **same-artist leakage**: a model may recognize Leonardo more strongly than a sitter.

## Proposed evidence stack

### 1. Historiography

Build a source map for Lisa del Giocondo, Salaì, composite, and self-portrait claims. Distinguish contemporary documents, later biographies, scholarly interpretation, journalism, and unsupported internet repetition.

### 2. Provenance-first image dataset

Use the highest-resolution public-domain museum scans available. Candidate material should include:

- Mona Lisa
- Saint John the Baptist
- Bacchus
- drawings or portraits seriously proposed as Salaì
- Leonardo portraits of other sitters
- comparable portraits by contemporaries
- known same-sitter pairs where scholarly identification is strong
- known different-sitter controls

Every image requires source, attribution confidence, date, crop, pose, scan/restoration notes, license, and checksum.

### 3. Interpretable geometry

Use manually reviewed facial landmarks and report ratios or contours that can be inspected by humans. Separate pose-sensitive measurements from approximately stable ones. Preferred language is **facial geometry** or **craniofacial proportion analysis**; "bone analysis" overstates what can be inferred from a painted surface.

### 4. Embedding models

Benchmark multiple open face-embedding models only after painted-portrait validation. Report distributions across preprocessing choices and models, not one confidence percentage.

### 5. 3D-aware secondary analysis

Explore 3D morphable reconstruction cautiously. Generated frontalizations and reconstructed depth are model estimates, not recovered anatomy. Stability across crops, lighting, and pose matters more than a pretty mesh.

### 6. Controls and falsification

Pre-register the primary comparison and success criteria. Include:

- same-artist versus different-artist controls
- unrelated sitters
- shuffled labels
- crop, reflection, pose, and resolution ablations
- multiple models and landmark systems
- permutation tests
- correction for multiple comparisons
- blinded review of overlays where practical

A result that disappears when the mouth is masked, the crop changes, or another model is used is weak evidence.

## Initial source leads

These are starting points for the first research pass, not yet a final bibliography:

- Frank Zöllner, *Leonardo's Portrait of Mona Lisa del Giocondo* — documentary argument for Lisa del Giocondo.
- Heidelberg University Library announcement concerning Agostino Vespucci's 1503 marginal note.
- Lillian F. Schwartz, *Morphing the three faces of Mona* (1995) — an early computer-aided morphing analysis, though it advances a different identity/composite proposal.
- Borkowski, *Mona Lisa: The Enigma of the Smile* (1992) — forensic dental interpretation, useful chiefly as precedent and as a warning about inference from painted anatomy.
- Modern perception research on Mona Lisa's expression, asymmetry, and gaze, which can help identify features especially vulnerable to visual or preprocessing effects.
- Scholarship and museum catalogues concerning Saint John the Baptist, Bacchus, Salaì, and attribution of proposed Salaì portraits.

## Public page shape

The reader-facing page should behave like an open research notebook, not a conspiracy kiosk:

1. The question
2. What historians currently know
3. Why Salaì entered the conversation
4. Side-by-side artwork viewer
5. Methods and controls
6. Results by method
7. Strongest evidence against the theory
8. What remains unknown
9. Full citations, data, code, and change log

The conclusion should be generated from the evidence categories, with separate confidence labels for documentary history, visual similarity, computational results, and interpretation.
