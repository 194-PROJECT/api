from flask import request
from core.api import Api, GetModelRequest, response

from database.model.users import User, UserKeyEnum, UserKeyTypes
from src.handler.user.user_handler import UserHandler

app = Api.application

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id: int):
    user = UserHandler.get_user(id)

    if not user:
        return response(
            message="User not found",
            code=404
        )

    return response(
        message=f"User {user.username} found",
        code=200,
        data=user.model_dump(exclude=['password'])
    )

@app.route('/user', methods=['GET'])
def get_users():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': User,
        'table_keys': UserKeyEnum,
        'key_types': UserKeyTypes,
    })

    users = UserHandler.get_users(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not users or not len(users):
        return response(
            message="No users found",
            code=404
        )

    return response(
        message="Users found",
        code=200,
        data=[user.model_dump(exclude=['password']) for user in users]
    )

@app.route('/user', methods=['POST'])
def create_user():
    return response(
        message = 'Route not implemented',
        code = 501,
    )

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id: int):
    user = UserHandler.get_user(id)

    if not user:
        return response(
            message="Cannot update user that does not exist",
            code=404
        )

    user_update_request = user.model_copy(update=request.json)
    updated_user = UserHandler.update_user(id, user_update_request)
    
    return response(
        message=f"User {updated_user.username} updated",
        code=200,
        data=updated_user.model_dump(exclude=['password'])
    )

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = UserHandler.get_user(id)
    
    if not user:
        return response(
            message="Cannot delete user that does not exist",
            code=404
        )
    
    UserHandler.delete_user(id)
    
    return response(
        message=f"User {user.username} deleted",
        code=200
    )

@app.route('/user', methods=['DELETE'])
def delete_users():
    user_ids = request.args.getlist('ids', type=int)

    if not isinstance(user_ids, list) or not all(isinstance(id, int) for id in user_ids):
        return response(
            message="User ids must be a list of integers",
            code=400
        )

    if not user_ids or not len(user_ids):
        return response(
            message="No user ids provided",
            code=400
        )

    UserHandler.delete_users_by_id(user_ids)
    
    return response(
        message="Users deleted",
        code=200
    )