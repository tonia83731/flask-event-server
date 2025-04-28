from app import db
from app.model.base import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

class BookingSchema(Base):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('events.id'), nullable=False)
    
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    
    status = db.Column(db.Integer, default=0, nullable=False)
    # PENDING: 0, CONFIRMED: 1, COMPLETED: 2, CANCELED: 3
    # payment_status = db.Column(db.Integer, default=0, nullable=False)
    # PENDING: 0, SUCCESS: 1, FAILED: 2
    qrcode_id = db.Column(db.Integer, ForeignKey('qrcode.id'))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    users = relationship("UserSchema", back_populates="bookings")
    events = relationship("EventSchema", back_populates="bookings")
    # qrcode = relationship("QRcodeSchema", back_populates="bookings")

    def to_dict(self, include_user=False, include_event=False):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()

        if include_user:
            t['user'] = self.users.to_dict() if self.users else None

        if include_event:
            t['event'] = self.events.to_dict() if self.events else None

        return t