import unittest, json
from app.app import create_app

class TestBackground(unittest.TestCase):

    def setUp(self):
        self.app, status = create_app()
        self.client = self.app.test_client()

    def test_get_background_empty(self):
        res = self.client.get('fs-uv/bc/api/antecedentes?type=dfsdf')
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(json.loads(res.data)['data']))

    def test_get_background(self):
        res = self.client.get('fs-uv/bc/api/antecedentes')
        self.assertEqual(200, res.status_code)
        self.assertNotEqual(0, len(json.loads(res.data)['data']))