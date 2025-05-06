from app import db
from app.model.base import Base
from sqlalchemy import func
from sqlalchemy.orm import relationship

class CategorySchema(Base):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # events = relationship('EventSchema', back_populates='category', cascade="all, delete-orphan")

    def to_dict(self):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()
        return t