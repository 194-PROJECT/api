from typing import Optional

from sqlalchemy import TextClause
from src.dto.reservation.reservation_dto import ReservationDTO
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO, ReservationRequestEquipmentItemDTO
from src.repository.reservation.reservation_equipment_repository import ReservationEquipmentRepository
from src.repository.reservation.reservation_repository import ReservationRepository

class ReservationHandler:
    @staticmethod
    def create_reservation(
        reservation: ReservationDTO,
        equipments: list[ReservationRequestEquipmentItemDTO],
    ) -> Optional[ReservationDTO]:
        reservation = ReservationRepository.create_reservation(reservation)
        for equipment in equipments:
            for item_id in equipment.items:
                reservation_equipment = ReservationEquipmentDTO(
                    reservation_id=reservation.id,
                    equipment_id=equipment.id,
                    equipment_item_id=item_id,
                )
                ReservationEquipmentRepository.add_reservation_equipment(reservation_equipment)
        
        return reservation

    @staticmethod
    def get_reservation(id: int) -> Optional[ReservationDTO]:
        return ReservationRepository.get_reservation(id)

    @staticmethod
    def get_reservations(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause] = None,
        where_clause: Optional[TextClause] = None,
    ) -> Optional[list[ReservationDTO]]:
        return ReservationRepository.get_reservations(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def get_user_reservations(
        user_id: int,
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause] = None,
        where_clause: Optional[TextClause] = None,
    ) -> Optional[list[ReservationDTO]]:
        return ReservationRepository.get_user_reservations(user_id, limit, offset, order_by_clause, where_clause)

    @staticmethod
    def get_reservation_count(
        where_clause: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> int:
        return ReservationRepository.get_reservation_count(
            where_clause=where_clause,
            user_id=user_id,
        )

    @staticmethod
    def update_reservation(id: int, reservation: ReservationDTO) -> Optional[ReservationDTO]:
        return ReservationRepository.update_reservation(id, reservation)

    @staticmethod
    def delete_reservation(id: int) -> None:
        ReservationRepository.delete_reservation(id)

    @staticmethod
    def delete_reservations_by_id(ids: list[int]) -> None:
        ReservationRepository.delete_reservations_by_id(ids)
