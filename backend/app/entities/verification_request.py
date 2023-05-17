from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, text, inspect
from sqlalchemy.orm import relationship
from ..database import db

class VerificationRequestModel(db.Model):
    __tablename__ = 'verification_request'
    id = Column(Integer, autoincrement=True, primary_key=True)
    background_id = Column(Integer, ForeignKey('background.id'))
    title = Column(String, nullable=False)
    candidate_id = Column(Integer, nullable=False)
    comment = Column(String, default='N/A')
    state = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    background = relationship('BackgroundModel', back_populates='candidate_verification_request')

    def __init__(self, background_id, title, candidate_id, comment, state):
        self.background_id = background_id
        self.title = title
        self.candidate_id = candidate_id
        self.comment = comment
        self.state = state

    def to_json(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}