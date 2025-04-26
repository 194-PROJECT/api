from database.postgres.database import PostgresDatabase
from database.postgres.query import QueryExecutor
from database.model.group_user import GroupUser
from sqlalchemy import delete, insert, select, update, orm
from sqlalchemy.dialects import postgresql
from typing import Optional
from src.dto.group.group_user_dto import GroupUserDTO

class GroupUserRepository:
    @staticmethod
    def create_group_user(group_user: GroupUserDTO) -> GroupUserDTO:
        try:
            query = (
                insert(GroupUser)
                .values(
                    group_id=group_user.group_id,
                    user_id=group_user.user_id,
                )
                .returning(GroupUser.id)
            )
            session = PostgresDatabase.get_session()
            inserted_id = session.execute(query).scalar_one()
            session.commit()
            
            query = (
                select(GroupUser)
                .options(
                    orm.selectinload(GroupUser.user),
                )
                .where(GroupUser.id == inserted_id)
            )
            data = session.execute(query).scalar_one_or_none()
            return GroupUserDTO.model_validate(data) if data else None
        finally:
            session.close()

    @staticmethod
    def get_group_user(id: int) -> Optional[GroupUserDTO]:
        query = select(GroupUser).where(GroupUser.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return GroupUserDTO(**data) if data else None
    
    @staticmethod
    def get_group_users(group_id: int) -> Optional[list[GroupUserDTO]]:
        query = select(GroupUser).where(GroupUser.group_id == group_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_all(str(query))
        return [GroupUserDTO(**item) for item in data] if data else None

    @staticmethod
    def update_group_user(id: int, group_user: GroupUserDTO) -> Optional[GroupUserDTO]:
        query = (
            update(GroupUser)
            .where(GroupUser.id == id)
            .values(
                group_id=group_user.group_id,
                user_id=group_user.user_id,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return GroupUserDTO(**data) if data else None

    @staticmethod
    def delete_group_user(id: int) -> None:
        query = (
            delete(GroupUser)
            .where(GroupUser.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def user_in_group(user_id: int, group_id: int) -> bool:
        query = select(GroupUser).where(
            GroupUser.user_id == user_id,
            GroupUser.group_id == group_id,
        ).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return data is not None
