#!./venv/bin/python

from typing import Any

import imutils.text
import numpy as np

from vidutils import procs
from vidutils import script
from vidutils import video

# Input requires to be passed from CLI.
parser = script.ArgumentParser()
parser.add_io_group()
args = parser.parse_args()


# Create Player.
capture = video.Capture(args.source, args.input)
player = video.Player(capture, algorithm=procs.Algorithm(), display=args.display)

# Loop.
player.loop()
