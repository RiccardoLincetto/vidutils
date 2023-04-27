from pathlib import Path

import cv2
import numpy as np
from numpy.typing import ArrayLike


class Frame(np.ndarray):
    """Video frame definition.

    This class represents only single RGB or grayscale frames.
    This is achieved inheriting from numpy N-dimensional array.
    The number of dimensions N can be either 2 or 3.
    - A grayscale frame can be represented with dimensions: `(H, W)` or `(H, W, 1)`.
    - An RGB frame can be represented with dimensions: `(H, W, 3)`.
    """

    def __new__(cls, input_array: ArrayLike) -> np.ndarray:  # type: ignore
        obj = np.asarray(input_array).view(cls)

        # Return RGB frames as is
        if obj.ndim == 3 and obj.shape[2] in (3, 1):
            return obj

        # Turn grayscale frames into 3D arrays by adding a trailing dimension
        elif obj.ndim == 2:
            return obj[:, :, np.newaxis]

        # Raise an error for invalid shapes
        raise ValueError(f"Invalid shape for Frame: {obj.shape}")

    @property
    def height(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def channels(self) -> int:
        return self.shape[2]


class Reader(cv2.VideoCapture):
    """Video reader."""

    @property
    def height(self) -> int:
        return int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))  # pragma: no cover

    @property
    def width(self) -> int:
        return int(self.get(cv2.CAP_PROP_FRAME_WIDTH))  # pragma: no cover

    @property
    def fps(self) -> int:
        return int(self.get(cv2.CAP_PROP_FPS))  # pragma: no cover


class Writer(cv2.VideoWriter):
    """Video writer."""

    _EXT_TO_FOURCC = {
        ".avi": "DIVX",
        ".mkv": "X264",
        ".mp4": "mp4v",
    }

    def __init__(self, filename: Path | str, reader: cv2.VideoCapture) -> None:
        super().__init__(
            str(filename),
            cv2.VideoWriter_fourcc(*self._EXT_TO_FOURCC[Path(filename).suffix]),
            int(reader.get(cv2.CAP_PROP_FPS)),
            (int(reader.get(cv2.CAP_PROP_FRAME_WIDTH)), int(reader.get(cv2.CAP_PROP_FRAME_HEIGHT))),
        )
