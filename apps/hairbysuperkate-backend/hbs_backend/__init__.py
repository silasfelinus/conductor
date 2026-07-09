"""Hair by Superkate local/test backend scaffold."""

from .config import BackendConfig
from .service import SuperkateSyncService
from .store import InMemorySyncStore

__all__ = [
    "BackendConfig",
    "InMemorySyncStore",
    "SuperkateSyncService",
]
