from app import db

class Base(db.Model):
    __abstract__ = True

    def created(self):
        db.session.add(self)
        db.session.commit()
    def created_flush(self):
        db.session.add(self)
        db.session.flush()
    def deleted(self):
        db.session.delete(self)
        db.session.commit()

    # def updated(self):
    #     db.session.commit()