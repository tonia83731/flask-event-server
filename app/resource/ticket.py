from flask import request
from flask_restful import Resource
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema
from app.lib.code_handling import EventStatus, BookingStatus
from app import db
from datetime import datetime

def is_event_expired(event_date, event_end_time):
    event_datetime = datetime.combine(event_date, event_end_time)
    curr_datetime = datetime.now()

    return event_datetime < curr_datetime

class Ticket(Resource):
    def get(self):
        user_id = request.args.get('user_id', type=int)
        booking_id = request.args.get('booking_id', type=int)

        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id, BookingSchema.user_id == user_id).first()
        
        if not booking:
            return {
                "is_valid": False,
                "message": "The booking is not existed."
            }, 200
        
        if booking.status == BookingStatus.BOOKING_CANCELED:
            return {
                "is_valid": False,
                "message": "The booking has been canceled."
            }, 200
        
        event = booking.event
        if event.status in [EventStatus.EVENT_COMPLETED, EventStatus.EVENT_CANCELED] or is_event_expired(event.event_date, event.event_end_time):
            return {
                "is_valid": False,
                "message": "The event has been canceled or has already ended."
            }, 200
       
        qrcode = db.session.query(QRcodeSchema).filter(QRcodeSchema.id == event.qrcode_id).first()

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
            "redirect_url": f"?user_id={user_id}&booking_id={booking_id}"
        }, 200
    


    # class TicketConfirmed(Resource):
#     @jwt_required()
#     def post(self, user_id, booking_id):        
#         booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id, BookingSchema.user_id == user_id).first()
        
#         if not booking:
#             return {
#                 "message": "Booking not found"
#             }, 404
        
#         identity = get_jwt()
#         identity_id = int(identity)
#         event = booking.event
#         if event.admin_id != identity_id:
#             return {
#                 "message": "Permission denied"
#             }, 403
        

#         qrcode = db.session.query(QRcodeSchema).filter(QRcodeSchema.id == booking.qrcode_id).first()
#         if not qrcode:
#             return {
#                 "message": "QR code not found"
#             }, 404
        
#         booking.status = BookingStatus.BOOKING_COMPLETED
#         qrcode.is_valid = False
#         qrcode.is_applied = True

#         db.session.commit()

#         return {
#             "message": "Booking status and QR code is updated"
#         }, 200