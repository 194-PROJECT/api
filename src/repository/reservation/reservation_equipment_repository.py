from typing import Optional, List
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.query import QueryExecutor
from sqlalchemy import insert, select, delete, update
from sqlalchemy.dialects import postgresql

from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO

class ReservationEquipmentRepository:
    @staticmethod
    def get_reservation_equipment(id: int) -> Optional[ReservationEquipmentDTO]:
        query = select(ReservationEquipment).where(ReservationEquipment.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return ReservationEquipmentDTO(**data) if data else None

    @staticmethod
    def get_reservation_equipments(reservation_id: int) -> Optional[List[ReservationEquipmentDTO]]:
        query = select(ReservationEquipment).where(ReservationEquipment.reservation_id == reservation_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_all(str(query))
        return [ReservationEquipmentDTO(**item) for item in data] if data else None

    @staticmethod
    def add_reservation_equipment(reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
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
    def update_reservation_equipment(id: int, reservation_equipment: ReservationEquipmentDTO) -> Optional[ReservationEquipmentDTO]:
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
