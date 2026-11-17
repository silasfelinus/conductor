# Deepheart

Playbook on the Playbook Kit. Conductor slug `deepheart`; spec
`utils/playbookKit/games/deepheart.ts` in kind_robots; development preview
`/admin/deepheart`. Started 2026-11-16 at the **Saga** tier. Roadmap hub:
kind_robots#5256.

## 1. Title, premise and dramatic question

- **Title / tagline:** Deepheart. "Three layers down. Bring someone you would follow anywhere."
- **Premise:** A delver and one to three companions go down a three-layer dungeon (the Ossuary Gate, the Drowned Halls, the Ember Deep) to the living heart of the mountain. What they do on the way down, and who they become to each other, decides what happens at the bottom.
- **Dramatic question:** Can a delver and the companions they choose reach the living heart at the bottom, and what will they decide to do with it, and with each other, when they get there?
- **Tone and touchstones:** traditional torchlit dungeon crawl with party banter and campfire romance; original work.

## 2. Tier and complexity budget

- **Tier:** Saga, because Silas asked for about fifty presets up front.
- **Allowances:** followers 50, romances 42, threads 50. A single delve runs at most three companions, so only one or two romances and a handful of supports are live at once.
- **What would earn more:** playtest evidence that a fourth layer or more room types keep delves fresh.

## 3. Play loop and meters

- **One turn:** choose a door (fight, puzzle, treasure, choice, camp; scouts reveal more), resolve the room, take loot, watch companions approve or disapprove, move one room deeper. Seven rooms a layer, a boss at the bottom of each.
- **Meters:** depth, party health, gold, potions.
- **Failure:** fights can knock members out (campfires revive them); failed puzzles spring traps; a full wipe is the Lanterns Out ending, recorded in the chronicle.

## 4. Cast

- **Followers:** 50 anthropomorphic presets across 15 roles, with species limited to the visual art specification. Any of them can lead. 42 are romanceable (mutual attraction required), 6 are aromantic and swear oaths instead, Quillon and Ambrose are married, and Brannoc and Thessaly are a poly couple courted together.
- **Principal villain:** the Hollow King, the first delver, who took the heart and was taken by it. Reveal `king-name`, endings Redemption and Delver.
- **Other villains:** the Bone Warden, Mother Brine and Vesper the Lich. **Figures:** Ottoline the Undermerchant, Snag, Maren of the Weeping Door.
- **Romance:** optional and player-chosen, built at campfires; hidden when the romance setting is off.

## 5. Factions, reveals and endings

- **Factions:** the Bone Court, the Brine Choir, the Ember Throne (one per layer).
- **Reveals:** 8, including the Warden's oath, Maren, the lighthouse keeper, the living heart, Vesper's court, the keystone, the king's name and the Undermerchant.
- **Endings (9):** Delver, Usurper (crown), Lichbound (pact), Dawnbringer (spirit + seed), Redemption (mercy), Sealed (keystone), Gilded (gold), Hearthbound (a partner), Lanterns Out (wipe).

## 6. Scrapbook and trailer

- **Moments:** 72 (16 scenes, 3 boss falls, 12 signature supports, 41 romance plates), all unlocked by play.
- **Trailer:** six spoiler-free beats.

## 7. Screens

- Title (New, Continue, Load, Chronicle, Scrapbook, Achievements, Settings); party builder (roster grid, detail, hero customization, party bar with synergies, supports, score and optimizer); delve (party strip, door hand, fight deck, puzzle boards, event/camp/loot/finale hands); ending plate; chronicle and save slots.

## 8. Completion gates

- Agent-owned: everything on the roadmap through t-013, including rendered art and 390 / 768 / 1440 px checks.
- Graduation (t-014): playtest at normal priority; the hub issue is flagged and closed.
- Silas: human playtest verdict, then any public `/play` release (publish gate).

## Visual canon: anthro Deepheart (Silas, 2026-11-16 PT)

- Living characters belong to an **anthropomorphic animal-person fantasy**, with a Zuzu-family animation sensibility but original designs. Every preset has one explicit visual species, silhouette, coloration, size, costume and role in Kind Robots `utils/deepheart/anthro.ts`. Species appear **only in art prompts**, never titles, biographies, UI labels or dialogue. Introduce someone as “Jeffery the Rogue,” never “Jeffery the Raccoon.”
- Preserve all fifty playable identities, IDs, gender diversity, romance/oath preferences, relationships, abilities and saves. The cast spans men, women and nonbinary people, ages, body sizes, mobility and silhouettes, mammals, birds, reptiles, insects and amphibians. Animal design must not imply character, culture, or combat balance.
- The builder starts on the Hero tab; all fifty presets can lead or be selected as companions. Maintain an art-led, single-screen console with bounded scrolling.
- The 139 kit images and 29 supplemental images remain traceable, but their human/fantasy-humanoid renderings are NOT accepted as final anthro art. The proposed 94-subject repaint (50 portraits, 41 romances, 3 figures) is now a PRIVATE DRAFT with `auto_submit: false` pending the new style trial. Avoid generating an entire wrong-style cast a second time. Undead and elemental bosses remain monsters.
- **Private high-priority style trial (2026-11-16 PT):** five fixed-seed scenes across eight render lanes (40 independent ArtJobs): Krea 2 plus the available Arthemy, Nova Comic, Illustrij, NTR Mix, Furrytoon, Illustrious Realism and Realism Illustrious By checkpoints. `projects/deepheart/art/ANTHRO-STYLE-TRIAL-2026-11-16.yaml` has `priority: 900` and `auto_submit: true`. Every scene specifies physical anthro anatomy and modern mature Western fantasy-cel-animation direction.
- Trial scenes: Oona the heavyset bison guardian; Vex the nonbinary bat rogue; the Ossuary Horror; Oona and Vex confronting the beast; and an affectionate waterfall bath for the established **adult** Brannoc/Thessaly couple, with deep opaque water, cascading white spray, rocks and ferns blocking anatomy below shoulders. Images are marked private and mature, and no public release is authorized.
- The admin-only, mature-enabled `/admin/deepheart/bible` is the staging room: private cast briefs, visual canon, five-subject gallery grouped by model, ArtJob status, local ratings and review notes. Compare before commissioning the full 94. The bible link appears on the Deepheart admin title screen only for qualifying viewers.
- Queued is not rendered or attached: verify accepted ArtJobs, ArtImages, canonical files and working URLs before marking t-012 complete. Do not confuse submission with delivery.


## The vertical world: politics all the way down (Silas, November 16 PT)

Deepheart is a **settled vertical world**, not a staircase of combat arenas. The
surface is home to animal-person adventurers, guilds, sponsors and ordinary
families. Beneath it, entire communities make their lives around shafts,
reservoirs, markets, graveyards, heatworks and root gardens. Riches can be found
below, but the surface habit of calling every valuable discovery "loot" is a
form of colonial blindness. The underground has its own cultures, property
claims, unions, merchants and politics.

- **Bellmouth and the Ossuary Gate:** Surface supply depots and gravekeepers,
  ropewalk porters, toll elevators, lantern schools and debt registries. The
  residents are not obliged to welcome treasure hunters into their homes.
- **The Drowned Halls:** A lived-in floodplain of barges, water markets,
  landlord-held dry stairways, salvage crews, community kitchens and
  neighbourhood councils. Access to clean water and upward transit is power.
- **The Ember Deep:** Forgers, heatworks labourers, root-farm commons, legal
  disputes over the mountain's living heart and nobles who regard time as
  their hereditary property.

Punk aesthetics should come from lived-in civic resistance: scavenged heraldry,
repaired jackets, hand-painted strike signs, anarchic music, salvage and neon
thread in old court gowns. The cyberpunk parallel is **vertical privilege,
resource monopolies, identity paperwork, access control, financial debt and
propaganda**, transposed into fantasy without turning the setting into a
computer world.

**Playable obstacle grammar:** Minor threats include a busted lift or a
sabotaged school beam. Major threats include a flood-ward eviction, debt-backed
food shortages, and an industrial lockout. Every added society/fairy choice
event offers multiple nonviolent d20 ability checks and a no-roll refusal or
costly alternative. Checks use the seeded run RNG, 1d20 plus the best conscious
party member's relevant stat divided by four (rounded down, minimum zero),
against a visible difficulty. Failures cost resources or cause harm but do not
silently force combat. Rolls and totals are printed in the run log and remain
deterministic across save/reload.

## The Glass Family: the fairy court

All mortal residents are anthropomorphic animal people. **The six fairy gods
are the deliberate supernatural exception:** they look eerily and
unmistakably **human**, with varied adult complexions, body types and gender
presentations. This is not explained at introduction. The player discovers
the anomaly organically, and different locals offer incompatible theories.
Later revelations establish how much these rulers have manipulated the
surface's understanding of identity.

| Fairy ruler | Magical jurisdiction | Political pressure |
| --- | --- | --- |
| Duchess Aveline, Mistress of Names | Names, citizenship and erasure | Registry determines who counts as a person |
| Prince Ilex, Weight of the World | Gravity, stairs, transit | Toll lifts determine whose food and medicine can move |
| Lady Serein, Matron of Interest | Debt and borrowed tomorrows | Tomorrow can be repossessed |
| Lord Vireo, Last Supper | Food multiplication and famine | Royal banquets control community kitchens |
| Countess Cauline, Seamstress of the Hour | Stolen, rewoven time | Working hours are hereditary collateral |
| Consort Ludo, Prince of False Faces | Masks, fame and public memory | Gossip and propaganda rewrite dissent |

The court is a **bored family of scheming adult nobles**, not an unbroken
villain team. Their power is immense, their emotional maturity questionable.
At the core are half-siblings, an annulled marriage with collateral claims,
cousins whose youthful affair was erased from the registry, estranged parents,
adopted heirs, a staged engagement, feuds, false genealogies, leaked letters,
public hookups, breakups, and revenge plots. These are non-explicit soap-opera
relationships, written to illuminate the political machinery they built.

### Playable audiences and endings

Six fairy audience events can appear throughout the three strata. The
player may bargain, expose, defy, or walk away. The first meeting reveals the
god's human face in the scrapbook. Successful investigations and bargains
reveal one of twelve distinct connections in the family diagram.

Once a god has been met, the player may accept one **last audience** after
choosing any of Deepheart's original nine major endings. This is an optional
second decision hand: choose which known patron to face, then **bargain,
expose, or defy** on a visible 1d20 check. Each choice has a distinct
success/failure epilogue and unlocks the relevant reveal entry. Declining all
audiences ends normally. This preserves old ending IDs, saves and achievements
while layering a personal court resolution onto the original finish.

### Scrapbook as a relationship flowchart

The Deepheart Scrapbook has **Court Connections** and **Lived Moments** tabs.
The former is a genuine node-and-edge flowchart for all six rulers, with
twelve typed connections: kinship, affairs, former lovers, annulments, grudges,
schemes and revenge. Unknown nobles are concealed and unknown links are
unlabelled; actually meeting, investigating, and resolving a final audience
unlocks names and relationship explanations. Clicking a known node filters its
connection captions and dossiers. This is a story graph, not a decorative
family-tree picture.

The private art bible may display spoiler-rich visual design prompts, while
the public scrapbook only reveals what the individual save has earned.
**Do not resume the 94-image bulk anthro repaint until the existing 40-image
model comparison has established the accepted mature Western cartoon style.**
When rendering these rulers, their human faces must be visibly distinct from
the world's anthropomorphic citizens; use their human appearances only in
fairy art prompts, not as a reason to revert the mortal cast to generic humans.
