"""
P4rsInSight - Status Badge Widget
A pill-shaped label showing ok / warning / error status using text only.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from core.i18n_manager import i18n

# Maps status → (object_name, text_i18n_key)
_STATUS_MAP = {
    "ok":      ("badge_ok",      "dashboard.status_ok"),
    "warning": ("badge_warning", "dashboard.status_warning"),
    "error":   ("badge_error",   "dashboard.status_error"),
}


class StatusBadge(QLabel):
    """
    Small pill badge.  Status is one of: 'ok', 'warning', 'error'.
    """

    def __init__(self, status: str = "ok", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status = status
        self.set_status(status)
        i18n.language_changed.connect(lambda _: self.set_status(self._status))

    def set_status(self, status: str) -> None:
        self._status = status
        obj_name, text_key = _STATUS_MAP.get(status, _STATUS_MAP["ok"])
        self.setObjectName(obj_name)
        self.setText(i18n.tr(text_key))
        # Force restyle
        self.style().unpolish(self)
        self.style().polish(self)
