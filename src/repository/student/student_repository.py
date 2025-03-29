from typing import Optional
from database.model.student import Student
from database.postgres.query import QueryExecutor
from sqlalchemy import TextClause, insert, select, update, delete
from sqlalchemy.dialects import postgresql

from src.dto.student.student_dto import StudentDTO

class StudentRepository:
    @staticmethod
    def create_student(student: StudentDTO) -> StudentDTO:
        query = (
            insert(Student)
            .values(
                user_id=student.user_id,
                program_id=student.program_id,
                student_id=student.student_id,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return StudentDTO(**data) if data else None
    
    @staticmethod
    def get_student(id: int) -> StudentDTO:
        query = select(Student).where(Student.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return StudentDTO(**data) if data else None

    @staticmethod
    def get_student_by_user_id(user_id: int) -> Optional[StudentDTO]:
        query = select(Student).where(Student.user_id == user_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return StudentDTO(**data) if data else None
    
    @staticmethod
    def get_students(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[StudentDTO]]:
        query = select(Student).order_by(order_by_clause)

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
        return [StudentDTO(**student) for student in data] if data else None
    
    @staticmethod
    def get_student_count(where_clause: Optional[TextClause]) -> int:
        query = f"""
            SELECT COUNT({Student.__table__}.id) AS count
            FROM {Student.__table__}
        """
        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(str(query))
        return data['count'] if data else 0

    @staticmethod
    def update_student(id: int, student: StudentDTO) -> StudentDTO:
        query = (
            update(Student)
            .where(Student.id == id)
            .values(
                user_id=student.user_id,
                program_id=student.program_id,
                student_id=student.student_id,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return StudentDTO(**data) if data else None

    @staticmethod
    def delete_student(id: int) -> None:
        query = (
            delete(Student)
            .where(Student.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_students_by_id(ids: list[int]) -> None:
        query = (
            delete(Student)
            .where(Student.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
