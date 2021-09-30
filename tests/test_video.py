import unittest
from unittest.mock import Mock

from vidutils import video


class TestSource(unittest.TestCase):

    def test_file(self):
        source = video.Source.FILE
        self.assertIs(source, video.Source.FILE)
        self.assertIsNot(source, video.Source.CAMERA)
        self.assertIsNot(source, video.Source.STREAM)

    def test_camera(self):
        source = video.Source.CAMERA
        self.assertIsNot(source, video.Source.FILE)
        self.assertIs(source, video.Source.CAMERA)
        self.assertIsNot(source, video.Source.STREAM)

    def test_stream(self):
        source = video.Source.STREAM
        self.assertIsNot(source, video.Source.FILE)
        self.assertIsNot(source, video.Source.CAMERA)
        self.assertIs(source, video.Source.STREAM)


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
        cls.close()
