from flask import request
from dateutil import parser
from requests import post

class User: 

    @staticmethod
    def get_by_document(document):
        # se comprueba que el documento ingresado por la empresa, corresponda a un candidato registrado en la aplicación FSUV
        try:
            resp = post(
                'https://dolphin-app-5gjh6.ondigitalocean.app/portfolio/student/get_background_check_info/',
                json = {'student_id': document},
                headers = {'Authorization': request.headers.get('Authorization')}
            )
            data = None

            if resp.status_code == 200:
                data = resp.json()
                # se formatea la fecha de expiración
                data['issue_date'] = parser.parse(data['issue_date'], fuzzy=True).strftime('%d/%m/%Y')

            return data
        except:
            return None