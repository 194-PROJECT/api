from typing import Optional
from src.dto.reservation.reservation_dto import ReservationDTO
from src.repository.reservation.reservation_repository import ReservationRepository

class ReservationHandler:
    @staticmethod
    def create_reservation(reservation: ReservationDTO) -> Optional[ReservationDTO]:
        return ReservationRepository.create_reservation(reservation)

    @staticmethod
    def get_reservation(id: int) -> Optional[ReservationDTO]:
        return ReservationRepository.get_reservation(id)

    @staticmethod
    def get_reservations(
        limit: int,
        offset: int,
        order_by_clause: Optional[str] = None,
        where_clause: Optional[str] = None,
    ) -> Optional[list[ReservationDTO]]:
        return ReservationRepository.get_reservations(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def update_reservation(id: int, reservation: ReservationDTO) -> Optional[ReservationDTO]:
        return ReservationRepository.update_reservation(id, reservation)

    @staticmethod
    def delete_reservation(id: int) -> None:
        ReservationRepository.delete_reservation(id)

    @staticmethod
    def delete_reservations_by_id(ids: list[int]) -> None:
        ReservationRepository.delete_reservations_by_id(ids)
