import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()
const service = 'Humboldt Scoop CMS'

app.get('/', (c) => c.json({ success: true, service, message: 'Service is running. Dummy data only.' }))
app.get('/health', (c) => c.json({ success: true, status: 'ok', service: 'humboldt-scoop-cms', timestamp: new Date().toISOString() }))

const port = Number.parseInt(process.env.PORT ?? '3000', 10)

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`${service} listening on http://localhost:${info.port}`)
})
