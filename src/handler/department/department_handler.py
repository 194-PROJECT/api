from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.department.department_dto import DepartmentDTO
from src.repository.department.department_repository import DepartmentRepository

class DepartmentHandler:
    @staticmethod
    def create_department(department: DepartmentDTO) -> Optional[DepartmentDTO]:
        return DepartmentRepository.create_department(department)
    
    @staticmethod
    def get_department(id: int) -> Optional[DepartmentDTO]:
        return DepartmentRepository.get_department(id)
    
    @staticmethod
    def get_departments(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[DepartmentDTO]]:
        return DepartmentRepository.get_departments(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def update_department(id: int, department: DepartmentDTO) -> Optional[DepartmentDTO]:
        return DepartmentRepository.update_department(id, department)
    
    @staticmethod
    def delete_department(id: int) -> None:
        DepartmentRepository.delete_department(id)
    
    @staticmethod
    def delete_departments_by_id(ids: List[int]) -> None:
        DepartmentRepository.delete_departments_by_id(ids)
