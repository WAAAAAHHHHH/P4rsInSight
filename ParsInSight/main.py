"""
P4rsInSight - Application Entry Point
Initializes logging, settings, i18n, QApplication, and launches the main window.
Shows the first-launch wizard on first run.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on Python path
_ROOT = Path(__file__).parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from core.logger import setup_logging, get_logger
from core.settings_manager import settings
from core.i18n_manager import i18n


def main() -> int:
    # ── 1. Logging ────────────────────────────────────────────────────
    setup_logging()
    log = get_logger("main")
    log.info("=" * 60)
    log.info("P4rsInSight starting up")
    log.info("=" * 60)

    # ── 2. QApplication ───────────────────────────────────────────────
    app = QApplication(sys.argv)
    app.setApplicationName("P4rsInSight")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("TÜBİTAK Pardus")
    # High DPI is enabled by default in Qt6 — no manual flag needed

    # ── 3. i18n — load active language ───────────────────────────────
    i18n.set_language(settings.language)
    log.info("Language set to: %s", settings.language)

    # ── 4. Apply initial stylesheet ───────────────────────────────────
    from ui.styles.dark_theme import get_dark_stylesheet

    app.setStyleSheet(get_dark_stylesheet(settings.font_size))
    log.info("Theme applied: dark")

    # ── 5. Show first-launch wizard if needed ─────────────────────────
    if settings.first_launch:
        from ui.pages.welcome_wizard import WelcomeWizard
        wizard = WelcomeWizard()
        wizard.setup_complete.connect(
            lambda lang, level: _on_wizard_complete(app, lang, level)
        )
        result = wizard.exec()
        log.info("Wizard completed with result: %s", result)

    # ── 6. Main window ────────────────────────────────────────────────
    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()
    log.info("Main window shown")

    return app.exec()


def _on_wizard_complete(
    app: QApplication, lang: str, level: str
) -> None:
    """Apply wizard choices before main window opens."""
    from ui.styles.dark_theme import get_dark_stylesheet

    i18n.set_language(lang)
    app.setStyleSheet(get_dark_stylesheet(settings.font_size))


if __name__ == "__main__":
    sys.exit(main())
