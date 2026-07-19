"""
P4rsInSight - Reusable Card Widget
A styled container with rounded corners, subtle shadow, and hover effect.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget


class Card(QFrame):
    """
    A styled card container.

    Usage
    -----
    card = Card()
    card.layout().addWidget(some_widget)
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(18, 16, 18, 16)
        self._layout.setSpacing(8)

    def layout(self) -> QVBoxLayout:  # type: ignore[override]
        return self._layout


class StatusCard(Card):
    """
    Card variant that includes a title, description, status badge, and action button.
    Pre-structured for dashboard health cards.
    """

    def __init__(
        self,
        icon: str = "",
        title: str = "",
        description: str = "",
        status: str = "ok",   # "ok" | "warning" | "error"
        parent: QWidget | None = None,
    ) -> None:
        from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton

        super().__init__(parent)

        from ui.components.status_badge import StatusBadge

        # Top row: icon + title + badge
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 22px; background: transparent;")
        icon_label.setFixedWidth(30)
        top_row.addWidget(icon_label)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("card_title")
        top_row.addWidget(self.title_label, 1)

        self.badge = StatusBadge(status)
        top_row.addWidget(self.badge, 0, Qt.AlignmentFlag.AlignRight)

        self.layout().addLayout(top_row)

        # Description
        self.desc_label = QLabel(description)
        self.desc_label.setObjectName("card_description")
        self.desc_label.setWordWrap(True)
        self.layout().addWidget(self.desc_label)

        # Action button (hidden by default)
        self.action_btn = QPushButton("")
        self.action_btn.setObjectName("btn_secondary")
        self.action_btn.setVisible(False)
        self.layout().addWidget(self.action_btn, 0, Qt.AlignmentFlag.AlignRight)

    def set_action(self, label: str, callback) -> None:
        """Show and configure the action button."""
        self.action_btn.setText(label)
        self.action_btn.clicked.connect(callback)
        self.action_btn.setVisible(True)

    def update_status(self, status: str, description: str = "") -> None:
        self.badge.set_status(status)
        if description:
            self.desc_label.setText(description)
