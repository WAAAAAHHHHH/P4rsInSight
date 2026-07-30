"""
P4rsInSight - Software Center Page
Categorized app catalog with install/remove buttons, search, and multi-install queue.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger
from core.package_manager import CommandWorker, package_manager
from core.settings_manager import settings
import shutil
from ui.components.card import Card
from ui.components.install_button import InstallButton
from ui.components.terminal_panel import TerminalPanel

log = get_logger("software_center")

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "apps_catalog.json"

CATEGORY_ICONS = {
    "internet": "🌐", "office": "📄", "multimedia": "🎬",
    "graphics": "🎨", "gaming": "🎮", "development": "💻",
    "communication": "💬", "utilities": "🔧", "education": "📚",
}


def _load_catalog() -> tuple[list[dict], list[dict]]:
    try:
        with _DATA_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("apps", []), data.get("categories", [])
    except Exception as exc:
        log.error("Failed to load apps catalog: %s", exc)
        return [], []


class AppCard(Card):
    """Card widget for a single application."""

    def __init__(
        self,
        app: dict,
        installed: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.app = app
        self._setup(installed)

    def _setup(self, installed: bool) -> None:
        layout = self.layout()
        layout.setSpacing(8)

        # Header row
        header = QHBoxLayout()
        icon_label = QLabel(CATEGORY_ICONS.get(self.app.get("category", ""), "📁"))
        icon_label.setStyleSheet("font-size: 26px; background: transparent;")
        icon_label.setFixedWidth(36)
        header.addWidget(icon_label)

        name_col = QVBoxLayout()
        name_col.setSpacing(2)
        self.name_label = QLabel(f"<b>{self.app['name']}</b>")
        self.name_label.setObjectName("card_title")
        method = self.app.get("install_method", "apt").upper()
        method_label = QLabel(f"via {method}")
        method_label.setStyleSheet("color: #50506A; font-size: 10px;")
        name_col.addWidget(self.name_label)
        name_col.addWidget(method_label)
        header.addLayout(name_col, 1)

        layout.addLayout(header)

        # Description
        desc_key = "description_en" if i18n.current_language == "en" else "description"
        desc_text = self.app.get(desc_key, self.app.get("description", ""))
        self.desc_label = QLabel(desc_text[:120] + ("..." if len(desc_text) > 120 else ""))
        self.desc_label.setObjectName("card_description")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        # Install button
        self.install_btn = InstallButton(self.app["id"], installed=installed)
        layout.addWidget(self.install_btn, 0, Qt.AlignmentFlag.AlignRight)


class SoftwareCenterPage(QWidget):
    """Software center with category filtering, search, and install queue."""

    def __init__(self, terminal_panel: TerminalPanel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._apps, self._categories = _load_catalog()
        self._current_category = "all"
        self._search_text = ""
        self._app_cards: dict[str, AppCard] = {}
        self._worker: Optional[CommandWorker] = None
        self._active_workers: list[CommandWorker] = []
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # --- Filter bar ---
        filter_bar = QWidget()
        filter_bar.setStyleSheet("background: transparent; border-bottom: 1px solid #282828; padding: 0;")
        filter_layout = QHBoxLayout(filter_bar)
        filter_layout.setContentsMargins(20, 12, 20, 12)
        filter_layout.setSpacing(12)

        # Search
        self._search_input = QLineEdit()
        self._search_input.setObjectName("search_bar")
        self._search_input.setPlaceholderText(i18n.tr("software_center.search_placeholder"))
        self._search_input.textChanged.connect(self._on_search)
        filter_layout.addWidget(self._search_input, 1)

        # Category dropdown
        self._cat_combo = QComboBox()
        self._cat_combo.addItem(i18n.tr("software_center.all_categories"), "all")
        for cat in self._categories:
            icon = CATEGORY_ICONS.get(cat["id"], "")
            name = cat.get("name_en" if i18n.current_language == "en" else "name", cat["id"])
            self._cat_combo.addItem(f"{icon}  {name}", cat["id"])
        self._cat_combo.currentIndexChanged.connect(self._on_category_change)
        filter_layout.addWidget(self._cat_combo)

        outer.addWidget(filter_bar)

        # --- Scroll area for app cards ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        self._grid_container = QWidget()
        self._grid_container.setObjectName("page_content")
        self._grid = QGridLayout(self._grid_container)
        self._grid.setContentsMargins(20, 20, 20, 20)
        self._grid.setSpacing(14)
        self._grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self._grid_container)
        outer.addWidget(scroll, 1)

        # Initial render
        self._render_apps()

    def _render_apps(self) -> None:
        """Clear and re-render the app grid based on current filter."""
        # Clear grid
        for i in reversed(range(self._grid.count())):
            w = self._grid.itemAt(i).widget()
            if w:
                w.deleteLater()
        self._app_cards.clear()

        filtered = [
            app for app in self._apps
            if self._matches_filter(app)
        ]

        if not filtered:
            no_results = QLabel(f"🔍  {i18n.tr('software_center.no_results')}")
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_results.setStyleSheet("color: #50506A; font-size: 15px; padding: 40px;")
            self._grid.addWidget(no_results, 0, 0, 1, 3)
            return

        installed_list = settings.get("installed_apps", [])
        cols = 3
        for idx, app in enumerate(filtered):
            is_installed = app["id"] in installed_list
            card = AppCard(app, installed=is_installed)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            card.install_btn.install_requested.connect(self._on_install)
            card.install_btn.remove_requested.connect(self._on_remove)
            self._app_cards[app["id"]] = card
            row, col = divmod(idx, cols)
            self._grid.addWidget(card, row, col)

    def _matches_filter(self, app: dict) -> bool:
        if self._current_category != "all" and app.get("category") != self._current_category:
            return False
        if self._search_text:
            q = self._search_text.lower()
            if q not in app.get("name", "").lower() and q not in app.get("description", "").lower():
                return False
        return True

    def _on_search(self, text: str) -> None:
        self._search_text = text
        self._render_apps()

    def _on_category_change(self, index: int) -> None:
        self._current_category = self._cat_combo.itemData(index)
        self._render_apps()

    def _on_install(self, app_id: str) -> None:
        app = next((a for a in self._apps if a["id"] == app_id), None)
        if not app:
            return

        # Build command
        method = app.get("install_method", "apt")
        if method == "flatpak":
            flatpak_id = app.get("flatpak_id", "")
            if not shutil.which("flatpak"):
                # Auto install flatpak and flathub repository, then install application
                cmd = [
                    "sudo", "bash", "-c",
                    f"apt-get update && apt-get install -y flatpak && "
                    f"flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo && "
                    f"flatpak install -y flathub {flatpak_id}"
                ]
            else:
                cmd = ["flatpak", "install", "-y", "flathub", flatpak_id]
        else:
            pkgs = app.get("apt_package", app["id"]).split()
            cmd = ["sudo", "apt", "install", "-y"] + pkgs

        # Show in terminal panel
        if self._terminal:
            exp = package_manager.build_command_explanation(cmd)
            self._terminal.show_command(
                cmd_str=" ".join(cmd),
                description=f"Installing {app['name']}",
                args_info=exp.get("args", []),
            )

        # Confirm
        msg = QMessageBox(self)
        msg.setWindowTitle(i18n.tr("software_center.confirm_install"))
        msg.setText(i18n.tr("software_center.confirm_install_msg", name=app["name"]))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            card = self._app_cards.get(app_id)
            if card:
                card.install_btn.set_busy(True)

            worker = CommandWorker(cmd)
            if self._terminal:
                worker.output_line.connect(self._terminal.append_output)
            worker.finished.connect(
                lambda ok, m, aid=app_id: self._on_install_done(aid, ok)
            )
            worker.start()
            self._active_workers.append(worker)

    def _on_remove(self, app_id: str) -> None:
        app = next((a for a in self._apps if a["id"] == app_id), None)
        if not app:
            return

        method = app.get("install_method", "apt")
        if method == "flatpak":
            cmd = ["flatpak", "uninstall", "-y", app.get("flatpak_id", "")]
        else:
            pkgs = app.get("apt_package", app["id"]).split()
            cmd = ["sudo", "apt", "remove", "-y"] + pkgs

        msg = QMessageBox(self)
        msg.setWindowTitle(i18n.tr("software_center.confirm_remove"))
        msg.setText(i18n.tr("software_center.confirm_remove_msg", name=app["name"]))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            card = self._app_cards.get(app_id)
            if card:
                card.install_btn.set_busy(True)

            worker = CommandWorker(cmd)
            if self._terminal:
                worker.output_line.connect(self._terminal.append_output)
            worker.finished.connect(
                lambda ok, m, aid=app_id: self._on_remove_done(aid, ok)
            )
            worker.start()
            self._active_workers.append(worker)

    def _on_install_done(self, app_id: str, success: bool) -> None:
        card = self._app_cards.get(app_id)
        if card:
            card.install_btn.set_installed(success)
        if success:
            installed_list = list(settings.get("installed_apps", []))
            if app_id not in installed_list:
                installed_list.append(app_id)
                settings.set("installed_apps", installed_list)

    def _on_remove_done(self, app_id: str, success: bool) -> None:
        card = self._app_cards.get(app_id)
        if card:
            card.install_btn.set_installed(not success)
        if success:
            installed_list = list(settings.get("installed_apps", []))
            if app_id in installed_list:
                installed_list.remove(app_id)
                settings.set("installed_apps", installed_list)

    def _retranslate(self) -> None:
        self._search_input.setPlaceholderText(i18n.tr("software_center.search_placeholder"))
        self._render_apps()
