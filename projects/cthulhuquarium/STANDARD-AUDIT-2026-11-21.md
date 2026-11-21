# Cthulhuquarium — main-game standard, re-audit (t-100)

2026-11-21. This refreshes [STANDARD-AUDIT-2026-11-12.md](STANDARD-AUDIT-2026-11-12.md) after
kind_robots #5472, #5479, #5497 and #5498 and canon #82–#86. The evidence for each line is the
cross-device acceptance run in [`qa/`](qa/) (184 checks across six viewports, plus a
reduced-motion run with the portraits missing) and the code named in the table.

| Item | Status | Evidence | Remaining |
|---|---|---|---|
| Title screen | Met | `cthulhuquarium-title-card.vue` shows once per browser session, after the intro, over the `screen-arrival` plate: Enter the tank, Memory Book, Settings, Achievements | None |
| Settings | Met | `cthulhuquarium-settings.vue` opens from the HUD gear and sets volume, text speed, larger story text, high contrast and a motion override. Settings are kept per browser (`utils/cthulhuquariumSettings.ts`, read defensively). Esc closes it, and focus starts on Close | A tank reset was not added. It is destructive and wasn't asked for |
| Save/load | Met | Unchanged: everything is server-side, with offline settlement | None |
| Achievements 12+ | Met | 19 in `utils/achievements/catalog/main/cthulhuquarium.ts`, including `cthulhuquarium-bottom-of-things` for the floor V key | Catalog seeding runs through the usual maintenance workflow |
| Scrapbook | Met | The Memory Book replays every seen scene in descent order and shows unseen ones as dark cards. Replays record nothing. The Ichthyonomicon and backgrounds are unchanged | None |
| Endings with plates | Met | Three soft endings on a Memory Book shelf, each with its plate: "Every One" (book complete), "After the Last Aquarium" and "The Bottom of Things" (floor V). The tank never ends | None |
| Characters | Silas's call | No player avatar. Charlotte and Wilbur now carry a five-floor visual-novel arc, with Wilbur's injuries escalating in the art only | Whether "the tank is the player's identity" is enough, or a customizable keeper is wanted, is a design decision for Silas |
| Replay hooks (3+) | Met | The five-floor descent with bought keys, the 151-species book, endings, upgrades and sets, public tanks and the leaderboard | None |

Defects found and fixed by this audit's QA run (kind_robots, QA fixes PR):

- **Phone HUD overflow.** At 390px, the HUD row pushed its last button off the edge. Fixed: the
  day capsule hides below a 460px container.
- **Tablet HUD overlap.** At 768px, the wordmark cartouche overlapped the coin capsule. Fixed: it
  hides below an 820px container.
- **Settings panel.** The headings were dark on dark, and Esc did nothing. Fixed: the panel uses the
  theme's base colours and catches Esc.
- **Missing portraits.** A portrait that failed to load could show its alt text on stage. Fixed:
  it is hidden, and the dialogue box still names the speaker.
