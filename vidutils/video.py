# Video application
# This module contains the main tools for video captures and playback.

import logging
import sys
from pathlib import Path
from time import sleep

import cv2 as cv
import vidsz.opencv

from .procs import IAlgorithm
from .script import Key


class Reader(vidsz.opencv.Reader):
    """# Video Reader
    This class is a wrapper to vidsz.opencv.Reader class.
    """

    pass


class Writer(vidsz.opencv.Writer):
    """# Video Writer
    This class is a wrapper to vidsz.opencv.Writer class.
    """

    pass


class Player:
    """# Video Player
    This tool is based on opencv backend and allows to:
    - read video streams/files;
    - process video frame-by-frame;
    - display annotations on top of frames;
    - write video output;
    - (TODO) log to console or to file.
    """

    def __init__(
        self,
        reader: Reader,
        algorithm: IAlgorithm = None,
        writer: Writer = None,
        display: bool = False,
        log: bool = True,
        no_wait: bool = True,
    ) -> None:
        """##  Video player
        Instantiate a video player object with the passed configuration.

        :param capture: capture for the actual video source;
        :param algorithm: algorithm for frame-by-frame processing. It must implement the functions `run()` and `plot()`;
            NOTE passing the algorithm here means that the player does not support switching algorithm at runtime.
            This moves the complexity towards the algorithm side.
        :param writer: opencv video writer;
        :param display: whether to show the video being processed;
        :param log: (TODO)
        :param no_wait: whether to proceed to next frame, without waiting the time needed to play output video with the
            same FPS of input.
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
        self.cap = reader

        # Processing
        self.proc = algorithm

        # Output
        self.out = writer
        self.display = display
        # TODO self.logs = log

        # Playback state
        self.is_paused = False
        self.input_wait_time = 1  # [ms]
        self.no_wait = no_wait

    def loop(self) -> None:
        """## Main loop function
        This method iterates over the entire video, or indefinitely in the case of streams.
        If an algorithm is passed to the player's constructor, its methods will be applied to each frame read.

        NOTE currently the player keeps in memory only a single frame. If more (past) frames are needed,
        a scheme for saving the required frames is to be implemented within the Algorithm class.
        """
        logging.info("starting main loop.")

        while self.cap.is_open():
            # Get cycle start time, to match processing frequency to input FPS.
            if not self.no_wait:
                start_cycle = cv.getTickCount()

            if not self.is_paused:
                frame = self.cap.read()

                # Processing
                if self.proc is not None:
                    res, dt_proc = self.proc.run(frame, *self.proc.run_args, **self.proc.run_kwargs)

                # Visualization
                if self.display or self.out is not None:
                    # Algorithm annotations
                    if res:
                        frame, _ = self.proc.plot(frame, *self.proc.plot_args, **self.proc.plot_kwargs)
                    # Player annotations
                    cv.putText(
                        frame,
                        f"Processing time [ms]: {dt_proc * 1e3:.3f}",
                        (10, 20),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                        lineType=cv.LINE_AA,
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
                    sleep(1 / self.cap.fps - (cv.getTickCount() - start_cycle) / cv.getTickFrequency())
                except ValueError:  # waiting time is negative
                    logging.debug(f"processing time slower than real-time input at {self.cap.fps} FPS")
                    continue

    def process_keyboard_input(self, wait_time: int = 1) -> None:
        """## Keyboard input processing
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
                filename = Path(f"./output/{self.cap.name}_{self.cap.frame_count}.png")
                filename.parent.mkdir(parents=True, exist_ok=True)
                cv.imwrite(str(filename), self.frame)

        except ValueError:
            logging.error(f"ignoring input key {k}: not implemented.")

    def close(self) -> None:
        """## Player closure
        Release input stream, output and display.
        """
        self.cap.release()
        if self.out is not None:
            self.out.release()
        cv.destroyAllWindows()
