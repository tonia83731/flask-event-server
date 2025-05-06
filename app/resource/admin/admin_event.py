from flask import request
from datetime import date, datetime
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.model.events_schema import EventSchema
from app.model.bookings_schema import BookingSchema
from app.lib.auth_handling import admin_authentication
from app.lib.code_handling import EventStatus, EventLocation, BookingStatus
from app import db

from marshmallow import Schema, fields, post_load, validate, ValidationError,EXCLUDE

class EventValidate(Schema):
    title = fields.String(required=True, validate=validate.Length(min=4, max=100))
    category_id = fields.Integer(required=True)
    description = fields.String(validate=validate.Length(max=300))
    event_date = fields.Date(required=True)
    event_start_time = fields.Time(required=True)
    event_end_time = fields.Time(required=True)
    location = fields.Integer(required=True)
    address = fields.String()
    url = fields.String()
    price = fields.Integer(required=True)
    max_attendees = fields.Integer(validate=validate.Range(min=1, max=999))
    
    @post_load
    def validate_input(self, data, **kwargs):
        event_date = data.get("event_date")

        start_time = data.get("event_start_time")
        end_time = data.get("event_end_time")
        
        location = data.get("location")

        if event_date is None or start_time is None or end_time is None or location is None:
            return data, None

        if event_date < date.today():
            raise ValidationError("Event date cannot be former than today")
        
        if end_time <= start_time:
            raise ValidationError("Event end time cannot former than event start time")
        
        if location == EventLocation.EVENT_ONLINE:
            if not data.get('url'):
                raise ValidationError("URL is required")
            else:
                url_validator = validate.URL()
                try:
                    url_validator(data["url"])
                except:
                    raise ValidationError("Invalid URL")
        if location == EventLocation.EVENT_OFFLINE and not data.get('address'):
            raise ValidationError("Address is required")
        return data
    
class AdminEvents(Resource):
    @jwt_required()
    def get(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        category_id = request.args.get('category_id', type=int)
        query = db.session.query(EventSchema)
        
        if category_id is not None:
            query = query.filter(EventSchema.admin_id == admin_id, EventSchema.category_id == category_id)
        else:
            query = query.filter(EventSchema.admin_id == admin_id)
        
        events = query.all()
        events = [e.to_dict(include_admin=False) for e in events]
        
        
        return {
            "data": events
        }, 200

    @jwt_required()
    def post(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400

        input = EventValidate()
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        data = input.load(request.json)
        data["admin_id"] = admin_id
        event = EventSchema(**data)
        event.created()

        return {
            "data": event.to_dict()
        }, 201    
     
class AdminEvent(Resource):
    @jwt_required()
    def get(self, admin_id, event_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id, EventSchema.admin_id == admin_id).first()
        if not event:
            return {
                "message": "Event not found"
            }, 404
        
        event = event.to_dict(include_admin=False)
        
        return {
            "data": event
        }, 200
    
    @jwt_required()
    def put(self, admin_id, event_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()
        if not event:
            return {
                "message": "Event not found"
            }, 404
        if event.admin_id != admin_id:
            return {
                "message": "Permission denied"
            }, 400
        input = EventValidate(partial=True)
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        
        data = request.json
        for field, value in data.items():
            setattr(event, field, value)

        db.session.commit()

        data = event.to_dict(include_admin=False, include_category=True)
        data = {
            **data,
            "category": data["category"]["name"] if "category" in data else None,
        }
        return {
            "data": data
        }, 200
    @jwt_required()
    def delete(self, admin_id, event_id):
        """ 刪除活動 (CAUTION) """
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()
        if not event:
            return {
                "message": "Event not found"
            }, 404
        if event.admin_id != admin_id:
            return {
                "message": "Permission denied"
            }, 400
        event.deleted()

        return {
            "message": "Event and related bookings have been deleted."
        }, 200
    
class AdminEventCanceled(Resource):
    @jwt_required()
    def put(self, admin_id, event_id):
        """ 取消活動 """
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()
        if not event:
            return {
                "message": "Event not found"
            }, 404
        
        if event.status != EventStatus.EVENT_AVAILABLE:
            return {
                "message": "Canceled not available"
            }, 400
        event.status = EventStatus.EVENT_CANCELED

        # 需一起取消 Booking.status 跟 Qrcode
        bookings = db.session.query(BookingSchema).filter(BookingSchema.event_id == event_id).all()
        for booking in bookings:
            booking.status = BookingStatus.BOOKING_CANCELED
            if booking.qrcode:
                booking.qrcode_id = None
                db.session.delete(booking.qrcode)

        db.session.commit()
        """ 此處更新 """
        return {
            "data": event.to_dict()
        }, 200

class AdminEventBookings(Resource):
    @jwt_required()
    def get(self, admin_id, event_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()

        return {
            "data": event.to_dict(include_admin=True, include_booking=True)
        }, 200
    
# 根據時間自動更新EVENT.STATUS
def update_event_status():    
    curr = datetime.now()
    curr_timestamp = int(curr.timestamp())

    events = db.session.query(EventSchema).all()

    for event in events:
        if event.status == EventStatus.EVENT_CANCELED:
            continue
        if event.event_end_date < curr_timestamp:
            event.status = EventStatus.EVENT_COMPLETED

        elif event.apply_end_date and event.apply_end_date < curr_timestamp:
            event.status = EventStatus.EVENT_APPLY_END

        elif event.apply_start_date <= curr_timestamp <= (event.apply_end_date or curr_timestamp):
            event.status = EventStatus.EVENT_AVAILABLE

    db.session.commit()
