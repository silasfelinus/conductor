# slime-city — task history archive

Full `note:` prose for completed slime-city tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Build three playable square-grid prototypes, teams, city and special cards

<!-- note:begin t-001 -->
SILAS 2026-10-30 PT overrides earlier pentagonal rules. Create a discoverable ADMIN-only /admin/slime-city single-screen comparison console with 8x8 hidden-army BLACKOUT (Stratego-like), 12x6 turn-based lane MEATBALL and 14x6 real-time BLOODRUSH. Orthogonal square movement, simple adjacent simultaneous combat, mana, concealed units, card targeting and win paths. Six named teams including gene-catgirls, punk bloodfairies and cyber-ogres, seven illustrated/stylized districts, creature/spell/trap/ equipment examples. Implement testable pure TypeScript engine, Pinia lab state and timer; no reward persistence or public launch. Do not call CSS art generated artwork. Seeded tests, TS checks and phone/tablet/desktop visual QA required before marking ready for final subjective feedback. Shared external-facing release remains gated.

MERGED: Kind Robots PR #4478 (361faeecc3998e73ef44c22299623e05901540e5) implemented the private /admin/slime-city lab with Blackout 8x8, Meatball 12x6 and Bloodrush 14x6, six teams, thirty-six prototype cards, seven district selections, square-grid simulation, admin navigation and repeatable sample match controls. All 23 app checks passed, including TypeScript, Nuxt production build, four contract shards and the new Slime City deterministic contract. Conductor PR #6809 merged the superseding design, roadmap, CONTROL direction and square-grid art prompts after all 26 checks completed. This completes the implementation slice, NOT generated art, actual campaign/economy or public launch. The self-hosted site has no PR preview or automatic deploy; rendered 390/768/1440 screenshot acceptance is still outstanding and belongs to t-016, with additional actual art provenance in t-017. Neither is counted as delivered. No secrets, production economy or outward-facing publishing were touched.
<!-- note:end t-001 -->

## t-002 — Harden square movement, fog-of-war, action costs and three cadences

<!-- note:begin t-002 -->
Validate 8x8, 12x6 and 14x6 coordinate topology, only four orthogonal neighbors, occupied collision, hidden placement and fair reveal/attack, movement AP, per-round mana and card timing. Test simultaneous adjacent damage minus armor, double knockout, real-time pause/resume consistency, football scoring, AI spawn fairness and ghost/pile-up exploits, seeded command replays. Remove old pentagon/facing/twist logic everywhere in this game. Honest proof-of-concept limitations belong in the UI tutorial.
MERGED 2026-10-30: Kind Robots PR #4496 (f5269545), all 23 checks green. The CPU (utils/slimeCity/cpu.ts) decides only from the redacted observe() view and plays creature, spell, trap and equipment cards with its own mana. It respects AP and runs, escorts and hunts the flag in BLACKOUT, defends lanes, and banks for BLOODRUSH waves. BLACKOUT: 20-round limit with HP tiebreak; end-of-round flag pickup; carrier walks 1 AP; a fallen carrier drops the flag in place; back-column return; seeded armies and flag square; hidden fighters fight back; alternating initiative. Lanes: front-to-back flow plus sidesteps (no pile-ups); 3+ AP sprint; field cap 6; one armed trap; each card once per round; MEATBALL 30 rounds. BLOODRUSH: fixed 1 s ticks, banked mana, board beat every 2 ticks, 4-tick card rest, 150 ticks; pause/resume and between-tick plays tested through the real Pinia store with mock timers. Also: command record + replayMatch, 60-line log, per-match seeds with SAME SEED, hidden-info leak tests (CPU view byte-identical under hidden perturbation, no enemy secrets in the log), and per-format HOW TO PLAY panels with prototype limits. Pentagon/facing code is absent and the test asserts it. Tests: verifySlimeCityLab + verifySlimeCityStore.
<!-- note:end t-002 -->

## t-003 — Experiment with flag, monster and rout objectives across prototype boards

<!-- note:begin t-003 -->
After initial comparative playtests, create toggles or authored scenarios for flag capture/return, neutral beast kill, and fighter rout with reversible rules; assess whether they belong in hidden army games, advancing lanes, timed waves, or a deliberate hybrid. Test victory ties, early board emptiness, carrier rules, target counterplay, score pacing and accessibility. Do not lock this into all modes without evidence or a human design verdict.
DONE 2026-10-30: Kind Robots PR #4520 (3688a309) merged, all 21 checks green. Six reversible rule variants, all OFF by default and selectable in the /admin/slime-city lab (RULE VARIANTS toggles, aria-pressed, restart on the same seed): GIANT MONSTER (neutral centre beast for all three boards; blocks its square, swats the weakest neighbour, damage spells can target it; killing blow wins, ties by final-exchange then match damage), lane ROUT (26/18 KOs), LANE MOMENTUM (scoring drought makes upfield runners surge a square), SUDDEN DEATH extra time, YARDAGE TIEBREAK and a BLOODRUSH initiative swap. CPU hunts the monster in BLACKOUT and finishes it with spells. Replays with variants are tested (verifySlimeCityCrews). Measured effects (10 seeds, conductor PLAYTEST-COMPARISON 'After rebalance'): MEATBALL momentum+sudden death+tiebreak draws 44 -> 1.3%, seats 49/49; BLOODRUSH momentum draws 17 -> 3%, seats 50/46; monster ends 69% of BLACKOUT matches and halves length; rout widens lane crew spread to 9-84% (not recommended); rush swap and BLOODRUSH monster worsen the seat split (34/53, 25/64). Recommendations recorded; final rules stay with Silas in t-013.
<!-- note:end t-003 -->

## t-016 — Adversarially playtest and compare the three square-grid rule variants

<!-- note:begin t-016 -->
Produce multiple seeded and manual runs of BLACKOUT 8x8, MEATBALL 12x6 and BLOODRUSH 14x6. Measure first meaningful decision, clarity, tension, match duration, 6-team counterplay, clogged lanes, stalemates, comeback frequency, card usefulness, input reachability and real-time burden. Deliver a concise comparative report with desktop/phone screenshots and retain each playable variant. No agent unilateral final-mode decision.
DONE 2026-10-30: projects/slime-city/PLAYTEST-COMPARISON.md compares 1,800 seeded CPU- vs-CPU matches (600 per format; all 30 ordered crew pairings x 20 seeds) on the Kind Robots f5269545 engine. Reproduce with: npx tsx utils/scripts/slimeCityPlaytest.ts 20. Headlines. BLACKOUT: mean 12.4 rounds; 69% flag runs, 30% clock; first-initiative 53/46; 48% comebacks; 14% decided by round 4. MEATBALL: 27% draws and 44.5% reach round 30; most card play and lead changes; crews most polarised. BLOODRUSH: median 44 ticks; 82% breakthroughs; second side 52/40. Meat Exchange over-performs in all three (72/75/82%) and Catgirls sit at 24% in MEATBALL. Rule-sensitivity runs are included. Nine screenshots (projects/slime-city/playtest/*.webp) are Chromium renders of the real page component, store and engine at 390/768/1440 in a Vite harness. The deployed admin site was NOT captured: it needs the DB and admin auth. No mode was chosen; the verdict stays with Silas in t-013.
<!-- note:end t-016 -->
