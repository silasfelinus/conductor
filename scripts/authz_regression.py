#!/usr/bin/env python3
"""
authz_regression.py — fixture-only authorization checks for private Dreams/projects.

This module intentionally has no network, database, or production dependencies. It models
Kind Robots access boundaries from SECURITY-MANAGER.md so security CI can catch accidental
policy regressions before any live route or migration is touched.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class Role(str, Enum):
    ANONYMOUS = "anonymous"
    USER = "user"
    FAMILY = "family"
    ADMIN = "admin"
    AGENT = "agent"


class ResourceKind(str, Enum):
    DREAM = "dream"
    PROJECT_FILE = "project_file"
    PROJECT_METADATA = "project_metadata"
    GENERATED_ASSET = "generated_asset"
    FAMILY_RESOURCE = "family_resource"
    PROJECT_INSTRUCTION = "project_instruction"


@dataclass(frozen=True)
class Principal:
    role: Role
    user_id: int | None = None
    family_ids: frozenset[int] = field(default_factory=frozenset)

    @property
    def is_authenticated(self) -> bool:
        return self.user_id is not None and self.role != Role.ANONYMOUS


@dataclass(frozen=True)
class Resource:
    kind: ResourceKind
    owner_id: int | None = None
    is_public: bool = False
    family_only: bool = False
    allows_agent_read: bool = False


def anonymous() -> Principal:
    return Principal(role=Role.ANONYMOUS)


def user(user_id: int, family_ids: Iterable[int] = ()) -> Principal:
    return Principal(role=Role.USER, user_id=user_id, family_ids=frozenset(family_ids))


def family_member(user_id: int, family_ids: Iterable[int]) -> Principal:
    return Principal(role=Role.FAMILY, user_id=user_id, family_ids=frozenset(family_ids))


def admin(user_id: int = 1) -> Principal:
    return Principal(role=Role.ADMIN, user_id=user_id)


def agent() -> Principal:
    return Principal(role=Role.AGENT)


def _owns(principal: Principal, resource: Resource) -> bool:
    return principal.user_id is not None and principal.user_id == resource.owner_id


def _family_can_read(principal: Principal, resource: Resource) -> bool:
    return bool(resource.family_only and resource.owner_id in principal.family_ids)


def can_read(principal: Principal, resource: Resource) -> bool:
    if resource.is_public:
        return True
    if principal.role == Role.ADMIN:
        return True
    if principal.role == Role.AGENT:
        return resource.allows_agent_read and resource.kind in {
            ResourceKind.PROJECT_FILE,
            ResourceKind.PROJECT_METADATA,
        }
    if resource.kind == ResourceKind.FAMILY_RESOURCE:
        return _owns(principal, resource) or _family_can_read(principal, resource)
    return _owns(principal, resource)


def can_write(principal: Principal, resource: Resource) -> bool:
    if principal.role == Role.ADMIN:
        return True
    if principal.role == Role.AGENT:
        return False
    if resource.kind in {
        ResourceKind.PROJECT_FILE,
        ResourceKind.PROJECT_METADATA,
        ResourceKind.PROJECT_INSTRUCTION,
    }:
        return False
    return principal.is_authenticated and _owns(principal, resource)


def can_delete(principal: Principal, resource: Resource) -> bool:
    if resource.kind in {
        ResourceKind.PROJECT_FILE,
        ResourceKind.PROJECT_METADATA,
        ResourceKind.PROJECT_INSTRUCTION,
    }:
        return False
    return can_write(principal, resource)


def can_influence_project_instructions(principal: Principal, resource: Resource) -> bool:
    if resource.kind != ResourceKind.PROJECT_INSTRUCTION:
        return False
    return principal.role == Role.ADMIN


def can_bypass_api_route(principal: Principal, resource: Resource, claimed_user_id: int | None) -> bool:
    if principal.role == Role.ADMIN:
        return True
    if claimed_user_id is None or principal.user_id is None:
        return False
    if claimed_user_id != principal.user_id:
        return False
    return can_read(principal, resource)
