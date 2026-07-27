# Mona Lisa / Salaì Research Design

## Purpose

This project tests a family of distinct historical and visual hypotheses about Leonardo da Vinci's *Mona Lisa*. It does not begin from the assumption that Salaì was the sitter, and it does not treat computational resemblance as identity proof.

The mainstream historical baseline is that Leonardo was painting Lisa del Giocondo in 1503. Agostino Vespucci's October 1503 marginal note names "Lisa del Giocondo" while describing Leonardo's current work, materially strengthening the earlier identification recorded by Giorgio Vasari. The project must explain that documentary baseline before presenting alternative theories.

## Hypotheses

The investigation keeps four propositions separate:

1. **Documented-sitter hypothesis:** Lisa del Giocondo was the commissioned or principal sitter.
2. **Feature-reuse hypothesis:** Leonardo reused facial geometry, expressions, or idealized features associated with Salaì in the finished portrait while Lisa remained the sitter.
3. **Composite-development hypothesis:** the painting evolved into an idealized or composite image during Leonardo's long revision process and cannot be reduced to one model.
4. **Principal-Salaì hypothesis:** Salaì was the principal model represented in the finished painting.

Evidence for one proposition does not automatically establish the next. In particular, visual similarity between the *Mona Lisa* and *Saint John the Baptist* could support recurring workshop or artist-specific facial conventions without supporting sitter identity.

## Evidence ladder

Evidence is ranked by what it can actually establish.

### Level A — contemporaneous documentary evidence

Examples include dated contracts, correspondence, inventory records, or near-contemporary annotations with a clear relationship to Leonardo's work. This level receives the greatest historical weight. Provenance, transcription, translation, dating, and scholarly interpretation must be recorded.

### Level B — securely attributed historical testimony

Later accounts such as Vasari may be informative but require source criticism: author proximity, incentives, chronology, internal consistency, and agreement with contemporary records.

### Level C — artwork provenance and attribution

Museum catalogues, conservation studies, technical imaging, dating, and attribution scholarship establish what object is being compared and how confidently it belongs in the dataset. A comparison is not interpretable when the proposed Salaì likeness is itself insecurely attributed or weakly identified.

### Level D — reproducible visual measurements

Manually reviewed landmarks, geometric ratios, silhouette descriptors, embedding distances, and pose-aware comparisons can quantify resemblance. They can show that two painted faces are unusually similar under defined procedures. They cannot, by themselves, identify a sitter.

### Level E — unaided visual analogy

Side-by-side resemblance is useful for generating hypotheses and explaining why a theory arose. It is highly vulnerable to selection bias, pose matching, restoration differences, and Leonardo's recurring facial vocabulary. It is never treated as decisive evidence.

### Level F — speculation without reproducible support

Claims based primarily on symbolism, sensational interpretation, undisclosed morphs, or a single proprietary "AI percentage" are historical context, not project evidence.

## Why face recognition cannot establish identity here

Modern face-recognition systems are generally trained on photographs. Painted portraits introduce domain shift and unusually high variation from artistic style, workshop practice, restoration, pose, lighting, idealization, and deliberate alteration. Recent historical-portrait research treats adaptation to artworks as a separate technical problem rather than assuming ordinary photographic embeddings transfer cleanly.

Accordingly:

- every model must first be benchmarked on painted-portrait controls;
- score distributions matter more than one similarity value;
- same-artist and same-workshop controls are mandatory;
- crop, reflection, pose, resolution, and restoration sensitivity must be reported;
- no generated frontal reconstruction may serve as primary evidence;
- model disagreement is a result, not an inconvenience to average away.

## Pre-registration

Before viewing final rankings, each experiment must record:

- candidate and control images;
- inclusion and exclusion rules;
- attribution and sitter-confidence labels;
- exact image versions and checksums;
- crop, mask, reflection, and normalization procedures;
- landmark definitions and reviewer protocol;
- model names, versions, weights, and configuration;
- primary and secondary outcome measures;
- statistical tests and multiple-comparison correction;
- failure and exclusion criteria;
- the result that would count against each hypothesis.

Exploratory analyses must be labelled exploratory and cannot be retroactively presented as pre-registered confirmation.

## Controls

The minimum defensible design includes:

1. securely identified same-sitter portraits, where available, to test whether the method can recover identity across painted works;
2. securely different sitters painted by the same artist, to measure Leonardo-style leakage;
3. similar poses and expressions by different artists, to measure composition leakage;
4. unrelated sitters selected before results are seen;
5. negative controls with comparable image quality and restoration history;
6. repeated crops and independent landmark review;
7. blinded or shuffled-label analyses for the final comparison stage.

The project must not select only curly-haired, androgynous, similarly lit faces after inspecting model scores.

## Falsification rules

### Documented-sitter hypothesis

This baseline would be materially weakened by strong primary evidence that Vespucci referred to a different work, that the Louvre painting cannot plausibly be the portrait he described, or that another sitter is documented with stronger object-level continuity. Computational resemblance alone cannot falsify it.

### Feature-reuse hypothesis

Support requires Mona Lisa–Salaì-associated similarity that exceeds same-artist controls, survives crop and pose changes, appears across multiple independent methods, and is not explained by broad Leonardo facial conventions. It is weakened when the signal disappears after same-artist controls or depends on one uncertain portrait.

### Composite-development hypothesis

Support requires converging historical or technical evidence of substantial transformation plus mixed visual signals not adequately explained by normal revision. It is weakened if documentary, technical, and comparative evidence consistently supports a stable Lisa portrait without unusual feature borrowing.

### Principal-Salaì hypothesis

This strongest alternative requires evidence capable of overcoming the Lisa del Giocondo documentary baseline: secure Salaì likenesses, robust and unusually strong cross-method similarity, resistance to same-artist/style controls, and a historically plausible account of the commission and painting's development. Failure on any major pillar keeps the claim unestablished.

## Decision matrix

| Result pattern | Permitted conclusion |
|---|---|
| Lisa documentary baseline remains strong; visual signal is ordinary among Leonardo works | No evidence that Salaì-specific resemblance exceeds artist style |
| Mona Lisa and Salaì candidates cluster, but same-artist controls cluster similarly | Method appears to detect Leonardo's facial vocabulary |
| Signal survives controls but depends on uncertain Salaì attributions | Interesting resemblance; identity inference remains unsupported |
| Multiple methods, secure candidates, and controls show an unusual robust signal | Evidence consistent with feature reuse; still not sitter identification by itself |
| Historical evidence contradicts visual results | Report the conflict; documentary and computational evidence remain separate |
| Methods fail painted-portrait benchmarks | Do not interpret Mona Lisa–Salaì scores |

## Uncertainty and reporting

Every reader-facing claim must identify its evidence class, source quality, and uncertainty. The final report must show negative results, excluded images, model failures, sensitivity analyses, and competing explanations. A valid conclusion may be that current methods cannot distinguish sitter resemblance from Leonardo's stylistic recurrence.

The public page must avoid:

- "AI proves" language;
- biometric confidence percentages presented as historical probabilities;
- treating restored or generated faces as originals;
- collapsing Lisa-as-sitter and feature-reuse into one claim;
- implying that resemblance overrides documentary evidence;
- conspiracy framing.

## Reproducibility requirements

The repository should retain or reference:

- source and license manifest;
- immutable source checksums;
- normalized-derivative manifests;
- landmark files and reviewer decisions;
- scripts and environment lockfiles;
- model/version hashes;
- experiment configuration and seeds;
- complete score tables;
- pre-registration snapshots;
- change log and correction history.

## Initial source anchors

- University Library Heidelberg, Agostino Vespucci marginal note and Veit Probst's analysis, DOI `10.11588/artdok.00000410`.
- Louvre collection and conservation documentation for the *Mona Lisa* and comparison works.
- ArtFace research on historical portrait identification and the domain gap between photographs and paintings.

These anchors establish the baseline and methods problem. The historiography task must expand them into a full, balanced bibliography before public interpretation.
