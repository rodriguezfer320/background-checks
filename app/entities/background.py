from app.models.database_connection import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

class Background(Base):
    __tablename__ = 'background'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    url = Column(String, default='N/A')
    type = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    candidate_background = relationship('CandidateBackground', back_populates='background')
    verification_request_background = relationship('VerificationRequest', back_populates='background')

    def __init__(self, name, url, type):
        self.name = name
        self.url = url
        self.type = type

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'type': self.type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }