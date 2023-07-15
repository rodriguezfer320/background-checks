import unittest, json, os
from werkzeug.datastructures import FileStorage
from sqlalchemy.sql import text
from app.app import create_app
from app.entities import VerificationRequestModel
from app.database import db
import shutil

class TestVerificationRequest(unittest.TestCase):

    def setUp(self):
        self.app, status = create_app()
        self.client = self.app.test_client()
        self.file = FileStorage(
            stream=open(os.getcwd() + '/tests/document_fake_test.pdf', 'rb'),
            filename='document_fake_test.pdf',
            content_type='application/pdf',
        )

    def test_create_request_required_fields(self):
        res = self.client.post('fs-uv/bc/api/verificacion-solicitud/crear', content_type='multipart/form-data', data={})
        data = {
            "code": 422,
            "errors": {
                "form": {
                    "antecedent": [
                        "Debe seleccionar un antecedente."
                    ],
                    "document": [
                        "Debe ingresar el número de identificación."
                    ],
                    "file_document": [
                        "Debe seleccionar un documento."
                    ],
                    "title": [
                        "Debe ingresar un título."
                    ],
                    "user_sub_key": [
                        "Debe ingresar el sub_key del usuario."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))

    def test_create_request_c(self):
        with self.app.app_context():
            verification_request = db.session.get(VerificationRequestModel, 1)
            
            if verification_request:
                db.session.delete(verification_request)
                db.session.execute(text('TRUNCATE TABLE verification_request RESTART IDENTITY'))
                db.session.commit()

        res = self.client.post(
            'fs-uv/bc/api/verificacion-solicitud/crear', 
            content_type='multipart/form-data', 
            data={
                'title': 'verificación de titulo academico',
                'document': '1118310093',
                'file_document': self.file,
                'antecedent': 7,
                'user_sub_key': '6228a350-99c9-45e1-a6d5-9c8a0b6e8b41'
            }
        )
        self.assertIn('6228a350-99c9-45e1-a6d5-9c8a0b6e8b41_7_university degree.pdf', os.listdir('app/static/verification_request_files/'))
        self.assertEqual(201, res.status_code)
        self.assertEqual('La solicitud se ha creado correctamente.', json.loads(res.data)['message'])

    def test_create_request_duplicate_bug(self):
        res = self.client.post(
            'fs-uv/bc/api/verificacion-solicitud/crear', 
            content_type='multipart/form-data', 
            data={
                'title': 'verificación de titulo academico',
                'document': '1118310093',
                'file_document': self.file,
                'antecedent': 7,
                'user_sub_key': '6228a350-99c9-45e1-a6d5-9c8a0b6e8b41'
            }
        )
        self.assertEqual(400, res.status_code)
        self.assertEqual('Solo se puede crear una solicitud por tipo de antecedente.', json.loads(res.data)['message'])

    def test_update_data_empty_fields(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-datos/1', 
            content_type='application/json', 
            data={}
        )
        data = {
            "code": 422,
            "errors": {
                "json": {
                    "document": [
                        "Debe ingresar el número de identificación."
                    ],
                    "title": [
                        "Debe ingresar un título."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))

    def test_update_data_request_not_registered(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-datos/50', 
            content_type='application/json', 
            json={
                'title': 'verificación de título académico',
                'document': '1118310093'
            }
        )
        self.assertEqual(404, res.status_code)
        self.assertEqual('No se encontró una solicitud de verificación.', json.loads(res.data)['message'])
    
    def test_update_data_request(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-datos/1', 
            content_type='application/json', 
            json={
                'title': 'verificación de título académico',
                'document': '1118310093'
            }
        )
        self.assertEqual(201, res.status_code)
        self.assertEqual('Los datos de la solicitud se han actualizado correctamente.', json.loads(res.data)['message'])

    def test_update_state_empty_fields(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-estado/1', 
            content_type='application/json', 
            data={}
        )
        data = {
            "code": 422,
            "errors": {
                "json": {
                    "comment": [
                        "Debe ingresar un comentario."
                    ],
                    "state": [
                        "Debe seleccionar un estado."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))

    def test_update_state_request_not_registered(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-estado/25', 
            content_type='application/json', 
            json={
                'comment': 'asdfasdfasdf',
                'state': 'rechazada'
            }
        )
        self.assertEqual(404, res.status_code)
        self.assertEqual('No se encontró una solicitud de verificación.', json.loads(res.data)['message'])

    def test_update_state(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-estado/1', 
            content_type='application/json', 
            json={
                'comment': 'El documento que se cargo no corresponde a un titulo academico, corregir.',
                'state': 'rechazada'
            }
        )
        self.assertEqual(201, res.status_code)
        self.assertEqual('El estado de la solicitud se ha actualizado correctamente.', json.loads(res.data)['message'])

    def test_update_document_empty_field(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-documento/1', 
            content_type='multipart/form-data', 
            data={}
        )
        data = {
            "code": 422,
            "errors": {
                "files": {
                    "file_document": [
                        "Debe seleccionar un documento."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }
        self.assertEqual(422, res.status_code)
        self.assertEqual(data, json.loads(res.data))

    def test_update_document_request_not_registered(self):
        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-documento/15', 
            content_type='multipart/form-data', 
            data={
                'file_document': self.file
            }
        )
        self.assertEqual(404, res.status_code)
        self.assertEqual('No se encontró una solicitud de verificación.', json.loads(res.data)['message'])

    def test_update_document_status_other_than_rejected(self):
        # se cambia el estado en la bd
        with self.app.app_context():
            verification_request = db.session.get(VerificationRequestModel, 1)
            verification_request.state = 'pendiente'
            db.session.commit()

        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-documento/1', 
            content_type='multipart/form-data', 
            data={
                'file_document': self.file
            }
        )
        self.assertEqual(400, res.status_code)
        self.assertEqual('El documento de la solicitud solo se puede actualizar cuando el estado sea rechazada.', json.loads(res.data)['message'])
    
    def test_update_document(self):
        # se cambia el estado en la bd
        with self.app.app_context():
            verification_request = db.session.get(VerificationRequestModel, 1)
            verification_request.state = 'rechazada'
            db.session.commit()

        res = self.client.put(
            'fs-uv/bc/api/verificacion-solicitud/editar-documento/1', 
            content_type='multipart/form-data', 
            data={
                'file_document': self.file
            }
        )
        self.assertEqual(201, res.status_code)
        self.assertEqual('El documento de la solicitud se ha actualizado correctamente.', json.loads(res.data)['message'])

    def test_get_file_request_not_registered(self):
        res = self.client.get('fs-uv/bc/api/verificacion-solicitud/file/10')
        self.assertEqual(404, res.status_code)
        self.assertEqual('No se encontró una solicitud de verificación.', json.loads(res.data)['message'])

    def test_get_file_not_found(self):
        # se elimina el archivo subido por el candidato
        os.remove(os.getcwd() + '/app/static/verification_request_files/6228a350-99c9-45e1-a6d5-9c8a0b6e8b41_7_university degree.pdf')

        res = self.client.get('fs-uv/bc/api/verificacion-solicitud/file/1')
        self.assertEqual(400, res.status_code)
        self.assertEqual('No se pudo obtener el archivo.', json.loads(res.data)['message'])

    def test_get_file(self):
        # se copia el archivo de  nuevo
        shutil.copy(
            os.getcwd() + '/tests/document_fake_test.pdf', 
            os.getcwd() + '/app/static/verification_request_files/6228a350-99c9-45e1-a6d5-9c8a0b6e8b41_7_university degree.pdf'
        )

        res = self.client.get('fs-uv/bc/api/verificacion-solicitud/file/1')
        self.assertEqual(200, res.status_code)

    def test_get_request_empty(self):
        res = self.client.get('fs-uv/bc/api/verificacion-solicitud?user_sub_key=1118310094')
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(json.loads(res.data)['data']))

    def test_get_request(self):
        res = self.client.get('fs-uv/bc/api/verificacion-solicitud')
        self.assertEqual(200, res.status_code)
        self.assertNotEqual(0, len(json.loads(res.data)['data']))    