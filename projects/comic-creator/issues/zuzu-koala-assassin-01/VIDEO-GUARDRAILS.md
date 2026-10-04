# Zuzu: Koala Assassin — guardrails for videos made from this comic

Two Kind Robots video projects consume this issue (Silas, 2026-10-04):

| Video | Project | Tasks |
|---|---|---|
| Intro / title music video | `music-video` | t-024 brief → t-029 render and verdict |
| Issue 1 as an animated short | `comic-film` | t-003 shot list → t-009 render and verdict |

Both inherit the comic's look and canon from here. BRAINSTORM-ROUND-3.md is the source of truth
wherever it disagrees with the v0 SERIES-BIBLE.md or ISSUE-01-SCRIPT.md.

## Look

- **Stills and keyframes:** render through the Comic Studio series `zuzu-koala-assassin` house lane, currently `Illustrious/furrytoonmix_xlV3.safetensors` (t-018 may replace it). Use the lane's prefix and suffix, plus the series negatives.
- **Character shots:** start from vetted comic attempts (verdict selected or liked) rather than fresh renders, until the design pick (t-015) and the character LoRAs (t-016) land.
- **Clip motion prompts:** write them in prose: camera movement plus one action. No art-direction jargon.

## Canon in every prompt

- **Zuzu is always serious:** Clint Eastwood stillness, never a smiling sensei.
- **The siblings are fennec foxes:** a gaunt sister of about ten and a toddler brother who only babbles. Both are starving, beaten and frightened.
- **Action over exposition:** issue 1 has about 60 words of dialogue. Backstory comes through movement.
- **Rated teen:** show violence only as aftermath, with no gore on screen.
- **Placeholders, not canon:** the v0 Kind Robots world (Gallowsun Junction, the Stationmaster, Tomoe, Old Shelba, contract-language captions). Use none of it.

## bannedTerms (never in any positive prompt, lyric, caption or title)

The buried twist stays secret until Silas picks the issue that reveals it. Copy this list into
`settings.bannedTerms` on every Zuzu video. The server refuses any scene prompt containing a term,
on every engine (music-video t-025).

```
human, humans, humanity, mankind, people, pharmacy, great wall, skyscraper, highway,
billboard, road sign, english lettering, gore, dismembered, decapitated
```

`people` is on the list because every character is an animal. In a prompt, say "townsfolk" or name
the species instead. The words "statue" and "ruins" are allowed for ordinary weird-west sets. Never
pair them with a giant figure or with lettering.
