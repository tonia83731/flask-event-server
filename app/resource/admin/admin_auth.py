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
                'message': 'Email already existed'
            }, 400
        
        hash = encoded_password(data['password'])
        data['password'] = hash
        data['is_admin'] = True
        user = UserSchema(**data)
        user.created()

        admin_token = generate_activation_token(user.id, user.email, salt='admin-email-activate')
        activation_link = f"http://127.0.0.1:5000/admin/activate/{admin_token}"

        msg = Message(
            subject='Activate Admin Account',
            recipients=[user.email],
            html=f"""
                <html>
                    <body>
                        <p>{user.name} 您好，</p>
                        <p>請確認以下您的資訊：</p>
                        <ul>
                            <li>電話：{user.phone}</li>
                            <li>地址：{user.address}</li>
                        </ul>
                        <p>確認無誤後，請點擊下方連結以啟用您的帳號：</p>
                        <p><a href="{activation_link}">啟用帳號</a></p>
                        <p>若您並未註冊此帳號，請忽略此封郵件。</p>
                    </body>
                </html>
            """
        )
        mail.send(msg)

        res = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

        return {
            'success': True,
            'data': res
        }, 201
    
class AdminRegisterActivate(Resource):
    def get(self, token):
        try:
            user_id, email = confirm_activation_token(token, salt='admin-email-activate')
        except:
            return {
                "success": False,
                "message": "Invalid activation link"
            }, 200
        
        user = db.session.query(UserSchema).filter(UserSchema.id == user_id, UserSchema.email == email, UserSchema.is_admin == True).first()

        if not user:
            return {
                'success': False,
                'message': "Admin not found"
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
   
# ----------------------------------------------------------------------------

# if admin forget password, admin should contect MAIN_ADMIN
class ForgotPassword(Resource):
    pass
class ResetPassword(Resource):
    pass



