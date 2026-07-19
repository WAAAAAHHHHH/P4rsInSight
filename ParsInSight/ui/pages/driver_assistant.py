"""
P4rsInSight - Driver Assistant Page
Detects hardware and recommends appropriate drivers.
"""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
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
from core.system_info import GpuInfo, NetworkInfo, collect_system_report
from ui.components.card import Card, StatusCard
from ui.components.terminal_panel import TerminalPanel

log = get_logger("driver_assistant")


class _ScanWorker(QThread):
    finished = Signal(object)

    def run(self) -> None:
        report = collect_system_report()
        self.finished.emit(report)


class DriverAssistantPage(QWidget):
    def __init__(self, terminal_panel: TerminalPanel | None = None, parent=None) -> None:
        super().__init__(parent)
        self._terminal = terminal_panel
        self._report = None
        self._workers: list[CommandWorker] = []
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)
        self._start_scan()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        self._content = QWidget()
        self._content.setObjectName("page_content")
        self._layout = QVBoxLayout(self._content)
        self._layout.setContentsMargins(24, 24, 24, 24)
        self._layout.setSpacing(16)

        # Loading state
        self._loading = QLabel(f"🔍  {i18n.tr('driver_assistant.scanning')}")
        self._loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._loading.setStyleSheet("font-size: 16px; color: #78909C; padding: 60px;")
        self._layout.addWidget(self._loading)

        # Cards container
        self._cards_container = QWidget()
        self._cards_layout = QVBoxLayout(self._cards_container)
        self._cards_layout.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.setSpacing(12)
        self._cards_container.setVisible(False)
        self._layout.addWidget(self._cards_container)
        self._layout.addStretch()

        scroll.setWidget(self._content)
        outer.addWidget(scroll, 1)

    def _start_scan(self) -> None:
        self._loading.setVisible(True)
        self._cards_container.setVisible(False)
        worker = _ScanWorker()
        worker.finished.connect(self._on_scan_done)
        worker.start()
        self._scan_worker = worker

    def _on_scan_done(self, report) -> None:
        self._report = report
        self._loading.setVisible(False)
        self._cards_container.setVisible(True)
        self._build_driver_cards(report)

    def _build_driver_cards(self, report) -> None:
        # Clear
        for i in reversed(range(self._cards_layout.count())):
            w = self._cards_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        # GPU Section
        gpu = report.gpu
        gpu_status = "ok" if gpu.driver_installed else "warning"
        gpu_desc = (
            f"{gpu.brand}" if gpu.driver_installed
            else f"{gpu.brand} — {i18n.tr('driver_assistant.recommended_driver')}: {gpu.recommended_driver or 'N/A'}"
        )
        gpu_card = StatusCard(
            icon="🎮",
            title=i18n.tr("driver_assistant.gpu_section"),
            description=gpu_desc,
            status=gpu_status,
        )
        if not gpu.driver_installed and gpu.vendor == "nvidia":
            gpu_card.set_action(
                i18n.tr("driver_assistant.install_driver"),
                lambda: self._install_driver(
                    ["sudo", "ubuntu-drivers", "install"],
                    "NVIDIA Driver",
                )
            )
        self._cards_layout.addWidget(gpu_card)

        # Wi-Fi Section
        net = report.network
        wifi_status = "ok" if net.wifi_present else "warning"
        wifi_desc = (
            i18n.tr("driver_assistant.driver_installed") if net.wifi_present
            else f"Wi-Fi adapter not detected"
        )
        wifi_card = StatusCard(
            icon="📶",
            title=i18n.tr("driver_assistant.wifi_section"),
            description=wifi_desc,
            status=wifi_status,
        )
        self._cards_layout.addWidget(wifi_card)

        # Audio
        audio_card = StatusCard(
            icon="🔊",
            title=i18n.tr("driver_assistant.audio_section"),
            description=i18n.tr("driver_assistant.driver_installed"),
            status="ok",
        )
        self._cards_layout.addWidget(audio_card)

        # Rescan button
        rescan_btn = QPushButton(f"🔄  {i18n.tr('common.refresh')}")
        rescan_btn.setObjectName("btn_secondary")
        rescan_btn.clicked.connect(self._start_scan)
        self._cards_layout.addWidget(rescan_btn, 0, Qt.AlignmentFlag.AlignLeft)

        # Warning note
        warning = QLabel(f"⚠️  {i18n.tr('driver_assistant.warning')}")
        warning.setStyleSheet("color: #F57F17; font-size: 12px; padding: 8px;")
        warning.setWordWrap(True)
        self._cards_layout.addWidget(warning)

    def _install_driver(self, cmd: list[str], driver_name: str) -> None:
        msg = QMessageBox(self)
        msg.setWindowTitle(i18n.tr("common.confirm"))
        msg.setText(
            f"{i18n.tr('driver_assistant.confirm_driver')}\n\n"
            f"{driver_name}\n\n<code>{' '.join(cmd)}</code>"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            if self._terminal:
                exp = package_manager.build_command_explanation(cmd)
                self._terminal.show_command(
                    cmd_str=" ".join(cmd),
                    description=f"Installing {driver_name}",
                    args_info=exp.get("args", []),
                )
            worker = CommandWorker(cmd)
            if self._terminal:
                worker.output_line.connect(self._terminal.append_output)
            worker.start()
            self._workers.append(worker)

    def _retranslate(self) -> None:
        self._loading.setText(f"🔍  {i18n.tr('driver_assistant.scanning')}")
        if self._report:
            self._build_driver_cards(self._report)
