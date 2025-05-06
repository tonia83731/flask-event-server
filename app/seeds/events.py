from app import create_app, db
from app.model.events_schema import EventSchema
from datetime import datetime
import time

def to_timestamp(date):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple()))

def event_seeds():
    app = create_app()

    with app.app_context():
        event_data = [
            EventSchema(
                admin_id=1,
                title="冰雪魔法工作坊",
                category_id=1,  # 教育與課程
                description="一場與艾莎一起學習冰雪魔法的互動課程，適合親子同樂。",
                event_start_date=to_timestamp("2025-06-01 10:00:00"),
                event_end_date=to_timestamp("2025-06-01 12:00:00"),
                apply_start_date=to_timestamp("2025-05-10 00:00:00"),
                apply_end_date=to_timestamp("2025-05-31 23:59:59"),
                url="https://frozen-magic.example.com",
                max_attendees=100
            ), # id = 1
            EventSchema(
                admin_id=1,
                title="冰之交響音樂會",
                category_id=2,  # 音樂與表演
                description="艾莎主辦的音樂會，結合視覺與聽覺的冰雪奇緣體驗。",
                event_start_date=to_timestamp("2025-06-15 19:00:00"),
                event_end_date=to_timestamp("2025-06-15 21:00:00"),
                apply_start_date=to_timestamp("2025-05-20 00:00:00"),
                apply_end_date=to_timestamp("2025-06-14 23:59:59"),
                address="台北市演藝大道99號 冰雪大劇院",
                max_attendees=500
            ), # id = 2
            EventSchema(
                admin_id=2,
                title="花木蘭武術課程",
                category_id=5,  # 體育與健身
                description="由花木蘭親自教授的武術訓練班，培養身心靈的平衡。",
                event_start_date=to_timestamp("2025-07-01 09:00:00"),
                event_end_date=to_timestamp("2025-07-01 11:30:00"),
                apply_start_date=to_timestamp("2025-06-01 00:00:00"),
                apply_end_date=to_timestamp("2025-06-30 23:59:59"),
                address="台南市英勇路88號 武藝館",
                max_attendees=30
            ), # id = 3
            EventSchema(
                admin_id=2,
                title="女性領導論壇",
                category_id=4,  # 商業與科技
                description="花木蘭邀請各界女性領袖，共同探討現代領導力與未來挑戰。",
                event_start_date=to_timestamp("2025-07-15 14:00:00"),
                event_end_date=to_timestamp("2025-07-15 17:00:00"),
                apply_start_date=to_timestamp("2025-06-15 00:00:00"),
                apply_end_date=to_timestamp("2025-07-14 23:59:59"),
                url="https://mulan-leadership.example.com",
                max_attendees=200
            ), # id = 4
            EventSchema(
                admin_id=3,
                title="米奇的創意畫畫課",
                category_id=3,  # 藝術與文化
                description="米奇親自教大家如何畫出屬於自己的創意卡通角色。",
                event_start_date=to_timestamp("2025-08-10 14:00:00"),
                event_end_date=to_timestamp("2025-08-10 16:00:00"),
                apply_start_date=to_timestamp("2025-07-10 00:00:00"),
                apply_end_date=to_timestamp("2025-08-09 23:59:59"),
                address="新竹市卡通大道10號 創意藝廊",
                max_attendees=50
            ), # id = 5
            EventSchema(
                admin_id=3,
                title="米奇線上歡樂派對",
                category_id=6,  # 社交與興趣
                description="加入米奇的線上派對，與全球朋友一起唱歌跳舞！",
                event_start_date=to_timestamp("2025-08-25 19:00:00"),
                event_end_date=to_timestamp("2025-08-25 21:00:00"),
                apply_start_date=to_timestamp("2025-07-20 00:00:00"),
                apply_end_date=to_timestamp("2025-08-24 23:59:59"),
                url="https://mickey-party.example.com",
                max_attendees=1000
            ) # id = 6
        ]

        db.session.add_all(event_data)
        db.session.commit()
        print('Event seeds added!')

if __name__ == '__main__':
    event_seeds()