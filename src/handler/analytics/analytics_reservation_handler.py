from typing import Optional
from src.dto.analytics.bar_graph_data_dto import BarGraphDataDTO
from src.repository.analytics.analytics_reservation_repository import AnalyticsReservationRepository

class AnalyticsReservationHandler:
    @staticmethod
    def get_reservations_made_per_month() -> Optional[list[BarGraphDataDTO]]:
        return AnalyticsReservationRepository.get_reservations_made_per_month()

    @staticmethod
    def get_reservations_made_per_day() -> Optional[list[BarGraphDataDTO]]:
        return AnalyticsReservationRepository.get_reservations_made_per_day()

    @staticmethod
    def get_average_reservation_duration() -> Optional[list[BarGraphDataDTO]]:
        return AnalyticsReservationRepository.get_average_reservation_duration()
    
    @staticmethod
    def get_reservation_lead_time_distribution() -> Optional[list[BarGraphDataDTO]]:
        return AnalyticsReservationRepository.get_reservation_lead_time_distribution()

    @staticmethod
    def get_reservation_return_delay_distribution() -> Optional[list[BarGraphDataDTO]]:
        return AnalyticsReservationRepository.get_reservation_return_delay_distribution()