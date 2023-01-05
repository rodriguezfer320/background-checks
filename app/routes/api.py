from flask import Blueprint

from ..models.driver import Driver
from ..models.judicial_background import JudicialBackground
from ..models.fiscal_background import FiscalBackground

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
    '''

    background = FiscalBackground()
    background.driver = driver
    background.data = {
        'url': 'https://www.contraloria.gov.co/web/guest/persona-natural',
        'cedula': '1118310093',
        'tipo-documento': 'CC'
    }
    background.search_for_background()

    return background.to_json()