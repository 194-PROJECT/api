from datetime import datetime
from core.dto_base import DTO

class ReservationEquipmentAvailabilityDTO(DTO):
    start_date: datetime
    end_date: datetime