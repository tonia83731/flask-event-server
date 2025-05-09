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

# [
#   {
#     "name": "Mickey Mouse",
#     "email": "mickey@disney.com",
#     "password": "mickey123",
#     "phone": "+886912345678",
#     "address": "台北市迪士尼大道123號10巷1弄"
#   },
#   {
#     "name": "Donald Duck",
#     "email": "donald@disney.com",
#     "password": "donald123",
#     "phone": "+886987654321",
#     "address": "台中市鴨子街45號2巷5弄"
#   },
#   {
#     "name": "Goofy",
#     "email": "goofy@disney.com",
#     "password": "goofy123",
#     "phone": "+886112233445",
#     "address": "高雄市高飛路89號7巷8弄"
#   },
#   {
#     "name": "Minnie Mouse",
#     "email": "minnie@disney.com",
#     "password": "minnie123",
#     "phone": "+886223344556",
#     "address": "台北市花園街56號3巷2弄"
#   },
#   {
#     "name": "Pluto",
#     "email": "pluto@disney.com",
#     "password": "pluto123",
#     "phone": "+886334455667",
#     "address": "新北市月亮路12號1巷4弄"
#   },
#   {
#     "name": "Daisy Duck",
#     "email": "daisy@disney.com",
#     "password": "daisy123",
#     "phone": "+886445566778",
#     "address": "台中市紫藤街78號5巷3弄"
#   }
# ]
