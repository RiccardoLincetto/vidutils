"""Artifacts module.

This module defines the Artifact class and its subclasses, which are used to represent the outputs of a generic image
processing pipeline.
"""

import abc

from numpy.typing import ArrayLike
from pydantic import BaseModel


class Artifact(BaseModel, metaclass=abc.ABCMeta):
    """Base class for artifacts.

    This class is a subclass of `pydantic.BaseModel` and it represents the class to inherit from to define custom
    artifacts. It is an abstract class because it does not define the `draw` method, which is dependant on the type of
    data represented with the class, which is entirely defined in the subclasses. The choice of using `pydantic` over
    `dataclasses` is due to the features of input validation and serialization/deserialization to JSON. In fact, one of
    the main purposes of this class is to be able to serialize the artifacts to JSON and deserialize them back, so that
    a player can read them from a file and draw them on the frames easily.
    """

    @abc.abstractmethod
    def draw(self, frame: ArrayLike) -> ArrayLike:
        """Draw the artifact on the given frame."""
        ...
