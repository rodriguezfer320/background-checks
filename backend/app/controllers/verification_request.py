from flask import request
from flask_smorest import Blueprint, abort
from ..models import (
    ForbiddenException, NotFoundException, FileSaveException, File, 
    VerificationRequestDAO, VerificationRequestArgsSchema, VerificationRequestPostSchema, 
    VerificationRequestPutDataSchema, VerificationRequestPutStateSchema, VerificationRequestFileSchema
)
from ..auth import authentication_required_and_permissions
from ..utils import Role, State
from ..auth import _verify_token

verificationRequestBlueprint = Blueprint('verification_request', __name__)

class VerificationRequestController:
    
    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.CANDIDATE.value, Role.OFFICER.value])
    @verificationRequestBlueprint.arguments(VerificationRequestArgsSchema, location='query')
    @verificationRequestBlueprint.response(200)
    def get_all(args):
        try:
            token = request.headers.get('Authorization').split()[1]
            args['token_data'] = _verify_token(token)
            verification_requests = VerificationRequestDAO.get_all(args)
            return {
                'data': [vr.to_dict() for vr in verification_requests.items],
                'pagination': {
                    'first': verification_requests.first,
                    'last': verification_requests.last,
                    'total': verification_requests.total,
                    'prev_page': verification_requests.prev_num,
                    'next_page': verification_requests.next_num,
                    'current_page': verification_requests.page,
                    'pages': [page for page in verification_requests.iter_pages()]
                }
            }
        except:
            abort(500, message='Ocurrió un error inesperado al obtener las solicitudes de verificación')

    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.COMPANY.value, Role.CANDIDATE.value, Role.OFFICER.value])
    @verificationRequestBlueprint.response(200)
    def get_file(id):
        try:
            verification_request = VerificationRequestDAO.get(id)

            if verification_request:
                filename = verification_request.user_sub_key + '_' + str(verification_request.background_id) + '_' + verification_request.background.name
                return File.get(filename)

            raise NotFoundException
        except NotFoundException:
            abort(404, message=f'No se pudo obtener el documento de la solicitud debido a que no se encontró una solicitud asociada al ID: {id}')
        except FileNotFoundError:
            abort(404, message='No se encontró el documento de la solicitud')
        except:
            abort(500, message='Ocurrió un error inesperado al obtener el documento de la solicitud')

    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.CANDIDATE.value])
    @verificationRequestBlueprint.arguments(VerificationRequestPostSchema, location='form')
    @verificationRequestBlueprint.response(201)
    def create(form):
        try:
            # se crea la instancia de la solicitud
            token = request.headers.get('Authorization').split()[1]
            form['token_data'] = _verify_token(token)
            verification_request = VerificationRequestDAO.save(form)

            if verification_request:
                # se guarda el archivo en una ubicación del servidor
                filename = verification_request.user_sub_key + '_' + str(verification_request.background_id) + '_' + verification_request.background.name
                
                try:
                    File.save(form['file_document'], filename)
                    return {'message': 'La solicitud se ha creado correctamente'}
                except:
                    VerificationRequestDAO.delete(verification_request.id)
                    raise FileSaveException

            raise ForbiddenException
        except FileSaveException:
            abort(400, message='No se pudo crear la solicitud debido a que ocurrio un error al guardar el documento de la solicitud')
        except ForbiddenException:
            abort(403, message='No se pudo crear la solicitud debido a que solo se puede crear una solicitud por tipo de antecedente')
        except:
            abort(500, message='Ocurrió un error inesperado al crear la solicitud')
    
    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.CANDIDATE.value])
    @verificationRequestBlueprint.arguments(VerificationRequestPutDataSchema, location='json')
    @verificationRequestBlueprint.response(201)
    def update_data(json, id):
        try:
            if VerificationRequestDAO.put_data(json, id): return {'message': 'Los datos de la solicitud se han actualizado correctamente'}
            raise NotFoundException
        except NotFoundException:
            abort(404, message=f'No se pudo actualizar los datos de la solicitud debido a que no se encontró una solicitud asociada al ID: {id}')
        except:
            abort(500, message='Ocurrió un error inespareado al actualizar los datos de la solicitud')

    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.OFFICER.value])
    @verificationRequestBlueprint.arguments(VerificationRequestPutStateSchema, location='json')
    @verificationRequestBlueprint.response(201)
    def update_state(json, id):
        try:
            if VerificationRequestDAO.put_state(json, id): return {'message': 'El estado de la solicitud se ha actualizado correctamente'}
            raise NotFoundException
        except NotFoundException:
            abort(404, message=f'No se pudo actualizar el estado de la solicitud debido a que no se encontró una solicitud asociada al ID: {id}')
        except:
            abort(500, message='Ocurrió un error inespareado al actualizar el estado de la solicitud')
    
    @staticmethod
    @authentication_required_and_permissions(allowedRoles=[Role.CANDIDATE.value])
    @verificationRequestBlueprint.arguments(VerificationRequestFileSchema, location='files')
    @verificationRequestBlueprint.response(201)
    def update_document(files, id):
        try:
            verification_request = VerificationRequestDAO.put_document(id)

            if verification_request:
                if verification_request.state == State.CORRECTED.value:
                    # se guarda el archivo en una ubicación del servidor
                    filename = verification_request.user_sub_key + '_' + str(verification_request.background_id) + '_' + verification_request.background.name
                    try:
                        File.save(files['file_document'], filename)
                        return {'message': 'El documento de la solicitud se ha actualizado correctamente'}
                    except:
                        VerificationRequestDAO.put_state({'comment': verification_request.comment, 'state': State.DENIED.value}, verification_request.id)
                        raise FileSaveException
            
                raise ForbiddenException            
            raise NotFoundException
        except FileSaveException:
            abort(400, message='No se pudo actualizar el documento de la solicitud debido a que ocurrio un error al guardar el docuemento')
        except ForbiddenException:
            abort(403, message=f'No se pudo actualizar el documento de la solicitud debido a que su estado debe ser rechazada')
        except NotFoundException:
            abort(404, message=f'No se pudo actualizar el documento de la solicitud debido a que no se encontró una solicitud asociada al ID: {id}')
        except:
            abort(500, message='Ocurrió un error inesperado al actualizar el documento de la solicitud')