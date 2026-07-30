"""
P4rsInSight - Dark Theme QSS Stylesheet
Deep steel-grey palette with subtle lavender-white accents.
"""


def get_dark_stylesheet(font_size: int = 13) -> str:
    fs = font_size
    fs_xs = max(fs - 3, 9)
    fs_sm = max(fs - 1, 10)
    fs_lg = fs + 3
    fs_xl = fs + 8

    # ── Color tokens ──────────────────────────────────────────────────
    BG_DEEP   = "#0E0E11"
    BG_BASE   = "#16161A"
    BG_RAISED = "#1C1C21"
    BG_HOVER  = "#222228"
    BG_PRESS  = "#0A0A0D"

    BORDER    = "rgba(255,255,255,0.07)"
    BORDER_HI = "rgba(255,255,255,0.14)"
    BORDER_ACT= "rgba(200,200,230,0.30)"

    TEXT_PRI  = "#F0F0F4"
    TEXT_SEC  = "#8080A0"
    TEXT_DIM  = "#50506A"

    ACCENT    = "#C8C8E8"
    ACCENT_HI = "#E4E4F8"

    OK        = "#52B788"
    OK_BG     = "#0D2318"
    WARN      = "#E9C46A"
    WARN_BG   = "#261E08"
    ERR       = "#E63946"
    ERR_BG    = "#200A0C"

    SIDEBAR_W = "200px"

    return f"""
/* ═══════════════════════════════════════════════
   GLOBAL RESET & BASE
═══════════════════════════════════════════════ */
* {{
    font-family: "Segoe UI", "Inter", "Ubuntu", "Noto Sans", sans-serif;
    font-size: {fs}px;
    color: {TEXT_PRI};
    outline: none;
    border: none;
}}

QMainWindow, QDialog {{
    background-color: {BG_DEEP};
}}

QWidget {{
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════
   SCROLLBARS — ultra minimal
═══════════════════════════════════════════════ */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: rgba(255,255,255,0.10);
    border-radius: 3px;
    min-height: 40px;
}}
QScrollBar::handle:vertical:hover {{
    background: rgba(255,255,255,0.18);
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    height: 0; background: transparent;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: rgba(255,255,255,0.10);
    border-radius: 3px;
    min-width: 40px;
}}
QScrollBar::handle:horizontal:hover {{
    background: rgba(255,255,255,0.18);
}}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    width: 0; background: transparent;
}}

/* ═══════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════ */
#sidebar {{
    background-color: {BG_BASE};
    border-right: 1px solid {BORDER};
    min-width: {SIDEBAR_W};
    max-width: {SIDEBAR_W};
}}

#sidebar_logo_area {{
    background-color: {BG_BASE};
    padding: 0;
    min-height: 68px;
    max-height: 68px;
}}

#sidebar_app_name {{
    color: {TEXT_PRI};
    font-size: {fs_lg}px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

#sidebar_tagline {{
    color: {TEXT_DIM};
    font-size: {fs_xs}px;
    letter-spacing: 0.2px;
}}

QPushButton#sidebar_item {{
    background-color: transparent;
    border: none;
    border-radius: 0;
    border-left: 2px solid transparent;
    padding: 9px 16px;
    text-align: left;
    color: {TEXT_SEC};
    font-size: {fs_sm}px;
    font-weight: 400;
    margin: 0;
}}

QPushButton#sidebar_item:hover {{
    background-color: {BG_HOVER};
    color: {TEXT_PRI};
    border-left-color: {BORDER_HI};
}}

QPushButton#sidebar_item[active="true"] {{
    background-color: rgba(200, 200, 240, 0.06);
    color: {ACCENT_HI};
    font-weight: 600;
    border-left: 2px solid {ACCENT};
}}

/* ═══════════════════════════════════════════════
   TOP BAR
═══════════════════════════════════════════════ */
#top_bar {{
    background-color: {BG_BASE};
    border-bottom: 1px solid {BORDER};
    padding: 0 24px;
    min-height: 52px;
    max-height: 52px;
}}

#page_title {{
    font-size: {fs_lg}px;
    font-weight: 700;
    color: {TEXT_PRI};
    letter-spacing: -0.3px;
}}

#page_subtitle {{
    font-size: {fs_xs}px;
    color: {TEXT_DIM};
    letter-spacing: 0.2px;
}}

/* ═══════════════════════════════════════════════
   SEARCH BAR
═══════════════════════════════════════════════ */
#search_bar {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 7px 12px;
    font-size: {fs_sm}px;
    color: {TEXT_PRI};
    min-width: 220px;
}}

#search_bar:focus {{
    border-color: {BORDER_ACT};
    background-color: {BG_HOVER};
}}

#search_bar::placeholder {{
    color: {TEXT_DIM};
}}

/* ═══════════════════════════════════════════════
   CARDS
═══════════════════════════════════════════════ */
#card {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 16px;
}}

#card:hover {{
    border-color: {BORDER_HI};
    background-color: {BG_HOVER};
}}

#card_title {{
    font-size: {fs_sm}px;
    font-weight: 600;
    color: {TEXT_PRI};
}}

#card_description {{
    font-size: {fs_xs}px;
    color: {TEXT_SEC};
    line-height: 1.5;
}}

/* ═══════════════════════════════════════════════
   STATUS BADGES
═══════════════════════════════════════════════ */
#badge_ok {{
    background-color: {OK_BG};
    color: {OK};
    border-radius: 4px;
    border: 1px solid rgba(82,183,136,0.25);
    padding: 2px 8px;
    font-size: {fs_xs}px;
    font-weight: 600;
}}

#badge_warning {{
    background-color: {WARN_BG};
    color: {WARN};
    border-radius: 4px;
    border: 1px solid rgba(233,196,106,0.25);
    padding: 2px 8px;
    font-size: {fs_xs}px;
    font-weight: 600;
}}

#badge_error {{
    background-color: {ERR_BG};
    color: {ERR};
    border-radius: 4px;
    border: 1px solid rgba(230,57,70,0.25);
    padding: 2px 8px;
    font-size: {fs_xs}px;
    font-weight: 600;
}}

/* ═══════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════ */
QPushButton {{
    background-color: rgba(200,200,240,0.10);
    color: {ACCENT_HI};
    border: 1px solid {BORDER_HI};
    border-radius: 6px;
    padding: 7px 18px;
    font-size: {fs_sm}px;
    font-weight: 600;
    min-height: 32px;
}}

QPushButton:hover {{
    background-color: rgba(200,200,240,0.16);
    border-color: {BORDER_ACT};
    color: #FFFFFF;
}}

QPushButton:pressed {{
    background-color: rgba(200,200,240,0.06);
    border-color: {BORDER_HI};
}}

QPushButton:disabled {{
    background-color: rgba(255,255,255,0.03);
    color: {TEXT_DIM};
    border-color: {BORDER};
}}

QPushButton#btn_primary {{
    background-color: rgba(200,200,240,0.14);
    color: {ACCENT_HI};
    border: 1px solid rgba(200,200,240,0.25);
}}

QPushButton#btn_primary:hover {{
    background-color: rgba(200,200,240,0.22);
    border-color: rgba(200,200,240,0.40);
}}

QPushButton#btn_secondary {{
    background-color: transparent;
    color: {TEXT_SEC};
    border: 1px solid {BORDER};
}}

QPushButton#btn_secondary:hover {{
    background-color: {BG_HOVER};
    color: {TEXT_PRI};
    border-color: {BORDER_HI};
}}

QPushButton#btn_danger {{
    background-color: {ERR_BG};
    color: {ERR};
    border: 1px solid rgba(230,57,70,0.20);
}}

QPushButton#btn_danger:hover {{
    background-color: rgba(230,57,70,0.14);
    border-color: rgba(230,57,70,0.40);
}}

QPushButton#btn_success {{
    background-color: {OK_BG};
    color: {OK};
    border: 1px solid rgba(82,183,136,0.20);
}}

QPushButton#btn_success:hover {{
    background-color: rgba(82,183,136,0.14);
    border-color: rgba(82,183,136,0.40);
}}

/* ═══════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════ */
QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    background: {BG_RAISED};
    top: -1px;
}}

QTabBar::tab {{
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 8px 20px;
    font-size: {fs_sm}px;
    color: {TEXT_SEC};
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    color: {TEXT_PRI};
    font-weight: 600;
    border-bottom-color: {ACCENT};
}}

QTabBar::tab:hover:!selected {{
    color: {TEXT_PRI};
    background: {BG_HOVER};
    border-radius: 6px 6px 0 0;
}}

/* ═══════════════════════════════════════════════
   INPUT FIELDS
═══════════════════════════════════════════════ */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 7px 12px;
    font-size: {fs_sm}px;
    color: {TEXT_PRI};
    selection-background-color: rgba(200,200,240,0.20);
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {BORDER_ACT};
    background-color: {BG_HOVER};
}}

/* ═══════════════════════════════════════════════
   COMBOBOX
═══════════════════════════════════════════════ */
QComboBox {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 7px 12px;
    font-size: {fs_sm}px;
    color: {TEXT_PRI};
    min-height: 32px;
}}

QComboBox:hover {{
    border-color: {BORDER_HI};
}}

QComboBox:focus {{
    border-color: {BORDER_ACT};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER_HI};
    border-radius: 6px;
    selection-background-color: {BG_HOVER};
    selection-color: {TEXT_PRI};
    padding: 4px;
    color: {TEXT_PRI};
    outline: none;
}}

/* ═══════════════════════════════════════════════
   CHECKBOXES & RADIO BUTTONS
═══════════════════════════════════════════════ */
QCheckBox, QRadioButton {{
    spacing: 8px;
    font-size: {fs_sm}px;
    color: {TEXT_SEC};
}}

QCheckBox:hover, QRadioButton:hover {{
    color: {TEXT_PRI};
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {BORDER_HI};
    border-radius: 4px;
    background: {BG_RAISED};
}}

QCheckBox::indicator:checked {{
    background-color: rgba(200,200,240,0.20);
    border-color: {BORDER_ACT};
}}

QCheckBox::indicator:hover {{
    border-color: {BORDER_ACT};
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {BORDER_HI};
    border-radius: 8px;
    background: {BG_RAISED};
}}

QRadioButton::indicator:checked {{
    background-color: rgba(200,200,240,0.20);
    border-color: {BORDER_ACT};
}}

/* ═══════════════════════════════════════════════
   SLIDER
═══════════════════════════════════════════════ */
QSlider::groove:horizontal {{
    height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
}}

QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}

QSlider::handle:horizontal:hover {{
    background: {ACCENT_HI};
}}

QSlider::sub-page:horizontal {{
    background: rgba(200,200,240,0.30);
    border-radius: 2px;
}}

/* ═══════════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════════ */
QProgressBar {{
    background-color: rgba(255,255,255,0.06);
    border: none;
    border-radius: 3px;
    height: 4px;
    text-align: center;
    font-size: {fs_xs}px;
    color: transparent;
}}

QProgressBar::chunk {{
    background-color: {ACCENT};
    border-radius: 3px;
}}

/* ═══════════════════════════════════════════════
   TERMINAL PANEL
═══════════════════════════════════════════════ */
#terminal_panel {{
    background-color: {BG_BASE};
    border-top: 1px solid {BORDER};
    padding: 0;
}}

#terminal_command {{
    background-color: {BG_DEEP};
    color: {ACCENT};
    font-family: "Cascadia Code", "Consolas", "Fira Code", "JetBrains Mono", monospace;
    font-size: {fs_sm}px;
    border-radius: 6px;
    padding: 10px 14px;
    border: 1px solid {BORDER};
    letter-spacing: 0.3px;
}}

#terminal_output {{
    background-color: {BG_DEEP};
    color: {TEXT_SEC};
    font-family: "Cascadia Code", "Consolas", "Fira Code", "JetBrains Mono", monospace;
    font-size: {fs_xs}px;
    border-radius: 6px;
    padding: 8px 14px;
    border: 1px solid {BORDER};
}}

#terminal_label {{
    color: {TEXT_DIM};
    font-size: {fs_xs}px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ═══════════════════════════════════════════════
   SECTION LABELS
═══════════════════════════════════════════════ */
QLabel#section_title {{
    font-size: {fs_sm}px;
    font-weight: 700;
    color: {TEXT_PRI};
    letter-spacing: -0.2px;
}}

QLabel#section_subtitle {{
    font-size: {fs_xs}px;
    color: {TEXT_DIM};
}}

/* ═══════════════════════════════════════════════
   TOOLTIPS
═══════════════════════════════════════════════ */
QToolTip {{
    background-color: {BG_RAISED};
    color: {TEXT_PRI};
    border: 1px solid {BORDER_HI};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: {fs_xs}px;
}}

/* ═══════════════════════════════════════════════
   LIST WIDGET
═══════════════════════════════════════════════ */
QListWidget {{
    background-color: transparent;
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    border-radius: 5px;
    padding: 8px 12px;
    color: {TEXT_SEC};
    margin: 1px 2px;
    border: none;
}}

QListWidget::item:selected {{
    background-color: {BG_HOVER};
    color: {TEXT_PRI};
}}

QListWidget::item:hover {{
    background-color: rgba(255,255,255,0.04);
    color: {TEXT_PRI};
}}

/* ═══════════════════════════════════════════════
   CONTENT AREA
═══════════════════════════════════════════════ */
#content_area {{
    background-color: {BG_DEEP};
}}

#page_content {{
    background-color: {BG_DEEP};
    padding: 24px;
}}

/* ═══════════════════════════════════════════════
   TERMINAL TOGGLE BUTTON
═══════════════════════════════════════════════ */
#terminal_toggle {{
    background-color: transparent;
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 5px 12px;
    font-size: {fs_xs}px;
    color: {TEXT_DIM};
    min-width: 72px;
    font-weight: 500;
}}

#terminal_toggle:hover {{
    border-color: {BORDER_HI};
    color: {TEXT_SEC};
}}

#terminal_toggle:checked {{
    border-color: {BORDER_ACT};
    color: {ACCENT};
    background-color: rgba(200,200,240,0.06);
}}

/* ═══════════════════════════════════════════════
   SEPARATOR
═══════════════════════════════════════════════ */
QFrame[frameShape="4"],
QFrame[frameShape="5"] {{
    color: {BORDER};
    background: {BORDER};
    border: none;
    max-height: 1px;
}}

/* ═══════════════════════════════════════════════
   WIZARD
═══════════════════════════════════════════════ */
#wizard_card {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 18px;
}}

#wizard_card:hover {{
    border-color: {BORDER_HI};
    background-color: {BG_HOVER};
}}

#wizard_card[selected="true"] {{
    border-color: {BORDER_ACT};
    background-color: rgba(200,200,240,0.08);
}}

#step_indicator {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 12px;
    color: {TEXT_DIM};
    font-size: {fs_xs}px;
    font-weight: 700;
    min-width: 24px;
    min-height: 24px;
    max-width: 24px;
    max-height: 24px;
    padding: 0;
}}

#step_indicator[active="true"] {{
    background-color: rgba(200,200,240,0.12);
    border-color: {BORDER_ACT};
    color: {ACCENT_HI};
}}

#step_indicator[done="true"] {{
    background-color: {OK_BG};
    border-color: rgba(82,183,136,0.30);
    color: {OK};
}}

/* ═══════════════════════════════════════════════
   SCROLL AREA
═══════════════════════════════════════════════ */
QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

/* ═══════════════════════════════════════════════
   TEXT BROWSER
═══════════════════════════════════════════════ */
QTextBrowser {{
    background-color: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 20px;
    color: {TEXT_PRI};
    font-size: {fs_sm}px;
    line-height: 1.6;
    selection-background-color: rgba(200,200,240,0.20);
}}

/* ═══════════════════════════════════════════════
   SPLITTER
═══════════════════════════════════════════════ */
QSplitter::handle {{
    background: {BORDER};
    width: 1px;
    height: 1px;
}}

QSplitter::handle:hover {{
    background: {BORDER_HI};
}}

/* ═══════════════════════════════════════════════
   MESSAGE BOX
═══════════════════════════════════════════════ */
QMessageBox {{
    background-color: {BG_RAISED};
}}

QMessageBox QLabel {{
    color: {TEXT_PRI};
    font-size: {fs_sm}px;
}}
"""
