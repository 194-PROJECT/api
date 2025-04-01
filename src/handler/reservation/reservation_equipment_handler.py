from typing import Optional, List
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO
from src.repository.reservation.reservation_equipment_repository import ReservationEquipmentRepository

class ReservationEquipmentHandler:
    @staticmethod
    def get_reservation_equipment(id: int) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.get_reservation_equipment(id)

    @staticmethod
    def get_reservation_equipments(reservation_id: int) -> Optional[List[ReservationEquipmentDTO]]:
        return ReservationEquipmentRepository.get_reservation_equipments(reservation_id)

    @staticmethod
    def add_reservation_equipment(reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.add_reservation_equipment(reservation_equipment)

    @staticmethod
    def update_reservation_equipment(id: int, reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.update_reservation_equipment(id, reservation_equipment)

    @staticmethod
    def delete_reservation_equipment(id: int) -> bool:
        return ReservationEquipmentRepository.delete_reservation_equipment(id)
