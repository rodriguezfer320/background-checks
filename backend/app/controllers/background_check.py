from flask import jsonify, views, json
from flask_smorest import Blueprint
from datetime import datetime
from ..entities import BackgroundModel, CandidateBackgroundModel, VerificationRequestModel
from ..models import (
    Driver, DisciplinaryBackground, FiscalBackground,
    JudicialBackground, CorrectiveActionBackground, MilitarySituationBackground,
    MilitarySituationBackground, TrafficInfractionBackground
)
from ..schemas import BackgroundCheckQueryArgsSchema
from ..database import db

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

    @bc.arguments(BackgroundCheckQueryArgsSchema, location='query')
    def get(self, args):
        result = []
        #assert 1 == 2

        # falta verificar el numero del documento en otra api
        #

        for ant in args['antecedents']:
            text = self.text.copy()

            # se consultan los datos del antecedente en la BD
            background = BackgroundModel.query.get(ant)

            # se válida el tipo de antecedente
            if background.type == 'web':
                # se consulta la información del antecdente asociado al candidato en la BD
                candidate_background = CandidateBackgroundModel.query\
                                                               .filter(CandidateBackgroundModel.candidate_id == args['document'])\
                                                               .filter(CandidateBackgroundModel.background_id == background.id)\
                                                               .first()

                days = 1

                # si el antecdente ya ha sido consultado, se verifica que hayan pasado 24h
                if (candidate_background is not None):
                    description = json.loads(candidate_background.description)['message']

                    if description != self.message_error:
                        diff = datetime.now() - candidate_background.updated_at
                        days = diff.days

                # si han pasado 24h, se consulta el antecdente en la web
                if days >= 1:
                    antecedent = self.antecedents[background.name]

                    # se consulta la información del antecedente en la web correpondiente
                    try:
                        antecedent.search_for_background({
                            'cedula': args['document'],
                            'fecha-expedicion': '08/08/2016',
                            'url': background.url
                        })
                        text = antecedent.text
                    except:
                        if antecedent.driver.browser: antecedent.driver.close_browser()
                        text['message'] = self.message_error

                    # si el antecdente no se a registrado en la BD, se inerta
                    if candidate_background is None:
                        candidate_background = CandidateBackgroundModel(
                            candidate_id=args['document'],
                            background_id=background.id,
                            description=json.dumps(text)
                        )
                        db.session.add(candidate_background)
                    else:  # si el antecdente estaregistrado en la BD, se actualiza
                        candidate_background.description = json.dumps(text)
                        candidate_background.updated_at = datetime.now()

                    db.session.commit()
                else:  # sino han pasado 24h, se obtiene la información de la BD
                    text = json.loads(candidate_background.description)
            else:  # antededentes que no se consultan en una web
                try:
                    verification_request = VerificationRequestModel.query\
                                                                   .filter(VerificationRequestModel.candidate_id == args['document'])\
                                                                   .filter(VerificationRequestModel.background_id == background.id)\
                                                                   .first()
                    
                    if background.name == 'university degree':
                        if verification_request is None or verification_request.state != 'aprobada':
                            text['message'] = 'El candidato no ha cargado su título académico o esta en proceso de validación.'
                        else:
                            text['message'] = verification_request.comment
                            text['link'] = '/api/verificacion-solicitud/file/{}'.format(verification_request.id)
                except:
                    text['message'] = self.message_error

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