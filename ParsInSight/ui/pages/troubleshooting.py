"""
P4rsInSight - Troubleshooting Page
Problem list sidebar + step-by-step solution detail panel.
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger
from core.package_manager import CommandWorker
from ui.components.terminal_panel import TerminalPanel

log = get_logger("troubleshooting")

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "troubleshooting.json"


def _load_problems() -> list[dict]:
    try:
        with _DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f).get("problems", [])
    except Exception as exc:
        log.error("Failed to load troubleshooting data: %s", exc)
        return []


class TroubleshootingPage(QWidget):
    """Troubleshooting guides with step-by-step solutions."""

    def __init__(self, terminal_panel: TerminalPanel | None = None, parent=None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._problems = _load_problems()
        self._workers: list[CommandWorker] = []
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # --- Left: problem list ---
        left = QWidget()
        left.setStyleSheet("background: #FFFFFF; border-right: 1px solid #E0E4EE;")
        left.setMinimumWidth(200)
        left.setMaximumWidth(260)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        lbl = QLabel(f"🆘  {i18n.tr('troubleshooting.title')}")
        lbl.setObjectName("section_title")
        left_layout.addWidget(lbl)

        self._list = QListWidget()
        self._list.setFrameShape(self._list.Shape.NoFrame)
        self._list.currentRowChanged.connect(self._show_problem)
        left_layout.addWidget(self._list, 1)
        splitter.addWidget(left)

        # --- Right: detail ---
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(right_scroll.Shape.NoFrame)

        self._detail = QWidget()
        self._detail.setObjectName("page_content")
        self._detail_layout = QVBoxLayout(self._detail)
        self._detail_layout.setContentsMargins(24, 24, 24, 24)
        self._detail_layout.setSpacing(14)
        self._detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        right_scroll.setWidget(self._detail)
        splitter.addWidget(right_scroll)
        splitter.setSizes([220, 600])

        outer.addWidget(splitter, 1)

        self._populate_list()

    def _populate_list(self) -> None:
        self._list.clear()
        lang = i18n.current_language
        for prob in self._problems:
            title_key = f"title_{lang}" if lang in ("tr", "en") else "title_en"
            title = prob.get(title_key, prob.get("title_en", ""))
            icon = prob.get("icon", "❓")
            item = QListWidgetItem(f"{icon}  {title}")
            item.setData(Qt.ItemDataRole.UserRole, prob["id"])
            self._list.addItem(item)
        if self._list.count() > 0:
            self._list.setCurrentRow(0)

    def _show_problem(self, row: int) -> None:
        if row < 0 or row >= len(self._problems):
            return
        prob = self._problems[row]
        lang = i18n.current_language
        sfx = "_tr" if lang == "tr" else "_en"

        # Clear detail
        for i in reversed(range(self._detail_layout.count())):
            w = self._detail_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        # Title
        title = prob.get(f"title{sfx}", "")
        icon = prob.get("icon", "")
        title_lbl = QLabel(f"{icon}  <b style='font-size:18px'>{title}</b>")
        title_lbl.setWordWrap(True)
        self._detail_layout.addWidget(title_lbl)

        # Description
        desc = prob.get(f"description{sfx}", "")
        desc_lbl = QLabel(desc)
        desc_lbl.setObjectName("card_description")
        desc_lbl.setWordWrap(True)
        self._detail_layout.addWidget(desc_lbl)

        # Causes
        causes = prob.get(f"causes{sfx}", [])
        if causes:
            causes_lbl = QLabel(f"<b>⚠️  {i18n.tr('troubleshooting.causes')}</b>")
            self._detail_layout.addWidget(causes_lbl)
            for c in causes:
                cl = QLabel(f"  • {c}")
                cl.setStyleSheet("color: #78909C;")
                self._detail_layout.addWidget(cl)

        # Steps
        steps = prob.get("steps", [])
        if steps:
            steps_lbl = QLabel(f"<b>🔧  {i18n.tr('troubleshooting.solution_steps')}</b>")
            self._detail_layout.addWidget(steps_lbl)

            for step in steps:
                step_num = step.get("step", 1)
                step_desc = step.get(f"description{sfx}", "")
                cmd = step.get("command", "")
                safe = step.get("safe", True)

                step_widget = QWidget()
                step_widget.setObjectName("card")
                step_layout = QVBoxLayout(step_widget)
                step_layout.setContentsMargins(14, 12, 14, 12)
                step_layout.setSpacing(8)

                step_header = QHBoxLayout()
                step_num_lbl = QLabel(str(step_num))
                step_num_lbl.setStyleSheet(
                    "background:#1565C0;color:white;border-radius:12px;"
                    "font-weight:700;font-size:11px;padding:2px 8px;"
                )
                step_num_lbl.setFixedHeight(22)
                step_header.addWidget(step_num_lbl)
                step_header.addSpacing(8)
                step_desc_lbl = QLabel(step_desc)
                step_desc_lbl.setWordWrap(True)
                step_header.addWidget(step_desc_lbl, 1)
                step_layout.addLayout(step_header)

                if cmd:
                    cmd_row = QHBoxLayout()
                    cmd_lbl = QLabel(f"<code style='background:#F5F7FA;padding:4px 8px;border-radius:6px;font-family:monospace'>{cmd}</code>")
                    cmd_lbl.setWordWrap(True)
                    cmd_row.addWidget(cmd_lbl, 1)

                    copy_btn = QPushButton(i18n.tr("troubleshooting.copy_command"))
                    copy_btn.setObjectName("btn_secondary")
                    copy_btn.setFixedHeight(28)
                    copy_btn.clicked.connect(lambda checked=False, c=cmd: self._copy_cmd(c, copy_btn))
                    cmd_row.addWidget(copy_btn)

                    if safe:
                        run_btn = QPushButton(f"▶  {i18n.tr('troubleshooting.run_command')}")
                        run_btn.setFixedHeight(28)
                        run_btn.clicked.connect(lambda checked=False, c=cmd: self._run_cmd(c))
                        cmd_row.addWidget(run_btn)
                    else:
                        warn_lbl = QLabel(f"⚠️ {i18n.tr('troubleshooting.caution_command')}")
                        warn_lbl.setStyleSheet("color: #F57F17; font-size: 11px;")
                        step_layout.addWidget(warn_lbl)

                    step_layout.addLayout(cmd_row)

                self._detail_layout.addWidget(step_widget)

        self._detail_layout.addStretch()

    def _copy_cmd(self, cmd: str, btn: QPushButton) -> None:
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(cmd)
        btn.setText(i18n.tr("common.copy") + " ✓")
        QTimer.singleShot(2000, lambda: btn.setText(i18n.tr("troubleshooting.copy_command")))

    def _run_cmd(self, cmd_str: str) -> None:
        cmd = cmd_str.split()
        if self._terminal:
            self._terminal.show_command(cmd_str=cmd_str, description=cmd_str)

        msg = QMessageBox(self)
        msg.setWindowTitle(i18n.tr("common.confirm"))
        msg.setText(f"{i18n.tr('maintenance.confirm_run')}\n\n<code>{cmd_str}</code>")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            worker = CommandWorker(cmd)
            if self._terminal:
                worker.output_line.connect(self._terminal.append_output)
            worker.start()
            self._workers.append(worker)

    def _retranslate(self) -> None:
        self._populate_list()
