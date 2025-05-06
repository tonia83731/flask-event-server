from app import db
from app.model.base import Base
from sqlalchemy import func
from sqlalchemy.orm import relationship


class UserSchema(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(512), unique=True, nullable=False)
    phone = db.Column(db.String(255))
    address = db.Column(db.String(255))

    # 帳號是否啟用
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    # 是否為管理員
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=func.now())  # Set automatically when created
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())  # Auto-update

    
    # Relationship
    # backref: 自動設定雙向關聯性(只需在一個模型中設定，另一方關聯會自動建立)
    # back_populates: 在兩邊都需明確定義關聯屬性，並指定對應關聯
    events = relationship("EventSchema", back_populates="admin")
    bookings = relationship("BookingSchema", back_populates="user")

    def to_dict(self):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()
        t.pop('password', None)
        
        return t