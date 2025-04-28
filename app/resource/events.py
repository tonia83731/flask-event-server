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
        events = [e.to_dict(include_admin=True, include_category=True) for e in events]

        data = [
            {
                **e,
                "admin_name": e["admin"]["name"] if "admin" in e else None,
                "admin_email": e["admin"]["email"] if "admin" in e else None,
                "admin_phone": e["admin"]["phone"] if "admin" in e else None,
                "admin_address": e["admin"]["address"] if "admin" in e else None,
                "category": e["category"]["name"] if "category" in e else None,
            }
            for e in events
        ]

        for entry in data:
            entry.pop("admin", None)
        
        return {
            "data": data
        }, 200
    
class Event(Resource):
    def get(self, event_id):
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()
        event = event.to_dict(include_admin=True, include_category=True)
        data = {
            **event,
            "admin_name": event["admin"]["name"] if "admin" in event else None,
            "admin_email": event["admin"]["email"] if "admin" in event else None,
            "admin_phone": event["admin"]["phone"] if "admin" in event else None,
            "admin_address": event["admin"]["address"] if "admin" in event else None,
            "category": event["category"]["name"] if "category" in event else None,
        }
        data.pop("admin", None)
        
        return {
            "data": data
        }, 200
  

    
