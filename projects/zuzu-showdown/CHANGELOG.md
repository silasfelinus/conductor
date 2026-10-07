# zuzu-showdown CHANGELOG

## 2026-10-07
- t-009 (in progress): the Dunes and the Thin Place (kind_robots#3349). The Dunes has a long golden sun,
  blowing sand, and a dune that heaves as something vast moves under it. The Thin Place has a dark column
  dropping onto a lone door, glowing tears in the sky, and light at the door that widens each round. Seven of
  eight stages are done. The Bone Yard's ribcage is on its third prompt (the model drew a beast, then a cathedral).
- t-009 (in progress): the Lone Apple Tree (kind_robots#3348), on the noon backdrop from the daylight lane.
  It has heat shimmer, drifting red leaves, a dust devil, and apples that drop, rest and fade. tools/stage.py
  learned `patches`: a source box painted out by blending each column from the pixels above it to those
  below (a stray bone). Five of the eight stages are done.
- t-009 (in progress): the Mission and Storm Canyon (kind_robots#3348). The Mission is a moonlit church
  with a flickering candle, chimney smoke, and a portal in the bell arch between rounds. Storm Canyon has
  rain, crows, and lightning that silhouettes the canyon walls; it is rate-limited and off under reduced
  motion. tools/stage.py learned `mirror: "before"` (a ridge rising right, set after its mirror image,
  becomes a canyon). The Lone Apple Tree waits on a noon backdrop (art/T009C-DAY.yaml): the house lane's
  dark prefix turned "harsh noon" into a burning dusk.
- t-022: Training mode (kind_robots#3345) has dummy settings, frame advantage, an input display with the
  motion parser's read, refills and position resets.
- t-023: sound (kind_robots#3347). Hits sound by strength, with block, whiff, parry, throw, the KO sting,
  the Showdown stinger and the Hollow Bell bell. Each stage has a minor-key loop. Keyboard and gamepad
  players now hear it too.
- t-009 (in progress): the first two stages, Hollow Bell and the Watering Hole (kind_robots#3344).
  tools/stage.py builds each stage's parallax layers, cutouts (the bell, the pennant) and anchors (the arch
  beam, the lantern's smoke, the water) from house-lane art and a config in tools/stages/, with a palette per
  layer so the sun and the pond's water keep their colours. The game sways and rings the bell, flaps the
  pennant, drifts the smoke, rolls tumbleweeds, letters the arch, and gives the Watering Hole its shimmer,
  vultures, glints and the croc's eyes. Six stages to go.
- t-019 (in progress): a KO now slows the match to a third of its speed for a moment, with a white flash on
  the finishing blow (kind_robots#3342; reduced motion keeps the slow-down, drops the flash).
- t-019 (in progress): the VS screen and the win screen (kind_robots#3341). Before each fight the fighters
  slam in and trade their matchup's intro lines, each on the speaker's side; after it the winner stands in
  the victory (or Perfect) pose and says their win quote to the loser. tools/matchups_to_ts.py ports
  matchups.yaml to the game as matchups.json (`--check` compares them as data). Character select, stage
  entrances and the slow-mo KO are still to come.
- t-018: every matchup line is written (matchups.yaml): 36 intros (28 pairs and 8 mirrors), 64 win quotes and
  the boss lines, in each fighter's voice (Zuzu in three words or fewer, the croc in sounds, nobody gloating
  over the Siblings). tools/check_matchups.py and tests/test_zuzu_showdown_matchups.py keep the set complete,
  under 60 characters a line and clear of banned terms.
- t-010: effects. The rig draws a pale crescent smear behind Zuzu's katana cuts and the Coyote's
  stabs (in both styles, never counted as reach), and the game throws hand-pixel hit sparks where
  the hitbox meets the hurtbox: yellow hits, pink counters, blue blocks, green parries, double size
  for heavy blows.
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
