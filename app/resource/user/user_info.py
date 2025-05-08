import bcrypt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app import db
from app.model.users_schema import UserSchema
from app.lib.auth_handling import JWTAuth
from app.lib.user_form_handling import UpdatedUserInfoForm
from app.lib.password_handling import encoded_password

class UserInfo(Resource):
    @jwt_required()
    def get(self, user_id):
        if not JWTAuth().is_user(user_id):
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
        if not JWTAuth.is_user(user_id):
            return {
                "message": "Permission denied"
            }, 400
        
        user = db.session.query(UserSchema).filter(UserSchema.id == user_id).first()
        if not user:
            return {
                'success': False,
                "message": "User not found"
            }, 404
        
        user_validation = UpdatedUserInfoForm()
        form_input = request.get_json()

        try:
            form = user_validation.load(form_input)
        except ValidationError as err:
            return {
                "message": err.messages
            }, 400
        
        # checked email
        if 'email' in form:
            is_existed = db.session.query(UserSchema).filter(UserSchema.email == form['email'], UserSchema.id != user_id).first()
            if is_existed:
                return {
                    "message": "Email already existed"
                }, 400
            
        # checked password
        if 'password' in form:
            if 'original_password' not in form:
                return {
                    "message": "Original password is required"
                }, 400
            
            # original_password checked
            is_password_match = bcrypt.checkpw(form['password'].encode(), user.password.encode())
            if not is_password_match:
                return {
                    'message': 'Original password incorrect'
                }, 400
            if form['original_password'] == form['password']:
                return {
                    "message": "The new password must be different from the original password"
                }
            
            user.password = encoded_password(form['password'])
            
        for field, value in form.items():
            if field not in ['original_password', 'password']:
                setattr(user, field, value)

        db.session.commit()

        return {
            'success': True,
            "data": user.to_dict()
        }, 200
    
        
