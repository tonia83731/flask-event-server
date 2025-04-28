from flask_jwt_extended import get_jwt, get_jwt_identity

def user_authentication(user_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    identity_id = int(identity)
    if identity_id != user_id or claims["role"] != 'user':
            return False
    return True

def admin_authentication(user_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    identity_id = int(identity)
    if identity_id != user_id or claims["role"] != 'admin':
            return False
    return True