from flask import Blueprint
from . import get_background_check_blueprint, get_background_blueprint, get_verification_request_blueprint

# se registran las rutas en la api
api = Blueprint('api', __name__, url_prefix='/fs-uv/bc/api/')
api.register_blueprint(get_background_check_blueprint(), url_prefix='verificacion-antecedentes')
api.register_blueprint(get_background_blueprint(), url_prefix='antecedentes')
api.register_blueprint(get_verification_request_blueprint(), url_prefix='verificacion-solicitud')