from typing import Any, Callable

import cv2
from numpy.typing import ArrayLike

from vidutils.artifacts import Artifact


class Looper:
    def __init__(
        self,
        reader: cv2.VideoCapture,
        processor: Callable[[Any], Any],
        preprocessor: Callable[[ArrayLike], Any] = None,
        postprocessor: Callable[[Any], list[Artifact]] = None,
        writer: cv2.VideoWriter = None,
    ) -> None:
        self.reader: cv2.VideoCapture = reader
        self.writer: cv2.VideoWriter = writer
        # TODO validate image processing pipeline
        self.preprocessor: Callable[[ArrayLike], Any] = preprocessor
        self.processor: Callable[[Any], Any] = processor
        self.postprocessor: Callable[[Any], list[Artifact]] = postprocessor

    def step(self):
        ok, frame = self.reader.read()

        if not ok:
            raise RuntimeError("Failed to read frame from video capture device")

        input: Any = self.preprocessor(frame) if self.preprocessor is not None else frame
        output: Any = self.processor(input)
        artifacts: list[Artifact] = self.postprocessor(output) if self.postprocessor is not None else output
        if artifacts:
            with open("artifacts.txt", "a") as f:
                [print(artifact, file=f) for artifact in artifacts]
            if self.writer:
                self.writer.write(frame)

    def loop(self):
        while self.reader.isOpened():
            self.step()
