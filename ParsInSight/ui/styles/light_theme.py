"""
P4rsInSight - Light Theme QSS Stylesheet
Modern, clean light UI inspired by Windows 11 Settings and GNOME Software.
Primary color: Pardus Blue #1565C0, Accent: #0288D1
"""


def get_light_stylesheet(font_size: int = 13) -> str:
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
    color: #1A1A2E;
    outline: none;
    box-sizing: border-box;
}}

QMainWindow, QDialog {{
    background-color: #F5F7FA;
}}

QWidget {{
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════
   SCROLLBARS
═══════════════════════════════════════════════ */
QScrollBar:vertical {{
    background: #EEF0F5;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #B0BEC5;
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #78909C;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: #EEF0F5;
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #B0BEC5;
    border-radius: 4px;
    min-width: 30px;
}}

/* ═══════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════ */
#sidebar {{
    background-color: #FFFFFF;
    border-right: 1px solid #E0E4EE;
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
    color: rgba(255,255,255,0.75);
    font-size: {fs_sm}px;
}}

QPushButton#sidebar_item {{
    background-color: transparent;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: left;
    color: #37474F;
    font-size: {fs}px;
    margin: 2px 8px;
}}

QPushButton#sidebar_item:hover {{
    background-color: #E3F2FD;
    color: #1565C0;
}}

QPushButton#sidebar_item[active="true"] {{
    background-color: #E3F2FD;
    color: #1565C0;
    font-weight: 600;
    border-left: 3px solid #1565C0;
    border-radius: 0px 10px 10px 0px;
    margin-left: 5px;
    padding-left: 11px;
}}

/* ═══════════════════════════════════════════════
   TOP BAR
═══════════════════════════════════════════════ */
#top_bar {{
    background-color: #FFFFFF;
    border-bottom: 1px solid #E0E4EE;
    padding: 8px 20px;
    min-height: 56px;
    max-height: 56px;
}}

#page_title {{
    font-size: {fs_xl}px;
    font-weight: 700;
    color: #1A1A2E;
}}

#page_subtitle {{
    font-size: {fs_sm}px;
    color: #78909C;
}}

/* ═══════════════════════════════════════════════
   SEARCH BAR
═══════════════════════════════════════════════ */
#search_bar {{
    background-color: #F5F7FA;
    border: 1.5px solid #E0E4EE;
    border-radius: 10px;
    padding: 8px 14px 8px 36px;
    font-size: {fs}px;
    color: #1A1A2E;
    min-width: 240px;
}}

#search_bar:focus {{
    border-color: #1565C0;
    background-color: #FFFFFF;
}}

/* ═══════════════════════════════════════════════
   CARDS
═══════════════════════════════════════════════ */
#card {{
    background-color: #FFFFFF;
    border: 1px solid #E8ECF5;
    border-radius: 14px;
    padding: 18px;
}}

#card:hover {{
    border-color: #BBDEFB;
    background-color: #FAFCFF;
}}

#card_title {{
    font-size: {fs}px;
    font-weight: 600;
    color: #1A1A2E;
}}

#card_description {{
    font-size: {fs_sm}px;
    color: #78909C;
    line-height: 1.4;
}}

/* ═══════════════════════════════════════════════
   STATUS BADGE
═══════════════════════════════════════════════ */
#badge_ok {{
    background-color: #E8F5E9;
    color: #2E7D32;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

#badge_warning {{
    background-color: #FFF8E1;
    color: #F57F17;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

#badge_error {{
    background-color: #FFEBEE;
    color: #C62828;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

/* ═══════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════ */
QPushButton {{
    background-color: #1565C0;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 9px 20px;
    font-size: {fs}px;
    font-weight: 600;
    min-height: 36px;
}}

QPushButton:hover {{
    background-color: #1976D2;
}}

QPushButton:pressed {{
    background-color: #0D47A1;
}}

QPushButton:disabled {{
    background-color: #CFD8DC;
    color: #90A4AE;
}}

QPushButton#btn_secondary {{
    background-color: #F5F7FA;
    color: #1565C0;
    border: 1.5px solid #BBDEFB;
}}

QPushButton#btn_secondary:hover {{
    background-color: #E3F2FD;
    border-color: #1565C0;
}}

QPushButton#btn_danger {{
    background-color: #FFEBEE;
    color: #C62828;
    border: 1.5px solid #FFCDD2;
}}

QPushButton#btn_danger:hover {{
    background-color: #FFCDD2;
    border-color: #C62828;
}}

QPushButton#btn_success {{
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 1.5px solid #C8E6C9;
}}

QPushButton#btn_success:hover {{
    background-color: #C8E6C9;
}}

/* ═══════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════ */
QTabWidget::pane {{
    border: 1px solid #E0E4EE;
    border-radius: 12px;
    background: #FFFFFF;
    top: -1px;
}}

QTabBar::tab {{
    background: #F5F7FA;
    border: 1px solid #E0E4EE;
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 9px 18px;
    font-size: {fs}px;
    color: #546E7A;
    margin-right: 3px;
}}

QTabBar::tab:selected {{
    background: #FFFFFF;
    color: #1565C0;
    font-weight: 600;
    border-bottom: 2px solid #1565C0;
}}

QTabBar::tab:hover:!selected {{
    background: #E3F2FD;
    color: #1565C0;
}}

/* ═══════════════════════════════════════════════
   INPUT FIELDS
═══════════════════════════════════════════════ */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: #F5F7FA;
    border: 1.5px solid #E0E4EE;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: {fs}px;
    color: #1A1A2E;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: #1565C0;
    background-color: #FFFFFF;
}}

/* ═══════════════════════════════════════════════
   COMBOBOX
═══════════════════════════════════════════════ */
QComboBox {{
    background-color: #F5F7FA;
    border: 1.5px solid #E0E4EE;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: {fs}px;
    color: #1A1A2E;
    min-height: 36px;
}}

QComboBox:hover {{
    border-color: #1565C0;
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    width: 0;
}}

QComboBox QAbstractItemView {{
    background-color: #FFFFFF;
    border: 1px solid #E0E4EE;
    border-radius: 10px;
    selection-background-color: #E3F2FD;
    selection-color: #1565C0;
    padding: 4px;
}}

/* ═══════════════════════════════════════════════
   CHECKBOXES & RADIO BUTTONS
═══════════════════════════════════════════════ */
QCheckBox, QRadioButton {{
    spacing: 8px;
    font-size: {fs}px;
    color: #37474F;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid #B0BEC5;
    border-radius: 5px;
    background: #FFFFFF;
}}

QCheckBox::indicator:checked {{
    background: #1565C0;
    border-color: #1565C0;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid #B0BEC5;
    border-radius: 9px;
    background: #FFFFFF;
}}

QRadioButton::indicator:checked {{
    background: #1565C0;
    border-color: #1565C0;
}}

/* ═══════════════════════════════════════════════
   SLIDER (Font Size)
═══════════════════════════════════════════════ */
QSlider::groove:horizontal {{
    height: 6px;
    background: #E0E4EE;
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: #1565C0;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::sub-page:horizontal {{
    background: #1565C0;
    border-radius: 3px;
}}

/* ═══════════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════════ */
QProgressBar {{
    background-color: #E0E4EE;
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    font-size: {fs_sm}px;
}}

QProgressBar::chunk {{
    background-color: #1565C0;
    border-radius: 6px;
}}

/* ═══════════════════════════════════════════════
   TERMINAL PANEL
═══════════════════════════════════════════════ */
#terminal_panel {{
    background-color: #1A1A2E;
    border-radius: 14px;
    padding: 16px;
}}

#terminal_command {{
    background-color: #0D1117;
    color: #58A6FF;
    font-family: "Consolas", "Cascadia Code", "Fira Code", monospace;
    font-size: {fs}px;
    border-radius: 8px;
    padding: 12px 16px;
    border: 1px solid #30363D;
}}

#terminal_output {{
    background-color: #0D1117;
    color: #8B949E;
    font-family: "Consolas", "Cascadia Code", "Fira Code", monospace;
    font-size: {fs_sm}px;
    border-radius: 8px;
    padding: 10px 14px;
    border: 1px solid #30363D;
}}

#terminal_label {{
    color: #ADBAC7;
    font-size: {fs_sm}px;
    font-weight: 600;
}}

/* ═══════════════════════════════════════════════
   LABELS
═══════════════════════════════════════════════ */
QLabel#section_title {{
    font-size: {fs_lg}px;
    font-weight: 700;
    color: #1A1A2E;
}}

QLabel#section_subtitle {{
    font-size: {fs_sm}px;
    color: #78909C;
}}

/* ═══════════════════════════════════════════════
   TOOLTIPS
═══════════════════════════════════════════════ */
QToolTip {{
    background-color: #37474F;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: {fs_sm}px;
}}

/* ═══════════════════════════════════════════════
   LIST WIDGET
═══════════════════════════════════════════════ */
QListWidget {{
    background-color: #FFFFFF;
    border: 1px solid #E0E4EE;
    border-radius: 12px;
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    border-radius: 8px;
    padding: 10px 12px;
    color: #37474F;
    margin: 2px;
}}

QListWidget::item:selected {{
    background-color: #E3F2FD;
    color: #1565C0;
}}

QListWidget::item:hover {{
    background-color: #F5F7FA;
}}

/* ═══════════════════════════════════════════════
   CONTENT AREA
═══════════════════════════════════════════════ */
#content_area {{
    background-color: #F5F7FA;
    padding: 0;
}}

#page_content {{
    background-color: #F5F7FA;
    padding: 20px;
}}

/* ═══════════════════════════════════════════════
   THEME TOGGLE BUTTON
═══════════════════════════════════════════════ */
#theme_toggle {{
    background-color: #F5F7FA;
    border: 1.5px solid #E0E4EE;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: {fs_sm}px;
    color: #546E7A;
    min-width: 80px;
}}

#theme_toggle:hover {{
    border-color: #1565C0;
    color: #1565C0;
}}

/* ═══════════════════════════════════════════════
   SEPARATOR
═══════════════════════════════════════════════ */
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: #E0E4EE;
}}

/* ═══════════════════════════════════════════════
   WIZARD
═══════════════════════════════════════════════ */
#wizard_card {{
    background-color: #FFFFFF;
    border: 2px solid #E0E4EE;
    border-radius: 16px;
    padding: 20px;
}}

#wizard_card:hover {{
    border-color: #1565C0;
    background-color: #F0F7FF;
}}

#wizard_card[selected="true"] {{
    border-color: #1565C0;
    background-color: #E3F2FD;
}}

#step_indicator {{
    background-color: #E0E4EE;
    border-radius: 14px;
    color: #78909C;
    font-size: {fs_sm}px;
    font-weight: 600;
    min-width: 28px;
    min-height: 28px;
    max-width: 28px;
    max-height: 28px;
    padding: 0;
}}

#step_indicator[active="true"] {{
    background-color: #1565C0;
    color: #FFFFFF;
}}

#step_indicator[done="true"] {{
    background-color: #4CAF50;
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
   TEXT BROWSER (Learning Center)
═══════════════════════════════════════════════ */
QTextBrowser {{
    background-color: #FFFFFF;
    border: 1px solid #E0E4EE;
    border-radius: 12px;
    padding: 20px;
    color: #1A1A2E;
    font-size: {fs}px;
    line-height: 1.6;
    selection-background-color: #BBDEFB;
}}

/* ═══════════════════════════════════════════════
   SPLITTER
═══════════════════════════════════════════════ */
QSplitter::handle {{
    background: #E0E4EE;
    width: 1px;
}}
"""
