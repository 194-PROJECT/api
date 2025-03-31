from typing import Optional, List
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.query import QueryExecutor
from sqlalchemy import insert, select, delete
from sqlalchemy.dialects import postgresql

from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO

class ReservationEquipmentRepository:
    @staticmethod
    def get_reservation_equipment(reservation_id: int) -> Optional[List[ReservationEquipmentDTO]]:
        query = select(ReservationEquipment).where(ReservationEquipment.reservation_id == reservation_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_all(str(query))
        return [ReservationEquipmentDTO(**item) for item in data] if data else None

    @staticmethod
    def add_reservation_equipment(equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
        query = (
            insert(ReservationEquipment)
            .values(
                reservation_id=equipment.reservation_id,
                equipment_id=equipment.equipment_id,
                quantity=equipment.quantity,
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
    def delete_reservation_equipment(reservation_id: int, equipment_id: int) -> bool:
        query = (
            delete(ReservationEquipment)
            .where(
                (ReservationEquipment.reservation_id == reservation_id)
                & (ReservationEquipment.equipment_id == equipment_id)
            )
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        return QueryExecutor.delete_one(str(query)) is not None
