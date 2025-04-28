from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app.model.img_schema import ImgSchema

from app.lib.auth_handling import admin_authentication

# https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
# https://www.youtube.com/watch?v=zMhmZ_ePGiM&t=57s

class Images(Resource):
    @jwt_required()
    def post(self, admin_id):
        if not admin_authentication(admin_id):
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
    
# def post(self):
    #     # 前端input name="pic"
    #     pic = request.files['pic']

    #     if not pic:
    #         return {
    #             "message": "No image uploaded"
    #         }, 400

    #     filename = secure_filename(pic.filename)
    #     mimetype = pic.mimetype

    #     img = ImgSchema(img=pic.read(), name=filename, mimetype=mimetype)
    #     img.created()

    #     return {
    #         "data": img.id
    #     }, 200