from flask import request
from core.api import Api, GetModelRequest, flatten_request_args, response

from database.model.program import Program, ProgramKeyEnum, ProgramKeyTypes
from src.dto.program.program_dto import ProgramDTO
from src.handler.program.program_handler import ProgramHandler

app = Api.application

@app.route('/program/<int:id>', methods=['GET'])
def get_program(id: int):
    program = ProgramHandler.get_program(id)

    if not program:
        return response(
            message="Program not found",
            code=404,
            errors=["Failed to retrieve the requested program"],
        )

    return response(
        message=f"Program {program.title} found",
        code=200,
        data=program.model_dump()
    )

@app.route('/program', methods=['GET'])
def get_programs():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': Program,
        'table_keys': ProgramKeyEnum,
        'key_types': ProgramKeyTypes,
    })

    programs = ProgramHandler.get_programs(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if programs is None:
        return response(
            message="No programs found",
            code=404,
            errors=["Failed to retrieve any programs"],
        )

    program_count = ProgramHandler.get_program_count(get_request.where_clause)

    return response(
        message="Programs found",
        code=200,
        data=[program.model_dump() for program in programs],
        page=get_request.page,
        total_rows=program_count,
    )

@app.route('/program/count', methods=['GET'])
def get_program_count():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': Program,
        'table_keys': ProgramKeyEnum,
        'key_types': ProgramKeyTypes,
    })

    program_count = ProgramHandler.get_program_count(get_request.where_clause)

    return response(
        message="Program count found",
        code=200,
        data=program_count
    )

@app.route('/program', methods=['POST'])
def create_program():
    program_data = ProgramDTO(**request.json)
    program = ProgramHandler.create_program(program_data)
    
    if not program:
        return response(
            message="Failed to create program",
            code=400,
            errors=["Failed to create the program with the provided data"],
        )
    
    return response(
        message=f"Program {program.title} created",
        code=201,
        data=program.model_dump()
    )

@app.route('/program/<int:id>', methods=['PATCH'])
def update_program(id: int):
    program = ProgramHandler.get_program(id)

    if not program:
        return response(
            message="Program not found",
            code=404,
            errors=["Cannot update program that does not exist"],
        )

    program_update_request = program.model_copy(update=request.json)
    updated_program = ProgramHandler.update_program(id, program_update_request)
    
    return response(
        message=f"Program {updated_program.title} updated",
        code=200,
        data=updated_program.model_dump()
    )

@app.route('/program/<int:id>', methods=['DELETE'])
def delete_program(id: int):
    program = ProgramHandler.get_program(id)
    
    if not program:
        return response(
            message="Program not found",
            code=404,
            errors=["Cannot delete program that does not exist"],
        )
    
    ProgramHandler.delete_program(id)
    
    return response(
        message=f"Program {program.title} deleted",
        code=200
    )

@app.route('/program', methods=['DELETE'])
def delete_programs():
    program_ids = request.args.getlist('ids', type=int)

    if not isinstance(program_ids, list) or not all(isinstance(id, int) for id in program_ids):
        return response(
            message="Invalid program ids provided",
            code=400,
            errors=["Program ids must be a list of integers"],
        )

    if not program_ids or not len(program_ids):
        return response(
            message="No program ids provided",
            code=400,
            errors=["Please provide a list of program ids to delete"],
        )

    ProgramHandler.delete_programs_by_id(program_ids)
    
    return response(
        message="Programs deleted",
        code=200
    )
