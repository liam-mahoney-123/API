import unittest

from shipt_dark_mode.theme import (
    DARK_THEME,
    LIGHT_THEME,
    InMemoryKeyValueStore,
    PersistedThemePreferenceStore,
    ThemeManager,
    ThemeMode,
    resolve_theme,
)


class ResolveThemeTests(unittest.TestCase):
    def test_explicit_light_mode_ignores_system_dark(self) -> None:
        result = resolve_theme(ThemeMode.LIGHT, system_prefers_dark=True)
        self.assertEqual(result.name, LIGHT_THEME.name)

    def test_explicit_dark_mode_ignores_system_light(self) -> None:
        result = resolve_theme(ThemeMode.DARK, system_prefers_dark=False)
        self.assertEqual(result.name, DARK_THEME.name)

    def test_system_mode_uses_system_dark_value(self) -> None:
        self.assertEqual(
            resolve_theme(ThemeMode.SYSTEM, system_prefers_dark=True).name,
            DARK_THEME.name,
        )
        self.assertEqual(
            resolve_theme(ThemeMode.SYSTEM, system_prefers_dark=False).name,
            LIGHT_THEME.name,
        )


class PreferenceStoreTests(unittest.TestCase):
    def test_default_preference_is_system(self) -> None:
        store = PersistedThemePreferenceStore(InMemoryKeyValueStore())
        self.assertEqual(store.load_mode(), ThemeMode.SYSTEM)

    def test_invalid_preference_falls_back_to_system(self) -> None:
        backend = InMemoryKeyValueStore()
        backend.set("theme_mode", "unexpected")
        store = PersistedThemePreferenceStore(backend)
        self.assertEqual(store.load_mode(), ThemeMode.SYSTEM)

    def test_save_and_load_preference(self) -> None:
        backend = InMemoryKeyValueStore()
        store = PersistedThemePreferenceStore(backend)
        store.save_mode(ThemeMode.DARK)
        self.assertEqual(store.load_mode(), ThemeMode.DARK)


class ThemeManagerTests(unittest.TestCase):
    def test_manager_reads_active_theme_from_system_when_mode_is_system(self) -> None:
        backend = InMemoryKeyValueStore()
        store = PersistedThemePreferenceStore(backend)
        manager = ThemeManager(store, system_dark_provider=lambda: True)
        self.assertEqual(manager.get_active_theme().name, DARK_THEME.name)

    def test_manager_toggles_from_light_to_dark(self) -> None:
        backend = InMemoryKeyValueStore()
        store = PersistedThemePreferenceStore(backend)
        manager = ThemeManager(store, system_dark_provider=lambda: False)
        manager.set_mode(ThemeMode.LIGHT)

        next_mode = manager.toggle_explicit_mode()

        self.assertEqual(next_mode, ThemeMode.DARK)
        self.assertEqual(manager.get_mode(), ThemeMode.DARK)

    def test_manager_toggles_from_system_using_current_active_theme(self) -> None:
        backend = InMemoryKeyValueStore()
        store = PersistedThemePreferenceStore(backend)
        manager = ThemeManager(store, system_dark_provider=lambda: True)
        manager.use_system_mode()

        next_mode = manager.toggle_explicit_mode()

        self.assertEqual(next_mode, ThemeMode.LIGHT)
        self.assertEqual(manager.get_mode(), ThemeMode.LIGHT)


if __name__ == "__main__":
    unittest.main()
