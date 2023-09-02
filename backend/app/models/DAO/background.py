from ..entities import BackgroundModel
from ...database import db

class BackgroundDAO:
    
    @staticmethod
    def get_all(data):
        # se forma el query de la consulta
        query = BackgroundModel.query

        # se aplica el filtro por tipo
        if data['type']:
            query = query.filter(BackgroundModel.type == data['type'])
        
        # se devuelven todos los antecedentes  
        return query.all()

    @staticmethod
    def get(id):
        return db.session.get(BackgroundModel, id)