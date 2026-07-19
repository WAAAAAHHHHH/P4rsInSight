"""
P4rsInSight - Sidebar Navigation Widget
Left navigation bar with text-only nav items, active state highlight and left accent border.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n


# Nav items — label_short is a 2-char uppercase abbreviation used as a visual icon
NAV_ITEMS: list[dict] = [
    {"id": "dashboard",             "abbr": "DB", "key": "nav.dashboard"},
    {"id": "software_center",       "abbr": "SW", "key": "nav.software_center"},
    {"id": "windows_alternatives",  "abbr": "WA", "key": "nav.windows_alternatives"},
    {"id": "profiles",              "abbr": "PR", "key": "nav.profiles"},
    {"id": "driver_assistant",      "abbr": "DV", "key": "nav.driver_assistant"},
    {"id": "maintenance",           "abbr": "MT", "key": "nav.maintenance"},
    {"id": "learning_center",       "abbr": "LC", "key": "nav.learning_center"},
    {"id": "troubleshooting",       "abbr": "TS", "key": "nav.troubleshooting"},
    {"id": "settings",              "abbr": "ST", "key": "nav.settings"},
]


class Sidebar(QWidget):
    """
    Left navigation sidebar.

    Signals
    -------
    page_requested(page_id)
        Emitted when the user clicks a nav item.
    """

    page_requested = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._active_id: str = "dashboard"
        self._buttons: dict[str, QPushButton] = {}
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # --- Logo area ---
        logo_area = QWidget()
        logo_area.setObjectName("sidebar_logo_area")
        logo_area.setFixedHeight(86)
        logo_layout = QVBoxLayout(logo_area)
        logo_layout.setContentsMargins(18, 16, 18, 16)
        logo_layout.setSpacing(3)

        self._app_name = QLabel("P4rsInSight")
        self._app_name.setObjectName("sidebar_app_name")

        self._tagline = QLabel(i18n.tr("app.tagline"))
        self._tagline.setObjectName("sidebar_tagline")
        self._tagline.setWordWrap(True)

        logo_layout.addWidget(self._app_name)
        logo_layout.addWidget(self._tagline)
        outer.addWidget(logo_area)

        # --- Divider ---
        div = QWidget()
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,0.15);")
        outer.addWidget(div)

        # --- Scrollable nav area ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        nav_widget = QWidget()
        self._nav_layout = QVBoxLayout(nav_widget)
        self._nav_layout.setContentsMargins(0, 10, 0, 10)
        self._nav_layout.setSpacing(2)
        self._nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._build_nav_items()

        scroll.setWidget(nav_widget)
        outer.addWidget(scroll, 1)

        # --- Version footer ---
        footer = QLabel("v 1.0.0")
        footer.setObjectName("sidebar_tagline")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setContentsMargins(0, 8, 0, 12)
        outer.addWidget(footer)

    def _build_nav_items(self) -> None:
        for item in NAV_ITEMS:
            label = i18n.tr(item["key"])
            btn = QPushButton(label)
            btn.setObjectName("sidebar_item")
            btn.setProperty("active", "false")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip(label)

            page_id = item["id"]
            btn.clicked.connect(lambda checked=False, pid=page_id: self._on_nav_click(pid))

            self._buttons[page_id] = btn
            self._nav_layout.addWidget(btn)

        self._update_active()

    def _on_nav_click(self, page_id: str) -> None:
        self._active_id = page_id
        self._update_active()
        self.page_requested.emit(page_id)

    def _update_active(self) -> None:
        for pid, btn in self._buttons.items():
            is_active = pid == self._active_id
            btn.setProperty("active", "true" if is_active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def set_active(self, page_id: str) -> None:
        """Programmatically activate a nav item."""
        self._active_id = page_id
        self._update_active()

    def _retranslate(self) -> None:
        """Update all text after language change."""
        self._tagline.setText(i18n.tr("app.tagline"))
        for item in NAV_ITEMS:
            if item["id"] in self._buttons:
                label = i18n.tr(item["key"])
                btn = self._buttons[item["id"]]
                btn.setText(label)
                btn.setToolTip(label)
