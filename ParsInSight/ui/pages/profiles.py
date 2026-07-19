"""
P4rsInSight - Installation Profiles Page
One-click profile cards for Student, Gamer, Developer, etc.
"""

from __future__ import annotations

import json
from pathlib import Path

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

log = get_logger("profiles")

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "profiles.json"
_APPS_PATH = Path(__file__).parent.parent.parent / "data" / "apps_catalog.json"


def _load_data() -> tuple[list[dict], list[dict]]:
    profiles, apps = [], []
    try:
        with _DATA_PATH.open("r", encoding="utf-8") as f:
            profiles = json.load(f).get("profiles", [])
        with _APPS_PATH.open("r", encoding="utf-8") as f:
            apps = json.load(f).get("apps", [])
    except Exception as exc:
        log.error("Failed to load profile data: %s", exc)
    return profiles, apps


class ProfileCard(QWidget):
    """Profile selection card."""

    def __init__(
        self,
        profile: dict,
        all_apps: list[dict],
        terminal: TerminalPanel | None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._profile = profile
        self._all_apps = all_apps
        self._terminal = terminal
        self._workers: list[CommandWorker] = []
        self._setup()

    def _setup(self) -> None:
        self.setObjectName("card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        lang = i18n.current_language
        name = self._profile.get(f"name_{lang}", self._profile.get("name_en", ""))
        icon = self._profile.get("icon", "")
        color = self._profile.get("color", "#1565C0")
        desc = self._profile.get(f"description_{lang}", self._profile.get("description_en", ""))
        pkg_ids = self._profile.get("packages", [])

        # Icon + name row
        header = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 32px; background: transparent;")
        icon_lbl.setFixedWidth(44)
        header.addWidget(icon_lbl)

        name_lbl = QLabel(f"<b style='font-size:16px; color:{color}'>{name}</b>")
        header.addWidget(name_lbl, 1)
        layout.addLayout(header)

        # Description
        desc_lbl = QLabel(desc)
        desc_lbl.setObjectName("card_description")
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl)

        # App list
        self._pkg_count_label = QLabel(
            f"{i18n.tr('profiles.apps_included', count=len(pkg_ids))}"
        )
        self._pkg_count_label.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 12px;")
        layout.addWidget(self._pkg_count_label)

        # App names preview
        preview_names = []
        for pid in pkg_ids[:5]:
            app = next((a for a in self._all_apps if a["id"] == pid), None)
            if app:
                preview_names.append(app["name"])
        if preview_names:
            preview = QLabel("  " + ",  ".join(preview_names) + ("..." if len(pkg_ids) > 5 else ""))
            preview.setStyleSheet("color: #90A4AE; font-size: 11px;")
            preview.setWordWrap(True)
            layout.addWidget(preview)

        # Install button
        self._install_btn = QPushButton(f"⚡  {i18n.tr('profiles.install_profile')}")
        self._install_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                opacity: 0.85;
            }}
        """)
        self._install_btn.clicked.connect(self._on_install)
        layout.addWidget(self._install_btn)

    def _on_install(self) -> None:
        lang = i18n.current_language
        name = self._profile.get(f"name_{lang}", self._profile.get("name_en", ""))
        pkg_ids = self._profile.get("packages", [])

        # Gather package names
        pkgs_to_install = []
        for pid in pkg_ids:
            app = next((a for a in self._all_apps if a["id"] == pid), None)
            if app:
                method = app.get("install_method", "apt")
                if method == "apt":
                    pkgs_to_install.extend(app.get("apt_package", pid).split())

        if not pkgs_to_install:
            return

        cmd = ["sudo", "apt", "install", "-y"] + pkgs_to_install
        app_names = [next((a["name"] for a in self._all_apps if a["id"] == pid), pid) for pid in pkg_ids]

        msg = QMessageBox()
        msg.setWindowTitle(i18n.tr("profiles.confirm_title"))
        msg.setText(
            i18n.tr("profiles.confirm_msg",
                    profile=name,
                    apps="\n  • " + "\n  • ".join(app_names))
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            if self._terminal:
                exp = package_manager.build_command_explanation(cmd)
                self._terminal.show_command(
                    cmd_str=" ".join(cmd),
                    description=f"Installing {name} profile",
                    args_info=exp.get("args", []),
                )

            self._install_btn.setEnabled(False)
            self._install_btn.setText(i18n.tr("profiles.installing_profile"))

            worker = CommandWorker(cmd)
            if self._terminal:
                worker.output_line.connect(self._terminal.append_output)
            worker.finished.connect(self._on_done)
            worker.start()
            self._workers.append(worker)

    def _on_done(self, success: bool, message: str) -> None:
        self._install_btn.setEnabled(True)
        self._install_btn.setText(
            "✅  " + i18n.tr("common.success") if success else "❌  " + i18n.tr("common.error")
        )


class ProfilesPage(QWidget):
    """One-click installation profiles page."""

    def __init__(self, terminal_panel: TerminalPanel | None = None, parent=None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._profiles, self._apps = _load_data()
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
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(24, 24, 24, 24)
        self._content_layout.setSpacing(16)

        self._grid = QGridLayout()
        self._grid.setSpacing(14)
        self._content_layout.addLayout(self._grid)
        self._content_layout.addStretch()

        self._build_grid()

        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

    def _build_grid(self) -> None:
        for i in reversed(range(self._grid.count())):
            w = self._grid.itemAt(i).widget()
            if w:
                w.deleteLater()

        cols = 2
        for idx, profile in enumerate(self._profiles):
            card = ProfileCard(profile, self._apps, self._terminal)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            row, col = divmod(idx, cols)
            self._grid.addWidget(card, row, col)

    def _retranslate(self) -> None:
        self._build_grid()
