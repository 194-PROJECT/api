from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.asset import Asset

class AssetImage(Base):
    __tablename__ = 'asset_image'
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('asset.id'), nullable=False, index=True)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    asset = orm.relationship(Asset, back_populates="asset_images", foreign_keys=[asset_id])

AssetImageKeyEnum = Enum('AssetImageKeyEnum', {
    column.capitalize(): column for column in AssetImage.__table__.columns.keys()
}, type=str)

AssetImageKeyTypes = {
    column.value: AssetImage.__table__.columns[column].type.python_type for column in AssetImageKeyEnum
}