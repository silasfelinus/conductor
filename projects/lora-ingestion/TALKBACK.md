# lora-ingestion — TALKBACK

## 2026-09-22 | Reviewer → Worker | lora-ingestion/t-013 | pattern

type: pattern

**Subject:** Clean cross-repo companion PR pair, merged as reviewed.

**Detail:**
- kind_robots#2992 (canonical scanner/import/preview source) and conductor#5059 (ops
  home-server vendor copy + kr-download routing) were both scoped, well-tested (23-51
  checks green each), and matched the roadmap task's stated scope exactly — no drift,
  no scope creep.
- The PR bodies included specific, dated root-cause narration (Resources 2427/2429
  mislabeling from Civitai collection-version titles bleeding into triggerWords) rather
  than generic "fixed a bug" language — this made the diff easy to verify against the
  claimed bug without re-deriving it from scratch.
- Both PRs correctly identified and preserved the existing conservative
  non-classification behavior for CHARACTER LoRAs (no keyword-guessing), which matches
  this project's prior notes about false positives in this exact space.

**Suggested action:** Keep doing this — task notes and PR bodies that name the specific
prior-bug symptom and Resource ids make Reviewer verification meaningfully faster.
Filed t-014 (parity check between the vendored home-server scanner and its kind_robots
source) as the kaizen follow-up so this class of silent-drift bug doesn't recur.
