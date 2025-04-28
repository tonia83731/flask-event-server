from app import db
from app.model.base import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

class EventSchema(Base):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False, default=11)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    event_start_time = db.Column(db.Time, nullable=False)
    event_end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.Integer, nullable=False, default=0)
    # online => url required, offline => address required
    # online: 1, offline: 0
    address = db.Column(db.String(255))
    url =  db.Column(db.String(255))
    # https://watson-john.medium.com/image-database-with-flask-d3015c935e2b
    # img_url = db.Column(db.String(255))
    img_id = db.Column(db.Integer, ForeignKey('image.id'), nullable=True)
    price = db.Column(db.Integer, nullable=False, default=0)
    max_attendees = db.Column(db.Integer, nullable=False, default=10)
    current_attendees = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    # 0: OPEN, 1: END, 2: CANCELED
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    categories= relationship("CategorySchema", back_populates="events")
    admins = relationship("UserSchema", back_populates="events")
    bookings = relationship("BookingSchema", back_populates="events")

    def to_dict(self, include_admin = False, include_category = False):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
        t["event_date"] = t["event_date"].isoformat()
        t["event_start_time"] = t["event_start_time"].strftime("%H:%M:%S")
        t["event_end_time"] = t["event_end_time"].strftime("%H:%M:%S")
        
        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()

        if include_admin:
            t['admin'] = self.admins.to_dict() if self.admins else None
        if include_category:
            t['category'] = self.categories.to_dict() if self.categories else None

        return t

