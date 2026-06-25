from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
)

from ui.file_panel import FilePanel
from ui.channel_tree import ChannelTree
from ui.plot_panel import PlotPanel
from ui.metadata_panel import MetadataPanel
# from ui.processing_panel import FilePanel

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TDMS Viewer")
        self.resize(1300, 850)

        self.file_panel = FilePanel()
        self.channel_tree = ChannelTree()
        self.plot_panel = PlotPanel()
        self.metadata_panel = MetadataPanel()

        self.open_action = QAction("Открыть TDMS...", self)
        self.open_action.setShortcut("Ctrl+O")

        self.export_csv_action = QAction("Экспорт текущего канала в CSV...", self)
        self.export_csv_action.setShortcut("Ctrl+S")
        self.export_csv_action.setEnabled(False)

        self.exit_action = QAction("Выход", self)
        self.exit_action.setShortcut("Ctrl+Q")

        self.about_action = QAction("О программе", self)

        self._build_menu()
        self._build_layout()

        self.statusBar().showMessage("Готово")

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.export_csv_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        help_menu = self.menuBar().addMenu("Справка")
        help_menu.addAction(self.about_action)

    def _build_layout(self) -> None:
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.addWidget(self.file_panel)
        left_splitter.addWidget(self.channel_tree)
        left_splitter.addWidget(self.metadata_panel)
        left_splitter.setSizes([120, 380, 260])

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(self.plot_panel)
        main_splitter.setSizes([420, 880])
        main_splitter.setStretchFactor(1, 1)

        self.setCentralWidget(main_splitter)

    def set_export_enabled(self, enabled: bool) -> None:
        self.export_csv_action.setEnabled(enabled)