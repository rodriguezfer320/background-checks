from flask import Blueprint
from ..controllers import (
    bc, BackgroundCheckController,
    bg, BackgroundController,
    vg, VerificationRequestController
)

# se definen las rutas para background_check
controllerBC = BackgroundCheckController()
bc.add_url_rule(rule='', view_func=controllerBC.get, methods=['GET'])

# se definen las rutas para background
controllerBG = BackgroundController()
bg.add_url_rule(rule='', view_func=controllerBG.get, methods=['GET'])

# se definen las rutas para verification_requets
controllerVG = VerificationRequestController()
vg.add_url_rule(rule='', view_func=controllerVG.get, methods=['GET'])
vg.add_url_rule(rule='/file/<int:id>', view_func=controllerVG.get_file, methods=['GET'])
vg.add_url_rule(rule='/crear', view_func=controllerVG.create, methods=['POST'])
vg.add_url_rule(rule='/editar-datos/<int:id>', view_func=controllerVG.update_data, methods=['PUT'])
vg.add_url_rule(rule='/editar-estado/<int:id>', view_func=controllerVG.update_state, methods=['PUT'])
vg.add_url_rule(rule='/editar-documento/<int:id>', view_func=controllerVG.update_document, methods=['PUT'])

# se registran las rutas en la api
api = Blueprint('api', __name__, url_prefix='/fs-uv/bc/api/')
api.register_blueprint(bc, url_prefix='verificacion-antecedentes')
api.register_blueprint(bg, url_prefix='antecedentes')
api.register_blueprint(vg, url_prefix='verificacion-solicitud')