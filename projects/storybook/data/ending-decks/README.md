# Ending decks

Authoring source for Storybook's ending decks (storybook/t-030). One YAML per deck; imported into
Kind Robots by `utils/scripts/seedStorybookDecks.ts` and verified by `verifyStorybookDecks.ts`.

Schema (see `../../docs/storymaker-redesign.md` § C7):

```yaml
key: genre-mystery            # EndingDeck.key, unique
title: Mystery
description: ...
ownerKind: GENRE_FACET        # LIFE | GENRE_FACET | SCENARIO
facetSlug: mystery            # or scenarioSlug for SCENARIO decks
axes:                         # bit order; outcomeKey[i] is axes[i], '1' = stat >= passValue
  - { key: truth, label: Truth, description: ..., passLabel: ..., failLabel: ... }
passValue: 1
turnBudgetByShape: { short-story: 5, chaptered: 8, episodic: 12 }
minTurnsBeforeResolve: null   # life: 6
endings:                      # exactly 2^len(axes) entries, one per outcomeKey
  - { outcomeKey: '111', title: ..., slug: ..., summary: ..., victoryType: VICTORY, artPrompt: ... }
```

`life.yaml` lists the Life deck's axes only; its 1,024 endings come from
`scripts/generate_davinci_endings.py` and `../../../davinci/data/ending-dimensions.yaml`.
Ending copy must be complete sentences that parse on their own (the `scripts/dream_prose_quality.py`
bar applies to card copy here too).
