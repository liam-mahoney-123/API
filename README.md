# Shipt Mobile App - Dark Mode Foundation

This repository now includes a small, production-oriented dark mode foundation
module for mobile apps:

- Semantic theme tokens (`ThemeTokens`) for light and dark palettes
- User preference modes (`LIGHT`, `DARK`, `SYSTEM`)
- Theme resolution logic based on user preference and system appearance
- Persistence abstraction for storing user selection
- A manager class that coordinates persistence + runtime resolution
- Unit tests covering the above behavior

## Module layout

- `shipt_dark_mode/theme.py`: core theme primitives and manager
- `shipt_dark_mode/__init__.py`: public exports
- `tests/test_theme.py`: unit tests

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Integration notes for mobile clients

1. Replace `InMemoryKeyValueStore` with your platform storage adapter
   (for example, secure prefs/user defaults/async storage).
2. Inject a real `system_dark_provider` that reads the OS appearance setting.
3. Consume `Theme.tokens` in UI components instead of hardcoded colors.
4. Expose a settings control with `Light`, `Dark`, and `System`.
