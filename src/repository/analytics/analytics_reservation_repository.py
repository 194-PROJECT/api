from typing import Optional

from sqlalchemy import String, func, literal, select, union_all
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
