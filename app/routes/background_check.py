from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json
from datetime import datetime
from ..models.driver import Driver
from ..models.disciplinary_background import DisciplinaryBackground
from ..models.fiscal_background import FiscalBackground
from ..models.judicial_background import JudicialBackground
from ..models.corrective_action_background import CorrectiveActionBackground
from ..models.military_situation_background import MilitarySituationBackground
from ..models.traffic_infraction_background import TrafficInfractionBackground
from ..models.database import session
from ..entities.background import Background
from ..entities.candidate_background import CandidateBackground
from ..request.request_background_check import request_background_check

background_check_scope = Blueprint('api', __name__)

@background_check_scope.route('verificacion-antecedentes', methods=('GET',))
@expects_json(request_background_check)
def background_check():
    request_data = request.get_json()
    driver = Driver()
    driver.load_options()
    result = {}

    for ant in request_data['antecedents']:
        text = None
        background = session.query(Background).filter(Background.name == ant).first()
        candidate_background = session.query(CandidateBackground).\
                                       filter(CandidateBackground.candidate_id == int(request_data['document']), 
                                              CandidateBackground.background_id == background.id).\
                                       first()

        if background.type == 'web':
            days = 1

            if candidate_background is not None:
                now = datetime.now()
                diff = now - candidate_background.updated_at
                days = diff.days
            
            if days >= 1:
                antecedent = None
                data = {
                    'cedula': request_data['document']
                }

                if ant == 'disciplinary':
                    antecedent = DisciplinaryBackground()
                    data['url'] = 'https://www.procuraduria.gov.co/Pages/Generacion-de-antecedentes.aspx'
                    data['tipo-documento'] = '1'
                elif ant == 'fiscal':
                    antecedent = FiscalBackground()
                    data['url'] = 'https://www.contraloria.gov.co/web/guest/persona-natural'
                    data['tipo-documento'] = 'CC'
                elif ant == 'judicial':
                    antecedent = JudicialBackground()
                    data['url'] = 'https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml'
                    data['tipo-documento'] = 'cc'
                elif ant == 'corrective actions':
                    antecedent = CorrectiveActionBackground()
                    data['url'] = 'https://srvcnpc.policia.gov.co/PSC/frm_cnp_consulta.aspx'
                    data['tipo-documento'] = '55'
                    data['fecha-expedicion'] = '08/08/2016'
                elif ant == 'military situation': 
                    antecedent = MilitarySituationBackground()
                    data['url'] = 'https://www.libretamilitar.mil.co/Modules/Consult/MilitarySituation'
                    data['tipo-documento'] = '100000001'
                elif ant == 'traffic infraction':
                    antecedent = TrafficInfractionBackground()
                    data['url'] = 'http://www2.simit.org.co/Simit/verificar/contenido_verificar_pago_linea.jsp'
                    data['tipo-documento'] = '1'
                
                antecedent.driver = driver
                antecedent.search_for_background(data)
                text = antecedent.text

                _candidate_background = CandidateBackground(
                    candidate_id = int(request_data['document']), 
                    background_id = background.id, 
                    description = text
                )
                session.add(_candidate_background)
                session.commit()
            else:
                text = candidate_background.description                
        else:
            pass

        result[ant] = text
        
    return jsonify({
        'results-background': result
    })