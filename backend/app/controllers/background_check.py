from flask_smorest import Blueprint, abort
from ..models import (
    BackgroundContext, BackgroundWebStrategy, BackgroundNoWebStrategy, 
    BackgroundDAO, BackgroundCheckArgsSchema, User, UserNotFoundException
)
from ..auth import authentication_required_and_permissions
from ..utils import Role, TYPEWEB

backgroundCheckBlueprint = Blueprint('background-check', __name__)

class BackgroundCheckController:

    @authentication_required_and_permissions(allowedRoles=[Role.COMPANY.value])
    @backgroundCheckBlueprint.arguments(BackgroundCheckArgsSchema, location='query')
    @backgroundCheckBlueprint.response(200)
    def get(args):
        try:
            # se verifica que el documento del candidato ingresado se encuentre registrado en la aplicación
            data = User.get_by_document(args['document'])

            if data:
                context = BackgroundContext()
                antecedents = []

                for ant in args['antecedents']:
                    # se consultan los datos del antecedente
                    background = BackgroundDAO.get(ant)
                    
                    # se establece la estrategia a aplicar para obtener los antecedentes según el tipo
                    context.strategy = BackgroundWebStrategy() if background.type == TYPEWEB else BackgroundNoWebStrategy()
                    
                    # se obtiene la información del antecedente
                    result = context.search_for_background({
                        'document': args['document'],
                        'user_sub_key': data['sub_key'],
                        'date-expedition': data['issue_date'],
                        'background': background
                    })

                    # se añade la información del antecedente a la lista
                    antecedents.append(result)            

                return antecedents

            raise UserNotFoundException
        except UserNotFoundException:
            abort(404, message='El candidato no ha actualizado su información o el documento ingresado no pertenece aún candiato registrado')
        except:
            abort(500, message='Ocurrió un error inesperado al obtener los antecedentes del candidato')