from typing import Optional, List
from database.model.reservation import Reservation
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.database import PostgresDatabase
from database.postgres.query import QueryExecutor
from sqlalchemy import TextClause, insert, select, delete, update, func, orm
from sqlalchemy.dialects import postgresql

from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO


class ReservationEquipmentRepository:
    @staticmethod
    def get_reservation_equipment(id: int) -> Optional[ReservationEquipmentDTO]:
        query = (
            select(ReservationEquipment)
            .where(ReservationEquipment.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.fetch_one(str(query))
        return ReservationEquipmentDTO(**data) if data else None

    @staticmethod
    def get_reservation_equipments(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
        reservation_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        query = select(ReservationEquipment).limit(limit).offset(offset)
        if order_by_clause is not None:
            query = query.order_by(order_by_clause)
        if where_clause is not None:
            query = query.where(where_clause)
        if reservation_id is not None:
            query = query.where(ReservationEquipment.reservation_id == reservation_id)

        query = query.compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_all(str(query))
        return [ReservationEquipmentDTO(**item) for item in data] if data else None

    @staticmethod
    def get_reservation_equipments_from_reservation(
        reservation_id: int,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        query = (
            select(ReservationEquipment)
            .where(ReservationEquipment.reservation_id == reservation_id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.fetch_all(str(query))
        return [ReservationEquipmentDTO(**item) for item in data] if data else None

    @staticmethod
    def get_reservation_equipments_with_data_request(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
        reservation_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        query = (
            select(ReservationEquipment)
            .options(
                orm.joinedload(ReservationEquipment.reservation).joinedload(Reservation.user),
                orm.joinedload(ReservationEquipment.equipment),
                orm.joinedload(ReservationEquipment.equipment_item),
            )
            .limit(limit)
            .offset(offset)
        )
        if order_by_clause is not None:
            query = query.order_by(order_by_clause)
        if where_clause is not None:
            query = query.where(where_clause)
        if reservation_id is not None:
            query = query.where(ReservationEquipment.reservation_id == reservation_id)
        if user_id is not None:
            query = (
                query
                .join(Reservation, ReservationEquipment.reservation_id == Reservation.id)
                .where(Reservation.user_id == user_id)
            )

        query = query.where(ReservationEquipment.data_requested).order_by(
            ReservationEquipment.data_received.asc(),
            ReservationEquipment.id.desc(),
        )

        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().all()
            return [ReservationEquipmentDTO.model_validate(item) for item in data] if data else None
        finally:
            session.close()

    @staticmethod
    def get_reservation_equipments_with_mishandle(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
        reservation_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List[ReservationEquipmentDTO]]:
        query = (
            select(ReservationEquipment)
            .options(
                orm.joinedload(ReservationEquipment.reservation).joinedload(Reservation.user),
                orm.joinedload(ReservationEquipment.equipment),
                orm.joinedload(ReservationEquipment.equipment_item),
            )
            .limit(limit)
            .offset(offset)
        )
        if order_by_clause is not None:
            query = query.order_by(order_by_clause)
        if where_clause is not None:
            query = query.where(where_clause)
        if reservation_id is not None:
            query = query.where(ReservationEquipment.reservation_id == reservation_id)
        if user_id is not None:
            query = (
                query
                .join(Reservation, ReservationEquipment.reservation_id == Reservation.id)
                .where(Reservation.user_id == user_id)
            )

        query = query.where(ReservationEquipment.mishandled).order_by(
            ReservationEquipment.id.desc(),
        )

        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().all()
            return [ReservationEquipmentDTO.model_validate(item) for item in data] if data else None
        finally:
            session.close()

    @staticmethod
    def get_reservation_equipment_count(
        where_clause: Optional[TextClause] = None,
        reservation_id: Optional[int] = None,
        user_id: Optional[int] = None,
        with_data_request: bool = False,
        with_mishandle: bool = False,
    ) -> int:
        query = select(func.count(ReservationEquipment.id).label("count"))

        if where_clause is not None:
            query = query.where(where_clause)
        if reservation_id is not None:
            query = query.where(ReservationEquipment.reservation_id == reservation_id)
        if user_id is not None:
            query = (
                query
                .join(Reservation, ReservationEquipment.reservation_id == Reservation.id)
                .where(Reservation.user_id == user_id)
            )
        if with_data_request:
            query = query.where(ReservationEquipment.data_requested)
        if with_mishandle:
            query = query.where(ReservationEquipment.mishandled)
        

        query = query.compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return data["count"] if data else 0

    @staticmethod
    def add_reservation_equipment(
        reservation_equipment: ReservationEquipmentDTO,
    ) -> Optional[ReservationEquipmentDTO]:
        query = (
            insert(ReservationEquipment)
            .values(
                reservation_id=reservation_equipment.reservation_id,
                equipment_id=reservation_equipment.equipment_id,
                equipment_item_id=reservation_equipment.equipment_item_id,
                returned=reservation_equipment.returned,
                mishandled=reservation_equipment.mishandled,
                mishandle_type=reservation_equipment.mishandle_type,
                mishandle_description=reservation_equipment.mishandle_description,
                data_requested=reservation_equipment.data_requested,
                data_received=reservation_equipment.data_received,
                data_request_description=reservation_equipment.data_request_description,
                data_request_date=reservation_equipment.data_request_date,
                rating=reservation_equipment.rating,
                comment=reservation_equipment.comment,
                admin_note=reservation_equipment.admin_note,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return ReservationEquipmentDTO(**data) if data else None

    @staticmethod
    def update_reservation_equipment(
        id: int, reservation_equipment: ReservationEquipmentDTO
    ) -> Optional[ReservationEquipmentDTO]:
        query = (
            update(ReservationEquipment)
            .where(ReservationEquipment.id == id)
            .values(
                reservation_id=reservation_equipment.reservation_id,
                equipment_id=reservation_equipment.equipment_id,
                equipment_item_id=reservation_equipment.equipment_item_id,
                returned=reservation_equipment.returned,
                mishandled=reservation_equipment.mishandled,
                mishandle_type=reservation_equipment.mishandle_type,
                mishandle_description=reservation_equipment.mishandle_description,
                data_requested=reservation_equipment.data_requested,
                data_received=reservation_equipment.data_received,
                data_request_description=reservation_equipment.data_request_description,
                data_request_date=reservation_equipment.data_request_date,
                rating=reservation_equipment.rating,
                comment=reservation_equipment.comment,
                admin_note=reservation_equipment.admin_note,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return ReservationEquipmentDTO(**data) if data else None

    @staticmethod
    def delete_reservation_equipment(id: int) -> None:
        query = (
            delete(ReservationEquipment)
            .where(ReservationEquipment.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))
