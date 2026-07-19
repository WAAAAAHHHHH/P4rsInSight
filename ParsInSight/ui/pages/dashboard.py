"""
P4rsInSight - Dashboard Page
Displays system health cards with status badges and one-click fix buttons.
Runs system analysis in a background QThread.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal, Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger
from core.system_info import SystemReport, collect_system_report
from ui.components.card import StatusCard
from ui.components.terminal_panel import TerminalPanel

log = get_logger("dashboard")


class _AnalysisWorker(QThread):
    """Runs collect_system_report() in a background thread."""
    finished = Signal(object)  # SystemReport

    def run(self) -> None:
        try:
            report = collect_system_report()
            self.finished.emit(report)
        except Exception as exc:
            log.exception("System analysis failed: %s", exc)
            self.finished.emit(None)


class DashboardPage(QWidget):
    """Main dashboard page."""

    action_requested = Signal(str, list)  # (description, cmd_list)

    def __init__(self, terminal_panel: TerminalPanel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._report: SystemReport | None = None
        self._cards: dict[str, StatusCard] = {}
        self._worker: _AnalysisWorker | None = None
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)
        self._start_analysis()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # --- Scroll area ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("page_content")
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(24, 24, 24, 24)
        self._content_layout.setSpacing(20)

        # Loading state
        self._loading_widget = QWidget()
        loading_layout = QVBoxLayout(self._loading_widget)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._loading_label = QLabel(i18n.tr("dashboard.analyzing"))
        self._loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._loading_label.setStyleSheet("font-size: 16px; color: #78909C;")

        self._progress = QProgressBar()
        self._progress.setRange(0, 0)  # indeterminate
        self._progress.setMaximumWidth(300)
        self._progress.setFixedHeight(6)

        loading_layout.addStretch()
        loading_layout.addWidget(self._loading_label, 0, Qt.AlignmentFlag.AlignCenter)
        loading_layout.addSpacing(12)
        loading_layout.addWidget(self._progress, 0, Qt.AlignmentFlag.AlignCenter)
        loading_layout.addStretch()
        self._content_layout.addWidget(self._loading_widget)

        # Cards container (hidden until loaded)
        self._cards_widget = QWidget()
        self._cards_widget.setVisible(False)
        self._cards_layout = QVBoxLayout(self._cards_widget)
        self._cards_layout.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.setSpacing(16)

        # Top row: status summary + refresh button
        top_row = QHBoxLayout()
        self._summary_label = QLabel("")
        self._summary_label.setObjectName("section_title")
        top_row.addWidget(self._summary_label)
        top_row.addStretch()

        self._refresh_btn = QPushButton(f"🔄  {i18n.tr('dashboard.refresh')}")
        self._refresh_btn.setObjectName("btn_secondary")
        self._refresh_btn.clicked.connect(self._start_analysis)
        top_row.addWidget(self._refresh_btn)
        self._cards_layout.addLayout(top_row)

        # Health cards grid
        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(14)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.addWidget(self._grid_widget)

        # System info section
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: #E0E4EE;")
        self._cards_layout.addWidget(sep)

        self._sysinfo_label = QLabel(f"💻  {i18n.tr('dashboard.system_info')}")
        self._sysinfo_label.setObjectName("section_title")
        self._cards_layout.addWidget(self._sysinfo_label)

        self._sysinfo_grid = QWidget()
        self._sysinfo_layout = QGridLayout(self._sysinfo_grid)
        self._sysinfo_layout.setSpacing(12)
        self._cards_layout.addWidget(self._sysinfo_grid)
        self._cards_layout.addStretch()

        self._content_layout.addWidget(self._cards_widget)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def _start_analysis(self) -> None:
        if self._worker and self._worker.isRunning():
            return

        self._cards_widget.setVisible(False)
        self._loading_widget.setVisible(True)
        self._refresh_btn.setEnabled(False) if hasattr(self, '_refresh_btn') else None

        self._worker = _AnalysisWorker()
        self._worker.finished.connect(self._on_analysis_done)
        self._worker.start()

    def _on_analysis_done(self, report: SystemReport | None) -> None:
        self._loading_widget.setVisible(False)
        self._cards_widget.setVisible(True)
        try:
            self._refresh_btn.setEnabled(True)
        except RuntimeError:
            pass

        if report is None:
            self._summary_label.setText("⚠ " + i18n.tr("common.error"))
            return

        self._report = report
        self._build_health_cards(report)
        self._build_system_info(report)

    def _build_health_cards(self, report: SystemReport) -> None:
        # Clear existing cards
        for i in reversed(range(self._grid.count())):
            widget = self._grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self._cards.clear()

        items = [
            {
                "id": "updates",
                "icon": "🔄",
                "title": i18n.tr("dashboard.card_system_update"),
                "ok": report.updates_available == 0,
                "desc_ok": i18n.tr("dashboard.up_to_date"),
                "desc_warn": i18n.tr("dashboard.updates_available", count=report.updates_available),
                "cmd": ["sudo", "apt", "upgrade", "-y"],
            },
            {
                "id": "gpu",
                "icon": "🎮",
                "title": i18n.tr("dashboard.card_gpu_driver"),
                "ok": report.gpu.driver_installed,
                "desc_ok": f"{report.gpu.brand} — " + i18n.tr("dashboard.installed"),
                "desc_warn": f"{report.gpu.brand} — " + i18n.tr("dashboard.recommended"),
                "cmd": ["sudo", "ubuntu-drivers", "install"],
            },
            {
                "id": "codecs",
                "icon": "🎬",
                "title": i18n.tr("dashboard.card_multimedia"),
                "ok": report.multimedia_codecs_installed,
                "desc_ok": i18n.tr("dashboard.installed"),
                "desc_warn": i18n.tr("dashboard.not_installed"),
                "cmd": ["sudo", "apt", "install", "-y", "ubuntu-restricted-extras"],
            },
            {
                "id": "flatpak",
                "icon": "📦",
                "title": i18n.tr("dashboard.card_flatpak"),
                "ok": report.flatpak_installed,
                "desc_ok": i18n.tr("dashboard.installed"),
                "desc_warn": i18n.tr("dashboard.not_installed"),
                "cmd": ["sudo", "apt", "install", "-y", "flatpak"],
            },
        ]

        issues = 0
        for idx, item in enumerate(items):
            ok = item["ok"]
            status = "ok" if ok else "warning"
            if not ok:
                issues += 1

            card = StatusCard(
                icon=item["icon"],
                title=item["title"],
                description=item["desc_ok"] if ok else item["desc_warn"],
                status=status,
            )
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            if not ok:
                cmd = item["cmd"]
                card.set_action(
                    i18n.tr("dashboard.fix"),
                    lambda checked=False, c=item["id"], cmd=cmd: self._on_fix(c, cmd),
                )

            self._cards[item["id"]] = card
            row, col = divmod(idx, 2)
            self._grid.addWidget(card, row, col)

        if issues == 0:
            self._summary_label.setText("✅  " + i18n.tr("dashboard.all_good"))
        else:
            self._summary_label.setText(f"⚠  {issues} " + i18n.tr("dashboard.fixes_available"))

    def _build_system_info(self, report: SystemReport) -> None:
        # Clear previous
        for i in reversed(range(self._sysinfo_layout.count())):
            w = self._sysinfo_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        info_items = [
            (i18n.tr("dashboard.cpu"),  f"{report.cpu.brand} ({report.cpu.cores_logical} cores)"),
            (i18n.tr("dashboard.ram"),  f"{report.ram.used_gb} GB / {report.ram.total_gb} GB"),
            (i18n.tr("dashboard.disk"), f"{report.disks[0].used_gb} GB / {report.disks[0].total_gb} GB" if report.disks else "N/A"),
            (i18n.tr("dashboard.os"),   f"{report.os.name} {report.os.version[:40]}"),
        ]

        for row, (label_text, value_text) in enumerate(info_items):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color: #78909C; font-size: 12px;")
            val = QLabel(value_text)
            val.setStyleSheet("font-weight: 600;")
            val.setWordWrap(True)
            self._sysinfo_layout.addWidget(lbl, row, 0)
            self._sysinfo_layout.addWidget(val, row, 1)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_fix(self, card_id: str, cmd: list[str]) -> None:
        from core.package_manager import package_manager

        explanation = package_manager.build_command_explanation(cmd)
        desc = f"Fixing: {card_id}"

        if self._terminal:
            self._terminal.show_command(
                cmd_str=" ".join(cmd),
                description=desc,
                args_info=explanation.get("args", []),
            )

        # Show confirmation dialog then run
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle(i18n.tr("common.confirm"))
        msg.setText(f"{i18n.tr('maintenance.confirm_run')}\n\n<code>{' '.join(cmd)}</code>")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            from core.package_manager import CommandWorker
            worker = CommandWorker(cmd)
            worker.output_line.connect(self._terminal.append_output)
            worker.finished.connect(lambda ok, msg: self._start_analysis())
            worker.start()
            self._workers = getattr(self, "_workers", [])
            self._workers.append(worker)

    def _retranslate(self) -> None:
        self._loading_label.setText(i18n.tr("dashboard.analyzing"))
        self._sysinfo_label.setText(f"💻  {i18n.tr('dashboard.system_info')}")
        self._refresh_btn.setText(f"🔄  {i18n.tr('dashboard.refresh')}")
        if self._report:
            self._build_health_cards(self._report)
            self._build_system_info(self._report)
