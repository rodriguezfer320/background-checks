from flask import jsonify, views, json, request
from flask_smorest import Blueprint
from datetime import datetime
from dateutil import parser
from requests import post
from ..entities import BackgroundModel, CandidateBackgroundModel, VerificationRequestModel
from ..models import (
    Driver, DisciplinaryBackground, FiscalBackground,
    JudicialBackground, CorrectiveActionBackground, MilitarySituationBackground,
    MilitarySituationBackground, TrafficInfractionBackground
)
from ..schemas import BackgroundCheckQueryArgsSchema
from ..database import db
from ..auth import authentication_required_and_permissions
from ..utils import ROLES

bc = Blueprint('background-check', __name__)

class BackgroundCheckController(views.MethodView):

    def __init__(self):
        super().__init__()
        # se carga el driver que permite interactuar con el navegador
        driver = Driver()
        driver.load_options()

        self.message_error = 'No se pudo obtener la información del canditato en este antecedente, debido a que, ocurrio un error inesperado.'
        self.antecedents = {
            'disciplinary': DisciplinaryBackground(driver),
            'fiscal': FiscalBackground(driver),
            'judicial': JudicialBackground(driver),
            'corrective actions': CorrectiveActionBackground(driver),
            'military situation': MilitarySituationBackground(driver),
            'traffic infraction': TrafficInfractionBackground(driver)
        }
        self.text = {
            'title': None,
            'date': None,
            'message': None,
            'data': None,
            'link': None
        }
    
    @authentication_required_and_permissions(allowedRoles=[ROLES['company']])
    @bc.arguments(BackgroundCheckQueryArgsSchema, location='query')
    def get(self, args):
        # se verifica que el documento del candidato ingresado se encuentre registrado en la aplicación
        data = self._get_user_by_document(args['document'])
        
        if data:
            result = []

            for ant in args['antecedents']:
                # se consultan los datos del antecedente en la BD
                background = db.session.get(BackgroundModel, ant)

                # se válida el tipo de antecedente
                if background.type == 'web':
                    text = self._web_background(args['document'], data['issue_date'], background)
                else:
                    text = self._no_web_background(data['sub_key'], background)

                # se añade la información obtenida
                result.append({
                    'id': background.id,
                    'name': background.name,
                    'type': background.type,
                    'information': text
                })

            return jsonify({
                'code': 200,
                'status': 'SUCCESS',
                'data': result
            }), 200
        else:
            return jsonify({
                'code': 404,
                'status': 'DOCUMENT NOT FOUND',
                'message': 'El candidato no ha actualizado su información o el documento ingresado no pertenece aún candiato registrado.'
            }), 404

    def _get_user_by_document(self, document):
        # se comprueba que el documento ingresado por la empresa, corresponda a un candidato registrado en la aplicación FSUV
        try:
            resp = post(
                'https://dolphin-app-5gjh6.ondigitalocean.app/portfolio/student/get_background_check_info/',
                json={'student_id': document},
                headers={'Authorization': request.headers.get('Authorization')}
            )
            data = None

            if resp.status_code == 200:
                data = resp.json()
                # se formatea la fecha de expiración
                data['issue_date'] = parser.parse(data['issue_date'], fuzzy=True).strftime('%d/%m/%Y')

            return data
        except:
            return None

    def _web_background(self, document, date_expedition, background):
        # se consulta la información del antecedente asociado al candidato en la BD
        candidate_background = CandidateBackgroundModel.query\
                                                       .filter(CandidateBackgroundModel.candidate_id == document)\
                                                       .filter(CandidateBackgroundModel.background_id == background.id)\
                                                       .first()

        days = 1

        # si el antecedente ya ha sido consultado, se verifica que hayan pasado 24h
        if candidate_background:
            description = json.loads(candidate_background.description)['message']

            if description != self.message_error:
                diff = datetime.now() - candidate_background.updated_at
                days = diff.days

        # si han pasado 24h, se consulta el antecedente en la web
        if days >= 1:
            antecedent = self.antecedents[background.name]

            # se consulta la información del antecedente en la web correspondiente
            try:
                antecedent.search_for_background({
                    'document': document,
                    'date-expedition': date_expedition,
                    'url': background.url
                })
                text = antecedent.text
            except:
                antecedent.driver.close_browser()
                text = self.text.copy()
                text['message'] = self.message_error

            # si el antecedente no se ha registrado en la BD, se inserta
            if candidate_background is None:
                candidate_background = CandidateBackgroundModel(
                    candidate_id=document,
                    background_id=background.id,
                    description=json.dumps(text)
                )
                db.session.add(candidate_background)
            else:  # si el antecedente esta registrado en la BD, se actualiza
                candidate_background.description = json.dumps(text)
                candidate_background.updated_at = datetime.now()

            db.session.commit()

            return text
        else:  # sino han pasado 24h, se obtiene la información de la BD
            return json.loads(candidate_background.description)

    def _no_web_background(self, user_sub_key, background):
        try:
            text = self.text.copy()
            verification_request = VerificationRequestModel.query\
                                                           .filter(VerificationRequestModel.user_sub_key == user_sub_key)\
                                                           .filter(VerificationRequestModel.background_id == background.id)\
                                                           .first()
            
            if background.name == 'university degree':
                if verification_request is None or verification_request.state != 'aprobada':
                    text['message'] = 'El candidato no ha cargado su título académico o esta en proceso de validación.'
                else:
                    text['message'] = verification_request.comment
                    text['link'] = '/verificacion-solicitud/file/{id}'.format(id=verification_request.id)
        except:
            text['message'] = self.message_error
        
        return text