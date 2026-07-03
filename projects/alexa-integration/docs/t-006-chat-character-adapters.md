# alexa-integration/t-006 — Chat and Character adapter patch

The intended code target is `silasfelinus/serendipity-voice`. During this Worker run, the GitHub connector allowed reading that repository but blocked creating the required `worker/alexa-integration-t-006` branch there. This document preserves the exact safe implementation plan and patch shape so a local-code or Claude session with branch-write access can apply it without re-designing the task.

No live endpoint, deploy, DNS, secret, billing, or production-data action was performed.

## Intended behavior

Wire the existing `parseSerendipityVoiceRequest()` output to a local adapter layer that can handle:

- `domain: "chat"` requests such as `Serendipity: ask AMI why my relay is cranky`
- `domain: "character"` requests such as `Serendipity: have Professor Sparklebiscuit explain this as a dungeon quest`

The adapter should return a short spoken answer and an optional longer transcript payload. It must not write production data, bypass auth, or call Kind Robots unless a caller explicitly provides a safe app-owned client.

## Add `src/kind-robots-adapters.ts`

```ts
import type { SerendipityVoiceRequest } from './voice-router.js'

export type VoiceAdapterResponse = {
  spokenText: string
  transcript?: string
  domain: 'chat' | 'character'
  characterSlug?: string
  source: 'draft' | 'kind-robots'
}

export type ChatAdapterInput = {
  prompt: string
  characterSlug?: string
}

export type KindRobotsVoiceClient = {
  generateChat(input: ChatAdapterInput): Promise<{ text: string; transcript?: string }>
}

function oneLine(value: string): string {
  return value.trim().replace(/\s+/g, ' ')
}

function trimForSpeech(value: string, maxLength = 280): string {
  const normalized = oneLine(value)
  if (normalized.length <= maxLength) return normalized
  return `${normalized.slice(0, maxLength - 1).trimEnd()}…`
}

function fallbackDraft(request: SerendipityVoiceRequest): VoiceAdapterResponse {
  const characterSlug = request.domain === 'character' ? request.characterSlug : undefined
  const voiceName = characterSlug ? characterSlug.replace(/-/g, ' ') : 'AMI'
  const spokenText = trimForSpeech(`${voiceName} says: I can help with ${request.userIntent}. I need a connected Kind Robots chat client before I can generate the full answer.`)

  return {
    spokenText,
    transcript: `Draft voice response for ${request.domain}: ${request.userIntent}`,
    domain: request.domain === 'character' ? 'character' : 'chat',
    characterSlug,
    source: 'draft',
  }
}

export async function handleChatOrCharacterIntent(
  request: SerendipityVoiceRequest,
  client?: KindRobotsVoiceClient,
): Promise<VoiceAdapterResponse> {
  if (request.requiresConfirmation) {
    return {
      spokenText: request.clarification || 'I need one more detail before I can answer.',
      transcript: request.blockedReason,
      domain: request.domain === 'character' ? 'character' : 'chat',
      characterSlug: request.characterSlug,
      source: 'draft',
    }
  }

  if (request.domain !== 'chat' && request.domain !== 'character') {
    throw new Error(`Chat adapter cannot handle ${request.domain} requests.`)
  }

  if (!client) return fallbackDraft(request)

  const response = await client.generateChat({
    prompt: request.userIntent,
    characterSlug: request.domain === 'character' ? request.characterSlug : undefined,
  })

  return {
    spokenText: trimForSpeech(response.text),
    transcript: response.transcript || response.text,
    domain: request.domain === 'character' ? 'character' : 'chat',
    characterSlug: request.characterSlug,
    source: 'kind-robots',
  }
}
```

## Add `src/kind-robots-adapters.test.ts`

```ts
import assert from 'node:assert/strict'

import { handleChatOrCharacterIntent } from './kind-robots-adapters.js'
import { parseSerendipityVoiceRequest } from './voice-router.js'

const draftChat = await handleChatOrCharacterIntent(parseSerendipityVoiceRequest('Serendipity: why is the relay cranky'))
assert.equal(draftChat.domain, 'chat')
assert.equal(draftChat.source, 'draft')
assert.match(draftChat.spokenText, /AMI says/)

const draftCharacter = await handleChatOrCharacterIntent(parseSerendipityVoiceRequest('Serendipity: have Professor Sparklebiscuit explain this as a dungeon quest'))
assert.equal(draftCharacter.domain, 'character')
assert.equal(draftCharacter.characterSlug, 'professor-sparklebiscuit')
assert.equal(draftCharacter.source, 'draft')

const connectedCharacter = await handleChatOrCharacterIntent(
  parseSerendipityVoiceRequest('Serendipity: ask AMI why my relay is cranky'),
  {
    async generateChat(input) {
      assert.equal(input.characterSlug, 'ami')
      assert.equal(input.prompt, 'why my relay is cranky')
      return {
        text: 'The relay is cranky because it wants a clearer adapter boundary and a snack.',
        transcript: 'Full transcript: adapter boundary, auth context, and snack diplomacy.',
      }
    },
  },
)
assert.equal(connectedCharacter.domain, 'character')
assert.equal(connectedCharacter.source, 'kind-robots')
assert.match(connectedCharacter.spokenText, /clearer adapter boundary/)
assert.match(connectedCharacter.transcript || '', /snack diplomacy/)

await assert.rejects(
  () => handleChatOrCharacterIntent(parseSerendipityVoiceRequest('Serendipity: play rainy day coding playlist')),
  /Chat adapter cannot handle music requests/,
)

console.log('kind-robots-adapters: 4 checks passed')
```

## Update `package.json`

Change the test script from:

```json
"test": "tsx src/voice-router.test.ts"
```

to:

```json
"test": "tsx src/voice-router.test.ts && tsx src/kind-robots-adapters.test.ts"
```

## Verification to run locally

```bash
npm test
npm run typecheck
```

Expected results:

- `voice-router: 9 checks passed`
- `kind-robots-adapters: 4 checks passed`
- `tsc --noEmit` clean

## Roadmap recommendation

Because the connector blocked the actual branch in `silasfelinus/serendipity-voice`, leave `alexa-integration/t-006` at `needs-human` with this document linked. A local-code Worker/Claude pass can apply the patch in the target repo, then mark the task `done` after PR merge.
