# Glyph history sources — licence review (t-030)

Status: review written 2026-09-29; **no source pinned, no data vendored.** Needs Silas's decision.

## Candidates

| Source | Licence | Fit | Concern |
|---|---|---|---|
| Wiktionary "Glyph origin" sections | CC BY-SA 4.0 (text); GFDL dual on older revisions | Best coverage of original meaning and borrowing (e.g. 我 as a pronged weapon, borrowed for "I") | Share-alike: adapted text must carry CC BY-SA. Attribution per entry with a link to the revision. |
| Outlier Linguistics | Commercial, all rights reserved | Highest scholarly quality | Cannot be vendored without written permission. |
| Make Me a Hanzi | Arphic PL / LGPL-style, structural only | Already used in t-029 | Has no historical record; do not extend it to claim one. |
| Unicode Unihan / CJKVI | Unicode licence | Variants only | No origins. |

## The open question

Kind Robots serves card data through its API and UI. Whether displaying Wiktionary-derived glyph text counts as an "adaptation" that makes the served card data CC BY-SA is a legal-interpretation call, and I have not made it. The task says to stop at needs-human with options rather than choose.

The honesty contract in `utils/mandarinLesson.ts` rules out writing these histories from memory, so there is no fallback that skips a source.

## Options

1. **Wiktionary, isolated.** Store `glyphHistory` as a separate, clearly attributed field (source, revision URL, licence badge) and label it CC BY-SA in the UI and API. The rest of the card data stays under its current terms. Cheapest, and the share-alike obligation applies only to that field.
2. **Ask Outlier Linguistics for permission.** Better content, slower, and may carry a fee (spend is a human gate).
3. **Link out only.** Show a "Glyph origin" link to the Wiktionary entry per character, with no vendored text. No licence exposure, but no in-app history.

Recommendation: option 1, after Silas accepts the share-alike scope on that one field. Ingestion should use the Wiktionary dump, not the live API. A live-API probe from this sandbox was rate-limited (HTTP 429) and could not confirm section format.

## Implementation once approved

Add per-character `glyphHistory` (originalMeaning, extendedMeaning, sourceRevision, licence) beside `formations` in kind_robots, and render it on the pieces and meet beats with credit. Ancient-form images only where the individual file licence allows.
