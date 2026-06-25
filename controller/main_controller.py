from __future__ import annotations

import re

from pathlib import Path
import numpy as np

from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from ui.main_window import MainWindow
from  model.tdms_model import TdmsModel
from domain.channel_data import ChannelData

class MainController:
    def __init__(self, model: TdmsModel, window: MainWindow) -> None:
        self.model = model
        self.window = window
        self.current_channel: ChannelData | None = None

        self.window.file_panel.file_selected.connect(self.open_file)
        self.window.channel_tree.channel_selected.connect(self.show_channel)
        self.window.open_action.triggered.connect(self.window.file_panel.open_dialog)
        self.window.export_csv_action.triggered.connect(self.export_current_channel)
        self.window.exit_action.triggered.connect(self.window.close)
        self.window.about_action.triggered.connect(self.show_about)


    def open_file(self, path: str) -> None:
        try:
            self.model.load(path)
            structure = self.model.get_structure()
            file_info = self.model.get_file_info()

            self.current_channel = None
            self.window.set_export_enabled(False)
            self.window.file_panel.set_current_file(path)
            self.window.channel_tree.set_structure(structure)
            self.window.metadata_panel.set_properties("Информация о файле", file_info)
            self.window.plot_panel.clear_plot("Файл загружен. Выберите канал слева.")
            self.window.setWindowTitle(f"TDMS Viewer — {Path(path).name}")
            self.window.statusBar().showMessage(f"Загружен файл: {Path(path).name}")

        except Exception as exc:
            QMessageBox.critical(
                self.window,
                "Ошибка загрузки",
                f"Не удалось открыть файл:\n{exc}",
            )

    def show_channel(self, group_name: str, channel_name: str) -> None:
        try:
            channel_data = self.model.get_channel_data(group_name, channel_name)
            self.current_channel = channel_data

            self.window.plot_panel.plot_channel(channel_data)
            self.window.metadata_panel.set_properties(
                channel_data.title,
                self._build_channel_properties(channel_data),
            )
            self.window.set_export_enabled(True)
            self.window.statusBar().showMessage(f"Показан канал: {channel_data.title}")

        except Exception as exc:
            QMessageBox.critical(
                self.window,
                "Ошибка отображения",
                f"Не удалось показать канал:\n{exc}",
            )

    def export_current_channel(self) -> None:
        if self.current_channel is None:
            QMessageBox.information(
                self.window,
                "Экспорт",
                "Сначала выберите канал.",
            )
            return

        default_name = self._safe_filename(self.current_channel.title) + ".csv"

        path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Сохранить CSV",
            default_name,
            "CSV files (*.csv);;All files (*.*)",
        )
        if not path:
            return

        try:
            data = np.column_stack((self.current_channel.x, self.current_channel.y))
            header = f"{self.current_channel.x_label};{self.current_channel.y_label}"

            with open(path, "w", encoding="utf-8", newline="") as file_obj:
                np.savetxt(
                    file_obj,
                    data,
                    delimiter=";",
                    header=header,
                    comments="",
                    fmt="%.12g",
                )

            self.window.statusBar().showMessage(
                f"CSV сохранён: {Path(path).name}",
                5000,
            )

        except Exception as exc:
            QMessageBox.critical(
                self.window,
                "Ошибка экспорта",
                f"Не удалось сохранить CSV:\n{exc}",
            )

    def show_about(self) -> None:
        QMessageBox.information(
            self.window,
            "О программе",
            "TDMS Viewer\n\n"
            "Минимальное настольное приложение для просмотра TDMS:\n"
            "- открытие TDMS\n"
            "- дерево каналов\n"
            "- график\n"
            "- свойства и статистика\n"
            "- экспорт канала в CSV",
        )

    def _build_channel_properties(self, channel_data: ChannelData) -> dict[str, str]:
        y = channel_data.y
        finite = y[np.isfinite(y)]

        info: dict[str, str] = {
            "Точек": self._format_int(len(y)),
            "NaN/inf": self._format_int(int(len(y) - len(finite))),
        }

        if len(finite) > 0:
            info.update(
                {
                    "Минимум": self._format_float(float(np.min(finite))),
                    "Максимум": self._format_float(float(np.max(finite))),
                    "Среднее": self._format_float(float(np.mean(finite))),
                    "Std": self._format_float(float(np.std(finite))),
                }
            )
        else:
            info.update(
                {
                    "Минимум": "нет конечных значений",
                    "Максимум": "нет конечных значений",
                    "Среднее": "нет конечных значений",
                    "Std": "нет конечных значений",
                }
            )

        info.update(channel_data.properties)
        return info

    @staticmethod
    def _format_int(value: int) -> str:
        return f"{value:,}".replace(",", " ")

    @staticmethod
    def _format_float(value: float) -> str:
        return f"{value:.6g}"

    @staticmethod
    def _safe_filename(text: str) -> str:
        cleaned = text.replace("/", "_").replace("\\", "_")
        cleaned = re.sub(r'[^0-9A-Za-zА-Яа-я._ -]+', "_", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned or "channel"