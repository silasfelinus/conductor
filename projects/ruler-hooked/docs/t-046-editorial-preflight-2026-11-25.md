# Ruler Hooked t-046: editorial preflight

2026-11-25 PT. Source snapshot: [Kind Robots 160baa84](https://github.com/silasfelinus/kind_robots/tree/160baa8482ff7b091756af0a266ed50ecbe46490).
This is the independent inventory and authored editorial pass requested while t-045 is in review. t-046 remains waiting on t-045; no claim, dependency bypass, completion, playthrough or rendered-art assertion. Reconcile pending [#5818](https://github.com/silasfelinus/kind_robots/pull/5818) before the final pass.

## Findings and implementation acceptance

| Severity | Source | Finding and proposed repair |
| --- | --- | --- |
| High | `content.ts`: elope-defiance/relent, wedding-reckoning, marina-family-charter | Relenting explicitly returns the married couple, but only the initial blessing records blessedMatch and the wedding petition requires elope-blessing. A genuine reconciliation therefore loses the later home and harbour arc. Set a distinct weddingCompleted flag on welcome and relent; allow both witnessed paths (including legacy saves via an appropriate migration or predicate) without giving the permanent estrangement route a wedding. |
| High | `applyEffects.ts`: resolveChoice; `select.ts`: eligiblePool | A defer choice with requeue=true still records the card as seen, making once-only cards unavailable forever. Separate resolved from deferred state: log deferral, but do not retire the card or unlock its resolved-card prerequisites. Apply a bounded cooldown so fishing remains possible. Test every authored defer, including Nix and the original north woods question. |
| High | `content.ts`: endings; `ruler-hooked-court-screen.vue` | The grove promises every fish twice without a collection prerequisite. Accepted finales show title and art but omit the body. Replace unsupported claims and retain full epilogue after acceptance and reload, not only in the offer. |
| Medium | `loop.ts`: eligibleEnding | Array order prioritizes metropolis when prosperity >=80 even when empire also qualifies. Do not silently change ending precedence; decide whether a choice of eligible finales is appropriate and prove all four legal witnesses under the actual store's cardsResolved rule. |
| Medium | `content.ts`: rival-angler, rival-angler-2, brack-trial, mossy-price and other counters | Authored dialogue increments/decrements fishCaught without Fishopedia specimens (Brack's catch even counts as yours). Separate actual landed specimens from narrated fishing, e.g. narratedCatches and fishGifted; preserve older saves and audit the secret ending, achievements, and any gates relying on that counter. |
| Medium | `advisor.ts`: currentAdvisorLine | Secret endings fall through to the generic mixed-reign warning; catch text claims a trophy cannot happen twice. Give the secret ending its own voice and remove unsupported rarity claims. |
| Low | `content.ts`: rival-angler/accept | “As kings do” ignores the selected honorific. Use gender-neutral copy. |

## Authored replacements (implementation-ready)

Retain stable outcome keys, art keys and thresholds in the editorial-only change. The following is the full replacement ending body for each existing key, not additional endings.

### druid-utopia — The Angler’s Grove

At the old millrace, the wheel turns slowly enough for the fish to pass. Sela runs the tree nursery, and Vex sells picnic baskets from a stall built entirely of salvaged timber. He insists the profit margin is excellent.

There are fewer grand projects and more mornings when nobody needs to ask the crown for permission. The lake has become a place people inherit together, rather than a possession passed from one ruler to the next.

Quill sets the last ledger beside your tackle box. “No emergency today. I checked twice.”

### warlock-metropolis — Boomtown by the Lake

The barges unload through the night. On the far shore, windows shine where the woods once stood. There is work for families who used to leave in winter, and a rent notice for some who can no longer afford to stay.

Vex brings you a commemorative model of the new skyline. Sela brings a jar of lake water. Neither asks you to choose between them this time.

Quill opens the accounts. “We have built a remarkable kingdom. We should remember what it cost.”

### thistlewood-empire — The Thistlewood Empire

Foreign banners rise above the ferry landing. Ships arrive with spices, tools and fish nobody in the village has learned to cook. Gristle has hired three assistants and still does his own arithmetic.

Thistle sends her last dispatch by ordinary post, without an armed escort. It contains a trade agreement and a request for a quiet week at the lake.

Quill removes a seal from the final ledger. “We can pay our debts. Now comes the harder question: what are we going to do with our freedom?”

### fishers-peace — The Ruler Who Never Ruled

The villagers have learned to settle small matters without a decree. The market committee argues over the price of bait, the fishers repair their own nets, and the crown is consulted principally when someone needs a signature.

Quill comes down the steps carrying two rods instead of a ledger. “They have asked for fewer meetings,” he says. “I believe we can accommodate them.”

The day passes without a single trumpet. There is still a kingdom behind you, and there is still a lake ahead.

### Existing-scene copy

- **elope-defiance / relent:** “Robin arrives first, carrying two battered rods. Ash follows with a bundle of wedding gifts returned by the court. You apologize without a speech. Robin takes your hand for a moment, then asks where the perch are biting.” The healed relationship must actually unlock the later home petition.
- **elope-defiance / stew:** “Their room remains empty. Quill forwards their letters without opening them. They are building a life somewhere beyond your orders; the dock feels larger than it used to.” Do not imply the couple stopped existing.
- **rival-angler / accept:** “You win by a whisker. The noble insists the scales were biased. You offer to let the fish adjudicate.”
- **brack-trial / grant-trial:** “Brack lands a perch the size of a footstool and walks free. Cordelia shakes his hand, then counts her fingers.” Keep the joke; the fish must not count as the player's catch.
- **Quill / secret finale:** “They seem to have learned how to manage without us. Shall I bring the second rod?”
- **Quill / trophy:** “A catch worth putting on the record. If another comes along, I shall be equally impressed.”

## Source inventory

41 free-draw cards, 6 arcs, 18 arc steps and four endings at the pinned snapshot. This is a source inventory, not an assertion that every route is reachable. The water-stewards petition in #5818 is outside this snapshot if not yet merged.

| Card | Deck | Authored choice IDs |
| --- | --- | --- |
| `warlock-druid-north` | kingdom-core | `develop`, `preserve`, `defer` |
| `harvest-festival` | kingdom-core | `fund`, `modest`, `skip` |
| `rival-angler` | kingdom-core | `accept`, `decline` |
| `warlock-return` | kingdom-core | `expand`, `cap-it`, `defer-vex` |
| `druid-sanctuary` | kingdom-core | `grant-sanctuary`, `partial-sanctuary`, `defer-sela` |
| `tax-season` | kingdom-core | `raise-taxes`, `cut-taxes`, `defer-gristle` |
| `guard-captain-wall` | kingdom-core | `fortify`, `open-borders`, `defer-cordelia` |
| `bard-ballad` | kingdom-core | `commission-flattering`, `commission-true`, `shoo-bard` |
| `smuggler-dock` | kingdom-core | `allow-smuggling`, `report-to-cordelia`, `defer-brack` |
| `duck-census` | kingdom-core | `commission-census`, `guess`, `ignore-census` |
| `rival-angler-2` | kingdom-core | `accept-again`, `decline-again`, `taunt` |
| `robin-ash-garden` | kingdom-core | `grant-garden`, `modest-plot` |
| `vex-model-village` | kingdom-core | `approve-terraces`, `orchard-terraces`, `refuse-terraces`, `defer-terraces` |
| `sela-tree-sit` | kingdom-core | `halt-building`, `remove-sela`, `join-sela` |
| `lake-watch` | kingdom-core | `conscript-anglers`, `volunteer-watch`, `refuse-watch`, `defer-watch` |
| `brack-lures` | kingdom-core | `buy-gold-lure`, `tip-cordelia`, `fish-with-brack` |
| `brack-trial` | kingdom-core | `grant-trial`, `exile-brack`, `pardon-brack` |
| `thistle-fish-exports` | kingdom-core | `sell-netting-rights`, `rustfish-only`, `refuse-exports`, `defer-exports` |
| `fish-tithe` | kingdom-core | `levy-fish`, `exempt-suppers`, `refuse-levy` |
| `fen-satire` | kingdom-core | `join-chorus`, `ban-song`, `answer-song` |
| `mossy-price` | kingdom-core | `pay-price`, `send-fen`, `refuse-price` |
| `public-dock` | kingdom-core | `fund-dock`, `share-royal-dock`, `decline-dock` |
| `vex-sela-truce` | kingdom-core | `approve-lodge`, `reject-lodge`, `let-them-explain` |
| `quill-day-off` | kingdom-core | `grant-day-off`, `fish-with-quill`, `deny-day-off` |
| `weir-reckoning` | kingdom-core | `reopen-migration`, `keep-netting` |
| `moat-reckoning` | kingdom-core | `restore-moat`, `license-roach` |
| `treaty-reckoning` | kingdom-core | `ease-the-border`, `hold-the-tolls` |
| `marina-reckoning` | kingdom-core | `return-the-reeds`, `clean-the-marina` |
| `wedding-reckoning` | kingdom-core | `family-orchard`, `family-nursery` |
| `river-commons-vote` | kingdom-core | `charter-the-run`, `license-the-run` |
| `marina-family-charter` | kingdom-core | `charter-the-cooperative`, `reserve-the-royal-pier` |
| `water-rights-hearing` | kingdom-core | `found-the-water-trust`, `auction-the-water` |
| `flood-debt-council` | kingdom-core | `fund-floodplain`, `mortgage-crossing` |
| `harbour-apprentice-hearing` | kingdom-core | `share-the-launch`, `sell-apprentice-licenses` |
| `nix-riddle` | lake-mysteries | `answer-honestly`, `answer-dodge`, `defer-nix` |
| `sunken-cache` | lake-mysteries | `dive-for-it`, `leave-it` |
| `golden-hour-catch` | lake-mysteries | `reel-it-in`, `let-it-go` |
| `nix-warning` | lake-mysteries | `heed-warning`, `dismiss-warning`, `defer-nix-warning` |
| `nix-old-name` | lake-mysteries | `restore-old-name`, `keep-royal-name`, `ask-nix-back` |
| `drowned-surface` | lake-mysteries | `clean-water`, `blame-vex`, `carp-are-fine` |
| `heron-delegation` | lake-mysteries | `grant-shallows`, `share-the-dock`, `shoo-herons` |

| Arc | Step | Authored choice IDs |
| --- | --- | --- |
| `child-elopes` | `elope-1` | `bless`, `forbid` |
| `child-elopes` | `elope-blessing` | `welcome` |
| `child-elopes` | `elope-defiance` | `relent`, `stew` |
| `envoy-treaty` | `envoy-1` | `negotiate-generous`, `negotiate-tough` |
| `envoy-treaty` | `envoy-generous` | `sign-generous` |
| `envoy-treaty` | `envoy-tough` | `finalize-tough` |
| `bog-witch-bargain` | `bog-1` | `accept-hex`, `refuse-hex` |
| `bog-witch-bargain` | `bog-accept` | `complete-accept` |
| `bog-witch-bargain` | `bog-refuse` | `complete-refuse` |
| `millrace-weir` | `weir-1` | `build-weir`, `ladder-weir` |
| `millrace-weir` | `weir-stone` | `net-the-run`, `open-sluice` |
| `millrace-weir` | `weir-ladder` | `open-ladder-pools`, `guard-ladder` |
| `reed-shallows` | `reed-1` | `dredge-cove`, `declare-nursery` |
| `reed-shallows` | `reed-marina` | `charge-moorings`, `village-berths` |
| `reed-shallows` | `reed-nursery` | `close-cove`, `catch-and-release` |
| `castle-moat` | `moat-1` | `enclose-moat`, `keep-moat-common` |
| `castle-moat` | `moat-poachers` | `fine-poachers`, `hire-poachers` |
| `castle-moat` | `moat-crowded` | `honour-rules`, `let-moat-run` |

## Required transcript matrix before t-046 closes

1. Bless/welcome, forbid/relent, forbid/stew: record family follow-ups and ensure the first two paths converge only after the player actually reconciles.
2. Defer each once-only petition and resolve it later; save/reload between attempts; log each offered card and verify no premature prerequisite.
3. Replay all existing t-045 legal route witnesses plus #5818 after merge. Record cast, card, choice, health deltas, flags and result prose.
4. Play from new saves to each finale using store-equivalent counters and deterministic draws. Record eligibility, competing ending conditions, accept and reload; all four distinct full epilogues remain visible.
5. Review the remaining deck rows against actual art, consequence, character voice and legal triggers; revise any unearned claims. This preflight is not a final editorial acceptance or a substitute for t-049's exhaustive simulation.
