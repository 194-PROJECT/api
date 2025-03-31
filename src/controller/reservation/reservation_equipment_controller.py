from flask import request
from core.api import Api, response
from src.dto.reservation.reservation_equipment_dto import ReservationEquipmentDTO
from src.handler.reservation.reservation_equipment_handler import ReservationEquipmentHandler

app = Api.application

@app.route('/reservation/<int:reservation_id>/equipment', methods=['GET'])
def get_reservation_equipment(reservation_id: int):
    equipment = ReservationEquipmentHandler.get_reservation_equipment(reservation_id)

    if not equipment:
        return response(
            message="No equipment found for the reservation",
            code=404,
            errors=["Failed to retrieve equipment for the reservation"],
        )

    return response(
        message="Equipment found for the reservation",
        code=200,
        data=[item.model_dump() for item in equipment],
    )

@app.route('/reservation/<int:reservation_id>/equipment', methods=['POST'])
def add_reservation_equipment(reservation_id: int):
    equipment_data = request.json
    equipment = ReservationEquipmentDTO(**equipment_data, reservation_id=reservation_id)

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

@app.route('/reservation/<int:reservation_id>/equipment/<int:equipment_id>', methods=['DELETE'])
def delete_reservation_equipment(reservation_id: int, equipment_id: int):
    success = ReservationEquipmentHandler.delete_reservation_equipment(reservation_id, equipment_id)

    if not success:
        return response(
            message="Failed to delete equipment from the reservation",
            code=400,
            errors=["Failed to delete the specified equipment"],
        )

    return response(
        message="Equipment deleted from the reservation",
        code=200,
    )