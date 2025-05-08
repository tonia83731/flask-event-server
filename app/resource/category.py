from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app import db
from app.model.category_schema import CategorySchema
from app.lib.auth_handling import JWTAuth

class Categories(Resource):
    def get(self):
        """ 客戶端: 取得所有分類 """
        categories = db.session.query(CategorySchema).all()
        return {
            "data": [c.to_dict() for c in categories]
        }, 200
    

class AdminCategories(Resource): 
    @jwt_required()
    def get(self, admin_id):
        if not JWTAuth.is_admin(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        
        categories = db.session.query(CategorySchema).all()
        return {
            "data": [c.to_dict() for c in categories]
        }, 200