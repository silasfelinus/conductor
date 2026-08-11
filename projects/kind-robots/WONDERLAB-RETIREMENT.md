# WonderLab retirement directive

Approved by Silas on 2026-08-11.

## Product decision

WonderLab is no longer a Kind Robots product surface or developer subsystem. Remove the museum, component catalog/store/API/build metadata generation, museum-only routes/admin pages, WonderLab-specific component-preview CI, and any build requirement that keeps orphaned components compilable.

`components/abandonware` may stay temporarily as fully excluded source while the live dependency graph is cut. Its intended final home is outside the Kind Robots repository for posterity.

## Preserve the useful work

The 706 polished WonderLab commentary entries are the source corpus for a new first-party review layer on live Kind Robots objects. Do not mutate old Component reactions to point at unrelated targets. Keep the old corpus intact until replacements exist.

Process the corpus in its canonical paired order. For each Bot/Character pair, use the old exchange only as creative evidence for voice and chemistry, then write a fresh two-speaker scene about a real reviewable object. Aim for setup/payoff, recognizable diction, different energy/eloquence, and characters experiencing the target together rather than writing software critique.

## Review-system end state

- Live reviewable models expose `allowReviews` from the selected-item/edit experience.
- First-party authored reactions preserve Bot or Character identity and link back to that speaker.
- User reactions continue to work as user reactions.
- Migrated first-party scenes are drafts until Silas approves publication.
- Old WonderLab Component/ReviewDraft/Reaction data remains available as migration source until the replacement corpus is approved and published; schema deletion is later and separate.

## Human gate

WonderLab infrastructure retirement is approved. Publishing newly generated replacement prose is outward-facing content and remains a human gate.
