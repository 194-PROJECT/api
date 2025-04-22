from calendar import monthrange
import datetime
from typing import Optional

from sqlalchemy import String, extract, func, literal, select, union_all
from sqlalchemy.dialects import postgresql

from database.model.reservation import Reservation
from database.postgres.query import QueryExecutor
from src.dto.analytics.bar_graph_data_dto import BarGraphDataDTO

class AnalyticsReservationRepository:
    @staticmethod
    def get_reservations_made_per_month() -> Optional[list[BarGraphDataDTO]]:
        months = union_all(*[
            select(literal(i).label("month")) for i in range(1, 13)
        ]).alias("months")

        reservation_counts = (
            select(
                func.extract('month', Reservation.start_date).label("month"),
                func.count(Reservation.id).label("total")
            )
            .where(func.date_part('year', Reservation.start_date) == func.date_part('year', func.current_date()))
            .group_by(func.extract('month', Reservation.start_date))
        ).alias("counts")

        query = (
            select(
                func.to_char(
                    func.to_date(
                        func.concat(
                            func.date_part('year', func.current_date()),
                            '-',
                            func.lpad(months.c.month.cast(String), 2, '0'),
                            '-01'
                        ),
                        'YYYY-MM-DD'
                    ),
                    'Mon'
                ).label("name"),
                func.coalesce(reservation_counts.c.total, 0).label("total")
            )
            .select_from(months.outerjoin(reservation_counts, months.c.month == reservation_counts.c.month))
            .order_by(months.c.month)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [BarGraphDataDTO(**entry) for entry in data] if data else None

    @staticmethod
    def get_reservations_made_per_day() -> Optional[list[BarGraphDataDTO]]:
        today = datetime.date.today()
        year = today.year
        month = today.month
        num_days = monthrange(year, month)[1]  # number of days in the current month

        days = union_all(*[
            select(literal(i).label("day")) for i in range(1, num_days + 1)
        ]).alias("days")

        # Count reservations per day
        reservation_counts = (
            select(
                func.extract('day', Reservation.start_date).label("day"),
                func.count(Reservation.id).label("total")
            )
            .where(
                func.date_part('year', Reservation.start_date) == year,
                func.date_part('month', Reservation.start_date) == month
            )
            .group_by(func.extract('day', Reservation.start_date))
        ).alias("counts")

        # Build the full query
        query = (
            select(
                func.to_char(
                    func.to_date(
                        func.concat(
                            str(year),
                            '-',
                            func.lpad(str(month), 2, '0'),
                            '-',
                            func.lpad(days.c.day.cast(String), 2, '0')
                        ),
                        'YYYY-MM-DD'
                    ),
                    'FMDDth'  # Format like 1st, 2nd, 3rd, etc.
                ).label("name"),
                func.coalesce(reservation_counts.c.total, 0).label("total")
            )
            .select_from(days.outerjoin(reservation_counts, days.c.day == reservation_counts.c.day))
            .order_by(days.c.day)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [BarGraphDataDTO(**entry) for entry in data] if data else None

    @staticmethod
    def get_average_reservation_duration() -> Optional[list[BarGraphDataDTO]]:
        # Calculate the duration in hours and round to nearest 0.25
        duration_hours = (
            func.round(
                (func.extract('epoch', Reservation.end_date - Reservation.start_date) / 3600.0) * 4
            ) / 4.0
        ).label("duration")

        # Query to count how many reservations fall into each 0.25 hour bucket
        query = (
            select(
                func.to_char(duration_hours, 'FM999999.00').concat('h').label("name"),
                func.count(Reservation.id).label("total")
            )
            .where(
                Reservation.created_at >= func.date_trunc('year', func.current_date())
            )
            .group_by(duration_hours)
            .order_by(duration_hours)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [BarGraphDataDTO(**entry) for entry in data] if data else None
    
    @staticmethod
    def get_reservation_lead_time_distribution() -> Optional[list[BarGraphDataDTO]]:
        lead_time_buckets = (
            select(
                func.round(
                    extract('epoch', Reservation.start_date - Reservation.created_at) / 3600 * 4
                ).label("quarter_hour_bucket"),
                func.count(Reservation.id).label("total")
            )
            .where(
                Reservation.created_at >= func.date_trunc('year', func.current_date()),
                Reservation.returned
            )
            .group_by("quarter_hour_bucket")
            .order_by("quarter_hour_bucket")
            .alias("buckets")
        )

        query = (
            select(
                func.to_char((lead_time_buckets.c.quarter_hour_bucket / 4.0), 'FM999990.00').concat('h').label("name"),
                lead_time_buckets.c.total.label("total")
            )
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [BarGraphDataDTO(**entry) for entry in data] if data else None

    @staticmethod
    def get_reservation_return_delay_distribution() -> Optional[list[BarGraphDataDTO]]:
        delay_buckets = (
            select(
                func.round(
                    extract('epoch', Reservation.return_date - Reservation.end_date) / 3600 * 4
                ).label("quarter_hour_bucket"),
                func.count(Reservation.id).label("total")
            )
            .where(
                Reservation.returned,
                Reservation.created_at >= func.date_trunc('year', func.current_date())
            )
            .group_by("quarter_hour_bucket")
            .order_by("quarter_hour_bucket")
            .alias("buckets")
        )

        query = (
            select(
                func.to_char((delay_buckets.c.quarter_hour_bucket / 4.0), 'FM999990.00').concat('h').label("name"),
                delay_buckets.c.total.label("total")
            )
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [BarGraphDataDTO(**entry) for entry in data] if data else None