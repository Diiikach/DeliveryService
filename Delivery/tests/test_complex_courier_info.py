import json
from django.test import TestCase
from . import jsons
import requests
import datetime


class IntegrationTest(TestCase):
    """
    Full untegration testing of all system,
    """
    def test_full1(self):
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

    def test_full2(self):
        orders = self.client.post('http://127.0.0.1:8000/orders', jsons.load_orders_final, content_type='text')
        self.assertEqual(self.client.post('http://127.0.0.1:8000/couriers', jsons.courier_json_to_assign_orders,
                                          content_type='text').status_code, 201)
        self.assertEqual(orders.status_code, 201)
        assigned = self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                                    content_type='text')

        self.assertEqual(assigned.status_code, 200)
        self.assertEqual(assigned.content.decode('utf-8').split('"assign_time"')[0],
                         jsons.current_assign_resp.split('"assign_time"')[0])

        data = json.loads(jsons.complete_order_2)
        data["complete_time"] = str(datetime.datetime.now().isoformat())  + 'Z'
        data = json.dumps(data)
        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', data,
                                          content_type='text').status_code, 200)
        data = json.loads(jsons.complete_order_3)
        data["complete_time"] = str(datetime.datetime.now().isoformat()) + 'Z'
        data = json.dumps(data)

        self.assertEqual(self.client.post('http://127.0.0.1:8000/orders/complete', data,
                                          content_type='text').status_code, 200)
        self.assertEqual(self.client.get('http://127.0.0.1:8000/couriers/1').content.decode('utf-8'),
                         jsons.current_full_info_ans)

    def test_full3(self):
        orders = self.client.post('http://127.0.0.1:8000/orders', jsons.load_orders_final2, content_type='text')
        self.assertEqual(self.client.post('http://127.0.0.1:8000/couriers', jsons.courier_json_to_assign_orders,
                                          content_type='text').status_code, 201)

        self.assertEqual(orders.status_code, 201)
        assigned = self.client.post('http://127.0.0.1:8000/orders/assign', jsons.courier_json_to_assign_orders_id,
                                    content_type='text')
        self.assertEqual(assigned.status_code, 200)

        data = json.loads(jsons.complete_order_3)
        data["complete_time"] = str(datetime.datetime.now().isoformat()) + 'Z'
        data = json.dumps(data)
        competed = self.client.post('http://127.0.0.1:8000/orders/complete', data, content_type='text')
        self.assertEqual(competed.status_code, 200)
        courier_info = self.client.get('http://127.0.0.1:8000/couriers/1')
        print(courier_info.content)