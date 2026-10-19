# ECOTONE: modular ending grammar, 56 signatures and a consequential middle

**Latest user-directed design, 2026-10-19 PT.** This supersedes **both** (a) three drug-defined mandatory dead ends and (b) the idea that 56 collectible entries require 56 entirely independent multi-decade epilogues. The LLM is free to *propose* bold futures, including utopian and dystopian cocaine, methamphetamine and MDMA openings. The public game still requires authored/curated payoff ideas with verified causal histories, not an unbounded runtime paragraph generator. These are text-only design specifications, **not** approval to generate images or publish.

## Endings are three compositions, not 56 separate novels

**7 optional adult openings** (`sober`, `tipsy`, `stoned`, `tripping`, `cocaine`, `meth`, `mdma`) × **4 final FOLLOWED companions** (`mara`, `kit`, `juniper`, `cedar`) × **2 earned outcomes** (`hope`, `dark`) = **56 stable collectible ending IDs (28 hopeful, 28 dark)**. Maintain all 32 original `lead.opening.fate` IDs; add 24 new entries. The final companion comes from guaranteed in-story **Stay / Follow** crossings, not an upfront character selector. Opening state does NOT assign morality, ideology, competence, or a guaranteed outcome.

**A fully rendered finale is assembled from:**

1. **Core future / companion-resolution spine: 4 × 2 = 8 carefully authored cores.** Each captures a substantial shared civic consequence, the final companion's central dilemma and an honest hopeful/dark resolution. Write a complete baseline **1-, 10- and 30-year** sequence for each core: **24 core temporal beats**. These eight are *not* the only civic possibilities: earlier world-future motifs, concrete flags and signature variants alter local consequences. Cedar's good cores must allow locally accountable technoutopia, and his logger/grower parents remain together in **every** timeline.
2. **Journey signature: 7 × 4 × 2 = 56 compact authored variants**, including **24 new variants** for cocaine/meth/MDMA × companion × fate. Each supplies **one genuinely specific, high-quality paragraph and a conceptually distinct visual brief/prompt** (and later, after art approval, optionally one image), reflecting how the initial lens reached that companion and the earned fate. **No invented stay/follow jump**: signature text is truthful for all legitimate play histories with that ID, or it must have a clearly constrained `when` clause and fallback. The already envisioned 32 signatures can be revised to this compact format without deleting their existing titles/plot directions.
3. **Salient choice callbacks: zero to two short paragraphs/images when materially earned.** Choose the most causally consequential, verified events from the **actual** seed, scene flags, commitments and stay/follow log. Some single high-leverage choices carry one callback; a deliberately authored pair of interacting decisions can carry **four possible combination outcomes (2×2)**. Those conditional variations are **not new collectible IDs**. A pairing belongs only when the second choice *changes the meaning* of the first; otherwise use independent small callbacks or none.

**Primary time-horizon rule:** integrate the signature and selected callback into the authored 1/10/30-year core at appropriate beats. No three-copy inflation of every signature. The original target of 56 separate triple epilogues (**168 full beats**) is **superseded as mandatory production scope**; 8 complete temporal spines + 56 distinct signature paragraphs/visual briefs + a carefully selected set of conditional callbacks are sufficient **if every resulting finale is coherent, satisfying, honest and distinct**.

## A tiny worked ending grammar

```ts
type Opening = 'sober' | 'tipsy' | 'stoned' | 'tripping' | 'cocaine' | 'meth' | 'mdma';
type Lead = 'mara' | 'kit' | 'juniper' | 'cedar';
type Fate = 'hope' | 'dark';
type EndingId = `${Lead}.${Opening}.${Fate}`; // 56 IDs, not every text permutation

type EarnedEvidence = {
  observedCards: string[];
  decisions: { choiceId: string; result: 'pass' | 'fail' | 'no_roll' }[];
  followHistory: { from: Lead | null; to: Lead | null; chapter: number; choiceId: string }[];
  trueFlags: string[];
  lastLead: Lead;
  opening: Opening;
  fate: Fate;
};

type EndingAssembly = {
  coreId: `${Lead}.${Fate}`;    // 8 narrative bases
  signatureId: EndingId;           // 56 paragraph + art prompt variants
  callbacks: string[];             // MAX 2, awarded on real predicates only
  renderedId: EndingId;            // exactly one unlock
};
```

**Example: `cedar.mdma.hope`**. The core says a locally owned technical network supports good rural work and a living watershed; in the 10-year beat Cedar's still-married Hispanic logger father and former Luna-ground-support activist mother disagree over how to repair a creek crossing. The **signature** evokes an unlikely bond made during the festival becoming the first accountable co-op meeting. **A callback** appears only if the player actually insisted on an enforceable public broadband charter; otherwise it must not claim that charter exists. A separate choice to fund habitat monitors is meaningful on its own; **if both charter AND habitat monitors were achieved**, a special joint callback describes the monitoring network publicly owned by the communities it serves. The four authored binary combinations are **(neither, charter only, monitors only, both)**. This is a potent four-way callback, not four more collectible endings.

**Example: `juniper.cocaine.hope`** could have a witty, fast-moving paragraph about an urgent, complicated land deal that ultimately protected bird habitat, *only if the actual journey supports that deal*. A person beginning with cocaine is not automatically selfish, or automatically a brilliant negotiator. Missing that particular action requires another signature that doesn't lie about it.

## Where complexity should live

**Fixed dramatic backbone:** preserve six regional chapters, ~45–75-minute variable main runs, stable historical truth, true supernatural events, five existing skills, fair visible **2d6**, guaranteed first meetings with all four companions, and meaningful **Stay / Follow** at each crossroad. The four original openings maintain their chosen-first-companion introductions; cocaine/meth/MDMA each needs an authored, appropriate initial encounter with one of the same four followers. All seven eventually can end with any follower, hope or dark. No mandatory short off-ramp by chemical type.

**Elastic middle:** keep **120+ fully authored canonical regional encounter cards**, generally ~10–18 experienced in a run. Author additional candidate scenes that have actual alternatives and consequence flags. Good complexity is **reconvergent with memory**, not uncontrolled branching: diverge where decisions cost something and change future opportunities, then merge to authored junctions carrying a concise set of trustworthy flags. The companion's presence, meeting/follow order and 4-axis ideological tensions change the situation. Avoid (7×4×120) duplicated generic scenes.

**Late funnel / consequence baskets:** before finale, collect verifiable concrete stakes: habitat easement, repair crew funding, community network ownership, fair labor deal, studio autonomy, public access, recognized artist credit, truthful radio corroboration, actual excluded-neighbor participation. The final resolution is determined by those accumulated *acts and their dice-backed outcomes*, not hidden individualist/community/nature/tech ideology points or the chosen drug. Maintain both hopeful and dark reachability in **all seven openings**.

## Selective interaction: spend complexity where choices collide

For each candidate callback, score a small **value-to-debt triage**:

- **Causal relevance:** Could a player recognize *their own decision* as the reason for this future?
- **Distinctiveness:** Does it create a truly different moment, not a synonym swap?
- **Pair interaction:** Does B meaningfully reinterpret A, yielding all four warranted outcomes? If not, do not create a 4-case matrix.
- **Truthfulness:** Are all referenced facts/relationships/land outcomes demonstrable from saved flags? Does it respect Cedar's parents-together invariant, immutable public history and tribal sovereignty?
- **Production debt:** Number of authored branches, prompt edits, unique art concepts, tests, QA comparisons, accessibility/alt-text work and revalidation when content changes.

**Budget proposal rather than hard limit:** first author **8 cores**, **56 high-signal signatures** (24 are new), and perhaps **8–16 carefully chosen two-choice interactions** with four compact outcomes each where value is unusually high. A scene or pairing that doesn't meaningfully change the actual end receives no separate art. Quality of the idea **and art prompt's ability to show that consequence** matter more than an arbitrary image count. Even with cheap generation, prompt curation, consistent species/people, continuity, image QA and runtime asset references cost editorial time.

## Art direction without premature generation

Each signature should have an **art brief** with `subject`, `Humboldt place/time`, `action already earned`, `visual contrast`, `must_include`, `must_not_imply`, `style/reference`, `alt_text`, `source_flags`, and `review_status`. Author multiple candidate prompts when an idea is weak; don't generate repetitive images as if that proves uniqueness. A callback-specific image may replace the default signature illustration **only when its predicate is true**. Use fallback art for nonmatching conditions. Do not infer tribal art, real activists' private conduct, or a real protective status that game flags did not earn. **NO image generation, ArtJobs, badge production or public release until the existing human creative gate is explicitly opened.**

## LLM writer's-room to audited content

1. **Propose widely:** generate counterintuitive, compassionate, unsettling futures, notably hopeful cocaine/meth/MDMA paths and dark outcomes that are failures of choices/institutions rather than the identities of drug users. Solicit *ideas the creator would not have chosen* without privileging a single ideology.
2. **Capture records:** one `core`, `signature` or `callback` candidate per record, with stable key, prerequisites, contradicted flags, bounded text, imagery prompt, actual referents, and a short "why this matters" clause. Track candidate revisions to avoid re-generating failed ideas.
3. **Automated gate:** check 56 ID set, original 32 IDs preserved, all seven by four by two reachability, callback predicates, no impossible combinations/duplicate effects/spoilers, no invented historical claims, accessibility/viewport fit, image asset fallback, deterministic save/replay and 32→56 local ledger migration **without falsely granting new IDs**. Use independent historical/cultural review where needed; an LLM self-check is not authority.
4. **Human gate:** prioritize **review of core concepts, signatures, unusually surprising pair interactions and final image prompts**. Present Keep / Modify / Reject at manageable batches, with seeded play examples showing each earned callback. Don't force the author to inspect ten thousand tiny permutations one at a time; do not silently publish unvetted generated ideas.
5. **Assemble deterministically at runtime:** `resolveFate(earnedChoices)` → `core(finalLead,fate)` → `signature(finalLead,opening,fate)` → at most two highest-priority compatible **verified callbacks**. Render with preapproved content and art assets, log source IDs and provide readable **“Because you…”** provenance. The LLM generates **candidates in authoring workflow**, not invented in-game player history during live epilogue.

## QA of 56 endings versus huge experiential space

- **Count:** 7×4×2 = 56, with **28 hopeful + 28 dark**, **14 slots per final companion** and **8 slots per opening lens**. Existing `lead.opening.fate` 32 IDs remain stable. All 24 new entries are truly reachable, not placeholder unlocks.
- **Pathfulness:** from all seven voluntary adult openings, naturally follow/rejoin each of the four companions, resolve either fate through real choices and checks, earn at least one valid signature without fabricating any historic jump.
- **4-outcome pair validation:** for each selected 2×2 interaction, test **all four conditions** and only the appropriate conditional text/art. An unearned action must never appear in prose, alt text, metadata, or illustration.
- **Ledger:** true unique unlocks only, persistent across runs and unchanged for previous 32 progress. The **Endings X/56** single-screen gallery, with optionally 28/28 split and 56/56 global achievement, is separate from number of prose/image variants; a visually different callback does NOT increase X/56.
- **Cultural/historical facts:** fixed Julia Butterfly Hill/Luna and real history, actual living tribal sovereignty, Kit's Hmong American identity, the separately grounded 1885 Chinese history and Cedar's Hispanic logger father, activist mother who fictionally helped supply the real Luna sit, and their enduring marriage remain true across permutations. Give different ideological positions plausible positive futures; avoid chemical/poverty stereotypes.
- **Viewport:** one bounded visual surface on mobile/tablet/desktop. Short enough signature/callback content to fit an epilogue tab with inner scroll only where necessary, no page scroll, keyboard and screen-reader access and no spoiler alt text.
