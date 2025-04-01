from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.equipment.equipment_dto import EquipmentDTO
from src.dto.reservation.reservation_dto import ReservationDTO
from src.repository.equipment.equipment_repository import EquipmentRepository

class EquipmentHandler:
    @staticmethod
    def create_equipment(equipment: EquipmentDTO) -> Optional[EquipmentDTO]:
        return EquipmentRepository.create_equipment(equipment)
    
    @staticmethod
    def get_equipment(id: int) -> Optional[EquipmentDTO]:
        return EquipmentRepository.get_equipment(id)
    
    @staticmethod
    def get_equipments(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[EquipmentDTO]]:
        return EquipmentRepository.get_equipments(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def get_equipment_reservations(
        id: int,
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
        ) -> Optional[list[ReservationDTO]]:
        return EquipmentRepository.get_equipment_reservations(
            id=id,
            limit=limit,
            offset=offset,
            order_by_clause=order_by_clause,
            where_clause=where_clause,
        )

    @staticmethod
    def get_equipment_count(where_clause: Optional[str]) -> int:
        return EquipmentRepository.get_equipment_count(where_clause)

    @staticmethod
    def update_equipment(id: int, equipment: EquipmentDTO) -> Optional[EquipmentDTO]:
        return EquipmentRepository.update_equipment(id, equipment)
    
    @staticmethod
    def delete_equipment(id: int) -> None:
        EquipmentRepository.delete_equipment(id)
    
    @staticmethod
    def delete_equipments_by_id(ids: List[int]) -> None:
        EquipmentRepository.delete_equipments_by_id(ids)
