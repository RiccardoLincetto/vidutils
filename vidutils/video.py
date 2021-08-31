# Video application
# This module contains the main tools for video captures and playback.

from enum import auto, Enum


class Source(Enum):
    FILE = auto()
    CAMERA = auto()
    STREAM = auto()
