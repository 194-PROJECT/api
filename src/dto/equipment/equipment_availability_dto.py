from datetime import datetime, timedelta
from core.dto_base import DTO

class EquipmentAvailabilityDTO(DTO):
    start_time: datetime = datetime.now()
    end_time: datetime = datetime.now() + timedelta(hours=1)
