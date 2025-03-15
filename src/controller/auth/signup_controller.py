import core.auth_helper as auth_helper
from core.api import Api, response
from flask import request
from core.email_format import is_email_from_up
from src.dto.auth.signup_request_dto import SignupRequest
from src.dto.user.user_dto import UserDTO
from src.dto.student.student_dto import StudentDTO
from src.enum.user.user_role_enum import UserRoleEnum
from src.enum.user.user_type_enum import UserTypeEnum
from src.handler.auth.session_handler import SessionHandler
from src.handler.student.student_handler import StudentHandler
from src.handler.user.user_handler import UserHandler

app = Api.application

@app.route('/signup', methods=['POST'])
def signup():
    """
    NOTE: This route assumes that the user came from the signup page. A different
    route should be used for admin-created users. We also assume that those that
    can go through this flow are users or guests
    
    Handles user signup process.
    This function performs the following steps:
    2. Checks if the email or username is already in use.
    3. Validates the email domain and required fields for specific roles.
    4. Decrypts the provided password.
    5. Creates a new user with the provided details.
    6. If applicable, creates a student record associated with the user.
    7. Creates a session for the newly created user.
    8. Returns a response indicating the success or failure of the signup process.
    
    Returns:
        Response: A response object containing a message, status code, and additional data if applicable.
    """
    
    signup_request = SignupRequest(**request.json)

    is_available = UserHandler.check_availability(signup_request.email, signup_request.username)

    if not is_available:
        return response(
            message='Signup failed',
            code=409,
            errors=['Email or username already in use'],
        )

    # Auto assign role and type based on email domain
    role = UserRoleEnum.USER if is_email_from_up(email=signup_request.email) else UserRoleEnum.GUEST
    type = UserTypeEnum.STUDENT if role == UserRoleEnum.USER else UserTypeEnum.GUEST
    
    # Guest should not be able to signup here
    if (role == UserRoleEnum.GUEST):
        return response(
            message='Signup failed',
            code=400,
            errors=['Guests are not allowed to signup'],
        )

    # Check if the email domain is UP and if the required fields are provided
    # User is specified as a student or a site user, and no program ID or student ID is provided
    if (
        signup_request.type == UserTypeEnum.STUDENT
        and (not signup_request.program_id or not signup_request.student_id)
    ):
        return response(
            message='Signup failed',
            code=400,
            errors=['Program ID and Student ID are required for students'],
        )

    signup_request.password = auth_helper.decrypt(signup_request.password)
    user = UserHandler.create_user(UserDTO(
        email=signup_request.email,
        username=signup_request.username,
        password=signup_request.password,
        first_name=signup_request.first_name,
        last_name=signup_request.last_name,
        type=type,
        role=role,
    ))

    if signup_request.program_id and signup_request.student_id:
        StudentHandler.create_student(StudentDTO(
            user_id=user.id,
            program_id=signup_request.program_id,
            student_id=signup_request.student_id,
        ))

    session = SessionHandler.create_session(user.id)
    
    return response('User created', 200, data={
        'user': user.model_dump(exclude={'password'}),
        'session': session
    })