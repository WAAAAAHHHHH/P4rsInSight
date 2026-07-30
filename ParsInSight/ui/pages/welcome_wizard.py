"""
P4rsInSight - Welcome Wizard
Multi-step first-launch dialog:
  Step 1: Language selection
  Step 2: Experience level selection
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import SUPPORTED_LANGUAGES, i18n
from core.settings_manager import settings



class WelcomeWizard(QDialog):
    """
    First-launch setup wizard.

    Signals
    -------
    setup_complete(language, level)
    """

    setup_complete = Signal(str, str)


    def __init__(self, parent: QWidget | None = None) -> None:

        super().__init__(parent)
        self.setWindowTitle("P4rsInSight – Setup")
        self.setModal(True)
        self.setMinimumSize(640, 520)
        self.resize(680, 560)
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint
        )

        self._selected_lang  = settings.language
        self._selected_level = settings.experience_level

        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- Header ---
        header = QWidget()
        header.setStyleSheet("background-color: #1A1A1A; padding: 28px 36px;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(36, 28, 36, 28)
        header_layout.setSpacing(6)

        title = QLabel("P4rsInSight")
        title.setStyleSheet(
            "color: white; font-size: 28px; font-weight: 700; background: transparent;"
        )
        subtitle = QLabel(i18n.tr("wizard.subtitle"))
        subtitle.setStyleSheet(
            "color: rgba(255,255,255,0.8); font-size: 14px; background: transparent;"
        )
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        root.addWidget(header)

        # --- Step indicators ---
        steps_bar = QWidget()
        steps_bar.setStyleSheet("background: #1E1E1E; padding: 12px 36px; border-bottom: 1px solid #282828;")
        steps_layout = QHBoxLayout(steps_bar)
        steps_layout.setContentsMargins(36, 10, 36, 10)
        steps_layout.setSpacing(8)
        steps_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._step_indicators: list[QPushButton] = []
        step_labels = [
            i18n.tr("wizard.step_language"),
            i18n.tr("wizard.step_level"),
        ]
        for i, label in enumerate(step_labels):
            indicator = QPushButton(str(i + 1))
            indicator.setObjectName("step_indicator")
            indicator.setFixedSize(28, 28)
            indicator.setEnabled(False)
            self._step_indicators.append(indicator)
            steps_layout.addWidget(indicator)

            step_lbl = QLabel(label)
            step_lbl.setStyleSheet("color: rgba(255,255,255,0.40); font-size: 11px; background: transparent;")
            steps_layout.addWidget(step_lbl)

            if i < len(step_labels) - 1:
                sep = QLabel("›")
                sep.setStyleSheet("color: #B0BEC5; font-size: 16px; background: transparent;")
                steps_layout.addWidget(sep)

        steps_layout.addStretch()
        root.addWidget(steps_bar)

        # --- Stacked pages ---
        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_language_page())
        self._stack.addWidget(self._build_level_page())
        root.addWidget(self._stack, 1)

        # --- Bottom buttons ---
        btn_bar = QWidget()
        btn_bar.setStyleSheet("background: #1A1A1A; border-top: 1px solid #282828; padding: 16px 36px;")
        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(36, 12, 36, 12)

        self._skip_btn = QPushButton(i18n.tr("wizard.btn_skip"))
        self._skip_btn.setObjectName("btn_secondary")
        self._skip_btn.clicked.connect(self._on_skip)

        self._back_btn = QPushButton(i18n.tr("wizard.btn_back"))
        self._back_btn.setObjectName("btn_secondary")
        self._back_btn.setVisible(False)
        self._back_btn.clicked.connect(self._on_back)

        self._next_btn = QPushButton(i18n.tr("wizard.btn_next"))
        self._next_btn.clicked.connect(self._on_next)

        btn_layout.addWidget(self._skip_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self._back_btn)
        btn_layout.addSpacing(8)
        btn_layout.addWidget(self._next_btn)

        root.addWidget(btn_bar)

        self._update_step_indicators(0)

    # ------------------------------------------------------------------
    # Page builders
    # ------------------------------------------------------------------

    def _build_language_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(16)

        title = QLabel(i18n.tr("wizard.choose_language"))
        title.setObjectName("section_title")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        grid_widget = QWidget()
        grid = QHBoxLayout(grid_widget)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self._lang_group = QButtonGroup(self)
        for code, name in SUPPORTED_LANGUAGES.items():
            card = self._make_choice_card(name, "", self._lang_group, code)
            grid.addWidget(card)
            if code == self._selected_lang:
                # Find the radio inside and check it
                for child in card.findChildren(QRadioButton):
                    child.setChecked(True)

        grid.addStretch()
        scroll.setWidget(grid_widget)
        layout.addWidget(scroll, 1)
        return page



    def _build_level_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(16)

        title = QLabel(i18n.tr("wizard.choose_level"))
        title.setObjectName("section_title")
        layout.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(14)
        self._level_group = QButtonGroup(self)

        levels = [
            ("beginner",     "🌱", "wizard.level_beginner",     "wizard.level_beginner_desc"),
            ("intermediate", "📈", "wizard.level_intermediate",  "wizard.level_intermediate_desc"),
            ("advanced",     "🚀", "wizard.level_advanced",      "wizard.level_advanced_desc"),
        ]
        for lvl_id, icon, name_key, desc_key in levels:
            card = self._make_choice_card(
                f"{icon}  {i18n.tr(name_key)}",
                i18n.tr(desc_key),
                self._level_group,
                lvl_id,
            )
            row.addWidget(card)
            for child in card.findChildren(QRadioButton):
                if child.property("value") == self._selected_level:
                    child.setChecked(True)

        row.addStretch()
        layout.addLayout(row)
        layout.addStretch()
        return page

    def _make_choice_card(
        self, title: str, description: str, group: QButtonGroup, value: str
    ) -> QWidget:
        """Build a clickable card with a radio button."""
        card = QWidget()
        card.setObjectName("wizard_card")
        card.setProperty("selected", "false")
        card.setMinimumWidth(160)
        card.setMaximumWidth(220)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        radio = QRadioButton(title)
        radio.setProperty("value", value)
        radio.setStyleSheet("font-size: 14px; font-weight: 600;")
        group.addButton(radio)

        radio.toggled.connect(lambda checked, c=card: self._on_card_selected(c, checked))

        layout.addWidget(radio)
        if description:
            desc = QLabel(description)
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #50506A; font-size: 11px;")
            layout.addWidget(desc)

        return card

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _current_step(self) -> int:
        return self._stack.currentIndex()

    def _on_next(self) -> None:
        step = self._current_step()

        if step == 0:
            btn = self._lang_group.checkedButton()
            if btn:
                self._selected_lang = btn.property("value")
                i18n.set_language(self._selected_lang)
        elif step == 1:
            btn = self._level_group.checkedButton()
            if btn:
                self._selected_level = btn.property("value")
            self._finish()
            return

        next_step = step + 1
        self._stack.setCurrentIndex(next_step)
        self._back_btn.setVisible(True)
        self._update_step_indicators(next_step)

        if next_step == 1:
            self._next_btn.setText(i18n.tr("wizard.btn_finish"))
        else:
            self._next_btn.setText(i18n.tr("wizard.btn_next"))

    def _on_back(self) -> None:
        step = self._current_step()
        if step > 0:
            prev = step - 1
            self._stack.setCurrentIndex(prev)
            self._update_step_indicators(prev)
            self._next_btn.setText(i18n.tr("wizard.btn_next"))
            if prev == 0:
                self._back_btn.setVisible(False)

    def _on_skip(self) -> None:
        self._finish()

    def _finish(self) -> None:
        settings.language       = self._selected_lang
        settings.set("experience_level", self._selected_level)
        settings.first_launch   = False
        i18n.set_language(self._selected_lang)
        self.setup_complete.emit(
            self._selected_lang,
            self._selected_level,
        )
        self.accept()

    def _on_card_selected(self, card: QWidget, checked: bool) -> None:
        card.setProperty("selected", "true" if checked else "false")
        card.style().unpolish(card)
        card.style().polish(card)

    def _update_step_indicators(self, current: int) -> None:
        for i, ind in enumerate(self._step_indicators):
            if i < current:
                ind.setProperty("done", "true")
                ind.setProperty("active", "false")
                ind.setText("✓")
            elif i == current:
                ind.setProperty("active", "true")
                ind.setProperty("done", "false")
                ind.setText(str(i + 1))
            else:
                ind.setProperty("active", "false")
                ind.setProperty("done", "false")
                ind.setText(str(i + 1))
            ind.style().unpolish(ind)
            ind.style().polish(ind)
