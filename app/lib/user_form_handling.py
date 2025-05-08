import re
from marshmallow import Schema, fields, validate, ValidationError

# BASIC USER SETTINGS
def user_phone_validate(value):
    mobile_pattern = r"09\d{8}$"
    if not re.match(mobile_pattern, value):
        raise ValidationError("Invalid mobile number")
    
class LoginValidationForm(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class UserValidationForm(LoginValidationForm):
    name = fields.String(required=True, validate=validate.Length(min=4, max=255))
    phone = fields.String(required=True, validate=user_phone_validate)

class AdminValidationForm(LoginValidationForm):
    name = fields.String(required=True, validate=validate.Length(min=4, max=255))
    phone = fields.String(required=True)
    address = fields.String(required=True)

# ----------------------------------------------------------------
# UPDATED USER SETTINGS
class UpdatedInfoForm(Schema):
    name = fields.String(validate=validate.Length(min=4, max=255))
    email = fields.Email()
    original_password = fields.String(validate=validate.Length(min=6))
    password = fields.String(validate=validate.Length(min=6))
    address = fields.String()


class UpdatedUserInfoForm(UpdatedInfoForm):
    phone = fields.String(validate=user_phone_validate)
class UpdatedAdminInfoForm(UpdatedInfoForm):
    phone = fields.String()

    