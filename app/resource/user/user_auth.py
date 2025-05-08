import bcrypt
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app import db
from app.model.users_schema import UserSchema
from app.lib.password_handling import encoded_password
from app.lib.token_handling import confirm_activation_token
from app.lib.user_form_handling import UserValidationForm, LoginValidationForm
from app.lib.email_handling import send_activate_email


class UserRegister(Resource):
    def post(self):
        """ INPUT FROM MARSHMALLOW """
        user_validation = UserValidationForm()
        form_input = request.get_json()

        try:
            form = user_validation.load(form_input)
        except ValidationError as err:
            return {
                "message": err.messages
            }, 400
        
        is_existed = db.session.query(UserSchema).filter(UserSchema.email == form['email']).first()
        if is_existed:
            return {
                'message': 'Email already existed'
            }, 400
        
        
        hash = encoded_password(form['password'])
        form['password'] = hash
        user = UserSchema(**form)
        user.created()

        # SEND ACTIVATION EMAIL
        send_activate_email(user.id, user.email, user.name)

        return {
            'success': True,
            "message": f"User #{user.id} registered success"
        }, 201

class UserLogin(Resource):
    def post(self):
        login_validation = LoginValidationForm()
        form_input = request.get_json()

        try:
            form = login_validation.load(form_input)
        except ValidationError as err:
            # print(err)
            return {
                "message": err.messages
            }, 400

        user = db.session.query(UserSchema).filter(UserSchema.email == form['email'], UserSchema.is_admin == False).first()
        if not user:
            return {
                'message': 'Email or password incorrect.'
            }, 400
        
        if not user.is_active:
            return {
                'message': 'Please activate your account before logging in.'
            }, 400
        
        is_password_match = bcrypt.checkpw(form['password'].encode(), user.password.encode())

        if not is_password_match:
            return {
                'message': 'Email or password incorrect.'
            }, 400

        user_data = {
            'id': user.id,
            'role': 'admin' if user.is_admin else 'user',
        }
        access_token = create_access_token(identity=str(user.id), additional_claims={
            "role": user_data["role"],
            "is_active": user.is_active,
            "is_super": user.is_super
        })
        user_data['token'] = access_token
        return {
            'success': True,
            'data': user_data
        }, 200


# -----------------------------------------------------

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