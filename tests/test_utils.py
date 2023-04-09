import logging
import os
import unittest
from time import sleep

from src.vidutils import utils


class TestTimerWrapper(unittest.TestCase):
    def setUp(self) -> None:
        self.sleep_time = 0.1

    @utils.timed
    def timed_function(self):
        sleep(self.sleep_time)

    def test_timer(self):
        _, dt = self.timed_function()
        self.assertIsInstance(dt, float)
        self.assertGreaterEqual(dt, self.sleep_time)
        # self.assertEqual(1e2 * dt // 1, 1e2 * self.sleep_time // 1)  # heuristic: check first 3 digits


class TestLoggerWrapper(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.filename = os.path.join("tests", "temp.log")
        logging.basicConfig(level=logging.DEBUG, filename=cls.filename, format="TEST %(levelname)s: %(message)s")

    @utils.logged
    def logged_function(self):
        pass

    def test_logger(self):
        self.logged_function()
        self.assertTrue(os.path.isfile(self.filename))
        with open(self.filename, "r") as f:
            lines = f.readlines()
        self.assertIsInstance(lines, list)
        self.assertEqual(len(lines), 1)
        self.assertIsInstance(lines[0], str)
        self.assertEqual(lines[0].rstrip("\n"), f"TEST DEBUG: called {self.logged_function.__name__}")

    def tearDown(self) -> None:
        os.remove(self.filename)
