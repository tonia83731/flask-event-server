import bcrypt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_mail import Message
from app import db
from app.extensions import mail
from app.lib.validation.auth import LoginValidate
from app.lib.password_handling import encoded_password
from app.lib.gmail_handling import generate_activation_token, confirm_activation_token
from app.model.users_schema import UserSchema
from marshmallow import Schema, fields, validate
class RegisterValidate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    email = fields.Email(required=True) 
    password = fields.String(required=True, validate=validate.Length(min=6))
    phone = fields.String(required=True)

class UserRegister(Resource):
    def post(self):
        input = RegisterValidate()
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        data = input.load(request.json)

        is_existed = db.session.query(UserSchema).filter(UserSchema.email == data['email']).first()
        if is_existed:
            return {
                'message': 'User already existed'
            }, 400
        
        hash = encoded_password(data['password'])
        data['password'] = hash
        user = UserSchema(**data)
        user.created()

        # SEND ACTIVATION EMAIL
        token = generate_activation_token(user.id, user.email, salt='email-activate')
        activation_link = f"http://127.0.0.1:5000/activate/{token}"

        msg = Message(
            subject="Activate Your Account",
            recipients=[user.email],
            html=f"""
                <html>
                    <body>
                        <p>Hi {user.name},</p>
                        <p>Please click the link below to activate your account:</p>
                        <p><a href="{activation_link}">Activate Account</a></p>
                        <p>If you did not sign up, please ignore this email.</p>
                    </body>
                </html>
            """
        )

        mail.send(msg)

        res = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        }

        return {
            'success': True,
            'data': res
        }, 201


class UserRegisterActivate(Resource):
    def get(self, token):

        try:
            user_id, email = confirm_activation_token(token, salt='email-activate')
        except:
            return {
                "success": False,
                "message": "Invalid activation link"
            }, 200

        user = db.session.query(UserSchema).filter(UserSchema.id == user_id, UserSchema.email == email).first()
        
        print(user_id, email, user)
        
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


class UserLogin(Resource):
    def post(self):
        input = LoginValidate()
        errors = input.validate(request.json)
        if errors:
            return {
                "message": errors
            }, 400
        data = input.load(request.json)

        user = db.session.query(UserSchema).filter(UserSchema.email == data['email'], UserSchema.is_admin == False).first()
        if not user:
            return {
                'message': 'Email or password incorrect.'
            }, 400
        
        if not user.is_active:
            return {
                'message': 'Please activate your account before logging in.'
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


# -----------------------------------------------------
class ForgotPassword(Resource):
    def post(self):
        email = request.json.get('email')
        if not email:
            return {
                "success": False,
                "message": "Email is required."
            }, 400
        
        user = db.session.query(UserSchema).filter(UserSchema.email == email).first()
        if not user:
            return {
                "success": False,
                "message": "User not found."
            }, 404
        
        reset_token = generate_activation_token(user.id, email, salt='reset-password')
        reset_url = f"http://127.0.0.1:5000/reset-password/{reset_token}"
        
        msg = Message(
            subject="Password Reset Request",
            recipients=[email],
            html=f"""
                <html>
                    <body>
                        <p>Hi {user.name},</p>
                        <p>"Click the following link to reset your password:</p>
                        <p><a href="{reset_url}">Reset Email</a></p>
                    </body>
                </html>
            """
        )
        mail.send(msg)

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