from core.api import Api, response

from src.handler.analytics.analytics_reservation_handler import AnalyticsReservationHandler

app = Api.application

@app.route('/analytics/reservation/count/month', methods=['GET'])
def get_reservation_count_by_month():
    dataset = AnalyticsReservationHandler.get_reservations_made_per_month()

    if dataset is None:
        return response(
            message="No data found",
            code=404,
            data=None,
        )

    return response(
        message="Reservations made per month",
        code=200,
        data=[entry.model_dump() for entry in dataset],
    )

@app.route('/analytics/reservation/count/day', methods=['GET'])
def get_reservation_count_by_day():
    dataset = AnalyticsReservationHandler.get_reservations_made_per_day()

    if dataset is None:
        return response(
            message="No data found",
            code=404,
            data=None,
        )

    return response(
        message="Reservations made per day",
        code=200,
        data=[entry.model_dump() for entry in dataset],
    )

@app.route('/analytics/reservation/average/duration', methods=['GET'])
def get_average_reservation_duration():
    dataset = AnalyticsReservationHandler.get_average_reservation_duration()

    if dataset is None:
        return response(
            message="No data found",
            code=404,
            data=None,
        )

    return response(
        message="Reservations average hourly",
        code=200,
        data=[entry.model_dump() for entry in dataset],
    )

@app.route('/analytics/reservation/distribution/lead-time', methods=['GET'])
def get_reservation_distribution_lead_time():
    dataset = AnalyticsReservationHandler.get_reservation_lead_time_distribution()

    if dataset is None:
        return response(
            message="No data found",
            code=404,
            data=None,
        )

    return response(
        message="Reservations lead time distribution",
        code=200,
        data=[entry.model_dump() for entry in dataset],
    )

@app.route('/analytics/reservation/distribution/return-delay', methods=['GET'])
def get_reservation_distribution_return_delay():
    dataset = AnalyticsReservationHandler.get_reservation_return_delay_distribution()

    if dataset is None:
        return response(
            message="No data found",
            code=404,
            data=None,
        )

    return response(
        message="Reservations return delay distribution",
        code=200,
        data=[entry.model_dump() for entry in dataset],
    )
