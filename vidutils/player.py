import logging
from typing import Callable

from vidutils.primitives import Frame, Reader, Writer


class Player:
    def __init__(self, reader: Reader, algorithm: Callable[[Frame], Frame], writer: Writer) -> None:
        self.reader: Reader = reader
        self.algorithm: Callable = algorithm
        self.writer: Writer | None = writer

    def _step(self) -> None:
        try:
            frame: Frame = self.reader.read()
        except EOFError:
            logging.info("End of file reached")
            self.close()
        else:
            frame: Frame = self.algorithm(frame)
            self.writer.write(frame)

    def close(self) -> None:
        self.reader.release()
        self.writer.release()

    def play(self) -> None:
        while self.reader.isOpened():
            self._step()
