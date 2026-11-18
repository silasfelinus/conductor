import pytest

from scripts.update_downward_mobility_project import (
    TITLE,
    patch_fields,
    pick_project,
)


def test_rename_preserves_identity_and_only_public_visibility():
    project = {
        "id": 42,
        "conductorSlug": "shifting-desks",
        "title": "The Elevator Only Goes Down",
        "isPublic": False,
        "isActive": True,
        "isMature": False,
        "slug": "shifting-desks",
    }
    assert pick_project([project, {"id": 123, "conductorSlug": "other"}]) is project
    assert patch_fields(project) == {"title": TITLE, "isPublic": True}
    assert patch_fields({**project, "title": TITLE, "isPublic": True}) == {}


def test_unsafe_or_ambiguous_project_updates_fail_closed():
    project = {"id": 42, "conductorSlug": "shifting-desks", "title": "Shifting Desks"}
    with pytest.raises(ValueError):
        pick_project([])
    with pytest.raises(ValueError):
        pick_project([project, project])
    with pytest.raises(ValueError):
        pick_project([{**project, "title": "Unrelated Game"}])
    with pytest.raises(ValueError):
        pick_project([{**project, "isMature": True}])
    with pytest.raises(ValueError):
        pick_project([{**project, "id": None}])
