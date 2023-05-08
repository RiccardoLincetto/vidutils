from unittest.mock import MagicMock

import cv2
import numpy as np
import pytest

from vidutils.artifacts import Artifact
from vidutils.engine import Looper


@pytest.fixture
def mock_reader():
    reader = MagicMock()
    reader.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))
    reader.get.return_value = 1
    yield reader


@pytest.fixture
def looper(reader):
    def processor(frame):
        # Example processor that returns a dummy artifact
        return [Artifact("dummy")]

    yield Looper(reader, processor)


def test_looper_step(looper):
    # Test that the step method processes a frame correctly
    looper.step()
    assert isinstance(looper.processor_output, list)
    assert isinstance(looper.processor_output[0], Artifact)


def test_looper_loop(looper):
    # Test that the loop method processes all frames
    looper.loop()
    assert looper.reader.get(cv2.CAP_PROP_POS_FRAMES) == looper.reader.get(cv2.CAP_PROP_FRAME_COUNT)


def test_looper_with_preprocessor(reader):
    # Test that the looper works with a preprocessor
    def preprocessor(frame):
        return np.zeros_like(frame)

    looper = Looper(reader, lambda x: x, preprocessor=preprocessor)
    looper.step()
    assert isinstance(looper.input, np.ndarray)


def test_looper_with_postprocessor(looper):
    # Test that the looper works with a postprocessor
    def postprocessor(output):
        return [Artifact("dummy_post")]

    looper.postprocessor = postprocessor
    looper.step()
    assert isinstance(looper.artifacts, list)
    assert isinstance(looper.artifacts[0], Artifact)
