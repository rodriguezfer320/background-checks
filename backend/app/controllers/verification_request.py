from flask import jsonify, views, send_file, request
from flask_smorest import Blueprint
from sqlalchemy.sql.expression import cast
from sqlalchemy import String
from os import getcwd
from datetime import datetime
from ..entities import VerificationRequestModel
from ..schemas import (VerificationRequestArgsSchema, VerificationRequestPostSchema, VerificationRequestPutDataSchema,
                       VerificationRequestPutStateSchema, VerificationRequestFileSchema)
from ..database import db
from ..auth import authentication_required_and_permissions
from ..utils import ROLES

vg = Blueprint('verification_request', __name__)

class VerificationRequestController(views.MethodView):

    def __init__(self):
        super().__init__()
        self.dir_file = getcwd() + r'/app/static/verification_request_files/{filename}.pdf'
        self.states = ('todos', 'pendiente', 'rechazada', 'corregida', 'aprobada')

    @authentication_required_and_permissions(allowedRoles=[ROLES['candidate'], ROLES['officer']])
    @vg.arguments(VerificationRequestArgsSchema, location='query')
    def get(self, args):
        # se forma la query de la consulta
        query = VerificationRequestModel.query

        # se aplica el filtro por documento
        if args['user_sub_key']:
            query = query.filter(VerificationRequestModel.user_sub_key == args['user_sub_key'])

            # se aplica el filtro de busqueda por id
            if args['search']:
                query = query.filter(cast(VerificationRequestModel.id, String).like(args['search']))

        # se aplica el filtro de busqueda por id o documento
        elif args['search']:
            query = query.filter(cast(VerificationRequestModel.id, String).like(args['search']) |
                                 cast(VerificationRequestModel.candidate_id, String).like(args['search']))

        # se aplica el filtro por estado
        if args['state'] != self.states[0]:
            query = query.filter(VerificationRequestModel.state == args['state'])            

        verification_requests = db.paginate(query.order_by(VerificationRequestModel.id), page=args['page'], per_page=10, error_out=False)

        return jsonify({
            'code': 200,
            'status': 'SUCCESS',
            'data': [vr.to_json() for vr in verification_requests.items],
            'pagination': {
                'first': verification_requests.first,
                'last': verification_requests.last,
                'total': verification_requests.total,
                'prev_page': verification_requests.prev_num,
                'next_page': verification_requests.next_num,
                'current_page': verification_requests.page,
                'pages': [page for page in verification_requests.iter_pages()]
            }
        }), 200

    @authentication_required_and_permissions(allowedRoles=[ROLES['candidate'], ROLES['company'], ROLES['officer']])
    def get_file(self, id):
        verification_request = db.session.get(VerificationRequestModel, id)

        if verification_request:
            try:
                filename = str(verification_request.user_sub_key) + '_' + str(verification_request.background_id) + '_' + verification_request.background.name
                return send_file(self.dir_file.format(filename=filename))
            except FileNotFoundError:
                return jsonify({
                    'code': 400,
                    'status': 'FAILD',
                    'message': 'No se pudo obtener el archivo.'
                }), 400
        else:
            return jsonify({
                'code': 404,
                'status': 'VERIFICATION REQUEST NOT FOUND',
                'message': 'No se encontró una solicitud de verificación.'
            }), 404

    @authentication_required_and_permissions(allowedRoles=[ROLES['candidate']])
    @vg.arguments(VerificationRequestPostSchema, location='form')
    def create(self, form):
        # se consulta si ya se ha registrado la solicitud para ese antecedente
        verification_request = VerificationRequestModel.query\
                                                       .filter(VerificationRequestModel.user_sub_key == form['user_sub_key'])\
                                                       .filter(VerificationRequestModel.background_id == form['antecedent'])\
                                                       .first()
        if verification_request is None:
            # se crea la instancia de la solicitud
            verification_request = VerificationRequestModel(
                user_sub_key=form['user_sub_key'],
                background_id=form['antecedent'],
                title=form['title'].strip(),
                candidate_id=form['document'].strip(),
                comment='N/A',
                state=self.states[1]
            )

            # se guardan los datos en la BD
            db.session.add(verification_request)
            db.session.commit()

            # se guarda el archivo en una ubicación del servidor
            filename = str(verification_request.user_sub_key) + '_' + str(verification_request.background_id) + '_' + verification_request.background.name
            form['file_document'].save(self.dir_file.format(filename=filename))

            return jsonify({
                'code': 201,
                'status': 'SUCCESS',
                'message': 'La solicitud se ha creado correctamente.'
            }), 201
        else:
            return jsonify({
                'code': 400,
                'status': 'FAILD',
                'message': 'Solo se puede crear una solicitud por tipo de antecedente.'
            }), 400

    @authentication_required_and_permissions(allowedRoles=[ROLES['candidate']])
    @vg.arguments(VerificationRequestPutDataSchema, location='json')
    def update_data(self, data, id):
        # se consulta una solicitud especifica creada por un candidato
        verification_request = db.session.get(VerificationRequestModel, id)
        if verification_request:
            # se asiganan los nuevos datos
            verification_request.title = data['title'].strip()
            verification_request.candiate_id = data['document']
            verification_request.updated_at = datetime.now()

            # se actualizan los datos en la BD
            db.session.commit()

            return jsonify({
                'code': 201,
                'status': 'SUCCESS',
                'message': 'Los datos de la solicitud se han actualizado correctamente.'
            }), 201
        else:
            return jsonify({
                'code': 404,
                'status': 'VERIFICATION REQUEST NOT FOUND',
                'message': 'No se encontró una solicitud de verificación.'
            }), 404

    @authentication_required_and_permissions(allowedRoles=[ROLES['officer']])
    @vg.arguments(VerificationRequestPutStateSchema, location='json')
    def update_state(self, data, id):
        # se consulta una solicitud especifica creada por un candidato
        verification_request = db.session.get(VerificationRequestModel, id)

        if verification_request:
            # se asiganan los nuevos datos
            verification_request.comment = data['comment'].strip()
            verification_request.state = data['state']
            verification_request.updated_at = datetime.now()

            # se actualizan los datos en la BD
            db.session.commit()

            return jsonify({
                'code': 201,
                'status': 'SUCCESS',
                'message': 'El estado de la solicitud se ha actualizado correctamente.'
            }), 201
        else:
            return jsonify({
                'code': 404,
                'status': 'VERIFICATION REQUEST NOT FOUND',
                'message': 'No se encontró una solicitud de verificación.'
            }), 404

    @authentication_required_and_permissions(allowedRoles=[ROLES['candidate']])
    @vg.arguments(VerificationRequestFileSchema, location='files')
    def update_document(self, files, id):
        # se consulta una solicitud especifica creada por un candidato
        verification_request = db.session.get(VerificationRequestModel, id)

        if verification_request:
            if verification_request.state == self.states[2]:
                # se actualizan los datos en la BD
                verification_request.state = self.states[3]
                verification_request.updated_at = datetime.now()
                db.session.commit()

                # se guarda el archivo en una ubicación del servidor
                filename = str(verification_request.user_sub_key) + '_' + str(verification_request.background_id) + '_' + verification_request.background.name
                files['file_document'].save(self.dir_file.format(filename=filename))

                return jsonify({
                    'code': 201,
                    'status': 'SUCCESS',
                    'message': 'El documento de la solicitud se ha actualizado correctamente.'
                }), 201
            else:
                return jsonify({
                    'code': 400,
                    'status': 'FAILD',
                    'message': 'El documento de la solicitud solo se puede actualizar cuando el estado sea rechazada.'
                }), 400
        else:
            return jsonify({
                'code': 404,
                'status': 'VERIFICATION REQUEST NOT FOUND',
                'message': 'No se encontró una solicitud de verificación.'
            }), 404