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
        limit: Optional[int] = None,
        offset: Optional[int] = None,
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
        user_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        return ReservationEquipmentRepository.get_reservation_equipments_with_data_request(
            limit=limit,
            offset=offset,
            order_by_clause=order_by_clause,
            where_clause=where_clause,
            reservation_id=reservation_id,
            user_id=user_id,
        )

    @staticmethod
    def get_reservation_equipments_with_mishandle(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause] = None,
        where_clause: Optional[TextClause] = None,
        reservation_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        return ReservationEquipmentRepository.get_reservation_equipments_with_mishandle(
            limit=limit,
            offset=offset,
            order_by_clause=order_by_clause,
            where_clause=where_clause,
            reservation_id=reservation_id,
            user_id=user_id,
        )

    @staticmethod
    def get_reservation_equipment_count(
        where_clause: Optional[TextClause] = None,
        reservation_id: Optional[int] = None,
        user_id: Optional[int] = None,
        with_data_request: bool = False,
        with_mishandle: bool = False,
    ) -> int:
        return ReservationEquipmentRepository.get_reservation_equipment_count(
            where_clause=where_clause,
            reservation_id=reservation_id,
            user_id=user_id,
            with_data_request=with_data_request,
            with_mishandle=with_mishandle,
        )

    @staticmethod
    def add_reservation_equipment(reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        return ReservationEquipmentRepository.add_reservation_equipment(reservation_equipment)

    @staticmethod
    def update_reservation_equipment(id: int, reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        print(f"Updating reservation equipment with ID {id} and data {reservation_equipment.model_dump()}")
        return ReservationEquipmentRepository.update_reservation_equipment(id, reservation_equipment)

    @staticmethod
    def delete_reservation_equipment(id: int) -> None:
        return ReservationEquipmentRepository.delete_reservation_equipment(id)
