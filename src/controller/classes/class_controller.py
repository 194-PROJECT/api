from flask import request
from core.api import Api, GetModelRequest, flatten_request_args, response

from database.model.classes import Class, ClassKeyEnum, ClassKeyTypes
from src.dto.classes.class_dto import ClassDTO
from src.handler.classes.class_handler import ClassHandler

app = Api.application

@app.route('/class/<int:id>', methods=['GET'])
def get_class(id: int):
    class_ = ClassHandler.get_class(id)

    if not class_:
        return response(
            message="Class not found",
            code=404,
            errors=["Failed to retrieve the requested class data"],
        )

    return response(
        message=f"Class {class_.name} found",
        code=200,
        data=class_.model_dump()
    )

@app.route('/class', methods=['GET'])
def get_classes():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': Class,
        'table_keys': ClassKeyEnum,
        'key_types': ClassKeyTypes,
    })

    classes = ClassHandler.get_classes(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if classes is None:
        return response(
            message="No classes found",
            code=404,
            errors=["Failed to retrieve any classes"],
        )

    class_count = ClassHandler.get_class_count(get_request.where_clause)

    return response(
        message="Classes found",
        code=200,
        data=[class_.model_dump() for class_ in classes],
        page=get_request.page,
        total_rows=class_count,
    )

@app.route('/class/count', methods=['GET'])
def get_class_count():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': Class,
        'table_keys': ClassKeyEnum,
        'key_types': ClassKeyTypes,
    })

    class_count = ClassHandler.get_class_count(get_request.where_clause)

    return response(
        message="Class count found",
        code=200,
        data=class_count
    )

@app.route('/class', methods=['POST'])
def create_class():
    class_data = ClassDTO(**request.json)
    new_class = ClassHandler.create_class(class_data)
    
    if not new_class:
        return response(
            message="Failed to create class",
            code=400,
            errors=["Failed to create the class with the provided data"],
        )

    return response(
        message=f"Class {new_class.name} created",
        code=201,
        data=new_class.model_dump()
    )

@app.route('/class/<int:id>', methods=['PATCH'])
def update_class(id: int):
    class_ = ClassHandler.get_class(id)

    if not class_:
        return response(
            message="Class not found",
            code=404,
            errors=["Cannot update class that does not exist"],
        )

    class_update_request = class_.model_copy(update=request.json)
    updated_class = ClassHandler.update_class(id, class_update_request)
    
    return response(
        message=f"Class {updated_class.name} updated",
        code=200,
        data=updated_class.model_dump()
    )

@app.route('/class/<int:id>', methods=['DELETE'])
def delete_class(id: int):
    class_ = ClassHandler.get_class(id)
    
    if not class_:
        return response(
            message="Class not found",
            code=404,
            errors=["Cannot delete class that does not exist"]
        )
    
    ClassHandler.delete_class(id)
    
    return response(
        message=f"Class {class_.name} deleted",
        code=200
    )

@app.route('/class', methods=['DELETE'])
def delete_classes():
    class_ids = request.args.getlist('ids', type=int)

    if not isinstance(class_ids, list) or not all(isinstance(id, int) for id in class_ids):
        return response(
            message="Invalid course ids provided",
            code=400,
            errors=["Class ids must be a list of integers"]
        )

    if not class_ids or not len(class_ids):
        return response(
            message="No class ids provided",
            code=400,
            errors=["Please provide class ids to delete"],
        )

    ClassHandler.delete_classes_by_id(class_ids)
    
    return response(
        message="Classes deleted",
        code=200
    )
