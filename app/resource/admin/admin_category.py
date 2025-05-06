from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.lib.auth_handling import admin_authentication
from app.model.category_schema import CategorySchema
from app import db
class AdminCategories(Resource): 
    @jwt_required()
    def get(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        
        categories = db.session.query(CategorySchema).all()
        return {
            "data": [c.to_dict() for c in categories]
        }, 200