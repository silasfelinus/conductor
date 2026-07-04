# alexa-integration/t-008 — Local music adapter handoff

Target repository: `silasfelinus/serendipity-voice`

Intended branch: `worker/alexa-integration-t-008`

Task: Prototype a local-only music playback adapter for requests like `Serendipity: play <music target>`.

## Tooling block

The GitHub connector blocked creating the required `worker/alexa-integration-t-008` branch in `silasfelinus/serendipity-voice`. Per AGENTS.md cross-repo fallback rules, this file preserves the exact intended patch instead of bypassing the branch boundary.

## Safety boundaries

- The adapter stays behind `SERENDIPITY_ENABLE_MUSIC`.
- The adapter reads only roots provided by `SERENDIPITY_MUSIC_LIBRARY_ROOT`.
- It searches for audio file names only and does not print absolute paths in voice output.
- It creates a local playback plan; it does not launch a player in this patch.
- It never mutates the music library.
- If multiple likely matches exist, it asks for a short clarification.

## Files to change in `silasfelinus/serendipity-voice`

- `src/adapters/music-adapter.ts`
- `src/adapters/music-adapter.test.ts`
- `src/handle-voice-request.test.ts`
- `src/run-all-tests.ts`

## Patch contents

### `src/adapters/music-adapter.ts`

```ts
import fs from 'node:fs'
import path from 'node:path'

import { loadRuntimeConfig, type RuntimeConfig } from '../runtime-config.js'
import type { SerendipityVoiceRequest } from '../voice-router.js'
import { makeVoiceResponse, type VoiceResponse } from '../voice-response.js'

const audioExtensions = new Set(['.mp3', '.flac', '.m4a', '.aac', '.ogg', '.opus', '.wav'])
const maxMatches = 6
const maxFilesScanned = 5000

export type MusicMatch = {
  title: string
  relativePath: string
  extension: string
}

export type MusicResolution =
  | {
      status: 'feature-flag-disabled'
      target: string
    }
  | {
      status: 'missing-library-root'
      target: string
    }
  | {
      status: 'no-match'
      target: string
      rootLabel: string
    }
  | {
      status: 'single-match'
      target: string
      rootLabel: string
      match: MusicMatch
    }
  | {
      status: 'multiple-matches'
      target: string
      rootLabel: string
      matches: MusicMatch[]
    }

function normalizeSearchText(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
}

function isAudioFile(filePath: string): boolean {
  return audioExtensions.has(path.extname(filePath).toLowerCase())
}

function toMusicMatch(root: string, filePath: string): MusicMatch {
  const relativePath = path.relative(root, filePath)
  const extension = path.extname(filePath).toLowerCase()
  const title = path.basename(filePath, extension).replace(/[_-]+/g, ' ').replace(/\s+/g, ' ').trim()
  return { title, relativePath, extension }
}

function collectMatches(root: string, target: string): MusicMatch[] {
  const normalizedTarget = normalizeSearchText(target)
  const matches: MusicMatch[] = []
  const stack = [root]
  let filesScanned = 0

  while (stack.length > 0 && matches.length < maxMatches && filesScanned < maxFilesScanned) {
    const current = stack.pop()
    if (!current) continue

    let entries: fs.Dirent[]
    try {
      entries = fs.readdirSync(current, { withFileTypes: true })
    } catch {
      continue
    }

    for (const entry of entries) {
      const entryPath = path.join(current, entry.name)
      if (entry.isDirectory()) {
        stack.push(entryPath)
        continue
      }

      if (!entry.isFile() || !isAudioFile(entryPath)) continue
      filesScanned += 1

      const match = toMusicMatch(root, entryPath)
      const haystack = normalizeSearchText(`${match.title} ${match.relativePath}`)
      if (haystack.includes(normalizedTarget)) matches.push(match)
      if (matches.length >= maxMatches || filesScanned >= maxFilesScanned) break
    }
  }

  return matches
}

function getRootLabel(root: string): string {
  return path.basename(root) || 'configured music library'
}

export function resolveMusicTarget(request: SerendipityVoiceRequest, config: RuntimeConfig = loadRuntimeConfig()): MusicResolution {
  const target = request.musicTarget ?? request.userIntent

  if (!config.enableMusic) {
    return { target, status: 'feature-flag-disabled' }
  }

  if (!config.musicLibraryRoot) {
    return { target, status: 'missing-library-root' }
  }

  const root = path.resolve(config.musicLibraryRoot)
  const rootLabel = getRootLabel(root)

  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    return { target, status: 'missing-library-root' }
  }

  const matches = collectMatches(root, target)
  if (matches.length === 0) return { target, rootLabel, status: 'no-match' }
  if (matches.length === 1) return { target, rootLabel, status: 'single-match', match: matches[0] }
  return { target, rootLabel, status: 'multiple-matches', matches }
}

export function handleMusicRequest(request: SerendipityVoiceRequest): VoiceResponse {
  const resolution = resolveMusicTarget(request)

  if (resolution.status === 'feature-flag-disabled') {
    return makeVoiceResponse({
      request,
      adapter: 'music',
      spokenText: `I recognized the music target ${resolution.target}, but local playback is disabled until you turn on the music feature flag.`,
      transcriptText: `Music request\nTarget: ${resolution.target}\nStatus: ${resolution.status}\nNo files were read, changed, or played.`,
      requiresConfirmation: true,
    })
  }

  if (resolution.status === 'missing-library-root') {
    return makeVoiceResponse({
      request,
      adapter: 'music',
      spokenText: 'Music is enabled, but I need a configured local music library root first.',
      transcriptText: `Music request\nTarget: ${resolution.target}\nStatus: ${resolution.status}\nSet SERENDIPITY_MUSIC_LIBRARY_ROOT to an approved local library root.`,
      requiresConfirmation: true,
    })
  }

  if (resolution.status === 'no-match') {
    return makeVoiceResponse({
      request,
      adapter: 'music',
      spokenText: `I could not find ${resolution.target} in the configured ${resolution.rootLabel} library.`,
      transcriptText: `Music request\nTarget: ${resolution.target}\nStatus: ${resolution.status}\nLibrary: ${resolution.rootLabel}`,
      requiresConfirmation: true,
    })
  }

  if (resolution.status === 'multiple-matches') {
    const choices = resolution.matches.map((match) => match.title).join(', ')
    return makeVoiceResponse({
      request,
      adapter: 'music',
      spokenText: `I found more than one match: ${choices}. Which one should I play?`,
      transcriptText: `Music request\nTarget: ${resolution.target}\nStatus: ${resolution.status}\nChoices:\n${resolution.matches.map((match) => `- ${match.title}`).join('\n')}`,
      requiresConfirmation: true,
    })
  }

  return makeVoiceResponse({
    request,
    adapter: 'music',
    spokenText: `I found ${resolution.match.title}. I can queue it for local playback once the player bridge is connected.`,
    transcriptText: `Music request\nTarget: ${resolution.target}\nStatus: ${resolution.status}\nLibrary: ${resolution.rootLabel}\nTrack: ${resolution.match.title}\nPlanned local path: ${resolution.match.relativePath}\nNo playback process was launched by this adapter.`,
    requiresConfirmation: true,
  })
}
```

### `src/adapters/music-adapter.test.ts`

```ts
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

import { resolveMusicTarget } from './music-adapter.js'
import { parseSerendipityVoiceRequest } from '../voice-router.js'

function makeRequest(text: string) {
  return parseSerendipityVoiceRequest(text)
}

const disabled = resolveMusicTarget(makeRequest('Serendipity: play rainy day coding playlist'), {
  mode: 'local',
  enableArt: false,
  enableMusic: false,
  kindRobotsBaseUrl: 'http://localhost:3000',
  conductorRepo: 'silasfelinus/conductor',
  musicLibraryRoot: '/music',
})
assert.equal(disabled.status, 'feature-flag-disabled')

const missingRoot = resolveMusicTarget(makeRequest('Serendipity: play rainy day coding playlist'), {
  mode: 'local',
  enableArt: false,
  enableMusic: true,
  kindRobotsBaseUrl: 'http://localhost:3000',
  conductorRepo: 'silasfelinus/conductor',
})
assert.equal(missingRoot.status, 'missing-library-root')

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'serendipity-music-'))
fs.mkdirSync(path.join(root, 'playlists'))
fs.writeFileSync(path.join(root, 'playlists', 'Rainy Day Coding Playlist.mp3'), 'fake audio')
fs.writeFileSync(path.join(root, 'playlists', 'Rainy Day Coding Playlist live.flac'), 'fake audio')
fs.writeFileSync(path.join(root, 'playlists', 'notes.txt'), 'not audio')
fs.mkdirSync(path.join(root, 'albums'))
fs.writeFileSync(path.join(root, 'albums', 'Robot Fox Theme.ogg'), 'fake audio')

const multiple = resolveMusicTarget(makeRequest('Serendipity: play rainy day coding playlist'), {
  mode: 'local',
  enableArt: false,
  enableMusic: true,
  kindRobotsBaseUrl: 'http://localhost:3000',
  conductorRepo: 'silasfelinus/conductor',
  musicLibraryRoot: root,
})
assert.equal(multiple.status, 'multiple-matches')
if (multiple.status === 'multiple-matches') {
  assert.equal(multiple.matches.length, 2)
  assert.deepEqual(
    multiple.matches.map((match) => match.title).sort(),
    ['Rainy Day Coding Playlist', 'Rainy Day Coding Playlist live'],
  )
}

const single = resolveMusicTarget(makeRequest('Serendipity: play robot fox theme'), {
  mode: 'local',
  enableArt: false,
  enableMusic: true,
  kindRobotsBaseUrl: 'http://localhost:3000',
  conductorRepo: 'silasfelinus/conductor',
  musicLibraryRoot: root,
})
assert.equal(single.status, 'single-match')
if (single.status === 'single-match') {
  assert.equal(single.match.title, 'Robot Fox Theme')
  assert.equal(single.match.relativePath, path.join('albums', 'Robot Fox Theme.ogg'))
}

const noMatch = resolveMusicTarget(makeRequest('Serendipity: play ocean jazz'), {
  mode: 'local',
  enableArt: false,
  enableMusic: true,
  kindRobotsBaseUrl: 'http://localhost:3000',
  conductorRepo: 'silasfelinus/conductor',
  musicLibraryRoot: root,
})
assert.equal(noMatch.status, 'no-match')

fs.rmSync(root, { recursive: true, force: true })

console.log('music-adapter: 5 checks passed')
```

### `src/handle-voice-request.test.ts`

Replace the existing music assertions with:

```ts
const music = handleVoiceRequest('Serendipity: play rainy day coding playlist')
assert.equal(music.adapter, 'music')
assert.equal(music.request.domain, 'music')
assert.equal(music.request.musicTarget, 'rainy day coding playlist')
assert.equal(music.requiresConfirmation, true)
assert.match(music.spokenText, /music target rainy day coding playlist/)
assert.match(music.transcriptText, /feature-flag-disabled/)
assert.match(music.transcriptText, /No files were read, changed, or played/)
```

Update the final log string from `10 checks passed` to remain accurate if desired, or leave it as-is because the file still exercises the same top-level cases.

### `src/run-all-tests.ts`

Add the adapter test import:

```ts
import './runtime-config.test.js'
import './voice-router.test.js'
import './adapters/music-adapter.test.js'
import './handle-voice-request.test.js'
import './alexa/skill-event.test.js'

console.log('all tests imported successfully')
```

## Verification still needed

Run in `silasfelinus/serendipity-voice` after applying the patch:

```bash
npm run test
npm run typecheck
```

## Expected behavior

- With `SERENDIPITY_ENABLE_MUSIC` unset or false, a music request remains recognized but disabled.
- With music enabled and no configured root, the adapter asks for `SERENDIPITY_MUSIC_LIBRARY_ROOT`.
- With one match, it returns a local playback plan without launching a player.
- With several matches, it asks which one to use.
- With no match, it reports that no configured-library match was found.

## Roadmap update note

The conductor roadmap claim/update also hit the connector safety filter because the full `projects/alexa-integration/roadmap.yaml` contains protected-infra boundary language. The intended roadmap state after applying this handoff should be soft `needs-human` unless the target patch is applied and merged in `serendipity-voice`, in which case `t-008` can be marked `done`.
