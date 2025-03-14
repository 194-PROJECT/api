from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.classes.class_dto import ClassDTO
from src.repository.classes.class_repository import ClassRepository

class ClassHandler:
    @staticmethod
    def create_class(class_data: ClassDTO) -> Optional[ClassDTO]:
        return ClassRepository.create_class(class_data)

    @staticmethod
    def get_class(id: int) -> Optional[ClassDTO]:
        return ClassRepository.get_class(id)

    @staticmethod
    def get_classes(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[List[ClassDTO]]:
        return ClassRepository.get_classes(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def update_class(id: int, class_data: ClassDTO) -> Optional[ClassDTO]:
        return ClassRepository.update_class(id, class_data)

    @staticmethod
    def delete_class(id: int) -> None:
        ClassRepository.delete_class(id)

    @staticmethod
    def delete_classes_by_id(ids: List[int]) -> None:
        ClassRepository.delete_classes_by_id(ids)
