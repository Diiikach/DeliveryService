from django.test import TestCase
from . import jsons
from django.test import Client


class CreatingCouriers(TestCase):
    def test_creating_couriers(self):
        resp = self.client.post('http://127.0.0.1:8000/couriers', jsons.valid_courier_json_load, content_type='text')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.content.decode('utf-8'), jsons.valid_courier_json_ans)

    def test_unvalid_fully(self):
        resp = self.client.post('http://127.0.0.1:8000/couriers', jsons.fully_unvalid_courier_json_load,
                                content_type='text')
        self.assertEqual(resp.status_code, 400)

    def test_partially_unvalid(self):
        resp = self.client.post('http://127.0.0.1:8000/couriers', jsons.parially_courier_json_load, content_type='text')
        self.assertEqual(resp.content.decode('utf-8'), jsons.parially_courier_json_ans)
        self.assertEqual(resp.status_code, 400)


class IntegrationTest(TestCase):
    def test_check_user_info(self):
        self.client.post('http://127.0.0.1:8000/orders', jsons.orders_json_to_assign, content_type='text')
        self.client.post('http://127.0.0.1:8000/couriers', jsons.courier_json_to_assign_orders, content_type='text')
        self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                         content_type='text')

        self.client.patch('http://127.0.0.1:8000/couriers/1', jsons.changed_type_courier,
                          content_type='text')

        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', jsons.complete_order_1,
                                          content_type='text').status_code, 200)

        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', jsons.complete_order_2,
                                          content_type='text').status_code, 400)
        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', jsons.complete_order_3,
                                          content_type='text').status_code, 400)
        self.assertEqual(self.client.get('http://127.0.0.1:8000/couriers/1').status_code,
                         200)

