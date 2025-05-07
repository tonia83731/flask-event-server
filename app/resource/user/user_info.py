from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.model.users_schema import UserSchema
from app.lib.auth_handling import user_authentication
from app.lib.password_handling import encoded_password
from app import db
from marshmallow import Schema, fields, validate

class ClientInfoValidate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    email = fields.Email(required=True) 
    phone = fields.String(required=True)
    address = fields.String(required=False, allow_none=True)

class User(Resource):
    @jwt_required()
    def get(self, user_id):
        if not user_authentication(user_id):
            return {
                "message": "Permission denied"
            }, 400
        
        user = db.session.query(UserSchema).filter(UserSchema.id == user_id).first()
        if not user:
            return {
                'message': 'User not found'
            }, 404
        
        return {
            'success': True,
            'data': user.to_dict()
        }, 200
    
    @jwt_required()
    def put(self, user_id):
        if not user_authentication(user_id):
            return {
                'success': False,
                "message": "permission denied"
            }, 400
        
        user = db.session.query(UserSchema).filter(UserSchema.id == user_id).first()
        if not user:
            return {
                'success': False,
                "message": "User not found"
            }, 404
        input_data = ClientInfoValidate(partial=True)
        errors = input_data.validate(request.json)
        if errors:
            return {
                'success': False,
                "message": errors
            }, 400
        
        data = input_data.load(request.json)
        if 'email' in data:
            is_existed = db.session.query(UserSchema).filter(UserSchema.email == data['email'], UserSchema.id != user_id).first()
            if is_existed:
                return {
                    'success': False,
                    "message": "Email already existed"
                }, 400
            
        for field, value in data.items():
            setattr(user, field, value)

        db.session.commit()

        return {
            'success': True,
            "data": user.to_dict()
        }, 200
    
        
        

        
