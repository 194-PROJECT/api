# NOTE: Table names are in singular form, except for a few exceptions like 'users' and 'groups'
#       since these are reserved keywords in a lot of SQL databases.
from .asset_image import AssetImage # noqa: F401
from .asset import Asset # noqa: F401
from .class_schedule import ClassSchedule # noqa: F401
from .classes import Class # noqa: F401
from .course import Course # noqa: F401
from .department import Department # noqa: F401
from .equipment_availability import EquipmentAvailability # noqa: F401
from .equipment_image import EquipmentImage # noqa: F401
from .equipment import Equipment # noqa: F401
from .group_user import GroupUser # noqa: F401
from .groups import Group # noqa: F401
from .program import Program # noqa: F401
from .reservation_equipment import ReservationEquipment # noqa: F401
from .reservation import Reservation # noqa: F401
from .semester import Semester # noqa: F401
from .session import Session # noqa: F401
from .student import Student # noqa: F401
from .users import User  # noqa: F401
