from flask import jsonify, views
from flask_smorest import Blueprint
from ..entities import BackgroundModel
from ..schemas import BackgroundArgsSchema
from ..auth import authentication_required_and_permissions
from ..utils import ROLES

bg = Blueprint('background', __name__)

class BackgroundController(views.MethodView):

    def __init__(self):
        super().__init__()

    @authentication_required_and_permissions(allowedRoles=[ROLES['candidate'], ROLES['company'], ROLES['officer']])
    @bg.arguments(BackgroundArgsSchema, location='query')
    def get(self, args):
        # se forma el query de la consulta
        query = BackgroundModel.query

        # se aplica el filtro por tipo
        if args['type']:
            query = query.filter(BackgroundModel.type == args['type'])

        # se obtienen los datos y se parsean a json
        antecedents = [ant.to_json() for ant in query.all()]

        return jsonify({
            'code': 200,
            'status': 'SUCCESS',
            'data': antecedents
        }), 200  