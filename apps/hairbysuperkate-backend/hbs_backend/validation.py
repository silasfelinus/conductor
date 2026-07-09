from __future__ import annotations

from datetime import date, datetime
import re


class ValidationError(ValueError):
    def __init__(self, message: str, *, field: str | None = None):
        super().__init__(message)
        self.message = message
        self.field = field


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MAX_CENTS = 1_000_000
_MAX_MINUTES = 24 * 60


def validate_business_slug(value: object, expected: str = "hair-by-superkate") -> str:
    if value != expected:
        raise ValidationError("Business slug is not available.", field="businessSlug")
    return expected


def validate_text(value: object, *, field: str, max_length: int = 120) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be text.", field=field)
    normalized = value.strip()
    if not normalized:
        raise ValidationError(f"{field} is required.", field=field)
    if len(normalized) > max_length:
        raise ValidationError(f"{field} is too long.", field=field)
    return normalized


def validate_optional_email(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError("Email must be text.", field="email")
    normalized = value.strip().lower()
    if not normalized:
        return None
    if len(normalized) > 254 or not _EMAIL_RE.match(normalized):
        raise ValidationError("Email must look like an email address.", field="email")
    return normalized


def validate_non_negative_int(value: object, *, field: str, max_value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{field} must be a non-negative integer.", field=field)
    if value < 0:
        raise ValidationError(f"{field} must be zero or greater.", field=field)
    if value > max_value:
        raise ValidationError(f"{field} is too large for the v1 test contract.", field=field)
    return value


def validate_cents(value: object, *, field: str) -> int:
    return validate_non_negative_int(value, field=field, max_value=_MAX_CENTS)


def validate_minutes(value: object, *, field: str = "timeSpentMinutes") -> int:
    return validate_non_negative_int(value, field=field, max_value=_MAX_MINUTES)


def validate_iso_datetime(value: object, *, field: str) -> str:
    if value is None:
        raise ValidationError(f"{field} is required.", field=field)
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be an ISO datetime string.", field=field)
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{field} must be a valid ISO datetime.", field=field) from exc
    return value


def validate_optional_iso_datetime(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return validate_iso_datetime(value, field=field)


def validate_iso_date(value: object, *, field: str = "appointmentDate") -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be an ISO date string.", field=field)
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{field} must be a valid ISO date.", field=field) from exc
    return value


def calculate_appointment_total_cents(*, hourly_rate_cents: int, time_spent_minutes: int, product_cost_cents: int) -> int:
    return round((hourly_rate_cents * time_spent_minutes) / 60) + product_cost_cents
