"""
P4rsInSight - Windows Alternatives Page
Search for Windows applications and get Linux equivalents with pros/cons and install.
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
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
from ui.components.card import Card
from ui.components.terminal_panel import TerminalPanel

log = get_logger("windows_alternatives")

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "windows_alternatives.json"


def _load_alternatives() -> list[dict]:
    try:
        with _DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f).get("alternatives", [])
    except Exception as exc:
        log.error("Failed to load alternatives: %s", exc)
        return []


class AlternativeCard(Card):
    """Card showing one Linux alternative for a Windows app."""

    def __init__(self, alt: dict, terminal: TerminalPanel | None, parent=None) -> None:
        super().__init__(parent)
        self._alt = alt
        self._terminal = terminal
        self._setup()

    def _setup(self) -> None:
        layout = self.layout()
        layout.setSpacing(10)

        # Name + similarity
        header = QHBoxLayout()
        lang = i18n.current_language
        name_lbl = QLabel(f"<b style='font-size:15px'>{self._alt['name']}</b>")
        header.addWidget(name_lbl)
        header.addStretch()

        sim = self._alt.get("similarity", 0)
        sim_color = "#2E7D32" if sim >= 80 else "#F57F17" if sim >= 60 else "#C62828"
        sim_lbl = QLabel(f"<span style='color:{sim_color};font-weight:700'>{sim}% {i18n.tr('windows_alternatives.similarity')}</span>")
        header.addWidget(sim_lbl)
        layout.addLayout(header)

        # Description
        desc_key = "description_en" if lang == "en" else "description_tr"
        desc = QLabel(self._alt.get(desc_key, ""))
        desc.setObjectName("card_description")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Pros & Cons
        pros = self._alt.get("pros", [])
        cons = self._alt.get("cons", [])
        if pros or cons:
            pc_row = QHBoxLayout()
            pc_row.setSpacing(16)
            if pros:
                pros_col = QVBoxLayout()
                pros_label = QLabel(f"✅ {i18n.tr('windows_alternatives.pros')}")
                pros_label.setStyleSheet("font-weight: 600; color: #2E7D32;")
                pros_col.addWidget(pros_label)
                for p in pros:
                    l = QLabel(f"  • {p}")
                    l.setStyleSheet("color: #37474F; font-size: 11px;")
                    pros_col.addWidget(l)
                pc_row.addLayout(pros_col)
            if cons:
                cons_col = QVBoxLayout()
                cons_label = QLabel(f"❌ {i18n.tr('windows_alternatives.cons')}")
                cons_label.setStyleSheet("font-weight: 600; color: #C62828;")
                cons_col.addWidget(cons_label)
                for c in cons:
                    l = QLabel(f"  • {c}")
                    l.setStyleSheet("color: #37474F; font-size: 11px;")
                    cons_col.addWidget(l)
                pc_row.addLayout(cons_col)
            pc_row.addStretch()
            layout.addLayout(pc_row)

        # Install button
        method = self._alt.get("install_method", "apt")
        if method != "manual":
            install_btn = QPushButton(f"↓  {i18n.tr('windows_alternatives.install_this')}")
            install_btn.clicked.connect(self._on_install)
            layout.addWidget(install_btn, 0, Qt.AlignmentFlag.AlignLeft)

    def _on_install(self) -> None:
        method = self._alt.get("install_method", "apt")
        name = self._alt.get("name", "")
        if method == "flatpak":
            cmd = ["flatpak", "install", "-y", "flathub", self._alt.get("flatpak_id", "")]
        else:
            pkg = self._alt.get("apt_package", "")
            cmd = ["sudo", "apt", "install", "-y", pkg]

        if self._terminal:
            exp = package_manager.build_command_explanation(cmd)
            self._terminal.show_command(
                cmd_str=" ".join(cmd),
                description=f"Installing {name}",
                args_info=exp.get("args", []),
            )

        msg = QMessageBox()
        msg.setWindowTitle(i18n.tr("common.confirm"))
        msg.setText(f"{i18n.tr('software_center.confirm_install_msg', name=name)}")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            worker = CommandWorker(cmd)
            if self._terminal:
                worker.output_line.connect(self._terminal.append_output)
            worker.start()
            self._worker = worker


class WindowsAlternativesPage(QWidget):
    """Windows alternatives finder page."""

    def __init__(self, terminal_panel: TerminalPanel | None = None, parent=None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._data = _load_alternatives()
        self._search_text = ""
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Search bar
        search_bar = QWidget()
        search_bar.setStyleSheet("background: #FFFFFF; border-bottom: 1px solid #E0E4EE;")
        sb_layout = QHBoxLayout(search_bar)
        sb_layout.setContentsMargins(20, 12, 20, 12)

        self._search = QLineEdit()
        self._search.setObjectName("search_bar")
        self._search.setPlaceholderText(i18n.tr("windows_alternatives.search_placeholder"))
        self._search.textChanged.connect(self._on_search)
        sb_layout.addWidget(self._search)
        outer.addWidget(search_bar)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        self._content = QWidget()
        self._content.setObjectName("page_content")
        self._layout = QVBoxLayout(self._content)
        self._layout.setContentsMargins(24, 24, 24, 24)
        self._layout.setSpacing(14)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self._content)
        outer.addWidget(scroll, 1)

        self._render()

    def _render(self) -> None:
        # Clear
        for i in reversed(range(self._layout.count())):
            w = self._layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        q = self._search_text.lower()
        results = [
            item for item in self._data
            if not q or q in item.get("windows_app", "").lower()
        ]

        if not results:
            no = QLabel(f"🔍  {i18n.tr('windows_alternatives.no_results')}")
            no.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no.setStyleSheet("color: #78909C; font-size: 16px; padding: 60px;")
            self._layout.addWidget(no)
            return

        for item in results:
            lang = i18n.current_language
            desc_key = "description_en" if lang == "en" else "description_tr"

            # Windows app header
            win_header = QLabel(
                f"🪟  <b style='font-size:17px'>{item['windows_app']}</b>"
                f"  <span style='color:#78909C;font-size:12px'>— {item.get(desc_key, '')}</span>"
            )
            win_header.setWordWrap(True)
            self._layout.addWidget(win_header)

            for alt in item.get("alternatives", []):
                card = AlternativeCard(alt, self._terminal)
                card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                self._layout.addWidget(card)

            # Separator
            sep = QWidget()
            sep.setFixedHeight(1)
            sep.setStyleSheet("background: #E0E4EE;")
            self._layout.addWidget(sep)

    def _on_search(self, text: str) -> None:
        self._search_text = text
        self._render()

    def _retranslate(self) -> None:
        self._search.setPlaceholderText(i18n.tr("windows_alternatives.search_placeholder"))
        self._render()
