# Scripting utilities
# This module contains utility classes and functions, useful for scripting.

import argparse

# TODO check if better relative or absolute import.
# from vidutils.video import Source
from .video import Source


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
            'mutually exclusive group, used to select the type and specify the video source.')
        self.input = self.input.add_mutually_exclusive_group(required=True)
        self.input.add_argument('-v', '--video-file', type=str,
                                help='video filename')
        self.input.add_argument('-i', '--camera-index', type=int,
                                help='camera index')
        self.input.add_argument('-u', '--stream-url', type=str,
                                help='network stream url')
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
        # Use single variable to distinguish between source types.
        if arguments.video_file is not None:
            arguments.source = Source.FILE
            arguments.input = arguments.video_file
        elif arguments.camera_index is not None:
            arguments.source = Source.CAMERA
            arguments.input = arguments.camera_index
        elif arguments.stream_url is not None:
            arguments.source = Source.STREAM
            arguments.input = arguments.stream_url
        return arguments
