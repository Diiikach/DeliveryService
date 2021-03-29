from django.test import TestCase
from . import jsons


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
