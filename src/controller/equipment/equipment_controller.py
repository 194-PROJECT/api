from flask import request
from core.api import Api, GetModelRequest, response

from database.model.equipment import Equipment, EquipmentKeyEnum, EquipmentKeyTypes
from database.model.reservation import Reservation, ReservationKeyEnum, ReservationKeyTypes
from src.dto.equipment.equipment_dto import EquipmentDTO
from src.handler.equipment.equipment_handler import EquipmentHandler

app = Api.application

@app.route('/equipment/<int:id>', methods=['GET'])
def get_equipment(id: int):
    equipment = EquipmentHandler.get_equipment(id)

    if not equipment:
        return response(
            message="Equipment not found",
            code=404,
            errors=["Failed to retrieve the requested equipment"],
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
            code=404,
            errors=["Failed to retrieve any equipments"],
        )

    equipment_count = EquipmentHandler.get_equipment_count(get_request.where_clause)

    return response(
        message="Equipments found",
        code=200,
        data=[equipment.model_dump() for equipment in equipments],
        page=get_request.page,
        total_rows=equipment_count,
    )

@app.route('/equipment/count', methods=['GET'])
def get_equipment_count():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Equipment,
        'table_keys': EquipmentKeyEnum,
        'key_types': EquipmentKeyTypes,
    })

    equipment_count = EquipmentHandler.get_equipment_count(get_request.where_clause)

    return response(
        message="Equipment count found",
        code=200,
        data=equipment_count
    )

@app.route('/equipment/<int:id>/reservation', methods=['GET'])
def get_equipment_reservations(id: int):
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Reservation,
        'table_keys': ReservationKeyEnum,
        'key_types': ReservationKeyTypes,
    })

    equipment = EquipmentHandler.get_equipment(id)

    if not equipment:
        return response(
            message="Equipment not found",
            code=404,
            errors=["Failed to retrieve the requested reservations for equipment"],
        )

    reservations = EquipmentHandler.get_equipment_reservations(
        id=id,
        limit=get_request.limit,
        offset=get_request.offset,
        order_by_clause=get_request.order_by_clause,
        where_clause=get_request.where_clause,
    )

    if not reservations or not len(reservations):
        return response(
            message="No reservations found for the equipment",
            code=200,
            data=[],
            errors=["Failed to retrieve any reservations for the equipment"],
        )

    return response(
        message=f"Reservations for Equipment {equipment.name} found",
        code=200,
        data=[reservation.model_dump() for reservation in reservations],
    )

@app.route('/equipment', methods=['POST'])
def create_equipment():
    equipment_data = EquipmentDTO(**request.json)
    equipment = EquipmentHandler.create_equipment(equipment_data)
    
    if not equipment:
        return response(
            message="Failed to create equipment",
            code=400,
            errors=["Failed to create equipment from the provided data"],
        )

    return response(
        message=f"Equipment {equipment.name} created",
        code=201,
        data=equipment.model_dump()
    )

@app.route('/equipment/<int:id>', methods=['PATCH'])
def update_equipment(id: int):
    equipment = EquipmentHandler.get_equipment(id)

    if not equipment:
        return response(
            message="Equipment not found",
            code=404,
            errors=["Failed to retrieve the requested equipment for update"],
        )

    equipment_update_request = equipment.model_validate(obj=request.json)
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
            message="Equipment not found",
            code=404,
            errors=["Failed to retrieve the requested equipment for deletion"],
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
            message="Invalid equipment ids provided",
            code=400,
            errors=["Equipment ids must be a list of integers"],
        )

    if not equipment_ids or not len(equipment_ids):
        return response(
            message="No equipment ids provided",
            code=400,
            errors=["Please provide a list of equipment ids to delete"],
        )

    EquipmentHandler.delete_equipments_by_id(equipment_ids)
    
    return response(
        message="Equipments deleted",
        code=200
    )
