from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema
from app.lib.auth_handling import admin_authentication
from app.lib.code_handling import BookingStatus
from app import db
from qrcode import make
import io

class AdminBookingUpdated(Resource):
    @jwt_required()
    def put(self, admin_id, booking_id):
        if not admin_authentication(admin_id):
            return {
                "message": 'Permission denied'
            }, 400
        
        booking = db.session.query(BookingSchema).filter(BookingSchema.id == booking_id).first()

        if not booking:
            return {
                "message": "Booking not found"
            }, 404
        
        if booking.status != BookingStatus.BOOKING_PENDING:
            return {
                "message": "Unabled to update booking status"
            }, 404
        
        """ 前端轉址url """
        ticket_url = f"http://127.0.0.1:5000/ticket?user_id={booking.user_id}&booking_id={booking.id}"
        qr_code = make(ticket_url)
        qr_bytes = io.BytesIO()
        qr_code.save(qr_bytes, format='PNG')
        qr_data = qr_bytes.getvalue()

        qrcode = QRcodeSchema(img=qr_data, name=f"booking_{booking.id}.png", mimetype="image/png", is_valid=True)
        qrcode.created()

        booking.status = BookingStatus.BOOKING_CONFIRMED
        booking.qrcode_id = qrcode.id
        db.session.commit()

        return {
            "data": booking.to_dict(include_user=True, include_event=False)
        }, 200
