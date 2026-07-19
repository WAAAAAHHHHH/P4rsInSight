"""
P4rsInSight - System Maintenance Page
Grid of maintenance tool cards, each requiring confirmation before executing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger
from core.package_manager import CommandWorker, package_manager
from ui.components.terminal_panel import TerminalPanel

log = get_logger("maintenance")


@dataclass
class MaintenanceAction:
    id: str
    icon: str
    title_key: str
    desc_key: str
    cmd: list[str]


_ACTIONS: list[MaintenanceAction] = [
    MaintenanceAction("update_list",     "🔃", "maintenance.update_list",     "maintenance.update_list_desc",   ["sudo", "apt", "update"]),
    MaintenanceAction("upgrade",         "⬆️",  "maintenance.upgrade",          "maintenance.upgrade_desc",        ["sudo", "apt", "upgrade", "-y"]),
    MaintenanceAction("autoremove",      "🧹", "maintenance.autoremove",       "maintenance.autoremove_desc",     ["sudo", "apt", "autoremove", "-y"]),
    MaintenanceAction("clean_cache",     "💾", "maintenance.clean_cache",      "maintenance.clean_cache_desc",    ["sudo", "apt", "clean"]),
    MaintenanceAction("install_codecs",  "🎬", "maintenance.install_codecs",   "maintenance.install_codecs_desc", ["sudo", "apt", "install", "-y", "ubuntu-restricted-extras"]),
    MaintenanceAction("enable_flatpak",  "📦", "maintenance.enable_flatpak",   "maintenance.enable_flatpak_desc", ["sudo", "apt", "install", "-y", "flatpak"]),
    MaintenanceAction("check_drivers",   "🔌", "maintenance.check_drivers",    "maintenance.check_drivers_desc",  ["ubuntu-drivers", "devices"]),
    MaintenanceAction("disk_usage",      "💿", "maintenance.disk_usage",       "maintenance.disk_usage_desc",     ["df", "-h"]),
]


class MaintenanceCard(QWidget):
    """Card for a single maintenance action."""

    def __init__(
        self,
        action: MaintenanceAction,
        terminal: TerminalPanel | None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._action = action
        self._terminal = terminal
        self._worker: CommandWorker | None = None
        self.setObjectName("card")
        self._setup()

    def _setup(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        # Icon + title
        header = QHBoxLayout()
        icon = QLabel(self._action.icon)
        icon.setStyleSheet("font-size: 26px; background: transparent;")
        icon.setFixedWidth(36)
        header.addWidget(icon)

        self._title = QLabel(f"<b>{i18n.tr(self._action.title_key)}</b>")
        self._title.setObjectName("card_title")
        header.addWidget(self._title, 1)
        layout.addLayout(header)

        # Description
        self._desc = QLabel(i18n.tr(self._action.desc_key))
        self._desc.setObjectName("card_description")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        # Command preview
        cmd_preview = QLabel(f"<code style='color:#78909C; font-size:10px'>{' '.join(self._action.cmd)}</code>")
        layout.addWidget(cmd_preview)

        # Run button
        self._btn = QPushButton(f"▶  {i18n.tr('maintenance.run')}")
        self._btn.clicked.connect(self._on_run)
        layout.addWidget(self._btn, 0, Qt.AlignmentFlag.AlignRight)

    def _on_run(self) -> None:
        cmd = self._action.cmd

        if self._terminal:
            exp = package_manager.build_command_explanation(cmd)
            self._terminal.show_command(
                cmd_str=" ".join(cmd),
                description=i18n.tr(self._action.title_key),
                args_info=exp.get("args", []),
            )

        msg = QMessageBox()
        msg.setWindowTitle(i18n.tr("maintenance.run"))
        msg.setText(
            f"{i18n.tr('maintenance.confirm_run')}\n\n"
            f"<b>{i18n.tr(self._action.title_key)}</b>\n"
            f"<code>{' '.join(cmd)}</code>"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self._btn.setEnabled(False)
            self._btn.setText(f"⏳  {i18n.tr('maintenance.running')}")

            self._worker = CommandWorker(cmd)
            if self._terminal:
                self._worker.output_line.connect(self._terminal.append_output)
            self._worker.finished.connect(self._on_done)
            self._worker.start()

    def _on_done(self, success: bool, message: str) -> None:
        self._btn.setEnabled(True)
        if success:
            self._btn.setText(f"✅  {i18n.tr('maintenance.operation_complete')}")
        else:
            self._btn.setText(f"❌  {i18n.tr('common.error')}")

    def retranslate(self) -> None:
        self._title.setText(f"<b>{i18n.tr(self._action.title_key)}</b>")
        self._desc.setText(i18n.tr(self._action.desc_key))
        self._btn.setText(f"▶  {i18n.tr('maintenance.run')}")


class MaintenancePage(QWidget):
    """System maintenance tools page."""

    def __init__(self, terminal_panel: TerminalPanel | None = None, parent=None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._action_cards: list[MaintenanceCard] = []
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("page_content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        self._grid = QGridLayout()
        self._grid.setSpacing(14)
        content_layout.addLayout(self._grid)
        content_layout.addStretch()

        cols = 2
        for idx, action in enumerate(_ACTIONS):
            card = MaintenanceCard(action, self._terminal)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self._action_cards.append(card)
            row, col = divmod(idx, cols)
            self._grid.addWidget(card, row, col)

        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

    def _retranslate(self) -> None:
        for card in self._action_cards:
            card.retranslate()
