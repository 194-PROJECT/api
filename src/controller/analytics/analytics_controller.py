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
