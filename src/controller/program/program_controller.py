from flask import request
from core.api import Api, GetModelRequest, response

from database.model.program import Program, ProgramKeyEnum, ProgramKeyTypes
from src.handler.program.program_handler import ProgramHandler

app = Api.application

@app.route('/program/<int:id>', methods=['GET'])
def get_program(id: int):
    program = ProgramHandler.get_program(id)

    if not program:
        return response(
            message="Program not found",
            code=404
        )

    return response(
        message=f"Program {program.title} found",
        code=200,
        data=program.model_dump()
    )

@app.route('/program', methods=['GET'])
def get_programs():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
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

    if not programs or not len(programs):
        return response(
            message="No programs found",
            code=404
        )

    return response(
        message="Programs found",
        code=200,
        data=[program.model_dump() for program in programs]
    )

@app.route('/program', methods=['POST'])
def create_program():
    program_data = request.json
    program = ProgramHandler.create_program(program_data)
    
    if not program:
        return response(
            message="Failed to create program",
            code=400
        )
    
    return response(
        message=f"Program {program.title} created",
        code=201,
        data=program.model_dump()
    )

@app.route('/program/<int:id>', methods=['PUT'])
def update_program(id: int):
    program = ProgramHandler.get_program(id)

    if not program:
        return response(
            message="Cannot update program that does not exist",
            code=404
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
            message="Cannot delete program that does not exist",
            code=404
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
            message="Program ids must be a list of integers",
            code=400
        )

    if not program_ids or not len(program_ids):
        return response(
            message="No program ids provided",
            code=400
        )

    ProgramHandler.delete_programs_by_id(program_ids)
    
    return response(
        message="Programs deleted",
        code=200
    )
