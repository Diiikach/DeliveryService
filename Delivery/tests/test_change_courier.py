import json
from django.test import TestCase
from couriers.models import Courier
from . import jsons


class ChangeCourier(TestCase):
    def test_change_region(self):
        self.client.post('http://127.0.0.1:8000/couriers', jsons.valid_courier_json_load, content_type='text')
        resp = self.client.patch('http://127.0.0.1:8000/couriers/1', jsons.change_courier_regions_valid,
                                 content_type='text')
        self.assertEqual(resp.content.decode('utf-8'), jsons.change_courier_regions_valid_ans)

    def test_change_wh(self):
        self.client.post('http://127.0.0.1:8000/couriers', jsons.valid_courier_json_load, content_type='text')
        resp = self.client.patch('http://127.0.0.1:8000/couriers/1', jsons.change_courier_wh_valid,
                                 content_type='text')
        self.assertEqual(resp.content.decode('utf-8'), jsons.change_courier_wh_valid_ans)

    def test_change_type(self):
        self.client.post('http://127.0.0.1:8000/couriers', jsons.valid_courier_json_load, content_type='text')
        resp = self.client.patch('http://127.0.0.1:8000/couriers/1', jsons.change_courier_type_valid,
                                 content_type='text')
        self.assertEqual(resp.content.decode('utf-8'), jsons.change_courier_type_valid_ans)

