from __future__ import annotations

from .config import BackendConfig
from .models import AppointmentRecord, CustomerRecord
from .store import InMemorySyncStore
from .validation import (
    ValidationError,
    calculate_appointment_total_cents,
    validate_business_slug,
    validate_cents,
    validate_iso_date,
    validate_iso_datetime,
    validate_minutes,
    validate_optional_email,
    validate_optional_iso_datetime,
    validate_text,
)


class AuthError(PermissionError):
    pass


def success(data: dict) -> dict:
    return {"success": True, "data": data}


def failure(code: str, message: str, field_errors: dict | None = None) -> dict:
    result = {"success": False, "code": code, "message": message}
    if field_errors:
        result["fieldErrors"] = field_errors
    return result


class SuperkateSyncService:
    def __init__(self, *, config: BackendConfig | None = None, store: InMemorySyncStore | None = None) -> None:
        self.config = config or BackendConfig.from_env()
        self.store = store or InMemorySyncStore()

    def health(self) -> dict:
        return success(
            {
                "service": "hair-by-superkate-sync",
                "mode": "local-test" if self.config.is_local_test else "production",
                "database": "fake-in-memory" if self.config.is_local_test else "configured",
            }
        )

    def authenticate(self, authorization: str | None) -> str:
        expected = f"Bearer {self.config.local_auth_token}"
        if authorization != expected:
            raise AuthError("Missing or invalid local test auth token.")
        return self.config.fake_owner_user_id

    def bootstrap(self, *, authorization: str | None) -> dict:
        owner = self.authenticate(authorization)
        return success(
            {
                "businessSlug": self.config.business_slug,
                "ownerUserId": owner,
                "serverVersion": self.store.server_version,
                "features": {
                    "pushCustomers": True,
                    "pushAppointments": True,
                    "pullChanges": True,
                    "directEmailSend": False,
                    "analytics": False,
                },
            }
        )

    def push(self, payload: dict, *, authorization: str | None) -> dict:
        owner = self.authenticate(authorization)
        try:
            business_slug = validate_business_slug(payload.get("businessSlug"), self.config.business_slug)
        except ValidationError as exc:
            return failure("VALIDATION_ERROR", exc.message, {exc.field or "businessSlug": exc.message})

        accepted_customers = []
        accepted_appointments = []
        rejected = []

        for row in payload.get("customers", []):
            try:
                accepted_customers.append(
                    self.store.upsert_customer(self._customer_from_payload(row, owner, business_slug)).as_sync_payload()
                )
            except ValidationError as exc:
                rejected.append({"entity": "customer", "localId": row.get("localId"), "code": "VALIDATION_ERROR", "field": exc.field, "message": exc.message})
            except ValueError as exc:
                rejected.append({"entity": "customer", "localId": row.get("localId"), "code": str(exc), "message": "A newer saved version already exists."})

        for row in payload.get("appointments", []):
            try:
                accepted_appointments.append(
                    self.store.upsert_appointment(self._appointment_from_payload(row, owner, business_slug)).as_sync_payload()
                )
            except ValidationError as exc:
                rejected.append({"entity": "appointment", "localId": row.get("localId"), "code": "VALIDATION_ERROR", "field": exc.field, "message": exc.message})
            except ValueError as exc:
                rejected.append({"entity": "appointment", "localId": row.get("localId"), "code": str(exc), "message": "A newer saved version already exists."})

        return success(
            {
                "accepted": {
                    "customers": accepted_customers,
                    "appointments": accepted_appointments,
                },
                "rejected": rejected,
                "serverVersion": self.store.server_version,
            }
        )

    def pull(self, *, business_slug: str, after_version: int = 0, authorization: str | None) -> dict:
        owner = self.authenticate(authorization)
        validate_business_slug(business_slug, self.config.business_slug)
        customers, appointments = self.store.pull_changes(
            owner_user_id=owner,
            business_slug=business_slug,
            after_version=after_version,
        )
        return success(
            {
                "customers": [c.as_sync_payload() for c in customers],
                "appointments": [a.as_sync_payload() for a in appointments],
                "serverVersion": self.store.server_version,
                "hasMore": False,
            }
        )

    def reset_test_data(self, *, authorization: str | None) -> dict:
        self.authenticate(authorization)
        if not self.config.is_local_test:
            return failure("NOT_AVAILABLE", "Test data reset is unavailable outside local/test mode.")
        self.store.reset()
        return success({"serverVersion": self.store.server_version})

    def _customer_from_payload(self, row: dict, owner: str, business_slug: str) -> CustomerRecord:
        return CustomerRecord(
            local_id=validate_text(row.get("localId"), field="localId"),
            owner_user_id=owner,
            business_slug=business_slug,
            name=validate_text(row.get("name"), field="name"),
            email=validate_optional_email(row.get("email")),
            created_at=validate_iso_datetime(row.get("createdAt"), field="createdAt"),
            updated_at=validate_iso_datetime(row.get("updatedAt"), field="updatedAt"),
            deleted_at=validate_optional_iso_datetime(row.get("deletedAt"), field="deletedAt"),
        )

    def _appointment_from_payload(self, row: dict, owner: str, business_slug: str) -> AppointmentRecord:
        hourly_rate_cents = validate_cents(row.get("hourlyRateCents"), field="hourlyRateCents")
        time_spent_minutes = validate_minutes(row.get("timeSpentMinutes"))
        product_cost_cents = validate_cents(row.get("productCostCents", 0), field="productCostCents")
        expected_total = calculate_appointment_total_cents(
            hourly_rate_cents=hourly_rate_cents,
            time_spent_minutes=time_spent_minutes,
            product_cost_cents=product_cost_cents,
        )
        sent_total = validate_cents(row.get("appointmentTotalCents"), field="appointmentTotalCents")
        if sent_total != expected_total:
            raise ValidationError("Appointment total does not match rate, time, and product cost.", field="appointmentTotalCents")
        return AppointmentRecord(
            local_id=validate_text(row.get("localId"), field="localId"),
            owner_user_id=owner,
            business_slug=business_slug,
            customer_local_id=row.get("customerLocalId") or None,
            client_name_snapshot=validate_text(row.get("clientNameSnapshot"), field="clientNameSnapshot"),
            appointment_date=validate_iso_date(row.get("appointmentDate")),
            hourly_rate_cents=hourly_rate_cents,
            time_spent_minutes=time_spent_minutes,
            product_cost_cents=product_cost_cents,
            appointment_total_cents=sent_total,
            created_at=validate_iso_datetime(row.get("createdAt"), field="createdAt"),
            updated_at=validate_iso_datetime(row.get("updatedAt"), field="updatedAt"),
            deleted_at=validate_optional_iso_datetime(row.get("deletedAt"), field="deletedAt"),
        )
