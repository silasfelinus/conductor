# Ecotone: four value-tension scenes (authoring pass)

**2026-11-04 PT · weird-humboldt/t-023 · text-only, not integrated gameplay.** One guaranteed-quality scene per fault line defined in [IDEOLOGICAL-ECOTONES.md](IDEOLOGICAL-ECOTONES.md): Autonomy ↔ Solidarity, Continuity ↔ Reinvention, Ecology ↔ Engineering, Agency ↔ Fate. These are draft-ready cards for the existing 120-card deck's neighbors (the 120 main cards are untouched), not engine code and not a new gallery slot. They respect [EXCLUDED-CONTENT-2026-10-22.md](EXCLUDED-CONTENT-2026-10-22.md) and [OPTIONAL-DETOURS.md](OPTIONAL-DETOURS.md). No art, ArtJobs, deploy or public release is authorized by this text.

## Authoring contract

- **The opening is a camera, never a verdict.** Each scene carries seven one-line *camera notes* (`sober`, `tipsy`, `stoned`, `tripping_balls`, `cocaine`, `meth`, `mdma`). A note says what the scene happens to foreground and ends on how any player can see past it. It grants no axis offset, no free success, no moral score and no required choice. Nothing here describes how to obtain, prepare or take anything, or claims a real physiological or psychological effect.
- **Every opening can land on either pole, and on the hybrid.** Hopeful and difficult results are written for all three choices in every scene. No pole is the hopeful one.
- **Three real choices per scene:** two use the visible 2d6 + skill rule, with different success and failure text; one is a costed, no-roll alternative. One of the three is a *hybrid* that can fail on its merits (flag `hybrid_attempted` either way).
- **Each companion can argue both poles** of the tensions that involve them (see the table in each scene). Nobody is a straw opponent; the people with the opposing view are named, paid, and right about something.
- **Rights are not on the slider.** Consent, wages owed, public safety and living tribal sovereignty are fixed constraints inside every option, never a point to trade against a value.
- **Metadata is proposal-only:** `tensions`, `stakes`, `decision_flags` follow the schema sketched in IDEOLOGICAL-ECOTONES.md. Flags are set only after the described action, and none of them selects a hope/dark fate by itself.

## TEN-AS · The ice house vote (Autonomy ↔ Solidarity)

`tensions: [autonomy-solidarity]` · `stakes: shared_cold_storage, landing_records_privacy, small_boat_livelihood` · `decision_flags: ice_house_pooled, ice_house_exempt, ice_house_charter_split`

**Scene.** At the harbor, the cooperative ice house is failing: its compressor is older than the youngest deckhand. Dolores Aquino, who has fished alone for thirty years, will not sign a pooled-storage charter that requires every boat to log landings where neighbors can read them. "My numbers are my business, and the last people who wanted them took my quota." Across the dock, Teo Larsen, who runs three boats' worth of other people's fish through that ice, has a spoiled shipment on a tarp and no money to replace the compressor alone. The vote is at noon. Both are right about something.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Draft a **hybrid two-tier charter**: pooled ice for anyone who opts in, landing logs sealed to an elected clerk | Wits 9 | A workable charter passes narrowly. Dolores keeps her numbers private and pays a higher per-load rate; Teo's compressor is funded for one season. Flag `ice_house_charter_split`. | A clause is ambiguous and the clerk's role is challenged. The vote is postponed one tide; both agree to meet again if you read the text aloud on the dock. |
| Back Dolores: ask the harbor to **exempt private boats** and fund the compressor by a one-time public appeal | Rizz 9 | Her independence is protected and the appeal raises half the cost. Teo's crews ice at a distant plant for a month, a real loss. Flag `ice_house_exempt`. | The appeal sounds like charity; people give less than hoped, and Dolores decides you spoke for her without asking. She will still hear you out later. |
| Back Teo: **commit your own weekends** to run the pooled ice house for a month and make the logs open | No roll; lose two interludes | The compressor is patched, the pooled model survives the season, and open logs expose one quiet over-fishing habit before it becomes a crisis. Dolores keeps fishing alone, without the ice. Flag `ice_house_pooled`. | Not applicable. |

**Camera notes.**
- `sober`: you read the quota paperwork first and see exactly what a log can be used for. Anyone can read it that way.
- `tipsy`: the dock conversation is the real vote, and you hear who nobody has asked. Anyone can ask.
- `stoned`: the whole harbor looks like one slow animal sharing a pulse. Anyone can count its actual dependencies.
- `tripping_balls`: two possible harbors shimmer, one pooled and one scattered; neither is the forecast, and you can go and check the ledgers.
- `cocaine`: the clock is loud and you notice who is waiting on whom before the noon vote. Anyone can read a queue.
- `meth`: you catch the compressor's failing rhythm from across the dock, a detail the committee missed. Anyone can put a hand on the casing.
- `mdma`: you notice the person nobody has greeted all morning and the room softens around her. Warmth does not write the charter; the clauses still have to hold.

**Both poles.** Juniper argues for shared obligation, then for a boat that needs no committee. Kit defends the artist's right to refuse a collective and the duty to pay collaborators. Mara guards her own ledger and explains why a trusted clerk is not surveillance. Cedar proposes an encrypted shared log, then admits a ledger is only as honest as the neighbors who read it.

**Hope and difficulty.** A pooled harbor can be generous or coercive depending on its clerk; an independent harbor can be free or abandoned depending on who still shows up with ice. Either can be told as a good ending, or as a cautionary one.

## TEN-CR · The mill whistle (Continuity ↔ Reinvention)

`tensions: [continuity-reinvention]` · `stakes: mill_apprenticeship, shift_whistle, workforce_memory` · `decision_flags: whistle_kept, whistle_retired, whistle_retuned`

**Scene.** The old mill's shift whistle still blows at 6:10, 2:10 and 10:10 though nothing has been milled there in years. Nobody has found the valve. A developer proposes a training hub in the sheds: robotics, composite fabrication, a Wi-Fi mast on the stack. Ruth Okamoto-Reyes, who worked the green chain for twenty-six years, wants the sheds left as a plain hall with the machines in place: "If you paint over the floor, you paint over my knees." Her niece, Miguel, who wants an apprenticeship that pays this year, holds a printed offer from the hub. Tradition here belongs to loggers, millwrights, kitchen cooks and the people who clean the bathrooms alike; nobody gets to claim it alone.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Propose a **living-shop hybrid**: keep the green chain as a working demonstration floor and teach new fabrication around it | Rizz 9 | Ruth agrees to train the first cohort on the old equipment before the new, and Miguel's wage is secured. The hub's budget takes a hit. Flag `whistle_retuned`. | The developer reads the hybrid as a delay. The deal survives only if you present the numbers at a second meeting, and Ruth is annoyed to be handled. |
| Archive what is there, **then** convert: interview shift veterans and record the floor before any change | Local Lore 9 | The archive turns up a safety rule that the new plan would have broken; the redesign respects it. Some workers want no archive at all, and say so. Flag `whistle_retired`. | The recording is patchy; a veteran refuses to speak until the project stops using her family's name. You lose a day to rebuilding trust. |
| Stand with Ruth: **help her keep the sheds as they are** and pay for a minimal weatherproofing yourself | No roll; owe four weekends | The hall stays and becomes a quiet, unusual place; the apprenticeship goes to another town. Miguel is hurt, and keeps working with you anyway. Flag `whistle_kept`. | Not applicable. |

**Camera notes.**
- `sober`: payroll records and fire-code plans stand out. Anyone can find them.
- `tipsy`: the bar-stool oral history is warmer than the archive and less reliable. Anyone can cross-check a story.
- `stoned`: the floor seems to hum with forty years of footsteps. Anyone can follow the actual wear patterns.
- `tripping_balls`: the whistle seems to be answering someone; a second mill stands behind the first. Anyone can trace the pipework.
- `cocaine`: the apprentice's offer letter has a deadline, and you see it. Anyone can read a deadline fairly.
- `meth`: you hear the whistle's missing half-beat and chase it into the rafters. Anyone can find the stuck valve there by hand.
- `mdma`: you notice how much each person is holding back out of love for the other. Tenderness is not a plan; someone still has to sign.

**Both poles.** Cedar wants a locally owned mast and also wants to save the sawdust smell. Juniper cares for the living moss in the rafters and for a job that pays. Kit treats the whistle as a score worth preserving and a sound worth rewriting. Mara argues for a master's craft and for an apprentice's right to leave.

**Hope and difficulty.** Kept floors can become a museum nobody can afford, and rebuilt floors can forget the people who paid for them. Either can be told as a good ending, or as a cautionary one.

## TEN-EE · The tide gate (Ecology ↔ Engineering)

`tensions: [ecology-engineering]` · `stakes: tidal_marsh, sea_level_rise_flooding, farmland_road_access` · `decision_flags: gate_built, shoreline_restored, gate_and_marsh_hybrid`

**Scene.** King tides are overtopping the farm road at the slough. A county engineer, Anika Brandt, has a plan for a concrete tide gate with remote sensors. A restoration ecologist, Dr. Sam Whitehorse-Park, wants the dike breached so the marsh can migrate inland, the way the bay used to breathe. A dairy family whose land sits between the two plans will lose their only road in either design unless someone builds a third. Reading either side as a villain is a mistake: the engineer cares about the bay's fish, and the ecologist depends on a power supply.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Draft a **hybrid**: a small adjustable gate, a staged breach and a raised road section | Wits 10 | The three plans merge into one. It costs more than either and lands later; the family keeps road access and the marsh gets room. Flag `gate_and_marsh_hybrid`. | The hydrology model misses a spring tide. Both experts agree to rerun it with local tide-gauge notes, delaying the project a season. |
| Walk the slough with the dairy family and map where the water **actually** goes | Local Lore 9 | The family's decades-old observations correct the model: the worst flooding is at a culvert nobody listed. A cheap fix buys time for a real decision. Flag `shoreline_restored`. | The map is imprecise and the family is skeptical of outsiders. They agree to a second walk if you bring boots and listen first. |
| Back the engineer: **volunteer on the sensor build** and push for a public data feed anyone can read | No roll; lose two interludes | The gate is built with transparent monitoring and a clause to review the design in ten years. Some marsh is lost; the road is secure. Flag `gate_built`. | Not applicable. |

**Camera notes.**
- `sober`: the tide table and the road's elevation survey stand out. Anyone can read a survey.
- `tipsy`: the argument turns on who has been invited to the meeting. Anyone can invite the dairy family.
- `stoned`: roots, culverts and cables look like one circulatory system. Anyone can follow where they cross.
- `tripping_balls`: the marsh tastes of a hundred-year-old shoreline; the gate looks like a held breath. Both are metaphors, and a tide gauge is not.
- `cocaine`: the funding deadline dominates everything and you notice it before the ecology. Anyone can decide that a deadline is not the whole question.
- `meth`: a faint electrical whine from the sensor box sends you under the road. Anyone can follow a bad ground to its loose clamp.
- `mdma`: you feel the family's dread and the ecologist's grief at once. Compassion does not move water; the plan still needs an engineer and a marsh.

**Both poles.** Juniper accepts a concrete gate if the herons keep their flats. Cedar wants sensors that serve the marsh instead of replacing it. Kit sees the dike as a human sculpture worth keeping and a breach as a necessary erasure. Mara argues for stewardship that can be handed down.

**Hope and difficulty.** A gate can protect a road while starving a bay; a restored marsh can protect a bay while stranding a family. Either can be told as a good ending, or as a cautionary one.

## TEN-AF · The forecast frequency (Agency ↔ Fate)

`tensions: [agency-fate]` · `stakes: levee_inspection, community_trust_in_forecasts, evidence_preservation` · `decision_flags: forecast_verified, forecast_disproved, forecast_reframed`

**Scene.** A dead-air CB channel starts reading tomorrow's headlines: *Levee fails at Ryan Slough, 4:40 a.m.* It has been correct twice this week about trivial things. Frankie Holm, the night dispatcher, believes it and wants to start evacuating. Councilwoman Iris Takeda calls it a hoax and wants nobody frightened without evidence. If the prediction is certain, nothing anyone does matters; if it is only a prediction, the right action is not obvious either. Predictions here are not villains, and neither is doubt.

| Choice | Check | Success / deterministic consequence | Failed check |
| --- | --- | --- | --- |
| Run a **hybrid**: inspect the levee tonight, stage a voluntary evacuation, and publish what you find | Wits 9 | The inspection finds a real seep at the weak point. A crew shores it up, a few families sleep elsewhere, and 4:40 comes and goes. The channel falls silent. Flag `forecast_disproved`. | The inspection crew is late and the seep is smaller than feared. The channel repeats its message and you cannot prove it wrong; the town stays on edge. |
| Corroborate the broadcast: **log every transmission** against tide data and dispatch records | Local Lore 9 | A pattern emerges: the channel is reading real engineering notes some hours before they are filed. It is either a sophisticated source or something stranger, and that is more useful than certainty. Flag `forecast_verified`. | The log gaps are large and the council dismisses it as noise. Frankie keeps a copy and agrees to try again after the next transmission. |
| Walk the levee with Frankie and **knock on doors yourself** | No roll; lose a night's rest | You warn eleven households, most of whom listen. Some are angry about the false alarm; no one is hurt by the seep. You do not learn whether the channel was right. Flag `forecast_reframed`. | Not applicable. |

**Camera notes.**
- `sober`: you check the transmission against the dispatch log before anything else. Anyone can do that.
- `tipsy`: the town gossip about the channel is louder than the channel. Anyone can ask who started it.
- `stoned`: the voice seems to belong to the slough itself. Anyone can still go and measure the slough.
- `tripping_balls`: tomorrow seems already printed and the room fills with possible tomorrows. A seep is a fact either way, and facts can change the page.
- `cocaine`: the 4:40 deadline sharpens everything; you act before you finish thinking. Anyone can choose to pause and verify first.
- `meth`: you hear a pattern in the static and feel sure it means something. Anyone can test a pattern against the logs.
- `mdma`: you feel the town's fear as your own and want to hold everyone. Care still needs a plan; a plan still needs facts.

**Both poles.** Cedar has the radio and the rule that a foretold future may still be changed. Juniper trusts seasons and respects that some cycles will not be argued with. Kit believes a story can be rewritten and also that some endings were always going to be sung. Mara argues that what is inked cannot be erased, and that people still choose what to mark next.

**Hope and difficulty.** A prediction can be a warning that helps everyone act, or a certainty that makes people stop acting. Free will can be a gift or an excuse. Either can be told as a good ending, or as a cautionary one.

## Continuity

- These scenes can run as optional side encounters between Stay/Follow crossroads or as one-time chapter 2–5 inserts. A late arrival gets a short, factual recap and never implies attendance.
- All seven openings, all four leads and both fates remain available after every scene. The 56 gallery signatures and 8 authored core futures are unchanged; these scenes only add callbacks (`ice_house_*`, `whistle_*`, `gate_*`, `forecast_*`).
- Review before any integration: confirm the invented locals do not map onto real private individuals, confirm the hybrid on each card can really fail, and keep the stoned/tripping lines from implying a universal drug effect.
