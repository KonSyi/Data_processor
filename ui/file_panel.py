from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class FilePanel(QWidget):
    file_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.info_label = QLabel("Файл не выбран")
        self.info_label.setWordWrap(True)

        self.open_button = QPushButton("Открыть TDMS")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Файл"))
        layout.addWidget(self.info_label)
        layout.addWidget(self.open_button)

        self.open_button.clicked.connect(self.open_dialog)

    def open_dialog(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть TDMS файл",
            "",
            "TDMS files (*.tdms);;All files (*.*)",
        )
        if path:
            self.file_selected.emit(path)

    def set_current_file(self, path: str | None) -> None:
        self.info_label.setText(path if path else "Файл не выбран")