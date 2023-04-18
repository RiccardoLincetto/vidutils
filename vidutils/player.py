from typing import Callable

from vidutils.primitives import Frame, Reader, Writer


class Player:
    def __init__(self, reader: Reader, algorithm: Callable[[Frame], Frame], writer: Writer = None) -> None:
        self.reader: Reader = reader
        self.algorithm: Callable = algorithm
        self.writer: Writer | None = writer

    def _step(self) -> None:
        frame = Frame(self.reader.read())
        frame = self.algorithm(frame)
        if self.writer is not None:
            self.writer.write(frame)

    def close(self) -> None:
        self.reader.release()
        if self.writer is not None:
            self.writer.release()

    def play(self) -> None:
        while self.reader.isOpened():
            self._step()
