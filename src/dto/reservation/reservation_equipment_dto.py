from datetime import datetime
from core.dto_base import DTO
from typing import Optional

from src.dto.equipment.equipment_dto import EquipmentDTO
from src.dto.equipment.equipment_item_dto import EquipmentItemDTO
from src.dto.reservation.reservation_dto import ReservationDTO
from src.enum.reservation_equipment.mishandle_type_enum import MishandleTypeEnum

class ReservationEquipmentDTO(DTO):
    id: Optional[int] = 0
    reservation_id: int
    equipment_id: Optional[int] = None
    equipment_item_id: Optional[int] = None
    returned: Optional[bool] = None
    mishandled: Optional[bool] = None
    mishandle_type: Optional[MishandleTypeEnum] = None
    mishandle_description: Optional[str] = None
    data_requested: Optional[bool] = None
    data_received: Optional[bool] = None
    data_request_description: Optional[str] = None
    data_request_date: Optional[datetime] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    admin_note: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    reservation: Optional[ReservationDTO] = None
    equipment: Optional[EquipmentDTO] = None
    equipment_item: Optional[EquipmentItemDTO] = None

class ReservationRequestEquipmentItemDTO(DTO):
    id: int
    items: list[int]
