import logging
from typing import Callable

from vidutils.primitives import Frame, Reader, Writer


class Player:
    def __init__(self, reader: Reader, algorithm: Callable[[Frame], Frame], writer: Writer) -> None:
        self.reader: Reader = reader
        self.algorithm: Callable = algorithm
        self.writer: Writer = writer

    def _step(self) -> None:
        ok, frame = self.reader.read()
        if ok:
            frame = Frame(frame)
            frame: Frame = self.algorithm(frame)
            self.writer.write(frame)
        else:
            logging.info("End of file reached")
            self.close()

    def close(self) -> None:
        self.reader.release()
        self.writer.release()
        logging.warning("Video player closed")

    def play(self) -> None:
        while self.reader.isOpened():
            self._step()
