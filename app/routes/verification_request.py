from flask import jsonify, request
from flask_smorest import Blueprint
from os import getcwd
from math import ceil
from datetime import datetime
from app.models.database_connection import session
from app.entities.verification_request import VerificationRequest
from app.schemas.verification_request_schema import PostDataSchema, FileSchema, PutDataSchema, PutStateSchema

bvr = Blueprint('verification_request', __name__, url_prefix='/api/verificacion-solicitud/', description='Operaciones de verificación de solicitud.')

@bvr.get('all')
def get_all():
    # filtros de búsqueda
    page = request.args.get('page', 1, type=int) - 1
    id = request.args.get('id', type=int)
    candidate_id = request.args.get('candidate_id', type=int)
    state = request.args.get('state', type=str)

    # otros datos
    LIMIT = 10
    count = session.query(VerificationRequest).count()
    count_page = ceil(count / LIMIT) - 1

    # se obtienen todas las solicitudes creadas, según los filtros aplicados
    query = session.query(VerificationRequest)
                                   
    if id is not None:
        query = query.filter(VerificationRequest.id == id)

    if candidate_id is not None:
       query = query.filter(VerificationRequest.candidate_id == candidate_id)

    if state is not None:
        query = query.filter(VerificationRequest.state == state)               
    
    verification_requests = query.limit(LIMIT)\
                                 .offset(page * LIMIT)\
                                 .all()
    
    # se parsea la información a json
    results = [vr.to_json() for vr in verification_requests]

    return jsonify({
        'verification_requests': results,
        'previous': None if page == 0 or len(results) == 0 else request.base_url + '?page={}'.format(page - 1),
        'next': None if page == count_page or len(results) == 0 else request.base_url + '?page={}'.format(page + 1),
    }), 200

@bvr.post('crear')
@bvr.arguments(PostDataSchema, location='form')
@bvr.arguments(FileSchema, location='files')
def add_verification_request(data, file):
    # se consulta si ya se ha registrado la solicitud para ese antecedente
    verification_request = session.query(VerificationRequest)\
                                  .filter(VerificationRequest.background_id == data['background_id'])\
                                  .filter(VerificationRequest.candidate_id == data['candidate_id'])\
                                  .first()

    if verification_request is None:
        # se crea la instancia de la solicitud
        verification_request = VerificationRequest(
            background_id = data['background_id'],
            title = data['title'],
            candidate_id = data['candidate_id'],
            comment = 'N/A',
            state = 'pendiente'
        )

        # se guardan los datos en la BD
        session.add(verification_request)
        session.commit()
        
        # se guarda el archivo en una ubicación del servidor
        filename = str(verification_request.background_id) + '_' + str(verification_request.candidate_id) + '_' + verification_request.background.name
        document_path = getcwd() + '\\app\\static\\verification_request_files\\{}.pdf'.format(filename)
        file['document'].save(document_path)

        return jsonify({'message': 'La solicitud se ha creado correctamente.'}), 201
    else:
        return jsonify({'message': 'Solo se puede crear una solicitud por antecedente.'}), 400

@bvr.put('editar-datos/<int:id>')
@bvr.arguments(PutDataSchema, location='form')
def update_data(data, id):
    # se consulta una solicitud especifica creada por un candidato
    verification_request = session.query(VerificationRequest).get(id)
    
    verification_request.title = data['title']
    verification_request.candiate_id = data['candidate_id']
    verification_request.updated_at = datetime.now()

    # se actualizan los datos en la BD
    session.commit()

    return jsonify({'message': 'Los datos de la solicitud se han actualizado correctamente.'}), 201

@bvr.put('editar-documento/<int:id>')
@bvr.arguments(FileSchema, location='files')
def update_document(file, id):
    # se consulta una solicitud especifica creada por un candidato
    verification_request = session.query(VerificationRequest).get(id)

    if verification_request.state == 'rechazada':
        # se actualizan los datos en la BD
        verification_request.state = 'corregida'
        verification_request.updated_at = datetime.now()
        session.commit()

        # se guarda el archivo en una ubicación del servidor
        filename = str(verification_request.background_id) + '_' + str(verification_request.candidate_id) + '_' + verification_request.background.name
        document_path = getcwd() + '\\app\\static\\verification_request_files\\{}.pdf'.format(filename)
        file['document'].save(document_path)

        return jsonify({'message': 'El documento de la solicitud se ha actualizado correctamente.'}), 201
    else: 
        return jsonify({'message': 'El documento de la solicitud solo se puede actualizar cuando el estado sea rechazada.'}), 400

@bvr.put('editar-estado/<int:id>')
@bvr.arguments(PutStateSchema, location='form')
def update_state(data, id):
    # se consulta una solicitud especifica creada por un candidato
    verification_request = session.query(VerificationRequest).get(id)
    verification_request.comment = data['comment']
    verification_request.state = data['state']
    verification_request.updated_at = datetime.now()

    # se actualizan los datos en la BD
    session.commit()

    return jsonify({'message': 'El estado de la solicitud se ha actualizado correctamente.'}), 201