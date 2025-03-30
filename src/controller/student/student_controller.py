from flask import request
from core.api import Api, GetModelRequest, response

from database.model.student import Student, StudentKeyEnum, StudentKeyTypes
from src.dto.student.student_dto import StudentDTO
from src.enum.user.user_role_enum import UserRoleEnum
from src.enum.user.user_type_enum import UserTypeEnum
from src.handler.student.student_handler import StudentHandler
from src.handler.user.user_handler import UserHandler

app = Api.application

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id: int):
    student = StudentHandler.get_student(id)

    if not student:
        return response(
            message="Student not found",
            code=404,
            errors=["Failed to retrieve the requested student"],
        )

    return response(
        message=f"Student {student.id} found",
        code=200,
        data=student.model_dump()
    )

@app.route('/student', methods=['GET'])
def get_students():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Student,
        'table_keys': StudentKeyEnum,
        'key_types': StudentKeyTypes,
    })

    students = StudentHandler.get_students(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not students or not len(students):
        return response(
            message="No students found",
            code=404,
            errors=["Failed to retrieve any students"],
        )

    student_count = StudentHandler.get_student_count(get_request.where_clause)

    return response(
        message="Students found",
        code=200,
        data=[student.model_dump() for student in students],
        page=get_request.page,
        total_rows=student_count,
    )

@app.route('/student/count', methods=['GET'])
def get_student_count():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Student,
        'table_keys': StudentKeyEnum,
        'key_types': StudentKeyTypes,
    })

    student_count = StudentHandler.get_student_count(get_request.where_clause)

    return response(
        message="Student count found",
        code=200,
        data=student_count
    )

@app.route('/student', methods=['POST'])
def create_student():
    student_data = StudentDTO(**request.json)
    user = UserHandler.get_user(student_data.user_id)
    student = StudentHandler.get_student_by_user_id(student_data.user_id)
    
    if student:
        return response(
            message="Student already exists",
            code=400,
            errors=["Cannot create student with a user that is already a student"],
        )

    if not user:
        return response(
            message="User not found",
            code=404,
            errors=["Cannot create student with a user that does not exist"],
        )

    if user.type == UserTypeEnum.STUDENT:
        return response(
            message="User already exists",
            code=400,
            errors=["Cannot create student with a user that is already a student"],
        )
    
    student = StudentHandler.create_student(student_data)

    if not student:
        return response(
            message="Failed to create student",
            code=400,
            errors=["Failed to create student with the provided data"],
        )

    UserHandler.update_user(user.id, user.model_validate(obj={
        'type': UserTypeEnum.STUDENT,
        'role': UserRoleEnum.USER,
    }))

    return response(
        message=f"Student {student.id} created",
        code=201,
        data=student.model_dump()
    )

@app.route('/student/<int:id>', methods=['PATCH'])
def update_student(id: int):
    student = StudentHandler.get_student(id)

    if not student:
        return response(
            message="Student not found",
            code=404,
            errors=["Cannot update student that does not exist"],
        )

    student_update_request = student.model_copy(update=request.json)
    updated_student = StudentHandler.update_student(id, student_update_request)
    
    return response(
        message=f"Student {updated_student.id} updated",
        code=200,
        data=updated_student.model_dump()
    )

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id: int):
    student = StudentHandler.get_student(id)
    
    if not student:
        return response(
            message="Student not found",
            code=404,
            errors=["Cannot delete student that does not exist"],
        )
    
    StudentHandler.delete_student(id)
    
    user = UserHandler.get_user(student.user_id)
    
    # If the user is a student, update their type and role to GUEST
    if user and user.type == UserTypeEnum.STUDENT:
        UserHandler.update_user(user.id, user.model_validate(obj={
            'type': UserTypeEnum.GUEST,
            'role': UserHandler.user_type_to_role_map[UserTypeEnum.GUEST],
        }))
    
    return response(
        message=f"Student {student.id} deleted",
        code=200
    )

@app.route('/student', methods=['DELETE'])
def delete_students():
    student_ids = request.args.getlist('ids', type=int)

    if not isinstance(student_ids, list) or not all(isinstance(id, int) for id in student_ids):
        return response(
            message="Invalid student ids",
            code=400,
            errors=["Student ids must be a list of integers"],
        )

    if not student_ids or not len(student_ids):
        return response(
            message="No student ids provided",
            code=400,
            errors=["Please provide a list of student ids to delete"],
        )

    StudentHandler.delete_students_by_id(student_ids)
    
    return response(
        message="Students deleted",
        code=200
    )
