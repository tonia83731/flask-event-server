from app import db
from app.model.base import Base

class QRcodeSchema(Base):
    __tablename__ = 'qrcode'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False) 
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    is_valid = db.Column(db.Boolean, nullable=False, default=False)
    # event.status == 2 (canceled) / booking.status == 2, 3
    is_applied = db.Column(db.Boolean, nullable=False, default=False)