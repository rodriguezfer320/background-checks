from app.models.database_connection import Base
from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

class CandidateBackground(Base):
    __tablename__ = 'candidate_background'
    candidate_id = Column(Integer, primary_key=True)
    background_id = Column(Integer, ForeignKey('background.id'), primary_key=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    background = relationship('Background', back_populates='candidate_background')

    def __init__(self, candidate_id, background_id, description):
        self.candidate_id = candidate_id
        self.background_id = background_id
        self.description = description

    def to_json(self):
        return {
            'candidate_id': self.candidate_id,
            'background_id': self.background_id,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }