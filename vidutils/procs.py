# Processing module
# Here are all classes related to video processing.

import abc

import numpy as np


class IAlgorithm(metaclass=abc.ABCMeta):
    """ # Processing algorithm interface
    This class represents the public interface of an algorithm for it to be called within video.Player.
    Implement this interface, or use a predefined derived class, when passing an algorithm to the video.Player.
    ## Rationale
    The purpose of this interface is to make sure that classes implementing it can be used with video.Player.
    This means to guarantee calls to `run()` and `plot()`.
    """

    @abc.abstractmethod
    def run(self, frame: np.ndarray) -> bool:
        """ ## Run algorithm
        Execute the algorithm on a single frame.

        NOTE: parameters for functions called here can be saved in run_args and run_kwargs.

        :param frame: image on which the algorithm is run.
        """
        ...

    @abc.abstractmethod
    def plot(self, frame: np.ndarray) -> np.ndarray:
        """ ## Plot results
        Annotate video output with processing results.

        :param frame: image on which annotations are drawn;
        :return: image to be displayed.
        """
        ...

