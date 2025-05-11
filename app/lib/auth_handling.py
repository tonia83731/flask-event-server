from flask_jwt_extended import get_jwt, get_jwt_identity

class JWTAuth:
    def __init__(self):
        self.identity = int(get_jwt_identity())
        self.claims = get_jwt()
        self.role = self.claims.get("role")
        self.is_active = self.claims.get("is_active", False)
        self.super_flag = self.claims.get("is_super", False)
        # print(self.super_flag)

    def _base_check(self, user_id, required_role):
        return (self.identity == user_id and self.role == required_role and self.is_active is True)
    
    def is_user(self, user_id):
        return self._base_check(user_id, "user")
    
    def is_admin(self, admin_id):
        return self._base_check(admin_id, "admin")
    
    def is_super(self):
        return self.super_flag