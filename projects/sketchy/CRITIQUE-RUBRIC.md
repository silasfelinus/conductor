# Sketchy AI Critique Rubric and Next-Assignment Routing

Detailed spec for sketchy/t-003. Builds on `PRODUCT-SPEC.md`'s AI Critique Flow (dimensions,
output JSON shape, safety/privacy) and `SKILL-LADDER.md`'s critique-to-next-assignment routing
examples and friendly progression rules — this doc formalizes both into something an engine can
actually implement, plus the system-prompt template `docs/ai-critique-apis.md` called for.

## Goals

- Score every submission consistently enough that the same drawing gets a similar score from two
  separate critique calls.
- Never let the critique feel like art-school judgment — every score exists to pick the next
  assignment, not to grade the user.
- Make the skip/apply rules and the routing algorithm concrete enough to implement without
  guessing, while leaving room for the model's own judgment on the actual score value.

## 1. Scoring dimensions and rubric anchors

Same five dimensions as `PRODUCT-SPEC.md`'s Critique Dimensions table, each scored 1–10. Anchors
below give the model (and a human reviewing its output) a shared reference for what a low/mid/high
score looks like — these are guidance for the system prompt, not a rigid checklist to recite back
to the user.

| Dimension | Low (1–3) | Mid (4–7) | High (8–10) |
|---|---|---|---|
| Construction | Forms are guessed directly in outline; no underlying structure visible | Basic forms (box/cylinder/sphere) present but proportions drift between them | Forms read as a coherent 3D structure the linework was built on top of |
| Proportions | Parts are randomly sized relative to each other; no consistent unit | Proportions are close but one or two relationships are off (e.g. head-to-body) | Proportions hold up under scrutiny; relationships are intentional, not accidental |
| Line quality | Line is scratchy, repeatedly re-traced, or hesitant throughout | Line is mostly confident with a few uncertain patches | Line is deliberate — weight and direction support the form, minimal backtracking |
| Value / light | No clear light logic, or values fight each other for attention | Light direction is identifiable; value grouping is uneven in places | Value groups read clearly at a glance; one obvious focal point via contrast |
| Observation | Drawing doesn't resemble the reference/intent in any structural way | Major shapes and proportions match; details diverge | Matches reference/intent closely in structure, proportion, and key details |

Do not average dimensions into one number anywhere in the pipeline (routing or display) — treat
them as independent signals. A high average with one very low dimension is exactly the case
routing needs to catch (see §3).

## 2. Dimension applicability by category

`PRODUCT-SPEC.md` already notes dimensions can be skipped per assignment (e.g. gesture skips
observation with no reference). This table makes that rule concrete per `SKILL-LADDER.md`'s nine
categories — `-` means always skip for that category, `?` means skip only when the specific
assignment's `successCriteria` doesn't call for it (the assignment generator's
`nextLikelyCategories`/`successCriteria` fields already carry enough context to decide this at
generation time, so store the applicable-dimension list on the assignment record itself rather
than re-deriving it at critique time).

| Category | Construction | Proportions | Line quality | Value | Observation |
|---|---|---|---|---|---|
| Fundamentals | yes | yes | yes | ? | ? |
| Gesture | yes | yes | yes | - | ? |
| Shape | ? | yes | yes | - | - |
| Value | ? | ? | ? | yes | ? |
| Perspective | yes | yes | ? | ? | ? |
| Anatomy | yes | yes | yes | ? | ? |
| Character design | ? | yes | yes | ? | - |
| Environments | yes | ? | ? | ? | ? |
| Style studies | ? | ? | yes | ? | - |
| Finished pieces | yes | yes | yes | yes | ? |

A dimension marked `-` must not appear in the returned `scores` object at all (not a null or a 0 —
absent key), so the routing algorithm in §3 never has to special-case "scored but not applicable."

## 3. Weakest-skill routing algorithm

Formalizes `SKILL-LADDER.md`'s illustrative routing table (wobbly linework → fundamentals, etc.)
into an actual procedure:

1. **Filter to applicable dimensions** for the just-completed assignment's category (§2).
2. **Find the minimum score** among those dimensions. If there's a tie, break it using this fixed
   priority order (earlier wins): `construction > proportions > observation > line quality >
   value`. Rationale: structural issues compound downstream issues, so fix those first even when
   a later-stage dimension (line quality, value) ties at the same score.
3. **Map the winning dimension to a next category** using this table (mirrors and extends
   `SKILL-LADDER.md`'s examples so every dimension has exactly one primary target):

   | Weakest dimension | Next category |
   |---|---|
   | Construction | Fundamentals |
   | Proportions | Fundamentals (or Anatomy, if the submission was an anatomy-category assignment) |
   | Line quality | Gesture |
   | Value | Value |
   | Observation | Perspective (structural mismatch) or Shape (silhouette mismatch) — the critique call's own `improvements` text should make which one applies obvious to the assignment generator; default to Perspective if ambiguous |

4. **Apply the friendly-progression override**: if the *previous* assignment's critique also
   routed off a correction (i.e., wasn't already a confidence-building pick), do not pick another
   correction drill — instead route to Shape or Character design (SKILL-LADDER's "confidence
   building" categories) regardless of what step 3 produced, and note in the assignment record
   that this was a progression override so it doesn't repeat two cycles in a row.
5. **All dimensions score 8+**: route to Finished pieces or Style studies (the two "combine
   everything" categories) rather than re-running Fundamentals on a submission with no real
   weakness to target.
6. Write the winning category into the assignment record's provenance (which dimension triggered
   it, what the score was) — not shown to the user, but needed to debug routing quality later and
   to detect the "recurring weakness stays visible in the profile" rule from
   `SKILL-LADDER.md`'s friendly progression rules.

## 4. Critique system prompt template

Per `docs/ai-critique-apis.md`'s integration notes (Claude Vision primary, cache the rubric portion
of the system prompt, vary only image + skill-level context per call):

```
You are Sketchy's drawing coach: warm, specific, and encouraging — never a harsh critic.
This is an educational drawing-practice service. The user submitted a hand-drawn study for
skill feedback in response to the assignment below. Respond only with critique of drawing
technique.

Assignment: {assignment.prompt}
Skill level: {assignment.level}
Success criteria: {assignment.successCriteria}
Applicable dimensions for this category ({assignment.category}): {applicable_dimensions_list}

Score ONLY the applicable dimensions listed above, 1-10 each, using this rubric:
{rubric_table_from_section_1}

Tone rules:
- Lead with something specific and true, not generic praise ("your ellipses are tightening up"
  beats "nice work!").
- Name at most ONE priority fix — the single highest-impact thing, not a checklist of everything
  wrong. Multiple real issues still collapse to the one worth fixing next.
- Never use discouraging language ("wrong", "bad", "you need to") — use direction instead
  ("try", "next time", "this will read cleaner if").
- If the skill level is beginner, keep the improvement note to one sentence and avoid jargon.

Respond with JSON only, matching this shape:
{critique_output_json_shape_from_product_spec}
```

`{applicable_dimensions_list}` and `{rubric_table_from_section_1}` are the cacheable static
portion per `docs/ai-critique-apis.md`; only the assignment/skill-level/image vary per call.

### Edge cases the prompt must handle without a special code path

- **Blank or near-blank submission**: score every applicable dimension 1–2, `overall` gently asks
  if the upload worked or if they'd like more time — do not treat as a failure to route around.
- **Image unrelated to the assignment** (wrong subject entirely): the model's `observation` score
  (when applicable) naturally floors, which routes correctly without a separate "off-topic" flag.
- **Content the API declines to critique** (policy refusal): the caller (not the prompt) must
  catch a refusal/error response and show a neutral "couldn't process that image, try re-uploading
  or a different angle" message — never surface a raw API error or content-policy language to the
  user.

## 5. Safety and privacy

No new policy beyond what's already specified — cross-referencing rather than duplicating:

- Image handling, retention, and provider data-use terms: `PRODUCT-SPEC.md` → AI Critique Flow →
  Safety / Privacy, and `docs/ai-critique-apis.md` §3.
- Content-policy / over-refusal mitigation (the "this is educational critique" framing) is now
  folded into the system prompt template in §4 rather than left as a future integration note.

## Acceptance criteria

- Every dimension score returned by a critique call is 1–10 and only for dimensions applicable to
  that assignment's category (§2) — no extra keys, no skipped-dimension nulls.
- Given a critique's scores and the previous assignment's routing history, §3's algorithm produces
  exactly one next category deterministically (no ties reach the caller unresolved).
- Two consecutive assignments never both route off a correction per the friendly-progression
  override in §3 step 4.
- The system prompt in §4 is the actual prompt sent to the critique API — not paraphrased at
  implementation time — so tone behavior stays consistent with what's specified here.
