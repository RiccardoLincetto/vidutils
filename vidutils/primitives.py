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

    def __new__(cls, input_array: ArrayLike) -> np.ndarray:  # TODO check output type is valid
        obj = np.asarray(input_array).view(cls)

        # Turn grayscale frames into 3D arrays by adding a trailing dimension
        if obj.ndim == 2:
            obj = obj[:, :, np.newaxis]

        # Check if the frame is valid
        elif obj.ndim != 3 or obj.shape[2] not in (1, 3):
            raise ValueError(f"Invalid shape for Frame: {obj.shape}")

        return obj

    @property
    def height(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def channels(self) -> int:
        return self.shape[2]
