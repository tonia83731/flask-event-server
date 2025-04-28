from flask import json
from app.tests.base import TestBase


class TestUser(TestBase):
    def test_login(self):
        self.register()
        res = self.login()
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('role', res_data['data'])
        self.assertIn('token', res_data['data'])

    def test_login_format_failed(self):
        self.register()
        url = '/auth/login'
        res = self.client().post(
            url,
            json = {
                'email': 'test',
                'password': 'test1111'
            }
        )

        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('email', res_data['message'])

    def test_login_failed(self):
        self.register()

        url = '/auth/login'
        res = self.client().post(
            url,
            json = {
                'email': 'test@example.com',
                'password': 'test1111'
            }
        )

        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Email or password incorrect.')


class TestAdmin(TestBase):
    def test_admin_login(self):
        self.register(role="Admin")
        res = self.login(role="Admin")
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('role', res_data['data'])
        self.assertIn('token', res_data['data'])
    def test_admin_login_format_failed(self):
        self.register(role="Admin")
        url = '/admin/auth/login'
        res = self.client().post(
            url,
            json = {
                'email': 'admin',
                'password': 'admin1111'
            }
        )

        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('email', res_data['message'])
    def test_admin_login_failed(self):
        self.register(role="Admin")
        url = '/admin/auth/login'
        res = self.client().post(
            url,
            json = {
                'email': 'admin@example.com',
                'password': 'admin1111'
            }
        )
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Email or password incorrect.')
        