from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_activation_token(user_id, email, salt):
    s = URLSafeTimedSerializer(current_app.config['REGISTER_SCRET_KEY'])
    return s.dumps((user_id, email), salt=salt)


def confirm_activation_token(token, salt, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['REGISTER_SCRET_KEY'])
    try:
        user_id, email = s.loads(token, salt=salt, max_age=expiration)
    except:
        return None, None
    return user_id, email