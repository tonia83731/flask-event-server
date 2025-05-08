from app import create_app, db
from app.model.users_schema import UserSchema
from app.lib.password_handling import encoded_password
# python -m app.seeds.users  
def user_seeds():
    app = create_app()
    with app.app_context():
        user_data = [
            UserSchema(
                name="TestAdmin",
                email="a83731americacowchang@gmail.com",
                password=encoded_password("TestAdmin1234"),
                is_active=True,
                is_admin=True,
                is_super=True,
                address="新北市中和區成功路123號",
                phone="0912345678"
            )
        ]

        db.session.add_all(user_data)
        db.session.commit()
        print('User seeds added!')

if __name__ == '__main__':
    user_seeds()