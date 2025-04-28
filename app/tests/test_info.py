from flask import json
from app.tests.base import TestBase

class TestUser(TestBase):
    def test_user_get(self):
        _, user_id, auth_token = self.user_info()
        url = f"/users/{user_id}"

        res = self.client().get(
            url,
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('name', res_data['data'])
        self.assertIn('email', res_data['data'])
        self.assertIn('phone', res_data['data'])
        self.assertIn('is_admin', res_data['data'])

    def test_user_permission_denied(self):
        _, _, auth_token = self.user_info()
        url = "/users/{}".format(2)

        res = self.client().get(
            url,
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Permission denied')

    def test_user_put(self):
        _, user_id, auth_token = self.user_info()
        url = f"/users/{user_id}"

        res = self.client().put(
            url,
            json={
                'name': 'Test new',
                'email': "test123@example.com",
                'phone': '0988776655'
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data']['name'], 'Test new')
        self.assertEqual(res_data['data']['email'], 'test123@example.com')
        self.assertEqual(res_data['data']['phone'], '0988776655')



class TestAdmin(TestBase):
    def test_admin_get(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        url = f"/admin/users/{admin_id}"
        res = self.client().get(
            url,
            headers = {
                'Authorization': auth_token
            }
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('name', res_data['data'])
        self.assertIn('email', res_data['data'])
        self.assertIn('phone', res_data['data'])
        self.assertIn('address', res_data['data'])
        self.assertIn('is_admin', res_data['data'])

    def test_admin_permission_denied(self):
        _, _, auth_token = self.user_info(role="Admin")
        url = "/admin/users/{}".format(2)
        res = self.client().get(
            url,
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Permission denied')
    
    def test_admin_put(self):
        _, admin_id, auth_token = self.user_info(role="Admin", include_data=True)
        url = f"/admin/users/{admin_id}"
        res = self.client().put(
            url,
            json={
                'name': 'Admin new',
                'email': "admin123@example.com",
                'phone': '0988776655'
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data']['name'], 'Admin new')
        self.assertEqual(res_data['data']['email'], 'admin123@example.com')
        self.assertEqual(res_data['data']['phone'], '0988776655')
    def test_admin_put_denied(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        url = f"/admin/users/{admin_id}"
        res = self.client().put(
            url,
            json={
                'name': 'Admin new',
                'email': "admin123@example.com",
                'phone': '0988776655'
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'The current admin does not have permission to perform updates.')