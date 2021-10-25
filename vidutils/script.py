# Scripting utilities
# This module contains utility classes and functions, useful for scripting.

import argparse
import enum
import logging


class ArgumentParser(argparse.ArgumentParser):
    """
    argparse.ArgumentParser with extended capabilities for videos.

    This class adds by default some arguments related to the following groups:
    - input/output: input file selection, output file selection, display and logging;
    - camera specs: camera physical parameters, like frame size and frames per second;
    """

    def add_io_group(self) -> None:
        """Enable arguments group for input/output."""
        # Input
        self.input = self.add_argument_group(
            'input arguments',
            'select the input video.')
        self.input.add_argument('-i', '--input', type=str,
                                help='video path or camera index (opencv convention)')
        # Output
        self.output = self.add_argument_group(
            'output arguments',
            'specify which type of output is desired.')
        self.output.add_argument('-d', '--display', action='store_true', default=False,
                                 help='enable real-time window display')
        self.output.add_argument('-s', '--save', type=str,
                                 help='save video to output file')
        self.output.add_argument('-l', '--log', type=str,
                                 help='log result to file')

    def add_camera_group(self) -> None:
        """Enable arguments group for camera specifications."""
        self.cam = self.add_argument_group(
            'camera', 'information on camera output.')
        self.cam.add_argument('-x', '--width', type=int, default=0,
                              help='frame width')
        self.cam.add_argument('-y', '--height', type=int, default=0,
                              help='frame height')
        self.cam.add_argument('-c', '--channels', type=int, default=3, choices=[1, 3],
                              help='color channels')
        self.cam.add_argument('-f', '--fps', type=int, default=30,
                              help='frames-per-second')

    def parse_args(self, *args, **kwargs):
        """Parse arguments and fix input."""
        arguments = super(ArgumentParser, self).parse_args(*args, **kwargs)
        # Use single variable to distinguish between source types
        try:
            arguments.input = int(arguments.input)
            logging.debug("parsed input as integer")
        except ValueError:
            logging.debug("parsed input as str")
        return arguments


@enum.unique
class Key(enum.Enum):
    """ # Keyboard inputs
    List of keyboard inputs accepted by the player. Keys that are not inserted here will
    trigger a logging.ERROR, because the process won't be able to parse the raw value into
    a Key, and thus into a command.
    """
    NOINPUT = -1
    ESC = 27
    SPACEBAR = 32
    Q = ord('q')
    S = ord('s')
