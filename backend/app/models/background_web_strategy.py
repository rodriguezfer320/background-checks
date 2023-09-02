from flask import json
from datetime import datetime
from .background_strategy import BackgroundStrategy
from .DAO import CandidateBackgroundDAO
from .background_web_factory import BackgroundWebFactory

class BackgroundWebStrategy(BackgroundStrategy):

    def __init__(self):
        super().__init__()
        self._background_web_factory = BackgroundWebFactory(self._description)

    def get_background_information(self, data):
        antecedent = None

        try:
            # se consulta la información del antecedente asociado al candidato en la BD
            candidate_background = CandidateBackgroundDAO.get_by_background_and_user_id(data['document'], data['background'].id)
            days = 1

            # si el antecedente ya ha sido consultado, se verifica si han pasado 24h desde que se actualizó su información 
            if candidate_background:
                diff = datetime.now() - candidate_background.updated_at
                days = diff.days

            # si han pasado 24h, se consulta el antecedente en la web
            if days >= 1:
                # se consulta la información del antecedente en la web correspondiente
                antecedent = self._background_web_factory.create_background(data['background'].name)                
                antecedent.get_background_information(data)
                antecedent.process_information(data)
                data['description'] = antecedent.description
                
                # se guarda o actualiza la información del antecedente
                CandidateBackgroundDAO.save(data)  if candidate_background is None else CandidateBackgroundDAO.put(data)
            else:
                data['description'] = json.loads(candidate_background.description)
        except:
            if antecedent: antecedent.driver.close_browser()
            data['description'] = self._description
            data['description']['message'] = self._message_error

        return data['description']