from ..controllers import verificationRequestBlueprint, VerificationRequestController

# ruta GET, para obtener todas las solicitudes de verificación
verificationRequestBlueprint.add_url_rule(
    rule='', 
    view_func=VerificationRequestController.get_all, 
    methods=['GET']
)
# ruta GET, para obtener el documento de una solicitud de verificación
verificationRequestBlueprint.add_url_rule(
    rule='/file/<int:id>', 
    view_func=VerificationRequestController.get_file, 
    methods=['GET']
)
# ruta POST, para crear una solicitud de verificación
verificationRequestBlueprint.add_url_rule(
    rule='/crear', 
    view_func=VerificationRequestController.create, 
    methods=['POST']
)
# ruta PUT, para actualizar los datos de una solicitud de verificación
verificationRequestBlueprint.add_url_rule(
    rule='/editar-datos/<int:id>', 
    view_func=VerificationRequestController.update_data, 
    methods=['PUT']
)
# ruta PUT, para actualizar el estado de una solicitud de verificación
verificationRequestBlueprint.add_url_rule(
    rule='/editar-estado/<int:id>', 
    view_func=VerificationRequestController.update_state, 
    methods=['PUT']
)
# ruta PUT, para actualizar el documento de una solicitud de verificación
verificationRequestBlueprint.add_url_rule(
    rule='/editar-documento/<int:id>', 
    view_func=VerificationRequestController.update_document, 
    methods=['PUT']
)

# se devuelve el blueprint que controla las rutas de verification-request
def get_verification_request_blueprint():
    return verificationRequestBlueprint