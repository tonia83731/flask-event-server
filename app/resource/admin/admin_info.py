from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.model.users_schema import UserSchema
from app.lib.auth_handling import admin_authentication
# from app.resource.admin.admin_auth import AdminRegisterValidate
from app.resource.user.user_info import ClientInfoValidate
from app import db

class Admin(Resource):
    @jwt_required()
    def get(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission denied"
            }, 400
        
        user = user = db.session.query(UserSchema).filter(UserSchema.id == admin_id).first()
        if not user:
            return {
                "message": "Admin not found"
            }, 404
        return {
            "data": user.to_dict()
        }, 200
    
    @jwt_required()
    def put(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "permission denied"
            }, 400
        
        user = db.session.query(UserSchema).filter(UserSchema.id == admin_id).first()
        if not user:
            return {
                "message": "Admin not found"
            }, 404
        if user.email == 'admin@example.com':
            return {
                "message": "The current admin does not have permission to perform updates."
            }, 400
        input = ClientInfoValidate(partial=True)
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        data = input.load(request.json)

        if 'email' in data:
            is_existed = db.session.query(UserSchema).filter(UserSchema.email == data['email'], UserSchema.id != admin_id).first()
            if is_existed:
                return {
                    "message": "Email already existed"
                }, 400
        for field, value in data.items():
            setattr(user, field, value)

        db.session.commit()
        return {
            "data": user.to_dict()
        }, 200