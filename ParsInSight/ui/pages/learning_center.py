"""
P4rsInSight - Learning Center Page
Topic list sidebar + article viewer with beginner-friendly content.
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from core.i18n_manager import i18n
from core.logger import get_logger

log = get_logger("learning_center")

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "tutorials.json"


def _load_tutorials() -> list[dict]:
    try:
        with _DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f).get("tutorials", [])
    except Exception as exc:
        log.error("Failed to load tutorials: %s", exc)
        return []


def _markdown_to_html(text: str) -> str:
    """Simple markdown→HTML converter for tutorial content."""
    import re
    lines = text.split("\n")
    html_lines = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            if in_code:
                html_lines.append("</pre></code>")
                in_code = False
            else:
                html_lines.append("<code><pre style='background:#F5F7FA;padding:12px;border-radius:8px;'>")
                in_code = True
            continue
        if in_code:
            html_lines.append(line)
            continue
        # Headers
        if line.startswith("# "):
            html_lines.append(f"<h1 style='color:#1565C0'>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2 style='color:#1565C0'>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.strip() == "":
            html_lines.append("<br>")
        elif "|" in line and line.strip().startswith("|"):
            # Table
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if "---" in line:
                continue  # Skip separator
            html_lines.append("<tr>" + "".join(f"<td style='padding:6px 12px;border:1px solid #E0E4EE'>{c}</td>" for c in cells) + "</tr>")
        else:
            # Bold, inline code
            line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"`(.+?)`", r"<code style='background:#F0F4FF;padding:2px 6px;border-radius:4px'>\1</code>", line)
            line = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href='\2'>\1</a>", line)
            html_lines.append(f"<p style='margin:4px 0;line-height:1.6'>{line}</p>")

    return "<html><body style='font-family:Segoe UI,Ubuntu,sans-serif;font-size:13px;padding:8px'>" + "\n".join(html_lines) + "</body></html>"


class LearningCenterPage(QWidget):
    """Learning center with topic list and content viewer."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._tutorials = _load_tutorials()
        self._setup_ui()
        i18n.language_changed.connect(self._retranslate)

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # --- Left: topic list ---
        left = QWidget()
        left.setStyleSheet("background: #FFFFFF; border-right: 1px solid #E0E4EE;")
        left.setMinimumWidth(200)
        left.setMaximumWidth(260)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        topics_label = QLabel(f"📚  {i18n.tr('learning_center.all_topics')}")
        topics_label.setObjectName("section_title")
        left_layout.addWidget(topics_label)

        self._list = QListWidget()
        self._list.setFrameShape(self._list.Shape.NoFrame)
        self._list.currentRowChanged.connect(self._on_topic_selected)
        left_layout.addWidget(self._list, 1)

        splitter.addWidget(left)

        # --- Right: content viewer ---
        right = QWidget()
        right.setObjectName("page_content")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(24, 24, 24, 24)
        right_layout.setSpacing(0)

        self._browser = QTextBrowser()
        self._browser.setOpenLinks(False)
        self._browser.setFrameShape(self._browser.Shape.NoFrame)
        right_layout.addWidget(self._browser)

        splitter.addWidget(right)
        splitter.setSizes([220, 600])

        outer.addWidget(splitter, 1)

        self._populate_list()

    def _populate_list(self) -> None:
        self._list.clear()
        lang = i18n.current_language
        for tut in self._tutorials:
            title_key = f"title_{lang}" if lang in ("tr", "en") else "title_en"
            title = tut.get(title_key, tut.get("title_en", ""))
            icon = tut.get("icon", "📄")
            item = QListWidgetItem(f"{icon}  {title}")
            item.setData(Qt.ItemDataRole.UserRole, tut["id"])
            self._list.addItem(item)

        if self._list.count() > 0:
            self._list.setCurrentRow(0)

    def _on_topic_selected(self, row: int) -> None:
        if row < 0 or row >= len(self._tutorials):
            return
        tut = self._tutorials[row]
        lang = i18n.current_language
        content_key = f"content_{lang}" if lang in ("tr", "en") else "content_en"
        content = tut.get(content_key, tut.get("content_en", i18n.tr("learning_center.no_content")))
        self._browser.setHtml(_markdown_to_html(content))

    def _retranslate(self) -> None:
        self._populate_list()
