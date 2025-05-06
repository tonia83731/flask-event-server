from app import create_app, db
from app.model.bookings_schema import BookingSchema


def booking_seeds():
    app = create_app()

    with app.app_context():
        booking_data = [
            # Event 1: 冰雪魔法工作坊
            BookingSchema(user_id=2, event_id=1),   # Ariel
            BookingSchema(user_id=5, event_id=1),   # Belle
            BookingSchema(user_id=9, event_id=1),   # Tiana

            # Event 2: 冰之交響音樂會
            BookingSchema(user_id=3, event_id=2),   # Simba
            BookingSchema(user_id=6, event_id=2),   # Stitch

            # Event 3: 花木蘭武術課程
            BookingSchema(user_id=10, event_id=3),  # Woody
            BookingSchema(user_id=2, event_id=3),   # Ariel (updated to existing user)

            # Event 4: 女性領導論壇
            BookingSchema(user_id=3, event_id=4),   # Simba (updated to existing user)
            BookingSchema(user_id=6, event_id=4),   # Stitch (updated to existing user)
            BookingSchema(user_id=9, event_id=4),   # Tiana (updated to existing user)

            # Event 5: 米奇的創意畫畫課
            BookingSchema(user_id=2, event_id=5),   # Ariel (updated to existing user)
            BookingSchema(user_id=5, event_id=5),   # Belle (updated to existing user)

            # Event 6: 米奇線上歡樂派對
            BookingSchema(user_id=3, event_id=6),   # Simba (updated to existing user)
            BookingSchema(user_id=6, event_id=6),   # Stitch (updated to existing user)
            BookingSchema(user_id=9, event_id=6)    # Tiana (updated to existing user)
        ]
        db.session.add_all(booking_data)
        db.session.commit()
        print('Booking seeds added!')

if __name__ == '__main__':
    booking_seeds()