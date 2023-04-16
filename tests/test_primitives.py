import numpy as np
import pytest

from tests import settings
from vidutils.primitives import Frame


class TestFrameCreation:
    @pytest.mark.parametrize("shape", settings.GOOD_SHAPES)
    def test_create_frame_from_numpy_array(self, shape: tuple[int, ...]):
        arr = np.zeros(shape)
        frame = Frame(arr)
        assert isinstance(frame, np.ndarray)
        assert isinstance(frame, Frame)
        assert len(frame.shape) == 3

    @pytest.mark.parametrize("shape", settings.BAD_SHAPES)
    def test_create_frame_from_numpy_array_with_invalid_shape(self, shape: tuple[int, ...]):
        arr = np.zeros(shape)
        with pytest.raises(ValueError):
            Frame(arr)


@pytest.mark.parametrize("shape", settings.GOOD_SHAPES)
class TestFrameProperties:
    def test_height(self, shape: tuple[int, ...]):
        frame = Frame(np.zeros(shape))
        assert frame.height == shape[0]

    def test_width(self, shape: tuple[int, ...]):
        frame = Frame(np.zeros(shape))
        assert frame.width == shape[1]

    def test_channels(self, shape: tuple[int, ...]):
        frame = Frame(np.zeros(shape))
        assert frame.channels == (shape[2] if len(shape) == 3 else 1)
