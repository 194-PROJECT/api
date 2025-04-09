from database.model.equipment_item import EquipmentItem
from database.postgres.query import QueryExecutor
from sqlalchemy import delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional
from src.dto.equipment.equipment_item_dto import EquipmentItemDTO

class EquipmentItemRepository:
    @staticmethod
    def create_equipment_item(equipment_item: EquipmentItemDTO) -> EquipmentItemDTO:
        query = (
            insert(EquipmentItem)
            .values(
                item_code=equipment_item.item_code,
                equipment_id=equipment_item.equipment_id,
                available=equipment_item.available,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return EquipmentItemDTO(**data) if data else None

    @staticmethod
    def get_equipment_item(id: int) -> Optional[EquipmentItemDTO]:
        query = select(EquipmentItem).where(EquipmentItem.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return EquipmentItemDTO(**data) if data else None
    
    @staticmethod
    def get_equipment_items(
        limit: int,
        offset: int,
        order_by_clause: str,
        where_clause: Optional[str] = None,
        equipment_id: Optional[int] = None,
    ) -> list[EquipmentItemDTO]:
        query = select(EquipmentItem).order_by(order_by_clause)
        
        if where_clause is not None:
            query = query.where(where_clause)
        
        if equipment_id is not None:
            query = query.where(EquipmentItem.equipment_id == equipment_id)
        
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
        return [EquipmentItemDTO(**item) for item in data] if data else []

    @staticmethod
    def get_equipment_item_count(where_clause: Optional[str]) -> int:
        query = f"""
            SELECT COUNT({EquipmentItem.__table__}.id) AS count
            FROM {EquipmentItem.__table__}
        """

        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(query)
        return data['count'] if data else 0

    @staticmethod
    def update_equipment_item(id: int, equipment_item: EquipmentItemDTO) -> Optional[EquipmentItemDTO]:
        query = (
            update(EquipmentItem)
            .where(EquipmentItem.id == id)
            .values(
                item_code=equipment_item.item_code,
                equipment_id=equipment_item.equipment_id,
                available=equipment_item.available,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return EquipmentItemDTO(**data) if data else None

    @staticmethod
    def delete_equipment_item(id: int) -> None:
        query = (
            delete(EquipmentItem)
            .where(EquipmentItem.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))
