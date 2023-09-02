from ..controllers import backgroundBlueprint, BackgroundController

# ruta GET, para obtener todas las verificaciones que proporciona la aplicación
backgroundBlueprint.add_url_rule(
    rule='', 
    view_func=BackgroundController.get_all, 
    methods=['GET']
)

# se devuelve el blueprint que controla las rutas de background
def get_background_blueprint():
    return backgroundBlueprint