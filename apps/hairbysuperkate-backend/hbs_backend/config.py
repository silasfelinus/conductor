from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BackendConfig:
    """Runtime configuration for the local/test backend scaffold.

    The scaffold records the future database URL shape but never opens it. Real
    database connection, secrets, DNS, and deploy configuration remain separate
    human-gated work.
    """

    env: str = "local"
    business_slug: str = "hair-by-superkate"
    fake_owner_user_id: str = "test-owner-superkate"
    local_auth_token: str = "local-test-token"
    database_url: str | None = None

    @property
    def is_local_test(self) -> bool:
        return self.env in {"local", "test"}

    @classmethod
    def from_env(cls) -> "BackendConfig":
        return cls(
            env=os.getenv("HBS_ENV", "local"),
            business_slug=os.getenv("HBS_BUSINESS_SLUG", "hair-by-superkate"),
            fake_owner_user_id=os.getenv("HBS_FAKE_OWNER_USER_ID", "test-owner-superkate"),
            local_auth_token=os.getenv("HBS_LOCAL_AUTH_TOKEN", "local-test-token"),
            database_url=os.getenv("HBS_DATABASE_URL") or None,
        )
