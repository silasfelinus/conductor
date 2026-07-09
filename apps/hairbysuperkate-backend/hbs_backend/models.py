from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_server_id(prefix: str) -> str:
    return f"srv_{prefix}_{uuid4().hex}"


@dataclass(frozen=True)
class CustomerRecord:
    local_id: str
    name: str
    email: str | None
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    server_id: str = field(default_factory=lambda: new_server_id("customer"))
    owner_user_id: str = "test-owner-superkate"
    business_slug: str = "hair-by-superkate"
    server_version: int = 0
    synced_at: str = field(default_factory=utc_now_iso)

    def with_server_state(self, *, server_version: int, synced_at: str) -> "CustomerRecord":
        return replace(self, server_version=server_version, synced_at=synced_at)

    def as_sync_payload(self) -> dict:
        return {
            "entity": "customer",
            "localId": self.local_id,
            "serverId": self.server_id,
            "ownerUserId": self.owner_user_id,
            "businessSlug": self.business_slug,
            "name": self.name,
            "email": self.email,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
            "serverVersion": self.server_version,
            "syncedAt": self.synced_at,
        }


@dataclass(frozen=True)
class AppointmentRecord:
    local_id: str
    client_name_snapshot: str
    appointment_date: str
    hourly_rate_cents: int
    time_spent_minutes: int
    product_cost_cents: int
    appointment_total_cents: int
    created_at: str
    updated_at: str
    customer_local_id: str | None = None
    deleted_at: str | None = None
    server_id: str = field(default_factory=lambda: new_server_id("appointment"))
    customer_server_id: str | None = None
    owner_user_id: str = "test-owner-superkate"
    business_slug: str = "hair-by-superkate"
    server_version: int = 0
    synced_at: str = field(default_factory=utc_now_iso)

    def with_server_state(self, *, server_version: int, synced_at: str) -> "AppointmentRecord":
        return replace(self, server_version=server_version, synced_at=synced_at)

    def as_sync_payload(self) -> dict:
        return {
            "entity": "appointment",
            "localId": self.local_id,
            "serverId": self.server_id,
            "ownerUserId": self.owner_user_id,
            "businessSlug": self.business_slug,
            "customerLocalId": self.customer_local_id,
            "customerServerId": self.customer_server_id,
            "clientNameSnapshot": self.client_name_snapshot,
            "appointmentDate": self.appointment_date,
            "hourlyRateCents": self.hourly_rate_cents,
            "timeSpentMinutes": self.time_spent_minutes,
            "productCostCents": self.product_cost_cents,
            "appointmentTotalCents": self.appointment_total_cents,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
            "serverVersion": self.server_version,
            "syncedAt": self.synced_at,
        }
