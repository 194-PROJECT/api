from typing import Optional, List
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO
from src.repository.reservation.reservation_equipment_repository import ReservationEquipmentRepository

class ReservationEquipmentHandler:
    @staticmethod
    def get_reservation_equipment(reservation_id: int) -> Optional[List[ReservationEquipmentDTO]]:
        return ReservationEquipmentRepository.get_reservation_equipment(reservation_id)

    @staticmethod
    def add_reservation_equipment(equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.add_reservation_equipment(equipment)

    @staticmethod
    def delete_reservation_equipment(reservation_id: int, equipment_id: int) -> bool:
        return ReservationEquipmentRepository.delete_reservation_equipment(reservation_id, equipment_id)
