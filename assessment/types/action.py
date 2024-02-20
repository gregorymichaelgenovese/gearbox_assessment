from enum import Enum


class Action(Enum):
    """Actions the driver can take"""

    REVERSE = -1
    NEUTRAL = 0
    PARK = 1
    DRIVE = 2
    MANUAL = 3
    UP = 4
    DOWN = 5
