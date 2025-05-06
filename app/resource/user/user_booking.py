from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.model.events_schema import EventSchema
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema
from app.lib.auth_handling import user_authentication
from app.lib.code_handling import BookingStatus, EventStatus
from app import db
from qrcode import make
import io

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

        if event.status != EventStatus.EVENT_AVAILABLE:
            return {
                "message": "Booking is not available"
            }, 400
        
        existing_booking = db.session.query(BookingSchema).filter(BookingSchema.user_id == user_id, BookingSchema.event_id == event_id).first()

        if existing_booking:
            return {
                "message": "User already booked"
            }, 400
        
        # step1: create booking
        booking = BookingSchema(user_id=user_id, event_id=event_id)
        booking.created_flush()
        
        # step2: generate QR code & save
        """ 前端轉址url """
        ticket_url = f"http://127.0.0.1:5000/ticket?booking_id={booking.id}"
        qr_code = make(ticket_url)
        qr_bytes = io.BytesIO()
        qr_code.save(qr_bytes, format='PNG')
        qr_data = qr_bytes.getvalue()

        qrcode = QRcodeSchema(img=qr_data, name=f"booking_{user_id}.png", mimetype="image/png", is_valid=True)
        qrcode.created()

        booking.qrcode_id = qrcode.id

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
        bookings = [b.to_dict(include_event=True) for b in bookings]

        return {
            "success": True,
            "data": bookings
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
        
        booking = booking.to_dict(include_event=True)
        
        return {
            "data": booking
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
            if qrcode:
                qrcode.deleted()
                booking.qrcode_id = None

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