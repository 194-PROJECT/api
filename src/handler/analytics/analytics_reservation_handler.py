from typing import Optional
from src.dto.analytics.bar_graph_data_dto import BarGraphDataDTO
from src.repository.analytics.analytics_reservation_repository import AnalyticsReservationRepository

class AnalyticsReservationHandler:
    @staticmethod
    def get_reservations_made_per_month() -> Optional[list[BarGraphDataDTO]]:
        return AnalyticsReservationRepository.get_reservations_made_per_month()
