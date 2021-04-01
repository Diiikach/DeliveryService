import json
from django.test import TestCase
from . import jsons


class AssignTest(TestCase):
    """
    Testing assigning orders process.
    """
    def test_assign_orders(self):
        orders = 'http://127.0.0.1:8000/orders'
        self.client.post(orders, jsons.orders_json_to_assign, content_type='text')
        self.client.post('http://127.0.0.1:8000/couriers', jsons.courier_json_to_assign_orders, content_type='text')
        req = self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                               content_type='text')
        self.assertEqual(json.loads(req.content.decode('utf-8'))['orders'],
                         json.loads(jsons.valid_assigned_orders)['orders'])

    def test_assign_to_other_courier(self):
        orders = 'http://127.0.0.1:8000/orders'
        self.client.post(orders, jsons.orders_json_to_assign, content_type='text')
        self.client.post('http://127.0.0.1:8000/couriers', jsons.courier_json_to_assign_orders, content_type='text')
        self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                         content_type='text')

        req = self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                               content_type='text')
        self.assertEqual(req.status_code, 200)
        self.assertEqual(json.loads(req.content)['orders'], json.loads(jsons.assign_to_other_courier_ans)['orders'])
