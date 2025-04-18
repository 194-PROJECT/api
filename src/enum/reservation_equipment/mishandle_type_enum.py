from enum import Enum

class MishandleTypeEnum(str, Enum):
    MINOR_DAMAGE = "minor_damage"
    NON_FUNCTIONAL = "non_functional"
    LOST = "lost"
    OTHER = "other"
