from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema
from app.lib.code_handling import BookingStatus
from app.lib.code_handling import EventStatus
from app import db
from datetime import datetime

def is_event_expired(event_date, event_end_time):
    event_datetime = datetime.combine(event_date, event_end_time)
    curr_datetime = datetime.now()

    return event_datetime < curr_datetime

class Ticket(Resource):
    def get(self, user_id, booking_id):
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id, BookingSchema.user_id == user_id).first()

        if not booking:
            return {
                "is_valid": False,
                "message": "Booking not found"
            }, 200
        
        if booking.status == BookingStatus.BOOKING_CANCELED:
            return {
                "is_valid": False,
                "message": "Booking has been canceled"
            }, 200
        
        event = booking.events
        if event.status in [EventStatus.EVENT_COMPLETED, EventStatus.EVENT_CANCELED] or is_event_expired(event.event_date, event.event_end_time):
            return {
                "is_valid": False,
                "message": "The event has been canceled or has already ended."
            }, 200
        
        qrcode = db.session.query(QRcodeSchema).filter(QRcodeSchema.id == booking.qrcode_id).first()
        if not qrcode:
            return {
                "is_valid": False,
                "message": "The QR code is not existed."
            }, 200
        if not qrcode.is_valid:
            return {
                "is_valid": False,
                "message": "The QR code not valid."
            }, 200
        if qrcode.is_applied:
            return {
                "is_valid": False,
                "message": "The QR has been applied."
            }, 200
        
        return {
            "is_valid": True,
            "message": "Valid User",
            "redirect_url": f"?user_id={user_id}&booking_id={booking_id}&qrcode_id={booking.qrcode_id}"
        }, 200

class TicketConfirmed(Resource):
    @jwt_required()
    def post(self, user_id, booking_id, qrcode_id):
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id, BookingSchema.user_id == user_id).first()
        qrcode = db.session.query(QRcodeSchema).filter(QRcodeSchema.id == qrcode_id).first()

        identity = get_jwt_identity()
        identity_id = int(identity)

        if booking.events.admin_id != identity_id:
            return {
                "message": "Permission denined"
            }, 403

        booking.status = BookingStatus.BOOKING_COMPLETED
        qrcode.is_applied = True

        db.session.commit()
        return {
            "message": "Booking status and QR code is updated"
        }, 200