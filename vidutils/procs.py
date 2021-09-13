# Processing module
# Here are all classes related to video processing.

import numpy as np


class Algorithm:
    """ # Processing algorithm
    This class represents the public interface of an algorithm for it to be called within video.Player.
    Please extend this class when passing an algorithm to the video.Player.
    """

    def __init__(self, run_kwargs: dict = {}, plot_kwargs: dict = {}) -> None:
        """ ## Processing algorithm
        Provide the constructor with `run()` and `plot()` methods parameters as separate dictionaries,
        which will be passed as keyword arguments.

        :param run_kwargs: keyword arguments for `run()` method
        :param plot_kwargs: keyword arguments for `plot()` method
        """
        # Dictionaries for specifing the behaviour of run() and plot() functions.
        self.run_kwargs = run_kwargs
        self.plot_kwargs = plot_kwargs

    def run(self, frame: np.ndarray, **kwargs):
        """ ## Run algorithm
        Execute the algorithm on a single frame.

        :param frame: image on which the algorithm is run;
        :param **kwargs: algorithm specific arguments.
        """
        pass

    def plot(self, frame: np.ndarray, **kwargs):
        """ ## Plot results
        Annotate video output with processing results.

        :param frame: image on which annotations are displayed;
        :param **kwargs: plot specific arguments.
        """
        pass
