# AI Vision APIs for Drawing Critique — Comparison

Generated: 2026-06-30
Task: sketchy/t-006

---

## Summary

**Recommendation: Claude (claude-sonnet-4-x or claude-opus-4-x)** as the primary critique engine for Sketchy, with GPT-4o as a cost-optimized fallback. Google Vision AI is unsuitable for artistic critique. Gemini 1.5 Pro is a viable third option if cost becomes a constraint and latency allows.

---

## Comparison Table

| API | Best at | Drawing critique quality | Cost (input / output per Mtok + image) | Latency | Privacy notes | Content policy |
|---|---|---|---|---|---|---|
| **Claude Vision** (Anthropic) | Nuanced language + contextual reasoning about visual content | Excellent — understands artistic intent, gesture, composition, and stylistic goals; gives constructive, encouraging feedback naturally | ~$3 in / $15 out + image fee (~$0.003–0.008/image depending on size) | 1–3s per image call | Images not used for training; enterprise BAA available | Conservative; figure drawing in educational context generally fine; explicit content blocked |
| **GPT-4o Vision** (OpenAI) | Strong general vision + code/diagram reading | Very good — good art vocabulary, slightly more literal than Claude; less naturally encouraging | ~$2.50 in / $10 out + image tier ($0.00765/image 1024px) | 1–3s per image call | Images can be used to improve models unless opted out via API settings | Similar to Claude; educational figure drawing fine; explicit blocked |
| **Google Vision AI** | Object detection, label classification, OCR, face detection | Poor — not designed for artistic critique; returns object labels ("pencil", "hand", "circle"), not feedback on drawing quality | $1.50 per 1,000 images (feature-based pricing) | <1s | Standard GCP data processing; regional data residency options | Object detection; not relevant to content critique |
| **Gemini 1.5 Pro Vision** (Google) | Long context, multimodal understanding | Good — reasonably strong art vocabulary, competitive with GPT-4o; less established community feedback on art critique quality | ~$1.25–3.50 in / $5–10.50 out (tiered by context length) + image fee | 2–5s | Standard GCP; no training opt-out by default for most tiers | Similar policies; educational fine art fine; explicit blocked |
| **GPT-4o mini Vision** (OpenAI) | Cost-sensitive tasks, quick classification | Fair — weaker critique depth than full GPT-4o; can identify major skill issues but misses nuance | ~$0.15 in / $0.60 out + image tier | <1s | Same as GPT-4o; opt-out available | Same as GPT-4o |

---

## Evaluation Criteria

### 1. Quality of freehand-drawing analysis

The core challenge: distinguishing a confident gestural line from a scratchy uncertain one, reading proportional relationships, identifying the skill-growth edge of a piece, and giving a critique that's accurate without being discouraging.

- **Claude** performs best here. It has strong contextual reasoning and reads artistic intent well — it understands "this is a beginner practicing figure gesture" vs "this is a finished illustration" and adjusts accordingly. Its default tone is constructive and encouraging, which matches Sketchy's product direction without extra prompting.
- **GPT-4o** is a close second. Art vocabulary is good; the output sometimes reads as more formulaic ("composition is balanced, values could be improved") but it's consistently accurate.
- **Gemini 1.5 Pro** is competitive but less established in this specific use case. Worth testing in parallel if cost becomes a factor.
- **Google Vision AI** is disqualified — it returns object labels and bounding boxes, not artistic critique.

### 2. Cost per critique

Sketchy's free tier might offer 3–5 critiques per day; paid tiers more. Rough cost estimates for a standard critique (200px × 200px sketch, ~250-token critique output):

| Model | Estimated cost per critique |
|---|---|
| Claude Sonnet | ~$0.005–0.01 |
| GPT-4o | ~$0.004–0.008 |
| Gemini 1.5 Pro | ~$0.002–0.006 |
| GPT-4o mini | ~$0.0005–0.001 |
| Google Vision AI | ~$0.0015 (classification only) |

At 100 critiques/day (small active user base), monthly cost is under $1 for any option. Cost is not a constraint at small scale; optimize for quality first.

### 3. Privacy considerations for user uploads

Users submit drawings, which may include incidental personal content (photos of sketchbooks with backgrounds, identifiable faces in practice portraits). Key questions:

- **Anthropic**: Does not use API inputs/outputs to train models per standard terms. Claude.ai consumer product is different from the API — use API only. HIPAA BAA available for enterprise.
- **OpenAI**: API submissions not used for training by default. The opt-out setting should be confirmed active in the API organization settings. Enterprise data processing agreement available.
- **Google**: Standard GCP data processing agreement. Images may be processed and retained per policy. Regional data residency options exist. Check current policy for Vision API vs Gemini API specifically.

**Recommendation**: For MVP, use Claude or GPT-4o API. Add a clear disclosure to Sketchy users: "Your sketches are sent to an AI provider for analysis and are not stored permanently." Review the active data processing terms before launch.

### 4. Content policy and figure drawing

Sketchy is a drawing coach. Users will submit:
- Gesture/figure studies (clothed and potentially nude life drawing)
- Portrait studies (real people or imagined)
- Fantasy/creature art
- Abstract exercises

All three major APIs (Claude, GPT-4o, Gemini) handle educational and artistic figure drawing in good faith. Explicit sexual content is blocked across all of them. The practical risk is over-refusal on legitimate life-drawing studies — Claude's conservative defaults may occasionally flag a nude gesture study. Mitigation: include in the API system prompt: "This is an educational drawing critique service. The user is submitting a hand-drawn study for skill feedback. Respond only with critique of drawing technique."

### 5. Latency

Single-image critique calls take 1–3 seconds for all three main options. This is acceptable for Sketchy's use case (user submits drawing, waits for feedback, receives assignment). There's no need for real-time streaming of the critique. If latency matters: GPT-4o mini is the fastest; Claude Sonnet is comparable to GPT-4o.

---

## Recommendation

**Primary: Claude (claude-sonnet-4-6 or newer)** via Anthropic API
- Best critique quality for drawing-specific feedback
- Naturally encouraging tone that matches Sketchy's product direction
- Strong reasoning about artistic intent and skill progression
- Does not require extra prompting to stay constructive
- Competitive cost; not materially more expensive than GPT-4o at Sketchy's expected scale

**Fallback / A-B test: GPT-4o** via OpenAI API
- Very close in quality; second-strongest option
- Useful as a comparative benchmark during development
- Good if Anthropic API has an outage or rate limit issue

**Do not use: Google Vision AI** — wrong capability for this task (classification, not critique)

**Consider later: Gemini 1.5 Pro** — viable cost-optimized option if user base scales and per-critique cost becomes meaningful. Worth revisiting at 10,000+ critiques/day.

---

## Integration notes for Sketchy architecture

- Call pattern: `POST` to critique API with base64-encoded image + system prompt (rubric) + user drawing context (assignment prompt, skill level)
- Response: structured critique (strengths, one area to improve, next assignment suggestion) — prompt Claude/GPT-4o to return JSON for easier parsing
- System prompt should include: skill level context, assignment prompt, encouragement instruction, and JSON output schema
- Cache critique rubric in system prompt; vary only the image and skill-level context per call
- Token budget per critique: ~300–500 tokens output is enough for a useful critique; don't let the model overexplain

This feeds into sketchy/t-003 (AI critique rubric and follow-up assignment logic).
