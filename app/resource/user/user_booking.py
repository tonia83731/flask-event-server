from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.model.events_schema import EventSchema
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema
from app.lib.auth_handling import user_authentication
from app.lib.code_handling import BookingStatus, EventStatus
from app import db


from marshmallow import Schema, fields, validate

class BookingValidate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    email = fields.Email(required=True) 
    phone = fields.String()


class EventBooking(Resource):    
    @jwt_required()
    def post(self, user_id, event_id):
        if not user_authentication(user_id):
            return {
                "message": 'Permission denied'
            }, 400
        
        event = db.session.query(EventSchema).filter(EventSchema.id == event_id).first()
        if not event:
            return {
                "message": "Event not found"
            }, 404

        if event.status == EventStatus.EVENT_FULL:
            return {
                "message": "Event is fully booked"
            }, 400
        
        booking = db.session.query(BookingSchema).filter(BookingSchema.user_id == user_id, BookingSchema.event_id == event_id).first()

        if booking:
            return {
                "message": "User already booked"
            }, 400
        
        input = BookingValidate()
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400

        data = input.load(request.json)

        data['user_id'] = user_id
        data['event_id'] = event_id

        booking = BookingSchema(**data)
        booking.created()

        event.current_attendees += 1
        if event.current_attendees == event.max_attendees:
            event.status = EventStatus.EVENT_FULL
        db.session.commit()

        """ 需要email通知相關admin 使用者報名 """

        return {
            "data": booking.to_dict()
        }, 201
    
class ClientBookings(Resource):
    @jwt_required()
    def get(self, user_id):
        if not user_authentication(user_id):
            return {
                "message": 'Permission denied'
            }, 400
        bookings = db.session.query(BookingSchema).filter(BookingSchema.user_id == user_id).all()
        bookings = [b.to_dict(include_user=False, include_event=True) for b in bookings]
        data = [
            {
                **b,
                "event_title": b['event']['title'] if 'event' in b else None,
                "event_date": b['event']['event_date'] if 'event' in b else None,
                "event_start_time": b['event']['event_start_time'] if 'event' in b else None,
                "event_end_time": b['event']['event_end_time'] if 'event' in b else None,
                "event_location": b['event']['location'] if 'event' in b else None,
                "event_address": b['event']['address'] if 'event' in b else None,
                "event_url": b['event']['url'] if 'event' in b else None,
            }
            for b in bookings
        ]

        for entry in data:
            entry.pop('event', None)

        return {
            "data": data
        }, 200


class ClientBooking(Resource):
    @jwt_required()
    def get(self, user_id, booking_id):
        if not user_authentication(user_id):
            return {
                "message": 'Permission denied'
            }, 400
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id).first()
        if not booking:
            return {
                "message": "Booking not found"
            }, 404
        
        booking = booking.to_dict(include_user=False, include_event=True)
        data = {
                **booking,
                "event_title": booking['event']['title'] if 'event' in booking else None,
                "event_date": booking['event']['event_date'] if 'event' in booking else None,
                "event_start_time": booking['event']['event_start_time'] if 'event' in booking else None,
                "event_end_time": booking['event']['event_end_time'] if 'event' in booking else None,
                "event_location": booking['event']['location'] if 'event' in booking else None,
                "event_address": booking['event']['address'] if 'event' in booking else None,
                "event_url": booking['event']['url'] if 'event' in booking else None,
            }
        
        data.pop('event', None)
        
        return {
            "data": data
        }, 200
    
class ClientBookingUpdated(Resource):
    @jwt_required()
    def put(self, user_id, booking_id):
        if not user_authentication(user_id):
            return {
                "message": 'Permission denied'
            }, 400
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id, BookingSchema.user_id == user_id).first()
        if not booking:
            return {
                "message": "Booking not found"
            }, 404
        
        input = BookingValidate(partial=True)
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        
        data = input.load(request.json)
        for field, value in data.items():
            setattr(booking, field, value)

        db.session.commit()

        return {
            "data": booking.to_dict()
        }, 200
    

class ClientBookingCanceled(Resource):
    @jwt_required()
    def put(self, user_id, booking_id):
        """ 取消報名活動 """
        if not user_authentication(user_id):
            return {
                "message": 'Permission denied'
            }, 400
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id, BookingSchema.user_id == user_id).first()
        if not booking:
            return {
                "message": "Booking not found"
            }, 404
        
        booking.status = BookingStatus.BOOKING_CANCELED

        """ 更新QRcode 狀態 """
        if booking.qrcode_id:
            qrcode = db.session.query(QRcodeSchema).filter(QRcodeSchema.id == booking.qrcode_id).first()
            if qrcode.is_valid and not qrcode.is_applied:
                qrcode.is_valid = False

        event = db.session.query(EventSchema).filter(EventSchema.id == booking.event_id).first()
        if not event:
            return {
                "message": "Event not found"
            }, 404
        if event.current_attendees > 0:
            event.current_attendees -= 1
        db.session.commit()

        return {
            "data": booking.to_dict()
        }, 200