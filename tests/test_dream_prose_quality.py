import copy

import scripts.author_dream_proposal as author
import scripts.build_dream_proposal as proposals
from scripts import dream_prose_quality as prose


def _quality_sample():
    proposal = copy.deepcopy(proposals.SAMPLE_PROPOSAL)
    proposal["idea"] = (
        "A courthouse turns every spoken testimony into living color, forcing witnesses "
        "to confront what their answers physically change."
    )
    proposal["vibe"]["line"] = (
        "Every answer changes the room that asked it, so truth becomes architecture."
    )
    proposal["locations"][0].update(
        known_for=(
            "Its prismatic chambers turn spoken testimony into color that stains the walls "
            "until each case is settled."
        ),
        local_rule=(
            "No witness may repeat a hue after their testimony has changed it."
        ),
        best_scene=(
            "A disputed childhood memory turns the courtroom black while every exit "
            "quietly moves to a new wall."
        ),
    )
    proposal["scenarios"][0]["setup"] = (
        "In The Kindly Cross-Examination at The Refracted Court, Mara Venn defends an "
        "engineered witness while the chamber changes color around every disputed answer."
    )
    return proposal


def test_user_facing_prose_accepts_complete_explanatory_copy():
    assert prose.complaints(_quality_sample()) == []


def test_sharp_complete_vibe_line_can_stay_short():
    proposal = _quality_sample()
    proposal["vibe"]["line"] = "The storm only spares the block that out-sings it."

    assert not any("vibe.line" in problem for problem in prose.complaints(proposal))


def test_user_facing_prose_rejects_monsoon_static_style_fragments():
    proposal = _quality_sample()
    proposal["locations"][0].update(
        known_for="rooftop stages wired straight into the flood barriers",
        local_rule="the loudest verse gets the power",
        best_scene="the surge climbs the stairwell while the mast crew hauls glowing silk line back up hand over hand",
    )

    problems = prose.complaints(proposal)

    assert any("known_for is too terse" in problem for problem in problems)
    assert any("known_for must begin" in problem for problem in problems)
    assert any("known_for must end" in problem for problem in problems)
    assert any("local_rule is too terse" in problem for problem in problems)
    assert any("best_scene must end" in problem for problem in problems)


def test_story_diversity_contract_includes_prose_quality_gate(monkeypatch):
    proposal = _quality_sample()
    proposal["locations"][0]["known_for"] = "rooftop stages wired straight into the flood barriers"
    monkeypatch.setattr(author.ruts, "name_rut_complaints", lambda names, facets: [])

    problems = author.story_diversity_complaints(proposal, [], proposal["seed_facets"])

    assert any("known_for is too terse" in problem for problem in problems)


def test_canonical_sample_proposal_satisfies_the_contract_it_documents():
    # The --sample fixture is the worked example of the card-copy contract, so it
    # must not itself be the telegraphic style the gate exists to reject.
    assert prose.complaints(proposals.SAMPLE_PROPOSAL) == []


def test_character_fields_are_card_copy_and_reject_stem_completion_fragments():
    # The 2026-08-16 bundle shipped "keep her cactus herd calm through the quakes
    # so the circus can perform" as a character's whole digest summary: the field
    # was written to complete "**Name** — ", not to be read on its own.
    proposal = _quality_sample()
    proposal["characters"][0].update(
        role_drive="keep her cactus herd calm through the quakes",
        carries="a coil of dragon-scale rope",
        complication="her herd is bred from the last wild line",
    )

    problems = prose.complaints(proposal)

    assert any("characters[0].role_drive must begin" in problem for problem in problems)
    assert any("characters[0].role_drive must end" in problem for problem in problems)
    assert any("characters[0].carries is too terse" in problem for problem in problems)
    assert any("characters[0].complication must begin" in problem for problem in problems)


def test_reward_fields_are_card_copy_and_reject_stem_completion_fragments():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward.update(
            grants="reveals omissions",
            best_used_when="a story is too neat",
            catch="it reveals yours",
        )

    problems = prose.complaints(proposal)

    for label in ("item", "skill"):
        assert any(f"rewards[{label}].grants is too terse" in p for p in problems)
        assert any(f"rewards[{label}].best_used_when must begin" in p for p in problems)
        assert any(f"rewards[{label}].catch must end" in p for p in problems)


def test_art_prompt_fields_stay_exempt_from_the_sentence_contract():
    # `look` and `art_direction` feed Krea and are supposed to be visual noun
    # phrases; forcing them into sentences would degrade the render prompts.
    proposal = _quality_sample()
    proposal["characters"][0]["look"] = "mantis-shrimp advocate in a midnight suit"
    proposal["locations"][0]["art_direction"] = "prismatic courtroom"

    problems = prose.complaints(proposal)

    assert not any("look" in problem for problem in problems)
    assert not any("art_direction" in problem for problem in problems)


def test_label_echo_is_flagged_where_a_label_sits_beside_the_value():
    # "Best scene: The best scene is ..." on a PitchSheet highlight.
    proposal = _quality_sample()
    proposal["locations"][0].update(
        known_for="The Refracted Court is known for turning testimony into staining color.",
        best_scene="The best scene is a disputed memory turning the whole courtroom black.",
        local_rule="The local rule is simple: no witness may repeat a hue they changed.",
    )
    for reward in proposal["rewards"]:
        reward["best_used_when"] = "Use it when a story arrives suspiciously clean and complete."

    problems = prose.complaints(proposal)

    assert any("locations[0].known_for restates its own label" in p for p in problems)
    assert any("locations[0].best_scene restates its own label" in p for p in problems)
    assert any("locations[0].local_rule restates its own label" in p for p in problems)
    # "Use it when ..." now reports under the more precise construction message.
    assert any("rewards[item].best_used_when is an instruction to the reader" in p
               for p in problems)


def test_carries_is_not_treated_as_a_label_echo():
    # Its only user-facing home is the unlabelled Character backstory, where
    # "She carries a cracked spectrum lens" is exactly the right sentence.
    proposal = _quality_sample()
    proposal["characters"][0]["carries"] = (
        "She carries a cracked spectrum lens that still holds her deleted testimony."
    )

    assert not any("carries restates" in p for p in prose.complaints(proposal))


def test_grants_may_open_with_ordinary_english():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward["grants"] = "It grants the bearer one honest answer per hearing."

    assert not any("grants restates" in p for p in prose.complaints(proposal))


def test_label_words_later_in_a_sentence_are_not_an_echo():
    proposal = _quality_sample()
    proposal["locations"][0]["best_scene"] = (
        "A disputed childhood memory turns the courtroom black, which is the best scene "
        "the building has staged in a decade."
    )

    assert not any("best_scene restates" in p for p in prose.complaints(proposal))


def test_best_used_when_rejects_any_verb_it_when_opening():
    # The phrase list only knew "use it when". The catalog was full of the same
    # construction under different verbs, which sailed straight past it.
    proposal = _quality_sample()
    for opening in ("Reach for it when", "Call on it when", "Rely on it when",
                    "Turn to it once", "Use it when"):
        for reward in proposal["rewards"]:
            reward["best_used_when"] = f"{opening} the courtroom has already gone dark."
        problems = prose.complaints(proposal)
        assert any("best_used_when is an instruction to the reader" in p
                   or "best_used_when spends the sentence" in p for p in problems), opening


def test_best_used_when_accepts_a_plain_situation():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward["best_used_when"] = "A story arrives suspiciously clean, with no loose ends at all."

    assert not any("best_used_when" in p for p in prose.complaints(proposal))


def test_a_reward_whose_grants_opens_with_it_is_not_flagged():
    # "It gives ..." must not trip the "<verb> it when" construction check.
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward["grants"] = "It gives a spent voice one more full verse."

    assert not any("instruction to the reader" in p for p in prose.complaints(proposal))


def test_grants_padding_is_flagged():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward["grants"] = "It grants the ability to infer what a blank card once said."

    problems = prose.complaints(proposal)

    assert any("pads the verb that matters" in p for p in problems)


def test_idea_restating_the_vibe_line_is_flagged():
    # The digest prints these two back to back in the vibe row.
    proposal = _quality_sample()
    proposal["vibe"]["line"] = "The whole town's work is keeping one enormous thing asleep."
    proposal["idea"] = (
        "A coastal town's whole economy is keeping one enormous sleeping thing asleep, "
        "and the crop-duster pilot who flies between its ribs has been told to wake it."
    )

    problems = prose.complaints(proposal)

    assert any("idea opens by restating vibe.line" in p for p in problems)


def test_an_idea_that_complements_the_line_is_not_flagged():
    proposal = _quality_sample()
    proposal["vibe"]["line"] = (
        "Every flower here is armed, and so is every heart that lingers too long."
    )
    proposal["idea"] = (
        "In a brimstone-vented greenhouse where bred orchid mantises guard a black market "
        "of grafted cacti, a duelist-wrangler falls for someone she keeps testing."
    )

    assert not any("restating vibe.line" in p for p in prose.complaints(proposal))


def test_a_line_echoed_late_in_a_long_idea_is_not_flagged():
    proposal = _quality_sample()
    proposal["vibe"]["line"] = "Every answer changes the room that asked it."
    proposal["idea"] = (
        "A courthouse refracts testimony into living color across its prismatic chambers, "
        "and witnesses learn the hard way that every answer changes the room that asked it."
    )

    assert not any("restating vibe.line" in p for p in prose.complaints(proposal))


def test_best_used_when_rejects_the_it_verb_when_form_too():
    # Round three at the same defect. Round one banned the literal "use it when";
    # round two banned "<verb> it when" but excluded openings starting with "It"
    # to protect "It gives ...", and 27 rewards promptly sat in that exclusion.
    proposal = _quality_sample()
    for opening in ("It works best when", "It serves best when", "It shines when",
                    "It works when", "It is best when", "This helps when"):
        for reward in proposal["rewards"]:
            reward["best_used_when"] = f"{opening} the courtroom has already gone dark."
        problems = prose.complaints(proposal)
        assert any("best_used_when spends the sentence" in p for p in problems), opening


def test_a_situation_that_merely_begins_with_it_is_left_alone():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward["best_used_when"] = (
            "It is the only moment the tide runs low enough to cross the reach."
        )

    assert not any("best_used_when" in p for p in prose.complaints(proposal))


def test_best_used_when_rejects_the_claim_moved_to_the_end():
    # Round four, and the first defect this file caught its own repair lane
    # creating. Told to drop the opening frame, the repair model moved it to the
    # tail: "... is exactly the moment this ladle earns its keep." Same sentence,
    # same wasted clause, and a leading-only check reports it clean.
    proposal = _quality_sample()
    for tail in ("is exactly the moment this ladle earns its keep",
                 "is when this treaty proves most valuable",
                 "is precisely the situation this was made for",
                 "is exactly where this draw belongs",
                 "is the moment this locket's promise takes hold"):
        for reward in proposal["rewards"]:
            reward["best_used_when"] = f"A disputed memory turns the courtroom black, which {tail}."
        problems = prose.complaints(proposal)
        assert any("best_used_when spends the sentence" in p for p in problems), tail


def test_best_used_when_rejects_a_when_opening_and_an_imperative():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward["best_used_when"] = "When the courtroom has gone dark, this keeps the peace."
    assert any("opens with 'when'" in p for p in prose.complaints(proposal))

    for reward in proposal["rewards"]:
        reward["best_used_when"] = "Study the disputed memory up close without entering the chamber."
    assert any("is an instruction to the reader" in p for p in prose.complaints(proposal))


def test_reward_and_location_copy_may_not_hard_code_the_character():
    # Every asset is meant to be liftable into another story on its own, so a
    # reward welded to one name cannot be mixed. The Scenario is exempt by design.
    proposal = _quality_sample()
    name = proposal["characters"][0]["name"].split()[0]
    proposal["rewards"][0]["grants"] = f"It lets {name} read a hearing before the first word lands."
    proposal["locations"][0]["best_scene"] = f"At dusk {name} balances on the witness rail, testing a hue."

    problems = prose.complaints(proposal)
    assert any("rewards[item].grants hard-codes the character name" in p for p in problems)
    assert any("locations[0].best_scene hard-codes the character name" in p for p in problems)
    assert not any("scenarios" in p and "hard-codes" in p for p in problems)


def test_a_scenario_may_name_the_character_freely():
    proposal = _quality_sample()
    name = proposal["characters"][0]["name"]
    proposal["scenarios"][0]["setup"] = (
        f"{name} must prove a hue was never spoken while the court repaints itself around the claim, "
        "and every honest answer costs another shade of the room."
    )

    assert not any("hard-codes" in p for p in prose.complaints(proposal))


def test_schema_vocabulary_never_reaches_card_copy():
    proposal = _quality_sample()
    proposal["scenarios"][0]["setup"] = (
        "Under the vibe Paperwork for a God, a clerk is mid-stamp when the real inspector "
        "wades ashore on the tide, holding a decade of forged authorizations."
    )

    assert any("names the schema out loud" in p for p in prose.complaints(proposal))


def test_a_scenario_schema_complaint_says_to_keep_the_vibe_title():
    # The setup is structurally required to contain the vibe title, so a repair
    # that sheds the schema noun by dropping the title fails the whole batch.
    # Run 33463517245 did exactly that, twice, and aborted 17 bundles. The
    # complaint text is what the repair model is handed, so it carries the fix.
    proposal = _quality_sample()
    proposal["scenarios"][0]["setup"] = (
        "Under the dream vibe Refracted Testimony, a clerk is mid-stamp when the real "
        "inspector wades ashore holding a decade of forged authorizations."
    )

    problems = [p for p in prose.complaints(proposal) if "names the schema" in p]

    assert problems, "the schema noun must still be flagged"
    assert "KEEP the vibe title" in problems[0]


def test_grants_may_not_open_by_naming_its_own_reward():
    # The card prints the reward name directly above `grants`, so "The Dawnpin
    # locks any hinge" spends its subject on what the reader just read. The
    # authoring prompt already banned exactly this for `known_for`; it was never
    # applied to `grants`, where a census found 16 of 68 doing it.
    proposal = _quality_sample()
    item = next(r for r in proposal["rewards"] if r["reward_type"] == "ITEM")
    for opening in ("The Spectrum Lens reveals", "The lens reveals", "This cracked lens reveals"):
        item["name"] = "The Spectrum Lens"
        item["grants"] = f"{opening} which hue a witness actually spoke before the room repainted it."
        assert any("opens by naming the reward" in p for p in prose.complaints(proposal)), opening


def test_grants_naming_a_verb_that_matches_the_reward_is_not_self_naming():
    # "Cold Read" + "The ability to read ..." -- `read` there is the verb, not
    # the reward naming itself. Subject position is what makes it an echo.
    proposal = _quality_sample()
    item = next(r for r in proposal["rewards"] if r["reward_type"] == "ITEM")
    item["name"] = "Cold Read"
    item["grants"] = "It reads a witness's injuries and lies in a single glance."
    assert not any("opens by naming" in p for p in prose.complaints(proposal))


def test_a_reward_may_not_be_described_as_granting_itself():
    proposal = _quality_sample()
    item = next(r for r in proposal["rewards"] if r["reward_type"] == "ITEM")
    item["name"] = "Heavensteel Spore Jar"
    item["grants"] = "It grants a sealed jar that stores one breath of bloom-air, safe to study."
    assert any("granting itself" in p for p in prose.complaints(proposal))


def test_reward_copy_may_not_use_a_gendered_pronoun_with_no_antecedent():
    # The card shows the reward alone, so "She starts to feel the next breath"
    # refers to nobody the reader has met.
    proposal = _quality_sample()
    skill = next(r for r in proposal["rewards"] if r["reward_type"] == "SKILL")
    skill["catch"] = "She starts to feel the next answer forming in her own chest, whether she wants to or not."
    assert any("with nobody for it to refer to" in p for p in prose.complaints(proposal))


def test_a_pronoun_bound_inside_its_own_sentence_is_left_alone():
    # "Its previous owner was trusted ... around him" is properly anchored, and
    # so is a singular they. Eleven of fifteen pronoun hits were this shape.
    proposal = _quality_sample()
    skill = next(r for r in proposal["rewards"] if r["reward_type"] == "SKILL")
    for value in (
        "Its previous owner was trusted by everyone around him, right up until that trust got him killed.",
        "It carries an outsider through a hearing they were never taught to survive.",
        "It only works if the performer lets the tremor move through their own body first.",
    ):
        skill["catch"] = value
        assert not any("refer to" in p for p in prose.complaints(proposal)), value


def test_the_reward_type_noun_is_schema_vocabulary_too():
    proposal = _quality_sample()
    skill = next(r for r in proposal["rewards"] if r["reward_type"] == "SKILL")
    skill["grants"] = "This skill lets you reprogram a hue on the fly, seasoning testimony toward any verdict."
    assert any("names the schema out loud" in p for p in prose.complaints(proposal))
