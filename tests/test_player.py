from unittest.mock import MagicMock

import numpy as np
import pytest

from vidutils.primitives import Frame, Reader, Writer
from vidutils.player import Player


@pytest.fixture
def mock_reader() -> MagicMock:
    mock_reader = MagicMock(spec=Reader)
    mock_reader.isOpened.return_value = True
    mock_reader.read.return_value = Frame(np.random.randint(0, 255, (100, 100, 3)))
    mock_reader.release.return_value = None
    return mock_reader


@pytest.fixture
def mock_writer() -> MagicMock:
    mock_writer = MagicMock(spec=Writer)
    mock_writer.write.return_value = None
    mock_writer.release.return_value = None
    return mock_writer


class TestPlayerWithoutWriter:
    def test_init(self, mock_reader):
        player = Player(mock_reader)
        assert isinstance(player, Player)
        assert isinstance(player.reader, Reader)
        assert player.writer is None

    def test_step(self, mock_reader):
        player = Player(mock_reader)
        player._step()
        assert mock_reader.read.call_count == 1

    def test_close(self, mock_reader):
        player = Player(mock_reader)
        player.close()
        assert mock_reader.release.call_count == 1


class TestPlayerWithWriter:
    def test_init(self, mock_reader, mock_writer):
        player = Player(mock_reader, mock_writer)
        assert isinstance(player, Player)
        assert isinstance(player.reader, Reader)
        assert isinstance(player.writer, Writer)

    def test_step(self, mock_reader, mock_writer):
        player = Player(mock_reader, mock_writer)
        player._step()
        assert mock_reader.read.call_count == 1
        assert mock_writer.write.call_count == 1

    def test_close(self, mock_reader, mock_writer):
        player = Player(mock_reader, mock_writer)
        player.close()
        assert mock_reader.release.call_count == 1
        assert mock_writer.release.call_count == 1
