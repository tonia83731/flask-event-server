from flask_restful import Resource
from app.model.category_schema import CategorySchema
from app import db

class Category(Resource):
    def get(self):
        """ 客戶端: 取得所有分類 """
        categories = db.session.query(CategorySchema).all()
        return {
            "data": [c.to_dict() for c in categories]
        }, 200