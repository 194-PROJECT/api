from database.postgres.query import QueryExecutor
from database.model.asset import Asset
from sqlalchemy import TextClause, delete, insert, select, update
from sqlalchemy.dialects import postgresql
from typing import Optional

from src.dto.asset.asset_dto import AssetDTO

class AssetRepository:
    @staticmethod
    def create_asset(asset: AssetDTO) -> Optional[AssetDTO]:
        query = (
            insert(Asset)
            .values(
                name=asset.name,
                description=asset.description,
                category=asset.category,
                purchase_date=asset.purchase_date,
                price=asset.price,
                purchased_by=asset.purchased_by,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return AssetDTO(**data) if data else None
    
    @staticmethod
    def get_asset(id: int) -> Optional[AssetDTO]:
        query = select(Asset).where(Asset.id == id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return AssetDTO(**data) if data else None

    @staticmethod
    def get_assets(
        limit: int,
        offset: int,
        order_by_clause: Optional[TextClause],
        where_clause: Optional[TextClause],
    ) -> Optional[list[AssetDTO]]:
        query = select(Asset).order_by(order_by_clause)

        if where_clause is not None:
            query = query.where(where_clause)

        query = (
            query
            .limit(limit)
            .offset(offset)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )

        data = QueryExecutor.fetch_all(str(query))
        return [AssetDTO(**asset) for asset in data] if data else None

    @staticmethod
    def update_asset(id: int, asset: AssetDTO) -> Optional[AssetDTO]:
        query = (
            update(Asset)
            .where(Asset.id == id)
            .values(
                name=asset.name,
                description=asset.description,
                category=asset.category,
                purchase_date=asset.purchase_date,
                price=asset.price,
                purchased_by=asset.purchased_by,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.update_one(str(query))
        return AssetDTO(**data) if data else None

    @staticmethod
    def delete_asset(id: int) -> None:
        query = (
            delete(Asset)
            .where(Asset.id == id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))

    @staticmethod
    def delete_assets_by_id(ids: list[int]) -> None:
        query = (
            delete(Asset)
            .where(Asset.id.in_(ids))
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_many(str(query))
