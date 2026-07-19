"""
P4rsInSight - Terminal Learning Panel
Slide-in panel that shows the command being executed, with explanation,
argument breakdown, and live output streaming.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger

log = get_logger("terminal_panel")


class TerminalPanel(QWidget):
    """
    Slide-up terminal learning panel.

    Shows:
    - The command being executed
    - A description of the command
    - Per-argument explanations
    - Live command output
    - Copy button

    Usage
    -----
    panel.show_command(
        cmd_str="sudo apt install firefox",
        explanation={"command": "...", "args": [...]},
        description="Installing Firefox"
    )
    panel.append_output("Reading package lists...")
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("terminal_panel")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 14)
        outer.setSpacing(12)

        # --- Header row ---
        header = QHBoxLayout()

        self._title_label = QLabel(i18n.tr("terminal_panel.title"))
        self._title_label.setObjectName("terminal_label")
        self._title_label.setStyleSheet(
            "font-size: 13px; font-weight: 700; color: #58A6FF;"
        )
        header.addWidget(self._title_label)
        header.addStretch()

        self._copy_btn = QPushButton(i18n.tr("terminal_panel.copy"))
        self._copy_btn.setObjectName("btn_secondary")
        self._copy_btn.setFixedHeight(28)
        self._copy_btn.clicked.connect(self._copy_command)
        header.addWidget(self._copy_btn)

        self._close_btn = QPushButton("✕")
        self._close_btn.setObjectName("btn_secondary")
        self._close_btn.setFixedSize(28, 28)
        self._close_btn.clicked.connect(self.hide)
        header.addWidget(self._close_btn)

        outer.addLayout(header)

        # --- Command label ---
        self._cmd_label_title = QLabel(i18n.tr("terminal_panel.command_label"))
        self._cmd_label_title.setObjectName("terminal_label")
        outer.addWidget(self._cmd_label_title)

        self._cmd_display = QLabel("$ ")
        self._cmd_display.setObjectName("terminal_command")
        self._cmd_display.setWordWrap(True)
        self._cmd_display.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        outer.addWidget(self._cmd_display)

        # --- Explanation ---
        self._explanation_title = QLabel(i18n.tr("terminal_panel.explanation"))
        self._explanation_title.setObjectName("terminal_label")
        outer.addWidget(self._explanation_title)

        self._explanation = QLabel("")
        self._explanation.setWordWrap(True)
        self._explanation.setStyleSheet(
            "color: #8B949E; font-size: 11px; background: transparent;"
        )
        outer.addWidget(self._explanation)

        # --- Output ---
        self._output_title = QLabel(i18n.tr("terminal_panel.output"))
        self._output_title.setObjectName("terminal_label")
        outer.addWidget(self._output_title)

        self._output = QPlainTextEdit()
        self._output.setObjectName("terminal_output")
        self._output.setReadOnly(True)
        self._output.setMaximumHeight(120)
        outer.addWidget(self._output)

        self._cmd_str: str = ""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show_command(
        self,
        cmd_str: str,
        description: str = "",
        args_info: Optional[list[dict]] = None,
    ) -> None:
        """
        Display a new command in the panel and make it visible.

        Parameters
        ----------
        cmd_str      : The full command string (e.g. "sudo apt install firefox")
        description  : Human-friendly description of what it does
        args_info    : List of {token, explanation} dicts from PackageManager
        """
        self._cmd_str = cmd_str
        self._cmd_display.setText(f"$ {cmd_str}")
        self._output.clear()

        if description:
            self._explanation.setText(description)
        elif args_info:
            parts = [
                f"<b>{a['token']}</b>: {a['explanation']}"
                for a in args_info if a.get("explanation")
            ]
            self._explanation.setText("  |  ".join(parts[:4]))
        else:
            self._explanation.setText("")

        self.show()

    def append_output(self, line: str) -> None:
        """Append a line of text to the output viewer."""
        self._output.appendPlainText(line)
        # Auto-scroll to bottom
        sb = self._output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def clear(self) -> None:
        self._cmd_display.setText("$ ")
        self._output.clear()
        self._explanation.setText("")

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _copy_command(self) -> None:
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(self._cmd_str)
        self._copy_btn.setText(i18n.tr("terminal_panel.copied"))
        QTimer.singleShot(2000, lambda: self._copy_btn.setText(i18n.tr("terminal_panel.copy")))

    def _retranslate(self) -> None:
        self._title_label.setText(i18n.tr("terminal_panel.title"))
        self._copy_btn.setText(i18n.tr("terminal_panel.copy"))
        self._cmd_label_title.setText(i18n.tr("terminal_panel.command_label"))
        self._explanation_title.setText(i18n.tr("terminal_panel.explanation"))
        self._output_title.setText(i18n.tr("terminal_panel.output"))
