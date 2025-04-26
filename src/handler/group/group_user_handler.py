from typing import Optional
from src.dto.group.group_user_dto import GroupUserDTO
from src.repository.group.group_user_repository import GroupUserRepository

class GroupUserHandler:
    @staticmethod
    def create_group_user(group_user: GroupUserDTO) -> Optional[GroupUserDTO]:
        return GroupUserRepository.create_group_user(group_user)

    @staticmethod
    def get_group_user(id: int) -> Optional[GroupUserDTO]:
        return GroupUserRepository.get_group_user(id)

    @staticmethod
    def get_group_users(group_id: int) -> Optional[list[GroupUserDTO]]:
        return GroupUserRepository.get_group_users(group_id)

    @staticmethod
    def update_group_user(id: int, group_user: GroupUserDTO) -> Optional[GroupUserDTO]:
        return GroupUserRepository.update_group_user(id, group_user)

    @staticmethod
    def delete_group_user(id: int) -> None:
        GroupUserRepository.delete_group_user(id)

    @staticmethod
    def user_in_group(user_id: int, group_id: int) -> bool:
        return GroupUserRepository.user_in_group(user_id, group_id)
