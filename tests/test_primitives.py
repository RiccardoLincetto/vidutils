from unittest.mock import MagicMock

import cv2
import numpy as np
import pytest

from tests import settings
from vidutils.primitives import Frame, Reader, Writer


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


class TestWriter:
    @pytest.fixture
    def mock_capture(self) -> MagicMock:
        mock_capture = MagicMock(spec=cv2.VideoCapture)
        mock_capture.get.side_effect = (30, 100, 100)  # fps, width, height
        return mock_capture

    @pytest.fixture
    def mock_reader(self) -> MagicMock:
        mock_reader = MagicMock(spec=Reader)
        mock_reader.get.side_effect = (30, 100, 100)  # fps, width, height
        return mock_reader

    def test_init_with_capture(self, mock_capture: cv2.VideoCapture):
        writer = Writer("path/to/output/video.mp4", mock_capture)
        assert isinstance(writer, Writer)
        assert isinstance(writer, cv2.VideoWriter)

    def test_init_with_reader(self, mock_reader: Reader):
        writer = Writer("path/to/output/video.mp4", mock_reader)
        assert isinstance(writer, Writer)
        assert isinstance(writer, cv2.VideoWriter)
