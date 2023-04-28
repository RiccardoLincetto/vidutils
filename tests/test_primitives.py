from unittest.mock import MagicMock

import cv2
import numpy as np
import pytest
from numpy.typing import NDArray

from tests import settings
from vidutils.primitives import Frame, Writer


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

        mock_capture.isOpened.return_value = True
        mock_capture.isOpened.side_effect = [
            True,
        ] * 30 + [
            False
        ]  # video of 1 second
        mock_capture.read.return_value = (True, np.random.randint(0, 255, (100, 100, 3)))
        mock_capture.release.return_value = None
        return mock_capture

    def test_init_with_capture(self, mock_capture: cv2.VideoCapture):
        writer = Writer("video.mp4", mock_capture)
        assert mock_capture.get.call_count == 3  # fps, width, height
        assert writer.isOpened()
        writer.release()
        assert not writer.isOpened()

        writer = Writer("video.mp4", mock_capture)
        while mock_capture.isOpened():
            mock_ok, mock_frame = mock_capture.read()
            if mock_ok:
                writer.write(mock_capture)
            else:
                mock_frame.release()
        writer.release()


class TestWritingFrame:
    """Test writing a frame to a video file.

    `cv2.VideoWriter.write` expects a numpy array, but we want to be able to pass a `Frame` object.
    """

    def test_writing_frame(self):
        """Write a video with a single frame."""
        frame_numpy: NDArray[(320, 480, 3)] = np.random.randint(0, 255, (320, 480, 3), dtype=np.uint8)
        # Write video with numpy frame
        writer = cv2.VideoWriter("video_numpy.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (480, 320))
        writer.write(frame_numpy)
        writer.release()
        # Convert frame to Frame object
        Frame(frame_numpy)
        # Write video with frame
        writer = cv2.VideoWriter("video_frame.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (480, 320))
        writer.write(frame_numpy)
        writer.release()
        # Compare videos
        capture_numpy = cv2.VideoCapture("video_numpy.mp4")
        capture_frame = cv2.VideoCapture("video_frame.mp4")
        while capture_numpy.isOpened() and capture_frame.isOpened():
            ok_numpy, frame_numpy = capture_numpy.read()
            ok_frame, frame_frame = capture_frame.read()
            if ok_numpy and ok_frame:
                assert np.array_equal(frame_numpy, frame_frame)
            else:
                break
