import unittest
import os
from app import create_app, db
from flask import json
from app.lib.code_handling import EventLocation
class TestBase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_ENV'] = 'testing'

        self.app = create_app()
        self.client = self.app.test_client
        self.user_data = {
            'name': 'test',
            'email': 'test@example.com',
            'password': 'test1234',
            'phone': '0912345678'
        }
        self.user_data2 = {
            'name': 'user',
            'email': 'user@example.com',
            'password': 'user1234',
            'phone': '0911335577'
        }
        self.admin_data = {
            'name': 'admin',
            'email': 'admin@example.com',
            'password': 'admin1234',
            'phone': '0987654321',
            'address': "5F, No. 123, Section 4, Ren'ai Road, Da’an District, Taipei City 106, Taiwan"
        }
        self.admin_data2 = {
            'name': 'admin2',
            'email': 'admin2@example.com',
            'password': 'admin1111',
            'phone': '0987654321',
            'address': "5F, No. 123, Section 4, Ren'ai Road, Da’an District, Taipei City 106, Taiwan"
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def register(self, role='User', include_data=False):
        if role == 'User':
            url = '/auth/register'
            # data_to_send = user_data if user_data else self.user_data
            if include_data:
                data = self.user_data2
            else:
                data = self.user_data

            res = self.client().post(
                url,
                json=data
            )
        elif role == 'Admin':
            url = '/admin/auth/register'
            if include_data:
                data = self.admin_data2
            else:
                data = self.admin_data
            res = self.client().post(
                url,
                json=data
            )
        return res
    
    def login(self, role='User', include_data=False):
        if role == 'User':
            url = '/auth/login'
            if include_data:
                data = {
                    'email': "user@example.com",
                    'password': 'user1234'
                }
            else:
                data = {
                    'email': "test@example.com",
                    'password': 'test1234'
                }
            res = self.client().post(
                url,
                json=data
            )
        elif role == 'Admin':
            url = '/admin/auth/login'
            if include_data:
                data = {
                    'email': 'admin2@example.com',
                    'password': 'admin1111',
                }
            else:
                data = {
                    'email': 'admin@example.com',
                    'password': 'admin1234',
                }
            res = self.client().post(
                url,
                json = data
            )

        return res
    
    def user_info(self, role="User", include_data=False):
        self.register(role=role, include_data=include_data)
        res = self.login(role=role, include_data=include_data)
        res_data = json.loads(res.get_data(as_text=True))
        user_id = res_data['data']['id']
        token = res_data['data']['token']
        auth_token = f'Bearer {token}'
        return res, user_id, auth_token
    
    def create_category(self, admin_id, auth_token, category_data=None):
        url = f"/admin/categories/{admin_id}"
        res = self.client().post(
            url,
            json = category_data,
            headers = {
                'Authorization': auth_token
            }
        )

        return res
    
    def create_multiple_category(self, admin_id, auth_token):
        self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
                'name': '其他',
                'code': 'OTH'
            })
        self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
                'name': 'Category1',
                'code': 'C1'
            })
        self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
                'name': 'Category2',
                'code': 'C2'
            })
        
    def create_event(self, admin_id, auth_token, max_attendees=2):
        res = self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
            'name': '其他',
            'code': 'OTH'
        })
        res_data = json.loads(res.get_data(as_text=True))
        category_id = res_data["data"]["id"]

        url = f"/admin/events/{admin_id}"

        res = self.client().post(
            url,
            json = {
                "title": "Python Programming Workshop",
                "category_id": category_id,
                "description": "A workshop to learn Python programming.",
                "event_date": "2025-06-15",
                "event_start_time": "10:00:00",
                "event_end_time": "16:00:00",
                "location": EventLocation.EVENT_OFFLINE,
                "address": "123 Tech Street, Python City",
                # "url": "",
                "price": 50,
                "max_attendees": max_attendees
            },
            headers = {'Authorization': auth_token}
        )

        return res
    def create_event_for_booking(self, max_attendees=2):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res = self.create_event(admin_id=admin_id, auth_token=auth_token, max_attendees=max_attendees)
        res_data = json.loads(res.get_data(as_text=True))
        return res_data['data']['id']
