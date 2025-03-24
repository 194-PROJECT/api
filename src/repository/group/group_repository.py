from database.postgres.query import QueryExecutor
from database.model.groups import Group
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.group.group_dto import GroupDTO

class GroupRepository:
    @staticmethod
    def create_group(group: GroupDTO) -> GroupDTO:
        query = (
            insert(Group)
            .values(
                class_id=group.class_id,
                name=group.name,
                description=group.description,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return GroupDTO(**data) if data else None
    
    @staticmethod
    def get_group(id: int) -> Optional[GroupDTO]:
        query = select(Group).where(Group.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return GroupDTO(**data) if data else None

    @staticmethod
    def get_groups(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[GroupDTO]]:
        query = select(Group).order_by(order_by_clause)

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
        return [GroupDTO(**group) for group in data] if data else None

    @staticmethod
    def get_group_count(where_clause: Optional[TextClause]) -> int:
        query = f"""
            SELECT COUNT({Group.__table__}.id) AS count
            FROM {Group.__table__}
        """
        if where_clause is not None:
            query = f"{query} WHERE {where_clause}"

        data = QueryExecutor.fetch_one(str(query))
        return data['count'] if data else 0
    
    @staticmethod
    def update_group(id: int, group: GroupDTO) -> Optional[GroupDTO]:
        query = (
            update(Group)
            .where(Group.id == id)
            .values(
                class_id=group.class_id,
                name=group.name,
                description=group.description,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return GroupDTO(**data) if data else None

    @staticmethod
    def delete_group(id: int) -> None:
        query = (
            delete(Group)
            .where(Group.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_groups_by_id(ids: list[int]) -> None:
        query = (
            delete(Group)
            .where(Group.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
