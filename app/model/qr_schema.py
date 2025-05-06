from app import db
from app.model.base import Base
from sqlalchemy.orm import relationship

class QRcodeSchema(Base):
    __tablename__ = 'qrcode'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False) 
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    is_applied = db.Column(db.Boolean, nullable=False, default=False)

    bookings = relationship("BookingSchema", back_populates="qrcode", cascade="all, delete-orphan")