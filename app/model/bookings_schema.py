from app import db
from app.model.base import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

class BookingSchema(Base):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)

    # pending: 0, confirmed: 1, completed: 2, canceled: 3
    status = db.Column(db.Integer, default=0, nullable=False)
    qrcode_id = db.Column(db.Integer, ForeignKey('qrcode.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    user = relationship("UserSchema", back_populates="bookings")
    event = relationship("EventSchema", back_populates="bookings")
    qrcode = relationship("QRcodeSchema", back_populates="bookings")

    def to_dict(self, include_event=False):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        t["user_name"] = self.user.name
        t["user_email"] = self.user.email
        t["user_phone"] = self.user.phone

        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()

        if include_event:
            event_dict = self.event.to_dict(include_admin=True) if self.event else {}
            t['event_title'] = event_dict.get('title')
            t['event_start_date'] = event_dict.get('event_start_date')
            t['event_end_date'] = event_dict.get('event_end_date')
            t['event_location'] = event_dict.get('location')
            if event_dict.get('location') == 0:
                t['event_address'] = event_dict.get('address')
            elif event_dict.get('location') == 1:
                t['event_url'] = event_dict.get('url')
            t['category'] = event_dict.get('category')
            t['admin_name'] = event_dict.get('admin_name')
            t['admin_email'] = event_dict.get('admin_email')

        return t