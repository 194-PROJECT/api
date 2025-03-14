from typing import Optional
from database.model.reservation import Reservation
from database.postgres.query import QueryExecutor
from sqlalchemy import TextClause, insert, select, update, delete
from sqlalchemy.dialects import postgresql

from src.dto.reservation.reservation_dto import ReservationDTO

class ReservationRepository:
    @staticmethod
    def create_reservation(reservation: ReservationDTO) -> ReservationDTO:
        query = (
            insert(Reservation)
            .values(
                user_id=reservation.user_id,
                admin_id=reservation.admin_id,
                group_id=reservation.group_id,
                accepted=reservation.accepted,
                returned=reservation.returned,
                reason=reservation.reason,
                admin_note=reservation.admin_note,
                return_note=reservation.return_note,
                return_date=reservation.return_date,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return ReservationDTO(**data) if data else None

    @staticmethod
    def get_reservation(id: int) -> Optional[ReservationDTO]:
        query = select(Reservation).where(Reservation.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return ReservationDTO(**data) if data else None

    @staticmethod
    def get_reservations(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ReservationDTO]]:
        query = select(Reservation).order_by(order_by_clause)

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [ReservationDTO(**reservation) for reservation in data] if data else None

    @staticmethod
    def update_reservation(id: int, reservation: ReservationDTO) -> ReservationDTO:
        query = (
            update(Reservation)
            .where(Reservation.id == id)
            .values(
                user_id=reservation.user_id,
                admin_id=reservation.admin_id,
                group_id=reservation.group_id,
                accepted=reservation.accepted,
                returned=reservation.returned,
                reason=reservation.reason,
                admin_note=reservation.admin_note,
                return_note=reservation.return_note,
                return_date=reservation.return_date,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return ReservationDTO(**data) if data else None

    @staticmethod
    def delete_reservation(id: int) -> None:
        query = (
            delete(Reservation)
            .where(Reservation.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_reservations_by_id(ids: list[int]) -> None:
        query = (
            delete(Reservation)
            .where(Reservation.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
