import unittest

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
