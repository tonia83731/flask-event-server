from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app.lib.validation.auth import LoginValidate
from app.lib.password_handling import encoded_password
from app.model.users_schema import UserSchema
from app import db
import bcrypt

from marshmallow import Schema, fields, validate
class AdminRegisterValidate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    email = fields.Email(required=True) 
    password = fields.String(required=True, validate=validate.Length(min=6))
    phone = fields.String(required=True)
    address = fields.String(required=True)

class AdminRegister(Resource):
    def post(self):
        input = AdminRegisterValidate()
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        data = input.load(request.json)

        is_existed = db.session.query(UserSchema).filter(UserSchema.email == data['email']).first()
        if is_existed:
            return {
                'message': 'Admin already existed'
            }, 400
        
        hash = encoded_password(data['password'])
        data['password'] = hash
        data['is_admin'] = True
        user = UserSchema(**data)
        user.created()

        res = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

        return {
            'success': True,
            'data': res
        }, 201
class AdminLogin(Resource):
   def post(self):
        input = LoginValidate()
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        data = input.load(request.json)

        user = db.session.query(UserSchema).filter(UserSchema.email == data['email'], UserSchema.is_admin == True).first()
        if not user:
            return {
                'message': 'Email or password incorrect.'
            }, 400
        
        is_password_match = bcrypt.checkpw(data['password'].encode(), user.password.encode())

        if not is_password_match:
            return {
                'message': 'Email or password incorrect.'
            }, 400

        user_data = {
            'id': user.id,
            'role': 'admin' if user.is_admin else 'user',
        }
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user_data["role"]})
        user_data['token'] = access_token
        return {
            'success': True,
            'data': user_data
        }, 200