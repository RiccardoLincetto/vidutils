H: int = 1  # height (set to 1 for testing)
W: int = 1  # width (set to 1 for testing)

GOOD_SHAPES = ((H, W), (H, W, 1), (H, W, 3))
BAD_SHAPES = (
    (H),
    (H, W, 2),
    (H, W, 4),
    (H, W, 1, 1),
)
