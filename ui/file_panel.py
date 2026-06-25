from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyqtgraph as pg
from nptdms import TdmsFile
from numpy.typing import NDArray
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
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