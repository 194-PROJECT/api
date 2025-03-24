from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.group.group_dto import GroupDTO
from src.repository.group.group_repository import GroupRepository

class GroupHandler:
    @staticmethod
    def create_group(group: GroupDTO) -> Optional[GroupDTO]:
        return GroupRepository.create_group(group)
    
    @staticmethod
    def get_group(id: int) -> Optional[GroupDTO]:
        return GroupRepository.get_group(id)
    
    @staticmethod
    def get_groups(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[GroupDTO]]:
        return GroupRepository.get_groups(limit, offset, order_by_clause, where_clause)
    
    @staticmethod
    def get_group_count(where_clause: Optional[str]) -> int:
        return GroupRepository.get_group_count(where_clause)
    
    @staticmethod
    def update_group(id: int, group: GroupDTO) -> Optional[GroupDTO]:
        return GroupRepository.update_group(id, group)
    
    @staticmethod
    def delete_group(id: int) -> None:
        GroupRepository.delete_group(id)
    
    @staticmethod
    def delete_groups_by_id(ids: List[int]) -> None:
        GroupRepository.delete_groups_by_id(ids)
