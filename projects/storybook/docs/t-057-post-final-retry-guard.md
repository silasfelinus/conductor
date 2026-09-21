# t-057 implementation handoff: post-final retry guard

Session: `openai-scheduled-2026-09-21T031604Z-storybook-t057-a11`

Target repository: `silasfelinus/kind_robots`

Intended implementation branch: `worker/storybook-t057-openai-scheduled-2026-09-21T031604Z-storybook-t057-a11`

## Verified defect

`server/utils/storybookRuns.ts` currently has two inconsistent terminal-turn paths.

In `submitStoryTurn()`, the normal move path computes `isFinalTurn` from `run.currentChapter >= turnBudget` and deliberately persists `pendingTurn: null` for that final move. The run remains `ACTIVE` until explicit resolution. A subsequent null move, used by the Reading UI's "Ask for it again" recovery action, therefore enters the null-move branch with no pending scene.

That branch currently calls `narrateInto()` unconditionally. `narrateInto()` always writes a new `pendingTurn`, including when `turnIndex >= turnBudget`. The same null-move response computes `readyToResolve` as `(isEndless || questDone(quest)) && run.currentChapter > minTurns`, dropping the budget-complete case used by the replay/main branches. The result can both hide resolution and persist an off-budget scene.

## Exact patch shape

Keep the fix inside `server/utils/storybookRuns.ts`; no schema/API shape change is needed.

Immediately inside the `if (!input.move)` branch, after the existing `pending` guard and before `narrateInto(...)`, compute the terminal budget condition:

```ts
const isFinalTurn = !isEndless && run.currentChapter >= turnBudget
if (isFinalTurn) {
  return {
    run,
    deck,
    turn: null,
    pendingTurn: null,
    inventory,
    turnIndex: run.currentChapter,
    turnBudget,
    isFinalTurn: true,
    readyToResolve: true,
    replayed: false,
  }
}
```

This makes the recovery request idempotently return terminal state instead of invoking the narrator or writing a post-budget `pendingTurn`.

For the non-terminal null-move response, align `readyToResolve` with the established replay branch rather than its current narrower formula:

```ts
readyToResolve:
  (isEndless
    ? run.currentChapter > minTurns
    : run.currentChapter > turnBudget) ||
  (questDone(quest) && run.currentChapter > minTurns),
```

The budgeted branch should normally be unreachable there because the terminal guard returns first, but using the same formula prevents the branches from drifting again.

## Regression coverage

Extend the existing Storybook play-loop contract rather than adding a database-dependent verifier. The regression must demonstrate all of these in one budgeted run:

1. Play through the configured final turn.
2. Confirm the final response has `pendingTurn === null`, `isFinalTurn === true`, and `readyToResolve === true`.
3. Call `submitStoryTurn()` again for the current chapter with `move: null`, matching "Ask for it again".
4. Confirm the response remains terminal: `pendingTurn === null`, `isFinalTurn === true`, `readyToResolve === true`.
5. Confirm the injected narrator was not called by that post-final retry and no additional choice/stat mutation occurred.

Run the focused Storybook play-loop/final-turn contract, TypeScript, ESLint/Prettier ratchets, and normal PR CI.

## Connector limitation

This session verified the defect against current `kind_robots/main` and created the intended target branch, but the available GitHub connector only exposes whole-file replacement for existing files. `server/utils/storybookRuns.ts` is a large file and Conductor's connector-worker rules explicitly forbid reconstructing a large replacement from paged/truncated reads. No target code was overwritten or approximated. A shell-capable worker should apply the small patch above to the live file, run the tests, and open/merge the normal Kind Robots PR.

The empty target branch contains no unique commit and is safe for the branch janitor to remove if it remains after the handoff.