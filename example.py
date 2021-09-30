#!./venv/bin/python

from typing import Any

import cv2 as cv
import numpy as np

from vidutils import procs
from vidutils import script
from vidutils import video

# Input requires to be passed from CLI.
parser = script.ArgumentParser()
parser.add_io_group()
args = parser.parse_args()


# Processing is set as a class extending procs.Algorithm interface.
class CannyEdge(procs.IAlgorithm):

    def __init__(self, run_args, run_kwargs) -> None:
        self.run_args = run_args
        self.run_kwargs = run_kwargs

    def run(self, frame: np.ndarray) -> bool:
        self.edges = cv.Canny(frame, *self.run_args, **self.run_kwargs)
        return True

    def plot(self, frame: np.ndarray) -> np.ndarray:
        return self.edges


algorithm = CannyEdge(
    run_args=[50, 10],
    run_kwargs={}
)

# Create Player.
capture = video.Capture(args.source, args.input)
player = video.Player(capture, algorithm=algorithm, display=args.display)

# Loop.
player.loop()
