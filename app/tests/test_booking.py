from flask import json
from app.tests.base import TestBase
from app.lib.code_handling import BookingStatus


class TestBookings(TestBase):
    def test_booking_create(self):
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
        self.assertEqual(res_data['data'].get('status'), BookingStatus.BOOKING_PENDING)
        self.assertIn('name', res_data['data'])
        self.assertIn('email', res_data['data'])
        self.assertIn('phone', res_data['data'])

    def test_event_full(self):
        event_id = self.create_event_for_booking(max_attendees=1)
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
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'Event is fully booked')

    def test_booking_already_existed(self):
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
        res = self.client().post(
            url,
            json = {
                "name": "test",
                "email": "test@example.com",
                "phone": "0912345678"
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 400)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'User already booked')

    def test_booking_get(self):
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
        res_data = json.loads(res.get_data(as_text=True))
        booking_id = res_data['data']['id']

        url = f"/bookings/{user_id}/{booking_id}"
        res = self.client().get(
            url,
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('name', res_data['data'])
        self.assertIn('email', res_data['data'])
        self.assertIn('phone', res_data['data'])
        self.assertIn('status', res_data['data'])
        
    def test_booking_put(self):
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
        res_data = json.loads(res.get_data(as_text=True))
        booking_id = res_data['data']['id']

        url = f"/bookings/{user_id}/{booking_id}/updated"
        res = self.client().put(
            url,
            json = {
                "phone": "0933221166"
            },
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('name', res_data['data'])
        self.assertIn('email', res_data['data'])
        self.assertIn('phone', res_data['data'])
        self.assertIn('status', res_data['data'])

    def test_booking_canceled(self):
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
        res_data = json.loads(res.get_data(as_text=True))
        booking_id = res_data['data']['id']

        url = f"/bookings/{user_id}/{booking_id}/canceled"
        res = self.client().put(
            url,
            headers = {'Authorization': auth_token}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['data'].get('status'), BookingStatus.BOOKING_CANCELED)