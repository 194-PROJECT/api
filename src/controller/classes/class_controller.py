from flask import request
from core.api import Api, GetModelRequest, response

from database.model.classes import Class, ClassKeyEnum, ClassKeyTypes
from src.handler.classes.class_handler import ClassHandler

app = Api.application

@app.route('/class/<int:id>', methods=['GET'])
def get_class(id: int):
    class_ = ClassHandler.get_class(id)

    if not class_:
        return response(
            message="Class not found",
            code=404
        )

    return response(
        message=f"Class {class_.name} found",
        code=200,
        data=class_.model_dump()
    )

@app.route('/class', methods=['GET'])
def get_classes():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
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

    if not classes or not len(classes):
        return response(
            message="No classes found",
            code=404
        )

    return response(
        message="Classes found",
        code=200,
        data=[class_.model_dump() for class_ in classes]
    )

@app.route('/class', methods=['POST'])
def create_class():
    class_data = request.json
    new_class = ClassHandler.create_class(class_data)
    
    if not new_class:
        return response(
            message="Failed to create class",
            code=400
        )

    return response(
        message=f"Class {new_class.name} created",
        code=201,
        data=new_class.model_dump()
    )

@app.route('/class/<int:id>', methods=['PUT'])
def update_class(id: int):
    class_ = ClassHandler.get_class(id)

    if not class_:
        return response(
            message="Cannot update class that does not exist",
            code=404
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
            message="Cannot delete class that does not exist",
            code=404
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
            message="Class ids must be a list of integers",
            code=400
        )

    if not class_ids or not len(class_ids):
        return response(
            message="No class ids provided",
            code=400
        )

    ClassHandler.delete_classes_by_id(class_ids)
    
    return response(
        message="Classes deleted",
        code=200
    )
