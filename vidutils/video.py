# Video application
# This module contains the main tools for video captures and playback.
# NOTE vidsz has an interesting alternative for video captures and writers.

import logging
import sys
from datetime import datetime
from enum import Enum, auto, unique
from pathlib import Path
from time import sleep
from typing import Any, Tuple, Union

import cv2 as cv
import numpy as np

from .procs import IAlgorithm


@unique
class Source(Enum):
    """ # Video source
    Enumerates the types of input allowed by Capture.
    """
    FILE = auto()
    CAMERA = auto()
    STREAM = auto()


class Capture(cv.VideoCapture):
    """ # Extended capabilities for OpenCV VideoCapture
    This class extends cv.VideoCapture with some methods which are more comfortably called within python.
    The Player class relies on these methods.
    """

    def __init__(self, source: Source, *args, **kwargs) -> None:
        """ ## Video capture
        Read input from files, cameras or network streams.
        The opened video is checked for validity and its properties are inferred from reading the first frame.

        :param source: indicates the type of video source, passed as Source enumeration;
        :param *args: arguments passed to cv.VideoCapture constructor.
            NOTE there needs to be the video source here.
        :param **kwargs: keyword arguments passed to cv.VideoCapture constructor.
        """
        super(Capture, self).__init__(*args, **kwargs)
        assert self.isOpened(), print(f"Failed to open from source: {source}")
        self.source = source

        # Video filename, used as base to save video frames as images
        self.filename = Path(args[0]).stem if self.source is Source.FILE else None

        # Frame shape, inferred from first frame.
        # Note: there is no cv.VideoCapture property for the number of channels.
        frame = self.read()
        self._default_shape = frame.shape
        self._desired_shape = frame.shape
        # Current number of channels, user controllable.
        # self.channels = self._default_shape[-1]

    # Temporal dimension

    def __len__(self) -> int:
        """ ## Video length
        Length of the video input, from CV_CAP_PROP_FRAME_COUNT.
        """
        return int(self.get(cv.CAP_PROP_FRAME_COUNT)) if self.source is Source.FILE else 0

    @property
    def cursor(self) -> int:
        """ ## Frame counter
        Get cursor position. The cursor increases only for files, as the total number of frames is known in advance.
        In the case of streams, it returns always -1, so that when compared to length 0 of streams the condition of
        having a frame next `has_next()` is always true.
        """
        return int(self.get(cv.CAP_PROP_POS_FRAMES)) if self.source is Source.FILE else -1

    @cursor.setter
    def cursor(self, index: int) -> None:
        """ ## Frame counter
        Set cursor position. This is allowed only for video files, to jump between non adjacent frames.

        :param index: frame index to be read next.
        """
        if self.source is Source.FILE:
            if 0 <= index < len(self):
                self.set(cv.CAP_PROP_POS_FRAMES, index)
            else:
                raise IndexError
        else:  # Source.CAMERA or Source.STREAM
            logging.error(f"cannot set cursor for {self.source.value}.")

    @property
    def has_next(self) -> bool:
        """ ## End of file check
        Indicates whether the video has incoming frames to be read/processed.
        Note that for streams, this function relies on the fact that the cursor is always -1
        and the length is always 0, so that the condition is always true.
        """
        return self.cursor < len(self)

    @property
    def fps(self) -> float:
        """ ## Frames per second
        Get input FPS from video capture properties.
        """
        return self.get(cv.CAP_PROP_FPS)

    @fps.setter
    def fps(self, value: Union[int, float]) -> None:
        """ ## Frames per second
        Set input frames per second. Available only for attached cameras.

        NOTE this might influence physically the camera, so it needs to be a supported configuration,
        considering also the frame size.

        :param value: desired frame rate.
        """
        if self.source is Source.CAMERA:
            self.set(cv.CAP_PROP_FPS, value)
        else:  # Source.FILE or Source.STREAM
            logging.error(f"cannot set fps for {self.source.value}.")

    # Spatial dimension

    @property
    def shape(self) -> Tuple[int, int, int]:
        """ ## Frame shape
        Get frame shape, as [height, width, channels].

        NOTE channels currently read-only.
        """
        return int(self.get(cv.CAP_PROP_FRAME_HEIGHT)), \
               int(self.get(cv.CAP_PROP_FRAME_WIDTH)), \
               self._default_shape[2]

    @shape.setter
    def shape(self, new_shape: Tuple[int, int, int]) -> None:
        """ ## Frame shape
        Set desired frame shape.

        NOTE channels currently read-only, except for video cameras.

        :param new_shape: [height, witdh, channels].
        """
        if self.source in (Source.FILE, Source.STREAM):
            # Store values and smooth+resize every new frame.
            # When channel is set, it influences the way frames are read.
            raise NotImplementedError
        elif self.source is Source.CAMERA:
            # Set camera mode to work with desired resolution.
            try:
                self.set(cv.CAP_PROP_FRAME_HEIGHT, new_shape[0])
                self.set(cv.CAP_PROP_FRAME_WIDTH, new_shape[1])
            except Any as e:
                print(f"{e}\nPossibly unsupported frame size.")
                # TODO Store values and smooth+resize every new frame.
        # Color channels are a physical parameter, not electronically controllable.
        # The only supported options are 1 (mono) or 3 (rgb).
        if new_shape[2] in (1, 3):
            pass
            # self.channels = new_shape[2]
        else:
            raise NotImplementedError

    @property
    def is_rgb(self) -> bool:
        """ ## Color camera check
        Whether the capturing sensor supports color images.
        """
        return self._default_shape[2] == 3

    @property
    def is_gray(self) -> bool:
        """ ## Mono camera check
        Whether the capturing sensor is monochromatic.
        """
        return self._default_shape[2] == 1

    # Main methods

    def read(self, frame_index: int = None) -> Union[np.ndarray, None]:
        """ ## Read frame
        Read <frame_index>-th frame.

        :param frame_index: index of the frame to be read.
        """
        if frame_index is not None:
            self.cursor = frame_index
        ret, frame = super(Capture, self).read()
        return frame if ret else None


@unique
class Key(Enum):
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


class Player:
    """ # OpenCV-based simple video player
    This tool is based on opencv backend and allows to:
    - read video streams/files;
    - process video frame-by-frame;
    - display annotations on top of frames;
    - write video output;
    - (TODO) log to console or to file.
    """

    def __init__(self,
                 capture: Capture,
                 algorithm: IAlgorithm = None,
                 writer: cv.VideoWriter = None,
                 display: bool = False,
                 log: bool = True,
                 no_wait: bool = True) -> None:
        """ ##  Video player
        Instantiate a video player object with the passed configuration.

        :param capture: capture for the actual video source;
        :param algorithm: algorithm for frame-by-frame processing. It must implement the functions `run()` and `plot()`;
            NOTE passing the algorithm here means that the player does not support switching algorithm at runtime.
            This moves the complexity towards the algorithm side.
        :param writer: opencv video writer;
        :param display: whether to show the video being processed;
        :param log: (TODO)
        :param no_wait: whether to proceed to next frame, without waiting the time needed to play output video with the same FPS of input.
        """
        # Optional args check
        if algorithm is None and not display:
            logging.critical("aborting; output equals input, but display disabled.")
            sys.exit(0)
        elif algorithm is None and writer is not None:  # (and display) is implied by the else clause
            logging.warning("disabling video writer; no algorithm passed.")
            writer = None
        elif not display and writer is None:
            logging.critical("aborting; no output.")
            sys.exit(0)
        else:
            logging.debug("continuing with proper configuration.")

        # Input
        self.cap = capture

        # Processing
        self.proc = algorithm

        # Output
        # NOTE consider initializing cv.VideoWriter directly inside here, instead of passing an instance.
        # Instantiating here requires knowing frame shape and fps. Condider replicating input ones.
        self.out = writer
        self.display = display
        # self.logs = log

        # Playback state
        self.is_paused = False
        self.input_wait_time = 1  # [ms]
        self.no_wait = no_wait

    def loop(self) -> None:
        """ ## Main loop function
        This method iterates over the entire video, or indefinitely in the case of streams.
        If an algorithm is passed to the player's constructor, its methods will be applied to each frame read.

        NOTE currently the player keeps in memory only a single frame. If more (past) frames are needed,
        a scheme for saving the required frames is to be implemented within the Algorithm class.
        """
        logging.info("starting main loop.")

        while self.cap.isOpened() and self.cap.has_next:

            # Get cycle start time, to match processing frequency to input FPS.
            if not self.no_wait:
                start_cycle = cv.getTickCount()

            if not self.is_paused:
                frame = self.cap.read()

                # Processing
                if self.proc is not None:
                    tick_start_proc = cv.getTickCount()
                    res = self.proc.run(frame)
                    time_proc = (cv.getTickCount() -
                                    tick_start_proc) / cv.getTickFrequency()

                # Visualization
                if self.display or self.out is not None:
                    # Algorithm annotations
                    if self.proc is not None:
                        frame = self.proc.plot(frame)
                    # Player annotations
                    cv.putText(
                        frame,
                        f"Processing FPS: {int(1 / time_proc)}",
                        (10, 20),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                        lineType=cv.LINE_AA
                    )

                    # Display
                    cv.namedWindow("player", cv.WINDOW_NORMAL)
                    cv.imshow("player", frame)

                # Output
                if self.out is not None:
                    self.out.write(frame)

            # Keyboard input processing
            self.process_keyboard_input(self.input_wait_time)

            # When processing is faster than real-time video, if no_wait flag is False,
            # wait for the amount of time necessary to match frame processing frequency to input FPS.
            if not self.no_wait:
                # Time elapsed in seconds:
                # (cv.getTickCount() - start_cycle) / cv.getTickFrequency()
                try:
                    sleep(1 / self.cap.fps - (cv.getTickCount() -
                          start_cycle) / cv.getTickFrequency())
                except ValueError:  # waiting time is negative
                    logging.debug(
                        f"processing time slower than real-time input at {self.cap.fps} FPS")
                    continue

    def process_keyboard_input(self, wait_time: int = 1) -> None:
        """ ## Keyboard input processing
        The method waits for the desired amount of time [ms] for keyboard input,
        and executes the commanded action.

        :param wait_time: time [ms] to be waited for receiving input.
        """
        k = cv.waitKey(wait_time)

        try:
            k = Key(k)

            if k is Key.NOINPUT:
                # This condition does not execute anything, it is just inserted
                # to implement an early-exit strategy for the most common input value.
                pass

            elif k is Key.ESC or k is Key.Q:  # stop player
                self.close()

            elif k is Key.SPACEBAR:  # toggle playback state
                if self.is_paused:
                    self.is_paused = False
                else:
                    self.is_paused = True

            elif k is Key.S:  # save current frame
                filename = Path(f"./output/{self.cap.filename}_{self.cap.cursor}.png") \
                    if self.cap.source is Source.FILE \
                    else Path(f"./output/{str(datetime.now())}.png")
                filename.parent.mkdir(parents=True, exist_ok=True)
                cv.imwrite(str(filename), self.frame)

        except ValueError:
            logging.error(f"ignoring input key {k}: not implemented.")

    def close(self) -> None:
        """ ## Player closure
        Release input stream, output and display.
        """
        self.cap.release()
        if self.out is not None and self.out.isOpened():
            self.out.release()
        cv.destroyAllWindows()
