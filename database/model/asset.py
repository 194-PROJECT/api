from enum import Enum
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.users import User

class Asset(Base):
    __tablename__ = 'asset'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255))
    category = Column(String(255), index=True)
    purchase_date = Column(Date, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    purchased_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now())
    # 'From' Relationships
    user = orm.relationship(User, back_populates="purchased_assets", foreign_keys=[purchased_by])
    # 'To' Relationships
    asset_images = orm.relationship("AssetImage", back_populates="asset")

AssetKeyEnum = Enum('AssetKeyEnum', {
    column.capitalize(): column for column in Asset.__table__.columns.keys()
}, type=str)

AssetKeyTypes = {
    column.value: Asset.__table__.columns[column].type.python_type for column in AssetKeyEnum
}
