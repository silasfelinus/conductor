# engagement — task history archive

Full `note:` prose for completed engagement tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Design and add Referral model to schema

<!-- note:begin t-001 -->
Model already present in kind_robots/prisma/schema.prisma: Referral (id, createdAt, referrerId, referredId unique, codeUsed, cutRate 0.05, Referrer and Referred relations, index on referrerId). User.referralCode @unique also present. signedUpAt covered by createdAt. KarmaTransaction model and KarmaReason enum also confirmed present (REFERRAL_SIGNUP, REFERRAL_CUT among values). Schema-level work is complete; no migration needed here.
<!-- note:end t-001 -->

## t-002 — Add KarmaTransaction model and wire first triggers

<!-- note:begin t-002 -->
All karma infrastructure was already in place: KarmaTransaction model, KarmaReason enum, awardKarma() utility, KARMA_LIVE=false gate, and KARMA_AMOUNTS constants in server/utils/karma.ts. Existing triggers already wired: REACTION_GIVEN (reactions/index.post.ts), CONTENT_CREATED_PUBLIC (prompts/index.post.ts), REFERRAL_SIGNUP (users/register.post.ts). Added missing trigger: REACTION_RECEIVED (content owner awarded when someone reacts to their content) in reactions/index.post.ts via getContentOwnerId() helper. Skips self-reactions (ownerId !== reactor.id). Component model has no userId so returns null for that category. All awards are fire-and-forget; gated by KARMA_LIVE=false until Silas approves rates.
<!-- note:end t-002 -->
