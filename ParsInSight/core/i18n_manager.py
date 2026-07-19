"""
P4rsInSight - Internationalization Manager
Loads JSON translation files and provides a tr() function.
Falls back to English when a key is missing in the active language.
Emits language_changed so all widgets can refresh their text.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from PySide6.QtCore import QObject, Signal

from core.logger import get_logger

log = get_logger("i18n")

# Path to the i18n directory relative to this file
_I18N_DIR = Path(__file__).parent.parent / "i18n"

SUPPORTED_LANGUAGES: dict[str, str] = {
    "tr": "Türkçe",
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "ar": "العربية",
}


class I18nManager(QObject):
    """
    Translation engine.

    Usage
    -----
    from core.i18n_manager import i18n
    text = i18n.tr("dashboard.title")
    i18n.set_language("en")

    Signals
    -------
    language_changed(language_code)
        Emitted after a successful language switch.
    """

    language_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._current_lang: str = "tr"
        self._translations: dict[str, Any] = {}
        self._fallback: dict[str, Any] = {}
        self._load_language("en")  # pre-load English as fallback
        self._fallback = self._translations.copy()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_json(self, lang_code: str) -> dict:
        path = _I18N_DIR / f"{lang_code}.json"
        if not path.exists():
            log.warning("Translation file not found: %s", path)
            return {}
        try:
            with path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            log.error("Failed to load translation %s: %s", lang_code, exc)
            return {}

    def _load_language(self, lang_code: str) -> bool:
        data = self._load_json(lang_code)
        if not data:
            return False
        self._translations = data
        self._current_lang = lang_code
        return True

    @staticmethod
    def _get_nested(data: dict, key: str) -> Optional[str]:
        """Navigate dot-separated keys in nested dict."""
        parts = key.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return str(current) if current is not None else None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_language(self, lang_code: str) -> bool:
        """
        Switch the active language.

        Returns True on success.  Falls back to English on failure.
        Emits language_changed on success.
        """
        if lang_code == self._current_lang:
            return True
        if lang_code not in SUPPORTED_LANGUAGES:
            log.warning("Unsupported language: %s", lang_code)
            return False
        success = self._load_language(lang_code)
        if not success:
            log.warning("Failed to load language %s; keeping %s", lang_code, self._current_lang)
            return False
        log.info("Language switched to: %s", lang_code)
        self.language_changed.emit(lang_code)
        return True

    @property
    def current_language(self) -> str:
        return self._current_lang

    def tr(self, key: str, **kwargs) -> str:
        """
        Return translated string for *key*.

        Supports simple placeholder replacement via **kwargs::

            i18n.tr("greeting", name="Alice")  # "Merhaba, Alice!"

        Falls back to English, then to the raw key if still not found.
        """
        value = self._get_nested(self._translations, key)
        if value is None:
            value = self._get_nested(self._fallback, key)
        if value is None:
            log.debug("Missing translation key: %s", key)
            value = key  # Last resort: return the key itself
        if kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError as exc:
                log.warning("Translation format error for key '%s': %s", key, exc)
        return value

    def language_name(self, lang_code: str) -> str:
        """Return the human-readable name for *lang_code*."""
        return SUPPORTED_LANGUAGES.get(lang_code, lang_code)



# Singleton
i18n = I18nManager()

# Convenience alias
def tr(key: str, **kwargs) -> str:
    """Module-level shortcut for i18n.tr()."""
    return i18n.tr(key, **kwargs)
