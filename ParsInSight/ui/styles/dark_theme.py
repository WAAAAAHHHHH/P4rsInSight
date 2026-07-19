"""
P4rsInSight - Dark Theme QSS Stylesheet
Modern dark UI with Pardus Blue accents.
"""


def get_dark_stylesheet(font_size: int = 13) -> str:
    fs = font_size
    fs_sm = max(fs - 2, 10)
    fs_lg = fs + 2
    fs_xl = fs + 6

    return f"""
/* ═══════════════════════════════════════════════
   GLOBAL RESET & BASE
═══════════════════════════════════════════════ */
* {{
    font-family: "Segoe UI", "Ubuntu", "Inter", "Noto Sans", sans-serif;
    font-size: {fs}px;
    color: #E8EAF0;
    outline: none;
}}

QMainWindow, QDialog {{
    background-color: #0F1117;
}}

QWidget {{
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════
   SCROLLBARS
═══════════════════════════════════════════════ */
QScrollBar:vertical {{
    background: #1E2130;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #3D4460;
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #5C6BC0;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: #1E2130;
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #3D4460;
    border-radius: 4px;
    min-width: 30px;
}}

/* ═══════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════ */
#sidebar {{
    background-color: #141824;
    border-right: 1px solid #2A2D3E;
    min-width: 220px;
    max-width: 220px;
}}

#sidebar_logo_area {{
    background-color: #1565C0;
    padding: 20px 16px;
    min-height: 80px;
}}

#sidebar_app_name {{
    color: #FFFFFF;
    font-size: {fs_xl}px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

#sidebar_tagline {{
    color: rgba(255,255,255,0.7);
    font-size: {fs_sm}px;
}}

QPushButton#sidebar_item {{
    background-color: transparent;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: left;
    color: #8892B0;
    font-size: {fs}px;
    margin: 2px 8px;
}}

QPushButton#sidebar_item:hover {{
    background-color: #1E2640;
    color: #90CAF9;
}}

QPushButton#sidebar_item[active="true"] {{
    background-color: #1E2640;
    color: #90CAF9;
    font-weight: 600;
    border-left: 3px solid #42A5F5;
    border-radius: 0px 10px 10px 0px;
    margin-left: 5px;
    padding-left: 11px;
}}

/* ═══════════════════════════════════════════════
   TOP BAR
═══════════════════════════════════════════════ */
#top_bar {{
    background-color: #141824;
    border-bottom: 1px solid #2A2D3E;
    padding: 8px 20px;
    min-height: 56px;
    max-height: 56px;
}}

#page_title {{
    font-size: {fs_xl}px;
    font-weight: 700;
    color: #E8EAF0;
}}

#page_subtitle {{
    font-size: {fs_sm}px;
    color: #8892B0;
}}

/* ═══════════════════════════════════════════════
   SEARCH BAR
═══════════════════════════════════════════════ */
#search_bar {{
    background-color: #1E2130;
    border: 1.5px solid #2A2D3E;
    border-radius: 10px;
    padding: 8px 14px 8px 36px;
    font-size: {fs}px;
    color: #E8EAF0;
    min-width: 240px;
}}

#search_bar:focus {{
    border-color: #42A5F5;
    background-color: #252840;
}}

/* ═══════════════════════════════════════════════
   CARDS
═══════════════════════════════════════════════ */
#card {{
    background-color: #1A1D2E;
    border: 1px solid #2A2D3E;
    border-radius: 14px;
    padding: 18px;
}}

#card:hover {{
    border-color: #3D4DB7;
    background-color: #1E2240;
}}

#card_title {{
    font-size: {fs}px;
    font-weight: 600;
    color: #E8EAF0;
}}

#card_description {{
    font-size: {fs_sm}px;
    color: #8892B0;
    line-height: 1.4;
}}

/* ═══════════════════════════════════════════════
   STATUS BADGE
═══════════════════════════════════════════════ */
#badge_ok {{
    background-color: #1B3A2E;
    color: #66BB6A;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

#badge_warning {{
    background-color: #3A2E0E;
    color: #FFA726;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

#badge_error {{
    background-color: #3A0E0E;
    color: #EF5350;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

/* ═══════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════ */
QPushButton {{
    background-color: #1976D2;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 9px 20px;
    font-size: {fs}px;
    font-weight: 600;
    min-height: 36px;
}}

QPushButton:hover {{
    background-color: #42A5F5;
}}

QPushButton:pressed {{
    background-color: #0D47A1;
}}

QPushButton:disabled {{
    background-color: #2A2D3E;
    color: #4A4E6A;
}}

QPushButton#btn_secondary {{
    background-color: #1E2130;
    color: #90CAF9;
    border: 1.5px solid #2A2D3E;
}}

QPushButton#btn_secondary:hover {{
    background-color: #252840;
    border-color: #42A5F5;
}}

QPushButton#btn_danger {{
    background-color: #2D1111;
    color: #EF5350;
    border: 1.5px solid #4A1A1A;
}}

QPushButton#btn_danger:hover {{
    background-color: #3A1515;
}}

QPushButton#btn_success {{
    background-color: #1B3A2E;
    color: #66BB6A;
    border: 1.5px solid #2A5A3E;
}}

QPushButton#btn_success:hover {{
    background-color: #234E3A;
}}

/* ═══════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════ */
QTabWidget::pane {{
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    background: #1A1D2E;
    top: -1px;
}}

QTabBar::tab {{
    background: #141824;
    border: 1px solid #2A2D3E;
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 9px 18px;
    font-size: {fs}px;
    color: #8892B0;
    margin-right: 3px;
}}

QTabBar::tab:selected {{
    background: #1A1D2E;
    color: #90CAF9;
    font-weight: 600;
    border-bottom: 2px solid #42A5F5;
}}

QTabBar::tab:hover:!selected {{
    background: #1E2240;
    color: #90CAF9;
}}

/* ═══════════════════════════════════════════════
   INPUT FIELDS
═══════════════════════════════════════════════ */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: #1E2130;
    border: 1.5px solid #2A2D3E;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: {fs}px;
    color: #E8EAF0;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: #42A5F5;
    background-color: #252840;
}}

/* ═══════════════════════════════════════════════
   COMBOBOX
═══════════════════════════════════════════════ */
QComboBox {{
    background-color: #1E2130;
    border: 1.5px solid #2A2D3E;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: {fs}px;
    color: #E8EAF0;
    min-height: 36px;
}}

QComboBox:hover {{
    border-color: #42A5F5;
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox QAbstractItemView {{
    background-color: #1A1D2E;
    border: 1px solid #2A2D3E;
    border-radius: 10px;
    selection-background-color: #1E2640;
    selection-color: #90CAF9;
    padding: 4px;
    color: #E8EAF0;
}}

/* ═══════════════════════════════════════════════
   CHECKBOXES & RADIO BUTTONS
═══════════════════════════════════════════════ */
QCheckBox, QRadioButton {{
    spacing: 8px;
    font-size: {fs}px;
    color: #8892B0;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid #3D4460;
    border-radius: 5px;
    background: #1E2130;
}}

QCheckBox::indicator:checked {{
    background: #1976D2;
    border-color: #42A5F5;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid #3D4460;
    border-radius: 9px;
    background: #1E2130;
}}

QRadioButton::indicator:checked {{
    background: #1976D2;
    border-color: #42A5F5;
}}

/* ═══════════════════════════════════════════════
   SLIDER
═══════════════════════════════════════════════ */
QSlider::groove:horizontal {{
    height: 6px;
    background: #2A2D3E;
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: #42A5F5;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::sub-page:horizontal {{
    background: #1976D2;
    border-radius: 3px;
}}

/* ═══════════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════════ */
QProgressBar {{
    background-color: #2A2D3E;
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    font-size: {fs_sm}px;
    color: #8892B0;
}}

QProgressBar::chunk {{
    background-color: #42A5F5;
    border-radius: 6px;
}}

/* ═══════════════════════════════════════════════
   TERMINAL PANEL
═══════════════════════════════════════════════ */
#terminal_panel {{
    background-color: #0D1117;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #21262D;
}}

#terminal_command {{
    background-color: #161B22;
    color: #58A6FF;
    font-family: "Consolas", "Cascadia Code", "Fira Code", monospace;
    font-size: {fs}px;
    border-radius: 8px;
    padding: 12px 16px;
    border: 1px solid #30363D;
}}

#terminal_output {{
    background-color: #161B22;
    color: #8B949E;
    font-family: "Consolas", "Cascadia Code", "Fira Code", monospace;
    font-size: {fs_sm}px;
    border-radius: 8px;
    padding: 10px 14px;
    border: 1px solid #30363D;
}}

#terminal_label {{
    color: #8B949E;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

/* ═══════════════════════════════════════════════
   LABELS
═══════════════════════════════════════════════ */
QLabel#section_title {{
    font-size: {fs_lg}px;
    font-weight: 700;
    color: #E8EAF0;
}}

QLabel#section_subtitle {{
    font-size: {fs_sm}px;
    color: #8892B0;
}}

/* ═══════════════════════════════════════════════
   TOOLTIPS
═══════════════════════════════════════════════ */
QToolTip {{
    background-color: #1E2130;
    color: #E8EAF0;
    border: 1px solid #3D4460;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: {fs_sm}px;
}}

/* ═══════════════════════════════════════════════
   LIST WIDGET
═══════════════════════════════════════════════ */
QListWidget {{
    background-color: #1A1D2E;
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    border-radius: 8px;
    padding: 10px 12px;
    color: #8892B0;
    margin: 2px;
}}

QListWidget::item:selected {{
    background-color: #1E2640;
    color: #90CAF9;
}}

QListWidget::item:hover {{
    background-color: #1E2130;
}}

/* ═══════════════════════════════════════════════
   CONTENT AREA
═══════════════════════════════════════════════ */
#content_area {{
    background-color: #0F1117;
}}

#page_content {{
    background-color: #0F1117;
    padding: 20px;
}}

/* ═══════════════════════════════════════════════
   THEME TOGGLE BUTTON
═══════════════════════════════════════════════ */
#theme_toggle {{
    background-color: #1E2130;
    border: 1.5px solid #2A2D3E;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: {fs_sm}px;
    color: #8892B0;
    min-width: 80px;
}}

#theme_toggle:hover {{
    border-color: #42A5F5;
    color: #90CAF9;
}}

/* ═══════════════════════════════════════════════
   SEPARATOR
═══════════════════════════════════════════════ */
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: #2A2D3E;
}}

/* ═══════════════════════════════════════════════
   WIZARD
═══════════════════════════════════════════════ */
#wizard_card {{
    background-color: #1A1D2E;
    border: 2px solid #2A2D3E;
    border-radius: 16px;
    padding: 20px;
}}

#wizard_card:hover {{
    border-color: #42A5F5;
    background-color: #1E2240;
}}

#wizard_card[selected="true"] {{
    border-color: #42A5F5;
    background-color: #1E2640;
}}

#step_indicator {{
    background-color: #2A2D3E;
    border-radius: 14px;
    color: #8892B0;
    font-size: {fs_sm}px;
    font-weight: 600;
    min-width: 28px;
    min-height: 28px;
    max-width: 28px;
    max-height: 28px;
    padding: 0;
}}

#step_indicator[active="true"] {{
    background-color: #1976D2;
    color: #FFFFFF;
}}

#step_indicator[done="true"] {{
    background-color: #388E3C;
    color: #FFFFFF;
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
    background-color: #1A1D2E;
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    padding: 20px;
    color: #E8EAF0;
    font-size: {fs}px;
    line-height: 1.6;
    selection-background-color: #1E2640;
}}

/* ═══════════════════════════════════════════════
   SPLITTER
═══════════════════════════════════════════════ */
QSplitter::handle {{
    background: #2A2D3E;
    width: 1px;
}}
"""
