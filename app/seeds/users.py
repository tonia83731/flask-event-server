from app import create_app, db
from app.model.users_schema import UserSchema
from app.lib.password_handling import encoded_password
# python -m app.seeds.users  
def user_seeds():
    app = create_app()
    with app.app_context():
        user_data = [
            # UserSchema(name="Elsa", email="elsa.admin@example.com", password=encoded_password("FrozenQueen123!"), is_admin=True, address="台北市冰雪大道1號", phone="0912345678"),
            # UserSchema(name="Ariel", email="ariel.user@example.com", password=encoded_password("Mermaid456!"), is_admin=False, address="高雄市海洋路22號", phone="0923456789"), # id=2
            # UserSchema(name="Simba", email="simba.user@example.com", password=encoded_password("LionKing789!"), is_admin=False, address="台中市榮耀街3號", phone="0934567890"), # id=3
            # UserSchema(name="Mulan", email="mulan.admin@example.com", password=encoded_password("Warrior321!"), is_admin=True, address="台南市花木巷88弄", phone="0945678901"),
            # UserSchema(name="Belle", email="belle.user@example.com", password=encoded_password("BookLover147!"), is_admin=False, address="新北市玫瑰路147號", phone="0956789012"), # id=5
            # UserSchema(name="Stitch", email="stitch.user@example.com", password=encoded_password("Ohana258!"), is_admin=False, address="桃園市外星大道258號", phone="0967890123"), # id=6
            # UserSchema(
            #     name="Mickey",
            #     email="mickey.admin@example.com",
            #     password=encoded_password("MickeyMagic1928!"),
            #     is_admin=True,
            #     address="新竹市奇幻路1928號",
            #     phone="0923456789"
            # )
            # UserSchema(
            #     name="Tiana",
            #     email="tiana.user@example.com",
            #     password=encoded_password("FrogPrincess789!"),
            #     is_admin=False,
            #     address="台南市河畔街789號",
            #     phone="0978901234"
            # ), # id=9
            # UserSchema(
            #     name="Woody",
            #     email="woody.user@example.com",
            #     password=encoded_password("Sheriff456!"),
            #     is_admin=False,
            #     address="台中市玩具巷456弄",
            #     phone="0989012345"
            # ) # id=10

            UserSchema(
                name="TestAdmin",
                email="a83731americacowchang@gmail.com",
                password=encoded_password("TestAdmin1234"),
                is_admin=True,
                is_admin_main=True,
                address="新北市中和區成功路123號",
                phone="0912345678"
            ) 

        ]

        db.session.add_all(user_data)
        db.session.commit()
        print('User seeds added!')

if __name__ == '__main__':
    user_seeds()