from app import create_app, db
from app.model.users_schema import UserSchema
from app.lib.password_handling import encoded_password
# python -m app.seeds.run_seeds  
def user_seeds():
    app = create_app()
    with app.app_context():
        user_data = [
            UserSchema(name="Alice", email="alice.admin@example.com", password=encoded_password("AdminPass123!"), is_admin=True, address="123 Admin Street, New York, NY", phone="123-456-7890"),
            UserSchema(name="Bob", email="bob.boss@example.com", password=encoded_password("BossMan456@"), is_admin=True, address="456 Leader Lane, Los Angeles, CA", phone="987-654-3210"),
            UserSchema(name="Charlie", email="charlie.guest@example.com", password=encoded_password("Guest123!")),
            UserSchema(name="Diana", email="diana.visitor@example.com", password=encoded_password("VisitMe456$")),
            UserSchema(name="Eli", email="eli.user@example.com", password=encoded_password("User789@#")),
            UserSchema(name="Fay", email="fay.regular@example.com", password=encoded_password("Regular456%")),
        ]

        db.session.add_all(user_data)
        db.session.commit()
        print('User seeds added!')

if __name__ == '__main__':
    user_seeds()

# {
#     "email": "contact@taiwanevent.com",
#     "password": "Company@2025"
# }