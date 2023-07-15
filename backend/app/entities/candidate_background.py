from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, text, inspect
from sqlalchemy.orm import relationship
from ..database import db

class CandidateBackgroundModel(db.Model):
    __tablename__ = 'candidate_background'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    candidate_id = Column(Integer, primary_key=True)
    background_id = Column(Integer, ForeignKey('background.id'), primary_key=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    background = relationship('BackgroundModel', back_populates='candidate_background')

    def __init__(self, candidate_id, background_id, description):
        self.candidate_id = candidate_id
        self.background_id = background_id
        self.description = description

    def to_json(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}