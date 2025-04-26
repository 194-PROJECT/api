from flask import request
from core.api import Api, response
from src.dto.group.group_user_dto import GroupUserDTO
from src.handler.group.group_handler import GroupHandler
from src.handler.group.group_user_handler import GroupUserHandler
from src.handler.user.user_handler import UserHandler

app = Api.application

@app.route('/group/user/<int:id>', methods=['GET'])
def get_group_user(id: int):
    group_user = GroupUserHandler.get_group_user(id)

    if not group_user:
        return response(
            message="Group user not found",
            code=404,
            errors=["Failed to retrieve the requested group user"],
        )

    return response(
        message=f"Group user {group_user.id} found",
        code=200,
        data=group_user.model_dump()
    )

@app.route('/group/<int:group_id>/user', methods=['GET'])
def get_group_users(group_id: int):
    group_users = GroupUserHandler.get_group_users(group_id)

    if group_users is None:
        return response(
            message="No group users found",
            code=404,
            errors=["Failed to retrieve any group users"],
        )

    return response(
        message=f"Group users for group {group_id} found",
        code=200,
        data=[group_user.model_dump() for group_user in group_users]
    )


@app.route('/group/user', methods=['POST'])
def create_group_user():
    group_user_data = GroupUserDTO(**request.json)
    user_id = group_user_data.user_id
    group_id = group_user_data.group_id
    user = UserHandler.get_user(user_id)
    group = GroupHandler.get_group(group_id)
    
    if not user:
        return response(
            message="User not found",
            code=404,
            errors=["Failed to retrieve the requested user"],
        )

    if not group:
        return response(
            message="Group not found",
            code=404,
            errors=["Failed to retrieve the requested group"],
        )

    if GroupUserHandler.user_in_group(user_id, group_id):
        return response(
            message="User already in group",
            code=400,
            errors=["The user is already a member of the group"],
        )

    group_user = GroupUserHandler.create_group_user(group_user_data)

    if not group_user:
        return response(
            message="Failed to create group user",
            code=400,
            errors=["Failed to create the group user with the provided data"],
        )

    return response(
        message=f"Group user {group_user.id} created",
        code=201,
        data=group_user.model_dump()
    )

@app.route('/group/user/<int:id>', methods=['PATCH'])
def update_group_user(id: int):
    group_user = GroupUserHandler.get_group_user(id)

    if not group_user:
        return response(
            message="Group user not found",
            code=404,
            errors=["Failed to retrieve the requested group user for update"],
        )

    group_user_update_request = group_user.model_copy(update=request.json)
    updated_group_user = GroupUserHandler.update_group_user(id, group_user_update_request)

    return response(
        message=f"Group user {updated_group_user.id} updated",
        code=200,
        data=updated_group_user.model_dump()
    )

@app.route('/group/user/<int:id>', methods=['DELETE'])
def delete_group_user(id: int):
    group_user = GroupUserHandler.get_group_user(id)

    if not group_user:
        return response(
            message="Group user not found",
            code=404,
            errors=["Failed to retrieve the requested group user for deletion"],
        )

    GroupUserHandler.delete_group_user(id)

    return response(
        message=f"Group user {group_user.id} deleted",
        code=200
    )
