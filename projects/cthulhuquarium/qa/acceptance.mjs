// Cthulhuquarium cross-device acceptance pass (conductor cthulhuquarium/t-089,
// t-091, t-095). Drives a LOCAL kind_robots dev server (never production):
//
//   node projects/cthulhuquarium/qa/acceptance.mjs OUT_DIR [--only 390x844 | --only reduced]
//
// Needs the local MariaDB (`mysql -uroot kindrobots`) the dev server uses.
// Per viewport: a fresh player with ten species and the Below Stairs key for
// sale; the title card; every console room; the key purchase into its scene,
// a reply and the handover; settings; the Memory Book with its endings shelf;
// keyboard-only room cycling. Checks no outer scroll or sideways overflow on
// every screen and no page errors. Then one reduced-motion run with every
// character portrait 404ing, to prove the scene still plays.
import { execFileSync } from 'node:child_process'
import { mkdirSync, readFileSync } from 'node:fs'
import { createRequire } from 'node:module'

const require = createRequire(import.meta.url)
let chromium
try {
  chromium = require('playwright').chromium
} catch {
  chromium = createRequire('/home/user/kind_robots/package.json')('playwright').chromium
}

const BASE = process.env.CQ_BASE ?? 'http://127.0.0.1:3000'
const OUT = process.argv[2] ?? 'cq-acceptance'
const only = process.argv.includes('--only') ? process.argv[process.argv.indexOf('--only') + 1] : null
mkdirSync(OUT, { recursive: true })
const sql = (q) =>
  execFileSync('mysql', ['-uroot', 'kindrobots', '-N', '-e', q]).toString().trim()

const KR = process.env.KIND_ROBOTS_DIR ?? '/home/user/kind_robots'
const generated = readFileSync(`${KR}/server/utils/cthulhuquariumBackgrounds.generated.ts`, 'utf8')
const SCENE_IDS = [
  ...generated
    .slice(generated.indexOf('CTHULHUQUARIUM_SCENE_IDS'))
    .split('\n]')[0]
    .matchAll(/'([a-z0-9_]+)'/g),
].map((m) => m[1])

const VIEWPORTS = [
  ['phone', 390, 844],
  ['tablet', 768, 1024],
  ['tablet-tall', 1024, 1366],
  ['tablet-landscape', 1366, 1024],
  ['desktop', 1440, 900],
  ['short-wide', 1280, 600],
]

const results = []
const check = (vp, cond, msg) => {
  results.push({ vp, ok: !!cond, msg })
  console.log(`${cond ? 'ok  ' : 'FAIL'} [${vp}] ${msg}`)
}

async function api(path, body, token) {
  const res = await fetch(BASE + path, {
    method: body ? 'POST' : 'GET',
    headers: {
      'content-type': 'application/json',
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  return res.json().catch(() => ({}))
}

async function freshPlayer() {
  const username = `qa${Date.now() % 1000000}`
  const password = 'deep-water-123'
  await api('/api/users/register', { username, password })
  const token = (await api('/api/auth/login', { username, password })).data.token
  await api('/api/aquarium/catalog?take=24', null, token)
  const uid = sql(`select id from User where username='${username}'`)
  const tank = sql(`select id from Aquarium where userId=${uid}`)
  sql(`update Aquarium set coins=100000 where id=${tank}`)
  sql(`update User set introDismissedAt=NOW() where id=${uid}`)
  // Room for ten species of any size (a fixture, not a purchase).
  sql(`update Aquarium set sizeCap=40 where id=${tank}`)
  const shelf = (await api('/api/aquarium/catalog?take=60', null, token)).data
  let bought = 0
  const refused = []
  for (const m of shelf) {
    if (bought >= 10) break
    const r = await api('/api/aquarium/purchase', { type: 'species', monsterId: m.id }, token)
    if (r.success) bought++
    else refused.push(r.message)
  }
  if (bought < 10) throw new Error(`fixture: only ${bought} species bought (${refused.slice(0, 3).join(' | ')})`)
  await api('/api/aquarium/feed', {}, token)
  // Every scene seen except Below Stairs', which the key purchase plays.
  for (const id of SCENE_IDS) {
    if (id === 'milestone_bestiary_10') continue
    sql(`insert ignore into AquariumEvent (aquariumId, kind) values (${tank}, 'story-seen-${id}')`)
  }
  // Reconcile now, so the milestones exist before they are re-dated (the
  // page load would otherwise write them after, and grandfather the key).
  await api('/api/aquarium/story/reconcile', {}, token)
  // Fixture milestones are dated after FLOOR_KEYS_INTRODUCED_AT, so the tank
  // is a new player's (who must buy the key), not a grandfathered veteran's.
  sql(`update AquariumEvent set occurredAt=GREATEST(NOW(), '2026-11-22 01:00:00') where aquariumId=${tank} and kind like 'milestone-%'`)
  sql(`delete from AquariumEvent where aquariumId=${tank} and kind like 'floor-key-%'`)
  sql(`update Aquarium set coins=100000 where id=${tank}`)
  return { username, token, tank, uid }
}

async function noOuterScroll(page) {
  return page.evaluate(() => {
    const d = document.documentElement
    return {
      vertical: d.scrollHeight - window.innerHeight,
      sideways: d.scrollWidth - window.innerWidth,
    }
  })
}

async function shot(page, name) {
  await page.screenshot({ path: `${OUT}/${name}.png` })
}

async function screen(page, vp, label) {
  const o = await noOuterScroll(page)
  check(vp, o.vertical <= 1 && o.sideways <= 1, `${label}: no outer scroll (v ${o.vertical}, h ${o.sideways})`)
  await shot(page, `${vp}-${label}`)
}

async function walkScene(page, replyFirst) {
  const stage = page.locator('.cq-vn-stage')
  let replied = false
  for (let i = 0; i < 30; i++) {
    if (!(await stage.count())) return { closed: true, replied }
    const reply = page.locator('[data-testid^="cq-reply-"]')
    if (replyFirst && !replied && (await reply.count())) {
      await page.waitForTimeout(700)
      await reply.first().click()
      replied = true
      await page.waitForTimeout(900)
      continue
    }
    const handover = page.locator('.cq-vn-stage button.btn-primary')
    if (await handover.count()) {
      await handover.first().click()
      await page.waitForTimeout(900)
      continue
    }
    await page.keyboard.press('Space')
    await page.waitForTimeout(120)
    await page.keyboard.press('Space')
    await page.waitForTimeout(350)
  }
  return { closed: !(await stage.count()), replied }
}

async function runViewport([vp, width, height]) {
  const player = await freshPlayer()
  const browser = await chromium.launch()
  const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 })
  await context.addCookies([{ name: 'kind-session', value: player.token, url: BASE }])
  await context.addInitScript((t) => {
    try {
      localStorage.setItem('token', t)
      localStorage.setItem('cthulhuquarium:guide-seen', 'seen')
    } catch {}
  }, player.token)
  const page = await context.newPage()
  const errors = []
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 200)))
  await page.goto(`${BASE}/play/aquarium`, { waitUntil: 'domcontentloaded', timeout: 240000 })

  // Title card.
  const title = page.locator('#cq-title-wordmark')
  await title.waitFor({ timeout: 240000 }).catch(() => {})
  check(vp, await title.count(), 'title card shows on a fresh browser session')
  if (await title.count()) {
    await page.waitForTimeout(500)
    await screen(page, vp, '01-title')
    await page.getByRole('button', { name: 'Enter the tank' }).click()
    await page.waitForTimeout(800)
  }

  // The tank and every room.
  // Wait for the game's own HUD: in dev, Vite can reload the page once while
  // it optimises dependencies, and the site loader also draws on a canvas.
  await page.locator('.cq-capsules').waitFor({ state: 'visible', timeout: 240000 })
  await page.locator('.cq-glass canvas').waitFor({ timeout: 60000 })
  await page.locator('.loader-root').waitFor({ state: 'detached', timeout: 120000 }).catch(() => {})
  check(vp, (await page.locator('.cq-glass canvas').count()) > 0, 'tank canvas renders')
  await screen(page, vp, '02-tank')
  for (const tab of ['feed', 'creatures', 'relics', 'market', 'tank']) {
    await page.locator(`[data-tab="${tab}"]`).click()
    await page.waitForTimeout(700)
    check(vp, (await page.locator(`[data-tab="${tab}"][aria-pressed="true"]`).count()) === 1, `room ${tab} opens`)
    if (tab !== 'tank') await screen(page, vp, `03-room-${tab}`)
  }

  // Keyboard: E cycles to the next room, Q back.
  await page.locator('body').click({ position: { x: 5, y: 5 } }).catch(() => {})
  await page.keyboard.press('e')
  await page.waitForTimeout(500)
  check(vp, (await page.locator('[data-tab="feed"][aria-pressed="true"]').count()) === 1, 'E moves to the next room')
  await page.keyboard.press('q')
  await page.waitForTimeout(500)
  check(vp, (await page.locator('[data-tab="tank"][aria-pressed="true"]').count()) === 1, 'Q moves back')
  await page.keyboard.press('Tab')
  const focusVisible = await page.evaluate(() => {
    const el = document.activeElement
    if (!el || el === document.body) return false
    const r = el.getBoundingClientRect()
    return r.width > 0 && r.bottom > 0 && r.top < window.innerHeight
  })
  check(vp, focusVisible, 'Tab lands on a visible control')

  // The key, its scene, a reply, the handover.
  await page.locator('[data-tab="market"]').click()
  await page.waitForTimeout(900)
  const key = page.locator('.cq-pedestal-key')
  check(vp, await key.count(), 'the key to Below Stairs is on sale')
  if (await key.count()) {
    await key.scrollIntoViewIfNeeded()
    await screen(page, vp, '04-market-key')
    await key.getByRole('button', { name: /Buy the key/ }).click()
    const stage = page.locator('.cq-vn-stage')
    await stage.waitFor({ timeout: 15000 }).catch(() => {})
    check(vp, await stage.count(), 'buying the key plays the floor scene')
    await page.waitForTimeout(600)
    await screen(page, vp, '05-scene')
    const walked = await walkScene(page, true)
    check(vp, walked.replied, 'a reply could be chosen')
    check(vp, walked.closed, 'the scene finishes and closes')
    const keys = sql(`select count(*) from AquariumEvent where aquariumId=${player.tank} and kind='floor-key-2'`)
    check(vp, keys === '1', `key recorded once (${keys})`)
  }

  // Settings.
  await page.keyboard.press('Escape')
  await page.locator('.cq-hud-button[aria-label="Settings"]').click()
  await page.waitForTimeout(600)
  const settings = page.getByRole('button', { name: 'Close settings' })
  check(vp, await settings.count(), 'settings open from the HUD')
  await screen(page, vp, '06-settings')
  await page.keyboard.press('Escape')
  await page.waitForTimeout(400)
  check(vp, !(await settings.count()), 'Esc closes settings')

  // Memory Book and endings.
  // The HUD button is hidden at phone width; the Tank room's prompt is the way in.
  const worldHud = page.locator('.cq-hud-button[aria-label="World and story"]')
  if (await worldHud.isVisible()) {
    await worldHud.click()
  } else {
    await page.locator('[data-tab="tank"]').click()
    await page.waitForTimeout(400)
    await page.locator('.cq-prompt', { hasText: 'World & story' }).click()
  }
  await page.waitForTimeout(900)
  const book = page.locator('.cq-memory-book')
  check(vp, await book.count(), 'Memory Book opens')
  if (await book.count()) {
    await book.scrollIntoViewIfNeeded()
    check(vp, (await page.locator('.cq-endings li').count()) === 3, 'three endings on the shelf')
    await screen(page, vp, '07-memory-book')
  }
  check(vp, errors.length === 0, `no page errors (${errors.slice(0, 2).join(' | ')})`)
  await browser.close()
}

async function runReducedMotionMissingArt() {
  const vp = 'reduced-motion-404'
  const player = await freshPlayer()
  const browser = await chromium.launch()
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    reducedMotion: 'reduce',
  })
  await context.addCookies([{ name: 'kind-session', value: player.token, url: BASE }])
  await context.addInitScript((t) => {
    try {
      localStorage.setItem('token', t)
      localStorage.setItem('cthulhuquarium:guide-seen', 'seen')
      sessionStorage.setItem('cthulhuquarium:title-seen', 'seen')
    } catch {}
  }, player.token)
  // Only image requests: in dev, Vite also serves imported images as JS
  // modules (`?import`), and 404ing those breaks the page, not the art.
  await context.route(/(charlotte|wilbur)[^/]*\.(webp|png)/, (route) =>
    route.request().resourceType() === 'image'
      ? route.fulfill({ status: 404, body: '' })
      : route.continue(),
  )
  const page = await context.newPage()
  const errors = []
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 200)))
  await page.goto(`${BASE}/play/aquarium`, { waitUntil: 'domcontentloaded', timeout: 240000 })
  await page.locator('canvas').first().waitFor({ timeout: 240000 })
  await page.locator('[data-tab="market"]').click()
  await page.waitForTimeout(900)
  await page.locator('.cq-pedestal-key').getByRole('button', { name: /Buy the key/ }).click()
  const stage = page.locator('.cq-vn-stage')
  await stage.waitFor({ timeout: 15000 }).catch(() => {})
  check(vp, await stage.count(), 'scene plays with every portrait missing')
  const broken = await page.evaluate(() =>
    [...document.querySelectorAll('.cq-vn-stage img')].filter(
      (img) => img.complete && img.naturalWidth === 0 && img.getAttribute('alt') !== '' && getComputedStyle(img).display !== 'none' && getComputedStyle(img).visibility !== 'hidden',
    ).length,
  )
  check(vp, broken === 0, `no visible broken image (alt text or icon) on stage (${broken})`)
  await shot(page, `${vp}-scene`)
  const walked = await walkScene(page, true)
  check(vp, walked.closed, 'scene still finishes under reduced motion')
  check(vp, errors.length === 0, `no page errors (${errors.slice(0, 2).join(' | ')})`)
  await browser.close()
}

for (const v of VIEWPORTS) {
  if (only && `${v[1]}x${v[2]}` !== only) continue
  try {
    await runViewport(v)
  } catch (error) {
    check(v[0], false, `run crashed: ${String(error).slice(0, 300)}`)
  }
}
if (!only || only === 'reduced') {
  try {
    await runReducedMotionMissingArt()
  } catch (error) {
    check('reduced-motion-404', false, `run crashed: ${String(error).slice(0, 300)}`)
  }
}
const failed = results.filter((r) => !r.ok)
console.log(`\n${results.length - failed.length}/${results.length} checks passed`)
process.exit(failed.length ? 1 : 0)
