from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

class PlotPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.caption_label = QLabel("Откройте файл и выберите канал")

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")

        plot_item = self.plot_widget.getPlotItem()
        plot_item.showGrid(x=True, y=True, alpha=0.3)
        plot_item.setDownsampling(auto=True, mode="peak")
        plot_item.setClipToView(True)

        self.curve = self.plot_widget.plot(
            [],
            [],
            pen=pg.mkPen(color="#1f77b4", width=1.2),
        )

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("График"))
        layout.addWidget(self.caption_label)
        layout.addWidget(self.plot_widget)

    def clear_plot(self, message: str = "Откройте файл и выберите канал") -> None:
        self.curve.setData([], [])
        self.plot_widget.setTitle("")
        self.plot_widget.setLabel("bottom", "")
        self.plot_widget.setLabel("left", "")
        self.caption_label.setText(message)

    def plot_channel(self, data: ChannelData) -> None:
        self.curve.setData(data.x, data.y)
        self.plot_widget.setTitle(data.title)
        self.plot_widget.setLabel("bottom", data.x_label)
        self.plot_widget.setLabel("left", data.y_label)
        self.plot_widget.getPlotItem().enableAutoRange()
        self.caption_label.setText(
            f"Показано точек: {len(data.y):,}".replace(",", " ")
        )