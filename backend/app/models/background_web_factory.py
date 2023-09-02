from .driver import Driver
from .disciplinary_background import DisciplinaryBackground
from .fiscal_background import FiscalBackground
from .judicial_background import JudicialBackground
from .corrective_action_background import CorrectiveActionBackground
from .military_situation_background import MilitarySituationBackground
from .traffic_infraction_background import TrafficInfractionBackground
from ..utils import BackgroundWeb

class BackgroundWebFactory:

    def __init__(self, description):
        self._driver = Driver()
        self._driver.load_options()
        self._description = description

    def create_background(self, antecedent):
        ant = None

        if antecedent == BackgroundWeb.DB.value:
            ant = DisciplinaryBackground(self._driver, self._description)
        elif antecedent == BackgroundWeb.FB.value:
            ant = FiscalBackground(self._driver, self._description)
        elif antecedent == BackgroundWeb.JB.value:
            ant = JudicialBackground(self._driver, self._description)
        elif antecedent == BackgroundWeb.CAB.value:
            ant = CorrectiveActionBackground(self._driver, self._description)
        elif antecedent == BackgroundWeb.MSB.value:
            ant = MilitarySituationBackground(self._driver, self._description)
        elif antecedent == BackgroundWeb.TIB.value:
            ant = TrafficInfractionBackground(self._driver, self._description)

        return ant