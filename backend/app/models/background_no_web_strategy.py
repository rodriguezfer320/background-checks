from .background_strategy import BackgroundStrategy
from .DAO import VerificationRequestDAO
from ..utils import BackgroundNoWeb, State

class BackgroundNoWebStrategy(BackgroundStrategy):

    def get_background_information(self, data):
        try:
            verification_request = VerificationRequestDAO.get_by_background_and_user_id(data['user_sub_key'], data['background'].id)

            if data['background'].name == BackgroundNoWeb.UD.value:
                if verification_request is None or verification_request.state != State.APPROVED.value:
                    self._description['message'] = 'El candidato no ha cargado su título académico o esta en proceso de validación.'
                else:
                    self._description['message'] = verification_request.comment
                    self._description['link'] = f'/verificacion-solicitud/file/{verification_request.id}'
        except:
            self._description['message'] = self._message_error
        
        return self._description