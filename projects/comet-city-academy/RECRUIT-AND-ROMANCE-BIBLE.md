# Prom of Doom: sixteen-recruit and romance bible

**Scope.** This is the canonical cast bible for the people who can join the player's night roster, plus the romance and throuple rules that apply to them (DESIGN-BRIEF section 4, task `t-002`). It sits alongside the 48 origin × affinity people in [IDENTITY-SYSTEM.md](IDENTITY-SYSTEM.md). Those 48 are the player's possible *identities* and rival heroes or villains. The people below are the *companions*. No recruit takes a name, codename or signature key from the 48.

**Everyone here is an adult.** The graduating class is 18 or older. City recruits are older adults with their own jobs and lives. **Faculty and staff are never romanceable.** Professor Veda Cross can be a field ally, but the academy's power over students rules out romance (DESIGN-BRIEF: "consent cannot be … coerced by teacher/student power"). Romance stays PG-13 and non-sexual. It is never required to save the city, and rewards can never buy it.

**Runtime status.** The twelve people marked **runtime** exist in Kind Robots `utils/cometAcademy/rules.ts` (`STUDENTS`). Eleven of them are in `relationships.ts` (`SOCIAL_CAST`), each with:
- a voice;
- a dilemma, a help scene and field terms;
- a private moment, an infirmary bedside scene and a boundary;
- machine-checked compatibility rules.

The four marked **authored** are designs only. They are not yet recruitable, they have no art, and they must not be counted as playable until a runtime PR and seeded tests land.

## Compatibility rules (runtime contract)

Each romanceable person reads the player through declarative rules on **form** (student / hero / villain), **vow** (Shelter / Unmask / Claim), **power family** and **city danger**:

- **closed**: a boundary they hold. No invitation or date is offered while it applies. The reason is shown to the player.
- **wary**: one more honest conversation is needed before a date (trust 4 instead of 3).
- **kindred**: changes what they say when invited. It never skips a step.
- **curious**: the default when nothing in the player's record draws or worries them.

The Followers screen shows mutual affinity as the player's trust (0–5) next to this read. A date always needs at least two separate days after the first invitation, and either person can step away at any time without a mechanical penalty.

## The sixteen

| # | Person (pronouns) | Status | Origin / skill | Where you meet them | Body and look (art canon) | Romance | Field roles | Boundary / compatibility | Injury reaction |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Mina Quill** (she/her) | runtime | academy · kinetic | Engineering Workshop | Broad-shouldered, dark brown skin, short curls, ivory rescue coat | Yes | Partner, sidekick | Closed to a public villain; kindred with Shelter; wary of Claim | Rigs a pulley on her bed and explains it until she falls asleep |
| 2 | **Sol Navarro** (he/him) | runtime | academy · technopathy | Archive Stacks | Slim, olive skin, close-cropped black hair, amber visor | Platonic | Partner | Prefers platonic collaboration this term | Reprograms the monitor to show the transit board |
| 3 | **Imani Vale** (she/her) | runtime | academy · empathy | Student Commons | Plus-size, copper-brown skin, long black braids, teal scarf | Yes | Partner | Closed above danger 12; kindred with empathy; wary of villains | Has you read her the shelter minutes |
| 4 | **Ash Calder** (they/them) | runtime | academy · elemental | Academy Roof | Lanky, pale, wind-tousled ash-blond hair, storm-gray weather coat | Platonic | Partner, sidekick | Wants friendship and field loyalty, not dating | Opens the window to hear the wind |
| 5 | **Nix Venn** (they/them) | runtime | academy · spatial | Transit Gate | Slender, tan skin, short silver hair, white jacket with purple lining | Yes | Partner, sidekick | Kindred with spatial; wary of Unmask (their father's letter) | Opens pocket portals to nowhere |
| 6 | **Kit Rowan** (she/her) | runtime | academy · biotech | Botanical Conservatory | Broad-hipped, pale skin, auburn hair, green medic vest full of seeds | Platonic | Partner | Close platonic partnership this month | Tries to triage the next bed |
| 7 | **Professor Veda Cross** (she/her) | runtime | faculty · kinetic | Training Arena | Fifty, broad-shouldered, dark brown skin, cropped silver hair | **Never** (faculty) | Night ally only | Ex-stunt hero chasing one last shot at glory | — |
| 8 | **Mara Fen** (she/her) | runtime | city · spatial | Transit Union Hall | Sturdy, light brown skin, side-shaved dark hair, orange safety coat | Yes | Partner once on the roster | Closed to Claim; wary of famous heroes; kindred with kinetic | Insists you tell the night crew she is fine, word for word |
| 9 | **DRIFT-9** (they/them) | runtime | experiment · biotech | Transit Lab | Lab-grown adult, opalescent grey skin, shaved head, cyan veins | Yes | Partner, sidekick once on the roster | Every step said in plain words; kindred with biotech; wary of villains | Asks which vitals mean "worry" |
| 10 | **Tessel Mire** (he/him) | runtime | anomaly · elemental | Skyport | Tall, willowy, dusky blue alien skin, luminous freckles | Yes | Partner once on the roster | Must stay free to go home; kindred with elemental; wary above danger 8 | Translates only the kind cloud shapes |
| 11 | **Jo Mercer** (they/them) | runtime | city · technopathy | Media Spire | Warm ochre skin, short neon-magenta hair, patched navy leather jacket | Yes | Partner, sidekick once on the roster | Never buries a story about power; kindred with Unmask; wary of Shelter | Broadcasts "Live From Bed Four" |
| 12 | **Lark Sato** (he/him) | runtime | city · empathy | Civic Hospital | Light brown skin, short messy dark hair, teal flight suit, rust scarf | Yes | Partner once on the roster | Closed above danger 18; wary of famous heroes; kindred with villains | Reads his own chart upside down, shares his pudding |
| 13 | **Vesna Duarte** (she/her) | authored | academy · empathy | Ethics Hall | Tall, angular, deep olive skin, silver-streaked undercut, immaculate council blazer | Not planned | Partner | The glamorous student-council fixer. She trades favours with both the dean and the mastermind's accomplices and will defect if the player shames her in public | Runs council business from the bed and resents every minute |
| 14 | **Bram Kowalczyk** (he/him) | authored | academy · kinetic | Theater Wing | Big, soft-bodied, ruddy pale skin, red beard, sequinned prom-committee sash | Not planned | Partner, sidekick | The prom organizer whose decoration budget unknowingly paid for a transmitter part. He can expose it on day 29 or be blamed for it | Keeps asking whether the chandelier was delivered |
| 15 | **Femi Ilunga** (they/them) | authored | academy · elemental | Student Dormitory | Short, wiry, dark brown skin, shaved sides with copper beads, oversized hand-me-down cape | Not planned | Sidekick | Wants to be a sidekick but dreads becoming a symbol. They leave if the player puts their face on a poster without asking | Refuses visitors until the bruises fade, then wants all the gossip |
| 16 | **Cyrus Adeyemi** (he/him) | authored | city · kinetic | Waterfront Market | Thirties, broad, heavyset, brown skin, shaved head, flour-dusted apron over an old hero vest | Not planned | Partner | A trans man and retired independent hero ("Short Order") who cooks nights at the market diner. He recruits only after the player shows up for a non-emergency shift | Brings you soup, which is worse than being injured himself |

**Diversity check (romanceable eight):** three she/her (Mina, Imani, Mara), three they/them (Nix, DRIFT-9, Jo) and two he/him (Tessel, Lark). Bodies include plus-size, sturdy, broad-shouldered, slender, lab-grown and alien. All eight are open to the player whatever the player's gender. Body descriptions repeat `TEAM_LOOKS` so art stays consistent.

## Throuple arcs (runtime)

Both arcs need the player to be **already dating one member**. There is never a choice to pursue the other person behind a partner's back. Every beat:
- spends a separate social day;
- needs both adults available (neither injured nor separated by betrayal) and no closed boundary;
- needs the third person's *own* trust with the player;
- offers at least one way to pause or decline, with no penalty.

Saves are validated by replaying the recorded choices, so a beat cannot be skipped. If either adult steps away, the arrangement ends and any remaining couple continues on its own terms.

### 1. The Listening Accord: Imani Vale + Nix Venn (player-initiated)
1. **What you owe the person you are with.** Tell your partner first, or keep the third person as a dear friend.
2. **Your partner answers.** They ask to talk to the third person alone first. Agree without asking what was said, pause, or stay a couple.
3. **Writing the accord.** Imani runs a listening session, and both partners say yes out loud. Choose a weekly renegotiation check-in or time for each pair, or settle on friendship by agreement.
4. **Who gets to know.** A gossip photo leaks. A joint public statement gives city standing +1 and academy standing −1. You can also agree on privacy together, or pause.
5. **Three yeses** on the academy roof, or a very close friendship by agreement.

### 2. The Night Shift: Jo Mercer + Lark Sato (partner-initiated)
1. **Your partner says it first.** Before telling anyone else, they admit feelings for their old friend and ask what you want: talk, take time, or stay two.
2. **The four a.m. booth.** In Jo's pirate radio booth above Lark's ward, the third person answers for themselves and asks to be allowed to be scared.
3. **Three night schedules.** Choose a dawn breakfast or a three-click "I need you" radio signal, or admit it is the wrong month.
4. **The broadcast that hurts.** Jo's segment exposes Lark's ward. You can mediate (trust +1), give them a day apart, or take a side (trust −1 and the arc pauses until an apology).
5. **Three yeses at shift change**, or close friends.

**Consequences in play:** a committed triad on one dispatch team adds +1 coordination, beside the existing field-partner and sidekick bonuses. Prom epilogues name all three people and the terms they chose. Declines and pauses change nothing else.

## Still open for t-002 and t-005

- Bring the four authored recruits (#13–16) into runtime, with intro sites, recruitment events, defection conditions and art.
- Give the eight romances date and breakup variants across the five narrative bands. The t-005 "eight romance routes" target is relationship *scene* coverage across the month. The underlying eight routes and two throuples now exist.
- Add relationship-art states (neutral, joyous, angry, afraid, hurt, injured) for all sixteen through the project's ArtJob ledger.
