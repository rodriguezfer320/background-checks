from flask import Blueprint

from ..models.driver import Driver
from ..models.judicial_background import JudicialBackground
from ..models.fiscal_background import FiscalBackground
from ..models.corrective_action_certificate import CorrectiveActionCertificate
from ..models.military_situation import MilitarySituation

api_scope = Blueprint('api', __name__)

@api_scope.route('verificacion-antecedentes', methods=('GET',))
def background_check():
    driver = Driver()
    driver.load_options()

    '''
    background = JudicialBackground()
    background.driver = driver
    background.data = {
        'url': 'https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml',
        'cedula': '1118310093',
        'tipo-documento': 'cc'
    }
    background.search_for_background()

    background = FiscalBackground()
    background.driver = driver
    background.data = {
        'url': 'https://www.contraloria.gov.co/web/guest/persona-natural',
        'cedula': '1118310093',
        'tipo-documento': 'CC'
    }
    background.search_for_background()

    background = CorrectiveActionCertificate()
    background.driver = driver
    background.data = {
        'url': 'https://srvcnpc.policia.gov.co/PSC/frm_cnp_consulta.aspx',
        'cedula': '1118310093',
        'tipo-documento': '55',
        'fecha-expedicion': '08/08/2017'
    }
    background.search_for_background()
    '''

    background = MilitarySituation()
    background.driver = driver
    background.data = {
        'url': 'https://www.libretamilitar.mil.co/Modules/Consult/MilitarySituation',
        'cedula': '98073060443',#'1118310093',
        'tipo-documento': '100000000'#'100000001'
    }
    background.search_for_background()

    return background.to_json()