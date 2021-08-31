import sys
import unittest

from vidutils import script
from vidutils.video import Source


class TestArgumentParser(unittest.TestCase):
    """Tests for script.ArgumentParser class."""

    def setUp(self):
        self.parser = script.ArgumentParser()
        self.parser.add_io_group()
        self.parser.add_camera_group()

    def test_file_input(self):
        sys.argv[1:] = ["--video-file=video.mp4"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.video_file, str)
        self.assertEqual(args.video_file, "video.mp4")
        self.assertEqual(args.source, Source.FILE)

    def test_camera_input(self):
        sys.argv[1:] = ["--camera-index=0"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.camera_index, int)
        self.assertEqual(args.camera_index, 0)
        self.assertEqual(args.source, Source.CAMERA)

    def test_stream_input(self):
        sys.argv[1:] = ["--stream-url=rtp://ip:port"]
        args = self.parser.parse_args()
        self.assertIsInstance(args.stream_url, str)
        self.assertEqual(args.stream_url, "rtp://ip:port")
        self.assertEqual(args.source, Source.STREAM)

