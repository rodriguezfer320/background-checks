from app.models.database_connection import Base
from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

class VerificationRequest(Base):
    __tablename__ = 'verification_request'
    id = Column(Integer, autoincrement=True, primary_key=True)
    background_id = Column(Integer, ForeignKey('background.id'))
    title = Column(String, nullable=False)
    candidate_id = Column(Integer, nullable=False)
    comment = Column(String, default='N/A')
    state = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    background = relationship('Background', back_populates='verification_request_background')

    def __init__(self, background_id, title, candidate_id, comment, state):
        self.background_id = background_id
        self.title = title
        self.candidate_id = candidate_id
        self.comment = comment
        self.state = state

    def to_json(self):
        return {
            'id': self.id,
            'background_id': self.background_id,
            'title': self.title,
            'candidate_id': self.candidate_id,
            'comment': self.comment,
            'state': self.state,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }