"""
P4rsInSight - Main Window
Assembles: sidebar + top bar + stacked page content + terminal panel.
Manages theme switching, page navigation, and search.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger
from core.settings_manager import settings
from ui.components.sidebar import Sidebar
from ui.components.terminal_panel import TerminalPanel
from ui.pages.dashboard import DashboardPage
from ui.pages.driver_assistant import DriverAssistantPage
from ui.pages.learning_center import LearningCenterPage
from ui.pages.maintenance import MaintenancePage
from ui.pages.profiles import ProfilesPage
from ui.pages.settings_page import SettingsPage
from ui.pages.software_center import SoftwareCenterPage
from ui.pages.troubleshooting import TroubleshootingPage
from ui.pages.windows_alternatives import WindowsAlternativesPage
from ui.styles.dark_theme import get_dark_stylesheet
from ui.styles.light_theme import get_light_stylesheet

log = get_logger("main_window")


# Page display info: id → (title_key, subtitle_key)
PAGE_META: dict[str, tuple[str, str]] = {
    "dashboard":            ("dashboard.title",             "dashboard.subtitle"),
    "software_center":      ("software_center.title",       "software_center.subtitle"),
    "windows_alternatives": ("windows_alternatives.title",  "windows_alternatives.subtitle"),
    "profiles":             ("profiles.title",              "profiles.subtitle"),
    "driver_assistant":     ("driver_assistant.title",      "driver_assistant.subtitle"),
    "maintenance":          ("maintenance.title",           "maintenance.subtitle"),
    "learning_center":      ("learning_center.title",       "learning_center.subtitle"),
    "troubleshooting":      ("troubleshooting.title",       "troubleshooting.subtitle"),
    "settings":             ("settings.title",              "settings.title"),
}

PAGE_ORDER = [
    "dashboard", "software_center", "windows_alternatives",
    "profiles", "driver_assistant", "maintenance",
    "learning_center", "troubleshooting", "settings",
]


class MainWindow(QMainWindow):
    """
    Main application window.

    Layout
    ------
    ┌─────────────┬──────────────────────────────────┐
    │             │  TOP BAR (title + search + theme) │
    │   SIDEBAR   ├──────────────────────────────────┤
    │             │  PAGE CONTENT (stacked)           │
    │             ├──────────────────────────────────┤
    │             │  TERMINAL PANEL (slide-in)        │
    └─────────────┴──────────────────────────────────┘
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("P4rsInSight")
        self.setMinimumSize(1050, 680)
        self.resize(1280, 800)

        self._setup_ui()
        self._apply_theme(settings.theme)
        self._navigate("dashboard")

        # Connect settings signals
        settings.theme_changed.connect(self._apply_theme)
        i18n.language_changed.connect(self._retranslate)

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # --- Sidebar ---
        self._sidebar = Sidebar()
        self._sidebar.page_requested.connect(self._navigate)
        root_layout.addWidget(self._sidebar)

        # --- Right area ---
        right_area = QWidget()
        right_area.setObjectName("content_area")
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Top bar
        right_layout.addWidget(self._build_top_bar())

        # Terminal panel (hidden by default)
        self._terminal = TerminalPanel()
        self._terminal.setVisible(False)
        self._terminal.setMinimumHeight(220)
        self._terminal.setMaximumHeight(320)

        # Stack
        self._stack = QStackedWidget()
        self._pages: dict[str, QWidget] = {}
        self._build_pages()
        right_layout.addWidget(self._stack, 1)

        # Terminal at bottom
        right_layout.addWidget(self._terminal)

        root_layout.addWidget(right_area, 1)

    def _build_top_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("top_bar")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)

        # Title area
        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        self._page_title = QLabel("")
        self._page_title.setObjectName("page_title")
        self._page_subtitle = QLabel("")
        self._page_subtitle.setObjectName("page_subtitle")
        title_col.addWidget(self._page_title)
        title_col.addWidget(self._page_subtitle)
        layout.addLayout(title_col, 1)

        # Theme toggle
        self._theme_btn = QPushButton("🌙  Dark" if settings.theme == "light" else "☀️  Light")
        self._theme_btn.setObjectName("theme_toggle")
        self._theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self._theme_btn)

        # Terminal mode toggle
        self._term_btn = QPushButton("💻  Terminal")
        self._term_btn.setObjectName("btn_secondary")
        self._term_btn.setFixedHeight(32)
        self._term_btn.clicked.connect(self._toggle_terminal)
        layout.addWidget(self._term_btn)

        return bar

    def _build_pages(self) -> None:
        page_classes = {
            "dashboard":            lambda: DashboardPage(self._terminal),
            "software_center":      lambda: SoftwareCenterPage(self._terminal),
            "windows_alternatives": lambda: WindowsAlternativesPage(self._terminal),
            "profiles":             lambda: ProfilesPage(self._terminal),
            "driver_assistant":     lambda: DriverAssistantPage(self._terminal),
            "maintenance":          lambda: MaintenancePage(self._terminal),
            "learning_center":      lambda: LearningCenterPage(),
            "troubleshooting":      lambda: TroubleshootingPage(self._terminal),
            "settings":             self._build_settings_page,
        }

        for page_id in PAGE_ORDER:
            page = page_classes[page_id]()
            self._pages[page_id] = page
            self._stack.addWidget(page)

    def _build_settings_page(self) -> SettingsPage:
        page = SettingsPage()
        page.theme_changed.connect(self._apply_theme)
        page.font_size_changed.connect(self._apply_font_size)
        return page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _navigate(self, page_id: str) -> None:
        if page_id not in self._pages:
            log.warning("Unknown page: %s", page_id)
            return

        self._current_page = page_id
        self._stack.setCurrentWidget(self._pages[page_id])
        self._sidebar.set_active(page_id)

        # Update top bar
        meta = PAGE_META.get(page_id, (page_id, ""))
        self._page_title.setText(i18n.tr(meta[0]))
        self._page_subtitle.setText(i18n.tr(meta[1]))

        log.debug("Navigated to: %s", page_id)

    # ------------------------------------------------------------------
    # Theme & Styling
    # ------------------------------------------------------------------

    def _apply_theme(self, theme: str) -> None:
        if theme == "dark":
            stylesheet = get_dark_stylesheet(settings.font_size)
            self._theme_btn.setText("☀️  Light")
        else:
            stylesheet = get_light_stylesheet(settings.font_size)
            self._theme_btn.setText("🌙  Dark")
        QApplication.instance().setStyleSheet(stylesheet)
        settings.set("theme", theme)
        log.debug("Theme applied: %s", theme)

    def _apply_font_size(self, size: int) -> None:
        theme = settings.theme
        if theme == "dark":
            stylesheet = get_dark_stylesheet(size)
        else:
            stylesheet = get_light_stylesheet(size)
        QApplication.instance().setStyleSheet(stylesheet)

    def _toggle_theme(self) -> None:
        new_theme = "dark" if settings.theme == "light" else "light"
        self._apply_theme(new_theme)

    def _toggle_terminal(self) -> None:
        self._terminal.setVisible(not self._terminal.isVisible())

    # ------------------------------------------------------------------
    # i18n
    # ------------------------------------------------------------------

    def _retranslate(self) -> None:
        meta = PAGE_META.get(getattr(self, "_current_page", "dashboard"), ("", ""))
        self._page_title.setText(i18n.tr(meta[0]))
        self._page_subtitle.setText(i18n.tr(meta[1]))
