from datetime import date
from database.model.semester import Semester
from database.postgres.database import PostgresDatabase
from database.postgres.query import QueryExecutor
from database.model.classes import Class
from sqlalchemy import TextClause, delete, insert, select, update, orm
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
        query = (
            select(Class)
            .options(
                orm.selectinload(Class.course),
                orm.selectinload(Class.instructor),
                orm.selectinload(Class.semester),
            )
            .where(Class.id == id)
        )

        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().one_or_none()
            return ClassDTO.model_validate(data) if data else None
        finally:
            session.close()

    @staticmethod
    def get_classes(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ClassDTO]]:
        query = (
            select(Class)
            .options(
                orm.selectinload(Class.course),
                orm.selectinload(Class.instructor),
                orm.selectinload(Class.semester),
            )
            .order_by(order_by_clause)
        )

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        
        session = PostgresDatabase.get_session()
        try:
            data = session.execute(query).scalars().unique().all()
            return [ClassDTO.model_validate(reservation) for reservation in data] if data else None
        finally:
            session.close()

    @staticmethod
    def get_classes_by_current_semester(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[ClassDTO]]:
        session = PostgresDatabase.get_session()
        try:
            today = date.today()
            semester_query = (
                select(Semester)
                .where(Semester.start_date <= today, Semester.end_date >= today)
            )
            current_semester = session.execute(semester_query).scalar_one_or_none()

            if not current_semester:
                return None

            query = (
                select(Class)
                .options(
                    orm.selectinload(Class.course),
                    orm.selectinload(Class.instructor),
                    orm.selectinload(Class.semester),
                )
                .where(Class.semester_id == current_semester.id)
                .order_by(order_by_clause)
            )
            
            if where_clause is not None:
                query = query.where(where_clause)

            query = (
                query
                .limit(limit)
                .offset(offset)
            )

            data = session.execute(query).scalars().unique().all()
            return [ClassDTO.model_validate(c) for c in data] if data else None
        finally:
            session.close()

    @staticmethod
    def get_class_count(where_clause: Optional[TextClause]) -> int:
        query = f"""
            SELECT COUNT({Class.__table__}.id) AS count
            FROM {Class.__table__}
        """
        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(str(query))
        return data['count'] if data else 0

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
