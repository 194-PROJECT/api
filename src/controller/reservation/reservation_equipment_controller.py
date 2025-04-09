from flask import request
from core.api import Api, response
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO
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

@app.route('/reservation/<int:reservation_id>/equipment', methods=['GET'])
def get_reservation_equipments(reservation_id: int):
    reservation_equipments = ReservationEquipmentHandler.get_reservation_equipments(reservation_id)

    if reservation_equipments is None:
        return response(
            message="No equipment found for the reservation",
            code=404,
            errors=["Failed to retrieve equipment for the reservation"],
        )

    return response(
        message="Equipment found for the reservation",
        code=200,
        data=[
            reservation_equipment.model_dump()
            for reservation_equipment in reservation_equipments
        ],
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
    print(reservation_equipment_update_request)
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
