from __future__ import annotations

from pathlib import Path

import numpy as np
from nptdms import TdmsFile
from numpy.typing import NDArray

from domain.channel_data import ChannelData

class TdmsModel:
    """Работа только с данными TDMS. GUI здесь нет."""

    def __init__(self) -> None:
        self.path: Path | None = None
        self._tdms: TdmsFile | None = None

    def close(self) -> None:
        if self._tdms is not None and hasattr(self._tdms, "close"):
            try:
                self._tdms.close()
            except Exception:
                pass
        self._tdms = None
        self.path = None

    def load(self, path: str | Path) -> None:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        self.close()

        # Ленивая загрузка: метаданные читаются сразу, данные канала — по запросу.
        self._tdms = TdmsFile.open(str(file_path))
        self.path = file_path

    def get_structure(self) -> dict[str, list[str]]:
        tdms = self._require_file()
        structure: dict[str, list[str]] = {}

        for group in tdms.groups():
            structure[group.name] = [channel.name for channel in group.channels()]

        return structure

    def get_file_info(self) -> dict[str, str]:
        structure = self.get_structure()

        return {
            "Файл": self.path.name if self.path else "",
            "Путь": str(self.path) if self.path else "",
            "Групп": str(len(structure)),
            "Каналов": str(sum(len(channels) for channels in structure.values())),
        }

    def get_channel_data(self, group_name: str, channel_name: str) -> ChannelData:
        tdms = self._require_file()

        group = tdms[group_name]
        channel = group[channel_name]

        y_raw = np.asarray(channel[:])

        if y_raw.ndim > 1:
            y_raw = y_raw.reshape(-1)

        if not np.issubdtype(y_raw.dtype, np.number):
            raise ValueError(
                f"Канал '{group_name} / {channel_name}' не является числовым "
                f"(dtype={y_raw.dtype}) и не может быть показан на графике."
            )

        y = y_raw.astype(np.float64, copy=False)
        x, x_label = self._build_x_axis(channel, len(y))
        y_label = self._extract_y_label(channel)

        properties = {
            str(key): self._format_property(value)
            for key, value in channel.properties.items()
        }
        properties.setdefault("Размер массива", str(len(y)))
        properties.setdefault("Тип данных", str(y_raw.dtype))

        return ChannelData(
            title=f"{group_name} / {channel_name}",
            x=x,
            y=y,
            x_label=x_label,
            y_label=y_label,
            properties=properties,
        )

    def _require_file(self) -> TdmsFile:
        if self._tdms is None:
            raise RuntimeError("TDMS файл ещё не загружен")
        return self._tdms

    def _build_x_axis(self, channel, length: int) -> tuple[NDArray[np.float64], str]:
        if length == 0:
            return np.array([], dtype=np.float64), "Отсчёт"

        try:
            x_raw = np.asarray(channel.time_track())

            if x_raw.ndim > 1:
                x_raw = x_raw.reshape(-1)

            if np.issubdtype(x_raw.dtype, np.number):
                return x_raw.astype(np.float64, copy=False), "Время, с"

            if np.issubdtype(x_raw.dtype, np.timedelta64):
                x_ns = x_raw.astype("timedelta64[ns]").astype(np.int64)
                return (x_ns / 1e9).astype(np.float64, copy=False), "Время, с"

            if np.issubdtype(x_raw.dtype, np.datetime64):
                x_ns = x_raw.astype("datetime64[ns]").astype(np.int64)
                x_sec = (x_ns - x_ns[0]) / 1e9
                return x_sec.astype(np.float64, copy=False), "Время от начала, с"

        except Exception:
            pass

        return np.arange(length, dtype=np.float64), "Отсчёт"

    def _extract_y_label(self, channel) -> str:
        for key in ("unit_string", "NI_UnitDescription", "wf_yunit_string"):
            value = channel.properties.get(key)
            if value is not None and str(value).strip():
                return f"Значение, {value}"
        return "Значение"

    @staticmethod
    def _format_property(value: object) -> str:
        if isinstance(value, np.ndarray):
            return f"array(shape={value.shape}, dtype={value.dtype})"
        return str(value)