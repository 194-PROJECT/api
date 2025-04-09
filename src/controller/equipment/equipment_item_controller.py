from flask import request
from core.api import Api, GetModelRequest, flatten_request_args, response

from database.model.equipment_item import EquipmentItem, EquipmentItemKeyEnum, EquipmentItemKeyTypes
from src.dto.equipment.equipment_item_dto import EquipmentItemDTO
from src.handler.equipment.equipment_item_handler import EquipmentItemHandler

app = Api.application

@app.route('/equipment/item/<int:id>', methods=['GET'])
def get_equipment_item(id: int):
    equipment_item = EquipmentItemHandler.get_equipment_item(id)

    if not equipment_item:
        return response(
            message="Equipment item not found",
            code=404,
            errors=["Failed to retrieve the requested equipment item"],
        )

    return response(
        message=f"Equipment item {equipment_item.item_code} found",
        code=200,
        data=equipment_item.model_dump()
    )

@app.route('/equipment/item', methods=['GET'])
def get_equipment_items():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': EquipmentItem,
        'table_keys': EquipmentItemKeyEnum,
        'key_types': EquipmentItemKeyTypes,
    })

    equipment_items = EquipmentItemHandler.get_equipment_items(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not equipment_items:
        return response(
            message="No equipment items found",
            code=404,
            errors=["Failed to retrieve equipment items"],
        )
    
    equipment_item_count = EquipmentItemHandler.get_equipment_item_count(get_request.where_clause)

    return response(
        message="Equipment items retrieved",
        code=200,
        data=[item.model_dump() for item in equipment_items],
        total_rows=equipment_item_count,
    )

@app.route('/equipment/<int:equipment_id>/item', methods=['GET'])
def get_items_by_equipment(equipment_id: int):
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': EquipmentItem,
        'table_keys': EquipmentItemKeyEnum,
        'key_types': EquipmentItemKeyTypes,
    })

    equipment_items = EquipmentItemHandler.get_equipment_items(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
        equipment_id,
    )

    if not equipment_items:
        return response(
            message="No items found for the specified equipment",
            code=404,
            errors=["Failed to retrieve items for the specified equipment"],
        )
    
    equipment_item_count = EquipmentItemHandler.get_equipment_item_count(get_request.where_clause)

    return response(
        message=f"Items for equipment {equipment_id} retrieved",
        code=200,
        data=[item.model_dump() for item in equipment_items],
        total_rows=equipment_item_count,
    )

@app.route('/equipment/item', methods=['POST'])
def create_equipment_item():
    equipment_item_data = EquipmentItemDTO(**request.json)
    equipment_item = EquipmentItemHandler.create_equipment_item(equipment_item_data)

    if not equipment_item:
        return response(
            message="Failed to create equipment item",
            code=400,
            errors=["Failed to create equipment item from the provided data"],
        )

    return response(
        message=f"Equipment item {equipment_item.item_code} created",
        code=201,
        data=equipment_item.model_dump()
    )

@app.route('/equipment/item/<int:id>', methods=['PATCH'])
def update_equipment_item(id: int):
    equipment_item = EquipmentItemHandler.get_equipment_item(id)

    if not equipment_item:
        return response(
            message="Equipment item not found",
            code=404,
            errors=["Failed to retrieve the requested equipment item for update"],
        )

    equipment_item_update_request = equipment_item.model_validate(obj=request.json)
    updated_equipment_item = EquipmentItemHandler.update_equipment_item(id, equipment_item_update_request)

    return response(
        message=f"Equipment item {updated_equipment_item.item_code} updated",
        code=200,
        data=updated_equipment_item.model_dump()
    )

@app.route('/equipment/item/<int:id>', methods=['DELETE'])
def delete_equipment_item(id: int):
    equipment_item = EquipmentItemHandler.get_equipment_item(id)

    if not equipment_item:
        return response(
            message="Equipment item not found",
            code=404,
            errors=["Failed to retrieve the requested equipment item for deletion"],
        )

    EquipmentItemHandler.delete_equipment_item(id)

    return response(
        message=f"Equipment item {equipment_item.item_code} deleted",
        code=200
    )
