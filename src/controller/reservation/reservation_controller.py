from flask import request
from core.api import Api, GetModelRequest, response

from database.model.reservation import Reservation, ReservationKeyEnum, ReservationKeyTypes
from src.dto.reservation.reservation_dto import ReservationDTO
from src.handler.reservation.reservation_handler import ReservationHandler

app = Api.application

@app.route('/reservation/<int:id>', methods=['GET'])
def get_reservation(id: int):
    reservation = ReservationHandler.get_reservation(id)

    if not reservation:
        return response(
            message="Reservation not found",
            code=404
        )

    return response(
        message=f"Reservation {reservation.id} found",
        code=200,
        data=reservation.model_dump()
    )

@app.route('/reservation', methods=['GET'])
def get_reservations():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Reservation,
        'table_keys': ReservationKeyEnum,
        'key_types': ReservationKeyTypes,
    })

    reservations = ReservationHandler.get_reservations(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not reservations or not len(reservations):
        return response(
            message="No reservations found",
            code=404
        )

    return response(
        message="Reservations found",
        code=200,
        data=[reservation.model_dump() for reservation in reservations]
    )

@app.route('/reservation', methods=['POST'])
def create_reservation():
    reservation_data = request.json
    reservation = ReservationDTO(**reservation_data)
    created_reservation = ReservationHandler.create_reservation(reservation)
    
    return response(
        message=f"Reservation {created_reservation.id} created",
        code=201,
        data=created_reservation.model_dump()
    )

@app.route('/reservation/<int:id>', methods=['PUT'])
def update_reservation(id: int):
    reservation = ReservationHandler.get_reservation(id)

    if not reservation:
        return response(
            message="Cannot update reservation that does not exist",
            code=404
        )

    reservation_update_request = reservation.model_copy(update=request.json)
    updated_reservation = ReservationHandler.update_reservation(id, reservation_update_request)
    
    return response(
        message=f"Reservation {updated_reservation.id} updated",
        code=200,
        data=updated_reservation.model_dump()
    )

@app.route('/reservation/<int:id>', methods=['DELETE'])
def delete_reservation(id: int):
    reservation = ReservationHandler.get_reservation(id)
    
    if not reservation:
        return response(
            message="Cannot delete reservation that does not exist",
            code=404
        )
    
    ReservationHandler.delete_reservation(id)
    
    return response(
        message=f"Reservation {reservation.id} deleted",
        code=200
    )

@app.route('/reservation', methods=['DELETE'])
def delete_reservations():
    reservation_ids = request.args.getlist('ids', type=int)

    if not isinstance(reservation_ids, list) or not all(isinstance(id, int) for id in reservation_ids):
        return response(
            message="Reservation ids must be a list of integers",
            code=400
        )

    if not reservation_ids or not len(reservation_ids):
        return response(
            message="No reservation ids provided",
            code=400
        )

    ReservationHandler.delete_reservations_by_id(reservation_ids)
    
    return response(
        message="Reservations deleted",
        code=200
    )
