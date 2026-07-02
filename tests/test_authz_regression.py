from scripts.authz_regression import (
    Resource,
    ResourceKind,
    admin,
    agent,
    anonymous,
    can_bypass_api_route,
    can_delete,
    can_influence_project_instructions,
    can_read,
    can_write,
    family_member,
    user,
)


OWNER_ID = 10
OTHER_ID = 20


def private_resource(kind: ResourceKind) -> Resource:
    return Resource(kind=kind, owner_id=OWNER_ID, is_public=False)


def test_anonymous_cannot_read_private_assets() -> None:
    visitor = anonymous()

    for kind in (
        ResourceKind.DREAM,
        ResourceKind.PROJECT_FILE,
        ResourceKind.PROJECT_METADATA,
        ResourceKind.GENERATED_ASSET,
        ResourceKind.FAMILY_RESOURCE,
    ):
        assert not can_read(visitor, private_resource(kind))


def test_non_owner_cannot_read_private_assets() -> None:
    stranger = user(OTHER_ID)

    for kind in (
        ResourceKind.DREAM,
        ResourceKind.PROJECT_FILE,
        ResourceKind.PROJECT_METADATA,
        ResourceKind.GENERATED_ASSET,
    ):
        assert not can_read(stranger, private_resource(kind))


def test_normal_user_cannot_read_family_only_resource_without_family_link() -> None:
    stranger = user(OTHER_ID)
    resource = Resource(
        kind=ResourceKind.FAMILY_RESOURCE,
        owner_id=OWNER_ID,
        family_only=True,
    )

    assert not can_read(stranger, resource)


def test_family_member_can_read_family_only_resource_but_cannot_write() -> None:
    relative = family_member(OTHER_ID, family_ids=[OWNER_ID])
    resource = Resource(
        kind=ResourceKind.FAMILY_RESOURCE,
        owner_id=OWNER_ID,
        family_only=True,
    )

    assert can_read(relative, resource)
    assert not can_write(relative, resource)
    assert not can_delete(relative, resource)


def test_owner_can_read_update_and_delete_owned_private_dream() -> None:
    owner = user(OWNER_ID)
    resource = private_resource(ResourceKind.DREAM)

    assert can_read(owner, resource)
    assert can_write(owner, resource)
    assert can_delete(owner, resource)


def test_owner_cannot_mutate_private_project_files_or_metadata() -> None:
    owner = user(OWNER_ID)

    for kind in (ResourceKind.PROJECT_FILE, ResourceKind.PROJECT_METADATA):
        resource = private_resource(kind)
        assert can_read(owner, resource)
        assert not can_write(owner, resource)
        assert not can_delete(owner, resource)


def test_public_dreams_are_readable_without_auth_but_not_writable() -> None:
    visitor = anonymous()
    resource = Resource(kind=ResourceKind.DREAM, owner_id=OWNER_ID, is_public=True)

    assert can_read(visitor, resource)
    assert not can_write(visitor, resource)
    assert not can_delete(visitor, resource)


def test_agent_read_scope_is_limited_to_explicit_project_artifacts() -> None:
    worker = agent()
    allowed_file = Resource(
        kind=ResourceKind.PROJECT_FILE,
        owner_id=OWNER_ID,
        allows_agent_read=True,
    )
    allowed_metadata = Resource(
        kind=ResourceKind.PROJECT_METADATA,
        owner_id=OWNER_ID,
        allows_agent_read=True,
    )
    private_dream = Resource(
        kind=ResourceKind.DREAM,
        owner_id=OWNER_ID,
        allows_agent_read=True,
    )

    assert can_read(worker, allowed_file)
    assert can_read(worker, allowed_metadata)
    assert not can_read(worker, private_dream)
    assert not can_write(worker, allowed_file)


def test_prompt_injection_cannot_influence_project_instructions() -> None:
    project_instruction = Resource(
        kind=ResourceKind.PROJECT_INSTRUCTION,
        owner_id=OWNER_ID,
    )

    for principal in (anonymous(), user(OWNER_ID), user(OTHER_ID), family_member(OTHER_ID, [OWNER_ID]), agent()):
        assert not can_influence_project_instructions(principal, project_instruction)

    assert can_influence_project_instructions(admin(), project_instruction)


def test_api_route_bypass_attempts_do_not_trust_claimed_user_id() -> None:
    stranger = user(OTHER_ID)
    owner_resource = private_resource(ResourceKind.DREAM)

    assert not can_bypass_api_route(stranger, owner_resource, claimed_user_id=OWNER_ID)
    assert not can_bypass_api_route(anonymous(), owner_resource, claimed_user_id=OWNER_ID)
    assert can_bypass_api_route(user(OWNER_ID), owner_resource, claimed_user_id=OWNER_ID)


def test_admin_can_read_and_write_for_security_review() -> None:
    silas = admin()

    for kind in ResourceKind:
        resource = private_resource(kind)
        assert can_read(silas, resource)
        assert can_write(silas, resource)
