from django.test import TestCase
from . import jsons


class CreateOrders(TestCase):
    def test_creation(self):
        resp = self.client.post('http://127.0.0.1:8000/orders', jsons.valid_orders_json_load, content_type='text')
        self.assertEqual(resp.content.decode('utf-8'), jsons.valid_orders_json_ans)

    def test_invalid_creation(self):
        resp = self.client.post('http://127.0.0.1:8000/orders', jsons.invalid_orders_json_load, content_type='text')
        self.assertEqual(resp.status_code, 400)

    def test_partialy_invalid_creation(self):
        resp = self.client.post('http://127.0.0.1:8000/orders', jsons.partialy_invalid_orders_json_load, content_type='text')
        self.assertEqual(resp.status_code, 400)