"""Dark mode primitives for a mobile app."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, Protocol


class ThemeMode(str, Enum):
    """User preference for theme selection."""

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass(frozen=True)
class ThemeTokens:
    """Semantic color tokens consumed by UI components."""

    background: str
    surface: str
    text_primary: str
    text_secondary: str
    border: str
    accent: str
    success: str
    warning: str
    error: str


@dataclass(frozen=True)
class Theme:
    """Named theme wrapper with token payload."""

    name: str
    tokens: ThemeTokens


LIGHT_THEME = Theme(
    name="light",
    tokens=ThemeTokens(
        background="#FFFFFF",
        surface="#F8FAFC",
        text_primary="#111827",
        text_secondary="#4B5563",
        border="#E5E7EB",
        accent="#0077C8",
        success="#0C8F49",
        warning="#A16207",
        error="#B42318",
    ),
)


DARK_THEME = Theme(
    name="dark",
    tokens=ThemeTokens(
        background="#0B1220",
        surface="#111827",
        text_primary="#F9FAFB",
        text_secondary="#9CA3AF",
        border="#374151",
        accent="#4BA3FF",
        success="#35C77A",
        warning="#F59E0B",
        error="#F97066",
    ),
)


class KeyValueStore(Protocol):
    """Persistence contract for user preferences."""

    def get(self, key: str) -> Optional[str]:
        """Return a stored value if present."""

    def set(self, key: str, value: str) -> None:
        """Persist a value."""


class InMemoryKeyValueStore:
    """Simple in-memory store useful for tests and local flows."""

    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value


class PersistedThemePreferenceStore:
    """Read/write theme mode to a key-value backend."""

    def __init__(self, key_value_store: KeyValueStore, key: str = "theme_mode") -> None:
        self._store = key_value_store
        self._key = key

    def load_mode(self) -> ThemeMode:
        raw_value = self._store.get(self._key)
        if raw_value is None:
            return ThemeMode.SYSTEM
        try:
            return ThemeMode(raw_value)
        except ValueError:
            return ThemeMode.SYSTEM

    def save_mode(self, mode: ThemeMode) -> None:
        self._store.set(self._key, mode.value)


def resolve_theme(mode: ThemeMode, system_prefers_dark: bool) -> Theme:
    """Resolve the active theme from user mode + system appearance."""

    if mode == ThemeMode.LIGHT:
        return LIGHT_THEME
    if mode == ThemeMode.DARK:
        return DARK_THEME
    return DARK_THEME if system_prefers_dark else LIGHT_THEME


class ThemeManager:
    """Coordinator that resolves and persists app theme settings."""

    def __init__(
        self,
        preference_store: PersistedThemePreferenceStore,
        system_dark_provider: Optional[Callable[[], bool]] = None,
    ) -> None:
        self._preference_store = preference_store
        self._system_dark_provider = system_dark_provider or (lambda: False)

    def get_mode(self) -> ThemeMode:
        return self._preference_store.load_mode()

    def set_mode(self, mode: ThemeMode) -> None:
        self._preference_store.save_mode(mode)

    def use_system_mode(self) -> None:
        self.set_mode(ThemeMode.SYSTEM)

    def get_active_theme(self) -> Theme:
        return resolve_theme(
            mode=self.get_mode(),
            system_prefers_dark=self._system_dark_provider(),
        )

    def toggle_explicit_mode(self) -> ThemeMode:
        """Toggle between explicit light and dark user settings."""

        current_mode = self.get_mode()
        if current_mode == ThemeMode.LIGHT:
            next_mode = ThemeMode.DARK
        elif current_mode == ThemeMode.DARK:
            next_mode = ThemeMode.LIGHT
        else:
            active_is_dark = self.get_active_theme().name == DARK_THEME.name
            next_mode = ThemeMode.LIGHT if active_is_dark else ThemeMode.DARK
        self.set_mode(next_mode)
        return next_mode
