import unittest, json
from app.app import create_app

class TestBackgroundCheck(unittest.TestCase):

    def setUp(self):
        self.app, status = create_app()
        self.client = self.app.test_client()

    def test_empty_fields(self):
        res = self.client.get('fs-uv/bc/api/verificacion-antecedentes')
        data = {
            "code": 422,
            "errors": {
                "query": {
                    "antecedents": [
                        "Debe seleccionar al menos un antecedente."
                    ],
                    "document": [
                        "Debe ingresar el número de identificación."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))

    def test_incorrect_document(self):
        res = self.client.get('fs-uv/bc/api/verificacion-antecedentes?document=12569&antecedents=1')
        data = {
            "code": 422,
            "errors": {
                "query": {
                    "document": [
                        "Ingrese un número de identificación entre 8 y 10 digitos."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))
    
    def test_incorrect_background(self):
        res = self.client.get('fs-uv/bc/api/verificacion-antecedentes?document=1118310092&antecedents=1&antecedents=1')
        data = {
            "code": 422,
            "errors": {
                "query": {
                    "antecedents": [
                        "No modifique las propiedades de las opciones, no deden haber opciones repetidas."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))
    
    def test_get_background(self):
        res = self.client.get('fs-uv/bc/api/verificacion-antecedentes?document=1118310093&antecedents=3&antecedents=7')
        res_data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(2, len(res_data['data']))
        self.assertEqual(3, res_data['data'][0]['id'])
        self.assertEqual('judicial', res_data['data'][0]['name'])
        self.assertEqual(7, res_data['data'][1]['id'])
        self.assertEqual('university degree', res_data['data'][1]['name'])