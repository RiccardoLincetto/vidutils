# Processing module
# Here are all classes related to video processing.

import abc
from typing import Callable

import numpy as np

from .utils import logged, timed


class IAlgorithm(metaclass=abc.ABCMeta):
    """# Processing algorithm interface
    This class represents the public interface of an algorithm for it to be called within video.Player.
    Implement this interface, or use a predefined derived class, when passing an algorithm to the video.Player.
    ## Rationale
    The purpose of this interface is to make sure that classes implementing it can be used with video.Player.
    This means to guarantee calls to `run()` and `plot()`.
    """

    @abc.abstractmethod
    def run(self, frame: np.ndarray, *args, **kwargs) -> bool:
        """## Run algorithm
        Execute the algorithm on a single frame.

        NOTE: parameters for functions called here can be saved in run_args and run_kwargs.

        :param frame: image on which the algorithm is run.
        """
        ...

    @abc.abstractmethod
    def plot(self, frame: np.ndarray, *args, **kwargs) -> np.ndarray:
        """## Plot results
        Annotate video output with processing results.

        :param frame: image on which annotations are drawn;
        :return: image to be displayed.
        """
        ...


class AlgorithmFromFuncs(IAlgorithm):
    """# Processing algorithm
    Turn single processing and plotting functions into an Algorithm class, compatible with video.Player.
    Functions are passed as callable objects, method parameters as args and kwargs.
    Both are fixed at instantiation, so they are kept constant throughout the execution.
    ## Example usage
    Assuming there are two function, one for processing and the other for plotting:
    ``` python
    def process(frame: np.ndarray, *args, **kwargs) -> bool:
        ...
        return True

    def annotate(frame: np.ndarray, *args, result=None, **kwargs) -> np.ndarray:
        ...
        return frame
    ```
    instantiate this class as:
    ``` python
    algo = Algorithm(
        process,
        process_args,
        process_kwargs,
        annotate,
        annotate_args,
        annotate_kwargs
    )
    ```
    where args and kwargs are passed as lists and dicts, unpacked directly into the callable object.
    """

    def __init__(
        self,
        run_func: Callable = None,
        run_args: list = [],
        run_kwargs: dict = {},
        plot_func: Callable = None,
        plot_args: list = [],
        plot_kwargs: dict = {},
    ) -> None:
        """## Processing algorithm
        Provide the constructor with `run()` and `plot()` methods and their parameters.

        `run()` method is a hook to `run_func(frame, *run_args, **run_kwargs)`

        `plot()` method is a hook to `plot_func(frame, *plot_args, **plot_kwargs)`

        :param run_func: function used for processing;
        :param run_args: arguments for `run()` method;
        :param run_kwargs: keyword arguments for `run()` method;
        :param plot_func: function used for processing;
        :param plot_args: arguments for `plot()` method;
        :param plot_kwargs: keyword arguments for `plot()` method;
        """
        # Run function
        self.run_func = run_func
        self.run_args = run_args
        self.run_kwargs = run_kwargs
        # Plot function
        self.plot_func = plot_func
        self.plot_args = plot_args
        self.plot_kwargs = plot_kwargs

    @logged
    @timed
    def run(self, frame: np.ndarray, *args, **kwargs) -> bool:
        """## Run algorithm
        Execute the algorithm on a single frame.

        :param frame: image on which the algorithm is run.
        """
        self.plot_kwargs["result"] = self.run_func(frame, *self.run_args, **self.run_kwargs)
        return self.plot_kwargs["result"] is not None

    @logged
    @timed
    def plot(self, frame: np.ndarray, *args, **kwargs) -> np.ndarray:
        """## Plot results
        Annotate video output with processing results.

        :param frame: image on which annotations are displayed.
        """
        return self.plot_func(frame, *self.plot_args, **self.plot_kwargs)
