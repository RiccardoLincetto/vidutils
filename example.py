#!./venv/bin/python

import logging

import cv2 as cv
import numpy as np

from src.vidutils import procs
from src.vidutils import script
from src.vidutils import video

# Input requires to be passed from CLI.
parser = script.ArgumentParser()
parser.add_io_group()
parser.add_logging_group()
args = parser.parse_args()

# Set logging.
# TODO consider moving to script module (maybe inside argument parsing?)
logging.basicConfig(
    level=args.log_level, format="[%(asctime)s]:%(module)s:%(levelname)s: %(message)s", filename=args.log_file
)


# %% Option 1
# Processing is set as a class extending procs.IAlgorithm interface.
class CannyEdge(procs.IAlgorithm):
    def __init__(self, run_args: list, run_kwargs: dict = {}, plot_args: list = [], plot_kwargs: dict = {}) -> None:
        """Instantiate CannyEdge detector parameters."""
        self.run_args = run_args
        self.run_kwargs = run_kwargs
        self.plot_args = plot_args
        self.plot_kwargs = plot_kwargs

    def run(self, frame: np.ndarray, th1, th2) -> bool:
        """Run Canny edge detection."""
        self.edges = cv.Canny(frame, th1, th2)
        return self.edges is not None

    def plot(self, frame: np.ndarray, *args, **kwargs) -> np.ndarray:
        """Plot results."""
        return self.edges


# Algorithm instantiation.
algorithm = CannyEdge(run_args=[100, 50])


# %% Option 2
# Processing class is instantiated directly from opencv function.
# It is still necessary to specify how to plot the results:
# `plot_func` is being passed the argument `result`, which is te output of `run_func`
def annotate(frame, result=None):
    return result


# %% Loop over
# Algorith instantiation.
algorithm = procs.AlgorithmFromFuncs(run_func=cv.Canny, run_args=[100, 50], plot_func=annotate)

# Create Player.
player = video.Player(video.Reader(args.input), algorithm=algorithm, display=args.display)

# Loop.
player.loop()
