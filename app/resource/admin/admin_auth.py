import bcrypt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app import db
from app.lib.password_handling import encoded_password
from app.model.users_schema import UserSchema
from app.lib.user_form_handling import AdminValidationForm, LoginValidationForm
from app.lib.email_handling import send_activate_email
class AdminRegister(Resource):
    def post(self):
        admin_validation = AdminValidationForm()
        form_input = request.get_json()

        try:
            form = admin_validation.load(form_input)
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
        form['is_admin'] = True
        user = UserSchema(**form)
        user.created()

        # SEND ACTIVATION EMAIL
        send_activate_email(user.id, user.email, user.name)

        return {
            'success': True,
            "message": f"Admin #{user.id} registered success"
        }, 201

class AdminLogin(Resource):
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

        user = db.session.query(UserSchema).filter(UserSchema.email == form['email'], UserSchema.is_admin == True).first()
        if not user or (user and not user.is_admin):
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