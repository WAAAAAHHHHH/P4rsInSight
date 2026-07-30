"""
P4rsInSight - Settings Manager
Reads and writes user configuration from/to ~/.config/parsinSight/settings.json.
Emits Qt signals when settings change so widgets can react instantly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal

from core.logger import get_logger

log = get_logger("settings_manager")

_DEFAULTS: dict[str, Any] = {
    "language": "tr",
    "font_size": 13,
    "animations_enabled": True,
    "terminal_learning_mode": True,
    "notifications_enabled": True,
    "experience_level": "beginner",       # beginner | intermediate | advanced
    "first_launch": True,
}

_CONFIG_DIR = Path.home() / ".config" / "parsinSight"
_CONFIG_FILE = _CONFIG_DIR / "settings.json"


class SettingsManager(QObject):
    """
    Central settings store.  Import the singleton ``settings`` from this module
    rather than instantiating directly.

    Signals
    -------
    setting_changed(key, value)
        Emitted whenever a setting is updated.
    language_changed(language_code)
        Emitted specifically when the language setting changes.
    """

    setting_changed = Signal(str, object)
    language_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._data: dict[str, Any] = dict(_DEFAULTS)
        self._load()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Load settings from disk, falling back to defaults for missing keys."""
        if _CONFIG_FILE.exists():
            try:
                with _CONFIG_FILE.open("r", encoding="utf-8") as fh:
                    stored = json.load(fh)
                self._data.update(stored)
                log.debug("Settings loaded from %s", _CONFIG_FILE)
            except (json.JSONDecodeError, OSError) as exc:
                log.warning("Could not load settings (%s) — using defaults", exc)
        else:
            log.debug("No settings file found — using defaults")

    def _save(self) -> None:
        """Persist current settings to disk."""
        try:
            _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with _CONFIG_FILE.open("w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=2, ensure_ascii=False)
            log.debug("Settings saved to %s", _CONFIG_FILE)
        except OSError as exc:
            log.error("Could not save settings: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for *key*, or *default* if not found."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Update *key* and persist to disk.  Emits ``setting_changed``."""
        self._data[key] = value
        self._save()
        self.setting_changed.emit(key, value)
        if key == "language":
            self.language_changed.emit(str(value))

    # Typed convenience properties -------------------------------------------

    @property
    def language(self) -> str:
        return str(self._data.get("language", "tr"))

    @language.setter
    def language(self, value: str) -> None:
        self.set("language", value)



    @property
    def font_size(self) -> int:
        return int(self._data.get("font_size", 13))

    @font_size.setter
    def font_size(self, value: int) -> None:
        self.set("font_size", value)

    @property
    def animations_enabled(self) -> bool:
        return bool(self._data.get("animations_enabled", True))

    @property
    def terminal_learning_mode(self) -> bool:
        return bool(self._data.get("terminal_learning_mode", True))

    @property
    def notifications_enabled(self) -> bool:
        return bool(self._data.get("notifications_enabled", True))

    @property
    def experience_level(self) -> str:
        return str(self._data.get("experience_level", "beginner"))

    @property
    def first_launch(self) -> bool:
        return bool(self._data.get("first_launch", True))

    @first_launch.setter
    def first_launch(self, value: bool) -> None:
        self.set("first_launch", value)


# Singleton instance — import this everywhere
settings = SettingsManager()
