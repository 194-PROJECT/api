from database.postgres.query import QueryExecutor
from database.model.course import Course
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.course.course_dto import CourseDTO

class CourseRepository:
    @staticmethod
    def create_course(course: CourseDTO) -> Optional[CourseDTO]:
        query = (
            insert(Course)
            .values(
                program_id=course.program_id,
                prerequisite_id=course.prerequisite_id,
                name=course.name,
                description=course.description,
                credits=course.credits,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return CourseDTO(**data) if data else None
    
    @staticmethod
    def get_course(id: int) -> Optional[CourseDTO]:
        query = select(Course).where(Course.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return CourseDTO(**data) if data else None

    @staticmethod
    def get_courses(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[CourseDTO]]:
        query = select(Course).order_by(order_by_clause)

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
        return [CourseDTO(**course) for course in data] if data else None
    
    @staticmethod
    def update_course(id: int, course: CourseDTO) -> Optional[CourseDTO]:
        query = (
            update(Course)
            .where(Course.id == id)
            .values(
                program_id=course.program_id,
                prerequisite_id=course.prerequisite_id,
                name=course.name,
                description=course.description,
                credits=course.credits,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return CourseDTO(**data) if data else None

    @staticmethod
    def delete_course(id: int) -> None:
        query = (
            delete(Course)
            .where(Course.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_courses_by_id(ids: list[int]) -> None:
        query = (
            delete(Course)
            .where(Course.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
