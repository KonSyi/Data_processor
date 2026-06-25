from __future__ import annotations

import sys

import pyqtgraph as pg
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from model.tdms_model import TdmsModel
from controller.main_controller import MainController

def main() -> None:
    pg.setConfigOptions(background="w", foreground="k", antialias=False)

    app = QApplication(sys.argv)
    app.setApplicationName("TDMS Viewer")

    model = TdmsModel()
    window = MainWindow()
    controller = MainController(model, window)

    # Чтобы объекты точно жили до конца приложения
    window._controller = controller  # type: ignore[attr-defined]

    app.aboutToQuit.connect(model.close)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()