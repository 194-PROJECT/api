from flask import request
from core.api import Api, GetModelRequest, response

from database.model.semester import Semester, SemesterKeyEnum, SemesterKeyTypes
from src.dto.semester.semester_dto import SemesterDTO
from src.handler.semester.semester_handler import SemesterHandler

app = Api.application

@app.route('/semester/<int:id>', methods=['GET'])
def get_semester(id: int):
    semester = SemesterHandler.get_semester(id)

    if not semester:
        return response(
            message="Semester not found",
            code=404,
            errors=["Failed to retrieve the requested semester"],
        )

    return response(
        message=f"Semester {semester.id} found",
        code=200,
        data=semester.model_dump()
    )

@app.route('/semester', methods=['GET'])
def get_semesters():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Semester,
        'table_keys': SemesterKeyEnum,
        'key_types': SemesterKeyTypes,
    })

    semesters = SemesterHandler.get_semesters(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not semesters or not len(semesters):
        return response(
            message="No semesters found",
            code=404,
            errors=["Failed to retrieve any semesters"],
        )

    return response(
        message="Semesters found",
        code=200,
        data=[semester.model_dump() for semester in semesters]
    )

@app.route('/semester', methods=['POST'])
def create_semester():
    semester_data = request.json
    semester = SemesterHandler.create_semester(SemesterDTO(**semester_data))

    if not semester:
        return response(
            message="Failed to create semester",
            code=400,
            errors=["Failed to create the semester with the provided data"],
        )

    return response(
        message=f"Semester {semester.id} created",
        code=201,
        data=semester.model_dump()
    )

@app.route('/semester/<int:id>', methods=['PUT'])
def update_semester(id: int):
    semester = SemesterHandler.get_semester(id)

    if not semester:
        return response(
            message="Semester not found",
            code=404,
            errors=["Cannot update semester that does not exist"],
        )

    semester_update_request = semester.model_copy(update=request.json)
    updated_semester = SemesterHandler.update_semester(id, semester_update_request)
    
    return response(
        message=f"Semester {updated_semester.id} updated",
        code=200,
        data=updated_semester.model_dump()
    )

@app.route('/semester/<int:id>', methods=['DELETE'])
def delete_semester(id: int):
    semester = SemesterHandler.get_semester(id)
    
    if not semester:
        return response(
            message="Semester not found",
            code=404,
            errors=["Cannot delete semester that does not exist"],
        )
    
    SemesterHandler.delete_semester(id)
    
    return response(
        message=f"Semester {semester.id} deleted",
        code=200
    )

@app.route('/semester', methods=['DELETE'])
def delete_semesters():
    semester_ids = request.args.getlist('ids', type=int)

    if not isinstance(semester_ids, list) or not all(isinstance(id, int) for id in semester_ids):
        return response(
            message="Invalid semester ids",
            code=400,
            errors=["Semester ids must be a list of integers"],
        )

    if not semester_ids or not len(semester_ids):
        return response(
            message="No semester ids provided",
            code=400,
            errors=["Please provide a list of semester ids to delete"],
        )

    SemesterHandler.delete_semesters_by_id(semester_ids)
    
    return response(
        message="Semesters deleted",
        code=200
    )
