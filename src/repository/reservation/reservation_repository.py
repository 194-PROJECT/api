from typing import Optional
from database.model.classes import Class
from database.model.group_user import GroupUser
from database.model.groups import Group
from database.model.reservation import Reservation
from database.postgres.database import PostgresDatabase
from database.postgres.query import QueryExecutor
from sqlalchemy import TextClause, insert, or_, select, update, delete, orm, func
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
                class_id=reservation.class_id,
                group_id=reservation.group_id,
                start_date=reservation.start_date,
                end_date=reservation.end_date,
                accepted=reservation.accepted,
                claimed=reservation.claimed,
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
        query = select(Reservation).options(
                orm.selectinload(Reservation.user),
                orm.selectinload(Reservation.admin),
                orm.selectinload(Reservation.class_).selectinload(
                    Class.course
                ),
                orm.selectinload(Reservation.group).selectinload(
                    Group.users
                ).selectinload(GroupUser.user),
            ).where(Reservation.id == id)
        
        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().one_or_none()
            return ReservationDTO.model_validate(data) if data else None
        finally:
            session.close()

    @staticmethod
    def get_reservations(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ReservationDTO]]:
        query = select(Reservation).options(
                orm.selectinload(Reservation.user),
                orm.selectinload(Reservation.admin),
                orm.selectinload(Reservation.class_).selectinload(
                    Class.course
                ),
                orm.selectinload(Reservation.group).selectinload(
                    Group.users
                ).selectinload(GroupUser.user),
            ).order_by(order_by_clause)

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        
        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().all()
            return [ReservationDTO.model_validate(reservation) for reservation in data] if data else None
        finally:
            session.close()

    @staticmethod
    def get_user_reservations(
        user_id: int,
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ReservationDTO]]:
        group_res_ids_subq = (
            select(Reservation.id)
            .join(Reservation.group)
            .join(Group.users)
            .where(GroupUser.user_id == user_id)
            .subquery()
        )

        query = (
            select(Reservation)
            .options(
                orm.selectinload(Reservation.user),
                orm.selectinload(Reservation.admin),
                orm.selectinload(Reservation.class_).selectinload(
                    Class.course
                ),
                orm.selectinload(Reservation.group).selectinload(
                    Group.users
                ).selectinload(GroupUser.user),
            )
            .where(
                or_(
                    Reservation.user_id == user_id, # direct reservation owner
                    Reservation.id.in_(select(group_res_ids_subq.c.id))
                )
            )
            .order_by(order_by_clause)
        )

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        
        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().all()
            return [ReservationDTO.model_validate(reservation) for reservation in data] if data else None
        finally:
            session.close()

    @staticmethod
    def get_reservation_count(
        where_clause: Optional[TextClause] = None,
        user_id: Optional[int] = None,
    ) -> int:
        query = select(func.count(Reservation.id).label("count"))

        if where_clause is not None:
            query = query.where(where_clause)
        if user_id is not None:
            query = query.where(Reservation.user_id == user_id)

        query = query.compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return data["count"] if data else 0

    @staticmethod
    def update_reservation(id: int, reservation: ReservationDTO) -> ReservationDTO:
        query = (
            update(Reservation)
            .where(Reservation.id == id)
            .values(
                user_id=reservation.user_id,
                admin_id=reservation.admin_id,
                class_id=reservation.class_id,
                group_id=reservation.group_id,
                start_date=reservation.start_date,
                end_date=reservation.end_date,
                accepted=reservation.accepted,
                claimed=reservation.claimed,
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
