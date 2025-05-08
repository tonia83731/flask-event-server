from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema
from app.lib.code_handling import BookingStatus, EventStatus
from app.lib.auth_handling import JWTAuth

class Ticket(Resource):
    @jwt_required()
    def get(self, booking_id):
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id).first()

        if not booking:
            return {
                "is_valid": False,
                "message": "Booking not found"
            }, 200
        
        
        auth = JWTAuth()
        user_id = auth.identity
        # admin/user both can access
        if booking.user_id != user_id or (not booking.event and booking.event.admin_id != user_id):
            return {
                "is_valid": False,
                "message": "Permission denied"
            }
        
        if booking.status != BookingStatus.BOOKING_CONFIRMED:
            return {
                "is_valid": False,
                "message": "Booking not available"
            }, 200

        if booking.event.status in [EventStatus.EVENT_COMPLETED, EventStatus.EVENT_CANCELED]:
            return {
                "is_valid": False,
                "message": "The event has been canceled or has already ended."
            }, 200
        
        qrcode = booking.qrcode

        if not qrcode:
            return {
                "is_valid": False,
                "message": "The QR code is not existed."
            }, 200
        if qrcode.is_applied:
            return {
                "is_valid": False,
                "message": "The QR has been applied."
            }, 200
        
        return {
            "is_valid": True,
            "message": "Valid User",
            # "redirect_url": f"?booking_id={booking_id}"
        }, 200

class TicketConfirmed(Resource):
    @jwt_required()
    def post(self, booking_id):
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id).first()

        identity = get_jwt_identity()
        identity_id = int(identity)

        if not booking:
            return {
                "message": "Booking not found"
            }, 404

        if booking.event.admin_id != identity_id:
            return {
                "message": "Permission denined"
            }, 403

        booking.status = BookingStatus.USER_ATTENDED
        
        if booking.qrcode:
            booking.qrcode.is_applied = True

        db.session.commit()
        return {
            "message": "Booking status and QR code is updated"
        }, 200