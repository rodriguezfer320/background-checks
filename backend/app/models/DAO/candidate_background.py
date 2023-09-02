from flask import json
from datetime import datetime
from ..entities import CandidateBackgroundModel
from ...database import db

class CandidateBackgroundDAO:

    @staticmethod
    def get_by_background_and_user_id(user_id, antecedent):
        return CandidateBackgroundModel.query\
                                             .filter(CandidateBackgroundModel.candidate_id == user_id)\
                                             .filter(CandidateBackgroundModel.background_id == antecedent)\
                                             .first()
    
    @staticmethod
    def save(data):
        candidate_background = CandidateBackgroundModel(
            candidate_id = data['document'],
            background_id = data['background'].id,
            description = json.dumps(data['description'])
        )
        db.session.add(candidate_background)
        db.session.commit()

    @staticmethod
    def put(data):
        candidate_background = CandidateBackgroundDAO.get_by_background_and_user_id(data['document'], data['background'].id)
        candidate_background.description = json.dumps(data['description'])
        candidate_background.updated_at = datetime.now()
        db.session.commit()