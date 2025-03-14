import core.auth_helper as auth_helper
from core.api import Api, response
from flask import request
from src.enum.auth.user_identifier_enum import UserIdentifierEnum
from src.dto.auth.login_request_dto import LoginRequest
from src.handler.auth.session_handler import SessionHandler
from src.handler.user.user_handler import UserHandler

app = Api.application

@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login by verifying credentials and creating a session.
    This function processes a login request by extracting the email, username,
    and password from the request JSON. It then identifies the user based on
    the provided email or username, verifies the password, and creates a session
    if the credentials are valid.
        Response: A response object containing the login status, user information,
        and session details. Possible status codes are:
            - 200: Login successful
            - 400: Invalid identifier
            - 401: Invalid password
            - 404: User not found
    """
    login_request = LoginRequest(**request.json)

    email = login_request.email
    username = login_request.username
    password = auth_helper.decrypt(login_request.password)
    identifier = UserIdentifierEnum.EMAIL if email else UserIdentifierEnum.USERNAME
    
    match identifier:
        case UserIdentifierEnum.EMAIL:
            user = UserHandler.get_user_from_email(email)
        case UserIdentifierEnum.USERNAME:
            user = UserHandler.get_user_from_username(username)
        case _:
            return response("Invalid identifier", 400)

    if not user:
        return response("User not found", 404)

    valid_password = auth_helper.verify_password(password, user.password)

    if not valid_password:
        return response("Invalid password", 401)
    
    session = SessionHandler.create_session(user.id)

    return response(f"Login successful for {username}", 200, data={
        'user': user.model_dump(exclude={'password'}),
        'session': session
    })