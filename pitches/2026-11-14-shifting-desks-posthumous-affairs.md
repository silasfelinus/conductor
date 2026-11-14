# Pitch: Department of Posthumous Affairs
date: 2026-11-14 PT
project-target: shifting-desks
status: awaiting-silas

## The idea

The Company's severance package is literal. Employees who reach **Position Eliminated** are escorted to a cheerful basement department where the dead must continue filing quarterly proof of nonexistence. The secret ending reframes a defeat as an administrative escape route: the player can get their personnel record legally declared deceased while their body is still on the payroll, but the paperwork transfers their remaining life to the next employee in line.

This is a **proposed optional epilogue**, not a twelfth shipped ending, a promise of new art, or a replacement for the existing eleven endings. It must never silently unlock on an ordinary loss.

## Why it's worth doing

Shifting Desks already makes employment, identity, and replacement part of its mechanics. Posthumous Affairs pays off those systems without adding an unrelated universe or flattening the existing endings. The joke is not that death is funny; the joke is that the Company has invented a second HR department that can deny it.

The player should recognize three earlier choices in the department's files. The secret route feels earned when the bureaucracy knows the specific forms they forged, the successor they sacrificed, and the union grievance they ignored. It also offers a rare, bitterly hopeful conclusion: refuse to transfer the debt, and the dead employees organize an unauthorized strike that halts the building's elevators for one night.

## Proposed experience

**Entry:** Only after the authored Position Eliminated conclusion, with a persistent, explicitly visible archive unlock. A first-time player gets the existing complete ending, not a surprise sixth department that steals their victory. On a later run, a personnel-file stamp offers the optional epilogue. No LLM at play time.

**Scene 1, The Waiting Room:** A receptionist with a desk calendar reading *Yesterday* asks for proof that the employee has stopped working. Every chair is occupied by a person waiting for their own death certificate. Choice: submit a truthful account and surrender a remaining memory, or borrow a predecessor's certificate and inherit their unfinished grievance. Neither is a clean win.

**Scene 2, The Probate Copier:** The copier produces three versions of the player's file, each signed by a different successor. A player with a society affiliation can call in one favor; a player carrying a mutation can physically reach the jammed original. Both routes should reuse existing flags and costs rather than introduce an isolated minigame.

**Scene 3, Exit Interview:** The manager offers three legible decisions: (a) accept deletion and leave a clean desk for the next employee, with the cost borne by that successor; (b) refuse the transfer and organize the waiting room, keeping one's name on the Company's permanent blacklist; (c) falsify the manager's own death certificate, allowing an escape but making the player responsible for processing future arrivals. Each outcome receives a short distinct epilogue and archive entry if the expansion is approved and built.

**Sample exchange:**

> “You cannot resign while deceased,” said the receptionist. “Resignation is a living-person benefit.”

> “Then I would like to be alive.”

> “That requires a supervisor's signature. Your supervisor was eliminated yesterday.”

> “Where is he?”

> “Waiting for yours.”

## Guardrails and integration

- Keep the core five-department campaign and existing eleven ending routes unchanged. The optional sequence must be clearly separated from the original Position Eliminated ending and never advertised as available until implemented and tested.
- The three scenes must have authored choices, explicit costs, seeded/replayable consequences, save/resume compatibility, and no unwinnable loop. Reuse the existing Composure, Clearance, Suspicion, Successors, Forms and personnel-file systems where applicable.
- Do not add permanent art placeholders. Before implementing, inventory approved existing art for the receptionist, copier, and exit interview. Queue only missing hero illustrations through the authorized Conductor pipeline, then require actual delivery and visual acceptance.
- Avoid a generic “bureaucracy in the afterlife” anthology. The comedy should be precise, causal and personal, with callbacks to this particular run. Do not turn the dead into disposable props or make the player the unquestioned hero.
- Keep this outside the current playtest-readiness finish line unless Silas explicitly makes it required. An optional expansion pitch must not manufacture a new blocker for the base game.

## Rough effort

medium, **if approved**: three authored scenes with branching outcomes and persistent callbacks; an archive unlock; three to five verified art slots depending on existing asset reuse; route/save regression tests and adversarial full-run acceptance.

## Suggested first task

After explicit creative approval, write an isolated route contract and three complete encounter scripts, including the precise entry flag, successor-cost propagation, save migration behavior and ending-gallery distinctions. Validate the route contract and simulate the three outcomes before commissioning any new art or modifying the live game.
