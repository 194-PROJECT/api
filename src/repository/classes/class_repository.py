from database.postgres.query import QueryExecutor
from database.model.classes import Class
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.classes.class_dto import ClassDTO

class ClassRepository:
    @staticmethod
    def create_class(class_data: ClassDTO) -> Optional[ClassDTO]:
        query = (
            insert(Class)
            .values(
                course_id=class_data.course_id,
                instructor_id=class_data.instructor_id,
                semester_id=class_data.semester_id,
                name=class_data.name,
                description=class_data.description,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return ClassDTO(**data) if data else None

    @staticmethod
    def get_class(id: int) -> Optional[ClassDTO]:
        query = select(Class).where(Class.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return ClassDTO(**data) if data else None

    @staticmethod
    def get_classes(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ClassDTO]]:
        query = select(Class).order_by(order_by_clause)

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
        return [ClassDTO(**class_) for class_ in data] if data else None

    @staticmethod
    def update_class(id: int, class_data: ClassDTO) -> Optional[ClassDTO]:
        query = (
            update(Class)
            .where(Class.id == id)
            .values(
                course_id=class_data.course_id,
                instructor_id=class_data.instructor_id,
                semester_id=class_data.semester_id,
                name=class_data.name,
                description=class_data.description,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return ClassDTO(**data) if data else None

    @staticmethod
    def delete_class(id: int) -> None:
        query = (
            delete(Class)
            .where(Class.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_classes_by_id(ids: list[int]) -> None:
        query = (
            delete(Class)
            .where(Class.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
