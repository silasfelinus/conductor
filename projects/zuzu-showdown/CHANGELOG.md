# zuzu-showdown CHANGELOG

## 2026-10-07
- t-010 (in progress): hitboxes authored against the art. rig.py measures each attack's striking layer
  (`hit` per frame), and the game's sprite test holds every kit hitbox to it on the active frames. Fixed
  in the art: both crouching anti-airs and Pocket Sand now strike on their active frames, the crouching
  light kicks and sweeps reach the floor, Zuzu's heavy kicks reach out, the jump kicks angle down. The
  katana and the Coyote's stump knife are drawn shorter. The kits follow the art for the rest
  (for example Iai Flash reaches 56 instead of 44, and Zuzu's sweep 36 instead of 48).
- t-010 (in progress): both fighters' sprite sets cover their whole kit: every normal, the dodges, landing,
  wake-up, throws, every special and super, the round intro and the Perfect pose (conductor#5726 and this
  change; kind_robots#3325 and its follow-up). The game plays the intro over the round intro and the
  Perfect pose on a flawless win. Pixel atlases are saved as exact indexed PNGs.
- t-010 (in progress): Zuzu and the Coyote Vagrant now fight as their art. The fighter rig (tools/rig.py,
  configs in tools/rigs/) poses HD parts cut from the Kontext parts sheets and derives the pixel style,
  with P2 colours and frame maps. Zuzu has 19 animations, the Coyote 18 (conductor#5712-#5721), and the
  game draws both from their pixel atlases (kind_robots#3321).
- t-007 done: the sprite bake-off (docs/t-007-sprite-bakeoff.md). HD masters are the source of truth and
  pixel is a derived style (Silas: "pixel is a style choice"); kr-arcade t-012 and zuzu-showdown t-027
  carry the resolution and render-style work.
- Engine milestone (kind_robots): t-003 sim core (#3291), t-004 controls + motion reader (#3294), t-005 combat
  systems (#3298), t-006 playable Admin-tab page with renderer and HUD (#3304). Screenshots in
  docs/t-006-screens/. The pre-verdict page is an Admin tab rather than an unlisted URL (Silas's
  no-hidden-routes rule).
- t-002 done: Silas confirmed the Coyote without his hand, a lighter Street Fighter tone (no blood, no
  gore, no fatalities), the name Zuzu Showdown, and online play later. Brief v1.2; fighters.yaml tone
  rule, and the Abbess's altar grab and Komodo's super toned down.

## 2026-10-06
- Silas confirmed the roster (the Hyena Matriarch and Old Komodo), the tentacle boss and the Siblings
  rules (t-002, in session). Four questions stay open (Coyote's stump, KO tone, name, online play).
- Project scaffolded via intake.py (Silas: a Street Fighter / Skullgirls / MvC-style fighting game in the
  world of Zuzu: Koala Assassin, "possibly our largest yet").
- DESIGN-BRIEF.md v1: controls (LP/HP/LK/HK + Dodge, Easy Specials), motion inputs, the strike/grab/guard
  triangle with READ! callouts, chains, launchers, scaling, infinite protection, combo breaker, red
  recoverable health, three-bar meter with Lv1 and Lv3 Showdown supers, taunt screens, eight animated
  stages, the pixel-art spec and pipeline options, modes, CPU, engine architecture, MVP phases, guardrails
  and open questions.
- fighters.yaml v1: Zuzu, Coyote Vagrant, the Abbess, the Siblings, Storm Crow, River Croc, the Hyena
  Matriarch and Old Komodo, plus the boss (The Thing Behind the Door): five specials, two supers, intro,
  taunt, victory/Perfect/KO poses each; the Siblings' children rules.
- matchups.yaml v0: the six rivalry matchups and the boss intros, as a voice sample.
- Roadmap: engine (sim, input, combat, renderer), art (pipeline bake-off, portraits, stages, four sprite
  pairs), fighters and modes (movesets, lines, taunt screens, CPU, Arcade + boss, Training, sound),
  polish and Silas's verdict.
- Project icon/card/hero prompts rewritten to the Krea rules.
