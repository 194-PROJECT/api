from database.postgres.query import QueryExecutor
from database.model.department import Department
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.department.department_dto import DepartmentDTO

class DepartmentRepository:
    @staticmethod
    def create_department(department: DepartmentDTO) -> DepartmentDTO:
        query = (
            insert(Department)
            .values(
                name=department.name,
                description=department.description,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return DepartmentDTO(**data) if data else None
    
    @staticmethod
    def get_department(id: int) -> Optional[DepartmentDTO]:
        query = select(Department).where(Department.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return DepartmentDTO(**data) if data else None

    @staticmethod
    def get_departments(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[DepartmentDTO]]:
        query = select(Department).order_by(order_by_clause)

        if where_clause is not None:
            query = query.where(where_clause)

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
        return [DepartmentDTO(**department) for department in data] if data else None

    @staticmethod
    def get_department_count(where_clause: Optional[TextClause]) -> int:
        query = f"""
            SELECT COUNT({Department.__table__}.id) AS count
            FROM {Department.__table__}
        """
        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(str(query))
        return data['count'] if data else 0

    @staticmethod
    def update_department(id: int, department: DepartmentDTO) -> Optional[DepartmentDTO]:
        query = (
            update(Department)
            .where(Department.id == id)
            .values(
                name=department.name,
                description=department.description,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return DepartmentDTO(**data) if data else None

    @staticmethod
    def delete_department(id: int) -> None:
        query = (
            delete(Department)
            .where(Department.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_departments_by_id(ids: list[int]) -> None:
        query = (
            delete(Department)
            .where(Department.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
