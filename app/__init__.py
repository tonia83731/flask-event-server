from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()

from app.model.users_schema import UserSchema
from app.model.category_schema import CategorySchema
from app.model.img_schema import ImgSchema
from app.model.events_schema import EventSchema
from app.model.bookings_schema import BookingSchema
from app.model.qr_schema import QRcodeSchema

from app.resource.hello import Hello
from app.resource.user.user_auth import UserRegister, UserLogin
from app.resource.admin.admin_auth import AdminRegister, AdminLogin
from app.resource.auth import RegisterActivate, ForgotPassword, ResetPassword
from app.resource.image import UploadImages, Image
from app.resource.qrcode import QRcode
from app.resource.user.user_info import UserInfo
from app.resource.admin.admin_info import AdminInfo
from app.resource.category import Categories, AdminCategories
from app.resource.events import Events, Event
from app.resource.admin.admin_event import AdminEvents, AdminEvent, AdminEventBookings, AdminEventCanceled
from app.resource.user.user_booking import EventBooking, ClientBooking, ClientBookings, ClientBookingCanceled
from app.resource.ticket import Ticket, TicketConfirmed

from app.lib.event_status_handling import update_event_status

from app.extensions import mail
from app.config import app_config

ENV = os.getenv('FLASK_ENV', 'development')
scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    CORS(app)
    # CORS(app, origins=["http://localhost:3000", "https://your-frontend.com"])
    api = Api(app)
    print(f"🚀 Starting app in {ENV} mode")
    app.config.from_object(app_config[ENV])
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    mail.init_app(app)

    # scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: update_event_status(app), trigger='interval', minutes=1)
    scheduler.start()

    api.add_resource(Hello, '/')
    # EVENT
    api.add_resource(Events, '/events')
    api.add_resource(Event, '/events/<int:event_id>')
    api.add_resource(AdminEvents, '/admin/events/<int:admin_id>')
    api.add_resource(AdminEvent, '/admin/events/<int:admin_id>/<int:event_id>')
    api.add_resource(AdminEventBookings, '/admin/events/<int:admin_id>/<int:event_id>/bookings')
    api.add_resource(AdminEventCanceled, '/admin/events/<int:admin_id>/<int:event_id>/canceled')
    
    # BOOKING
    api.add_resource(EventBooking, "/bookings/<int:user_id>/<int:event_id>/created")
    api.add_resource(ClientBookings, "/bookings/<int:user_id>")
    api.add_resource(ClientBooking, "/bookings/<int:user_id>/<int:booking_id>")
    api.add_resource(ClientBookingCanceled, "/bookings/<int:user_id>/<int:booking_id>/canceled")
    
    # TICKET
    api.add_resource(Ticket, "/ticket/<int:booking_id>")
    api.add_resource(TicketConfirmed, "/ticket/<int:booking_id>/confirmed")

    # CATEGORY
    api.add_resource(Categories, '/categories')
    api.add_resource(AdminCategories, '/admin/categories/<int:admin_id>')

    # USER
    api.add_resource(UserInfo, "/users/<int:user_id>")
    api.add_resource(AdminInfo, "/admin/users/<int:admin_id>")

    api.add_resource(UserRegister, "/auth/register", endpoint="user_register")
    api.add_resource(UserLogin, "/auth/login", endpoint="user_login")
    api.add_resource(AdminRegister, "/admin/auth/register", endpoint="admin_register")
    api.add_resource(AdminLogin, "/admin/auth/login", endpoint="admin_login")
    
    api.add_resource(RegisterActivate, "/activate/<token>")
    api.add_resource(ForgotPassword, "/forgot-password")
    api.add_resource(ResetPassword, "/reset-password/<token>")

    # IMAGE
    api.add_resource(UploadImages, "/upload/<int:admin_id>")
    api.add_resource(Image, "/image/<int:img_id>")
    # QRCODE
    api.add_resource(QRcode, "/qrcode/<int:qrcode_id>")

    return app

# do I need to compy migrations