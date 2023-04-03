from flask import jsonify
from flask_smorest import Blueprint
from datetime import datetime
from app.models.driver import Driver
from app.models.disciplinary_background import DisciplinaryBackground
from app.models.fiscal_background import FiscalBackground
from app.models.judicial_background import JudicialBackground
from app.models.corrective_action_background import CorrectiveActionBackground
from app.models.military_situation_background import MilitarySituationBackground
from app.models.traffic_infraction_background import TrafficInfractionBackground
from app.models.database_connection import session
from app.entities.background import Background
from app.entities.candidate_background import CandidateBackground
from app.entities.verification_request import VerificationRequest
from app.schemas.background_check_schema import GetDataSchema

bbc = Blueprint('background_check', __name__, url_prefix='/api/verificacion-antecedentes', description='Operaciones de verificación de antecedentes.')

@bbc.get('/')
@bbc.arguments(GetDataSchema, location='json')
def get_antecedents(data):
    # se carga el driver que permite interactuar con el navegador
    driver = Driver()
    driver.load_options()
    
    result = {}

    for ant in data['antecedents']:
        text = None

        # se consultan los datos del antecedente en la BD
        background = session.query(Background).get(ant)

        # se válida el tipo de antecedente
        if background.type == 'web':
            # se consulta la información del antecdente asociado al candidato en la BD
            candidate_background = session.query(CandidateBackground)\
                                          .filter(CandidateBackground.candidate_id == data['document'])\
                                          .filter(CandidateBackground.background_id == background.id)\
                                          .first()
            
            days = 1

            # si el antecdente ya ha sido consultado, se verifica que hayan pasado 24h
            if (candidate_background is not None and 
                candidate_background.description != 'No se pudo obtener la información del canditato en este antecdente, debido a que, ocurrio un error inesperado.'):
                    now = datetime.now()
                    diff = now - candidate_background.updated_at
                    days = diff.days
            
            # si han pasado 24h, se consulta el antecdente en la web
            if days >= 1:
                antecedent = None

                if background.name == 'disciplinary': antecedent = DisciplinaryBackground()
                elif background.name == 'fiscal': antecedent = FiscalBackground()
                elif background.name == 'judicial': antecedent = JudicialBackground()
                elif background.name == 'corrective actions': antecedent = CorrectiveActionBackground()
                elif background.name == 'military situation': antecedent = MilitarySituationBackground()
                elif background.name == 'traffic infraction': antecedent = TrafficInfractionBackground()
                
                antecedent.driver = driver

                # se consulta la información del antecdente en la web correpondiente
                try:
                    antecedent.search_for_background({
                        'cedula': data['document'],
                        'fecha-expedicion': '08/08/2016',
                        'url': background.url
                    })
                    text = antecedent.text
                except:
                    antecedent.driver.close_browser()
                    text = 'No se pudo obtener la información del canditato en este antecdente, debido a que, ocurrio un error inesperado.'

                # si el antecdente no se a registrado en la BD, se inerta
                if candidate_background is None:
                    candidate_background = CandidateBackground(
                        candidate_id = data['document'], 
                        background_id = background.id, 
                        description = text
                    )
                    session.add(candidate_background)
                else: # si el antecdente estaregistrado en la BD, se actualiza
                    candidate_background.description = text
                    candidate_background.updated_at = datetime.now()
                
                session.commit()
            else: # sino han pasado 24h, se obtiene la información de la BD
                text = candidate_background.description                
        else:# antededentes que no se consultan en una web
            verification_request = session.query(VerificationRequest)\
                                          .filter(VerificationRequest.candidate_id == data['document'])\
                                          .filter(VerificationRequest.background_id == background.id)\
                                          .first()
            
            if background.name == 'university degree': 
                if verification_request is None or verification_request.state != 'aprobada':
                    text = 'El candidato no ha cargado su título académico o esta en proceso de validación.'
                else:
                    text = verification_request.comment
        
        # se añade la información obtenida
        result[background.name] = text
    
    # se genera una respuesta en formato JSON
    return jsonify({
        'results-background': result
    })