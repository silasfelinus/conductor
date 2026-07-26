import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import { seedData } from './schema.js'
import { planRoute, RoutePlanError } from './routing/planRoute.js'
import type { RoutePlanRequest } from './routing/types.js'

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
