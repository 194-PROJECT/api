from flask import request
from core.api import Api, GetModelRequest, response

from database.model.equipment import Equipment, EquipmentKeyEnum, EquipmentKeyTypes
from src.handler.equipment.equipment_handler import EquipmentHandler

app = Api.application

@app.route('/equipment/<int:id>', methods=['GET'])
def get_equipment(id: int):
    equipment = EquipmentHandler.get_equipment(id)

    if not equipment:
        return response(
            message="Equipment not found",
            code=404
        )

    return response(
        message=f"Equipment {equipment.name} found",
        code=200,
        data=equipment.model_dump()
    )

@app.route('/equipment', methods=['GET'])
def get_equipments():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Equipment,
        'table_keys': EquipmentKeyEnum,
        'key_types': EquipmentKeyTypes,
    })

    equipments = EquipmentHandler.get_equipments(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not equipments or not len(equipments):
        return response(
            message="No equipments found",
            code=404
        )

    return response(
        message="Equipments found",
        code=200,
        data=[equipment.model_dump() for equipment in equipments]
    )

@app.route('/equipment', methods=['POST'])
def create_equipment():
    equipment_data = request.json
    equipment = EquipmentHandler.create_equipment(equipment_data)
    
    if not equipment:
        return response(
            message="Failed to create equipment",
            code=400
        )

    return response(
        message=f"Equipment {equipment.name} created",
        code=201,
        data=equipment.model_dump()
    )

@app.route('/equipment/<int:id>', methods=['PUT'])
def update_equipment(id: int):
    equipment = EquipmentHandler.get_equipment(id)

    if not equipment:
        return response(
            message="Cannot update equipment that does not exist",
            code=404
        )

    equipment_update_request = equipment.model_copy(update=request.json)
    updated_equipment = EquipmentHandler.update_equipment(id, equipment_update_request)
    
    return response(
        message=f"Equipment {updated_equipment.name} updated",
        code=200,
        data=updated_equipment.model_dump()
    )

@app.route('/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id: int):
    equipment = EquipmentHandler.get_equipment(id)
    
    if not equipment:
        return response(
            message="Cannot delete equipment that does not exist",
            code=404
        )
    
    EquipmentHandler.delete_equipment(id)
    
    return response(
        message=f"Equipment {equipment.name} deleted",
        code=200
    )

@app.route('/equipment', methods=['DELETE'])
def delete_equipments():
    equipment_ids = request.args.getlist('ids', type=int)

    if not isinstance(equipment_ids, list) or not all(isinstance(id, int) for id in equipment_ids):
        return response(
            message="Equipment ids must be a list of integers",
            code=400
        )

    if not equipment_ids or not len(equipment_ids):
        return response(
            message="No equipment ids provided",
            code=400
        )

    EquipmentHandler.delete_equipments_by_id(equipment_ids)
    
    return response(
        message="Equipments deleted",
        code=200
    )
