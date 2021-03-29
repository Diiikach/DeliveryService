from django.test import TestCase
from . import jsons


class IntegrationTest(TestCase):
    def test_check_user_info(self):
        self.client.post('http://127.0.0.1:8000/orders', jsons.orders_json_to_assign, content_type='text')
        self.client.post('http://127.0.0.1:8000/couriers', jsons.courier_json_to_assign_orders, content_type='text')
        self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                         content_type='text')

        resp = self.client.patch('http://127.0.0.1:8000/couriers/1', jsons.changed_type_courier,
                                 content_type='text')

        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', jsons.complete_order_1,
                                          content_type='text').status_code, 200)
        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', jsons.complete_order_2,
                                          content_type='text').status_code, 400)
        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', jsons.complete_order_3,
                                          content_type='text').status_code, 400)

        self.assertEqual(self.client.get('http://127.0.0.1:8000/couriers/1').content.decode('utf-8'), jsons.valid_full_user_ifo)