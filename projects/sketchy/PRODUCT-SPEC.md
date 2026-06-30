# Sketchy — Product Spec and App-Owned Schema

Generated: 2026-06-30
Task: sketchy/t-001
Informed by: docs/ai-critique-apis.md

---

## Product Vision

Sketchy is an encouraging, skill-aware drawing practice coach. It assigns drawing exercises matched to the user's current skill level, critiques uploaded work via AI, and recommends the next exercise. The tone is warm and constructive — a supportive mentor, not a brutal art-school critic.

**It is not:** a social network, a portfolio host, or a general image editor. Sketchy focuses on the practice loop: assignment → draw → upload → critique → next assignment.

---

## Core Loop

```
User opens Sketchy
  └─ See current assignment (or calibration prompt if new)
  └─ Complete the drawing (offline, on paper or tablet)
  └─ Upload photo/file
  └─ AI critique runs (Claude Vision)
  └─ Feedback shown: what worked, what to improve, skill dimension scores
  └─ Next assignment generated (or user picks from a short list)
  └─ Optional: add to practice journal
```

---

## User Journey

### First Session (Calibration)
1. User is asked 3 quick calibration questions:
   - "How long have you been drawing?" (New / A few months / 1–3 years / 3+ years)
   - "Which area do you want to focus on?" (Fundamentals / People / Animals / Environments / Imagination)
   - "Rate your comfort with: basic shapes, proportions, shading, perspective" (1–5 sliders)
2. Sketchy sets starting skill tier: Beginner / Intermediate / Advanced
3. First assignment is generated

### Ongoing Sessions
- Landing page shows current assignment + due (soft goal — no hard deadline)
- "I'm done" button → upload flow
- After critique, user sees feedback + skill dimension deltas
- "Next assignment" CTA generates the next one at the updated skill estimate

---

## Assignment Types

See `sketchy/t-002` (assignment taxonomy) for the full ladder. At a high level:

| Category | Example assignments |
|---|---|
| Fundamentals | "Draw 20 boxes in perspective," "Fill a page with overlapping circles" |
| Gesture | "Do 10 one-minute gesture poses from a reference set" |
| Shape/Value | "Render a simple object with 5 value zones, no outlines" |
| Perspective | "Draw your room from two-point perspective" |
| Anatomy | "Sketch an arm: shoulder to hand, 3 views" |
| Character Design | "Design a character with 3 costume variations" |
| Environments | "Draw an exterior storefront without people" |
| Style Studies | "Recreate a panel from your favorite comic in your own hand" |

---

## AI Critique Flow

**Primary engine:** Claude claude-sonnet-4-6 (Vision)  
**Fallback:** GPT-4o (Vision)  
**Why Claude:** Consistently encouraging tone that matches Sketchy's brand; handles educational figure drawing without content policy friction; Anthropic does not use input data for model training.

### Critique Dimensions

The AI scores each submission on 5 dimensions (1–10 scale):

| Dimension | What it measures |
|---|---|
| Construction | Basic shapes, structure, underlying form |
| Proportions | Relative sizing of parts |
| Line quality | Confidence, weight, direction |
| Value / light | Contrast, shadow placement, form reading |
| Observation | How faithfully it matches the reference or intent |

Not all dimensions apply to all assignments — gesture critiques skip "observation" if no reference was used; value studies skip "line quality" if the prompt was ink-free.

### Critique Output Format

```json
{
  "overall": "Your boxes are getting more confident! The cross-hatching on the right face is clean.",
  "strengths": ["Consistent line pressure", "Good convergence on the horizon line"],
  "improvements": ["The ellipses on the cylinder tops are slightly off-center — try drawing them slower"],
  "scores": { "construction": 7, "proportions": 6, "lineQuality": 8 },
  "nextSkillSuggestion": "Try drawing boxes at steeper vanishing angles to push your perspective confidence."
}
```

### Safety / Privacy

- Images are sent to Anthropic API; Anthropic's API privacy policy applies (no training on user data)
- Mature content flag: figure drawing (clothed and unclothed anatomy) is handled constructively; explicitly sexual content is blocked by Anthropic's API content policy
- Images are not stored on Sketchy servers beyond the active session unless the user opts into a Practice Journal

---

## Free vs. Paid Tiers (Using Kind Robots Economy)

Sketchy does NOT create a competing token economy. It uses the existing Kind Robots mana system.

| Tier | Daily critique requests | Assignment generation | Practice Journal |
|---|---|---|---|
| Guest (no login) | 2/day | 3/day | No |
| Free (logged in) | 5/day | 10/day | Limited (last 10 sessions) |
| Paid (mana subscriber) | 20/day | Unlimited | Full history |

**How it works:**
- Each AI critique call costs mana (deducted via `withArtMana` or equivalent mana hook)
- Free tier starts with a mana allowance that refreshes daily
- Paid tier has higher mana ceiling via the existing Kind Robots subscription model
- No separate Sketchy payment flow needed at MVP

**Remaining usage display:** Show a simple indicator: "3 critiques remaining today." No raw mana numbers shown in Sketchy UI — abstract it to "critique requests."

---

## App-Owned Schema

These tables live in the Sketchy database (or a dedicated Sketchy Prisma schema), separate from the shared Kind Robots backend. Sketchy consumes Kind Robots via API; it does not add tables to the shared DB without a backend pitch.

```
SketchyUser {
  id              Int       PK
  krUserId        Int       // kind_robots user.id — the shared identity link
  calibrationTier String    // 'beginner' | 'intermediate' | 'advanced'
  focusArea       String[]  // ['fundamentals', 'people', ...]
  createdAt       DateTime
}

SketchyAssignment {
  id              Int       PK
  userId          Int       FK → SketchyUser
  category        String    // 'fundamentals' | 'gesture' | 'perspective' | ...
  difficulty      Int       // 1–10
  promptText      String    @db.Text
  referenceUrl    String?   // external reference image link (optional)
  assignedAt      DateTime
  completedAt     DateTime? // null = still in progress
}

SketchyCritique {
  id              Int       PK
  assignmentId    Int       FK → SketchyAssignment
  imageUrl        String?   // temporary presigned URL or null if not stored
  overallText     String    @db.Text
  strengths       Json      // string[]
  improvements    Json      // string[]
  scores          Json      // { construction: N, proportions: N, ... }
  skillSuggestion String?
  engine          String    // 'claude' | 'gpt4o'
  manaCost        Int       // mana charged for this critique call
  createdAt       DateTime
}

SketchyJournalEntry {
  id              Int       PK
  userId          Int       FK → SketchyUser
  critiqueId      Int?      FK → SketchyCritique
  note            String?   @db.Text  // user's own reflection
  imageUrl        String?   // stored image path (only if user opts in to journal storage)
  savedAt         DateTime
}
```

---

## What Stays in Kind Robots (Read-Only from Sketchy)

- `User` model: identity, mana balance, subscription tier
- Mana deduction: via existing `withArtMana` utility call (same hook used by art generation)
- Auth: JWT from Kind Robots login (`POST /api/auth/login`)

Sketchy must not write to any Kind Robots tables other than mana deduction via the approved utility.

---

## What Needs a Backend Pitch (Not Implemented Yet)

| Need | Pitch target |
|---|---|
| Mana hook for "critique" operation type | kind_robots: add `SketchyCritique` as a recognized mana-consuming operation |
| Mana allowance reset (daily free tier) | kind_robots: cron or middleware for daily mana refill |
| Higher mana ceiling for paid Sketchy tier | kind_robots: subscription tier config update |

---

## Out of Scope at MVP

- Social feed / community sharing of drawings
- Live video critique or real-time drawing sessions
- Custom AI persona for the critic (fun v2 feature)
- Leaderboards or gamification beyond the skill tier display
- Mobile app (web first; Flutter port is a later milestone)

---

## Feeds Into

- sketchy/t-002: Full assignment taxonomy and skill ladder
- sketchy/t-003: AI critique rubric and follow-up assignment logic (details for the scores and dimensions above)
- sketchy/t-004: Token/request tier spec (mana math and daily limits)
