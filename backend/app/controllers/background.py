from flask_smorest import Blueprint, abort
from ..models import BackgroundDAO, BackgroundArgsSchema
from ..auth import authentication_required_and_permissions
from ..utils import Role

backgroundBlueprint = Blueprint('background', __name__)

class BackgroundController:
    
    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.COMPANY.value, Role.CANDIDATE.value, Role.OFFICER.value])
    @backgroundBlueprint.arguments(BackgroundArgsSchema, location='query')
    @backgroundBlueprint.response(200)
    def get_all(args):
        try:
            antecedents = BackgroundDAO.get_all(args)
            antecedents = [ant.to_dict() for ant in antecedents] # se parsean los datos a un diccionario
            return antecedents
        except:
            abort(500, message='Ocurrió un error inesperado al obtener los antecedentes')