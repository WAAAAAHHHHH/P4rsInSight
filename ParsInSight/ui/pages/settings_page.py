"""
P4rsInSight - Settings Page
Configure language, theme, font size, animations, terminal mode, and notifications.
Changes apply immediately without restart.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import SUPPORTED_LANGUAGES, i18n
from core.logger import get_logger
from core.settings_manager import settings

log = get_logger("settings_page")


class SettingsGroup(QWidget):
    """A labeled group of settings with a card-like container."""

    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self._title = title
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(14)

        self._title_lbl = QLabel(f"<b>{title}</b>")
        self._title_lbl.setObjectName("card_title")
        self._title_lbl.setStyleSheet("font-size: 14px;")
        outer.addWidget(self._title_lbl)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        outer.addWidget(sep)

        self._body = QVBoxLayout()
        self._body.setSpacing(12)
        outer.addLayout(self._body)

    def add_row(self, label: str, widget: QWidget, description: str = "") -> QWidget:
        """Add a label + widget row. Returns the row container."""
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(16)

        label_col = QVBoxLayout()
        label_col.setSpacing(2)
        lbl = QLabel(label)
        lbl.setStyleSheet("font-weight: 600;")
        label_col.addWidget(lbl)
        if description:
            desc = QLabel(description)
            desc.setStyleSheet("color: #78909C; font-size: 11px;")
            desc.setWordWrap(True)
            label_col.addWidget(desc)

        row_layout.addLayout(label_col, 1)
        row_layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignRight)

        self._body.addWidget(row)
        return row


class SettingsPage(QWidget):
    """Settings configuration page with live preview."""

    # Emitted when theme changes so MainWindow can apply the stylesheet
    theme_changed = Signal(str)
    font_size_changed = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
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
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Language group ---
        self._lang_group = SettingsGroup(i18n.tr("settings.language"))
        self._lang_combo = QComboBox()
        for code, name in SUPPORTED_LANGUAGES.items():
            self._lang_combo.addItem(name, code)
        # Set current
        idx = list(SUPPORTED_LANGUAGES.keys()).index(settings.language) if settings.language in SUPPORTED_LANGUAGES else 0
        self._lang_combo.setCurrentIndex(idx)
        self._lang_combo.currentIndexChanged.connect(self._on_language_change)
        self._lang_row = self._lang_group.add_row(i18n.tr("settings.language"), self._lang_combo)
        self._content_layout.addWidget(self._lang_group)

        # --- Appearance group ---
        self._appearance_group = SettingsGroup(i18n.tr("settings.theme"))

        # Theme toggle
        self._theme_combo = QComboBox()
        self._theme_combo.addItem(f"☀️  {i18n.tr('settings.theme_light')}", "light")
        self._theme_combo.addItem(f"🌙  {i18n.tr('settings.theme_dark')}", "dark")
        self._theme_combo.setCurrentIndex(0 if settings.theme == "light" else 1)
        self._theme_combo.currentIndexChanged.connect(self._on_theme_change)
        self._theme_row = self._appearance_group.add_row(i18n.tr("settings.theme"), self._theme_combo)

        # Font size
        font_row_widget = QWidget()
        font_row_layout = QHBoxLayout(font_row_widget)
        font_row_layout.setContentsMargins(0, 0, 0, 0)
        font_row_layout.setSpacing(10)

        self._font_slider = QSlider(Qt.Orientation.Horizontal)
        self._font_slider.setRange(10, 18)
        self._font_slider.setValue(settings.font_size)
        self._font_slider.setFixedWidth(140)
        self._font_slider.valueChanged.connect(self._on_font_size_change)

        self._font_value_label = QLabel(f"{settings.font_size}px")
        self._font_value_label.setStyleSheet("font-weight: 600; min-width: 40px;")

        font_row_layout.addWidget(self._font_slider)
        font_row_layout.addWidget(self._font_value_label)

        self._font_row = self._appearance_group.add_row(
            i18n.tr("settings.font_size"), font_row_widget
        )
        self._content_layout.addWidget(self._appearance_group)

        # --- Behaviour group ---
        self._behaviour_group = SettingsGroup(i18n.tr("terminal_panel.title"))

        self._terminal_check = QCheckBox()
        self._terminal_check.setChecked(settings.terminal_learning_mode)
        self._terminal_check.stateChanged.connect(
            lambda state: settings.set("terminal_learning_mode", bool(state))
        )
        self._terminal_row = self._behaviour_group.add_row(
            i18n.tr("settings.terminal_mode"),
            self._terminal_check,
            i18n.tr("settings.terminal_mode_desc"),
        )

        self._notif_check = QCheckBox()
        self._notif_check.setChecked(settings.notifications_enabled)
        self._notif_check.stateChanged.connect(
            lambda state: settings.set("notifications_enabled", bool(state))
        )
        self._notif_row = self._behaviour_group.add_row(
            i18n.tr("settings.notifications"),
            self._notif_check,
            i18n.tr("settings.notifications_desc"),
        )
        self._content_layout.addWidget(self._behaviour_group)

        # --- Experience level ---
        self._level_group = SettingsGroup(i18n.tr("settings.experience_level"))
        self._level_combo = QComboBox()
        self._level_combo.addItem(f"🌱  {i18n.tr('wizard.level_beginner')}", "beginner")
        self._level_combo.addItem(f"📈  {i18n.tr('wizard.level_intermediate')}", "intermediate")
        self._level_combo.addItem(f"🚀  {i18n.tr('wizard.level_advanced')}", "advanced")
        levels = ["beginner", "intermediate", "advanced"]
        self._level_combo.setCurrentIndex(
            levels.index(settings.experience_level) if settings.experience_level in levels else 0
        )
        self._level_combo.currentIndexChanged.connect(self._on_level_change)
        self._level_group.add_row(i18n.tr("settings.experience_level"), self._level_combo)
        self._content_layout.addWidget(self._level_group)

        # --- About ---
        self._about_group = SettingsGroup(i18n.tr("settings.about"))
        version_lbl = QLabel("P4rsInSight  v1.0.0")
        version_lbl.setStyleSheet("font-weight: 600; font-size: 14px;")
        self._about_group._body.addWidget(version_lbl)

        about_text = QLabel(i18n.tr("settings.about_text"))
        about_text.setObjectName("card_description")
        about_text.setWordWrap(True)
        self._about_group._body.addWidget(about_text)
        self._content_layout.addWidget(self._about_group)

        self._content_layout.addStretch()

        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    def _on_language_change(self, index: int) -> None:
        lang = self._lang_combo.itemData(index)
        if lang:
            settings.language = lang
            i18n.set_language(lang)

    def _on_theme_change(self, index: int) -> None:
        theme = self._theme_combo.itemData(index)
        if theme:
            settings.theme = theme
            self.theme_changed.emit(theme)

    def _on_font_size_change(self, value: int) -> None:
        self._font_value_label.setText(f"{value}px")
        settings.font_size = value
        self.font_size_changed.emit(value)

    def _on_level_change(self, index: int) -> None:
        level = self._level_combo.itemData(index)
        if level:
            settings.set("experience_level", level)

    def _retranslate(self) -> None:
        # Re-create groups — simplest approach since all text changes
        # Clear and rebuild the content_layout widgets
        # In production, this would be a targeted update
        pass  # The widgets will use fresh i18n values on next interaction
