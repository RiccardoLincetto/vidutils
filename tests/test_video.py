import unittest
from pathlib import Path
from unittest.mock import Mock

from vidutils import video


class TestReader(unittest.TestCase):

    def setUp(self) -> None:
        self.path = Path("tests/sample.mp4")
        self.stem = "sample"
        self.reader = video.Reader(self.path)

    def test_is_open(self):
        self.assertTrue(self.reader.is_open())

    def test_read(self):
        frame = self.reader.read()
        self.assertIsNotNone(frame)

    def test_fps(self):
        self.assertIsInstance(self.reader.fps, float)

    def test_name(self):
        self.assertEqual(self.reader.name, str(self.path))
        self.assertEqual(self.path.stem, self.stem)

    def test_frame_count(self):
        self.assertIsInstance(self.reader.frame_count, int)
        self.assertEqual(self.reader.frame_count, 0)
        _ = self.reader.read()
        self.assertEqual(self.reader.frame_count, 1)

    def test_release(self):
        self.reader.release()
        self.assertFalse(self.reader.is_open())
        
    def tearDown(self) -> None:
        self.reader.release()


class TestWriter(unittest.TestCase):

    def setUp(self) -> None:
        self.path_in = Path("tests/sample.mp4")
        self.path_out = Path("tests/sample_out.mp4")
        self.reader = video.Reader(self.path_in)
        self.writer = video.Writer(self.reader)

    def test_update_props(self):
        self.assertEqual(self.writer.name, str(self.path_out))
        self.assertEqual(self.writer.width, self.reader.width)
        self.assertEqual(self.writer.height, self.reader.height)
        self.assertEqual(self.writer.fps, self.reader.fps)
        self.assertEqual(self.writer.ext, self.path_in.suffix)

    def test_write(self):
        self.assertTrue(self.writer.is_open())
        self.writer.write(self.reader.read())

        self.assertTrue(self.path_out.exists())

    def test_release(self):
        self.writer.release()
        self.assertFalse(self.writer.is_open())

    def tearDown(self) -> None:
        self.reader.release()
        self.writer.release()
        self.path_out.unlink()


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
