from typing import Optional
from database.model.semester import Semester
from database.postgres.query import QueryExecutor
from sqlalchemy import TextClause, insert, select, update, delete
from sqlalchemy.dialects import postgresql

from src.dto.semester.semester_dto import SemesterDTO

class SemesterRepository:
    @staticmethod
    def create_semester(semester: SemesterDTO) -> SemesterDTO:
        query = (
            insert(Semester)
            .values(
                name=semester.name,
                start_date=semester.start_date,
                end_date=semester.end_date,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return SemesterDTO(**data) if data else None
    
    @staticmethod
    def get_semester(semester_id: int) -> SemesterDTO:
        query = select(Semester).where(Semester.id == semester_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return SemesterDTO(**data) if data else None
    
    @staticmethod
    def get_semesters(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[SemesterDTO]]:
        query = select(Semester).order_by(order_by_clause)

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
        return [SemesterDTO(**semester) for semester in data] if data else None

    @staticmethod
    def update_semester(id: int, semester: SemesterDTO) -> SemesterDTO:
        query = (
            update(Semester)
            .where(Semester.id == id)
            .values(
                name=semester.name,
                start_date=semester.start_date,
                end_date=semester.end_date,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return SemesterDTO(**data) if data else None

    @staticmethod
    def delete_semester(id: int) -> None:
        query = (
            delete(Semester)
            .where(Semester.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_semesters_by_id(ids: list[int]) -> None:
        query = (
            delete(Semester)
            .where(Semester.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
