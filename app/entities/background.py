from app.models.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

class Background(Base):
    __tablename__ = 'background'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    type = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    candidate_background = relationship('CandidateBackground', back_populates='background')

    def __init__(self, name, type):
        self._name = name
        self._type = type

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }