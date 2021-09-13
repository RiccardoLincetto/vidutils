import sys
import unittest

from vidutils import script
from vidutils.video import Source


class TestArgumentParser(unittest.TestCase):
    """Tests for script.ArgumentParser class."""

    @classmethod
    def setUpClass(cls):
        cls.parser = script.ArgumentParser()
        cls.parser.add_io_group()
        cls.parser.add_camera_group()

    def test_file_input(self):
        sys.argv[1:] = ["--video-file=video.mp4"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.video_file, str)
        self.assertEqual(args.input, "video.mp4")
        self.assertIs(args.source, Source.FILE)

    def test_camera_input(self):
        sys.argv[1:] = ["--camera-index=0"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.camera_index, int)
        self.assertEqual(args.input, 0)
        self.assertIs(args.source, Source.CAMERA)

    def test_stream_input(self):
        sys.argv[1:] = ["--stream-url=rtp://ip:port"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.stream_url, str)
        self.assertEqual(args.input, "rtp://ip:port")
        self.assertIs(args.source, Source.STREAM)
