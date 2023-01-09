from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json

from ..request.request_background_check import request_background_check
from ..models.driver import Driver
from ..models.disciplinary_background import DisciplinaryBackground
from ..models.fiscal_background import FiscalBackground
from ..models.judicial_background import JudicialBackground
from ..models.corrective_action_background import CorrectiveActionBackground
from ..models.military_situation_background import MilitarySituationBackground
from ..models.traffic_infraction_background import TrafficInfractionBackground

api_scope = Blueprint('api', __name__)

@api_scope.route('verificacion-antecedentes', methods=('GET',))
@expects_json(request_background_check)
def background_check():
    request_data = request.get_json()
    antecedents = {
        'disciplinary': {
            'object': DisciplinaryBackground(),
            'data': {
                'url': 'https://www.procuraduria.gov.co/Pages/Generacion-de-antecedentes.aspx',
                'cedula': request_data['document'],
                'tipo-documento': '1'
            }
        },
        'fiscal': {
            'object': FiscalBackground(),
            'data': {
                'url': 'https://www.contraloria.gov.co/web/guest/persona-natural',
                'cedula': request_data['document'],
                'tipo-documento': 'CC'
            }
        },
        'judicial': {
            'object': JudicialBackground(),
            'data': {
                'url': 'https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml',
                'cedula': request_data['document'],
                'tipo-documento': 'cc'
            }
        },
        'corrective-actions': {
            'object': CorrectiveActionBackground(),
            'data': {
                'url': 'https://srvcnpc.policia.gov.co/PSC/frm_cnp_consulta.aspx',
                'cedula': request_data['document'],
                'tipo-documento': '55',
                'fecha-expedicion': '08/08/2017'
            }
        },
        'military-situation': {
            'object': MilitarySituationBackground(),
            'data': {
                'url': 'https://www.libretamilitar.mil.co/Modules/Consult/MilitarySituation',
                'cedula': request_data['document'], #'98073060443'
                'tipo-documento': '100000001' #'100000000'
            }
        },
        'traffic-infraction': {
            'object': TrafficInfractionBackground(),
            'data': {
                'url': 'http://www2.simit.org.co/Simit/verificar/contenido_verificar_pago_linea.jsp',
                'cedula': request_data['document'],
                'tipo-documento': '1'
            }
        }
    }

    driver = Driver()
    driver.load_options()

    result = {}

    for background in request_data['antecedents']:
        _background = antecedents[background]['object']
        _background.driver = driver
        _background.search_for_background(antecedents[background]['data'])
        result[background] = _background.text

    return jsonify({
        'results-background': result
    })    