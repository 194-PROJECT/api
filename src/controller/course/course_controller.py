from flask import request
from core.api import Api, GetModelRequest, response

from database.model.course import Course, CourseKeyEnum, CourseKeyTypes
from src.handler.course.course_handler import CourseHandler

app = Api.application

@app.route('/course/<int:id>', methods=['GET'])
def get_course(id: int):
    course = CourseHandler.get_course(id)

    if not course:
        return response(
            message="Course not found",
            code=404
        )

    return response(
        message=f"Course {course.name} found",
        code=200,
        data=course.model_dump()
    )

@app.route('/course', methods=['GET'])
def get_courses():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Course,
        'table_keys': CourseKeyEnum,
        'key_types': CourseKeyTypes,
    })

    courses = CourseHandler.get_courses(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not courses or not len(courses):
        return response(
            message="No courses found",
            code=404
        )

    return response(
        message="Courses found",
        code=200,
        data=[course.model_dump() for course in courses]
    )

@app.route('/course', methods=['POST'])
def create_course():
    course_data = request.json
    course = CourseHandler.create_course(course_data)
    
    if not course:
        return response(
            message="Failed to create course",
            code=400
        )

    return response(
        message=f"Course {course.name} created",
        code=201,
        data=course.model_dump()
    )

@app.route('/course/<int:id>', methods=['PUT'])
def update_course(id: int):
    course = CourseHandler.get_course(id)

    if not course:
        return response(
            message="Cannot update course that does not exist",
            code=404
        )

    course_update_request = course.model_copy(update=request.json)
    updated_course = CourseHandler.update_course(id, course_update_request)
    
    return response(
        message=f"Course {updated_course.name} updated",
        code=200,
        data=updated_course.model_dump()
    )

@app.route('/course/<int:id>', methods=['DELETE'])
def delete_course(id: int):
    course = CourseHandler.get_course(id)
    
    if not course:
        return response(
            message="Cannot delete course that does not exist",
            code=404
        )
    
    CourseHandler.delete_course(id)
    
    return response(
        message=f"Course {course.name} deleted",
        code=200
    )

@app.route('/course', methods=['DELETE'])
def delete_courses():
    course_ids = request.args.getlist('ids', type=int)

    if not isinstance(course_ids, list) or not all(isinstance(id, int) for id in course_ids):
        return response(
            message="Course ids must be a list of integers",
            code=400
        )

    if not course_ids or not len(course_ids):
        return response(
            message="No course ids provided",
            code=400
        )

    CourseHandler.delete_courses_by_id(course_ids)
    
    return response(
        message="Courses deleted",
        code=200
    )
