// Render promo-1080x1350.html to hopeful-hues-promo-1080x1350.webp (via a PNG capture).
//   cd <kind_robots checkout> && node <this file> (playwright resolves there)
//   HOPEFUL_HUES_CHROMIUM=/path/to/chrome to pick a browser binary.
import { chromium } from 'playwright'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const env = globalThis.process.env
const browser = await chromium.launch(
  env.HOPEFUL_HUES_CHROMIUM ? { executablePath: env.HOPEFUL_HUES_CHROMIUM } : {},
)
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } })
await page.route('https://kindrobots.org/**', async (route) => {
  const upstream = await fetch(route.request().url())
  await route.fulfill({
    status: upstream.status,
    contentType: upstream.headers.get('content-type') || 'image/webp',
    body: Buffer.from(await upstream.arrayBuffer()),
  })
})
await page.goto('file://' + join(here, 'promo-1080x1350.html'))
await page.waitForLoadState('networkidle')
await page.screenshot({ path: join(here, 'hopeful-hues-promo-1080x1350.png') })
await browser.close()
