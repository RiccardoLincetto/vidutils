# Scripting utilities
# This module contains utility classes and functions, useful for scripting.

import argparse
import enum
import logging


class ArgumentParser(argparse.ArgumentParser):
    """
    argparse.ArgumentParser with extended capabilities for videos.

    This class adds by default some arguments related to the following groups:
    - input/output: input file selection, output file selection, display;
    - logging: control over logging options, like level and destination;
    - camera specs: camera physical parameters, like frame size and frames per second;
    """

    def add_io_group(self) -> None:
        """Enable arguments group for input/output."""
        # Input
        self.input = self.add_argument_group("input arguments", "select the input video.")
        self.input.add_argument("-i", "--input", type=str, help="video path or camera index (opencv convention)")
        # Output
        self.output = self.add_argument_group("output arguments", "specify which type of output is desired.")
        self.output.add_argument(
            "-d", "--display", action="store_true", default=False, help="enable real-time window display"
        )
        self.output.add_argument("-o", "--output", type=str, help="save output video to file")

    def add_logging_group(self) -> None:
        """Configure logging options."""
        self.log = self.add_argument_group("logging options", "configure logging level and destination.")
        self.log.add_argument(
            "-s",
            "--log-level",
            "--severity",
            type=str,
            default="warning",
            help="set logging level among {debug, info, warning, error, critical}",
        )
        self.log.add_argument(
            "-l",
            "--log-file",
            type=str,
            default=None,
            help="set logging destination to file. Default (None) is console.",
        )

    def add_camera_group(self) -> None:
        """Enable arguments group for camera specifications."""
        self.cam = self.add_argument_group("camera", "information on camera output.")
        self.cam.add_argument("-x", "--width", type=int, default=0, help="frame width")
        self.cam.add_argument("-y", "--height", type=int, default=0, help="frame height")
        self.cam.add_argument("-c", "--channels", type=int, default=3, choices=[1, 3], help="color channels")
        self.cam.add_argument("-f", "--fps", type=int, default=30, help="frames-per-second")

    def parse_args(self, *args, **kwargs):
        """Parse arguments and fix input."""
        arguments = super(ArgumentParser, self).parse_args(*args, **kwargs)

        # Get input source
        # If input string is convertible to integer, convert it. Otherwise leave it to a string.
        try:
            arguments.input = int(arguments.input) if arguments.input is not None else None
        except ValueError:
            pass

        # Get log-level
        # This piece of code are only for logging level parsing, but they do NOT set the logging configuration.
        # Logging configuration is to be set in the module calling this function.
        # This makes it easier to separate logging to console from logging to filename,
        # in different usages (e.g. testing vs deploying)
        arguments.log_level = getattr(logging, arguments.log_level.upper())

        return arguments


@enum.unique
class Key(enum.Enum):
    """# Keyboard inputs
    List of keyboard inputs accepted by the player. Keys that are not inserted here will
    trigger a logging.ERROR, because the process won't be able to parse the raw value into
    a Key, and thus into a command.
    """

    NOINPUT = -1
    ESC = 27
    SPACEBAR = 32
    Q = ord("q")
    S = ord("s")
