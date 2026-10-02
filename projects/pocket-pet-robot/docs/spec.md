# Pocket Pet Robot — Spec

date: 2026-10-02
task: pocket-pet-robot/t-003
home: kind_robots `/play/pocket-pet`
status: ready for t-004 (engine) to build against

No LLM at runtime, no account, no server. All state lives in the browser; everything is pure code plus static art.

## 1. State

```ts
interface PetState {
  version: 1
  name: string
  form: 'sprout' | 'buddy' | 'champion'
  careScore: number        // accumulated care points, drives growth
  hunger: number           // 0..100, 100 = full
  fun: number              // 0..100
  energy: number           // 0..100
  asleep: boolean
  lastTick: number         // epoch ms of last applied decay
  adoptedAt: number
  visitDays: number        // distinct local days with at least one action
  lastVisitDay: string     // YYYY-MM-DD, local
}
```

The engine is a set of pure functions: `adopt(name, now)`, `tick(state, now)`, `act(state, action, now)`, `mood(state)`, `form(state)`. Time is always passed in; the engine never reads the clock.

## 2. Needs and decay

Decay is applied lazily in `tick` from `now - lastTick`, so no timers run while the page is closed.

| Need | Awake decay / hour | Asleep change / hour |
|------|--------------------|----------------------|
| hunger | -6 | -2 |
| fun | -5 | -1 |
| energy | -4 | +15 |

Actions (each also adds care points; each has a 2-minute soft cooldown after which it gives half effect, so tapping repeatedly is harmless, never punished):

| Action | Effect | Care |
|--------|--------|------|
| feed | hunger +30 | 1 |
| play | fun +30, energy -8, hunger -4 | 1 |
| sleep / wake | toggles `asleep`; waking before energy 60 gives no penalty | 0 |
| tidy (room tap) | fun +5 | 0 |

All values clamp to 0..100.

## 3. Mood

`mood(state)` returns one of eight values, matching the eight sprites per form. First match wins:

1. `sleeping` if asleep
2. `sleepy` if energy < 25
3. `hungry` if hunger < 25
4. `bored` if fun < 25
5. `ecstatic` if all three needs >= 85
6. `happy` if the average of the needs >= 60
7. `content` if the average >= 40
8. `wistful` otherwise (low but never "sad/sick/dying")

## 4. Away behaviour: gentle, never punishing

- Decay while away is **floored**: hunger and fun never drop below 15 and energy never below 20 from time away alone. Nothing dies, runs away, gets sick or loses progress.
- Away longer than 8 hours: the pet is put to sleep automatically; on return it wakes with a short greeting line from a static pool (`utils/pocketPetLines.ts`) such as "You're back!".
- `careScore` and `form` never decrease.
- Clock changes (`now < lastTick`) are treated as zero elapsed time.

## 5. Growth: three forms over about two weeks

| Form | Reached when |
|------|--------------|
| sprout | on adoption |
| buddy | careScore >= 20 and visitDays >= 3 |
| champion | careScore >= 70 and visitDays >= 10 |

A casual visitor (a few actions on most days) reaches buddy near day 4–5 and champion near day 12–14. Care points are capped at 6 per local day so growth rewards regular visits, not binge play. Evolution plays a one-time celebration and is announced with `aria-live`.

## 6. Persistence

- Key `pocket-pet:v1` in `localStorage`, every read and write wrapped in try/catch; the page renders a fresh in-memory pet if storage is unavailable.
- Load validates the shape and clamps values; unknown `version` starts a new pet rather than throwing.
- Pinia store `usePocketPetStore` owns state; components never call the engine directly or any API.

## 7. Sprite and scene manifest

`public/pocket-pet/manifest.json`:

```json
{
  "version": 1,
  "forms": {
    "sprout": { "moods": { "happy": "sprites/sprout-happy.webp" } },
    "buddy": {},
    "champion": {}
  },
  "rooms": { "kitchen": "rooms/kitchen.webp" },
  "meta": { "model": "krea-2", "promptFile": "ART-PROMPTS.md" }
}
```

- 3 forms x 8 moods = 24 sprites: 512x512 WebP, transparent background, one consistent character design per form (same palette and outline weight), named `sprites/<form>-<mood>.webp`.
- 6 room backdrops, 1600x900 WebP: `kitchen`, `bedroom`, `playroom`, `garden`, `workshop`, `rooftop`. Room is chosen by the last action (feed→kitchen, sleep→bedroom, play→playroom) and time of day; the rest unlock with form.
- Each entry carries `prompt`, `model` and `seed` metadata per the Krea 2 contract in ART-PROMPTS.md. The validator in t-004 fails on a missing file or mood.
- Placeholder sprites (flat-colour SVG per mood) ship first so the page works before art lands.

## 8. Page

One room, pet centre, three buttons (Feed, Play, Sleep), three need meters with text values, name edit, and a reset-with-confirm. Responsive at 375/768/1280, keyboard operable, animation disabled under `prefers-reduced-motion`.

## 9. Tests (t-004)

DB-free tsx tests: decay maths, floors, cooldown halving, mood precedence table, growth thresholds and daily care cap, clock-skew, long-absence sleep, storage-shape validation, and a deterministic two-week simulation proving buddy/champion timing.

## 10. Out of scope

LLM calls, accounts, payments, multi-pet, trading, notifications and any deploy step.
