from flask import json
from app.tests.base import TestBase
from app.lib.code_handling import EventStatus, BookingStatus

class TestEvents(TestBase):
    def test_event_created(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res = self.create_event(admin_id=admin_id, auth_token=auth_token)
        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('title', res_data['data'])
        self.assertIn('description', res_data['data'])
        self.assertIn('event_date', res_data['data'])
        self.assertIn('event_start_time', res_data['data'])
        self.assertIn('event_end_time', res_data['data'])
        self.assertIn('location', res_data['data'])
        self.assertIn('price', res_data['data'])
        self.assertIn('max_attendees', res_data['data'])
        self.assertEqual(res_data['data'].get('status'), EventStatus.EVENT_AVAILABLE)
    def test_event_get(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res = self.create_event(admin_id=admin_id, auth_token=auth_token)
        res_data = json.loads(res.get_data(as_text=True))
        event_id = res_data["data"]["id"]

        url = f"/admin/events/{admin_id}/{event_id}"
        res = self.client().get(
            url,
            headers={
                'Authorization': auth_token
            }
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('title', res_data['data'])
        self.assertIn('description', res_data['data'])
        self.assertIn('event_date', res_data['data'])
        self.assertIn('event_start_time', res_data['data'])
        self.assertIn('event_end_time', res_data['data'])
        self.assertIn('location', res_data['data'])
        self.assertIn('price', res_data['data'])
        self.assertIn('max_attendees', res_data['data'])
        self.assertIn('status', res_data['data'])
    def test_event_put(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res = self.create_event(admin_id=admin_id, auth_token=auth_token)
        res_data = json.loads(res.get_data(as_text=True))
        event_id = res_data["data"]["id"]

        url = f"/admin/events/{admin_id}/{event_id}"
        res = self.client().put(
            url,
            json={
                "title": "Python Programming Workshop new",
                "description": "A workshop to learn Python programming. New",
                "event_date": "2025-06-25",
                "event_start_time": "09:00:00",
                "event_end_time": "17:00:00", 
                "max_attendees": 101
            },
            headers={
                'Authorization': auth_token
            }
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('id', res_data['data'])
        self.assertIn('title', res_data['data'])
        self.assertIn('description', res_data['data'])
        self.assertIn('event_date', res_data['data'])
        self.assertIn('event_start_time', res_data['data'])
        self.assertIn('event_end_time', res_data['data'])
        self.assertIn('location', res_data['data'])
        self.assertIn('price', res_data['data'])
        self.assertIn('max_attendees', res_data['data'])
        self.assertIn('status', res_data['data'])
    def test_event_canceled(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res = self.create_event(admin_id=admin_id, auth_token=auth_token)
        res_data = json.loads(res.get_data(as_text=True))
        event_id = res_data["data"]["id"]

        url = f"/admin/events/{admin_id}/{event_id}/canceled"
        res = self.client().put(
            url,
            headers={'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data'].get('status'), EventStatus.EVENT_CANCELED)
    def test_event_deleted(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        res = self.create_event(admin_id=admin_id, auth_token=auth_token)
        res_data = json.loads(res.get_data(as_text=True))
        event_id = res_data["data"]["id"]

        url = f"/admin/events/{admin_id}/{event_id}"
        res = self.client().delete(
            url,
            headers = {"Authorization": auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Event and related bookings have been deleted.')
    def test_events_get(self):
        _, admin_id, auth_token = self.user_info(role="Admin")
        self.create_event(admin_id=admin_id, auth_token=auth_token)
    
        url = "/events"
        res = self.client().get(
            url
        )
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(res_data['data']), 1)

    def test_event_booking_get(self):
        event_id = self.create_event_for_booking()
        _, user_id, auth_token = self.user_info()
        url = f"/bookings/{user_id}/{event_id}/created"
        res = self.client().post(
            url,
            json = {
                "name": "test",
                "email": "test@example.com",
                "phone": "0912345678"
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 201)
        _, user_id, auth_token = self.user_info(role="User", include_data=True)
        url = f"/bookings/{user_id}/{event_id}/created"
        res = self.client().post(
            url,
            json = {
                "name": "user",
                "email": "user@example.com",
                "phone": "0912345678"
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 201)

        _, admin_id, auth_token = self.user_info(role="Admin")
        url = f"/admin/events/{admin_id}/{event_id}/bookings"
        res = self.client().get(
            url,
            headers = {
                'Authorization': auth_token
            }
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(res_data['data']), 2)

    def test_event_booking_updated(self):
        event_id = self.create_event_for_booking()
        _, user_id, auth_token = self.user_info()
        url = f"/bookings/{user_id}/{event_id}/created"
        res = self.client().post(
            url,
            json = {
                "name": "test",
                "email": "test@example.com",
                "phone": "0912345678"
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.get_data(as_text=True))
        booking_id = res_data['data']['id']
        _, admin_id, auth_token = self.user_info(role="Admin")

        url = f"/admin/bookings/{admin_id}/{booking_id}/confirmed"
        res = self.client().put(
            url,
            headers = {'Authorization': auth_token}
        )

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data["data"]['status'], BookingStatus.BOOKING_CONFIRMED)
