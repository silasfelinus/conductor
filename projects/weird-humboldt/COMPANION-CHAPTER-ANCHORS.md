# Ecotone: four companion routes, guaranteed chapter anchors (authoring pass)

**2026-10-26 PT · weird-humboldt/t-017 · text-only, not integrated gameplay.** These are draft-ready scene cards for the existing six-chapter weekend, not a replacement for the 120-card random deck or a declaration that the endings are reachable in the reducer. They extend [COMPANION-INTROS.md](COMPANION-INTROS.md), [COMPANION-OPTIMAL-PATHS.md](COMPANION-OPTIMAL-PATHS.md) and [ECOTONE-CORE.md](ECOTONE-CORE.md). They respect [EXCLUDED-CONTENT-2026-10-22.md](EXCLUDED-CONTENT-2026-10-22.md). No new art, ArtJobs, deploy or public release is authorized by this text.

## Implementation contract

- **Guaranteed, not random:** Each character's five beats are authored anchor slots (invitation/re-encounter, contradiction, commitment, repair, payoff). An anchor can run with that character as active lead or as an independent NPC. Do not require all five before a late Chapter 4 follow: a Chapter 5 catch-up summarizes missed *facts*, offers the outstanding commitment and repair decisions, and never awards a decision flag retroactively. The first invitation may be declined without closing the route.
- **Real choices:** Each beat has three choices. Checked options use the game's visible 2d6 + skill rules; their success and failure are both written. The third is a deterministic, costed alternative. A failed roll is not a soft lock. A player may not reroll the same check by saving and reloading.
- **Flags are proposals, not live reducer fields:** `arc_<name>_evidence`, `arc_<name>_promise`, `arc_<name>_repair`, `arc_<name>_payoff`. Set only after the described action. A companion's hopeful personal callback requires evidence + an honored promise + a completed repair, with a Chapter 6 choice to stand by the outcome. Evidence is recoverable by a no-roll route, and the repair is always offered. No single skill, initial lens, opening companion, ideology or rare card draw is required. The county's separate hope/dark determination and stable collectible ending IDs remain untouched.
- **Costs are fiction-first until mapped to existing reducer resources:** `time` means losing an optional interlude or taking a fatigue penalty, `favor` means owing a named NPC a future task, and `supplies` means a specific item available in the anchor. Do not charge nonexistent inventory; provide the written labor/time alternative. No secret moral score.
- **Continuity:** `meeting_order`, `follow_history`, current lead and known evidence control the intro sentence. A previously declined or departed companion acts on their own. Never imply a player attended a meeting they skipped. Sober characters can verify every uncanny fact without consuming anything.
- **Consequence readability:** Each table's outcome text is a scene beat, not just a flag. For checked choices, the two outcome columns are different; no-roll actions have a concrete tradeoff. All paths converge at the next guaranteed anchor without erasing a previous cost.

## Juniper: The Shared Canopy

### JSC-1 · Invitation at the culvert (Chapter 1; intro or guaranteed re-encounter)

The potluck is gone, but the fern spiral has crept across the surveyor's orange paint. Juniper has a folding chair planted in the creek and a notebook full of dates. "I can make the water change direction," she says. "That doesn't make me a drainage engineer." A delivery driver waits upstream; the flooded crossing is his route home. If this is a late meeting, Juniper shows you the notebook without pretending you shared the potluck.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Compare her dates with the culvert inspection sticker | Wits 8 | The sticker predates the new flood line; photograph both, gaining `arc_juniper_evidence`. | The sticker tears; the driver gives you a dated dashcam clip at the next anchor. |
| Ask the driver where the water went before the road was widened | Rizz 8 | He points out an old wildlife crossing and offers testimony; gain evidence. | He suspects you're recruiting him for a protest; he will still show you the crossing if you help unload. |
| Help carry the delivery across before investigating | No roll; lose an interlude | You preserve his wages and earn access to his dashcam; gain evidence. Juniper has to do the survey alone. | Not applicable. |

**Callback:** The driver can later argue *for* an accessible road and *for* habitat repairs; he is not a straw-man opponent.

### JSC-2 · The fence that walks (Chapter 2; contradiction)

A temporary fence separates the marsh edge from an affordable-housing access path. At dawn it has moved three meters toward the road, roots still threaded through its feet. Juniper admits she moved it in anger. "The birds got a night. The bus riders lost a morning." Her apology cannot undo the missed shifts.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Map a corridor that keeps the path open | Local Lore 9 | A feasible crossing appears between nesting ground and bus stop; the plan needs a public hearing. | Your route floods at high tide; a maintenance worker marks the safe elevation, but you owe a day of survey work. |
| Invite the bus riders to critique Juniper's plan | Rizz 8 | They demand lighting, ramps and an emergency vehicle turn; Juniper writes them down. | The first meeting is angry. A rider agrees to return if Juniper admits she moved the fence. |
| Ask Juniper to put the fence back before anyone negotiates | No roll; lose a night's protection | Access returns. She does it herself, not as your obedient spellcaster; the nesting area needs a temporary human watch. | Not applicable. |

**Carry:** Whether the apology was made changes her next opening line, not the availability of a fair solution.

### JSC-3 · A covenant with two signatures (Chapter 3; commitment)

At the harbor meeting, a contractor offers a beautiful map with no maintenance budget. Juniper offers a perfect forest with no public access. The driver unfolds his worn route sheet between them. The player cannot sign for either side.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Negotiate a funded, accessible corridor and independent habitat monitoring | Rizz 10 | Both parties sign a *conditional* maintenance pledge; `arc_juniper_promise`. | The funding line is vague; secure a smaller written trial and take its budget to Chapter 5 repair. |
| Audit the contractor's water calculations with Juniper | Wits 9 | An omitted storm drain is exposed; the revised agreement protects homes and migration; promise earned. | The math is incomplete; an independent engineer will review it for a favor, leaving the pledge provisional. |
| Offer to do the first month of volunteer monitoring with the driver | No roll; owe four weekends | A modest, binding pilot begins; promise earned. Juniper must recruit other stewards rather than relying on you forever. | Not applicable. |

**Constraint:** A signature is conditional until Chapter 5 repair. The contractor can be useful and self-interested at once.

### JSC-4 · The quiet cost of stewardship (Chapter 5; repair, guaranteed late-follow catch-up)

The first storm arrives. One ramp is underwater and a camera shows an otter taking the unfinished crossing. Juniper could move the water again. The driver has brought sandbags and a furious transit dispatcher. If you joined Juniper only today, she explains the pilot and asks you to take responsibility for the present repair, not for past meetings you never attended.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Repair the ramp with the transit crew before nightfall | Burly 8 | A usable path opens; gain `arc_juniper_repair`, with a future inspection owed. | You wrench a bracket; the crew rigs a safe temporary detour. Repair still possible through the no-roll follow-up. |
| Test the drainage and demand the contractor honor the pledge | Wits 9 | The contract's storm clause funds the fix; gain repair. | The clause is weak. The contractor supplies gravel after the driver publicly documents the defect, but you owe an audit. |
| Organize a watch, signage and an accessible shuttle until repairs finish | No roll; sacrifice a festival night | Nobody is stranded; gain repair. Juniper learns that protecting a crossing means protecting the people crossing it. | Not applicable. |

**Recovery:** If JSC-1 evidence was missed, the driver's dated clip is shown here; the player can inspect it without a roll. If JSC-3's pledge failed, the pilot's maintenance log is sufficient for a limited, honest repair commitment.

### JSC-5 · What the forest keeps (Chapter 6; payoff)

At dawn the fern spiral uncoils. A little boy in a raincoat waits for a bus beside a fox watching from the other side of the repaired culvert. Juniper says, "I thought keeping something alive meant keeping people away from it." She stops, watching the bus kneel for a wheelchair. "I was wrong about some people. Not all."

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Publicly bind the maintenance budget to a named local steward group | Rizz 8 | The corridor survives the next funding fight; if evidence, promise and repair are present, gain `arc_juniper_payoff`. | The vote is deferred. A signed interim budget keeps the corridor open, but the permanent guarantee waits. |
| Publish the accessible crossing and wildlife monitoring records together | Wits 8 | Neither habitat nor transit access can be quietly erased; qualified payoff. | The charts confuse the crowd; the driver and Juniper explain the two measurements in plain language. |
| Volunteer for the first follow-up inspection and invite both crews | No roll; forfeit your own celebration | Qualified payoff, earned through continuing labor, not a magical restoration. | Not applicable. |

**Hopeful personal epilogue:** *One year:* Juniper learns the bus timetable by heart, because the crossing's users now help watch the nesting season. *Ten years:* a kid who once needed the ramp becomes the watershed technician who audits it. *Thirty years:* the canopy has shifted, the county has argued, and the route still belongs to creatures on both sides of the fence. Juniper sometimes loses an argument and stays for the next meeting anyway.

**Scarred personal epilogue:** The culvert is repaired only in pieces. Juniper saves a small grove but trusts fewer people; the driver still keeps a dated notebook, a credible opening for later cooperation. Do not describe the entire county as doomed because this arc fell short.

## Kit: The Living Stage

### KLS-1 · The invoice behind the curtain (Chapter 1; invitation/re-encounter)

Kit's giant puppet refuses to fold in a loading dock whose rent has doubled. A technician named Pa Nhia has spent the night replacing a gear. A sponsor's mock-up shows Kit's face and erases the crew. Kit tears it in half, then asks whether she has just torn up everyone's wages. If the player missed the festival introduction, the crew shows the puppet's impossible fold without implying prior acquaintance.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Compare crew timesheets with the sponsor's proposed credits | Wits 8 | Find omitted labor and a payment clause; `arc_kit_evidence`. | A page is missing; Pa Nhia has the duplicate and will share it after the show. |
| Ask the builders what *they* want before Kit answers | Rizz 8 | They choose paid attribution over an empty publicity promise; evidence gained. | They talk over one another; Kit agrees to a second, quieter meeting. |
| Help unload and inventory the machinery | No roll; lose a regional interlude | Discover signed parts and a receipt proving who built the rig; evidence gained. | Not applicable. |

### KLS-2 · The solo spotlight (Chapter 2; contradiction)

A touring company offers Kit a solo residency with a real salary, health coverage and an uncredited touring rig. Her collaborators cannot afford to follow. "I want the stage," she says. "I also want to be able to look at the people who built it."

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Cost a touring version with credited remote fabrication | Wits 9 | The numbers show a viable compromise, but not a guarantee. | Shipping destroys the margin; Kit keeps the solo offer while the group looks for another plan. |
| Ask Kit privately which part of the offer she actually wants | Rizz 8 | She names artistic freedom and paid rehearsal time, not applause. | She snaps at your interrogation, then writes her terms on a napkin without you. |
| Attend the crew's own showcase instead of the sponsor dinner | No roll; lose sponsor access | You hear Pa Nhia's independent artistic plan; Kit can now negotiate without speaking for the crew. | Not applicable. |

### KLS-3 · A lease with room for names (Chapter 3; commitment)

A fictional maker co-op can take a warehouse for six months if it proves income, accessibility and who owns the work. The sponsor offers to pay in exchange for naming rights over every future show.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Negotiate a limited performance license, not ownership of the crew's designs | Rizz 10 | A contract protects paid credit and Kit's separate career; `arc_kit_promise`. | The sponsor refuses; a smaller venue agrees to a three-show pilot instead. |
| Build an honest budget with the crew | Wits 9 | Fair wages, access costs and rent fit a phased plan; promise gained. | The budget runs short; Kit cuts her own marquee fee and asks the team whether the pilot is still worth it. |
| Volunteer to handle the first accessible community rehearsal | No roll; owe two workdays | A real public event secures a modest lease trial; promise gained. | Not applicable. |

### KLS-4 · The performance that doesn't fit (Chapter 5; repair/catch-up)

A lift jams before a show. The sponsor wants the wheelchair users moved to the back; Pa Nhia wants to cancel rather than improvise something unsafe. Kit looks at the audience and says, "We built a monster that can bow. We can build a ramp that doesn't."

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Diagnose the lift with Pa Nhia and an accessibility technician | Wits 9 | They approve a safe temporary stage; `arc_kit_repair`. | The motor is unsafe. The crew moves the show to floor level, a genuine artistic change, not a fake fix. |
| Negotiate a delayed show with refunds and transport honored | Rizz 8 | People can return without paying twice; repair gained. | Some leave. Kit personally explains the revised time, and the venue issues real refunds. |
| Help turn the loading dock into an accessible ground-level performance | No roll; sacrifice the spectacle | Repair gained; the puppet's shadow becomes the show and every builder gets named. | Not applicable. |

**Recovery:** Missing KLS-1 evidence is available as a dated invoice at this anchor; late followers must choose to examine it. No character's heritage substitutes for an engineering check or a credit agreement.

### KLS-5 · A stage with an exit (Chapter 6; payoff)

At dawn Kit stands beside a small crowd in a warehouse that smells of wet plywood. The puppet folds open onto the impossible street again. This time the crew has marked a safe exit and nobody needs to pretend the physics make sense.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Secure a public-use calendar with independent artist slots | Rizz 8 | If evidence, promise and repair exist, `arc_kit_payoff`; Kit retains her own touring dates. | The calendar is shorter; a six-month open trial remains enforceable. |
| Publish the rig drawings with chosen licenses and signed credit | Wits 8 | Qualified payoff; the builders decide what stays private. | One page is disputed; the team holds that page back rather than falsely claiming consensus. |
| Work the first free workshop and hand Kit the keys afterward | No roll; give up your finale spotlight | Qualified payoff, but the space belongs to the artists, not the player. | Not applicable. |

**Hopeful personal epilogue:** *One year:* Kit tours with her name in lights and Pa Nhia's crew credited on every program. *Ten years:* the warehouse teaches teenagers how to weld safely, invoice fairly and make the impossible look effortless. *Thirty years:* the puppet's joints have been replaced three times. Kit insists that this makes it more original, not less.

**Scarred personal epilogue:** Kit takes the residency, or keeps a smaller studio without the co-op. She is not punished for earning a living. A child still learns to balance a discarded gear on one finger at her occasional free workshop.

## Mara: Lines That Last

### MLL-1 · The duplicate before the original (Chapter 1; invitation/re-encounter)

Mara sets two drawings side by side. One was sent to a printer yesterday; the other, dated next week, arrived in a sealed envelope this morning. Both contain a private client's requested change. "I can prove the line is mine," she says. "I will not prove it by telling you whose skin it was for."

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Verify the printer metadata without opening the client's file | Wits 8 | Establish a copy chain and `arc_mara_evidence`. | The timestamp is ambiguous; the printer's public job receipt still identifies a second run. |
| Ask Mara what she needs protected first | Rizz 8 | She names confidentiality before reputation; evidence gained from a redacted proof. | She keeps her boundary; later she supplies a signed redacted statement on her terms. |
| Help secure the physical archive while she calls the printer | No roll; miss a festival interlude | Find a mislabeled public proof, evidence gained without exposing the client. | Not applicable. |

### MLL-2 · The cheaper lease (Chapter 2; contradiction)

A fictional chain offers Mara a storefront with affordable rent and a clause letting the landlord sell anonymized client artwork. Her apprentice prospect says the deal could keep everyone employed. Mara hates the clause, and hates that refusing it is easier for her than for someone just starting out.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Compare two leases and identify a limited privacy-safe alternative | Wits 9 | The landlord's vague rights can be struck; the studio still faces a deposit. | The alternative costs more; Mara decides what risk she can afford. |
| Ask the prospective apprentice to propose terms directly | Rizz 8 | Their paid training and authorship become non-negotiable topics. | The apprentice is wary of being used as leverage; Mara invites a separate conversation. |
| Help move the studio's equipment into a short-term shared space | No roll; spend a workday | The chain loses its artificial deadline; Mara keeps negotiating power. | Not applicable. |

### MLL-3 · Ink and ownership (Chapter 3; commitment)

A shop owner offers to sponsor Mara's expansion if every apprentice uses her signature motifs. Mara could keep control and make rent. Instead she lays blank paper on the table and asks the apprentice what *they* would draw.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Draft a paid apprenticeship agreement with separate portfolios | Wits 9 | `arc_mara_promise`; copyright, consent and pay are spelled out. | A clause is unenforceable; a volunteer legal clinic marks the revision, and the agreement remains provisional. |
| Mediate an honest conversation about credit and criticism | Rizz 9 | Mara and apprentice choose an evaluation process they both trust; promise gained. | Hurt feelings surface; Mara asks for a cooling-off day, not a coerced handshake. |
| Fund the first public portfolio night with volunteer setup labor | No roll; owe two evenings | The apprentice displays original work; promise gained. Mara decides who may photograph it. | Not applicable. |

### MLL-4 · The name on the wall (Chapter 5; repair/catch-up)

A mural outside the shop uses a stolen design. Mara could identify the client and win the argument instantly. Instead she calls the painter, who bought the image from a dubious stock library and did not know its source. The apprentice has a new design that might replace it.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Trace the stock license and negotiate removal without naming the client | Wits 9 | The painter takes down the stolen work and pays the apprentice for a new design; `arc_mara_repair`. | The license chain stalls. A temporary cover goes up while a mediator reviews the documents. |
| Invite the painter and apprentice to propose a consent-based replacement | Rizz 9 | A paid, credited mural follows; repair gained. | They disagree on price. Mara offers a smaller commission rather than free labor. |
| Help paint a neutral cover while the dispute is resolved | No roll; miss the final concert | Client privacy is preserved and repair gained; the actual commission still requires consent. | Not applicable. |

**Recovery:** A player arriving late receives the redacted printer proof, never a client's name. A failed agreement may be revised here. No supernatural power is attached to tattoos or ancestry.

### MLL-5 · A shop that can outlast its sign (Chapter 6; payoff)

Mara opens the studio door at dawn. Two people are waiting, one for a tattoo and one for an apprenticeship interview. She points the second toward the new artist's portfolio, not her own. "I used to think every line had to look like mine to survive."

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Help establish a client-consent and paid-mentorship policy | Wits 8 | If evidence, promise and repair exist, `arc_mara_payoff`. | The policy needs revision; the studio starts with a narrower enforceable version. |
| Ask the apprentice to present their own terms to the studio | Rizz 8 | Qualified payoff; Mara supports without speaking over them. | The apprentice requests more time and keeps their existing paid role. |
| Take the first administrative shift so both artists can work | No roll; give up a finale errand | Qualified payoff. The studio's future is chosen by its artists, not the protagonist. | Not applicable. |

**Hopeful personal epilogue:** *One year:* Mara has fewer late-night invoices and more difficult, interesting conversations about art. *Ten years:* her former apprentice opens a studio across town and sends clients back to her when the fit is right. *Thirty years:* the old sign is repainted. Nobody can agree who drew the lettering, which Mara finds delightful.

**Scarred personal epilogue:** The studio relocates or contracts. Mara keeps her clients' trust and the right to refuse bad terms; she can teach one artist without creating an institution. A smaller life is not a moral failure.

## Cedar: Two Ribbons, One Home

### CRH-1 · The ribbons in the glove box (Chapter 1; invitation/re-encounter)

Cedar's CB predicts a road closure before the road exists. At his parents' kitchen table, his Hispanic logger father insists the route would strand shift workers; his mother, raised in a backwoods growing family and a **fictional** former ground-support volunteer during the real Luna tree-sit, says a shortcut through fragile habitat will not fix it. They finish each other's sentences while disagreeing. They have been married for years and remain together in every outcome.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Compare the CB recording with the county's published road plan | Wits 8 | A future road marker matches a real survey; `arc_cedar_evidence`. | The tape is noisy; his father's dated shift map corroborates the road geometry. |
| Ask each parent what the old ribbons meant to *them* | Rizz 8 | You hear two lived memories, not a false history lesson; evidence gained. | They correct your assumptions and tell their stories separately over dishes. |
| Help repair the truck's antenna and log a second broadcast | No roll; lose an interlude | A sober-replayable recording confirms the anomaly; evidence gained. | Not applicable. |

**History guard:** No invented conversation with Julia Butterfly Hill, no implication of tree spiking, no invented national origin for Cedar's father. The CB's futuristic signal is fictional, not evidence of historical supernatural events.

### CRH-2 · The easy tower (Chapter 2; contradiction)

A broadband contractor offers fast rural service from a cheap ridge tower. The tower's generator would sit above a salmon stream, and the company's service contract would let it raise prices after two years. Cedar wants the signal; his parents each see a different hazard.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Inspect the power, flood and access plan | Wits 9 | Find a safer site and realistic operating costs. | A crucial map is missing; a field technician supplies it after a site walk. |
| Convene a worker, resident and habitat monitor to challenge the pitch | Rizz 9 | The contractor must answer specific questions in public. | The meeting becomes a shouting match; Cedar records the unanswered questions anyway. |
| Walk the proposed route with the field crew | No roll; miss a festival show | You find the damaged drainage culvert and the truck access bottleneck; neither faction can dismiss the other. | Not applicable. |

### CRH-3 · The network belongs to someone (Chapter 3; commitment)

Cedar has a schematic for locally owned fiber and watershed sensors. A well-funded developer offers to build it tomorrow, provided the county gives up control of pricing and environmental data. "I can fix a radio," Cedar says. "I can't fix a contract that says we aren't allowed to open it."

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Write transparent rate, privacy, energy and worker-safety provisions | Wits 10 | A viable cooperative charter emerges; `arc_cedar_promise`. | The draft misses an operating expense; the local utility accountant helps revise it at a cost. |
| Bring skeptical workers and conservationists into governance design | Rizz 9 | They win seats with actual voting power; promise gained. | Neither group trusts the first plan; a limited public pilot is the only honest promise. |
| Help trench the first short community-owned link with paid local crews | No roll; sacrifice two interludes | A small but functioning pilot and a published maintenance budget earn the promise. | Not applicable. |

**Agency:** Cedar proposes and revises the network. The player can support or challenge him but never simply grants him a technoutopia by decree.

### CRH-4 · The forecast that was almost right (Chapter 5; repair/catch-up)

The CB warns that a service truck will slide into a creek. The road is dry, the driver is exhausted, and the new tower's drainage has not been inspected. Cedar is tempted to block the road because the radio said so. His father says, "Ask the driver." His mother says, "Check the water." Both stay at the table afterward.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Inspect the culvert and log the physical risk | Local Lore 9 | A blocked drain is found and cleared; `arc_cedar_repair`. | The inspection misses a side ditch; the road crew finds it on the second walk and requires a paid maintenance shift. |
| Ask the driver and crew to agree on a safe pause | Rizz 8 | The delivery is delayed without anyone losing wages; repair gained. | The dispatcher resists. Cedar arranges a shorter route and a written rest break. |
| Set warning signs and accompany the crew until the drain is inspected | No roll; forfeit a finale interlude | Repair gained. The radio's warning becomes a question checked by people, not fate. | Not applicable. |

**Recovery:** If the original CB evidence was missed, the recording and public road plan are both present here. A failed charter can be repaired with a transparent pilot, not a miraculous full network.

### CRH-5 · Two ribbons, one table (Chapter 6; payoff)

Cedar's parents serve breakfast while a community-owned relay sends its first public watershed readings. His father asks about paid maintenance jobs; his mother asks who can turn the sensors off. Cedar answers both, then admits that his forecast got the hour wrong. His father laughs. His mother slides him another biscuit. Nothing in their marriage needed saving.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Publish the cooperative's rates, energy use and worker-safety audits | Wits 8 | If evidence, promise and repair exist, `arc_cedar_payoff`; the network remains locally accountable. | One audit is incomplete; publish the gap and schedule a binding review instead of faking success. |
| Secure ongoing community representation and appeal rights | Rizz 8 | Qualified payoff; skeptics retain a meaningful veto over harmful expansion. | A vote stalls; the pilot remains limited until representation is agreed. |
| Join the first paid maintenance crew and let Cedar chair the meeting | No roll; miss your own celebration | Qualified payoff; technology stays a tool people can maintain and challenge. | Not applicable. |

**Hopeful personal epilogue:** *One year:* Cedar's relay helps a crew catch a washed-out road before a night shift. *Ten years:* young technicians from the county maintain fiber and stream sensors with published budgets and decent wages. *Thirty years:* the cooperative has survived two ugly elections and three hardware generations. At his parents' kitchen table, the old ribbons still hang from a drawer pull. They are still married, still arguing, still passing the biscuits.

**Scarred personal epilogue:** The tower is privately owned or the cooperative stays small. Cedar learns to read contracts and distrust prophecies without giving up his curiosity. His parents remain together, disagreeing over the county's choices, not over whether they love each other.

## Continuity and adversarial acceptance matrix

| Route | Evidence | Honored commitment | Repair | Chapter 6 payoff | No-roll evidence/recovery |
| --- | --- | --- | --- | --- | --- |
| Juniper | `arc_juniper_evidence` | `arc_juniper_promise` | `arc_juniper_repair` | `arc_juniper_payoff` | Delivery and dashcam; Chapter 5 |
| Kit | `arc_kit_evidence` | `arc_kit_promise` | `arc_kit_repair` | `arc_kit_payoff` | Inventory and duplicate invoice; Chapter 5 |
| Mara | `arc_mara_evidence` | `arc_mara_promise` | `arc_mara_repair` | `arc_mara_payoff` | Archive and redacted proof; Chapter 5 |
| Cedar | `arc_cedar_evidence` | `arc_cedar_promise` | `arc_cedar_repair` | `arc_cedar_payoff` | Antenna recording and public plan; Chapter 5 |

**Before claiming these are playable:** implement actual flags/conditions in the canonical reducer, map costs to existing resources, write distinct success/failure log entries, and prove seeded transcripts for each of four opening lenses × four final companions, including declined introductions, Chapter 4 switches, failed early checks, low stats, sober parity, save/reload, and both civic fates. Assert Cedar's parents stay together across every ending; Mara's client is never exposed; no companion personal optimum is automatically inferred from a county hopeful ending. Art coverage is a separate requirement; none is generated by this document.
