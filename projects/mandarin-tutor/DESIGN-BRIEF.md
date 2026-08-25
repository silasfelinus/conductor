# Mandarin Tutor — Design Brief

## What it is

Mandarin Tutor is a visual, linguistics-forward Mandarin learning surface in Kind Robots. It combines ordinary vocabulary flashcards with the information that makes Chinese writing memorable: pronunciation, meaningful and phonetic components, traditional forms where useful, and sourced notes on how characters developed.

The first product is a responsive web app under **Play > Mandarin**. The domain must stay portable enough for later iOS and Android clients.

## Learning rule

**Teach the character that exists, not a mnemonic pretending to be history.**

A useful card can say that `说` uses the speech component `讠` and a phonetic component related to `兑`, but the UI must distinguish:

- the radical/indexing component;
- components that contribute meaning;
- components that primarily contribute sound;
- modern simplified substitutions;
- uncertain or disputed historical explanations;
- learner mnemonics, if added later, which are not etymology.

The tutor should reward curiosity without manufacturing tidy stories where scholarship is messy.

## Card model

A lexical card should be able to carry:

- stable key;
- simplified Hanzi;
- traditional Hanzi where different;
- tone-marked pinyin and normalized pronunciation identity;
- concise beginner meaning plus optional additional senses;
- lexical type (word, character, component, phrase);
- part of speech where useful;
- frequency / curriculum rank;
- categories and study-set membership;
- official-test/version tags;
- radical/indexing data;
- per-character component decomposition;
- component role: semantic, phonetic, form/indexing, or uncertain;
- source-backed historical/etymological note with provenance/confidence;
- classifiers / measure words where relevant;
- example usage in later iterations;
- illustration eligibility, ArtJob identity, and completed image identity;
- pronunciation-audio identity and asset URL/status.

Lexicon facts are shared. Learner progress and custom set membership are user state and must not duplicate or mutate canonical lexical facts.

## Starter curriculum

The first useful release targets **at least 500 lexical or component cards** and should feel like a serious beginner deck rather than an exam dump.

Built-in categories should include at minimum:

- numbers and money;
- colors;
- animals;
- family and people;
- body and health basics;
- food and drink;
- home and everyday objects;
- school and learning;
- work and occupations;
- travel and transportation;
- places and directions;
- weather and nature;
- dates, time, and calendar language;
- clothing;
- shopping;
- common verbs;
- common adjectives;
- question words and high-frequency function words;
- greetings and practical phrases.

Cards can belong to many categories. Users can build arbitrary custom sets without copying card data.

### Casino / gambling set

A dedicated practical set should cover language useful to a working casino dealer, including:

- wager/bet, chip, cash, table, hand, deck, card;
- suits and ranks;
- dealer, player, house;
- shuffle, cut, deal, draw, hold, fold, hit/stand where game-appropriate;
- win, lose, tie/push;
- odds, payout, limit, minimum/maximum;
- buy-in, cash-out, change;
- totals, money amounts, multipliers, fractions, and common number patterns;
- polite table instructions and customer-facing phrases;
- game-specific terminology added as real use reveals gaps.

Casino terms should include usage notes when literal dictionary Mandarin is not what speakers normally say at a table.

## Study experience

The primary card should be image-forward when an illustration helps memory. The learner can progressively reveal:

1. image / prompt side;
2. Hanzi;
3. pinyin and audio;
4. meaning;
5. word segmentation;
6. character components;
7. component roles and meanings;
8. historical development / traditional form;
9. source/provenance details.

The depth is optional per review. A learner who only wants a fast ten-card drill should not have to read a paleography essay, while the essay remains one tap away.

## Requested words

The user can request a Mandarin word, Hanzi form, pinyin, or English concept.

The application should:

1. resolve or create a structured lexical card;
2. show translation and pronunciation immediately;
3. flag uncertain generated linguistic fields for later curation rather than presenting them as canonical fact;
4. enqueue an appropriate **Krea 2** illustration through the existing durable `POST /api/art/enqueue` path when imagery is useful;
5. deduplicate image work with a stable Mandarin-card key;
6. make the card available to custom sets immediately while media completes asynchronously.

## Art contract

Do not create another render queue. Reuse Kind Robots:

```text
Mandarin card/request
  -> /api/art/enqueue (engine: krea2, projectSlug: mandarin-tutor)
  -> durable ArtJob
  -> kr-relay / Comfy
  -> ArtImage
  -> Mandarin card media association
```

An illustration depicts the *meaning* in a memorable, culturally sensible scene. It should not ask the image model to draw correct Chinese text. Hanzi itself is rendered by the web UI using fonts/text, not baked into generated art.

Abstract grammar/function cards and tiny components do not require decorative images merely to make a coverage counter green.

## Pronunciation and audio

Every lexical card requires tone-marked pinyin and a playback control. Audio should have deterministic identity based on the spoken Mandarin text plus voice/version so it can be cached and reused. The text/pinyin remains canonical even if audio generation is temporarily unavailable.

The web implementation should prefer a durable Kind Robots speech/audio asset when available. Browser speech synthesis may be a fallback, not the long-term definition of “audio clip.”

## Proficiency alignment

Test alignment is metadata, not the ontology of Mandarin.

Each curriculum mapping must record the source/standard/version it refers to. Future reports should answer questions such as:

- What vocabulary for target HSK level/version is covered?
- What required characters are covered?
- Which words have pronunciation/listening material?
- What reading/listening/grammar competencies are outside a flashcard catalog and need separate exercises?

This prevents a future HSK revision from silently changing what an existing “Level 2” badge means.

## Data sourcing and licensing

Open vocabulary datasets may bootstrap simplified/traditional forms, pinyin, definitions, radicals, frequency, and HSK membership. Character decomposition and historical claims need a source designed for those facts rather than inference from the radical alone.

Before vendoring any third-party dataset:

- verify its current license;
- preserve required attribution/license notices;
- transform only the fields needed by the app;
- record source/version in generated catalog metadata;
- avoid silently combining contradictory etymologies.

## Learning state

The first web implementation may use Pinia-owned local persistence for lightweight study state if that gets the learning loop in hand quickly, but the domain shape must support later authenticated sync. Components do not call `localStorage` directly.

Longer-term learner state should support:

- set membership;
- review history;
- recall/mastery state;
- due dates / spaced repetition;
- separate recognition dimensions where useful (meaning, Hanzi, pronunciation);
- import/export or server sync for mobile clients.

## Definition of the first useful release

A learner can open Play > Mandarin, choose a useful built-in category, study a deck from a 500+ card catalog, hear every studied word, reveal how a character is constructed, inspect a sourced history note when available, and create a custom set. Missing generated art does not block study; completed Krea 2 images appear as the ArtJob pipeline fills the catalog.
