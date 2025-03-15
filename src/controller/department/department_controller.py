from flask import request
from core.api import Api, GetModelRequest, response

from database.model.department import Department, DepartmentKeyEnum, DepartmentKeyTypes
from src.handler.department.department_handler import DepartmentHandler

app = Api.application

@app.route('/department/<int:id>', methods=['GET'])
def get_department(id: int):
    department = DepartmentHandler.get_department(id)

    if not department:
        return response(
            message="Department not found",
            code=404,
            errors=["Failed to retrieve the requested department"],
        )

    return response(
        message=f"Department {department.name} found",
        code=200,
        data=department.model_dump()
    )

@app.route('/department', methods=['GET'])
def get_departments():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Department,
        'table_keys': DepartmentKeyEnum,
        'key_types': DepartmentKeyTypes,
    })

    departments = DepartmentHandler.get_departments(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not departments or not len(departments):
        return response(
            message="No departments found",
            code=404,
            errors=["Failed to retrieve any departments"],
        )

    return response(
        message="Departments found",
        code=200,
        data=[department.model_dump() for department in departments]
    )

@app.route('/department', methods=['POST'])
def create_department():
    department_data = request.json
    department = DepartmentHandler.create_department(department_data)
    
    return response(
        message=f"Department {department.name} created",
        code=201,
        data=department.model_dump()
    )

@app.route('/department/<int:id>', methods=['PUT'])
def update_department(id: int):
    department = DepartmentHandler.get_department(id)

    if not department:
        return response(
            message="Department not found",
            code=404,
            errors=["Department does not exist"],
        )

    department_update_request = department.model_copy(update=request.json)
    updated_department = DepartmentHandler.update_department(id, department_update_request)
    
    return response(
        message=f"Department {updated_department.name} updated",
        code=200,
        data=updated_department.model_dump()
    )

@app.route('/department/<int:id>', methods=['DELETE'])
def delete_department(id: int):
    department = DepartmentHandler.get_department(id)
    
    if not department:
        return response(
            message="Department not found",
            code=404,
            errors=["Cannot delete department that does not exist"],
        )
    
    DepartmentHandler.delete_department(id)
    
    return response(
        message=f"Department {department.name} deleted",
        code=200
    )

@app.route('/department', methods=['DELETE'])
def delete_departments():
    department_ids = request.args.getlist('ids', type=int)

    if not isinstance(department_ids, list) or not all(isinstance(id, int) for id in department_ids):
        return response(
            message="Invalid department ids",
            code=400,
            errors=["Department ids must be a list of integers"],
        )

    if not department_ids or not len(department_ids):
        return response(
            message="No department ids provided",
            code=400,
            errors=["Please provide a list of department ids to delete"],
        )

    DepartmentHandler.delete_departments_by_id(department_ids)
    
    return response(
        message="Departments deleted",
        code=200
    )
