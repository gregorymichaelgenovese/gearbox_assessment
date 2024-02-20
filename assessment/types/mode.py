from enum import Enum


class Mode(Enum):
    """Automatic transmission states"""

    REVERSE = -1
    NEUTRAL = 0
    PARK = 1
    DRIVE = 2
    MANUAL = 3
