import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.json({
  success: true,
  service: 'Humboldt Poop Scoop CMS',
  message: 'Skeleton app is running. Dummy data only.',
}))

app.get('/health', (c) => c.json({
  success: true,
  status: 'ok',
  service: 'humboldt-poop-scoop-cms',
  timestamp: new Date().toISOString(),
}))

const port = Number.parseInt(process.env.PORT ?? '3000', 10)

serve({
  fetch: app.fetch,
  port,
}, (info) => {
  console.log(`Humboldt Poop Scoop CMS listening on http://localhost:${info.port}`)
})
