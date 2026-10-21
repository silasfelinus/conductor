# Shifting Desks Narrative Quality Pass II
*2026-10-21 PT · Conductor t-036 · Kind Robots #3994*

## Scope and verification

This is the next editorial pass requested by Silas after the four-office-supply identity correction and t-035. The aim is for the bureaucracy to behave unexpectedly while the player still recognizes their own choice, its failure, and its eventual cost.

All **24 Records & Forms scenes** were inventoried for choice/setup relationships, granted flags, chronology and possible later readers. The implementation concentrates on the strongest six Records scenes and six appropriate Toy Division callbacks, with direct ending evidence for choices whose Toy scene may never be drawn. Existing art and image prompts are unchanged. Mechanics remain 2–4 choices per encounter, 2d6 checks with only 7/9/11 targets, deterministically authored results, and no clean wins.

## Story rewrites and reasons

| Records scene | Earlier issue | Change |
| --- | --- | --- |
| The Tube That Goes Up | Sky and messages are promised, but the destination barely reacts | The guard at the real surface notices the employee, a tomorrow-dated maintenance wrapper becomes proof, and Pip's daring produces an administrative interview rather than a consequence-free dandelion |
| The Suggestion Tube | The player knows anonymity is fraudulent, yet later results do little with that knowledge | The transparent pipe makes handwriting surveillance explicit and Pip's petition remains consequential whether the player sacrifices, impersonates, protects or distracts him |
| Pip at Window 10 | Teaching Pip “no” counted as success even though he immediately approved the applicant anyway | On success Pip actually refuses someone, and a vulnerable applicant pays the price; on failure his new boundary is punished; other options have lasting human and quota consequences |
| Your Permanent Record | “Read about the incident” awarded a clue flag but concealed all details | The Thursday/parking-structure/bear report now reveals enough to matter while preserving who's responsible, and both correction outcomes specifically change what the file alleges |
| The Successor Index | B's personal card did not prepare the player for a later sincerity trial | The note and upcoming focus-group appointment give B his own motive, not just a convenient name for another anonymous test |
| Mail for Kevin | The watch was a lovely prop but not a meaningful piece of Kevin's story | The watch's unusual timing and Tube 14 mark return during the Mr. Sunshine mascot interview; Kevin's get-well card is a collective act with consequences |

A small causal-consistency correction was made before validation: the parents' circle obtains a **new signed copy** of Pip's petition rather than a posted original the player no longer has. The safety memo quotes the incident **from memory** rather than attaching a stolen record. Choices are not allowed to invent possessions.

## Six new Toy Division callbacks

1. **Concerned Parents:** owning the handwriting-traced petition changes who is endangered by the engineers' safety campaign.
2. **The Robot Panel:** a player who taught Pip to refuse can insist that one honest dissent counts, even when the robot loses its chair.
3. **Rate Their Sincerity:** knowing B's personal note lets a player challenge the predestined test, with both exoneration and confiscation outcomes.
4. **Beverly's Union Walkthrough:** the shared-desk agreement becomes an enforceable partnership, not an instantly forgotten modifier.
5. **Mr. Sunshine:** Kevin's four-minute-fast watch reveals that his mascot voice is stored and played separately.
6. **The Safe-Distance Memo:** remembering a dated future incident enables a warning that can be partly preserved or censored.

Every required flag is obtainable in Records before entering Toy Division, and every new check's result is tied to the attempted action. All six routes sit on existing cards that previously had three choices, preserving the maximum of four and reusing their established illustrated scene.

## Twenty-six ending echoes

The ten established ending families receive **26 additional flag-dependent epilogue paragraphs**. They carry consequences of Pip's quota review, the surface tube, successor approval, denied leave, Kevin's mail/watch, B's test, Beverly's solidarity, the parents' petition, the honest robot dissent, and warnings about Thursday's incident. In particular, risk and compassion are not synonyms for a guaranteed happy ending.

These are conditional *paragraphs*, not 26 new finales. A player must both trigger the correct ending family and have performed the relevant act. This keeps the authored branching finite while giving the world a memory independent of the one-in-eight chance of drawing a later scene.

## Outcome and outstanding work

The flag ledger moved from **504 distinct flags, 265 without explicit readers** at the start of this pass to **514 flags, 248 without readers** after the changes. This is not a ratio of good scenes to bad ones. Some one-scene observations and late-floor records are intentionally archival. For a material promise, however, an unread flag is a deliberate follow-up debt.

Next pass candidates: more nuanced Beverly denial and friendship branches (even if her inspection card is not drawn); Kevin's post-Wellness continuity; the suggestion that reaches upstairs; the relationship between the Board's collective voice and the player who kept PAL's secrets. Don't edit Wellness/Sub-Level decks concurrently with existing t-034 tone-ladder work. A final full narrative line-edit remains larger than either t-035 or t-036, and should be tracked honestly rather than declared finished.

## Validation checklist

- Canonical encounter validator, including no-clean-wins, 24-card decks, art_prompt contracts, legal roll targets, and flag-map regeneration
- Conductor Python suite and roadmap/security checks
- Kind Robots gameplay contract regression for all six reachable flags and their later readers, TypeScript and changed-file Prettier
- Exact Records/Toy/ENDINGS parity between canonical content and runtime snapshots, after stamping the final merged Conductor source SHA
- Distinguish merged commit from public production deployment; no new art jobs or irreversible changes

**Signoff condition:** both canonical and runtime PRs must complete their checks before being merged. No evidence of Alexandria deployment is implied by a green GitHub status.
