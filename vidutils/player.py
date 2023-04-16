from vidutils.primitives import Frame, Reader, Writer


class Player:
    def __init__(self, reader: Reader, writer: Writer = None) -> None:
        self.reader: Reader = reader
        self.writer: Writer | None = writer

    def _step(self) -> None:
        frame = Frame(self.reader.read())
        if self.writer is not None:
            self.writer.write(frame)

    def close(self) -> None:
        self.reader.release()
        if self.writer is not None:
            self.writer.release()

    def play(self) -> None:
        while self.reader.isOpened():
            self._step()
