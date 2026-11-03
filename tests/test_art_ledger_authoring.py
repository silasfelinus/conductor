"""Template-filled art ledgers are refused before they reach Krea (slime-city, 2026-11-02, #6951)."""
from pathlib import Path

import yaml

from scripts import art_ledger_authoring as auth
from scripts import enqueue_art_requests as enq

ROOT = Path(__file__).resolve().parent.parent

# Ledgers that already failed when the check landed (2026-11-02). Their unsubmitted cells are
# refused at enqueue until rewritten; remove an entry once its ledger passes. Never add one.
# CAMPUS-CHOICE, CASINO-CHOICE and COLLECTOR-CHOICE were re-prompted by hand on 2026-11-03.
HELD = {
    # Superseded by IDENTITY-SYSTEM.md (2026-10-26): its powers must not render, so it stays
    # unrewritten and refused rather than being re-prompted.
    "projects/comet-city-academy/art/COMPOSITE-POWERS-ROUND-1.yaml",
}

FACTIONS = [
    "Riot Saints of Redline, scarlet-and-hot-pink dangerous fireworks, gleeful adult demolition rebels",
    "Undertow Intelligence from teal-lit sewer canals, brass goggles, periscopes, damp emerald bricks",
]
NAMES = ["Last-Stand Matchbook", "Drainpipe Interrogator", "Noodle Cart Vet", "Gutterglass Scout",
         "Patent Saboteur", "Bribe-Licked Rat", "Subsurface Warden", "Parapet Ghost", "Emergency Molt",
         "Sterile Alley Wire"]
FLAVOR = ["Nobody mentioned the blast radius.", "The questions are so long they stop you walking.",
          "Soup first, stitches second.", "A stolen kit and a quiet step.", "Paperwork with teeth.",
          "Quick enough to deliver a bribe.", "The tide answers to her.", "The cutest nightmare pounces.",
          "Skin comes off, trouble stays.", "A wire nobody sees."]


def _templated(n=10):
    return [
        "An original collectible illustration of {}: a close dramatic equipment portrait showing functional "
        "details. Belongs to {}. Visual story to paint: {} Strong focal storytelling, humorous character "
        "attitude, sharply distinguished subject and environment.".format(NAMES[i], FACTIONS[i % 2], FLAVOR[i])
        for i in range(n)
    ]


HAND = [
    "An oversized scarlet matchbook strapped across a grinning adult rebel's chest, its giant matches lit and "
    "sputtering pink sparks while the rookie beside her in a borrowed hockey helmet edges away.",
    "An adult detective in a dripping trench coat leans out of a drainpipe and talks at a smuggler whose boots "
    "have sunk ankle-deep in sewer sludge, lantern light on wet emerald bricks.",
    "A street vet with tabby ears ladles noodle broth into a patient's mouth with one hand and stitches a "
    "glowing seam across his arm with the other, steam curling from a battered cart.",
    "An adult catgirl scout hangs upside down from a gutter by her tail, peering through a cracked monocle "
    "at a guard who is still mid-yawn three storeys below in blue lab neon.",
    "A pinstriped saboteur in rubber gloves slides a wrench into the gears of a brass patent press, sparks "
    "and springs bursting from its side while a clerk drops his coffee.",
    "A sleek grey rat in a tiny velvet waistcoat sprints along a bar counter clutching a coin bigger than its "
    "head, a bouncer's fist landing a moment too late on the polished wood.",
    "A towering adult warden in brass diving armour wades through a flooded tunnel, a whole canal current "
    "bending around her shins while lantern fish circle her helmet.",
    "A fluffy white ghost kitten with lab-tag ears drifts down from a parapet, claws out and eyes enormous, "
    "toward a startled courier carrying a crate of catnip seedlings.",
    "An adult catgirl peels out of her old skin like a jacket mid-sprint, the empty fur husk left in a "
    "surgeon's grip while she vaults a rooftop vent, laughing.",
    "A spool of nearly invisible silver wire stretched across a rain-slick alley catches a running thug at "
    "the shins, his takeout noodles flying in a perfect arc.",
]


def _ledger(prompts, jobs=False):
    return {"subjects": [{"key": f"s{i}", "prompt_prose": p, **({"jobs": {"krea2": 1}} if jobs else {})}
                         for i, p in enumerate(prompts)]}


def test_template_filled_ledger_is_flagged():
    problems = auth.ledger_problems(_ledger(_templated()))
    rules = {(key, rule) for key, rule, _ in problems}
    assert all((f"s{i}", "templated-prompt") in rules for i in range(10))
    assert all((f"s{i}", "rules-text") in rules for i in range(10))  # "Visual story to paint"


def test_hand_written_ledger_with_shared_style_tail_passes():
    tail = " Every surface bare and unmarked, one continuous scene."
    assert auth.ledger_problems(_ledger([p + tail for p in HAND])) == []


def test_game_keywords_are_rules_text():
    assert auth.rules_text("A street medic with REGEN heals one HP each round.") == ["REGEN", "HP", "each round"]
    assert auth.rules_text("A NASA engineer under a bright moon.") == []


def test_small_ledgers_are_not_judged_as_templates():
    assert auth.ledger_problems(_ledger(_templated(5)[:5]))  # still rules-text
    assert all(rule == "rules-text" for _, rule, _ in auth.ledger_problems(_ledger(_templated(5))))


def test_submitted_cells_are_skipped_by_default():
    assert auth.ledger_problems(_ledger(_templated(), jobs=True)) == []
    assert auth.ledger_problems(_ledger(_templated(), jobs=True), only_unsubmitted=False)


def test_enqueue_refuses_templated_cells(tmp_path):
    ledger = _ledger(_templated())
    ledger["lanes"] = [{"key": "krea2", "engine": "krea2", "prompt": "prose"}]
    for s in ledger["subjects"]:
        s["lane"] = "krea2"
    path = tmp_path / "L.yaml"
    path.write_text(yaml.safe_dump(ledger))
    header, loaded = enq.load_ledger(path)
    posted = []
    cells = list(enq.iter_cells(loaded))
    result = enq.submit(path, header, loaded, cells, post=lambda b: posted.append(b) or (200, {"data": {"jobId": 1}}),
                        live=lambda rows: [{"id": r["id"], "violations": []} for r in rows])
    assert posted == []
    assert result == (0, len(cells))


def test_repo_ledgers_have_no_new_templated_cells():
    failing = {}
    for path in auth.find_ledgers(ROOT):
        try:
            ledger = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(ledger, dict) and auth.ledger_problems(ledger):
            failing[str(path.relative_to(ROOT))] = len(auth.ledger_problems(ledger))
    assert set(failing) <= HELD, {k: v for k, v in failing.items() if k not in HELD}
