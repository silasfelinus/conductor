# interface-vision/t-137 — full note history archive

This file is the archaeology index for interface-vision/t-137 ("Ratchet Prettier formatting onto the front end instead of one repo-wide reformat"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-137 -->
Silas, 2026-09-14, on being offered a repo-wide format pass as its own PR: "this strikes me as something that can do double duty ... this feels like something that should be wrapped into that agent task list." Filed here rather than run as a one-off, because measuring it first showed a one-off is the wrong shape.
THE MEASUREMENT (2026-09-14): `npx prettier --check .` reports 1178 files, not the ~33 a single task touches -- 789 .ts, 168 .vue, 123 .json, 44 .mjs, 42 .md, concentrated in server/ (288), utils/ (277), components/ (159), prisma/ (119), config/ (116). A single reformat PR would be a 1178-file diff that conflicts with every in-flight branch, and t-104 alone is grinding 270+ slices right now. It would also be unreviewable: a real behaviour change hidden in it would be invisible.
FIRST MOVE, INDEPENDENTLY WORTH DOING: there is no `.prettierignore` at all, so `prettier --check .` is scanning machine-generated and data files nobody should ever hand-format -- prisma/generated (118 files, the checked-in Prisma client) and config/ (116 files, art-coverage and comment-draft JSON batches). That is ~20% of the count and pure noise. Add a `.prettierignore` covering generated clients, data batches, and any vendored tree, then re-measure. The remaining number is the real backlog.
THEN RATCHET IT, the way this project already does everything else. utils/scripts/ ratchetBaseline.ts exists precisely for this and already has four consumers (verifyLayoutContract, verifyLintRatchet, verifyComponentReachability, verifyRouteGalleryContract) -- this is the fifth, not new machinery. Bucket by directory or by extension rather than one total, for the same reason verifyLintRatchet buckets by rule: with a single number, formatting twenty files silently pays for twenty newly unformatted ones. A bucket may only ever shrink. Wire it as `test:prettier-ratchet` beside the existing ratchets.
HOW THE BACKLOG DRAINS: not as its own grind. Every other slice in this project already edits files; each one formats the files it was already touching and re-records the baseline downward. That is why this is `recurring: true` and why it costs almost nothing -- the work rides along with work already happening, and the ratchet makes the direction one-way. Do NOT bulk-format untouched files to make the number move faster; a formatting diff on a file no task is otherwise editing is exactly the review-hostile change this task exists to avoid.
WHY IT MATTERS BEYOND TIDINESS: package.json already defines `lint:prettier` (`prettier --check .`) as half of `npm run lint`, but no workflow runs it, so the script is decorative and the drift is unbounded. This makes the declared standard enforceable without a flag day. Never add `--write` to CI, and never let the ratchet bypass a genuine formatting regression by re-recording upward.

First bounded Prettier-ratchet slice: exclude generated Prisma client and generated/curation data batches from the formatting backlog before establishing the ratchet baseline.

PR #2918 merged after exact-head CI completed successfully; rearm recurring Prettier-ratchet work for the next bounded slice.

Released immediately after live workflow failure detection preempted worker role; no implementation started.

PR silasfelinus/kind_robots#2929 merged (squash 3c4b94d): verifyPrettierRatchet.ts
(reusing ratchetBaseline.ts, same shape as verifyLintRatchet.ts) buckets unformatted
files by top-level directory and refuses growth on --update. Initial baseline recorded
with the repo's pinned Prettier via node_modules (not npx-latest): 1097 files across 20
directories. Wired into contract-tests.yml. Also excluded utils/scripts/*-ratchet-
baseline.json from Prettier itself (self-referential bootstrap bug: the baseline's own
JSON.stringify formatting always differs from Prettier's, so it would otherwise flag
itself as newly-unformatted right after every --update). Review-claim caught a real gap
before merge: grownRatchetBuckets() only compares bucket length, so a same-bucket
substitution (fix one file, break a different one, count unchanged) would have slipped
through -- fixed with a local substitutedRatchetBuckets() membership check (kept local
rather than changing the shared helper, since eslint's line:column entries would false-
positive under exact-set comparison). No files reformatted -- this PR only adds the gate
and baseline. Rearming to ready (recurring) for the next bounded reformat slice.

PR silasfelinus/kind_robots#2930 merged (squash 150274b): bounded reformat slice for the
types/ ratchet bucket (coloringBookPackage.ts, coloringBookStudio.ts, ruler-hooked.ts --
pure union-type line-wrapping, no behavior change). Baseline re-recorded: types/ bucket
3 -> 0, total 1097 -> 1094. Rearming to ready (recurring) for the next bounded slice.

PR silasfelinus/kind_robots#2931 merged (squash 1b9b0d9): bounded reformat slice cycle 2
-- prisma/.vscode/assets buckets (5 files: prisma/seeds/inspiration-prompts.ts,
.vscode/bookmarks.json, .vscode/settings.json, assets/css/memory-dungeon.css,
assets/css/tailwind.css). Verified programmatically that the seed file's string content
is unchanged modulo whitespace/trailing-comma/quote-style. Baseline 1094 -> 1089, 19 ->
16 directories. Rearming to ready (recurring) for the next bounded slice.

PR silasfelinus/kind_robots#2932 merged (squash 56f324b): bounded reformat slice cycle 3
-- artifacts/plugins buckets (8 files: 4 JSON audit/proposal data files verified value-
identical via parse-and-compare, 4 client plugins verified formatting-only by hand).
Baseline 1089 -> 1081, 16 -> 14 directories. Rearming to ready (recurring) for the next
bounded slice.

Connector-only cycle inspected the live 1081-file Prettier baseline after the prior three bounded slices. No safe next formatting slice was applied because this transport cannot execute the repository-pinned Prettier or regenerate the membership baseline, and hand-editing the baseline would defeat t-137's exact-set regression guard. Re-armed without consuming a pass; no implementation branch was created.

Bounded reformat slice cycle 4: tests/contracts (8 files, verified content-preservation
by diffing tsx output before/after + eslint clean). Baseline 1081 -> 1073, 14 -> 13
directories. Rearming to ready (recurring) for the next bounded slice.

PR silasfelinus/kind_robots#2951 merged (squash 4733cb4): bounded reformat slice cycle 5
-- .github bucket (8 files: all .github/workflows/*.yml). Content-preservation verified
by parsing each file before/after with yaml.safe_load and comparing equal. Baseline re-
recorded: 1073 -> 1057 (.github bucket 8 -> 0; a few other buckets also drifted down
slightly on re-measurement since the baseline was last recorded, unrelated to this
slice). Rearming to ready (recurring) for the next bounded slice (next-smallest bucket:
content, 10 files).

Connector-only cycle verified PR #2956's follow-up finding against current main: the Prettier ratchet already runs in Contract Tests, but its baseline now has 33 newly-unformatted files from unrelated merges. This transport cannot run the repository-pinned Prettier or safely regenerate the exact-membership baseline, so no hand-formatted/baseline-forged slice was attempted. Re-armed without consuming a pass.
<!-- note:end t-137 -->
