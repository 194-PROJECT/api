from typing import Optional, List

from sqlalchemy import TextClause
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO
from src.repository.reservation.reservation_equipment_repository import ReservationEquipmentRepository

class ReservationEquipmentHandler:
    @staticmethod
    def get_reservation_equipment(id: int) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.get_reservation_equipment(id)

    @staticmethod
    def get_reservation_equipments(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause] = None,
        where_clause: Optional[TextClause] = None,
        reservation_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        return ReservationEquipmentRepository.get_reservation_equipments(
            limit=limit,
            offset=offset,
            order_by_clause=order_by_clause,
            where_clause=where_clause,
            reservation_id=reservation_id,
        )
    
    @staticmethod
    def get_reservation_equipments_with_data_request(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause] = None,
        where_clause: Optional[TextClause] = None,
        reservation_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        return ReservationEquipmentRepository.get_reservation_equipments_with_data_request(
            limit=limit,
            offset=offset,
            order_by_clause=order_by_clause,
            where_clause=where_clause,
            reservation_id=reservation_id,
        )

    @staticmethod
    def get_reservation_equipment_count(
        where_clause: Optional[TextClause] = None,
        reservation_id: Optional[int] = None,
        with_data_request: bool = False,
    ) -> int:
        return ReservationEquipmentRepository.get_reservation_equipment_count(
            where_clause=where_clause,
            reservation_id=reservation_id,
            with_data_request=with_data_request,
        )

    @staticmethod
    def add_reservation_equipment(reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.add_reservation_equipment(reservation_equipment)

    @staticmethod
    def update_reservation_equipment(id: int, reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.update_reservation_equipment(id, reservation_equipment)

    @staticmethod
    def delete_reservation_equipment(id: int) -> None:
        return ReservationEquipmentRepository.delete_reservation_equipment(id)
