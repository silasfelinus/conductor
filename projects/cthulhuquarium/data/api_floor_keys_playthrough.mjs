// API play-through of t-105 (canon rarity + floor keys) against the local server.
import { execFileSync } from 'node:child_process'
const BASE = 'http://127.0.0.1:3000'
const user = `keyer${Date.now() % 100000}`
const pass = 'deep-water-123'
const sql = (q) =>
  execFileSync('mysql', ['-uroot', 'kindrobots', '-N', '-e', q]).toString().trim()
let token = ''
async function api(path, body) {
  const res = await fetch(BASE + path, {
    method: body ? 'POST' : 'GET',
    headers: {
      'content-type': 'application/json',
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  const json = await res.json().catch(() => ({}))
  return { status: res.status, ...json }
}
let failed = 0
const ok = (cond, msg) => {
  if (!cond) failed++
  console.log(cond ? 'ok  ' : 'FAIL', msg)
}

await api('/api/users/register', { username: user, password: pass })
token = (await api('/api/auth/login', { username: user, password: pass })).data.token
let cat = await api('/api/aquarium/catalog?take=24')
const uid = sql(`select id from User where username='${user}'`)
const tank = sql(`select id from Aquarium where userId=${uid}`)
sql(`update Aquarium set coins=2000000 where id=${tank}`)

// Canon rarity: a common is priced as a common.
const commonRareStats = sql(
  `select id from Monster where depth=1 and tier='COMMON' and unlockCost=0 and (wits<>'COMMON' or charm<>'COMMON' or might<>'COMMON') limit 1`,
)
const commons = sql(`select id from Monster where depth=1 order by id limit 10`).split('\n').map(Number)
for (const id of commons) {
  const r = await api('/api/aquarium/purchase', { type: 'species', monsterId: id })
  if (!r.success) ok(false, `buy common ${id}: ${r.message}`)
}
const stock = (await api('/api/aquarium')).data?.Stock ?? []
const values = new Set(stock.map((s) => s.coinValue))
ok(
  stock.every((s) => s.Monster.tier !== 'COMMON' || s.coinValue === 3),
  `every COMMON fish drops a 3-coin coin (values seen: ${[...values].join(',')})`,
)

cat = await api('/api/aquarium/catalog?take=24')
ok(cat.meta.floor.floor === 1, 'ten species but no key: still floor I')
ok(cat.meta.floor.next.keyForSale === true, `key to II for sale at ${cat.meta.floor.next.keyCost}`)
ok(cat.data.every((m) => m.depth === 1), 'no floor II stock without the key')
const tier2 = sql(`select id from Monster where depth=2 limit 1`)
let r = await api('/api/aquarium/purchase', { type: 'species', monsterId: Number(tier2) })
ok(r.status === 403, `floor II species refused without the key (${r.status})`)
r = await api('/api/aquarium/floor-key', { floor: 3 })
ok(r.status === 403, `key III refused before II (${r.status})`)
r = await api('/api/aquarium/floor-key', { floor: 7 })
ok(r.status === 400, `nonsense floor refused (${r.status})`)
sql(`update Aquarium set coins=10 where id=${tank}`)
r = await api('/api/aquarium/floor-key', { floor: 2 })
ok(r.status === 402, `key refused without the coins (${r.status})`)
sql(`update Aquarium set coins=2000000 where id=${tank}`)
const [a, b] = await Promise.all([
  api('/api/aquarium/floor-key', { floor: 2 }),
  api('/api/aquarium/floor-key', { floor: 2 }),
])
ok([a, b].filter((x) => x.success).length === 1, `a double tap buys the key once (${a.status}/${b.status})`)
const keys = sql(`select count(*) from AquariumEvent where aquariumId=${tank} and kind='floor-key-2'`)
ok(keys === '1', `one key-2 event (${keys})`)
const coinsAfter = Number(sql(`select coins from Aquarium where id=${tank}`))
ok(coinsAfter === 2000000 - 150, `charged exactly once: ${2000000 - coinsAfter}`)
cat = await api('/api/aquarium/catalog?take=24')
ok(cat.meta.floor.floor === 2 && cat.data.some((m) => m.depth === 2), 'floor II open and stocked')
let story = await api('/api/aquarium/story')
ok(story.data.floorKeys?.includes(2) && story.data.floor === 2, 'story state knows the key')

// Grandfathering: a tank whose milestones predate keys gets them free once.
const user2 = `veteran${Date.now() % 100000}`
await api('/api/users/register', { username: user2, password: pass })
token = (await api('/api/auth/login', { username: user2, password: pass })).data.token
await api('/api/aquarium/catalog?take=1')
const uid2 = sql(`select id from User where username='${user2}'`)
const tank2 = sql(`select id from Aquarium where userId=${uid2}`)
const ids = sql(`select id from Monster where depth in (1,2) order by depth, id limit 30`).split('\n')
for (const id of ids) sql(`insert into AquariumCodexEntry (userId, monsterId) values (${uid2}, ${id})`)
sql(`insert into AquariumEvent (aquariumId, kind, occurredAt) values (${tank2}, 'milestone-bestiary_10', '2026-10-01'), (${tank2}, 'milestone-bestiary_25', '2026-10-02')`)
// A tank from before keys has no key-system marker (new tanks get one at birth).
sql(`delete from AquariumEvent where aquariumId=${tank2} and kind='floor-keys-introduced'`)
await api('/api/aquarium/story/reconcile', {})
story = await api('/api/aquarium/story')
ok(
  story.data.floorKeys?.includes(2) && story.data.floorKeys?.includes(3) && story.data.floor === 3,
  `veteran keeps floors II and III (keys ${story.data.floorKeys})`,
)
await api('/api/aquarium/story/reconcile', {})
const vk = sql(`select count(*) from AquariumEvent where aquariumId=${tank2} and kind like 'floor-key-%'`)
ok(vk === '2', `granted once, not twice (${vk})`)
console.log(failed ? `${failed} FAILED` : 'all passed')
