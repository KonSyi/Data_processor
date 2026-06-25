from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

class MetadataPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setLineWrapMode(QPlainTextEdit.NoWrap)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Свойства / статистика"))
        layout.addWidget(self.text)

    def set_properties(self, title: str, properties: dict[str, str]) -> None:
        lines = [title, "=" * len(title), ""]

        if not properties:
            lines.append("Нет данных")
        else:
            max_key_len = max(len(key) for key in properties)
            for key, value in properties.items():
                lines.append(f"{key:<{max_key_len}} : {value}")

        self.text.setPlainText("\n".join(lines))