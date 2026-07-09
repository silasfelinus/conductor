from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .models import AppointmentRecord, CustomerRecord, utc_now_iso


class InMemorySyncStore:
    """Tiny fake-data store for local scaffold tests.

    This mimics owner/business scoping and monotonic server versions without
    opening a real database connection.
    """

    def __init__(self) -> None:
        self._customers: dict[tuple[str, str, str], CustomerRecord] = {}
        self._appointments: dict[tuple[str, str, str], AppointmentRecord] = {}
        self._server_version = 0

    @property
    def server_version(self) -> int:
        return self._server_version

    def reset(self) -> None:
        self._customers.clear()
        self._appointments.clear()
        self._server_version = 0

    def upsert_customer(self, record: CustomerRecord) -> CustomerRecord:
        key = (record.owner_user_id, record.business_slug, record.local_id)
        existing = self._customers.get(key)
        if existing is not None and record.updated_at < existing.updated_at:
            raise ValueError("CONFLICT")
        self._server_version += 1
        saved = record
        if existing is not None:
            saved = replace(record, server_id=existing.server_id)
        saved = saved.with_server_state(
            server_version=self._server_version,
            synced_at=utc_now_iso(),
        )
        self._customers[key] = saved
        return saved

    def upsert_appointment(self, record: AppointmentRecord) -> AppointmentRecord:
        key = (record.owner_user_id, record.business_slug, record.local_id)
        existing = self._appointments.get(key)
        if existing is not None and record.updated_at < existing.updated_at:
            raise ValueError("CONFLICT")
        if record.customer_local_id:
            customer_key = (record.owner_user_id, record.business_slug, record.customer_local_id)
            customer = self._customers.get(customer_key)
        else:
            customer = None
        self._server_version += 1
        saved = record
        if existing is not None:
            saved = replace(record, server_id=existing.server_id)
        if customer is not None:
            saved = replace(saved, customer_server_id=customer.server_id)
        saved = saved.with_server_state(
            server_version=self._server_version,
            synced_at=utc_now_iso(),
        )
        self._appointments[key] = saved
        return saved

    def pull_changes(self, *, owner_user_id: str, business_slug: str, after_version: int = 0) -> tuple[list[CustomerRecord], list[AppointmentRecord]]:
        customers = self._filter_changes(
            self._customers.values(),
            owner_user_id=owner_user_id,
            business_slug=business_slug,
            after_version=after_version,
        )
        appointments = self._filter_changes(
            self._appointments.values(),
            owner_user_id=owner_user_id,
            business_slug=business_slug,
            after_version=after_version,
        )
        return customers, appointments

    @staticmethod
    def _filter_changes(records: Iterable, *, owner_user_id: str, business_slug: str, after_version: int):
        return sorted(
            [
                r
                for r in records
                if r.owner_user_id == owner_user_id
                and r.business_slug == business_slug
                and r.server_version > after_version
            ],
            key=lambda r: r.server_version,
        )
