import { serve } from '@hono/node-server'
import { serveStatic } from '@hono/node-server/serve-static'
import { Hono } from 'hono'
import { seedData } from './schema.js'
import { collectEligibleStops, planRoute, RoutePlanError } from './routing/planRoute.js'
import { getDraft, listDrafts, saveDraft } from './routing/drafts.js'
import type { RoutePlanRequest, RoutePlanResponse } from './routing/types.js'
import { DISPATCH_PAGE_HTML } from './dispatchPage.js'

const app = new Hono()
const service = 'Humboldt Scoop CMS'

const DUMMY_NOTICE = 'Dummy data only. No real customer records.'

app.get('/', (c) => c.json({ success: true, service, message: 'Service is running. Dummy data only.' }))
app.get('/health', (c) => c.json({ success: true, status: 'ok', service: 'humboldt-scoop-cms', timestamp: new Date().toISOString() }))

// GET /customers — list all customers with their properties and pets
app.get('/customers', (c) => {
  const customers = seedData.customers.map((cus) => ({
    ...cus,
    properties: seedData.properties.filter((p) => p.customerId === cus.id),
    pets: seedData.pets.filter((p) => p.customerId === cus.id),
    activePlan: seedData.servicePlans.find((sp) => sp.customerId === cus.id && sp.status === 'active') ?? null,
  }))
  return c.json({ success: true, notice: DUMMY_NOTICE, data: customers })
})

// GET /customers/:id — single customer with full detail
app.get('/customers/:id', (c) => {
  const id = c.req.param('id')
  const customer = seedData.customers.find((cus) => cus.id === id)
  if (!customer) return c.json({ success: false, message: 'Customer not found' }, 404)
  return c.json({
    success: true,
    notice: DUMMY_NOTICE,
    data: {
      ...customer,
      properties: seedData.properties.filter((p) => p.customerId === id),
      pets: seedData.pets.filter((p) => p.customerId === id),
      servicePlans: seedData.servicePlans.filter((sp) => sp.customerId === id),
      visits: seedData.visits.filter((v) => v.customerId === id),
      draftInvoices: seedData.draftInvoices.filter((inv) => inv.customerId === id),
    },
  })
})

// GET /routes/today — route cards for all visits scheduled today (per SPEC.md fields)
app.get('/routes/today', (c) => {
  const todayPrefix = new Date().toISOString().slice(0, 10)
  const todayVisits = seedData.visits.filter((v) => v.scheduledFor.startsWith(todayPrefix))

  // If no visits match today (likely in dev with static dummy dates), return all scheduled
  const visits = todayVisits.length > 0 ? todayVisits : seedData.visits.filter((v) => v.status === 'scheduled')

  const routeCards = visits.map((visit, idx) => {
    const customer = seedData.customers.find((c) => c.id === visit.customerId)
    const property = seedData.properties.find((p) => p.id === visit.propertyId)
    const pets = seedData.pets.filter((p) => p.propertyId === visit.propertyId)
    const plan = seedData.servicePlans.find((sp) => sp.id === visit.servicePlanId)

    return {
      routeSlot: `Morning ${String(idx + 1).padStart(2, '0')}`,
      visitId: visit.id,
      visitDate: visit.scheduledFor,
      customerName: customer?.displayName ?? 'Unknown',
      neighborhood: `${property?.city ?? 'Unknown'} / dummy sample area`,
      propertyLabel: property?.label ?? 'Unknown yard',
      serviceFrequency: plan?.frequency ?? 'unknown',
      pets: pets.map((p) => ({
        name: p.name,
        species: p.species,
        breed: p.breed ?? null,
        temperament: p.temperament,
        notes: p.notes ?? null,
      })),
      yardNotes: property?.serviceNotes ?? null,
      gateDetailsPlaceholder: '[GATE DETAILS REDACTED / ENTERED BY APPROVED HUMAN WORKFLOW]',
      visitChecklist: [
        'Confirm correct property/yard label',
        'Check pet status before entering',
        'Scoop main yard',
        'Scoop side yard or marked secondary area',
        'Bag and dispose according to service notes',
        'Close and latch gates',
        'Record bags used',
        'Add crew notes if anything needs follow-up',
      ],
      crewNotes: visit.crewNotes ?? null,
      billingMode: 'Draft — dummy data only. No live billing.',
    }
  })

  return c.json({
    success: true,
    notice: DUMMY_NOTICE,
    date: todayPrefix,
    count: routeCards.length,
    data: routeCards,
  })
})

// GET /routes/eligible — eligible customers for a date/filter, before selection.
// Powers the dispatcher UI's customer checklist (humboldt-scoop-cms/t-008).
app.get('/routes/eligible', (c) => {
  const date = c.req.query('date')
  if (!date || !/^\d{4}-\d{2}-\d{2}/.test(date)) {
    return c.json({ success: false, message: 'date query param is required and must be an ISO date (YYYY-MM-DD...).' }, 400)
  }
  const neighborhood = c.req.query('neighborhood') || undefined
  const frequency = c.req.query('frequency') || undefined

  const { eligible, missingCoordinates } = collectEligibleStops(seedData, date, { neighborhood, frequency })
  return c.json({ success: true, notice: DUMMY_NOTICE, data: { eligible, missingCoordinates } })
})

// POST /routes/draft — save a planned route as a draft (dispatcher "Save Draft" action).
// In-memory only; see routing/drafts.ts.
app.post('/routes/draft', async (c) => {
  const body = await c.req.json().catch(() => null)
  const plan = (body as { plan?: RoutePlanResponse } | null)?.plan
  if (!plan || !Array.isArray(plan.stops) || typeof plan.date !== 'string') {
    return c.json({ success: false, message: 'Request body must include a plan (a full /routes/plan response).' }, 400)
  }
  const label = typeof (body as { label?: unknown }).label === 'string' ? (body as { label: string }).label : null
  const draft = saveDraft(plan, label)
  return c.json({ success: true, notice: DUMMY_NOTICE, data: draft })
})

// GET /routes/drafts — list saved drafts (summary only).
app.get('/routes/drafts', (c) => {
  const drafts = listDrafts().map((d) => ({
    id: d.id,
    createdAt: d.createdAt,
    label: d.label,
    date: d.plan.date,
    stopCount: d.plan.stops.length,
    distanceMeters: d.plan.totals.distanceMeters,
    durationSeconds: d.plan.totals.durationSeconds,
  }))
  return c.json({ success: true, notice: DUMMY_NOTICE, data: drafts })
})

// GET /routes/drafts/:id — full saved draft, including the complete plan.
app.get('/routes/drafts/:id', (c) => {
  const draft = getDraft(c.req.param('id'))
  if (!draft) return c.json({ success: false, message: 'Draft not found' }, 404)
  return c.json({ success: true, notice: DUMMY_NOTICE, data: draft })
})

// GET /dispatch — dispatcher map UI (humboldt-scoop-cms/t-008). Self-contained
// HTML/JS page; no build step, no framework, calls the JSON API above.
app.get('/dispatch', (c) => c.html(DISPATCH_PAGE_HTML))

// Serve Leaflet's own JS/CSS/marker images from node_modules -- vendored, not a
// CDN, so the dispatcher map works without an external script/style fetch at
// runtime (matches this project's self-hosting posture; only the map *tiles*
// still come from the public OpenStreetMap tile server -- see dispatchPage.ts).
app.use(
  '/vendor/leaflet/*',
  serveStatic({
    root: './node_modules/leaflet/dist',
    rewriteRequestPath: (path) => path.replace(/^\/vendor\/leaflet/, ''),
  }),
)

// POST /routes/plan — deterministic mapped route for a selected set of customers.
// See projects/humboldt-scoop-cms/route-planner/SPEC.md. No LLM involvement;
// routing/optimization is always algorithmic (haversine fallback or self-hosted OSRM).
app.post('/routes/plan', async (c) => {
  const body = await c.req.json().catch(() => null)
  const validationError = validateRoutePlanRequest(body)
  if (validationError) {
    return c.json({ success: false, message: validationError }, 400)
  }

  try {
    const plan = await planRoute(body as RoutePlanRequest, seedData)
    return c.json({ success: true, notice: DUMMY_NOTICE, data: plan })
  } catch (err) {
    if (err instanceof RoutePlanError) {
      return c.json({ success: false, message: err.message }, err.status as 400 | 422)
    }
    throw err
  }
})

function validateRoutePlanRequest(body: unknown): string | null {
  if (!body || typeof body !== 'object') return 'Request body must be a JSON object.'
  const req = body as Record<string, unknown>

  if (typeof req.date !== 'string' || !/^\d{4}-\d{2}-\d{2}/.test(req.date)) {
    return 'date is required and must be an ISO date (YYYY-MM-DD...).'
  }

  const start = req.start as Record<string, unknown> | undefined
  if (!start || typeof start.lat !== 'number' || typeof start.lng !== 'number') {
    return 'start is required and must include numeric lat/lng.'
  }

  if (req.end !== undefined) {
    const end = req.end as Record<string, unknown>
    if (typeof end.lat !== 'number' || typeof end.lng !== 'number') {
      return 'end, if provided, must include numeric lat/lng.'
    }
  }

  const selection = req.selection as Record<string, unknown> | undefined
  if (!selection || (selection.mode !== 'explicit' && selection.mode !== 'fill-to-n')) {
    return 'selection.mode is required and must be "explicit" or "fill-to-n".'
  }
  if (selection.mode === 'explicit') {
    if (!Array.isArray(selection.customerIds) || !selection.customerIds.every((id) => typeof id === 'string')) {
      return 'selection.customerIds is required for explicit mode and must be an array of strings.'
    }
  } else {
    if (typeof selection.count !== 'number') {
      return 'selection.count is required for fill-to-n mode and must be a number.'
    }
    if (selection.sortBy !== undefined && selection.sortBy !== 'earliest-due' && selection.sortBy !== 'proximity') {
      return 'selection.sortBy, if provided, must be "earliest-due" or "proximity".'
    }
  }

  if (req.locked !== undefined) {
    if (!Array.isArray(req.locked)) return 'locked, if provided, must be an array.'
    for (const lock of req.locked) {
      const l = lock as Record<string, unknown>
      if (typeof l?.customerId !== 'string' || typeof l?.position !== 'number') {
        return 'Each locked entry requires a string customerId and a numeric position.'
      }
    }
  }

  return null
}

const port = Number.parseInt(process.env.PORT ?? '3000', 10)

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`${service} listening on http://localhost:${info.port}`)
})
