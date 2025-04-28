from app import db
from app.model.base import Base
from sqlalchemy.dialects.mysql import LONGBLOB

class ImgSchema(Base):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(LONGBLOB, nullable=False) 
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)