import sys
import unittest

from vidutils import script


class TestArgumentParser(unittest.TestCase):
    """Tests for script.ArgumentParser class."""

    @classmethod
    def setUpClass(cls):
        cls.parser = script.ArgumentParser()
        cls.parser.add_io_group()
        cls.parser.add_camera_group()

    def test_file_input(self):
        sys.argv[1:] = ["--input=video.mp4"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.input, str)
        self.assertEqual(args.input, "video.mp4")

    def test_camera_input(self):
        sys.argv[1:] = ["--input=0"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.input, int)
        self.assertEqual(args.input, 0)

    def test_stream_input(self):
        sys.argv[1:] = ["--input=rtp://ip:port"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.input, str)
        self.assertEqual(args.input, "rtp://ip:port")
