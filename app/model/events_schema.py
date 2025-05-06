from app import db
from app.model.base import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

class EventSchema(Base):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    # 只有UserSchema 內 is_active == True 和 is_admin == True
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False, default=9)
    description = db.Column(db.Text)
    # use unix timestamp
    event_start_date = db.Column(db.Integer, nullable=False)
    event_end_date = db.Column(db.Integer, nullable=False)
    apply_start_date = db.Column(db.Integer, nullable=False)
    apply_end_date = db.Column(db.Integer, nullable=True)
    location = db.Column(db.Integer, nullable=False, default=0)
    # offline:0, online:1
    # online => url required, offline => address required
    address = db.Column(db.String(255))
    url =  db.Column(db.String(255))
    # https://watson-john.medium.com/image-database-with-flask-d3015c935e2b
    img_id = db.Column(db.Integer, ForeignKey('image.id', ondelete='CASCADE'), nullable=True)
    max_attendees = db.Column(db.Integer, nullable=False, default=10)
    curr_attendees = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    # pending: 0, available: 1, full: 2, complete: 3, canceled: 4
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # Relationship
    admin = relationship("UserSchema", back_populates="events")
    category = relationship("CategorySchema", backref="events")
    bookings = relationship("BookingSchema", back_populates="event", cascade="all, delete-orphan")
    
    def to_dict(self, include_admin=False, include_booking=False):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
        t['category'] = self.category.name
        
        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()

        if include_admin:
            t['admin_name'] = self.admin.name if self.admin else None
            t['admin_email'] = self.admin.email if self.admin else None
        if include_booking:
            t['bookings'] = [
                {
                    'id': booking.id,
                    'user_id': booking.user_id,
                    'status': booking.status,
                    'user_name': booking.user.name if booking.user else None,
                    'user_email': booking.user.email if booking.user else None,
                    'user_phone': booking.user.phone if booking.user else None,
                }
                for booking in self.bookings
            ]
        return t

