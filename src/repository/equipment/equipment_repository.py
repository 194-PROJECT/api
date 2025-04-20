from datetime import datetime
from database.model.equipment_item import EquipmentItem
from database.model.reservation import Reservation
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.database import PostgresDatabase
from database.postgres.query import QueryExecutor
from database.model.equipment import Equipment
from sqlalchemy import TextClause, and_, delete, insert, or_, select, update, orm
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.equipment.equipment_dto import EquipmentDTO
from src.dto.reservation.reservation_dto import ReservationDTO

class EquipmentRepository:
    @staticmethod
    def create_equipment(equipment: EquipmentDTO) -> EquipmentDTO:
        query = (
            insert(Equipment)
            .values(
                name=equipment.name,
                description=equipment.description,
                category=equipment.category,
                purchased_by=equipment.purchased_by,
                purchase_date=equipment.purchase_date,
                price=equipment.price,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return EquipmentDTO(**data) if data else None
    
    @staticmethod
    def get_equipment(id: int) -> Optional[EquipmentDTO]:
        query = select(Equipment).where(Equipment.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return EquipmentDTO(**data) if data else None

    @staticmethod
    def get_equipments(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[EquipmentDTO]]:
        query = (
            select(Equipment)
            .options(
                orm.selectinload(Equipment.equipment_items),
                orm.selectinload(Equipment.equipment_images),
            ).order_by(order_by_clause)
        )

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        data = PostgresDatabase.get_session().execute(query).scalars().unique().all()
        return [EquipmentDTO.model_validate(equipment) for equipment in data] if data else None 

    @staticmethod
    def get_available_equipments(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
        start_date: datetime,
        end_date: datetime,
    ) -> Optional[list[EquipmentDTO]]:
        reserved_subq = (
            select(ReservationEquipment.equipment_item_id)
            .join(Reservation)
            .where(
                and_(
                    Reservation.start_date <= end_date,
                    Reservation.end_date >= start_date,
                    or_(
                        Reservation.accepted.is_(True), # Reserved
                        Reservation.accepted.is_(None), # Pending
                    ),
                )
            )
        )

        query = (
            select(Equipment)
            .options(
                orm.contains_eager(Equipment.equipment_items),
                orm.selectinload(Equipment.equipment_images),
            )
            .join(EquipmentItem, Equipment.id == EquipmentItem.equipment_id)
            .outerjoin(ReservationEquipment, ReservationEquipment.equipment_item_id == EquipmentItem.id)
            .outerjoin(Reservation, Reservation.id == ReservationEquipment.reservation_id)
            .where(
                EquipmentItem.available.is_(True),
                EquipmentItem.id.not_in(reserved_subq)
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

        data = PostgresDatabase.get_session().execute(query).scalars().unique().all()
        return [EquipmentDTO.model_validate(equipment) for equipment in data] if data else None

    @staticmethod
    def get_unavailable_equipments(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[EquipmentDTO]]:
        query = (
            select(Equipment)
            .options(
                orm.contains_eager(Equipment.equipment_items),
                orm.selectinload(Equipment.equipment_images),
            )
            .join(EquipmentItem, Equipment.id == EquipmentItem.equipment_id)
            .where(EquipmentItem.available.is_(False))
            .order_by(order_by_clause)
        )

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        data = PostgresDatabase.get_session().execute(query).scalars().unique().all()
        return [EquipmentDTO.model_validate(equipment) for equipment in data] if data else None

    @staticmethod
    def get_equipment_count(where_clause: Optional[TextClause]) -> int:
        query = f"""
            SELECT COUNT({Equipment.__table__}.id) AS count
            FROM {Equipment.__table__}
        """
        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(str(query))
        return data['count'] if data else 0

    @staticmethod
    def get_equipment_reservations(
        id: int,
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
        ) -> Optional[list[ReservationDTO]]:
        query = (
            select(Reservation)
            .join(ReservationEquipment, Reservation.id == ReservationEquipment.reservation_id)
        )

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .where(ReservationEquipment.equipment_id == id)
            .order_by(order_by_clause)
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
    def update_equipment(id: int, equipment: EquipmentDTO) -> Optional[EquipmentDTO]:
        query = (
            update(Equipment)
            .where(Equipment.id == id)
            .values(
                name=equipment.name,
                description=equipment.description,
                category=equipment.category,
                purchased_by=equipment.purchased_by,
                purchase_date=equipment.purchase_date,
                price=equipment.price,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return EquipmentDTO(**data) if data else None

    @staticmethod
    def delete_equipment(id: int) -> None:
        query = (
            delete(Equipment)
            .where(Equipment.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_equipments_by_id(ids: list[int]) -> None:
        query = (
            delete(Equipment)
            .where(Equipment.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
