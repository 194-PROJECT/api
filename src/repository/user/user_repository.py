from core.auth_helper import hash_password
from database.postgres.query import QueryExecutor
from database.model.users import User
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.user.user_dto import UserDTO

class UserRepository:
    @staticmethod
    def create_user(user: UserDTO) -> UserDTO:
        query = (
            insert(User)
            .values(
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                password=hash_password(user.password),
                role=user.role,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return UserDTO(**data) if data else None
    
    @staticmethod
    def get_user(id: int) -> Optional[UserDTO]:
        query = select(User).where(User.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return UserDTO(**data) if data else None

    @staticmethod
    def get_users(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[UserDTO]]:
        query = select(User).order_by(order_by_clause)

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
        return [UserDTO(**user) for user in data] if data else None
    
    @staticmethod
    def get_user_from_email(email: str)-> Optional[UserDTO]:
        query = select(User).where(User.email == email).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return UserDTO(**data) if data else None

    @staticmethod
    def get_user_from_username(username: str) -> Optional[UserDTO]:
        query = select(User).where(User.username == username).compile(
            compile_kwargs={"literal_binds": True}
        )
        data = QueryExecutor.fetch_one(str(query))
        return UserDTO(**data) if data else None

    @staticmethod
    def update_user(id: int, user: UserDTO) -> Optional[UserDTO]:
        query = (
            update(User)
            .where(User.id == id)
            .values(
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                type=user.type,
                role=user.role,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return UserDTO(**data) if data else None

    @staticmethod
    def delete_user(id: int) -> None:
        query = (
            delete(User)
            .where(User.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_users_by_id(ids: list[int]) -> None:
        query = (
            delete(User)
            .where(User.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
