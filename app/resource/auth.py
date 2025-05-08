from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from app import db
from app.model.users_schema import UserSchema
from app.lib.email_handling import send_reset_password_email
from app.lib.token_handling import confirm_activation_token
from app.lib.password_handling import encoded_password

class EmailValidation(Schema):
    email = fields.Email(required=True)

class RegisterActivate(Resource):
    def get(self, token):
        try:
            user_id, email = confirm_activation_token(token, salt='email-activate')
        except:
            return {
                "success": False,
                "message": "Invalid activation link"
            }, 200

        user = db.session.query(UserSchema).filter(UserSchema.id == user_id, UserSchema.email == email).first()
        
        if not user:
            return {
                'success': False,
                'message': "User not found"
            }, 200
        
        if user.is_active:
            return {
                "success": False,
                'message': "Account already activate"
            }, 200
        
        user.is_active = True
        db.session.commit()

        return {
            "success": True,
            "message": "Account successfully activated"
        }, 200
    
class ForgotPassword(Resource):
    def post(self):
        email_validation = EmailValidation()
        form_input = request.get_json()

        try:
            form = email_validation.load(form_input)
        except ValidationError as err:
            return {
                "message": err.messages
            }, 400

        
        user = db.session.query(UserSchema).filter(UserSchema.email == form['email']).first()
        if not user:
            return {
                "success": False,
                "message": "User not found."
            }, 404
        
        send_reset_password_email(user.id, user.email, user.name)

        return {"message": "Password reset email sent"}, 200
    
class ResetPassword(Resource):
    def post(self, token):
        try:
            user_id, email = confirm_activation_token(token, salt='reset-password')
        except:
            return {
                "success": False,
                "message": "Invalid or expired token"
            }, 200
        
        user = db.session.query(UserSchema).filter(UserSchema.id == user_id, UserSchema.email == email).first()

        if not user:
            return {
                'success': False,
                'message': "User not found"
            }, 400
        
        new_pwd = request.json.get('password')
        if not new_pwd:
            return {
                "success": False,
                "message": "Password is required"
            }, 400
        
        hashed_pwd = encoded_password(new_pwd)
        user.password = hashed_pwd
        db.session.commit()

        return {"message": "Password has been reset successfully"}, 200
