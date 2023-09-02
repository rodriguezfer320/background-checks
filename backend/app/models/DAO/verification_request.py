from sqlalchemy.sql.expression import cast
from sqlalchemy import String
from datetime import datetime
from ..entities import VerificationRequestModel
from ...database import db
from ...utils import State, Role

class VerificationRequestDAO:
    
    @staticmethod
    def get_all(data):
        # se forma la query de la consulta
        query = VerificationRequestModel.query

        # consulta para el rol de candiato
        if data['token_data']['role'] == Role.CANDIDATE.value:
            # se aplica el filtro por id del candiato
            query = query.filter(VerificationRequestModel.user_sub_key == data['token_data']['sub_key'])

            # se aplica el filtro de busqueda por id de la solicitud
            if data['search']:
                query = query.filter(cast(VerificationRequestModel.id, String).like(data['search']))

        # consulta para el rol de funcionario
        elif data['search']:
            # se aplica el filtro de busqueda por id de la solicitud o del candiato
            query = query.filter(cast(VerificationRequestModel.id, String).like(data['search']) |
                                 cast(VerificationRequestModel.candidate_id, String).like(data['search']))

        # se aplica el filtro por estado
        if data['state'] != State.ALL.value:
            query = query.filter(VerificationRequestModel.state == data['state'])
        
        # se devuelven los datos obtenidos con paginación
        return db.paginate(query.order_by(VerificationRequestModel.id), page=data['page'], per_page=10, error_out=False)

    @staticmethod
    def get(id):
        return db.session.get(VerificationRequestModel, id)

    @staticmethod
    def get_by_background_and_user_id(user_id, antecedent_id):
        return VerificationRequestModel.query\
                                              .filter((cast(VerificationRequestModel.candidate_id, String) == str(user_id)) |
                                                      (VerificationRequestModel.user_sub_key == str(user_id)))\
                                              .filter(VerificationRequestModel.background_id == antecedent_id)\
                                              .first()
    
    @staticmethod
    def save(data):
        verification_request = VerificationRequestDAO.get_by_background_and_user_id(data['token_data']['sub_key'], data['antecedent'])

        if verification_request is None:
            verification_request = VerificationRequestModel(
                user_sub_key = data['token_data']['sub_key'],
                background_id = data['antecedent'],
                title = data['title'].strip(),
                candidate_id = data['document'].strip(),
                comment = 'N/A',
                state=State.PENDING.value
            )
            db.session.add(verification_request)
            db.session.commit()
            return verification_request
        
        return None

    @staticmethod
    def put_data(data, id):
        verification_request = VerificationRequestDAO.get(id)
        
        if verification_request:
            # se actualizan los datos
            verification_request.title = data['title'].strip()
            verification_request.candiate_id = data['document']
            verification_request.updated_at = datetime.now()
            db.session.commit()
        
        return verification_request

    @staticmethod
    def put_state(data, id):
        verification_request = VerificationRequestDAO.get(id)
        
        if verification_request:
            # se actualizan los datos
            verification_request.comment = data['comment'].strip()
            verification_request.state = data['state']
            verification_request.updated_at = datetime.now()
            db.session.commit()
        
        return verification_request

    @staticmethod
    def put_document(id):
        verification_request = VerificationRequestDAO.get(id)
        
        if verification_request and verification_request.state == State.DENIED.value:
            # se actualizan los datos
            verification_request.state = State.CORRECTED.value
            verification_request.updated_at = datetime.now()
            db.session.commit()             
    
        return verification_request

    @staticmethod
    def delete(id):
        verification_request = VerificationRequestDAO.get(id)
        db.session.delete(verification_request)
        db.session.commit()