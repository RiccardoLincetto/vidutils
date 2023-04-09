import unittest
from unittest.mock import Mock

from src.vidutils import video


class TestPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cap = Mock()
        algo = Mock()
        out = Mock()
        cls.player = video.Player(cap, algo, out)

    def test_pause(self):
        self.assertEqual(self.player.is_paused, False)
        self.player.is_paused = True
        self.assertEqual(self.player.is_paused, True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.player.close()
