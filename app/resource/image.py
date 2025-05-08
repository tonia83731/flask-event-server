from flask import request
from flask import Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app import db
from app.model.img_schema import ImgSchema
from app.lib.auth_handling import JWTAuth

# https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
# https://www.youtube.com/watch?v=zMhmZ_ePGiM&t=57s

class UploadImages(Resource):
    @jwt_required()
    def post(self, admin_id):

        if not JWTAuth().is_admin(admin_id) and not JWTAuth().is_super():
            return {
                "message": "Permission denied"
            }, 403
        
        # 前端input name="pic"
        pic = request.files['pic']

        if not pic:
            return {
                "message": "No image uploaded"
            }, 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        img = ImgSchema(img=pic.read(), name=filename, mimetype=mimetype)
        img.created()

        return {
            "data": img.id
        }, 200


class Image(Resource):
    def get(self, img_id):
        """ 客戶端: 取得活動圖片by ID """
        img = db.session.query(ImgSchema).filter(ImgSchema.id == img_id).first()
        if not img:
            return {
                "message": "Image not found"
            }, 404
        
        return Response(img.img, mimetype=img.mimetype)

