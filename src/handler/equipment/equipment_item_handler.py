from typing import Optional

from sqlalchemy import TextClause
from src.dto.equipment.equipment_item_dto import EquipmentItemDTO
from src.repository.equipment.equipment_item_repository import EquipmentItemRepository

class EquipmentItemHandler:
    @staticmethod
    def create_equipment_item(equipment_item: EquipmentItemDTO) -> Optional[EquipmentItemDTO]:
        return EquipmentItemRepository.create_equipment_item(equipment_item)

    @staticmethod
    def get_equipment_item(id: int) -> Optional[EquipmentItemDTO]:
        return EquipmentItemRepository.get_equipment_item(id)
    
    @staticmethod
    def get_equipment_items(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: TextClause,
        equipment_id: int = None,
    ) -> list[EquipmentItemDTO]:
        return EquipmentItemRepository.get_equipment_items(
            limit=limit,
            offset=offset,
            order_by_clause=order_by_clause,
            where_clause=where_clause,
            equipment_id=equipment_id,
        )

    @staticmethod
    def get_equipment_item_count(where_clause: Optional[TextClause]) -> int:
        return EquipmentItemRepository.get_equipment_item_count(where_clause)

    @staticmethod
    def update_equipment_item(id: int, equipment_item: EquipmentItemDTO) -> Optional[EquipmentItemDTO]:
        return EquipmentItemRepository.update_equipment_item(id, equipment_item)

    @staticmethod
    def delete_equipment_item(id: int) -> None:
        EquipmentItemRepository.delete_equipment_item(id)
