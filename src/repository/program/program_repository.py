from database.postgres.query import QueryExecutor
from database.model.program import Program
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.program.program_dto import ProgramDTO

class ProgramRepository:
    @staticmethod
    def create_program(program: ProgramDTO) -> ProgramDTO:
        query = (
            insert(Program)
            .values(
                department_id=program.department_id,
                title=program.title,
                description=program.description,
                credits_required=program.credits_required,
                duration=program.duration,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return ProgramDTO(**data) if data else None
    
    @staticmethod
    def get_program(id: int) -> Optional[ProgramDTO]:
        query = select(Program).where(Program.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return ProgramDTO(**data) if data else None

    @staticmethod
    def get_programs(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ProgramDTO]]:
        query = select(Program).order_by(order_by_clause)

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
        return [ProgramDTO(**program) for program in data] if data else None

    @staticmethod
    def get_program_count(where_clause: Optional[TextClause]) -> int:
        query = f"""
            SELECT COUNT({Program.__table__}.id) AS count
            FROM {Program.__table__}
        """
        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(str(query))
        return data['count'] if data else 0

    @staticmethod
    def update_program(id: int, program: ProgramDTO) -> Optional[ProgramDTO]:
        query = (
            update(Program)
            .where(Program.id == id)
            .values(
                department_id=program.department_id,
                title=program.title,
                description=program.description,
                credits_required=program.credits_required,
                duration=program.duration,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return ProgramDTO(**data) if data else None

    @staticmethod
    def delete_program(id: int) -> None:
        query = (
            delete(Program)
            .where(Program.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_programs_by_id(ids: list[int]) -> None:
        query = (
            delete(Program)
            .where(Program.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
