from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.asset.asset_dto import AssetDTO
from src.repository.asset.asset_repository import AssetRepository

class AssetHandler:
    @staticmethod
    def create_asset(asset: AssetDTO) -> Optional[AssetDTO]:
        return AssetRepository.create_asset(asset)

    @staticmethod
    def get_asset(id: int) -> Optional[AssetDTO]:
        return AssetRepository.get_asset(id)

    @staticmethod
    def get_assets(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[AssetDTO]]:
        return AssetRepository.get_assets(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def get_asset_count(where_clause: Optional[str]) -> int:
        return AssetRepository.get_asset_count(where_clause)

    @staticmethod
    def update_asset(id: int, asset: AssetDTO) -> Optional[AssetDTO]:
        return AssetRepository.update_asset(id, asset)

    @staticmethod
    def delete_asset(id: int) -> None:
        AssetRepository.delete_asset(id)

    @staticmethod
    def delete_assets_by_id(ids: List[int]) -> None:
        AssetRepository.delete_assets_by_id(ids)
