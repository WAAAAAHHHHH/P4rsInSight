"""
P4rsInSight - Install/Remove Button Widget
Context-aware button that shows Install or Remove based on installation state.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QWidget

from core.i18n_manager import i18n


class InstallButton(QPushButton):
    """
    Smart install/remove toggle button.

    Signals
    -------
    install_requested(app_id)
    remove_requested(app_id)
    """

    install_requested = Signal(str)
    remove_requested = Signal(str)

    def __init__(
        self,
        app_id: str,
        installed: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.app_id = app_id
        self._installed = installed
        self._busy = False
        self._update_state()
        self.clicked.connect(self._on_click)
        i18n.language_changed.connect(self._on_lang_changed)

    def _on_lang_changed(self) -> None:
        self._update_state()

    @property
    def is_installed(self) -> bool:
        return self._installed

    def set_installed(self, value: bool) -> None:
        self._installed = value
        self._busy = False
        self._update_state()

    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        self._update_state()
        self.setEnabled(not busy)

    def _update_state(self) -> None:
        if self._busy:
            if self._installed:
                self.setText(i18n.tr("software_center.removing"))
                self.setObjectName("btn_secondary")
            else:
                self.setText(i18n.tr("software_center.installing"))
                self.setObjectName("btn_secondary")
        elif self._installed:
            self.setText(f"✕  {i18n.tr('software_center.remove')}")
            self.setObjectName("btn_danger")
        else:
            self.setText(f"↓  {i18n.tr('software_center.install')}")
            self.setObjectName("")
        self.style().unpolish(self)
        self.style().polish(self)

    def _on_click(self) -> None:
        if self._installed:
            self.remove_requested.emit(self.app_id)
        else:
            self.install_requested.emit(self.app_id)
