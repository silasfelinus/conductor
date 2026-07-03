# Serendipity Playthrough + Polish Report

Date: 2026-07-03
Task: `serendipity/t-007`
Status: connector-grounded playthrough audit; no live browser screenshots captured

## Scope

This pass reviewed the complete Serendipity path as implemented across the merged Kind Robots PRs and current source:

1. Theme pick: tone, LOCATION Dream, GENRE Dream, vibe words, optional project.
2. Story loop: opening beat, answered beats, momentum phases, bounded recap, finale.
3. Real-task weaving: HONEYDO todos and `needs-human` conductor tasks shown as story questions.
4. Write-back: explicit per-item Apply action in the Story ledger.
5. Finale recap: local summary of what the story learned.

I did not publish, deploy, call live endpoints, edit Kind Robots backend state, or touch roadmap approval gates.

## Runtime limitation

This Worker run had GitHub connector access, but no live browser session or local Kind Robots checkout. Because of that, I could not capture real screenshots or perform a visual click-through against a Vercel preview/production session. The report below is grounded in the merged PR handoffs and the current `kind_robots` source files.

Screenshot checklist for the first human/local browser pass:

- Intro screen with tone, LOCATION, GENRE, project selector, and vibe input.
- First woven story beat with the answer box.
- A real-task question showing the "This question is really about" reassurance card.
- Story ledger with one pending answer and the explicit Apply button.
- Finale state showing "The End" plus "What the story learned" recap.

## Playthrough path reviewed

### 1. Theme pick

The intro screen gives a clear entry point: tone buttons, optional LOCATION dreams, optional GENRE dreams, project selector, vibe words, Open the door, and Surprise me. This supports both low-friction play and directed project-help sessions.

Strengths:

- The copy stays playful: "Choose your door," "Story grammar," and "Open the door" feel on-brand.
- Empty state guidance tells the user to add LOCATION or GENRE Dreams when none are available.
- Project selection defaults to "A story just for me," so task weaving is opt-in.

Polish notes:

- The page could eventually show a tiny preview sentence after selections, such as: "A cozy story in the Moonlit Arcade, told like a fairy tale." That would make the door feel chosen before opening.
- The project selector is functionally clear, but emotionally quieter than the tone/place/genre controls. It may need a helper line: "Pick a project only if you want the story to help move real work."

### 2. Story loop

The store creates an app-owned session, persists it to localStorage, streams text through `chatStore.generateText`, and keeps long stories bounded with an opening + recent-beats recap strategy. The closing path is available after beat 2 and generates a finale with no question.

Strengths:

- Momentum phases are a good guard against cozy meandering: young, rising, deep, resolving.
- Bounded recaps are exactly the right move; otherwise this feature becomes a prompt-context spaghetti kraken.
- The story can be closed intentionally, which makes it feel like a toy rather than a trap.

Polish notes:

- The streaming text currently relies on the last chat added after `weaveStartChatCount`. This is already known from `serendipity/t-008`; the safer future fix is exposing an in-flight chat reference from `chatStore`.
- The answer box is direct and simple. A small "Skip / ask something else" option could help when a prompt misses, but that should be a separate task because it changes session behavior.

### 3. Real-task weaving

When a project is selected, the store gathers HONEYDO todos and `needs-human` conductor tasks. Each real item can become an in-world question, and already-used hooks are excluded by todo/task id.

Strengths:

- The reassurance card is doing important trust work: it names the real item and clearly says nothing is marked done or approved by answering.
- Project-scoped honeydos are honored through the PROJECT Dream id, while unscoped honeydos can still ride along.
- Needs-human conductor tasks are read-only at story time, which preserves conductor roadmap authority.

Polish notes:

- If there are no hooks for the selected project, the story silently becomes preference-only. That is acceptable, but a small intro note would reduce confusion: "No real tasks are waiting, so this one is just for exploration."
- The hook order is currently first available. Later, the story could prefer tasks with higher downstream impact, but that belongs in a future kaizen.

### 4. Story ledger and write-back

The ledger lists captured real-task answers and exposes one Apply button per item. Honey-do Apply marks the todo DONE and appends the answer to the description. Needs-human Apply creates an AGENT todo carrying the decision; the conductor roadmap is not edited by the app.

Strengths:

- This is the correct safety model. Answering is creative capture; Apply is the real action.
- The UI explains what Apply will do before the user clicks.
- Failed writes return to pending instead of disappearing. Excellent little seatbelt.
- The `written` badge gives closure without overclaiming approval.

Polish notes:

- After Apply succeeds, the card could show a tiny "Undo in Todos" hint for honey-dos, since the PR handoff says the write is reversible from the Todos page.
- Needs-human decision todos should get a future badge/filter in the Todos surface; that is already queued as `serendipity/t-011`.

### 5. Finale recap

The completed state shows "The End" and, when available, a "What the story learned" card summarizing tone, place, story grammar, vibes, preference clues, and real-world threads held for review.

Strengths:

- This gives the experience a nice landing page instead of simply stopping.
- The recap is local/session-derived and does not write preferences anywhere. Safe and reversible.
- "Real-world threads held for review" is a good phrase: it communicates usefulness without pretending work was done automatically.

Polish notes:

- The recap could later include a "Start a new story with these choices" button.
- If no recap items exist beyond tone, the card may feel thin; the current `v-if="sessionRecap.length"` is safe, but a richer empty recap message could help.

## Recommended first human playthrough script

Use a project that has at least one HONEYDO or `needs-human` task visible to the app.

1. Open Serendipity.
2. Choose `cozy` or `mysterious`.
3. Pick one LOCATION Dream and one GENRE Dream if present.
4. Select the project.
5. Add vibe words: `moonlit, practical, mischievous`.
6. Open the door.
7. Answer the first question in one sentence.
8. Confirm that a real-task reassurance card appears when a hook is woven.
9. Answer the real-task question.
10. Confirm the Story ledger shows the captured answer and proposed write.
11. Click Apply on one honey-do item and verify the todo flips DONE in the Todos surface.
12. Click Apply on one needs-human item and verify an AGENT todo is created.
13. Bring the story to a close.
14. Confirm the finale recap summarizes tone/place/genre/vibes and real-world threads.

## Verdict

Serendipity is coherent enough for a first full local/browser playthrough. The core safety line is intact: the story can ask meaningful questions and capture answers, but every real-world write requires an explicit Apply action, and the app never edits conductor roadmap YAML.

The biggest remaining risk is not product direction; it is runtime confidence. The next pass should be a real browser session with screenshots and backend verification, especially around Apply behavior and the known streaming-text heuristic.

## Follow-up candidates

- `serendipity/t-011`: badge and filter Serendipity-created AGENT todos in the Todos surface.
- New small task: Add an empty-hook note when a selected project has no honey-dos or needs-human tasks available.
- New small task: Add a human-browser screenshot playthrough artifact once a local/Vercel session is available.
