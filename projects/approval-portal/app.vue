<script setup lang="ts">
type ApiResponse<T> = { success: true; data: T } | { success: false; message: string }

type ProjectSummary = {
  slug: string
  kind: string
  priority: string
  priorityRank: number
  progressPercent: number
  taskCounts: Record<string, number>
  readyTaskCount: number
  needsHumanCount: number
  reviewCount: number
}

type ProjectDetail = {
  slug: string
  controlDirection: string
  roadmap: { kind: string }
  milestones: Array<{ id: string; title: string; status?: string; weight?: number }>
  tasks: Array<{ id: string; title: string; milestone?: string; status: string; owner?: string | null; stakes?: string; depends_on?: string | string[]; gate_human?: boolean; approved_by_human?: boolean; note?: string }>
}

const projects = ref<ProjectSummary[]>([])
const selectedProject = ref<ProjectDetail | null>(null)
const pending = ref(true)
const error = ref('')

const statusTone = (status: string) => {
  if (status === 'ready') return 'badge-success'
  if (status === 'claimed') return 'badge-info'
  if (status === 'review') return 'badge-secondary'
  if (status === 'needs-human') return 'badge-warning'
  if (status === 'blocked') return 'badge-error'
  if (status === 'waiting') return 'badge-neutral'
  return 'badge-ghost'
}

const groupedTasks = computed(() => {
  const tasks = selectedProject.value?.tasks ?? []
  return tasks.reduce<Record<string, typeof tasks>>((groups, task) => {
    groups[task.status] = groups[task.status] ?? []
    groups[task.status].push(task)
    return groups
  }, {})
})

const fetchProject = async (slug: string) => {
  const response = await $fetch<ApiResponse<ProjectDetail>>(`/api/project/${slug}`)
  if (!response.success) throw new Error(response.message)
  selectedProject.value = response.data
}

onMounted(async () => {
  try {
    const response = await $fetch<ApiResponse<ProjectSummary[]>>('/api/projects')
    if (!response.success) throw new Error(response.message)
    projects.value = response.data
    if (projects.value[0]) await fetchProject(projects.value[0].slug)
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : 'Unable to load dashboard'
  } finally {
    pending.value = false
  }
})
</script>

<template>
  <main class="min-h-screen bg-base-200 text-base-content">
    <section class="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6">
      <header class="rounded-2xl border border-base-300 bg-base-100 p-6 shadow-xl">
        <p class="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Conductor</p>
        <h1 class="mt-2 text-4xl font-black">Approval Portal</h1>
        <p class="mt-2 text-lg text-base-content/70">Local read-only dashboard for projects, milestones, task status, gates, and dependencies.</p>
      </header>

      <div v-if="error" class="alert alert-error rounded-2xl">{{ error }}</div>
      <div v-if="pending" class="rounded-2xl border border-base-300 bg-base-100 p-12 text-center">Loading…</div>

      <div v-else class="grid gap-6 xl:grid-cols-[1fr_420px]">
        <section class="rounded-2xl border border-base-300 bg-base-100 p-5 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-2xl font-black">Project Overview</h2>
            <span class="badge badge-primary badge-lg">read only</span>
          </div>
          <div class="grid gap-3 md:grid-cols-2">
            <button v-for="project in projects" :key="project.slug" class="rounded-2xl border border-base-300 bg-base-200 p-4 text-left" type="button" @click="fetchProject(project.slug)">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <p class="font-mono text-sm text-base-content/50">#{{ project.priorityRank }}</p>
                  <h3 class="text-xl font-black">{{ project.slug }}</h3>
                  <p class="text-sm uppercase tracking-wide text-base-content/60">{{ project.kind }} · {{ project.priority }}</p>
                </div>
                <div class="radial-progress text-primary" :style="{ '--value': project.progressPercent }" role="progressbar">{{ project.progressPercent }}%</div>
              </div>
              <div class="mt-4 flex flex-wrap gap-2">
                <span v-for="(count, status) in project.taskCounts" :key="status" class="badge" :class="statusTone(String(status))">{{ status }} {{ count }}</span>
              </div>
            </button>
          </div>
        </section>

        <aside class="rounded-2xl border border-base-300 bg-base-100 p-5 shadow-xl">
          <h2 class="text-2xl font-black">M1 status</h2>
          <div class="mt-4 space-y-3 text-base-content/70">
            <p>This milestone intentionally has no write actions.</p>
            <p>Project and task state is read from the same roadmap files the worker uses.</p>
            <p>Pitch and live PR queues remain informational follow-ups because this run could not safely add those endpoints through the connector.</p>
          </div>
        </aside>
      </div>

      <article v-if="selectedProject" class="rounded-2xl border border-base-300 bg-base-100 p-5 shadow-xl">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-2xl font-black">{{ selectedProject.slug }}</h2>
          <span class="badge badge-outline badge-lg">{{ selectedProject.roadmap.kind }}</span>
        </div>
        <pre v-if="selectedProject.controlDirection" class="mb-5 whitespace-pre-wrap rounded-2xl bg-base-200 p-4 text-sm text-base-content/70">{{ selectedProject.controlDirection }}</pre>
        <div class="mb-5 grid gap-3 md:grid-cols-2">
          <div v-for="milestone in selectedProject.milestones" :key="milestone.id" class="rounded-2xl border border-base-300 p-4">
            <h3 class="font-bold">{{ milestone.id }} · {{ milestone.title }}</h3>
            <span class="badge mt-2" :class="statusTone(milestone.status ?? 'unknown')">{{ milestone.status ?? 'unknown' }}</span>
          </div>
        </div>
        <section v-for="(tasks, status) in groupedTasks" :key="status" class="mb-4 rounded-2xl bg-base-200 p-4 last:mb-0">
          <h3 class="mb-3 text-lg font-black"><span class="badge mr-2" :class="statusTone(String(status))">{{ status }}</span>{{ tasks.length }} tasks</h3>
          <article v-for="task in tasks" :key="task.id" class="mb-3 rounded-2xl border border-base-300 bg-base-100 p-4 last:mb-0">
            <p class="font-mono text-sm text-base-content/50">{{ task.id }} · {{ task.milestone }}</p>
            <h4 class="text-lg font-bold">{{ task.title }}</h4>
            <div class="mt-3 flex flex-wrap gap-2 text-sm">
              <span class="badge badge-outline">owner: {{ task.owner ?? 'none' }}</span>
              <span class="badge badge-outline">stakes: {{ task.stakes ?? 'unknown' }}</span>
              <span v-if="task.depends_on" class="badge badge-outline">depends: {{ task.depends_on }}</span>
              <span v-if="task.gate_human" class="badge badge-warning">human gate</span>
              <span v-if="task.approved_by_human" class="badge badge-success">approved</span>
            </div>
            <p v-if="task.note" class="mt-3 text-sm text-base-content/70">{{ task.note }}</p>
          </article>
        </section>
      </article>
    </section>
  </main>
</template>
