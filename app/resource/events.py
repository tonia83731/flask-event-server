from flask import request
from flask_restful import Resource
from app.model.events_schema import EventSchema
from app import db


class Events(Resource):
    def get(self):
        category_id = request.args.get('category_id', type=int)

        query = db.session.query(EventSchema)

        if category_id is not None:
            query = query.filter(EventSchema.category_id == category_id)

        events = query.all()
        events = [e.to_dict(include_admin=True) for e in events]
        

        return {
            "success": True,
            "data": events
        }, 200
    
class Event(Resource):
    def get(self, event_id):
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()
        event = event.to_dict(include_admin=True)
        
        return {
            "success": True,
            "data": event
        }, 200
  

    
