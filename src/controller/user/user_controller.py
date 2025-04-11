from flask import request
from core import auth_helper
from core.api import Api, GetModelRequest, flatten_request_args, response

from core.email_service import EmailService
from database.model.users import User, UserKeyEnum, UserKeyTypes
from src.dto.user.user_dto import UserDTO
from src.enum.user.user_type_enum import UserTypeEnum
from src.handler.student.student_handler import StudentHandler
from src.handler.user.user_handler import UserHandler

app = Api.application

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id: int):
    user = UserHandler.get_user(id)

    if not user:
        return response(
            message="User not found",
            code=404,
            errors=["Failed to retrieve the requested user"],
        )

    return response(
        message=f"User {user.username} found",
        code=200,
        data=user.model_dump(exclude=['password'])
    )

@app.route('/user', methods=['GET'])
def get_users():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
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

    if users is None:
        return response(
            message="No users found",
            code=404,
            errors=["Failed to retrieve any users"],
        )

    user_count = UserHandler.get_user_count(get_request.where_clause)

    return response(
        message="Users found",
        code=200,
        data=[user.model_dump(exclude=['password']) for user in users],
        page=get_request.page,
        total_rows=user_count,
    )

@app.route('/user/count', methods=['GET'])
def get_user_count():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': User,
        'table_keys': UserKeyEnum,
        'key_types': UserKeyTypes,
    })

    user_count = UserHandler.get_user_count(get_request.where_clause)

    return response(
        message="Users count",
        code=200,
        data=user_count,
    )

@app.route('/user', methods=['POST'])
async def create_user():
    """
    Create a new user. This endpoint should only be accessible through admin.

    Returns:
        response: JSON response with the status of the request.
    """
    user_data = UserDTO(**request.json)
    is_available = UserHandler.check_availability(user_data.email, user_data.username)

    if not is_available:
        return response(
            message='Failed to create user',
            code=409,
            errors=['Email or username already in use'],
        )

    if user_data.type == UserTypeEnum.STUDENT:
        return response(
            message='Failed to create user',
            code=400,
            errors=['Students should be created through the student module after creating a user'],
        )

    user_data.role = UserHandler.user_type_to_role_map[user_data.type]
    user_data.password = auth_helper.decrypt(user_data.password)
    user = UserHandler.create_user(user_data)

    if not user:
        return response(
            message="Failed to create user",
            code=400,
            errors=["Failed to create user with the provided data"],
        )

    email_service = EmailService()
    await email_service.send_email(
        recipient_email=user.email,
        subject="DGE UP - Account created",
        body=f"""
            Good day {user.first_name} {user.last_name},
            
            Your account has been created successfully.
            You can now log in to the DGE UP platform using your credentials.

            Your password is: {user_data.password}
            
            Regards,
            DGE UP Team
        """,
    )

    return response(
        message=f"User {user.username} created",
        code=201,
        data=user.model_dump(exclude=['password'])
    )

@app.route('/user/<int:id>', methods=['PATCH'])
async def update_user(id: int):
    user = UserHandler.get_user(id)

    if not user:
        return response(
            message="User not found",
            code=404,
            errors=["Cannot update user that does not exist"],
        )

    user_update_request = user.update(data=request.json, debug=True)
    user_update_request.role = UserHandler.user_type_to_role_map[user_update_request.type]

    if user_update_request.type == UserTypeEnum.STUDENT and user.type != UserTypeEnum.STUDENT:
        return response(
            message="Cannot change user type to student",
            code=400,
            errors=["Use the student module to create a student"],
        )

    # If the user is a student and the type is changed to something else, delete the student
    if user.type == UserTypeEnum.STUDENT and user_update_request.type != UserTypeEnum.STUDENT:
        student = StudentHandler.get_student_by_user_id(user.id)
        if student:
            StudentHandler.delete_student(student.id)

    # Check if the password is being updated notify the user.
    # This is a security measure to ensure that the user is aware of the password change.
    if (
        'password' in request.json and
        not auth_helper.verify_password(user_update_request.password, user.password)
    ):
        decrypted_password = auth_helper.decrypt(user_update_request.password)
        user_update_request.password = auth_helper.hash_password(decrypted_password)
        email_service = EmailService()
        await email_service.send_email(
            recipient_email=user.email,
            subject="DGE UP - Password updated",
            body=f"""
                Good day {user.first_name} {user.last_name},
                
                Your password has been updated successfully.
                You can now log in to the DGE UP platform using your credentials.

                Your new password is: {decrypted_password}
                
                Regards,
                DGE UP Team
            """,
        )

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
            message="User not found",
            code=404,
            errors=["Cannot delete user that does not exist"],
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
            message="Invalid user ids",
            code=400,
            errors=["User ids must be a list of integers"],
        )

    if not user_ids or not len(user_ids):
        return response(
            message="No user ids provided",
            code=400,
            errors=["Please provide a list of user ids to delete"],
        )

    UserHandler.delete_users_by_id(user_ids)
    
    return response(
        message="Users deleted",
        code=200
    )