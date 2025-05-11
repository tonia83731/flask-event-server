from flask import Response
from flask_restful import Resource
from app.model.qr_schema import QRcodeSchema
from app import db

class QRcode(Resource):
    def get(self, qrcode_id):
        qrcode = db.session.query(QRcodeSchema).filter(QRcodeSchema.id == qrcode_id).first()
        if not qrcode:
            return {
                "message": "QR code not found"
            }, 404
        return Response(qrcode.img, mimetype=qrcode.mimetype)