from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.user.user_dto import UserDTO
from src.repository.user.user_repository import UserRepository

class UserHandler:
    @staticmethod
    def create_user(user: UserDTO) -> Optional[UserDTO]:
        return UserRepository.create_user(user)

    @staticmethod
    def get_user(id: int) -> Optional[UserDTO]:
        return UserRepository.get_user(id)

    @staticmethod
    def get_users(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[UserDTO]]:
        return UserRepository.get_users(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def get_user_from_email(email: str) -> Optional[UserDTO]:
        return UserRepository.get_user_from_email(email)

    @staticmethod
    def get_user_from_username(username: str) -> Optional[UserDTO]:
        return UserRepository.get_user_from_username(username)

    @staticmethod
    def update_user(id: int, user: UserDTO) -> Optional[UserDTO]:
        return UserRepository.update_user(id, user)

    @staticmethod
    def delete_user(id: int) -> None:
        UserRepository.delete_user(id)

    @staticmethod
    def delete_users_by_id(ids: List[int]) -> None:
        UserRepository.delete_users_by_id(ids)

    # TODO: build a check_availability method in the UserRepository class
    @staticmethod
    def check_availability(email: str, username: str) -> bool:
        return (not UserHandler.get_user_from_email(email)
                and not UserHandler.get_user_from_username(username))
