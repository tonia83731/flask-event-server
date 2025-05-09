from flask import request
from datetime import date, datetime
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app import db
from app.model.events_schema import EventSchema
from app.model.bookings_schema import BookingSchema
from app.lib.auth_handling import JWTAuth
from app.lib.code_handling import EventStatus, EventLocation, BookingStatus
from app.lib.event_form_handling import EventValidationForm
    
class AdminEvents(Resource):
    @jwt_required()
    def get(self, admin_id):
        if not JWTAuth().is_admin(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        # conditions when URL= ... ?category_id=
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
        if not JWTAuth().is_admin(admin_id):
            return {
                "message": "Permission denied"
            }, 400

        event_validation = EventValidationForm()
        form_input = request.get_json()

        try:
            form = event_validation.load(form_input)
        except ValidationError as err:
            print(err)
            return {
                "message": err.messages
            }, 400
        
        form["admin_id"] = admin_id
        event = EventSchema(**form)
        event.created()

        return {
            "data": event.to_dict()
        }, 201    
     
class AdminEvent(Resource):
    @jwt_required()
    def get(self, admin_id, event_id):
        if not JWTAuth().is_admin(admin_id):
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
        if not JWTAuth().is_admin(admin_id):
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
        
        event_validation = EventValidationForm()
        form_input = request.get_json()

        try:
            form = event_validation.load(form_input)
        except ValidationError as err:
            print(err)
            return {
                "message": err.messages
            }, 400
        
        for field, value in form.items():
            setattr(event, field, value)

        db.session.commit()

        data = event.to_dict()
        return {
            "data": data
        }, 200
    
    @jwt_required()
    def delete(self, admin_id, event_id):
        """ 刪除活動 (CAUTION) """
        if not JWTAuth().is_admin(admin_id):
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
        if not JWTAuth().is_admin(admin_id):
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
        if not JWTAuth().is_admin(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()

        return {
            "data": event.to_dict(include_admin=True, include_booking=True)
        }, 200
