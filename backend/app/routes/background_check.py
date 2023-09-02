from ..controllers import backgroundCheckBlueprint, BackgroundCheckController

# ruta GET, para obtener los antecedentes de un candidato
backgroundCheckBlueprint.add_url_rule(
    rule='', 
    view_func=BackgroundCheckController.get, 
    methods=['GET']
)

# se devuelve el blueprint que controla las rutas de background-check
def get_background_check_blueprint():
    return backgroundCheckBlueprint