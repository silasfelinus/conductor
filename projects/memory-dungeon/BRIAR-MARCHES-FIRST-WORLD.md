# Briar Marches — World 01 Production Registry

**Draft to implement, not live game content.** Authored for the existing 8×8 coordinate system (`1,1` through `8,8`), retaining `2,4` Briar Camp, `6,2` Rootbound Vault, `8,4` Thorn Gate, matching-wave reveal, Classic Match and existing save IDs. The House That Remembers is the narrative upgrade to Rootbound Vault, **not** a new coordinate or migration by renaming alone.

## First-session playable script

1. In a modern research workplace, an androgynous adult encounters Morrow, who asks pointed questions about living where there is no magic. The protagonist unknowingly accepts a fairy-bargain disguised as a minor exchange. The world slides sideways. **No long questionnaire or seven-screen prologue.**
2. In Morrow's fey body at `2,4`, the player learns fog, route visibility and how real memory matches can reveal locations. The first narrative choice is whether to help the unnamed courier or keep the one useful Lantern. These outcomes persist. Give the option to review concise tutorial hints in the sidebar; keep game artwork dominant.
3. At `4,4`, the twins intervene with cheerful certainty. At `4,3`, Oren performs a terrifying axe flourish solely to cut a damaged supply crate open, then solves an impassable travel problem with a meticulously maintained manifest. Gothic Char and proper Scylla look facially alike; their contrasting skin colors are never framed as an identity trick.
4. The player notices the wolf-tribute mystery and can reach `6,2` via discoverable paths. **Do not force a full match board** for every conversation, chest or passage. Combat happens in separately framed rooms.
5. A photographed moment at `2,5` shows Morrow losing the protagonist's job; a second at `8,6` depicts Morrow hurting a friend. The player initially feels vindicated. No children or romance are implied yet.
6. The House offers a genuine choice over how people who surrendered memories should be treated. The Bramble Chime opens the next-world gate, but alternative paths and companion differences change the aftermath.

## Authored map location registry

**Columns:** coordinate | stable label | primary category | discovery hook | action / persistent consequence. The categories overlap; the primary budget is reconciled in the global bible. Coordinates already exposed by current code must never be repurposed silently after saved discovery. The registry is source for implementation tickets, not yet a set of functional buttons or assets.

| Coordinate | Title | Kind | Encounter promise | Meaningful resolution seed |
|---|---|---|---|---|
| `1,1` | North Star Twin | lore | An inscribed star swears its twin lies beside another kingdom's lake. | Copy its angles now; a cross-realm partner later opens an Edgeworld. |
| `2,1` | Widow's Silhouette | danger | A grieving widow hires the living shadow of her lost spouse as a guard. | Calm the shadow with a memento or challenge its mistaken loyalty. |
| `3,1` | Sleepless Orchard | puzzle | The trees sleep with their eyes open and drop fruit in a strict order. | Deduce the three-bell harvest rhythm; an error only changes tonight's yield. |
| `4,1` | Rain Mirror | treasure | The puddle reflects a traveler carrying a lantern not yet purchased. | Take a future lantern at the price of a disclosed debt, or leave the vision intact. |
| `5,1` | Honeymoon Gutter | side | Two newlyweds are escaping a story that insists one is a monster. | Hide their path, earning their trust but angering the village registrar. |
| `6,1` | Rootbound Threshold | travel | A root arch links the upper marsh to the House's service passage. | Discover a one-way shortcut back from the dungeon; never replace the fixed vault site. |
| `7,1` | Wrongful Gallows | main | A gallows grows a fresh branch for every rumor spoken beneath it. | Free the accused by investigating, or fight the hangman's animated rope. |
| `8,1` | Whitewing Cipher | lore | A feather seal insists its reflection is hiding in the Salt Cliffs. | Record the cipher for a later realm's location-based pair. |
| `1,2` | Forty-Five Bells | danger | A flock of bell-wearing crows warns travelers by sounding different counts. | Decode the danger and avoid a fight, or disturb the flock and meet its sentinel. |
| `2,2` | Old Wolf Track | lore | Wolf prints march toward town but every set leaves the village again. | Note the defensive route that suggests the wolves are guarding the village. |
| `3,2` | Vesper's Unsent Map | companion | A cartographer has erased the route that would reach a forgotten friend. | Offer secrecy or exchange a flower for directions; future confidence changes. |
| `4,2` | Mosswick's Stall | travel | A merchant prices goods in wildflowers or enforceable promises. | Trade one flower for a Lantern, or examine the disputed ledger. |
| `5,2` | Sleeping Sigil | puzzle | Half a paired seal is warm with the breath of sleeping roots. | Take its trace; a second half exists beyond the House. |
| `6,2` | Rootbound Vault | travel | The existing dungeon entrance leads into the House That Remembers. | Enter the House; keep the saved vault-1/vault-2 aliases until migration. |
| `7,2` | Splinter Court | travel | The saplings sue an oak for stealing their sunlight across a public footpath. | Arbitrate shade versus growth; earn a grove shortcut and change patrol testimony. |
| `8,2` | Great Hunger | danger | A famine specter follows only travelers who have lied about eating. | Admit a theft or defeat the creature with remembered pair sequences. |
| `1,3` | Bent Spoon | treasure | A spoon feeds its owner a remembered taste, not actual nourishment. | Keep the comforting relic or return it to an exhausted cook. |
| `2,3` | Storm Bride | side | A bride's wedding procession continues after her partner vanished. | Search for a living explanation rather than assume a curse. |
| `3,3` | Memory Mill | puzzle | A mill grinds forgotten words into flour as its gears reverse. | Restore the word sequence; each correct rotation reveals a name. |
| `4,3` | Oren's Manifest | companion | A towering masked headsman reconciles three impossible supply inventories. | Help find a missing parcel; his axe stays untouched while he solves travel logistics. |
| `5,3` | Last Breadcrumb | danger | A trail of crumbs is rearranged by a bird offering misleading rescue. | Learn its counting habit to evade the nest or face a fair matching duel. |
| `6,3` | The House Hears Everything | main | Names scratched into the masonry contradict the royal registry. | Record the names for truth or conceal them from the Index to protect witnesses. |
| `7,3` | Thorn Patrol | danger | Two guards disagree on whether the House can be arrested. | Challenge their logic or settle their dispute instead of fighting. |
| `8,3` | Gilded Throne | treasure | A toy throne crowns anyone who sits on it and bills their neighbors. | Take a charm of persuasion or dismantle the throne and lose its reward. |
| `1,4` | Blood-Red Hood | main | A courier in a red cloak fears the grandmother who hired her. | Trust the wolf's warning, the courier's contract, or inspect the cottage first. |
| `2,4` | Briar Camp | main | The modern protagonist wakes in a borrowed fey body beside an impossible sign. | Tutorial: inspect one square, meet a messenger and make a first consequential choice. |
| `3,4` | The Unpaid Toll | side | An official charges for a bridge that has never been built. | Demand the receipt or sketch an imaginary crossing into being. |
| `4,4` | The Princesses Arrive | companion | Scylla and Char offer lavishly contradictory rescue schemes. | Invite their company; the difference between their clothing and coloring is not proof against their identical-twin claim. |
| `5,4` | A Knight's Mislaid Oath | main | The Brass Knight pledged to guard a crossing that no longer exists. | Carry his apology or warn the House; his opinion changes after the fact. |
| `6,4` | Pip's Contradiction | main | A courier brings two legitimate and mutually exclusive royal orders. | Choose which letter to deliver and own the human cost of suppressing the other. |
| `7,4` | The Index of Persons | main | An official demands the protagonist's name while refusing to disclose its custodian. | Register with a copy or decline and acquire an inconvenient classification. |
| `8,4` | Thorn Gate | travel | The regional exit beats with a bell buried under the path. | Use the Bramble Chime or an earned alternative resolution, not random loot. |
| `1,5` | A Sleepwalker's Warning | main | An elderly sleepwalker is stalked by their own awakened dreams. | Protect them by reading dream symbols; failure costs supplies but not their life. |
| `2,5` | Photograph: Dismissal | photo | A real-world photograph shows Morrow in the protagonist's body leaving a research office, dismissed. | File the image as a dated Chronicle clue; do not allow selling or duplicate claims. |
| `3,5` | Pip's Borrowed Voice | companion | Pip argues with a stump that repeats their voice and edits yesterday. | Use lanternlight to free a moth-like thief or listen and learn a harder truth. |
| `4,5` | The Shoemaker's Child | side | A child repairs shoes in exchange for stories no one else remembers. | Pay with a personal memory clue or supply leather from the camp. |
| `5,5` | The Sprite's Grievance | danger | A Moss Sprite fights because duels are the only events the Index cannot erase. | Offer a flower as proof of hearing them or resolve a telegraphed duel. |
| `6,5` | Thornsong Locks | puzzle | A thorn harp's wires vibrate only when touched in the correct order. | Use the sound-pattern hints from 2,2 to unlock a short forest route. |
| `7,5` | The Fawn's Trial | danger | A young beast stands accused of leading hunters into their own traps. | Defend with observed tracks or survive a three-turn trial by combat. |
| `8,5` | The Gate's Heartbeat | puzzle | A wooden mask offers immediate entry in exchange for a named memory. | Refuse and seek the Chime, or take on a promise without erasing a save. |
| `1,6` | Hair-Ladder Loft | treasure | A balcony offers a braided rope to anyone who asks the prisoner inside. | Rescue the keeper or steal the ladder; set later reputation. |
| `2,6` | Moss Inscription | lore | The stones say LEAF, LEAF, SUN; a gardener explains why order matters. | Copy a visible clue for the 2,7 puzzle. |
| `3,6` | Creekside Cache | treasure | A dry chest holds two wildflowers and someone's unfinished apology. | Claim once, or leave its contents as an offering that earns a future ally. |
| `4,6` | The Packmate's Petition | side | A wolf asks the village to stop calling its protective patrol a tribute raid. | Carry its account to town or barter for a safe route. |
| `5,6` | Bone Crow Duel | danger | A skeletal bird pecks names off forgotten headstones. | Recover one erased name through combat or bribe it with a spare trinket. |
| `6,6` | The Debtwell | puzzle | The well returns exactly what was dropped last week, never what was dropped today. | Deduce the dated coin sequence and win a delayed charm. |
| `7,6` | Riverbank Chest | treasure | An abandoned chest contains one lantern and a map of an unseen ferry. | Claim once, or offer the lantern to a lost child. |
| `8,6` | Photograph: The Gathering | photo | Morrow embarrasses a friend at an Earth-side social evening; the friend looks genuinely hurt. | Store the photograph with the timeline, planting the possibility of reconciliation. |
| `1,7` | The Floating Oak | danger | A tree uproots itself to escape its assigned ending as firewood. | Protect the tree against woodcutters or help it find a safe transplant. |
| `2,7` | Three Quiet Stones | puzzle | The carvings accept leaf, leaf, then sun, witnessed in the Moss Inscription. | Solve visibly; mistakes reset the local glyphs, not the player's discoveries. |
| `3,7` | Greenwood Challenge | danger | A knight politely requests a duel for trespassing in his own abandoned garden. | Play matching combat or prove shared ownership through the deed. |
| `4,7` | Stolen Laughter | lore | A village laughs at funerals because the cemetery owns its tears. | Discover whose bargain imposed the custom before judging anyone. |
| `5,7` | The Dam's Door | side | The miller's family has barricaded the spillway to keep memories from escaping. | Choose drought, risky flood, or investigate a third approach earned through clues. |
| `6,7` | Red Swan | danger | A swan warns passersby of a curse it is secretly transporting. | Identify and lift its cargo, or battle its feathered escort. |
| `7,7` | The Tailor's Measure | puzzle | A tailor's tape measures intentions differently from bodies. | Place three garment symbols in a fair spatial pattern; no identity-based penalties. |
| `8,7` | Briar Sentry | travel | A watchtower overlooks both the gate and the hidden southern shore. | Activate a return shortcut after earning trust; no endless encounter toll. |
| `1,8` | The Last Apple | treasure | An orchard's final apple remembers every hand that tended it. | Keep its healing use or plant it to improve the world's next chapter. |
| `2,8` | Witch's Calendar | side | A witch is being tried for a winter she correctly predicted. | Present weather records or let the accused set a dangerous bargain. |
| `3,8` | Fallow Field | lore | An empty field bears footsteps of an entire vanished procession. | Record the route for a secret area clue. |
| `4,8` | Tin Wedding | treasure | A metal flower can preserve one promise against magical revision. | Claim or return it to the couple from the vanished procession. |
| `5,8` | Shrewd Rat | danger | A rat attorney enforces unfair bread contracts with alarming competence. | Win a clause-matching challenge or pay a disclosed toll. |
| `6,8` | Pilgrim's Grave | lore | A memorial names the living among the dead, including someone met at camp. | Ask a witness why, changing later House dialogue. |
| `7,8` | Echo of the Barn | side | The barn remembers a childhood no present villager claims. | Open the barn for truth or protect the village's useful lie. |
| `8,8` | Moonroot Knot | lore | A last paired seal promises another knot under Moonwell Vale. | Keep its rune in the Chronicle for a future-world unlock. |

**Registry check:** 64 unique stable entries, 8 rows × 8 columns; 8 main, 8 side, 12 danger, 8 puzzle, 8 lore, 8 treasure, 6 travel, 4 companion and 2 Earth photographs, matching the realm budget. Current program only gives interactive story scenes to 13 coordinates; writing a registry does **not** make the other tiles accessible. Extend `BRIAR_LINKS`, authored `BRIAR_SCENES`, site behaviors and state transitions in incremental app PRs; validate every square is reachable on at least one legal route without breaking old save IDs. Use unique art references and conditional text for branch outcomes rather than copy-pasted flavor.

## First dungeon: The House That Remembers

The named entrance remains `6,2`. The initial implementation has two in-game rooms `vault-1` and `vault-2`; preserve those as stable saved identifiers while adding thirty-four rooms. A 6×6 room budget is a planning surface: rooms need not be visited in row-major order, and the authored graph must have honest junctions, looping shortcuts, an optional puzzle bypass, a true return route, and a boss that can be resolved in more than one fashion.

| Room | Name | Function | Authored beat |
|---|---|---|---|
| HD-01 | Porch of Borrowed Faces | entry | Intro: the threshold asks whose name the player wears |
| HD-02 | Umbrella Stand | lore | Every umbrella drips a different person's last rain |
| HD-03 | Boot-Rack Maze | puzzle | Place returned boots by remembered owner, not size |
| HD-04 | Clockwork Pantry | treasure | Take food only after admitting who will go without |
| HD-05 | The Wolf's Latch | choice | Open the wolf's route or seal it against the village |
| HD-06 | Broom Closet Exit | shortcut | Oren finds a reliable return path with proper signage |
| HD-07 | Family Portrait Hall | lore | Paintings contain guests who were never invited |
| HD-08 | Staircase of Three Apologies | puzzle | Sort apologies by who suffered, not speaker rank |
| HD-09 | Hearth-Guard | combat | A protective animated coal with telegraphed fire |
| HD-10 | Scylla's Inventory | companion | The proper twin offers confidence, Oren corrects the packing |
| HD-11 | Char's Wardrobe | companion | A goth closet hides a real protective charm, not a costume joke |
| HD-12 | Servants' Passage | shortcut | A service tunnel rejoins an earlier hallway |
| HD-13 | Letterpress Kitchen | puzzle | Read the recipe's missing-line pattern from clues |
| HD-14 | First Memory Jar | treasure | Acquire an image of the village's last festival once |
| HD-15 | The Polite Guest | choice | A cursed host requests a guest's consent in writing |
| HD-16 | Thornbound Housekeeper | combat | A defender who can be placated by returning a name |
| HD-17 | Gallery of Unsent Letters | lore | Competing stories expose the village elder's bargain |
| HD-18 | Quiet Bedchamber | rest | Safe recovery and Chronicle journal checkpoint |
| HD-19 | Mirror Corridor | puzzle | Match reflected geometry while art visibly explains reversals |
| HD-20 | Missing Daughter's Room | choice | Give testimony to a living family or keep a protected secret |
| HD-21 | Parlor of Embarrassments | lore | A mirror echoes Morrow's first documented humiliation |
| HD-22 | Index Collector | combat | Warned card-column seal after two full turns |
| HD-23 | Small Wardrobe Door | secret | Opening requires clues from the earlier Boot-Rack Maze |
| HD-24 | Dry Cellar Return | shortcut | A safe loop back to the entry, always available |
| HD-25 | The Bargain Ledger | puzzle | Cross-check dated promises against the photograph journal |
| HD-26 | Wolf-Mother's Defense | choice | Hear why wolves take payment for village protection |
| HD-27 | Unclaimed Portrait | treasure | Discover a portrait with a deliberately absent subject |
| HD-28 | Twinned Guard | combat | Two opponents each defend the other's marked cards |
| HD-29 | The Indenture Room | lore | Contracts show the House was asked to remember the unwanted |
| HD-30 | Lantern Landing | rest | Branch-dependent companion dialogue and bounded healing |
| HD-31 | Cellar of the Forgot | hazard | A rising fog hides exits, but explored routes persist |
| HD-32 | Rootbound Warden | guardian | Adapt existing vault-2 boss: memory tools and telegraphed pressure |
| HD-33 | The Last Kind Lie | choice | Choose to reveal the village's original consent or protect survivors |
| HD-34 | Broken Doorway | puzzle | Use learned paired seals for final conditional shortcut |
| HD-35 | Memory Hearth | climax | Liberate stored names, renegotiate the bargain, or preserve it knowingly |
| HD-36 | Bramble Chime Exit | exit | Earn Chime or alternate gate authorization, record consequences |

**Route shape:** HD-01 → either HD-02–06 or HD-07–12, rejoin HD-13–18, optional HD-19–24 or HD-25–30, and culminate HD-31–36. Loops HD-06→HD-01, HD-12→HD-07 and HD-24→HD-13 are safe exits. A shortcut earned by the twins can bridge HD-10→HD-25; discovering the wolf evidence can bridge HD-26→HD-34. Any room's optional puzzle can be abandoned at a disclosed cost. This draft adjacency must be materialized and validated by a graph test before gameplay uses it.

### Boss and endings for this realm

The **Rootbound Warden** is not evil for guarding the House. Someone arranged to store unwanted memories here; the Warden has protected records against thieves and also prevented people from reclaiming them. A combat victory is only one way past it. Proof from the wolf-tribute bargain, a returned portrait, or earned trust with the housekeeper can unlock alternate consent-based resolutions. The ending is not a binary good/evil label:

- **Release the records:** give memories back where possible; several villagers regain agency, while protective ignorance collapses and the wolf patrol changes its demand.
- **Renew the bargain:** negotiate revocable, informed storage with named witnesses; the village gets safety but the player owes ongoing oversight.
- **Break the machinery:** deny any entity ownership of memories; the House becomes dangerous and open, but future realms gain a way to challenge old bargains.

At least one loss continuation must send the party safely to an earlier checkpoint with a changed NPC response rather than erasing geography. Every outcome writes a Chronicle event and a next-realm callback; none awards unlimited re-claimable loot.

### Tutorial and art shot list

**Tutorial:** teach surface reveal once, nested combat once, a fair rune puzzle once, and one relationship choice in context. One-screen camera scene, in-world dialogue, accessible tooltips and a skippable/replayable help sidebar. Use the existing Classic mode as the original matching experience, not as an intrusive compulsory tutorial.

**High-priority illustration subjects:** Earth-side pact in ordinary research office; first borrowed-body reflection; Briar Camp at dusk; Scylla and Char in matching farm-strong physiques with divergent authentic proper/goth styling and skin coloration; perpetually hooded Oren with ceremonial axe and supply ledger; wolf patrol defending villagers; first Morrow dismissal photograph; damaged party photograph; House exterior/foyer; Warden action portrait; each of the three realm outcomes; map tile terrain atlas. Record ArtJob ID, prompt, style model, source, attachment and delivered URL separately; prose is not completed artwork.

### Validation for World 01 work

- 64 keys exactly once; preserve existing 14 named sites and existing 13 active scenes by compatibility migration, not blind replacement.
- Every nonoptional gate and dungeon room has a route with valid prerequisites; no dead-end or mandatory blind-guess puzzle.
- The two photographs are recoverable in a full first-world run, never duplicated and stored in timeline order even if discovered in reverse.
- At least one moral choice, an honest failure continuation, one alternate Warden outcome and a repeat NPC callback reach the UI.
- All existing Classic tests and saved Briar encounters remain playable. Confirm seed replay, reload after a scene, and no repeat chest claims.
- Verify phone 390px, tablet 768px and desktop 1440px when app code changes; screenshot the actual rendered experience before declaring visual acceptance.
