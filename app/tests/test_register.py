from flask import json
from app.tests.base import TestBase

class TestUser(TestBase):
    def test_user_register(self):
        res = self.register()

        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data'].get('name'), self.user_data['name'])
        self.assertEqual(res_data['data'].get('email'), self.user_data['email'])
        self.assertEqual(res_data['data'].get('phone'), self.user_data['phone'])

    def test_duplicate_user(self):
        res = self.register()
        self.assertEqual(res.status_code, 201)

        res = self.register()
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'User already existed')

class TestAdmin(TestBase):
    def test_admin_register(self):
        res = self.register(role="Admin")

        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data'].get('name'), self.admin_data['name'])
        self.assertEqual(res_data['data'].get('email'), self.admin_data['email'])

    def test_duplicate_admin(self):
        res = self.register(role="Admin")
        self.assertEqual(res.status_code, 201)

        res = self.register(role="Admin")
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Admin already existed')
