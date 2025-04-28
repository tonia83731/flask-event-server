from flask import Response
from flask_restful import Resource
from app.model.img_schema import ImgSchema
from app import db



class Image(Resource):
    def get(self, img_id):
        """ 客戶端: 取得活動圖片by ID """
        img = db.session.query(ImgSchema).filter(ImgSchema.id == img_id).first()
        if not img:
            return {
                "message": "Image not found"
            }, 404
        
        return Response(img.img, mimetype=img.mimetype)

