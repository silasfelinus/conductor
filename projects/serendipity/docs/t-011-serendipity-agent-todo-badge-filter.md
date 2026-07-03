# Serendipity-created AGENT todo badge/filter patch

Date: 2026-07-03
Task: serendipity/t-011

## Status

The intended implementation belongs in `silasfelinus/kind_robots`, primarily in:

- `stores/todoStore.ts`
- `components/pages/conductor-page.vue`
- optionally `stores/serendipityStore.ts` for stronger metadata on newly created story decision todos

During this Worker cycle, the GitHub connector safety filter blocked creating a `worker/serendipity-t-011` branch in `silasfelinus/kind_robots`, so I could not safely land the UI patch there. This file preserves the exact intended implementation for a local-code or Claude session with patch access.

## Detection rule

A Serendipity-created AGENT todo is currently identifiable by text produced from `stores/serendipityStore.ts` when applying a needs-human story answer:

- title starts with `Story decision on `
- description starts with `Captured by Serendipity for conductor task `
- category is `AGENT`

To avoid depending only on title text, the creation path should also set an icon when it creates the todo:

```ts
const created = await todoStore.createTodo({
  title: `Story decision on ${question.projectSlug}/${question.conductorTaskId}: ${beat.answer.text.slice(0, 80)}`,
  description: `Captured by Serendipity for conductor task ${question.projectSlug}/${question.conductorTaskId} ("${context?.title ?? ''}").\n\nProtagonist's answer: ${beat.answer.text}\n\nThe conductor task stays needs-human until Silas edits the roadmap.`,
  category: 'AGENT',
  dreamId: projectDreamId.value,
  icon: 'kind-icon:sparkles',
})
```

## Store helpers

Add these helpers to `stores/todoStore.ts` inside the Pinia setup, near the existing `agentTodos` computed:

```ts
function isSerendipityAgentTodo(todo: Todo): boolean {
  if (todo.category !== 'AGENT') return false
  const title = todo.title.toLowerCase()
  const description = todo.description?.toLowerCase() ?? ''
  return (
    todo.icon === 'kind-icon:sparkles' ||
    title.startsWith('story decision on ') ||
    description.startsWith('captured by serendipity for conductor task ')
  )
}

const serendipityAgentTodos = computed(() =>
  agentTodos.value.filter(isSerendipityAgentTodo),
)

const regularAgentTodos = computed(() =>
  agentTodos.value.filter((todo) => !isSerendipityAgentTodo(todo)),
)
```

Return the new helpers from the store:

```ts
return {
  todos,
  loading,
  hasLoaded,
  lastError,
  openTodos,
  doneTodos,
  archivedTodos,
  agentTodos,
  serendipityAgentTodos,
  regularAgentTodos,
  kaizenTodos,
  honeyDoTodos,
  isSerendipityAgentTodo,
  dreamKaizens,
  dreamFeatures,
  fetchTodos,
  fetchDreamTodos,
  createTodo,
  updateTodo,
  deleteTodo,
  toggleDone,
  archiveTodo,
}
```

## Todos surface filter

In `components/pages/conductor-page.vue`, extend the task tab type:

```ts
const taskTab = ref<'AGENT' | 'SERENDIPITY' | 'KAIZEN' | 'HONEYDO'>('AGENT')
```

Update the open-task tabs so the AGENT tab uses `regularAgentTodos.length`, and add a Serendipity tab after Agent:

```vue
<button
  type="button"
  role="tab"
  class="tab gap-1 text-xs"
  :class="taskTab === 'AGENT' ? 'tab-active' : ''"
  @click="taskTab = 'AGENT'"
>
  🤖 Agent
  <span
    v-if="todoStore.regularAgentTodos.length"
    class="badge badge-xs badge-primary"
    >{{ todoStore.regularAgentTodos.length }}</span
  >
</button>
<button
  type="button"
  role="tab"
  class="tab gap-1 text-xs"
  :class="taskTab === 'SERENDIPITY' ? 'tab-active' : ''"
  @click="taskTab = 'SERENDIPITY'"
>
  ✨ Story
  <span
    v-if="todoStore.serendipityAgentTodos.length"
    class="badge badge-xs badge-secondary"
    >{{ todoStore.serendipityAgentTodos.length }}</span
  >
</button>
```

Update `filteredTodos`:

```ts
const filteredTodos = computed(() => {
  if (todoFilter.value === 'DONE') return todoStore.doneTodos
  if (todoFilter.value === 'ARCHIVED') return todoStore.archivedTodos
  switch (taskTab.value) {
    case 'SERENDIPITY':
      return todoStore.serendipityAgentTodos
    case 'KAIZEN':
      return todoStore.kaizenTodos
    case 'HONEYDO':
      return todoStore.honeyDoTodos
    default:
      return todoStore.regularAgentTodos
  }
})
```

Update the `watch(taskTab, ...)` so the manual creation form remains a normal AGENT todo while viewing the Story filter:

```ts
watch(taskTab, (tab) => {
  newTodoCategory.value = tab === 'SERENDIPITY' ? 'AGENT' : tab
})
```

## Card badge

In the todo card row, add a badge before the priority badges:

```vue
<span
  v-if="todoStore.isSerendipityAgentTodo(todo)"
  class="badge badge-secondary badge-xs shrink-0"
  >✨ story</span
>
```

This gives Serendipity-created AGENT todos a visual badge in all task filters, including done/archive history, while the Story tab gives them a dedicated open-task queue.

## Verification checklist

Run in `silasfelinus/kind_robots` after applying the patch:

```bash
npm run test
```

Manual checks:

1. Open the Conductor workspace task surface.
2. Confirm the Agent tab excludes story-created AGENT todos.
3. Confirm the Story tab shows only Serendipity-created AGENT todos.
4. Confirm story-created todos show an `✨ story` badge in OPEN, DONE, and ARCHIVED views.
5. Confirm new manually-created tasks from the Story tab still create regular `AGENT` todos unless submitted by the Serendipity write-back path.
