from numpy.typing import NDArray
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class ChannelData:
    title: str
    x: NDArray[np.float64]
    y: NDArray[np.float64]
    x_label: str
    y_label: str
    properties: dict[str, str]