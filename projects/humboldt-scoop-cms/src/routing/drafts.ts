import type { RoutePlanResponse } from './types.js'

/**
 * In-memory route-draft store for the dispatcher UI's "Save Draft" action
 * (humboldt-scoop-cms/t-008). Dummy data only -- drafts do not survive a
 * server restart. Move to a real persistence layer once this project picks
 * a database (see roadmap.yaml milestones); this is a v1 placeholder, not a
 * design decision to keep drafts ephemeral forever.
 */
export type RouteDraft = {
  id: string
  createdAt: string
  label: string | null
  plan: RoutePlanResponse
}

const drafts = new Map<string, RouteDraft>()
let nextId = 1

export function saveDraft(plan: RoutePlanResponse, label: string | null = null): RouteDraft {
  const draft: RouteDraft = {
    id: `draft-${nextId++}`,
    createdAt: new Date().toISOString(),
    label,
    plan,
  }
  drafts.set(draft.id, draft)
  return draft
}

export function getDraft(id: string): RouteDraft | undefined {
  return drafts.get(id)
}

export function listDrafts(): RouteDraft[] {
  // Map iteration order is insertion order, so reversing gives newest-first
  // without relying on createdAt (two saves in the same millisecond would
  // otherwise tie and sort unpredictably).
  return Array.from(drafts.values()).reverse()
}

/** Test-only reset so drafts.test.ts runs don't leak state across test files. */
export function __resetDraftsForTest(): void {
  drafts.clear()
  nextId = 1
}
