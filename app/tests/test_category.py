from flask import json
from app.tests.base import TestBase


class TestCategories(TestBase):
    def test_category_created(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res= self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
                'name': '其他',
                'code': 'OTH'
            })

        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('name', res_data['data'])
        self.assertIn('code', res_data['data'])

    def test_category_get(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res= self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
                'name': '其他',
                'code': 'OTH'
            })
        
        res_data = json.loads(res.get_data(as_text=True))

        url = f"/admin/categories/{admin_id}/{res_data["data"]["id"]}"
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
        self.assertIn('code', res_data['data'])

    def test_category_put(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res= self.create_category(admin_id=admin_id, auth_token=auth_token, category_data={
                'name': '其他',
                'code': 'OTH'
            })
        
        res_data = json.loads(res.get_data(as_text=True))
        
        url = f"/admin/categories/{admin_id}/{res_data["data"]["id"]}"
        res = self.client().put(
            url,
            json = {
                'name': '其他 新',
                'code': 'OTH N'
            },
            headers = {
                'Authorization': auth_token
            }
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data']['name'], '其他 新')
        self.assertEqual(res_data['data']['code'], 'OTH N')

    def test_categories_get(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        self.create_multiple_category(admin_id=admin_id, auth_token=auth_token)
        
        url = "/categories"
        res = self.client().get(
            url
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(res_data['data']), 3)