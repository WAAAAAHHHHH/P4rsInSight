"""
P4rsInSight - Sidebar Navigation Widget
Minimal left navigation bar. No emojis — clean text labels with
left-border active indicator and pinned settings at the bottom.
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


# Primary nav items
NAV_ITEMS: list[dict] = [
    {"id": "dashboard",             "key": "nav.dashboard"},
    {"id": "software_center",       "key": "nav.software_center"},
    {"id": "windows_alternatives",  "key": "nav.windows_alternatives"},
    {"id": "profiles",              "key": "nav.profiles"},
    {"id": "driver_assistant",      "key": "nav.driver_assistant"},
    {"id": "maintenance",           "key": "nav.maintenance"},
    {"id": "learning_center",       "key": "nav.learning_center"},
    {"id": "troubleshooting",       "key": "nav.troubleshooting"},
]

# Pinned at the bottom
BOTTOM_ITEMS: list[dict] = [
    {"id": "settings", "key": "nav.settings"},
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

        # ── Logo area ──────────────────────────────────────────────────
        logo_area = QWidget()
        logo_area.setObjectName("sidebar_logo_area")
        logo_area.setFixedHeight(68)
        logo_layout = QVBoxLayout(logo_area)
        logo_layout.setContentsMargins(18, 14, 18, 14)
        logo_layout.setSpacing(2)

        self._app_name = QLabel("P4rsInSight")
        self._app_name.setObjectName("sidebar_app_name")

        self._tagline = QLabel(i18n.tr("app.tagline"))
        self._tagline.setObjectName("sidebar_tagline")
        self._tagline.setWordWrap(True)

        logo_layout.addWidget(self._app_name)
        logo_layout.addWidget(self._tagline)
        outer.addWidget(logo_area)

        # ── Thin divider ───────────────────────────────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,0.07); border: none;")
        outer.addWidget(div)

        # ── Scrollable nav area ────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        nav_widget = QWidget()
        self._nav_layout = QVBoxLayout(nav_widget)
        self._nav_layout.setContentsMargins(0, 6, 0, 6)
        self._nav_layout.setSpacing(0)
        self._nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Section label
        nav_lbl = QLabel("NAVIGATION")
        nav_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.18); font-size: 9px; "
            "font-weight: 700; letter-spacing: 1.0px; "
            "padding: 10px 18px 4px 18px;"
        )
        self._nav_layout.addWidget(nav_lbl)

        self._build_nav_items(NAV_ITEMS)

        scroll.setWidget(nav_widget)
        outer.addWidget(scroll, 1)

        # ── Bottom divider ─────────────────────────────────────────────
        div2 = QFrame()
        div2.setFrameShape(QFrame.Shape.HLine)
        div2.setFixedHeight(1)
        div2.setStyleSheet("background: rgba(255,255,255,0.07); border: none;")
        outer.addWidget(div2)

        # ── Pinned bottom section (Settings) ───────────────────────────
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 4, 0, 0)
        bottom_layout.setSpacing(0)

        self._build_nav_items(BOTTOM_ITEMS, layout=bottom_layout)

        # Version
        ver = QLabel("v 1.0.0")
        ver.setObjectName("sidebar_tagline")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver.setContentsMargins(0, 6, 0, 10)
        bottom_layout.addWidget(ver)

        outer.addWidget(bottom_widget)

    def _build_nav_items(
        self,
        items: list[dict],
        layout: QVBoxLayout | None = None,
    ) -> None:
        target = layout if layout is not None else self._nav_layout
        for item in items:
            label = i18n.tr(item["key"])
            btn = QPushButton(label)
            btn.setObjectName("sidebar_item")
            btn.setProperty("active", "false")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip(label)

            page_id = item["id"]
            btn.clicked.connect(
                lambda checked=False, pid=page_id: self._on_nav_click(pid)
            )

            self._buttons[page_id] = btn
            target.addWidget(btn)

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
        all_items = NAV_ITEMS + BOTTOM_ITEMS
        for item in all_items:
            if item["id"] in self._buttons:
                label = i18n.tr(item["key"])
                btn = self._buttons[item["id"]]
                btn.setText(label)
                btn.setToolTip(label)
