from sqlalchemy import Column, Integer, String, TIMESTAMP, text, inspect
from sqlalchemy.orm import relationship
from ...database import db

class BackgroundModel(db.Model):
    __tablename__ = 'background'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    url = Column(String, default='N/A')
    type = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    candidate_background = relationship('CandidateBackgroundModel', back_populates='background')
    candidate_verification_request = relationship('VerificationRequestModel', back_populates='background')

    def __init__(self, name, url, type):
        self.name = name
        self.url = url
        self.type = type

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}