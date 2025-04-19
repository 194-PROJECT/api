from flask import request
from core.api import Api, GetModelRequest, flatten_request_args, response
from database.model.reservation import ReservationKeyEnum, ReservationKeyTypes
from database.model.reservation_equipment import ReservationEquipment
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO
from src.enum.reservation_equipment.mishandle_type_enum import MishandleTypeEnum
from src.handler.equipment.equipment_item_handler import EquipmentItemHandler
from src.handler.reservation.reservation_equipment_handler import ReservationEquipmentHandler

app = Api.application

@app.route('/reservation/equipment/<int:equipment_id>', methods=['GET'])
def get_reservation_equipment(equipment_id: int):
    equipment = ReservationEquipmentHandler.get_reservation_equipment(equipment_id)

    if not equipment:
        return response(
            message="Equipment not found",
            code=404,
            errors=["Failed to retrieve the requested equipment"],
        )

    return response(
        message="Equipment found",
        code=200,
        data=equipment.model_dump(),
    )

@app.route('/reservation/equipment', methods=['GET'])
def get_all_reservation_equipments():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': ReservationEquipment,
        'table_keys': ReservationKeyEnum,
        'key_types': ReservationKeyTypes,
    })

    reservation_equipments = ReservationEquipmentHandler.get_reservation_equipments(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if reservation_equipments is None:
        return response(
            message="No equipment found",
            code=404,
            errors=["Failed to retrieve the requested equipment"],
        )

    reservation_equipment_count = ReservationEquipmentHandler.get_reservation_equipment_count(
        where_clause=get_request.where_clause,
    )

    return response(
        message="Equipment found",
        code=200,
        data=[
            reservation_equipment.model_dump()
            for reservation_equipment in reservation_equipments
        ],
        total_rows=reservation_equipment_count,
    )

@app.route('/reservation/<int:reservation_id>/equipment', methods=['GET'])
def get_reservation_equipments_from_reservation(reservation_id: int):
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': ReservationEquipment,
        'table_keys': ReservationKeyEnum,
        'key_types': ReservationKeyTypes,
    })

    reservation_equipments = ReservationEquipmentHandler.get_reservation_equipments(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
        reservation_id=reservation_id,
    )

    if reservation_equipments is None:
        return response(
            message="No equipment found",
            code=404,
            errors=["Failed to retrieve the requested equipment"],
        )

    reservation_equipment_count = ReservationEquipmentHandler.get_reservation_equipment_count(
        where_clause=get_request.where_clause,
        reservation_id=reservation_id,
    )

    return response(
        message="Equipment found",
        code=200,
        data=[
            reservation_equipment.model_dump()
            for reservation_equipment in reservation_equipments
        ],
        total_rows=reservation_equipment_count,
    )

@app.route('/reservation/equipment/data-request', methods=['GET'])
def get_reservation_equipment_with_data_request():
    get_request = GetModelRequest.model_validate(flatten_request_args(request), context={
        'model': ReservationEquipment,
        'table_keys': ReservationKeyEnum,
        'key_types': ReservationKeyTypes,
    })

    reservation_equipments = ReservationEquipmentHandler.get_reservation_equipments_with_data_request(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if reservation_equipments is None:
        return response(
            message="No equipment found",
            code=404,
            errors=["Failed to retrieve the requested equipment"],
        )

    reservation_equipment_count = ReservationEquipmentHandler.get_reservation_equipment_count(
        where_clause=get_request.where_clause,
        with_data_request=True,
    )

    return response(
        message="Equipment found",
        code=200,
        data=[
            reservation_equipment.model_dump()
            for reservation_equipment in reservation_equipments
        ],
        total_rows=reservation_equipment_count,
    )

@app.route('/reservation/<int:reservation_id>/equipment', methods=['POST'])
def add_reservation_equipment(reservation_id: int):
    equipment_data = request.json
    equipment = ReservationEquipmentDTO(**equipment_data)

    created_equipment = ReservationEquipmentHandler.add_reservation_equipment(equipment)

    if not created_equipment:
        return response(
            message="Failed to add equipment to the reservation",
            code=400,
            errors=["Failed to add the equipment with the provided data"],
        )

    return response(
        message="Equipment added to the reservation",
        code=201,
        data=created_equipment.model_dump(),
    )

@app.route('/reservation/equipment/<int:id>', methods=['PATCH'])
def update_reservation_equipment(id: int):
    reservation_equipment = ReservationEquipmentHandler.get_reservation_equipment(id)
    
    if not reservation_equipment:
        return response(
            message="Reservation equipment not found",
            code=404,
            errors=["Cannot update reservation equipment that does not exist"],
        )

    reservation_equipment_update_request = reservation_equipment.update(request.json)
    
    if not reservation_equipment_update_request.data_requested:
        reservation_equipment_update_request.data_requested = None
        reservation_equipment_update_request.data_request_description = None
        reservation_equipment_update_request.data_request_date = None
        reservation_equipment_update_request.data_received = None

    if not reservation_equipment_update_request.mishandled:
        reservation_equipment_update_request.mishandle_type = None
        reservation_equipment_update_request.mishandle_description = None

    if reservation_equipment_update_request.mishandle_type in (
        MishandleTypeEnum.NON_FUNCTIONAL,
        MishandleTypeEnum.LOST,
    ):
        equipment_item_id = reservation_equipment_update_request.equipment_item_id
        equipment_item = EquipmentItemHandler.get_equipment_item(equipment_item_id)
        if equipment_item is None:
            return response(
                message="Equipment item not found",
                code=404,
                errors=["Cannot update reservation equipment with a non-functional item that does not exist"],
            )

        equipment_item.update(data={"available": False})
        EquipmentItemHandler.update_equipment_item(equipment_item_id, equipment_item)

    reservation_equipment = ReservationEquipmentHandler.update_reservation_equipment(id, reservation_equipment_update_request)
    
    return response(
        message="Reservation equipment updated",
        code=200,
        data=reservation_equipment.model_dump()
    )

@app.route('/reservation/equipment/<int:id>', methods=['DELETE'])
def delete_reservation_equipment(id: int):
    ReservationEquipmentHandler.delete_reservation_equipment(id)

    return response(
        message="Equipment deleted from the reservation",
        code=200,
    )
